# -*- coding: utf-8 -*-
"""Focused QA for generated Cambridge listening batches."""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "listening"
EXPECTED_MISSING_AUDIO = {
    "c2-test3-l4",
    "c2-test4-l1", "c2-test4-l2", "c2-test4-l3", "c2-test4-l4",
}
BANNED_SEGMENT_TEXT = re.compile(
    r"Answer keys?|Academic Reading|Reading Passage|Practice Test|Tapescripts?|Audio Scripts?",
    re.I,
)


def duration(path):
    run = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True, capture_output=True,
    )
    try:
        return float(run.stdout.strip()) if run.returncode == 0 else 0.0
    except ValueError:
        return 0.0


def check_part(pid):
    errors, warnings = [], []
    path = DATA_DIR / f"{pid}.json"
    if not path.exists():
        return [f"missing JSON {pid}"], warnings
    data = json.loads(path.read_text(encoding="utf-8"))
    match = re.fullmatch(r"c(\d+)-test([1-4])-l([1-4])", pid)
    book, test, part = int(match.group(1)), int(match.group(2)), int(match.group(3))
    first, last = (part - 1) * 10 + 1, part * 10
    segments = data.get("segments") or []
    if not segments:
        errors.append(f"{pid}: no segments")
    expected_unit = "speaker_turn" if part in (1, 3) else "sentence"
    if data.get("practice_unit") != expected_unit:
        errors.append(f"{pid}: practice_unit={data.get('practice_unit')!r}")
    ids = [s.get("id") for s in segments]
    if ids != list(range(1, len(segments) + 1)):
        errors.append(f"{pid}: segment ids are not sequential")
    for segment in segments:
        text = segment.get("en") or ""
        if BANNED_SEGMENT_TEXT.search(text):
            errors.append(f"{pid}: leaked page text in segment {segment.get('id')}")
        if re.search(r"\bQ\s*\d{1,2}\b|\[\[Q", text):
            errors.append(f"{pid}: question marker left in segment {segment.get('id')}")
    starts = [s.get("start") for s in segments]
    numeric = [x for x in starts if isinstance(x, (int, float))]
    if numeric and numeric != sorted(numeric):
        errors.append(f"{pid}: timestamps are not monotonic")

    groups = data.get("questions") or []
    items = [item for group in groups for item in (group.get("items") or [])]
    numbers = [item.get("number") for item in items]
    expected_numbers = (list(range(numbers[0], numbers[-1] + 1)) if book == 1 and numbers
                        else list(range(first, last + 1)))
    if numbers != expected_numbers:
        errors.append(f"{pid}: question numbers {numbers}")
    empty_answers = [item.get("number") for item in items if not str(item.get("answer") or "").strip()]
    if empty_answers:
        errors.append(f"{pid}: empty answers {empty_answers}")
    if not groups or not str(groups[0].get("source_text") or "").strip():
        errors.append(f"{pid}: missing source_text")

    audio_value = data.get("audio")
    audio = ROOT / str(audio_value or "")
    if not audio_value or not audio.exists():
        if pid in EXPECTED_MISSING_AUDIO:
            warnings.append(f"{pid}: source package has no audio")
        else:
            errors.append(f"{pid}: audio missing")
    else:
        seconds = duration(audio)
        if seconds < 30:
            errors.append(f"{pid}: invalid/short audio ({seconds:.1f}s)")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--books", default="1,2,3,4,5")
    args = parser.parse_args()
    books = sorted({int(x.strip().lstrip("cC")) for x in args.books.split(",") if x.strip()})
    errors, warnings = [], []
    for book in books:
        for test in range(1, 5):
            for part in range(1, 5):
                e, w = check_part(f"c{book}-test{test}-l{part}")
                errors.extend(e)
                warnings.extend(w)
    for warning in warnings:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[FAIL] {error}")
    checked = len(books) * 16
    print(f"Checked {checked} parts: {len(errors)} error(s), {len(warnings)} warning(s)")
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
