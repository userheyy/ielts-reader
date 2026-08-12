"""Use Montreal Forced Aligner to create word/phone-aligned listening data.

Examples:
    py -3 tools/align_mfa.py c1-test1-l2 --in-place
    py -3 tools/align_mfa.py c1-test1-l2 --output data/listening/c1-test1-l2-mfa.json

The script keeps the visible transcript and answer data, while replacing each
segment's start/end and words with MFA's forced-alignment result. Docker keeps
MFA isolated from the app's other speech-recognition environments.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from batch_align_mfa import HF_VOLUME, convert_result, leading_trim_offset, shift_alignment_times


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "listening"
MODEL_ID = "MontrealCorpusTools/english_mfa"
IMAGE = "mmcauliffe/montreal-forced-aligner:latest"
MFA_VOLUME = "mfa-models"


def tokens(text):
    text = (text or "").replace("’", "'").replace("‘", "'")
    raw = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+", text)
    result = []
    for token in raw:
        if re.fullmatch(r"[A-Za-z]+'s", token, re.IGNORECASE):
            result.extend([token[:-2], "'s"])
        else:
            result.append(token)
    return result


def lab_text(text):
    text = (text or "").replace("’", "'").replace("‘", "'")
    text = re.sub(r"[^A-Za-z0-9' ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def run(command):
    print("$", " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, check=True)


def hf_offline_args():
    """Use the mounted Hugging Face cache without a network check when requested."""
    return ["-e", "HF_HUB_OFFLINE=1"] if os.environ.get("MFA_HF_OFFLINE") == "1" else []


def align_source(source, audio, beam=100, retry_beam=400, num_jobs=4,
                 trim_padding=2.0, mfa_root="/mfa"):
    """Align the complete article once, trimming only leading silence.

    The transcript remains one MFA utterance.  Existing approximate segment
    starts are used only to find a safe leading trim point, leaving the
    sentence boundaries to the single full-track alignment.
    """
    with tempfile.TemporaryDirectory(
        prefix=f"mfa-{source.get('id', 'article')}-", dir=ROOT / "tmp"
    ) as temp:
        work = Path(temp)
        trim_offset = leading_trim_offset(source, trim_padding)
        wav = work / "audio.wav"
        lab = work / "transcript.lab"
        alignment_path = work / "alignment"
        config_path = work / "mfa-config.yaml"
        config_path.write_text(
            f"beam: {beam}\nretry_beam: {retry_beam}\n",
            encoding="utf-8",
        )
        full_text = " ".join(segment.get("en", "") for segment in source["segments"])
        lab.write_text(lab_text(full_text) + "\n", encoding="utf-8")

        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(audio), "-ss", str(trim_offset), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav),
        ])
        run([
            "docker", "run", "--rm",
            "-v", f"{work}:/data",
            "-v", f"{MFA_VOLUME}:/mfa",
            "-v", f"{HF_VOLUME}:/home/mfauser/.cache/huggingface",
            "-e", f"MFA_ROOT_DIR={mfa_root}",
            "-e", "HF_HOME=/home/mfauser/.cache/huggingface",
            "-e", "HF_HUB_CACHE=/home/mfauser/.cache/huggingface/hub",
            "-e", "HUGGINGFACE_HUB_CACHE=/home/mfauser/.cache/huggingface/hub",
            *hf_offline_args(),
            IMAGE, "mfa", "align_one_hf",
            "/data/audio.wav", "/data/transcript.lab", MODEL_ID, "/data/alignment",
            "--config_path", "/data/mfa-config.yaml",
            "--output_format", "json", "--use_g2p", "--num_jobs", str(num_jobs),
        ])
        aligned = json.loads(alignment_path.read_text(encoding="utf-8"))

    return shift_alignment_times(convert_result(source, aligned), trim_offset)


def detect_silence_windows(audio, noise_db=-35, min_duration=0.35):
    """Return (start, end, duration) silence windows detected by ffmpeg."""
    command = [
        "ffmpeg", "-hide_banner", "-i", str(audio),
        "-af", f"silencedetect=noise={noise_db}dB:d={min_duration}",
        "-f", "null", "NUL",
    ]
    completed = subprocess.run(
        command, check=True, capture_output=True, text=True, encoding="utf-8",
        errors="replace",
    )
    lines = completed.stderr.splitlines()
    windows = []
    current_start = None
    for line in lines:
        start_match = re.search(r"silence_start:\s*([0-9.]+)", line)
        if start_match:
            current_start = float(start_match.group(1))
            continue
        end_match = re.search(r"silence_end:\s*([0-9.]+)", line)
        if end_match and current_start is not None:
            end = float(end_match.group(1))
            windows.append((current_start, end, end - current_start))
            current_start = None
    return windows


def choose_split_point(source, audio, min_part_seconds=90.0,
                       min_silence_duration=1.0):
    """Choose the longest natural silence between two source segments.

    The split must sit between source sentence starts and leave at least
    ``min_part_seconds`` of audio on both sides.  The returned point is the
    middle of the silence, so each child clip retains a small amount of
    surrounding silence instead of cutting on speech.
    """
    starts = []
    for segment in source.get("segments", []):
        try:
            starts.append((float(segment["start"]), segment.get("id")))
        except (KeyError, TypeError, ValueError):
            continue
    if len(starts) < 2:
        raise RuntimeError("not enough timed source segments for a split")
    starts.sort()
    duration = 0.0
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio)],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    duration = float(probe.stdout.strip())
    silences = detect_silence_windows(audio, min_duration=0.35)
    candidates = []
    for silence_start, silence_end, silence_duration in silences:
        if silence_duration < min_silence_duration:
            continue
        boundary = (silence_start + silence_end) / 2
        before = [item for item in starts if item[0] <= boundary]
        after = [item for item in starts if item[0] > boundary]
        if not before or not after:
            continue
        left = before[-1][0]
        right = after[0][0]
        # A valid cut is between sentence starts, never inside a source row.
        if left >= boundary or right <= boundary:
            continue
        left_length = boundary
        right_length = duration - boundary
        if left_length < min_part_seconds or right_length < min_part_seconds:
            continue
        candidates.append({
            "point": boundary,
            "silence_start": silence_start,
            "silence_end": silence_end,
            "silence_duration": silence_duration,
            "before_segment": before[-1][1],
            "after_segment": after[0][1],
            "left_seconds": left_length,
            "right_seconds": right_length,
        })
    if not candidates:
        raise RuntimeError("no natural silence between source segments")
    # Prefer the longest pause, with a slight preference for balanced parts.
    return max(candidates, key=lambda item: (
        item["silence_duration"],
        -abs(item["left_seconds"] - item["right_seconds"]),
    ))


def _align_source_clip(source, audio, clip_start, clip_end, beam, retry_beam,
                       num_jobs, mfa_root):
    """Align one clipped transcript and restore its original clock."""
    duration = max(0.05, float(clip_end) - float(clip_start))
    with tempfile.TemporaryDirectory(
        prefix=f"mfa-{source.get('id', 'article')}-", dir=ROOT / "tmp"
    ) as temp:
        work = Path(temp)
        wav = work / "audio.wav"
        lab = work / "transcript.lab"
        alignment_path = work / "alignment"
        config_path = work / "mfa-config.yaml"
        config_path.write_text(
            f"beam: {beam}\nretry_beam: {retry_beam}\n",
            encoding="utf-8",
        )
        full_text = " ".join(segment.get("en", "") for segment in source["segments"])
        lab.write_text(lab_text(full_text) + "\n", encoding="utf-8")

        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(audio), "-ss", str(clip_start), "-t", str(duration),
            "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav),
        ])
        run([
            "docker", "run", "--rm",
            "-v", f"{work}:/data",
            "-v", f"{MFA_VOLUME}:/mfa",
            "-v", f"{HF_VOLUME}:/home/mfauser/.cache/huggingface",
            "-e", f"MFA_ROOT_DIR={mfa_root}",
            "-e", "HF_HOME=/home/mfauser/.cache/huggingface",
            "-e", "HF_HUB_CACHE=/home/mfauser/.cache/huggingface/hub",
            "-e", "HUGGINGFACE_HUB_CACHE=/home/mfauser/.cache/huggingface/hub",
            *hf_offline_args(),
            IMAGE, "mfa", "align_one_hf",
            "/data/audio.wav", "/data/transcript.lab", MODEL_ID, "/data/alignment",
            "--config_path", "/data/mfa-config.yaml",
            "--output_format", "json", "--use_g2p", "--num_jobs", str(num_jobs),
        ])
        aligned = json.loads(alignment_path.read_text(encoding="utf-8"))

    relative_source = dict(source)
    relative_segments = []
    for segment in source["segments"]:
        relative = dict(segment)
        for field in ("start", "end"):
            try:
                relative[field] = float(segment[field]) - clip_start
            except (KeyError, TypeError, ValueError):
                pass
        relative_segments.append(relative)
    relative_source["segments"] = relative_segments
    return shift_alignment_times(convert_result(relative_source, aligned), clip_start)


def align_source_two_part(source, audio, beam=100, retry_beam=400, num_jobs=4,
                          trim_padding=2.0, mfa_root="/mfa",
                          fallback_beam=None, fallback_retry_beam=None):
    """Align an article in two parts split at its longest natural silence."""
    split = choose_split_point(source, audio)
    split_point = split["point"]
    trim_offset = leading_trim_offset(source, trim_padding)
    if trim_offset >= split_point:
        trim_offset = 0.0

    first_segments = []
    second_segments = []
    for segment in source["segments"]:
        try:
            segment_start = float(segment["start"])
        except (TypeError, ValueError):
            segment_start = split_point
        (first_segments if segment_start <= split_point else second_segments).append(segment)
    if not first_segments or not second_segments:
        raise RuntimeError("natural split did not divide the transcript")

    first_source = dict(source)
    first_source["segments"] = first_segments
    second_source = dict(source)
    second_source["segments"] = second_segments
    retried_parts = []
    attempt_beams = {}

    def align_part(part_number, part_source, start, end):
        attempts = [(beam, retry_beam)]
        if fallback_beam is not None and fallback_retry_beam is not None:
            attempts.append((fallback_beam, fallback_retry_beam))
            if fallback_retry_beam > fallback_beam:
                # MFA align_one_hf does not automatically consume
                # retry_beam after a command-level failure, so make the
                # retry beam an explicit final attempt for this half.
                attempts.append((fallback_retry_beam, fallback_retry_beam * 4))
        errors = []
        for attempt_index, (attempt_beam, attempt_retry) in enumerate(attempts):
            try:
                result = _align_source_clip(
                    part_source, audio, start, end, attempt_beam,
                    attempt_retry, num_jobs, mfa_root,
                )
                if attempt_index:
                    retried_parts.append(part_number)
                attempt_beams[str(part_number)] = attempt_beam
                return result
            except Exception as exc:
                errors.append(exc)
        raise RuntimeError(
            f"part {part_number} failed at beams "
            f"{[item[0] for item in attempts]}: {errors[-1]}"
        ) from errors[-1]

    first_last_end = max(
        float(segment["end"])
        for segment in first_segments
        if segment.get("end") is not None
    )
    second_first_start = min(
        float(segment["start"])
        for segment in second_segments
        if segment.get("start") is not None
    )
    second_last_end = max(
        float(segment["end"])
        for segment in second_segments
        if segment.get("end") is not None
    )
    # The split point may sit in a long pause.  Do not feed that whole pause
    # to MFA: keep only a small lead-in before the first sentence of part 2.
    second_audio_start = max(split_point, second_first_start - trim_padding)
    first_audio_end = min(split_point, first_last_end + trim_padding)
    second_audio_end = min(_audio_duration(audio), second_last_end + trim_padding)
    first = align_part(1, first_source, trim_offset, first_audio_end)
    second = align_part(2, second_source, second_audio_start, second_audio_end)

    result = dict(source)
    result["segments"] = first["segments"] + second["segments"]
    result["alignment"] = dict(first.get("alignment") or {})
    result["alignment"].update({
        "two_part_mfa": True,
        "split_strategy": "longest-natural-silence-between-source-segments",
        "split_point": split_point,
        "split_silence_start": split["silence_start"],
        "split_silence_end": split["silence_end"],
        "split_silence_duration": split["silence_duration"],
        "split_before_segment": split["before_segment"],
        "split_after_segment": split["after_segment"],
        "part1_seconds": split["left_seconds"],
        "part2_seconds": split["right_seconds"],
        "part2_audio_start": second_audio_start,
        "part1_audio_end": first_audio_end,
        "part2_audio_end": second_audio_end,
        "part1_segment_count": len(first_segments),
        "part2_segment_count": len(second_segments),
        "beam": beam,
        "retry_beam": retry_beam,
        "retried_parts": retried_parts,
        "part_beams": attempt_beams,
    })
    return result


def _audio_duration(audio):
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio)],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    return float(probe.stdout.strip())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paper_id", help="Listening JSON id, e.g. c1-test1-l2")
    parser.add_argument("--output", type=Path, help="Output JSON path")
    parser.add_argument("--in-place", action="store_true", help="Replace the source JSON")
    parser.add_argument("--num-jobs", type=int, default=2)
    parser.add_argument("--beam", type=int, default=100)
    parser.add_argument("--retry-beam", type=int, default=400)
    parser.add_argument("--trim-padding", type=float, default=2.0)
    parser.add_argument("--mfa-root", default="/mfa")
    args = parser.parse_args()

    source_path = DATA_DIR / f"{args.paper_id}.json"
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    if args.in_place and args.output:
        raise ValueError("Use either --in-place or --output, not both")
    output_path = source_path if args.in_place else (args.output or DATA_DIR / f"{args.paper_id}-mfa.json")
    output_path = output_path if output_path.is_absolute() else ROOT / output_path

    source = json.loads(source_path.read_text(encoding="utf-8"))
    audio = ROOT / source["audio"]
    if not audio.exists():
        raise FileNotFoundError(audio)

    result = align_source(
        source, audio, args.beam, args.retry_beam, args.num_jobs,
        args.trim_padding, args.mfa_root,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
