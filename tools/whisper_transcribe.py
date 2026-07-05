# -*- coding: utf-8 -*-
"""faster-whisper 批量转写 media/audio/*.mp3 → tools/out/listening/{id}.whisper.json。

单 Python 进程加载一次模型,顺序跑所有 mp3。CPU int8 small.en 上大约 10x realtime,
96 个 part(每 5-8 分钟)预计 1.5-2 小时。

用法:
    py tools/whisper_transcribe.py                             # 全 96 mp3
    py tools/whisper_transcribe.py --books c14                 # 单册
    py tools/whisper_transcribe.py --only c14-test1-part1      # 单个
    py tools/whisper_transcribe.py --resume                    # 跳过 out 里已有的
    py tools/whisper_transcribe.py --model small.en            # 默认 small.en,可换 medium.en
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "media" / "audio"
OUT_DIR = ROOT / "tools" / "out" / "listening"

FN_RE = re.compile(r"^(c\d+-test\d-part\d)\.mp3$", re.IGNORECASE)


def collect_files(books, only):
    if only:
        wanted = {p.strip() for p in only.split(",") if p.strip()}
        return sorted([AUDIO_DIR / f"{w}.mp3" for w in wanted])
    books = {b.strip() for b in books.split(",") if b.strip()} if books else None
    out = []
    for f in sorted(AUDIO_DIR.iterdir()):
        m = FN_RE.match(f.name)
        if not m:
            continue
        stem = m.group(1)
        book = stem.split("-", 1)[0]
        if books and book not in books:
            continue
        out.append(f)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--books", default="c14,c15,c16,c17,c18,c19")
    ap.add_argument("--only")
    ap.add_argument("--resume", action="store_true", help="跳过 out 里已有的 whisper.json")
    ap.add_argument("--model", default="small.en",
                    help="tiny.en / base.en / small.en / medium.en")
    ap.add_argument("--beam", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not AUDIO_DIR.exists():
        raise SystemExit(f"未找到 {AUDIO_DIR}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    files = collect_files(args.books, args.only)
    if args.resume:
        files = [f for f in files
                 if not (OUT_DIR / f"{f.stem}.whisper.json").exists()]

    print(f"待处理 {len(files)} 个 mp3")
    if not files or args.dry_run:
        for f in files:
            print(f"  {f.stem}")
        return 0

    # 延迟加载,避免 dry-run 也吃 model
    from faster_whisper import WhisperModel  # noqa: E402
    t0 = time.time()
    print(f"加载 faster-whisper {args.model} (int8 CPU) …")
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    print(f"  加载 {time.time()-t0:.1f}s")

    total_audio = 0.0
    total_wall = 0.0
    for i, f in enumerate(files, 1):
        out_path = OUT_DIR / f"{f.stem}.whisper.json"
        print(f"\n[{i}/{len(files)}] {f.name} …", end=" ", flush=True)
        t0 = time.time()
        try:
            segments, info = model.transcribe(
                str(f), beam_size=args.beam, vad_filter=True,
                language="en", word_timestamps=True)
            segs_out = []
            for s in segments:
                words = []
                if s.words:
                    for w in s.words:
                        words.append({"w": w.word.strip(),
                                      "s": round(w.start, 2),
                                      "e": round(w.end, 2)})
                segs_out.append({
                    "start": round(s.start, 2),
                    "end": round(s.end, 2),
                    "text": s.text.strip(),
                    "words": words,
                })
            wall = time.time() - t0
            total_audio += info.duration
            total_wall += wall
            data = {
                "id": f.stem,
                "audio": f"media/audio/{f.name}",
                "duration": round(info.duration, 2),
                "model": args.model,
                "segments": segs_out,
            }
            with open(out_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp, ensure_ascii=False, indent=1)
            print(f"{wall:.1f}s / {info.duration:.0f}s 音频 · {len(segs_out)} 段"
                  f" · {info.duration/max(wall,0.1):.1f}x realtime")
        except Exception as e:
            print(f"FAIL {type(e).__name__}: {e}")

    if total_wall > 0:
        print(f"\n合计: {total_wall/60:.1f} 分钟处理 {total_audio/60:.1f} 分钟音频 "
              f"({total_audio/max(total_wall,0.1):.1f}x realtime)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
