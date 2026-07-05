# -*- coding: utf-8 -*-
"""统计剑 14-19 阅读+听力真题里的词频,给 data/vocab-seed.json 里 1081 词
追加 bands 分级字段(top-N / reading-high / listening-high / cefr-* / rare)。

用法:
    python tools/analyze_word_freq.py                # 就地更新 vocab-seed.json
    python tools/analyze_word_freq.py --dry-run      # 只打印统计,不写盘

Bands 分级规则:
- top-100 / top-300 / top-500 / top-1000:按 reading+listening 合并频次降序排名
- reading-high:reading corpus 中出现 ≥ 5 次
- listening-high:listening corpus 中出现 ≥ 5 次
- cefr-B1/B2/C1/C2:沿用 vocab-seed 已有的 cefr 字段
- rare:freq_rank > 5000(供参考)

数据源:
- data/passages/*.json 里 sentences[].en 全文分词 + 每篇 phrases
- data/listening/*.json 里 segments[].en 全文分词
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_PATH = ROOT / "data" / "vocab-seed.json"
PASSAGES_DIR = ROOT / "data" / "passages"
LISTENING_DIR = ROOT / "data" / "listening"

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def normalize(w):
    """极简词形还原(与 word-popup.js lemmaCandidates 逻辑一致的简化版)。
    只做常见后缀去除,返回小写基本形式。"""
    w = w.lower().rstrip("'s").rstrip("'")
    # 后缀试探
    for suf in ("ies",):
        if w.endswith(suf) and len(w) > len(suf) + 1:
            return w[: -len(suf)] + "y"
    for suf in ("ing", "ied", "est"):
        if w.endswith(suf) and len(w) > len(suf) + 1:
            return w[: -len(suf)]
    for suf in ("ed", "es", "er"):
        if w.endswith(suf) and len(w) > len(suf) + 1:
            return w[: -len(suf)]
    if w.endswith("s") and len(w) > 2:
        return w[:-1]
    return w


def tokenize(text):
    """把英文段落切成词,过滤纯数字/单字符;返回小写词 list。"""
    tokens = []
    for m in WORD_RE.finditer(text or ""):
        tok = m.group(0).lower()
        if len(tok) < 2:
            continue
        tokens.append(tok)
    return tokens


def count_reading():
    """遍历 data/passages/*.json,累计每词出现次数。"""
    counter = Counter()
    if not PASSAGES_DIR.exists():
        return counter
    n_files = 0
    for f in sorted(PASSAGES_DIR.glob("*.json")):
        if f.name == "sample.json":
            continue
        d = load_json(f)
        for s in d.get("sentences", []):
            for tok in tokenize(s.get("en", "")):
                counter[tok] += 1
        n_files += 1
    print(f"  reading: 扫 {n_files} 篇 → 累计 {sum(counter.values())} 词元 / 独立 {len(counter)}")
    return counter


def count_listening():
    """遍历 data/listening/*.json(不含 index.json),累计每词。"""
    counter = Counter()
    if not LISTENING_DIR.exists():
        return counter
    n_files = 0
    for f in sorted(LISTENING_DIR.glob("*.json")):
        if f.name == "index.json" or f.name.startswith("_"):
            continue
        d = load_json(f)
        for s in d.get("segments", []):
            for tok in tokenize(s.get("en", "")):
                counter[tok] += 1
        n_files += 1
    print(f"  listening: 扫 {n_files} parts → 累计 {sum(counter.values())} 词元 / 独立 {len(counter)}")
    return counter


def merge_freq(r_counter, l_counter):
    """为每词汇总 reading + listening 的原始/词形还原命中数。
    返回 {lemma: {reading, listening, total, forms: [变形集]}}。"""
    merged = {}
    for src_name, ctr in (("reading", r_counter), ("listening", l_counter)):
        for tok, n in ctr.items():
            lem = normalize(tok)
            m = merged.setdefault(lem, {"reading": 0, "listening": 0, "forms": set()})
            m[src_name] = m.get(src_name, 0) + n
            m["forms"].add(tok)
    for m in merged.values():
        m["total"] = m.get("reading", 0) + m.get("listening", 0)
        m["forms"] = sorted(m["forms"])
    return merged


def rank_top_n(merged, N):
    """按 total 降序排序,取前 N 个 lemma,返回 set。"""
    sorted_lemmas = sorted(merged.items(), key=lambda kv: -kv[1]["total"])
    return set(lem for lem, _ in sorted_lemmas[:N])


def compute_bands(seed_words, merged):
    """给每个 seed 词计算 bands 数组。返回新的 seed_words(替换 in place 也可)。"""
    top100 = rank_top_n(merged, 100)
    top300 = rank_top_n(merged, 300)
    top500 = rank_top_n(merged, 500)
    top1000 = rank_top_n(merged, 1000)

    stats = {"top-100": 0, "top-300": 0, "top-500": 0, "top-1000": 0,
             "reading-high": 0, "listening-high": 0,
             "cefr-B1": 0, "cefr-B2": 0, "cefr-C1": 0, "cefr-C2": 0,
             "rare": 0, "unseen": 0}

    for w in seed_words:
        bands = []
        lem = normalize(w["word"])
        m = merged.get(lem) or merged.get(w["word"].lower())
        # 顶级频次层
        if m:
            if lem in top100 or w["word"].lower() in top100:
                bands.append("top-100"); stats["top-100"] += 1
            elif lem in top300:
                bands.append("top-300"); stats["top-300"] += 1
            elif lem in top500:
                bands.append("top-500"); stats["top-500"] += 1
            elif lem in top1000:
                bands.append("top-1000"); stats["top-1000"] += 1
            # 单侧高频
            if m.get("reading", 0) >= 5:
                bands.append("reading-high"); stats["reading-high"] += 1
            if m.get("listening", 0) >= 5:
                bands.append("listening-high"); stats["listening-high"] += 1
        else:
            stats["unseen"] += 1
        # CEFR 沿用
        cefr = w.get("cefr")
        if cefr:
            tag = f"cefr-{cefr}"
            bands.append(tag)
            if tag in stats:
                stats[tag] += 1
        # rare 参考
        fr = w.get("freq_rank")
        if isinstance(fr, int) and fr > 5000:
            bands.append("rare"); stats["rare"] += 1
        # 存频次原始数据(供 UI 展示"真题中出现 N 次")
        if m:
            w["freq_reading"] = m.get("reading", 0)
            w["freq_listening"] = m.get("listening", 0)
        else:
            w["freq_reading"] = 0
            w["freq_listening"] = 0
        w["bands"] = bands

    return seed_words, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    print("统计阅读语料 …")
    r_counter = count_reading()
    print("统计听力语料 …")
    l_counter = count_listening()

    print(f"合并词频 …")
    merged = merge_freq(r_counter, l_counter)
    print(f"  合并独立 lemma: {len(merged)}")

    print("加载 vocab-seed.json …")
    seed = load_json(SEED_PATH)
    words = seed.get("words", [])
    print(f"  已有 seed 词: {len(words)}")

    words, stats = compute_bands(words, merged)
    print("\nbands 分布:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    if args.dry_run:
        print("\n(dry-run,未写盘)")
        return 0

    seed["words"] = words
    seed.setdefault("meta", {})["bands_computed_at"] = "auto"
    with open(SEED_PATH, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)
    print(f"\n已更新 {SEED_PATH}")

    # 附带:输出高频但不在 seed 里的 candidates(前 200 个),供人工审阅
    seed_lemmas = set(normalize(w["word"]) for w in words)
    external = [(lem, m) for lem, m in merged.items()
                if lem not in seed_lemmas and m["total"] >= 3]
    external.sort(key=lambda kv: -kv[1]["total"])
    cand_path = ROOT / "data" / "vocab-seed-candidates.json"
    payload = {
        "note": "真题里出现 ≥3 次但不在 vocab-seed.json 里的 lemma 候选(供人工筛选)",
        "top": [
            {"lemma": lem, "total": m["total"],
             "reading": m.get("reading", 0), "listening": m.get("listening", 0),
             "forms": list(m["forms"])[:5]}
            for lem, m in external[:200]
        ],
    }
    with open(cand_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"外部高频候选 top-{min(200, len(external))} 已输出 → {cand_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
