# -*- coding: utf-8 -*-
"""就地扫 data/listening/*.json,把 start 明显早于历史 max 的 seg 置 null。

拆分脚本 align_starts 里只在拆出的多句内部做单调保护,跨 turn 时可能因为
whisper fuzzy match 定位到早期,产生 400s → 60s 这种回跳。
"""
import json
import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "listening"


def fix_file(path: Path) -> tuple[int, int]:
    d = json.loads(path.read_text(encoding="utf-8"))
    segs = d.get("segments", [])
    max_seen = -1.0
    fixed = 0
    for s in segs:
        st = s.get("start")
        if not isinstance(st, (int, float)):
            continue
        if max_seen >= 0 and st < max_seen - 0.5:
            s["start"] = None
            fixed += 1
        else:
            if st > max_seen:
                max_seen = float(st)
    if fixed:
        path.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return fixed, len(segs)


def main():
    total_fixed = 0
    for f in sorted(os.listdir(DATA_DIR)):
        if not f.endswith(".json") or f == "index.json" or f.startswith("_"):
            continue
        n, total = fix_file(DATA_DIR / f)
        if n:
            print(f"  {f}: {n}/{total} seg start 置 null")
            total_fixed += n
    print(f"合计:{total_fixed} 个 start 已修正为 null")


if __name__ == "__main__":
    main()
