# -*- coding: utf-8 -*-
"""DeepSeek 把 L3(Qwen-VL 官方英文)+ L4(whisper 时间戳)结构化成
data/listening/{id}.json,与 c14-test1-l1.json 同 shape。

输入:
    tools/out/listening/{book}.raw.json           Qwen-VL 全书抽取
    tools/out/listening/{part_id}.aligned.json    per-part 带 start 的 segments

输出:
    data/listening/{part_id}.json                 与 c14-test1-l1.json 同 shape

Few-shot:c14-test1-l1.json 的现成手工数据。

用法:
    py tools/gen_listening_transcript.py c14 --only c14-test1-l1  # pilot 单 part
    py tools/gen_listening_transcript.py c14                       # 一册所有 part
    py tools/gen_listening_transcript.py c14 --dry-run             # 只组装骨架,不调 DeepSeek
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deepseek_client import DeepSeekClient  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "tools" / "out" / "listening"
DATA_DIR = ROOT / "data" / "listening"

BATCH_SIZE = 8  # 每次让 DeepSeek 翻译多少 seg,平衡上下文与吞吐


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def load_fewshot():
    """从已有的 c14-test1-l1.json 挖 8 段作 few-shot 样例。"""
    p = DATA_DIR / "c14-test1-l1.json"
    if not p.exists():
        return None
    d = load_json(p)
    return d["segments"][:8]


# -------- 组装骨架 --------

def collect_questions_for_part(raw, test, part):
    """从 raw.json 拼出该 part 的 questions[] 结构(只取 topic=listening)。
    raw.pages[i].question_items 里可能含很多题(听力+阅读+写作混合),按 number+topic 归到对应 part。
    """
    number_lo = (part - 1) * 10 + 1
    number_hi = part * 10

    # 收集 listening question_items(限制到本 part 题号,去重)
    items_by_num = {}
    for _pn, item in raw.get("pages", {}).items():
        if item.get("kind") != "question":
            continue
        if item.get("test") != test:
            continue
        for q in item.get("question_items", []) or []:
            if q.get("topic") != "listening":
                continue
            n = q.get("number")
            if isinstance(n, int) and number_lo <= n <= number_hi:
                # 同题号在多页出现取第一个非空 prompt
                if n not in items_by_num or (not items_by_num[n].get("prompt") and q.get("prompt")):
                    items_by_num[n] = q

    # 收集 listening 答案(topic=listening)
    answers = {}
    for _pn, item in raw.get("pages", {}).items():
        if item.get("kind") != "answer_key":
            continue
        # answer_key 页可能不带 test 字段;若带且不等则跳过
        pt = item.get("test")
        if pt is not None and pt != test:
            continue
        for a in item.get("answer_entries", []) or []:
            if a.get("topic") != "listening":
                continue
            n = a.get("number")
            if isinstance(n, int) and number_lo <= n <= number_hi:
                answers[n] = a.get("answer", "")

    items_out = []
    for n in sorted(items_by_num.keys()):
        q = items_by_num[n]
        items_out.append({
            "number": n,
            "prompt": q.get("prompt", ""),
            "answer": answers.get(n, ""),
            "evidence_segment": None,
            "paraphrase": None,
        })
    if items_out:
        # 组一个默认 group;真实分组(如 1-4/5-10)靠后续人工微调 title/type
        return [{
            "title": f"Questions {number_lo}–{number_hi}",
            "type": (items_by_num[items_out[0]["number"]].get("hint") or "").lower() or "mixed",
            "instructions": [],
            "items": items_out,
        }]
    return []


def build_skeleton(part_id, book, test, part, aligned, raw):
    """把 aligned segments + raw questions 组装成 c14-test1-l1 同 shape 的骨架。
    zh/words/paraphrase 均置空,由 DeepSeek 填充。"""
    segs = []
    for i, s in enumerate(aligned["segments"], 1):
        seg = {
            "id": i,
            "start": s.get("start"),
            "speaker": s.get("speaker") or "",
            "en": s.get("text", ""),
            "zh": "",
            "words": [],
            "answers": list(s.get("answer_markers", []) or []),
        }
        segs.append(seg)

    questions = collect_questions_for_part(raw, test, part)
    # 反推 evidence_segment:优先"答案文本"出现在 seg.en 里的 seg;fallback 最后一个含 Q 标记的 seg
    for grp in questions:
        for q in grp["items"]:
            n = q["number"]
            ans = (q.get("answer") or "").strip().lower()
            # 去除答案里的括号/斜杠(如 "10(th) September" / "blond(e)" 等)
            import re as _re
            ans_core = _re.sub(r"[(){}\[\]/]", "", ans).strip()
            candidates = [s for s in segs if n in (s.get("answers") or [])]
            if not candidates:
                continue
            chosen = None
            # 1) 答案文本(去括号后)出现在 seg.en 里
            if ans_core:
                for s in candidates:
                    if ans_core and ans_core.lower() in s["en"].lower():
                        chosen = s["id"]; break
            # 2) fallback:候选里最后一个(答案通常出现在段末)
            if chosen is None:
                chosen = candidates[-1]["id"]
            q["evidence_segment"] = chosen

    return {
        "id": part_id,
        "source": f"剑桥雅思{book[1:]} · Test {test} · Part {part}",
        "title": "",   # DeepSeek 生成
        "audio": f"media/audio/{part_id.replace('-l', '-part')}.mp3",
        "segments": segs,
        "questions": questions,
    }


# -------- DeepSeek 提示词 --------

SEG_SYSTEM = """你是雅思听力老师。给你若干段听力英文原文,请为每段:
- 生成一句地道中文翻译(自然口语,不要机翻腔);
- 挑 0-3 个雅思听力 4.5-6.5 分学生的考点/生词(过难/过简单的词都跳过),每词给 w/pos/def。

严格输出 JSON:
{"items": [{"id": <seg id>, "zh": "…", "words":[{"w":"…","pos":"…","def":"…"}]}]}
"""

PARA_SYSTEM = """你是雅思听力老师,任务是给一道听力题标注"同义替换"映射。
给你:
- 题干 prompt
- 标准答案 answer
- 定位句 evidence_en(听力原文)

输出严格 JSON:
{"pairs":[{"q":"<题干关键词>","p":"<原文里逐字复制的对应词/短语>","kind":"syn|verbatim|para|neg","note":"一句话向 4.5-6 分学生讲清"}],
 "explain":"一两句话讲怎么定位"}

规则:
- p 必须是从 evidence_en 里"逐字"截取的连续文字(大小写可不同),不允许改写。
- 只做真正帮定位的替换,1-3 对足够。
- 全中文,只输出 JSON。"""


# -------- DeepSeek 调用 --------

def gen_seg_zh_words(client, skeleton, fewshot, batch_size=BATCH_SIZE):
    """逐批让 DeepSeek 为每 seg 生成 zh + words。"""
    segs = skeleton["segments"]
    fs_text = ""
    if fewshot:
        fs = [{"id": i+1, "zh": s["zh"], "words": s["words"]}
              for i, s in enumerate(fewshot[:5])]
        fs_ens = [s["en"] for s in fewshot[:5]]
        fs_text = ("# few-shot 示例(输入 5 段 en → 输出 items)\n"
                   f"输入 en: {json.dumps(fs_ens, ensure_ascii=False)}\n"
                   f"输出: {json.dumps({'items': fs}, ensure_ascii=False)}\n\n")
    for i in range(0, len(segs), batch_size):
        chunk = segs[i:i + batch_size]
        payload = [{"id": s["id"], "speaker": s["speaker"], "en": s["en"]}
                   for s in chunk]
        user = (fs_text +
                f"现在请翻译下面 {len(chunk)} 段:\n" +
                json.dumps(payload, ensure_ascii=False))
        messages = [{"role": "system", "content": SEG_SYSTEM},
                    {"role": "user", "content": user}]
        try:
            obj, _ = client.chat_json(messages, max_tokens=4096)
        except SystemExit as e:
            print(f"    seg batch [{i}-{i+len(chunk)}] FAIL: {e}")
            continue
        by_id = {it["id"]: it for it in obj.get("items", []) if "id" in it}
        for s in chunk:
            it = by_id.get(s["id"])
            if it:
                s["zh"] = it.get("zh", "") or s["zh"]
                s["words"] = it.get("words", []) or s["words"]
        print(f"    seg batch [{i+1}-{i+len(chunk)}] OK")


def gen_paraphrases(client, skeleton):
    """逐题让 DeepSeek 生成 paraphrase,严格 p 逐字校验。"""
    id2seg = {s["id"]: s for s in skeleton["segments"]}
    KINDS = {"syn", "verbatim", "para", "neg"}
    for grp in skeleton["questions"]:
        for q in grp["items"]:
            ev_id = q.get("evidence_segment")
            if ev_id is None or ev_id not in id2seg:
                continue
            ev_en = id2seg[ev_id]["en"]
            user = (f"【题干】{q['prompt']}\n【标准答案】{q['answer']}\n"
                    f"【定位句 evidence_en】{ev_en}")
            messages = [{"role": "system", "content": PARA_SYSTEM},
                        {"role": "user", "content": user}]
            try:
                para, _ = client.chat_json(messages, max_tokens=800)
            except SystemExit as e:
                print(f"    题{q['number']} FAIL: {e}")
                continue
            # 校验 p 逐字
            pairs = para.get("pairs") or []
            good_pairs = []
            for pr in pairs:
                p = pr.get("p", "")
                kind = pr.get("kind", "")
                if not p or kind not in KINDS:
                    continue
                if p.lower() not in ev_en.lower():
                    continue  # 逐字不通过,丢弃
                good_pairs.append(pr)
            if good_pairs:
                q["paraphrase"] = {"pairs": good_pairs,
                                   "explain": para.get("explain", "")}
                print(f"    题{q['number']} OK ({len(good_pairs)}/{len(pairs)} 对)")
            else:
                print(f"    题{q['number']} 无通过 pair (原文 {len(pairs)} 对全 fail 逐字)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book", help="册号 c14 …")
    ap.add_argument("--only", help="只处理指定 part id 逗号列表,如 c14-test1-l1")
    ap.add_argument("--dry-run", action="store_true", help="只组装骨架,不调 DeepSeek")
    ap.add_argument("--out-dir", default=None,
                    help="输出目录,默认写 data/listening/;pilot 可指定 tools/out/listening 避免覆盖 ground truth")
    args = ap.parse_args()

    out_root = Path(args.out_dir) if args.out_dir else DATA_DIR

    raw = load_json(OUT_DIR / f"{args.book}.raw.json")
    fewshot = load_fewshot()

    only = None
    if args.only:
        only = {p.strip() for p in args.only.split(",") if p.strip()}

    client = None if args.dry_run else DeepSeekClient()

    # 遍历本册所有 aligned.json
    for aligned_path in sorted(OUT_DIR.glob(f"{args.book}-*.aligned.json")):
        part_id = aligned_path.stem.replace(".aligned", "")
        # part_id 形如 c14-test1-part1
        # 目标 id 形如 c14-test1-l1
        target_id = part_id.replace("-part", "-l")
        if only and target_id not in only:
            continue
        parts = part_id.split("-")
        test = int(parts[1][4:])
        part_num = int(parts[2][4:])
        aligned = load_json(aligned_path)
        skeleton = build_skeleton(target_id, args.book, test, part_num, aligned, raw)
        print(f"\n[{target_id}] 骨架: {len(skeleton['segments'])} seg / "
              f"{sum(len(g['items']) for g in skeleton['questions'])} 题")
        if not args.dry_run:
            print("  DeepSeek: seg zh + words …")
            gen_seg_zh_words(client, skeleton, fewshot)
            print("  DeepSeek: paraphrase …")
            gen_paraphrases(client, skeleton)
        out_path = out_root / f"{target_id}.json"
        out_root.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(skeleton, f, ensure_ascii=False, indent=1)
        print(f"  → {out_path}")

    if client:
        print(client.report())


if __name__ == "__main__":
    main()
