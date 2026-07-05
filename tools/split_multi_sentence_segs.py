# -*- coding: utf-8 -*-
"""把 data/listening/*.json 里"一 seg 多句"的 segments 拆成"一句一 seg"。

问题:56% 的 seg(1069/1895)是一整个 speaker turn 合成的段落,如
"Good morning. What can I do for you?"—— 精听逐句体验要求每句独立。

拆分流程(每 part 一遍):
1) backup 原文件到 tools/out/listening/{part}.pre-split.json
2) 遍历 segments,按句子分割器(regex + 缩写 whitelist)拆 en
3) 每句用 whisper 词级 timestamps fuzzy-match 起始词 → start
4) 重编 seg id(1..N),旧→新 id 映射
5) 更新 questions[].items[].evidence_segment 到新 id
   (优先按 answer 文本匹配 seg.en;否则沿用旧 turn 的第一句)
6) 分配 zh:整 turn 的 zh 挂在**第一句**新 seg;其他新 seg zh=""
7) 分配 answers:answers 里的题号,按题目答案文本在哪句 en 里出现分配
8) 写回 data/listening/{part}.json

用法:
    py tools/split_multi_sentence_segs.py                     # 全库
    py tools/split_multi_sentence_segs.py --only c14-test2-l1 # 单 part pilot
    py tools/split_multi_sentence_segs.py --dry-run           # 只统计不写盘
"""
import argparse
import json
import os
import re
import shutil
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "listening"
WHISPER_DIR = ROOT / "tools" / "out" / "listening"
BACKUP_DIR = ROOT / "tools" / "out" / "listening"

# 缩写列表:遇到这些结尾的 "." 后不视作句子结束
ABBRS = {"mr", "mrs", "ms", "dr", "prof", "st", "rd", "ave", "e.g", "i.e", "etc", "vs",
         "u.s", "u.k", "no", "vol", "ph.d", "b.a", "m.a", "m.d", "jr", "sr", "inc", "ltd"}

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def split_sentences(text):
    """把英文段落切成句子列表。避开缩写。"""
    if not text or not text.strip():
        return []
    text = text.strip()
    # 找 [.!?] + 空白 + [大写] 的边界
    out = []
    buf = []
    i = 0
    while i < len(text):
        ch = text[i]
        buf.append(ch)
        if ch in ".!?" and i + 1 < len(text):
            # 判断后续是否句子分隔(空白 + 大写字母开头 or 引号 + 大写)
            j = i + 1
            while j < len(text) and text[j] in " \t\n":
                j += 1
            if j < len(text) and (text[j].isupper() or text[j] in '"“‘\''):
                # 检查是否缩写:向前找最近的字母词
                last_word = re.findall(r"[A-Za-z.]+", "".join(buf))
                last = last_word[-1].lower().rstrip(".").rstrip(".") if last_word else ""
                if last not in ABBRS:
                    out.append("".join(buf).strip())
                    buf = []
                    i = j
                    continue
        i += 1
    if buf:
        s = "".join(buf).strip()
        if s:
            out.append(s)
    return out


def tokens(text):
    return [m.group(0).lower() for m in WORD_RE.finditer(text or "")]


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def align_starts(sentences, whisper_data):
    """给拆分后的 N 个句子,用 SequenceMatcher 全局对齐 whisper 词流,返回每句 start(可能 null)。"""
    # 铺平所有句子的词序列 + 记录每句起始词下标
    a_words = []
    starts_a = []
    for s in sentences:
        starts_a.append(len(a_words))
        a_words.extend(tokens(s))
    # 铺平 whisper 词流
    stream = []
    for seg in (whisper_data or {}).get("segments", []):
        for w in seg.get("words", []):
            tok = (w.get("w") or "").strip().lower()
            for m in WORD_RE.finditer(tok):
                stream.append({"w": m.group(0), "s": w.get("s", 0.0)})
    if not stream or not a_words:
        return [None] * len(sentences)
    b_words = [x["w"] for x in stream]
    sm = SequenceMatcher(a=a_words, b=b_words, autojunk=False)
    blocks = [(a0, b0, sz) for a0, b0, sz in sm.get_matching_blocks() if sz >= 3]
    if not blocks:
        return [None] * len(sentences)

    def a_to_b(pos_a, max_dist=40):
        for a0, b0, sz in blocks:
            if a0 <= pos_a < a0 + sz:
                return b0 + (pos_a - a0)
        best, best_d = -1, 10 ** 9
        for a0, b0, sz in blocks:
            end_a = a0 + sz
            if pos_a < a0:
                d, cand = a0 - pos_a, b0
            else:
                d, cand = pos_a - end_a, b0 + sz - 1
            if d < best_d:
                best_d, best = d, cand
        return best if best_d <= max_dist else -1

    out = []
    prev = None
    for i, pa in enumerate(starts_a):
        bp = a_to_b(pa)
        if 0 <= bp < len(stream):
            st = round(stream[bp]["s"], 1)
            if prev is not None and st < prev - 0.5:
                st = None  # 非单调回退,置 null
            if st is not None:
                prev = st
            out.append(st)
        else:
            out.append(None)
    return out


def find_seg_for_answer(sentences, answer):
    """给答案文本,在拆出的句子里找最匹配的下标。空/未找到返回 -1。"""
    if not answer:
        return -1
    ans = re.sub(r"[(){}\[\]/]", "", answer).strip().lower()
    if not ans:
        return -1
    # 严格逐字匹配
    for i, s in enumerate(sentences):
        if ans in s.lower():
            return i
    # 松散:去括号后核心词匹配
    core = re.sub(r"\s+", " ", ans).split()[0] if ans.split() else ""
    if core and len(core) >= 3:
        for i, s in enumerate(sentences):
            if core in s.lower():
                return i
    return -1


def process_part(part_id, dry_run=False, log=print):
    data_path = DATA_DIR / f"{part_id}.json"
    audio_id = part_id.replace("-l", "-part")
    whisper_path = WHISPER_DIR / f"{audio_id}.whisper.json"
    if not data_path.exists():
        log(f"  跳过 {part_id}:data 文件不存在")
        return None
    d = load_json(data_path)
    whisper = load_json(whisper_path) if whisper_path.exists() else None

    old_segs = d.get("segments", [])
    if not old_segs:
        log(f"  跳过 {part_id}:无 segments")
        return None

    # 备份
    if not dry_run:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(data_path, BACKUP_DIR / f"{part_id}.pre-split.json")

    new_segs = []
    old2new_first = {}  # 旧 seg.id → 拆出的第一个新 seg.id(用于 evidence 兜底)
    old2new_by_answer = {}  # (旧 seg.id, 答案文本) → 新 seg.id(用于 evidence 精确)
    split_count = 0

    for old in old_segs:
        old_id = old.get("id")
        en = (old.get("en") or "").strip()
        zh = (old.get("zh") or "").strip()
        speaker = old.get("speaker") or ""
        old_answers = list(old.get("answers") or [])
        old_start = old.get("start")
        sents = split_sentences(en)
        if len(sents) <= 1:
            # 不拆:直接沿用
            new_id = len(new_segs) + 1
            old2new_first[old_id] = new_id
            for a in old_answers:
                old2new_by_answer[(old_id, a)] = new_id
            new_segs.append({
                "id": new_id, "start": old_start, "speaker": speaker,
                "en": en, "zh": zh, "words": list(old.get("words") or []),
                "answers": old_answers,
            })
            continue

        # 拆 en 成 N 句;用 whisper align 出每句 start(第一句沿用 old_start 若 whisper 拿不到)
        starts = align_starts(sents, whisper)
        if starts[0] is None:
            starts[0] = old_start

        # 分配 zh:整段 zh 挂第一句(不做智能拆分,后续可 DeepSeek 补)
        # 分配 words:整个 turn 的 words 全放第一句(避免遗漏)
        # 分配 answers:对每个旧答案,找答案文本在哪句 en 里 → 新 seg id
        answer_to_local = {}  # 答案题号 → 本 turn 内的句下标
        # 找该 turn 关联的题:从 d.questions 里 evidence_segment == old_id 的 items
        turn_items = []
        for grp in d.get("questions", []):
            for it in grp.get("items", []):
                if it.get("evidence_segment") == old_id:
                    turn_items.append(it)
        for it in turn_items:
            local_idx = find_seg_for_answer(sents, it.get("answer") or "")
            if local_idx < 0:
                local_idx = 0
            answer_to_local[it.get("number")] = local_idx

        # 拆分后每句一 seg
        turn_first_new_id = len(new_segs) + 1
        for i, sent in enumerate(sents):
            new_id = len(new_segs) + 1
            seg = {
                "id": new_id, "start": starts[i], "speaker": speaker,
                "en": sent, "zh": zh if i == 0 else "",
                "words": list(old.get("words") or []) if i == 0 else [],
                "answers": [],
            }
            new_segs.append(seg)
        # 分配 answers 到对应新 seg
        for num in old_answers:
            local = answer_to_local.get(num, 0)
            new_seg_id = turn_first_new_id + local
            if new_seg_id - 1 < len(new_segs):
                new_segs[new_seg_id - 1]["answers"].append(num)
                old2new_by_answer[(old_id, num)] = new_seg_id
        # 记录 fallback
        old2new_first[old_id] = turn_first_new_id
        split_count += 1

    # 更新 questions.items.evidence_segment
    for grp in d.get("questions", []):
        for it in grp.get("items", []):
            old_ev = it.get("evidence_segment")
            if old_ev is None:
                continue
            num = it.get("number")
            key = (old_ev, num)
            if key in old2new_by_answer:
                it["evidence_segment"] = old2new_by_answer[key]
            elif old_ev in old2new_first:
                it["evidence_segment"] = old2new_first[old_ev]

    d["segments"] = new_segs
    stats = {"old_count": len(old_segs), "new_count": len(new_segs),
             "splits": split_count, "growth": len(new_segs) - len(old_segs)}
    log(f"  {part_id}: {stats['old_count']} → {stats['new_count']} seg (+{stats['growth']}, {stats['splits']} 处拆分)")
    if not dry_run:
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="只处理指定 part id 逗号分隔")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    files = sorted(
        f for f in os.listdir(DATA_DIR)
        if f.endswith(".json") and f != "index.json" and not f.startswith("_")
    )
    if args.only:
        want = set(x.strip() for x in args.only.split(","))
        files = [f for f in files if f.replace(".json", "") in want]
    total_old = total_new = total_split = 0
    for f in files:
        part = f.replace(".json", "")
        s = process_part(part, dry_run=args.dry_run)
        if s:
            total_old += s["old_count"]
            total_new += s["new_count"]
            total_split += s["splits"]
    print(f"\n合计:{total_old} → {total_new} seg (+{total_new - total_old}),{total_split} 处拆分。"
          + (" [dry-run,未写盘]" if args.dry_run else ""))


if __name__ == "__main__":
    sys.exit(main())
