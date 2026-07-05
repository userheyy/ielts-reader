# -*- coding: utf-8 -*-
"""把 whisper 转写词级时间戳对齐到 Qwen-VL 抽的官方 audioscript_segments。

输入:
    tools/out/listening/{book}.raw.json      Qwen-VL 抽的 audioscript(权威英文)
    tools/out/listening/{part}.whisper.json  faster-whisper 转写(带 word timestamps)

输出:
    tools/out/listening/{part}.aligned.json  audioscript_segments,每段补 start 秒

算法:
1) 把 whisper 词序列铺平为一个 stream: [{w,s},{w,s},...]。
2) 遍历 audioscript_segments 里每段的首 3-5 词作为"锚",
   在 whisper stream 剩余部分找最匹配位置(SequenceMatcher.ratio 滑窗)。
3) 匹配到的 whisper word 的 s 就是 seg.start,cursor 前进到该段末端(用词数估算)。
4) 若某段找不到(fuzzy ratio 太低),start 记 null,不影响后续段落。

用法:
    py tools/align_timestamps.py c14                          # 一册所有 part
    py tools/align_timestamps.py c14 --only c14-test1-part1   # 单 part
"""
import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "tools" / "out" / "listening"


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


WORD_RE = re.compile(r"[A-Za-z']+|\d+")


def norm_words(text):
    """把一段文本切成小写 word list(标点丢弃,连字符保留)。"""
    return [w.lower() for w in WORD_RE.findall(text)]


def flatten_whisper_words(whisper_data):
    """把所有 segments.words 铺平成一个词流。"""
    words = []
    for seg in whisper_data.get("segments", []):
        for w in seg.get("words", []):
            token = w.get("w", "").strip()
            if not token:
                continue
            # 拆掉附着的标点
            for tok in WORD_RE.findall(token):
                words.append({"w": tok.lower(), "s": w["s"]})
                # words 的 s 用词组开始时间做近似,后续词用同一 s(足够近似)
    return words


def group_audioscript_segments_by_part(raw_data):
    """把 raw.json 里所有页的 audioscript_segments 按 (test, section) 归组。
    每组是一个 part 的完整 segments,顺序保留(按 page 号排序)。"""
    pages = raw_data.get("pages", {})
    sorted_pages = sorted(pages.items(), key=lambda kv: int(kv[0]))
    groups = {}  # (test, section) -> [segs...]
    for _pn, item in sorted_pages:
        if item.get("kind") != "audioscript":
            continue
        test = item.get("test")
        sec = item.get("section")
        if test is None:
            continue
        # section 可能为 null(续页) — 沿用上一次同 test 的 section
        if sec is None:
            # 找同 test 最后一个组
            last_sec = None
            for k in sorted(groups.keys(), key=lambda k: (k[0], k[1] if k[1] else 0)):
                if k[0] == test:
                    last_sec = k[1]
            if last_sec is None:
                continue
            sec = last_sec
        key = (test, sec)
        groups.setdefault(key, []).extend(item.get("audioscript_segments", []))
    return groups


def fuzzy_find(needle_words, haystack_words, start_hint=0, window_slack=None):
    """在 haystack_words[start_hint:] 里找最匹配 needle_words 前 5 词的位置。
    window_slack=None 表示从 start_hint 搜到 haystack 末尾(推荐,单调 cursor 已避免回头匹配)。
    返回 (best_index, best_ratio) — index 是 haystack 里的绝对下标。"""
    # 对短 seg(<3 词),取全 seg 作 needle;长 seg 取前 5 词
    if len(needle_words) < 3:
        needle = needle_words[:]
    else:
        needle = needle_words[:5]
    if not needle:
        return -1, 0.0
    needle_str = " ".join(needle)
    L = len(needle)
    best = (-1, 0.0)
    end = len(haystack_words) if window_slack is None \
        else min(len(haystack_words), start_hint + window_slack)
    for i in range(start_hint, max(start_hint + 1, end - L + 1)):
        hay = " ".join(w["w"] for w in haystack_words[i:i + L])
        r = SequenceMatcher(None, needle_str, hay).ratio()
        if r > best[1]:
            best = (i, r)
            if r > 0.95:
                break
    return best


_Q_INT_RE = re.compile(r"(\d+)")


def normalize_answer_markers(am):
    """Qwen 有时返回 ['Q1', 'Q2'] 字符串,统一转成 [1, 2] 整数列表。"""
    if not am:
        return []
    out = []
    for x in am:
        if isinstance(x, int):
            out.append(x)
        elif isinstance(x, str):
            m = _Q_INT_RE.search(x)
            if m:
                out.append(int(m.group(1)))
    return out


def align_one_part(part_id, audioscript_segs, whisper_data, log=print, **_):
    """全局对齐:用 SequenceMatcher 找 audioscript 词流与 whisper 词流的匹配块,
    再把每个 seg 的起始位置映射到 whisper start 时间。"""
    stream = flatten_whisper_words(whisper_data)
    # 展开 audioscript 到 word list,并记录每 seg 起始词位置
    a_words = []
    seg_starts = []  # audioscript 词序列里,每 seg 从第几个词开始
    for seg in audioscript_segs:
        seg_starts.append(len(a_words))
        a_words.extend(norm_words(seg.get("text", "")))
    seg_starts.append(len(a_words))  # 哨兵

    b_words = [w["w"] for w in stream]
    log(f"  {part_id}: {len(audioscript_segs)} seg / audioscript {len(a_words)} 词 / whisper {len(b_words)} 词")

    # 全局对齐(autojunk=False 提升准确度)
    sm = SequenceMatcher(a=a_words, b=b_words, autojunk=False)
    all_blocks = sm.get_matching_blocks()  # 最后一个 block 是 (len(a), len(b), 0) 哨兵
    # 只保留 size >= 3 的可信块,避免 1-2 词的偶合匹配主导映射
    blocks = [(a0, b0, sz) for a0, b0, sz in all_blocks if sz >= 3]
    log(f"    matching blocks(size≥3): {len(blocks)}")

    def a_to_b(pos_a, max_dist=30):
        """给 audioscript 词下标 pos_a,返回对应 whisper 词下标(-1 表示无实际匹配)。
        - 在某 block 内 → 精确插值
        - 距离最近 block < max_dist 词 → 用块边界近似
        - 否则 → -1(说明该段 audioscript 内容不在此 whisper 音频里,可能是 raw 归 test/section 错)。"""
        if not blocks:
            return -1
        # 落在某 block 内
        for a0, b0, sz in blocks:
            if a0 <= pos_a < a0 + sz:
                return b0 + (pos_a - a0)
        # 找最近 block
        best = -1
        best_dist = 10 ** 9
        for a0, b0, sz in blocks:
            end_a = a0 + sz
            if pos_a < a0:
                dist = a0 - pos_a
                cand = b0
            else:
                dist = pos_a - end_a
                cand = b0 + sz - 1
            if dist < best_dist:
                best_dist = dist
                best = cand
        return best if best_dist <= max_dist else -1

    aligned = []
    hits = misses = drops = 0
    for i, seg in enumerate(audioscript_segs):
        a_pos = seg_starts[i]
        seg_len = seg_starts[i + 1] - a_pos
        b_pos = a_to_b(a_pos)
        new = dict(seg)
        new["answer_markers"] = normalize_answer_markers(seg.get("answer_markers"))
        if b_pos >= 0 and b_pos < len(stream):
            new["start"] = round(stream[b_pos]["s"], 1)
            new["_align_via"] = "block"
            hits += 1
            aligned.append(new)
        else:
            # 该段 audioscript 完全不在 whisper 音频里 → 说明 raw 归属可能错(test/section 分类漂移)
            # 长 seg(>= 10 词)直接 drop;短 seg 保留 start=None 让下游按 speaker 顺序显示
            if seg_len >= 10:
                drops += 1
                continue
            new["start"] = None
            new["_align_via"] = "miss"
            misses += 1
            aligned.append(new)

    # 后处理:确保 start 单调不减(若某 seg start 比前面小,置 null)
    prev = None
    for s in aligned:
        if s["start"] is not None:
            if prev is not None and s["start"] < prev - 0.5:
                s["start"] = None
                s["_align_via"] = "non-monotonic"
                hits -= 1
                misses += 1
            else:
                prev = s["start"]

    log(f"    对齐 {hits} · 未对齐(短保留) {misses} · drop(长且不在音频里) {drops}")
    return aligned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book", help="册号 c14/c15/…")
    ap.add_argument("--only", help="只处理指定 part id 逗号列表,如 c14-test1-part1")
    ap.add_argument("--min-ratio", type=float, default=0.55)
    args = ap.parse_args()

    raw_path = OUT_DIR / f"{args.book}.raw.json"
    if not raw_path.exists():
        raise SystemExit(f"未找到 {raw_path},先跑 extract_listening_from_pdf.py")
    raw = load_json(raw_path)
    groups = group_audioscript_segments_by_part(raw)
    print(f"[{args.book}] 从 raw 抽到 {len(groups)} 个 (test, section) 组")

    only = None
    if args.only:
        only = {p.strip() for p in args.only.split(",") if p.strip()}

    fails = []
    for (test, section), segs in sorted(groups.items()):
        part_id = f"{args.book}-test{test}-part{section}"
        if only and part_id not in only:
            continue
        whisper_path = OUT_DIR / f"{part_id}.whisper.json"
        if not whisper_path.exists():
            print(f"  跳过 {part_id}:未找到 whisper.json")
            fails.append(part_id)
            continue
        wd = load_json(whisper_path)
        aligned = align_one_part(part_id, segs, wd, min_ratio=args.min_ratio)
        out_path = OUT_DIR / f"{part_id}.aligned.json"
        payload = {"id": part_id, "test": test, "section": section,
                   "audio": f"media/audio/{part_id}.mp3",
                   "segments": aligned}
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        print(f"  → {out_path.name}")

    print(f"\n完成。失败/缺文件: {fails}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
