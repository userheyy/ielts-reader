# -*- coding: utf-8 -*-
"""从 Downloads/剑桥雅思真题音频1-19/ 拷贝并规整命名到 media/audio/。

目标命名统一为 `c{n}-test{t}-part{p}.mp3`(见 media/audio/README.md)。

用法:
    py tools/import_audio.py                # 默认拷 c15-c19(c14 已规整)
    py tools/import_audio.py --dry-run      # 只打印映射,不实际拷贝
    py tools/import_audio.py --books c15    # 单册
"""
import argparse
import os
import re
import shutil
from pathlib import Path

SRC_BASE = Path(
    r"C:\Users\zuolu\Downloads\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）"
    r"\剑桥雅思真题音频1-19"
)
DST_DIR = Path(__file__).resolve().parent.parent / "media" / "audio"

# 每册的源目录识别关键词 + 文件名 regex(两个 group:test 号、part/section 号)
MAPPINGS = {
    "c14": {
        "keyword": "14",
        "pattern": re.compile(r"^T(\d)S(\d)\.mp3$", re.IGNORECASE),
    },
    "c15": {
        "keyword": "15",
        "pattern": re.compile(r"^IELTS15_test(\d)_audio(\d)\.mp3$", re.IGNORECASE),
    },
    "c16": {
        "keyword": "16",
        "pattern": re.compile(r"^Test\s+(\d)\s+Part\s+(\d)\.mp3$", re.IGNORECASE),
    },
    "c17": {
        "keyword": "17",
        "pattern": re.compile(r"^ELT_IELTS17_t(\d)_audio(\d)\.mp3$", re.IGNORECASE),
    },
    "c18": {
        "keyword": "18",
        # 剑18 是 3 级嵌套,每 Test 目录下 4 个 part。文件名同 c16 但要靠 walk 兜到
        "pattern": re.compile(r"^Test\s+(\d)\s+Part\s+(\d)\.mp3$", re.IGNORECASE),
    },
    "c19": {
        "keyword": "19",
        "pattern": re.compile(r"^Test(\d)\s+Part(\d)\.mp3$", re.IGNORECASE),
    },
}


def find_src_dir(keyword):
    """在 SRC_BASE 一级子目录中查找目录名包含 keyword 的项(且不含更大册号误匹配)。"""
    candidates = []
    for name in sorted(os.listdir(SRC_BASE)):
        p = SRC_BASE / name
        if not p.is_dir():
            continue
        # 排除 "1-19" 这种整包目录,只要单册目录
        if keyword in name:
            # 剑1 会误匹配剑14/15/... — 用"剑{keyword}"或数字边界避免
            # 简单粗暴:整个 name 里的数字连续段必须等于 keyword
            digits = re.findall(r"\d+", name)
            if any(d == keyword for d in digits):
                candidates.append(p)
    return candidates[0] if candidates else None


def import_book(book, dry_run):
    m = MAPPINGS[book]
    src_dir = find_src_dir(m["keyword"])
    if not src_dir:
        print(f"{book}: 未找到源目录(keyword={m['keyword']!r})")
        return 0, 0, 1
    pat = m["pattern"]
    copied = 0
    skipped = 0
    unmatched = 0
    for root, _, files in os.walk(src_dir):
        for f in files:
            if not f.lower().endswith(".mp3"):
                continue
            mo = pat.match(f)
            if not mo:
                unmatched += 1
                continue
            t, p = int(mo.group(1)), int(mo.group(2))
            src = Path(root) / f
            dst = DST_DIR / f"{book}-test{t}-part{p}.mp3"
            if dst.exists() and dst.stat().st_size > 0:
                skipped += 1
                continue
            print(f"  {'[dry] ' if dry_run else ''}{src.name}  →  {dst.name}")
            if not dry_run:
                shutil.copy2(src, dst)
            copied += 1
    return copied, skipped, unmatched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--books", default="c15,c16,c17,c18,c19")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not SRC_BASE.exists():
        raise SystemExit(f"源目录不存在: {SRC_BASE}")
    DST_DIR.mkdir(parents=True, exist_ok=True)

    books = [b.strip() for b in args.books.split(",") if b.strip()]
    tot_c = tot_s = tot_u = 0
    for book in books:
        if book not in MAPPINGS:
            print(f"跳过未知册 {book}")
            continue
        print(f"\n=== {book} ===")
        c, s, u = import_book(book, args.dry_run)
        tot_c += c; tot_s += s; tot_u += u
        print(f"{book}: 拷贝 {c} · 已存在跳过 {s} · 未匹配 {u}")
    print(f"\n合计 {'[dry] ' if args.dry_run else ''}拷贝 {tot_c},跳过 {tot_s},未匹配 {tot_u}")
    print(f"目标:{DST_DIR}")


if __name__ == "__main__":
    main()
