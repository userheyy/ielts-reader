"""Batch-replace listening JSON timing data with MFA word/phone alignment.

The script builds one temporary MFA corpus and runs the Docker image once,
which is substantially faster than starting a container for every article.
MFA can merge/split clitics, compounds, and numbers, so the write-back step
uses a monotonic token mapping instead of requiring identical word counts.
"""

import argparse
import difflib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "listening"
MODEL_ID = "MontrealCorpusTools/english_mfa"
IMAGE = "mmcauliffe/montreal-forced-aligner:latest"
MFA_VOLUME = "mfa-models"
HF_VOLUME = "mfa-hf-cache"


def tokens(text):
    text = (text or "").replace("’", "'").replace("‘", "'")
    raw = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+", text)
    result = []
    for token in raw:
        result.extend(expand_token(token))
    return result


def expand_token(token):
    """Expand common clitics so source and MFA token streams are comparable."""
    token = str(token).replace("’", "'").replace("‘", "'")
    lower = token.lower()
    if lower in {"<unk>", "<eps>"}:
        return [lower]
    for suffix in ("'ll", "'re", "'ve", "n't", "'d", "'m", "'s", "'t"):
        if lower.endswith(suffix) and len(token) > len(suffix):
            return [token[: -len(suffix)], suffix]
    if lower.endswith("'") and len(token) > 1:
        return [token[:-1]]
    return [token]


def lab_text(text):
    text = (text or "").replace("’", "'").replace("‘", "'")
    text = re.sub(r"[^A-Za-z0-9' ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def leading_trim_offset(source, padding=2.0, threshold=5.0):
    starts = []
    for segment in source.get("segments", []):
        try:
            value = float(segment.get("start"))
        except (TypeError, ValueError):
            continue
        if value >= 0:
            starts.append(value)
    if not starts or min(starts) <= threshold:
        return 0.0
    return max(0.0, min(starts) - padding)


def shift_alignment_times(result, offset):
    if not offset:
        return result
    for segment in result.get("segments", []):
        segment["start"] += offset
        segment["end"] += offset
        for word in segment.get("words", []):
            word["start"] += offset
            word["end"] += offset
    result.setdefault("alignment", {})["audio_trim_offset"] = offset
    return result


def run(command):
    print("$", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, check=True)


def load_articles(ids):
    wanted = set(ids or [])
    rows = []
    for path in sorted(DATA_DIR.glob("*.json")):
        if path.name.startswith(("_test", "index")):
            continue
        source = json.loads(path.read_text(encoding="utf-8"))
        if wanted and source.get("id") not in wanted and path.stem not in wanted:
            continue
        audio_value = str(source.get("audio") or "")
        audio = ROOT / audio_value if audio_value else None
        rows.append({"path": path, "source": source, "audio": audio})
    return rows


def mfa_word_entries(aligned):
    entries = aligned["tiers"]["words"]["entries"]
    words = []
    for entry in entries:
        label = str(entry[2]).strip()
        if label in ("<eps>", ""):
            continue
        for part in expand_token(label):
            words.append({
                "word": part,
                "start": float(entry[0]),
                "end": float(entry[1]),
            })
    return words


def token_key(token):
    token = str(token).lower().replace("’", "'").replace("‘", "'")
    if token == "<unk>":
        return token
    return re.sub(r"[^a-z0-9]+", "", token)


def map_word_times(source_words, mfa_words):
    """Map source words to monotonic MFA intervals despite count differences."""
    if not source_words or not mfa_words:
        raise RuntimeError("empty source or MFA word tier")

    source_keys = [token_key(word["word"]) for word in source_words]
    mfa_keys = [token_key(word["word"]) for word in mfa_words]
    matcher = difflib.SequenceMatcher(None, source_keys, mfa_keys, autojunk=False)
    assignments = [None] * len(source_words)
    matched = 0

    def fill_gap(source_start, source_end, mfa_start, mfa_end):
        count_source = source_end - source_start
        count_mfa = mfa_end - mfa_start
        if count_source <= 0 or count_mfa <= 0:
            return
        if count_source == 1:
            assignments[source_start] = mfa_start
            return
        for offset in range(count_source):
            ratio = offset / (count_source - 1)
            assignments[source_start + offset] = mfa_start + round(ratio * (count_mfa - 1))

    previous_source = 0
    previous_mfa = 0
    for block in matcher.get_matching_blocks():
        source_start, source_end = block.a, block.a + block.size
        mfa_start, mfa_end = block.b, block.b + block.size
        fill_gap(previous_source, source_start, previous_mfa, mfa_start)
        for offset in range(block.size):
            assignments[source_start + offset] = mfa_start + offset
        matched += block.size
        previous_source, previous_mfa = source_end, mfa_end

    # The final matching block is the SequenceMatcher sentinel (size 0), so
    # this also fills the real trailing gap without special casing it.
    fill_gap(previous_source, len(source_words), previous_mfa, len(mfa_words))

    mapped = []
    for index, source_word in enumerate(source_words):
        mfa_index = assignments[index]
        if mfa_index is not None:
            timing = mfa_words[mfa_index]
            start, end = timing["start"], timing["end"]
        else:
            previous = next((mapped[pos] for pos in range(len(mapped) - 1, -1, -1) if mapped[pos]["end"] is not None), None)
            next_source = next((pos for pos in range(index + 1, len(source_words)) if assignments[pos] is not None), None)
            following = mfa_words[assignments[next_source]] if next_source is not None else None
            start = previous["end"] if previous else mfa_words[0]["start"]
            end = following["start"] if following else mfa_words[-1]["end"]
            if end < start:
                end = start
        mapped.append({
            "word": source_word["word"],
            "start": start,
            "end": end,
        })
    return mapped, matched


def convert_result(source, aligned):
    mfa_words = mfa_word_entries(aligned)
    source_words = []
    segment_ranges = []
    for segment in source["segments"]:
        segment_start = len(source_words)
        source_words.extend({"word": word} for word in tokens(segment.get("en", "")))
        segment_ranges.append((segment_start, len(source_words)))
    mapped_words, matched = map_word_times(source_words, mfa_words)

    result = dict(source)
    result["alignment"] = {
        "engine": "montreal-forced-aligner",
        "model": MODEL_ID,
        "granularity": "word+phone",
        "fixed_transcript": True,
        "source_word_count": len(source_words),
        "mfa_word_count": len(mfa_words),
        "matched_word_count": matched,
    }
    result["segments"] = []
    placeholder_ids = []
    for segment, (start_index, end_index) in zip(source["segments"], segment_ranges):
        segment_words = mapped_words[start_index:end_index]
        if not segment_words:
            # Some imported transcripts contain punctuation-only placeholder
            # rows (for example ".. .", "," or "•").  They have no words for
            # MFA to align, so preserve them as zero-word timing rows rather
            # than borrowing speech from the adjacent sentence.
            copy = dict(segment)
            try:
                placeholder_start = float(segment.get("start"))
            except (TypeError, ValueError):
                placeholder_start = None
            previous_end = (
                result["segments"][-1].get("end")
                if result["segments"] else None
            )
            if placeholder_start is None:
                placeholder_start = previous_end if previous_end is not None else mfa_words[0]["start"]
            if previous_end is not None:
                placeholder_start = max(placeholder_start, previous_end)
            next_start = None
            segment_index = len(result["segments"])
            for following in source["segments"][segment_index + 1:]:
                try:
                    candidate = float(following.get("start"))
                except (TypeError, ValueError):
                    continue
                if candidate >= placeholder_start:
                    next_start = candidate
                    break
            placeholder_end = next_start if next_start is not None else placeholder_start
            copy["start"] = placeholder_start
            copy["end"] = max(placeholder_start, placeholder_end)
            copy["words"] = []
            copy["placeholder_segment"] = True
            result["segments"].append(copy)
            placeholder_ids.append(segment.get("id"))
            continue
        copy = dict(segment)
        copy["start"] = segment_words[0]["start"]
        copy["end"] = segment_words[-1]["end"]
        copy["words"] = segment_words
        result["segments"].append(copy)
    # Keep punctuation-only placeholder rows inside the actual neighboring
    # speech interval.  This matters when a clipped MFA pass has slightly
    # different timing from the old rough source timestamps.
    for index, segment in enumerate(result["segments"]):
        if not segment.get("placeholder_segment"):
            continue
        previous_end = (
            result["segments"][index - 1].get("end") if index else 0.0
        )
        next_start = (
            result["segments"][index + 1].get("start")
            if index + 1 < len(result["segments"]) else None
        )
        start = max(float(previous_end or 0.0), float(segment.get("start") or 0.0))
        if next_start is not None:
            next_start = float(next_start)
            end = next_start - 0.05
            start = max(float(previous_end or 0.0), end - 0.2)
            if start >= end:
                start = max(float(previous_end or 0.0), next_start - 0.2)
                end = max(start + 0.2, next_start)
            segment["start"] = start
            segment["end"] = end
        else:
            segment["start"] = start
            segment["end"] = max(start + 0.2, float(segment.get("end") or 0.0))
    if placeholder_ids:
        result["alignment"]["placeholder_segment_count"] = len(placeholder_ids)
        result["alignment"]["placeholder_segment_ids"] = placeholder_ids
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", help="Comma-separated ids for a limited test run")
    parser.add_argument("--force", action="store_true", help="Reprocess files already marked MFA")
    parser.add_argument("--num-jobs", type=int, default=4)
    parser.add_argument("--beam", type=int, default=10)
    parser.add_argument("--retry-beam", type=int, default=40)
    parser.add_argument("--fallback-beam", type=int, default=40)
    parser.add_argument("--fallback-retry-beam", type=int, default=160)
    args = parser.parse_args()
    ids = [x.strip() for x in args.ids.split(",")] if args.ids else None

    articles = load_articles(ids)
    eligible = []
    skipped = []
    failed = []
    for row in articles:
        source = row["source"]
        if row["audio"] is None or not row["audio"].exists():
            skipped.append({"id": source.get("id"), "reason": "missing audio"})
        elif source.get("alignment", {}).get("engine") == "montreal-forced-aligner" and not args.force:
            skipped.append({"id": source.get("id"), "reason": "already MFA"})
        else:
            eligible.append(row)

    print(f"Articles selected: {len(articles)}", flush=True)
    print(f"To align: {len(eligible)}; skipped before run: {len(skipped)}", flush=True)
    if not eligible:
        print(json.dumps({"aligned": [], "skipped": skipped, "failed": failed}, ensure_ascii=False, indent=2))
        return

    with tempfile.TemporaryDirectory(prefix="mfa-batch-", dir=ROOT / "tmp") as temp:
        work = Path(temp)
        corpus = work / "corpus"
        output = work / "output"
        corpus.mkdir()
        config = work / "mfa-config.yaml"
        config.write_text(f"beam: {args.beam}\nretry_beam: {args.retry_beam}\n", encoding="utf-8")
        for index, row in enumerate(eligible, start=1):
            stem = row["path"].stem
            wav = corpus / f"{stem}.wav"
            lab = corpus / f"{stem}.lab"
            print(f"[{index}/{len(eligible)}] prepare {stem}", flush=True)
            run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(row["audio"]), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav),
            ])
            full_text = " ".join(segment.get("en", "") for segment in row["source"]["segments"])
            lab.write_text(lab_text(full_text) + "\n", encoding="utf-8")

        run([
            "docker", "run", "--rm",
            "-v", f"{work}:/data",
            "-v", f"{MFA_VOLUME}:/mfa",
            "-v", f"{HF_VOLUME}:/home/mfauser/.cache/huggingface",
            "-e", "MFA_ROOT_DIR=/mfa",
            "-e", "HF_HOME=/home/mfauser/.cache/huggingface",
            "-e", "HF_HUB_CACHE=/home/mfauser/.cache/huggingface/hub",
            "-e", "HUGGINGFACE_HUB_CACHE=/home/mfauser/.cache/huggingface/hub",
            IMAGE, "mfa", "align_hf", "/data/corpus", MODEL_ID, "/data/output",
            "--config_path", "/data/mfa-config.yaml",
            "--output_format", "json", "--use_g2p", "--single_speaker",
            "--no_textgrid_cleanup", "--include_original_text",
            "--num_jobs", str(args.num_jobs), "--clean", "--overwrite",
        ])

        def output_map(directory):
            return {path.stem: path for path in directory.rglob("*.json")}

        aligned_paths = output_map(output)
        missing_rows = [row for row in eligible if row["path"].stem not in aligned_paths]
        print(f"First pass outputs: {len(aligned_paths)}/{len(eligible)}", flush=True)
        if missing_rows:
            retry_corpus = work / "retry-corpus"
            retry_output = work / "retry-output"
            retry_corpus.mkdir()
            retry_config = work / "retry-config.yaml"
            retry_config.write_text(
                f"beam: {args.fallback_beam}\nretry_beam: {args.fallback_retry_beam}\n",
                encoding="utf-8",
            )
            for row in missing_rows:
                stem = row["path"].stem
                shutil.copy2(corpus / f"{stem}.wav", retry_corpus / f"{stem}.wav")
                shutil.copy2(corpus / f"{stem}.lab", retry_corpus / f"{stem}.lab")
            print(f"Retrying {len(missing_rows)} files with fallback beam", flush=True)
            try:
                run([
                    "docker", "run", "--rm",
                    "-v", f"{work}:/data",
                    "-v", f"{MFA_VOLUME}:/mfa",
                    "-v", f"{HF_VOLUME}:/home/mfauser/.cache/huggingface",
                    "-e", "MFA_ROOT_DIR=/mfa",
                    "-e", "HF_HOME=/home/mfauser/.cache/huggingface",
                    "-e", "HF_HUB_CACHE=/home/mfauser/.cache/huggingface/hub",
                    "-e", "HUGGINGFACE_HUB_CACHE=/home/mfauser/.cache/huggingface/hub",
                    IMAGE, "mfa", "align_hf", "/data/retry-corpus", MODEL_ID, "/data/retry-output",
                    "--config_path", "/data/retry-config.yaml",
                    "--output_format", "json", "--use_g2p", "--single_speaker",
                    "--no_textgrid_cleanup", "--include_original_text",
                    "--num_jobs", str(args.num_jobs), "--clean", "--overwrite",
                ])
                aligned_paths.update(output_map(retry_output))
            except subprocess.CalledProcessError as exc:
                print(f"Fallback MFA run failed with exit code {exc.returncode}", flush=True)

        for index, row in enumerate(eligible, start=1):
            stem = row["path"].stem
            aligned_path = aligned_paths.get(stem)
            if aligned_path is None:
                failed.append({"id": row["source"].get("id"), "reason": "MFA output missing"})
                print(f"[{index}/{len(eligible)}] FAIL {stem}: MFA output missing", flush=True)
                continue
            try:
                result = convert_result(row["source"], json.loads(aligned_path.read_text(encoding="utf-8")))
                row["path"].write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"[{index}/{len(eligible)}] wrote {stem}", flush=True)
            except Exception as exc:
                failed.append({"id": row["source"].get("id"), "reason": str(exc)})
                print(f"[{index}/{len(eligible)}] FAIL {stem}: {exc}", flush=True)

    report = {"aligned": [row["source"].get("id") for row in eligible if row["source"].get("id") not in {x["id"] for x in failed}], "skipped": skipped, "failed": failed}
    report_path = ROOT / "tools" / "mfa-batch-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Report: {report_path}")
    print(json.dumps({"aligned": len(report["aligned"]), "skipped": len(skipped), "failed": len(failed)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
