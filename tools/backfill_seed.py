# -*- coding: utf-8 -*-
"""词库全量补齐:把 seed_wordlist.json 里尚未收录的高频词,逐批用 LLM 生成 aids,
校验通过后【增量合并进主词库 data/vocab-seed.json】。

安全 / 健壮性:
  - 只【追加】新词,永不覆盖已有词(按 word 小写去重)。
  - 每批生成后立即原子写盘(tmp + os.replace),中途中断也不丢已完成部分。
  - 可【断点续跑】:每次都从"当前还没收录的最高频词"接着来。
  - 校验不过的词记入 out/backfill_flagged.json 并在本次运行内跳过,不卡死。
  - 起跑前自动备份 data/vocab-seed.json → data/vocab-seed.json.bak。

用法:
    py -3 tools/backfill_seed.py                 # 跑到把 seed_wordlist 全部补齐
    py -3 tools/backfill_seed.py --max 40        # 本次最多新增 40 词(测试用)
    py -3 tools/backfill_seed.py --provider qwen # 换 Qwen
"""
import argparse
import json
import os
import shutil
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(HERE, "..", "data", "vocab-seed.json")
WORDLIST = os.path.join(HERE, "seed_wordlist.json")
OUT_DIR = os.path.join(HERE, "out")
FLAGGED = os.path.join(OUT_DIR, "backfill_flagged.json")
LOG = os.path.join(OUT_DIR, "backfill.log")

# 复用样品脚本里的 prompt / 校验 / 生成(单一真相源)
from gen_seed_sample import (  # noqa: E402
    SYSTEM_PROMPT, clean_translation, validate, make_client,
)


def load_json(path, fallback):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return fallback


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def seed_have():
    data = load_json(SEED, {"meta": {}, "words": []})
    return data, {w["word"].lower() for w in data.get("words", [])}


def pick_targets(n, have, skip):
    wl = sorted(load_json(WORDLIST, []), key=lambda x: x.get("freq_rank", 1e9))
    out = []
    for w in wl:
        word = (w.get("word") or "").strip()
        wlow = word.lower()
        if not word or wlow in have or wlow in skip:
            continue
        out.append(w)
        if len(out) >= n:
            break
    return out


def gen_batch(client, batch, max_tokens=8000):
    hint = "\n".join(
        f'{i+1}. {w["word"]}  /{w.get("phonetic","")}/  参考义: {clean_translation(w.get("translation"))}'
        for i, w in enumerate(batch)
    )
    obj, _ = client.chat_json(
        [{"role": "system", "content": SYSTEM_PROMPT},
         {"role": "user", "content": "为下面这些词生成卡片(freq_rank 用我给的值):\n" + hint}],
        max_tokens=max_tokens,
    )
    words = obj.get("words") if isinstance(obj, dict) else obj
    if not isinstance(words, list):
        return []
    by = {w["word"].lower(): w for w in batch}
    for wd in words:
        src = by.get((wd.get("word") or "").lower())
        if src:
            wd["phonetic"] = src.get("phonetic", wd.get("phonetic", ""))
            wd["freq_rank"] = src.get("freq_rank", wd.get("freq_rank"))
    return words


def merge_into_seed(new_words):
    data, have = seed_have()
    added = 0
    for wd in new_words:
        wl = (wd.get("word") or "").lower()
        if not wl or wl in have:
            continue
        data["words"].append(wd)
        have.add(wl)
        added += 1
    data.setdefault("meta", {})["generated_words"] = len(data["words"])
    tmp = SEED + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, SEED)
    return added, len(data["words"])


def save_flagged(items):
    prev = load_json(FLAGGED, [])
    prev.extend(items)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(FLAGGED, "w", encoding="utf-8") as f:
        json.dump(prev, f, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=0, help="本次最多新增多少词(0=全部)")
    ap.add_argument("--batch", type=int, default=6)
    ap.add_argument("--provider", choices=["deepseek", "qwen"], default="deepseek")
    args = ap.parse_args()

    # 起跑前备份一次
    if os.path.exists(SEED) and not os.path.exists(SEED + ".bak"):
        shutil.copyfile(SEED, SEED + ".bak")
        log(f"已备份 {SEED} → {SEED}.bak")

    data, have = seed_have()
    wl_total = len(load_json(WORDLIST, []))
    remaining0 = wl_total - len(have)
    log(f"起点: 词库 {len(have)} 词 / 词表 {wl_total};待补 {remaining0}。本次上限 {args.max or '全部'}。")

    client = make_client(args.provider)
    skip = set()
    total_added = 0
    empty_streak = 0
    batch_no = 0

    while True:
        if args.max and total_added >= args.max:
            log(f"达到本次上限 {args.max},停止。")
            break
        _, have = seed_have()
        room = args.batch if not args.max else min(args.batch, args.max - total_added)
        targets = pick_targets(room, have, skip)
        if not targets:
            log("没有待补的词了(或都进了跳过名单)。完成。")
            break
        batch_no += 1
        words_in = ", ".join(t["word"] for t in targets)
        try:
            gen = gen_batch(client, targets, max_tokens=8000)
        except SystemExit as e:
            log(f"API 出错,停止本次运行: {e}")
            break
        except Exception as e:
            log(f"第 {batch_no} 批异常({type(e).__name__}: {e}),跳过这批词。")
            skip.update(t["word"].lower() for t in targets)
            empty_streak += 1
            if empty_streak >= 5:
                log("连续 5 批失败,停止(可稍后重跑续上)。")
                break
            continue

        ok, bad = [], []
        for wd in gen:
            (bad if validate(wd) else ok).append(wd)
        # 本批里没被模型返回的目标词,也加入跳过,避免死循环
        returned = {(w.get("word") or "").lower() for w in gen}
        missing = [t for t in targets if t["word"].lower() not in returned]
        skip.update(t["word"].lower() for t in missing)
        skip.update(w["word"].lower() for w in bad)

        added, seed_total = merge_into_seed(ok)
        total_added += added
        if bad:
            save_flagged([{"word": w.get("word"), "problems": validate(w)} for w in bad])
        if added == 0 and not ok:
            empty_streak += 1
        else:
            empty_streak = 0
        log(f"第 {batch_no} 批 [{words_in}] → +{added} 词(词库共 {seed_total});"
            f"校验不过 {len(bad)},缺 {len(missing)};累计新增 {total_added}。")
        if empty_streak >= 5:
            log("连续多批无产出,停止。")
            break

    if hasattr(client, "report"):
        log(client.report())
    _, have = seed_have()
    log(f"结束。词库现有 {len(have)} 词。")


if __name__ == "__main__":
    main()
