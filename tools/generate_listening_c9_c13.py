# -*- coding: utf-8 -*-
"""Generate Cambridge IELTS 9-19 listening data in the shared app format.

Books 9 and 10 in the supplied package are image-only scans.  To avoid
shipping OCR mistakes in the shadowing transcript, this importer combines the
local official audio with structured public transcriptions, questions, and
answer keys, then runs the same segmentation/alignment pipeline used by the
older books.  Local audio always wins; a section URL is used only when the
supplied package is missing that recording (currently most of Cambridge 13).
"""
import argparse
import functools
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

from generate_listening_c2_c5 import evidence_for_answer, update_index


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT.parent / "雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）"
AUDIO_ROOT = PACK / "剑桥雅思真题音频1-19"
DATA_DIR = ROOT / "data" / "listening"
AUDIO_DIR = ROOT / "media" / "audio"
RAW_URL = (
    "https://raw.githubusercontent.com/khanh020905/SWP391-PROJECT/"
    "main/public/data/cam-tests/cam{book}-test-{test}.json"
)
REMOTE_AUDIO_IDS = {
    # The supplied C14 T2 Part 4 file is a 17-minute mismatched recording.
    (14, 2, 4),
}
REMOTE_AUDIO_URLS = {
    # The structured source points to the same mismatched 17-minute file.
    # This standalone recording contains the correct official Section 4 audio.
    (14, 2, 4): "https://www.youtube.com/watch?v=whgZZ_XNt3k",
}
TRANSCRIPT_OVERRIDES = {
    # The structured source accidentally contains an unlabelled speech-to-text
    # dump for this one dialogue.  Use the labelled transcript page so each
    # complete MARTIN/SUE turn remains a distinct shadowing unit.
    (11, 3, 1): (
        "https://r.jina.ai/https://ieltstrainingonline.com/"
        "audio-script-cambridge-ielts-11-listening-test-03/"
    ),
}
for _part in (1, 3):
    TRANSCRIPT_OVERRIDES[(18, 1, _part)] = (
        "https://r.jina.ai/https://ieltstrainingonline.com/"
        "audioscripts-cambridge-ielts-018-listening-test-01/"
    )
for _test in range(1, 5):
    for _part in (1, 3):
        TRANSCRIPT_OVERRIDES[(19, _test, _part)] = (
            "https://r.jina.ai/https://ieltstrainingonline.com/"
            f"audioscripts-cambridge-ielts-019-listening-test-{_test:02d}/"
        )


def clean_text(value):
    text = str(value or "")
    text = re.sub(r"[\ud800-\udfff\ufffd]", "", text)
    text = text.replace("\u00a0", " ").replace("…", "...")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def fetch_test(book, test):
    url = RAW_URL.format(book=book, test=test)
    request = urllib.request.Request(url, headers={"User-Agent": "ielts-library-importer/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


@functools.lru_cache(maxsize=None)
def fetch_override_page(url):
    request = urllib.request.Request(url, headers={"User-Agent": "ielts-library-importer/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def fetch_transcript_override(book, test, part):
    url = TRANSCRIPT_OVERRIDES.get((book, test, part))
    if not url:
        return None
    markdown = fetch_override_page(url)
    heading = re.search(rf"###\s+\*\*(?:SECTION|PART)\s+{part}\*\*", markdown, re.I)
    if not heading:
        raise ValueError(f"c{book} test{test} part{part}: override heading missing")
    tail = markdown[heading.end():]
    stop = re.search(r"\nAdvertisements\s*\n|\n###\s+(?:\*\*)?(?:SECTION|PART)\s+[1-4]", tail, re.I)
    body = tail[:stop.start()] if stop else tail
    body = re.sub(r"(?m)^>\s?", "", body)
    body = body.replace("**", "")
    body = re.sub(r"_Q(\d+(?:\s+Q\d+)*)_", r"Q\1", body, flags=re.I)
    body = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"(?m)^-+\s*$", "", body)
    if part in (1, 3):
        speaker_re = re.compile(r"^[A-Z][A-Z0-9 .'-]{0,40}:\s*.+$")
        labelled = [line.strip() for line in body.splitlines() if speaker_re.match(line.strip())]
        if len(labelled) >= 5:
            body = "\n".join(labelled)
    return clean_text(body)


def answer_value(value):
    if isinstance(value, list):
        return " / ".join(clean_text(item) for item in value if clean_text(item))
    if isinstance(value, dict):
        return " / ".join(clean_text(item) for item in value.values() if clean_text(item))
    return clean_text(value)


def collect_answers(value, result=None):
    result = result if result is not None else {}
    if isinstance(value, dict):
        mapped = value.get("correctAnswers")
        if isinstance(mapped, dict):
            for number, answer in mapped.items():
                if str(number).isdigit():
                    result[int(number)] = answer_value(answer)
        number = value.get("qNum", value.get("questionNumber", value.get("number")))
        if str(number).isdigit() and isinstance(mapped, list):
            # Grouped multiple-choice blocks use the first question number plus
            # an ordered list, e.g. qNum=19 and ["A", "E"] for Q19-20.
            for offset, answer in enumerate(mapped):
                result[int(number) + offset] = answer_value(answer)
        if str(number).isdigit() and "correctAnswer" in value:
            result[int(number)] = answer_value(value["correctAnswer"])
        for child in value.values():
            collect_answers(child, result)
    elif isinstance(value, list):
        for child in value:
            collect_answers(child, result)
    return result


def display_key(key):
    return re.sub(r"(?<!^)([A-Z])", r" \1", str(key)).replace("_", " ").strip().title()


def flatten_question_content(value, indent=0):
    prefix = "  " * indent
    rows = []
    if isinstance(value, str):
        text = clean_text(value)
        if text:
            rows.extend(prefix + line for line in text.splitlines() if line.strip())
    elif isinstance(value, (int, float)):
        rows.append(prefix + str(value))
    elif isinstance(value, list):
        for child in value:
            child_rows = flatten_question_content(child, indent + 1)
            if child_rows:
                rows.extend(child_rows)
    elif isinstance(value, dict):
        for key, child in value.items():
            if key in {"correctAnswer", "correctAnswers", "audioStart", "audioEnd"}:
                continue
            child_rows = flatten_question_content(child, indent + 1)
            if not child_rows:
                continue
            if isinstance(child, (str, int, float)) and len(child_rows) == 1:
                rows.append(f"{prefix}{display_key(key)}: {child_rows[0].strip()}")
            else:
                rows.append(f"{prefix}{display_key(key)}:")
                rows.extend(child_rows)
    return rows


def source_text(section, part):
    first, last = (part - 1) * 10 + 1, part * 10
    rows = [f"SECTION {part}", f"Questions {first}-{last}"]
    title = clean_text(section.get("title"))
    if title:
        rows.append(title)
    for block in section.get("blocks", []):
        heading = clean_text(block.get("heading"))
        instruction = clean_text(block.get("instruction"))
        if heading:
            rows.append(heading)
        if instruction:
            rows.append(instruction)
        rows.extend(flatten_question_content(block.get("content")))
    text = "\n".join(rows)
    text = re.sub(r"\{(\d{1,2})\}", r"[\1] __________", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def prompt_for_number(source, number):
    lines = source.splitlines()
    marker = re.compile(rf"(?:\[{number}\]|\b(?:Question|Q Num|Number):\s*{number}\b)", re.I)
    for index, line in enumerate(lines):
        if marker.search(line):
            begin = max(0, index - 1)
            end = min(len(lines), index + 5)
            return " ".join(item.strip() for item in lines[begin:end])[:900]
    return f"Question {number}（请根据上方原书题目作答）"


def protect_markers(text):
    text = re.sub(r"[\[(]\s*Q\s*(\d{1,2})\s*[\])]", r" [[Q\1]] ", text, flags=re.I)
    text = re.sub(r"\bQ\s*(\d{1,2})\b", r" [[Q\1]] ", text, flags=re.I)
    text = re.sub(r"[\[(]\s*Example\s*[\])]", " ", text, flags=re.I)
    return text


def split_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    pattern = r"(?<=[.!?])\s+(?=(?:\[\[Q\d+\]\]\s*)?[A-Z'\"“])"
    return [part.strip() for part in re.split(pattern, text) if part.strip()]


def transcript_turns(transcript):
    text = protect_markers(clean_text(transcript))
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]
    turns = []
    current_speaker = "SPEAKER"
    buffer = []

    def flush():
        nonlocal buffer
        speech = re.sub(r"\s+", " ", " ".join(buffer)).strip()
        if speech:
            turns.append((current_speaker, speech))
        buffer = []

    speaker_re = re.compile(r"^([A-Za-z][A-Za-z0-9 .'-]{0,40}):\s*(.*)$")
    for line in lines:
        match = speaker_re.match(line)
        if match:
            flush()
            current_speaker = re.sub(r"\s+", " ", match.group(1)).strip().upper()
            if match.group(2).strip():
                buffer.append(match.group(2).strip())
        else:
            buffer.append(line)
    flush()
    return turns


def parse_segments(transcript, part):
    turns = transcript_turns(transcript)
    units = turns if part in (1, 3) else [
        (speaker, sentence)
        for speaker, speech in turns
        for sentence in split_sentences(speech)
    ]
    segments = []
    for speaker, speech in units:
        markers = sorted({int(number) for number in re.findall(r"\[\[Q(\d+)\]\]", speech)})
        speech = re.sub(r"\s*\[\[Q\d+\]\]\s*", " ", speech)
        speech = re.sub(r"\s+", " ", speech).strip()
        if not speech:
            continue
        segments.append({
            "id": len(segments) + 1,
            "start": None,
            "speaker": speaker,
            "en": speech,
            "zh": "",
            "words": [],
            "answers": markers,
        })
    return segments


def build_part(book, test, part, section):
    first, last = (part - 1) * 10 + 1, part * 10
    answers = collect_answers(section.get("blocks", []))
    missing = [number for number in range(first, last + 1) if not answers.get(number)]
    if missing:
        raise ValueError(f"c{book} test{test} part{part}: missing answers {missing}")
    source = source_text(section, part)
    transcript = fetch_transcript_override(book, test, part) or section.get("fullTranscript", "")
    segments = parse_segments(transcript, part)
    if not segments:
        raise ValueError(f"c{book} test{test} part{part}: empty transcript")
    for segment in segments:
        segment["answers"] = [number for number in segment["answers"] if first <= number <= last]
    items = []
    for number in range(first, last + 1):
        answer = answers[number]
        evidence = next((seg["id"] for seg in segments if number in seg["answers"]), None)
        if evidence is None:
            evidence = evidence_for_answer(segments, answer)
        if evidence is not None:
            segment = segments[evidence - 1]
            if number not in segment["answers"]:
                segment["answers"].append(number)
                segment["answers"].sort()
        items.append({
            "number": number,
            "prompt": prompt_for_number(source, number),
            "answer": answer,
            "evidence_segment": evidence,
            "paraphrase": None,
        })
    pid = f"c{book}-test{test}-l{part}"
    return {
        "id": pid,
        "source": f"剑桥雅思{book} · Test {test} · Part {part}",
        "title": f"Listening Part {part}",
        "audio": f"media/audio/c{book}-test{test}-part{part}.mp3",
        "practice_unit": "speaker_turn" if part in (1, 3) else "sentence",
        "segments": segments,
        "questions": [{
            "title": f"Questions {first}–{last}",
            "type": "mixed",
            "instructions": ["Complete the original Cambridge IELTS listening questions below."],
            "source_text": source,
            "items": items,
        }],
    }


def local_audio(book, test, part):
    if (book, test, part) in REMOTE_AUDIO_IDS:
        return None
    folder = AUDIO_ROOT / f"剑{book}"
    candidates = []
    if book in (9, 10):
        candidates = list((folder / f"Test{test}").glob(f"Test{test}.Sect*{part}.mp3"))
    elif book == 11:
        candidates = [folder / f"IELTS11_Test{test}_Section{part}.mp3"]
    elif book == 12:
        candidates = [folder / f"IELTS 12 Test {test + 4}_S{part}.mp3"]
    elif book == 13:
        candidates = list(folder.glob(f"Test{test}.Sect*{part}.mp3"))
    elif book == 14:
        candidates = [folder / f"T{test}S{part}.mp3"]
    elif book == 15:
        candidates = [folder / f"IELTS15_test{test}_audio{part}.mp3"]
    elif book == 16:
        candidates = [folder / f"Test {test} Part {part}.mp3"]
    elif book == 17:
        candidates = [folder / f"ELT_IELTS17_t{test}_audio{part}.mp3"]
    elif book == 18:
        candidates = [folder / f"Test {test} Part {part}.mp3"]
    return next((path for path in candidates if path.exists()), None)


def import_audio(book, test, part, section):
    local = local_audio(book, test, part)
    source = str(local) if local else REMOTE_AUDIO_URLS.get(
        (book, test, part), clean_text(section.get("audioSrc"))
    )
    if not source:
        raise ValueError(f"c{book} test{test} part{part}: no local or remote audio")
    target = AUDIO_DIR / f"c{book}-test{test}-part{part}.mp3"
    downloaded = None
    if source.startswith(("https://www.youtube.com/", "https://youtu.be/")):
        template = AUDIO_DIR / f".{target.stem}.source.%(ext)s"
        subprocess.run([
            "yt-dlp", "--no-playlist", "-f", "bestaudio", "-o", str(template), source,
        ], check=True)
        matches = sorted(AUDIO_DIR.glob(f".{target.stem}.source.*"))
        if not matches:
            raise ValueError(f"c{book} test{test} part{part}: yt-dlp produced no audio")
        downloaded = matches[0]
        source = str(downloaded)
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", source,
        "-map", "0:a:0", "-ac", "1", "-b:a", "32k", str(target),
    ], check=True)
    if downloaded:
        downloaded.unlink(missing_ok=True)
    origin = "local" if local else "remote fallback"
    print(f"audio {target.name}: {origin}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--books", default="9,10,11,12,13,14,15,16,17,18,19", help="comma-separated book numbers")
    parser.add_argument("--import-audio", action="store_true")
    parser.add_argument("--audio-only", action="store_true", help="rebuild audio without rewriting aligned JSON")
    args = parser.parse_args()
    books = sorted({int(item.strip().lstrip("cC")) for item in args.books.split(",") if item.strip()})
    if any(book not in range(9, 20) for book in books):
        raise SystemExit("This generator supports Cambridge IELTS 9-19 only")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    generated = {}
    fetched = {}
    for book in books:
        generated[book] = {}
        for test in range(1, 5):
            payload = fetch_test(book, test)
            sections = sorted(payload.get("sections", []), key=lambda row: int(row.get("sectionNumber", 0)))
            if len(sections) != 4:
                raise ValueError(f"c{book} test{test}: expected 4 sections, got {len(sections)}")
            fetched[(book, test)] = sections
            if not args.audio_only:
                for part, section in enumerate(sections, 1):
                    data = build_part(book, test, part, section)
                    (DATA_DIR / f"{data['id']}.json").write_text(
                        json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
                    generated[book][(test, part)] = data
                    print(f"{data['id']}: {len(data['segments'])} units / 10 questions")
    if not args.audio_only:
        update_index(generated)

    if args.import_audio or args.audio_only:
        for book in books:
            for test in range(1, 5):
                for part, section in enumerate(fetched[(book, test)], 1):
                    import_audio(book, test, part, section)


if __name__ == "__main__":
    main()
