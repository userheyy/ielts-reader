# -*- coding: utf-8 -*-
"""Re-encode selected listening audio safely to a smaller speech bitrate."""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = (ROOT / "media" / "audio").resolve()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--books", default="14,15,16,17,18,19")
    parser.add_argument("--bitrate", default="32k")
    args = parser.parse_args()
    books = {int(item.strip().lstrip("cC")) for item in args.books.split(",") if item.strip()}
    if not AUDIO_DIR.is_dir() or ROOT not in AUDIO_DIR.parents:
        raise SystemExit("audio directory is outside the workspace")

    files = []
    for path in AUDIO_DIR.glob("c*-test*-part*.mp3"):
        match = re.match(r"c(\d+)-test", path.name)
        if match and int(match.group(1)) in books:
            files.append(path.resolve())
    files.sort()

    with tempfile.TemporaryDirectory(prefix="ielts-audio-") as temp_name:
        temp_dir = Path(temp_name).resolve()
        for index, source in enumerate(files, 1):
            if source.parent != AUDIO_DIR:
                raise RuntimeError(f"unexpected target path: {source}")
            output = temp_dir / source.name
            subprocess.run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(source), "-map", "0:a:0", "-ac", "1",
                "-b:a", args.bitrate, str(output),
            ], check=True)
            if not output.is_file() or output.stat().st_size < 100_000:
                raise RuntimeError(f"invalid encoded output: {source.name}")
            os.replace(output, source)
            if index % 12 == 0 or index == len(files):
                print(f"reencoded {index}/{len(files)}", flush=True)
    print("done")


if __name__ == "__main__":
    main()
