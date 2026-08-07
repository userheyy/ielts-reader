# -*- coding: utf-8 -*-
"""Fill missing Cambridge IELTS listening audio without rewriting JSON data."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from generate_listening_c9_c13 import AUDIO_ROOT, clean_text, fetch_test


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "listening"


def local_audio(book, test, part):
    folder = AUDIO_ROOT / f"剑{book}"
    names = {
        14: f"T{test}S{part}.mp3",
        15: f"IELTS15_test{test}_audio{part}.mp3",
        16: f"Test {test} Part {part}.mp3",
        17: f"ELT_IELTS17_t{test}_audio{part}.mp3",
        18: f"Test {test} Part {part}.mp3",
    }
    candidate = folder / names.get(book, "")
    return candidate if candidate.is_file() else None


def parse_id(value):
    match = re.fullmatch(r"c(\d+)-test(\d+)-l([1-4])", value)
    return tuple(map(int, match.groups())) if match else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--books", default="14,15,16,17,18,19")
    args = parser.parse_args()
    books = {int(item.strip().lstrip("cC")) for item in args.books.split(",") if item.strip()}
    cache = {}
    imported = 0
    for path in sorted(DATA_DIR.glob("c*-test*-l*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        parsed = parse_id(str(data.get("id", "")))
        if not parsed:
            continue
        book, test, part = parsed
        if book not in books or not data.get("audio"):
            continue
        target = ROOT / data["audio"]
        if target.exists():
            continue
        local = local_audio(book, test, part)
        if local:
            source = str(local)
            origin = "local"
        else:
            key = (book, test)
            if key not in cache:
                payload = fetch_test(book, test)
                cache[key] = {
                    int(section.get("sectionNumber", 0)): section
                    for section in payload.get("sections", [])
                }
            source = clean_text(cache[key].get(part, {}).get("audioSrc"))
            origin = "remote fallback"
        if not source:
            raise ValueError(f"{data['id']}: no local or remote audio source")
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", source,
            "-map", "0:a:0", "-ac", "1", "-b:a", "32k", str(target),
        ], check=True)
        imported += 1
        print(f"audio {target.name}: {origin}")
    print(f"Imported {imported} missing audio file(s).")


if __name__ == "__main__":
    main()
