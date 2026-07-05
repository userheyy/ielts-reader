# -*- coding: utf-8 -*-
"""批量生成题目级同义替换映射(paraphrase 字段) — DeepSeek 管线。

用法:
    py tools/gen_paraphrase_map.py c14-test1-p1 [--force]

输出 tools/out/{id}.para.json,人工抽查后由 merge_deep.py 合并。
硬校验:每组 pairs 的 p 必须逐字(忽略大小写)出现在 evidence 句的 en 中。
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deepseek_client import DeepSeekClient  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "tools" / "out"
KINDS = {"syn", "verbatim", "para", "neg"}

SYSTEM = """你是一名雅思阅读老师,专教"同义替换"(paraphrase)——雅思阅读定位答案的核心技能。
给你一道题(题干+标准答案)和它的答案定位句(原文),请输出该题的替换映射 JSON:

{"pairs":[{"q":"<题干中的关键词/词组>","p":"<原文句中对应的词/词组,必须逐字复制原文句里的文字>",
  "kind":"syn|verbatim|para|neg","note":"<一句话向基础弱的学生讲清这组替换>"}],
 "trap":"<干扰项/易错点说明,没有则空字符串>",
 "explain":"<一两句话讲定位思路:先抓题干什么词,到原文找什么>"}

规则:
- kind: syn=同义词替换 / verbatim=原词复现(定位锚点) / para=句式改写 / neg=反向表达;
- p 必须是"逐字"从原文句复制的连续文字(大小写可不同),绝不许改写;
- pairs 给 1-4 组,优先给真正帮定位的关键替换;
- 全中文 note/explain,大白话。只输出 JSON。"""


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_pairs(para, evidence_en):
    errs = []
    pairs = para.get("pairs")
    if not isinstance(pairs, list) or not pairs:
        return ["pairs 缺失或为空"]
    low = evidence_en.lower()
    for pr in pairs:
        if pr.get("kind") not in KINDS:
            errs.append(f"kind 非法: {pr.get('kind')!r}")
        p = pr.get("p", "")
        if not p or p.lower() not in low:
            errs.append(f"p 未逐字出现在原文句中: {p!r}")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("passage_id")
    ap.add_argument("--force", action="store_true", help="已有 paraphrase 的题也重生成")
    args = ap.parse_args()

    passage = load_json(ROOT / "data" / "passages" / f"{args.passage_id}.json")
    id2sentence = {s["id"]: s for s in passage["sentences"]}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{args.passage_id}.para.json"
    out = {"passage_id": args.passage_id, "items": {}}
    if out_path.exists():
        out = load_json(out_path)

    todo = []
    for group in passage.get("questions", []):
        for item in group.get("items", []):
            if item.get("paraphrase") and not args.force:
                continue
            ev = item.get("evidence_sentence")
            if ev not in id2sentence:
                print(f"  跳过第{item.get('number')}题:无有效 evidence_sentence")
                continue
            todo.append((group, item, id2sentence[ev]))

    if not todo:
        print("没有需要处理的题目")
        return

    client = DeepSeekClient()
    print(f"{args.passage_id}: 待生成 {len(todo)} 题 → {out_path}")
    fails = []
    for i, (group, item, ev) in enumerate(todo, 1):
        user = f"""【题型】{group.get('type', '')}({group.get('title', '')})
【题干】{item['prompt']}
【标准答案】{item['answer']}
【答案定位句(原文)】{ev['en']}
【定位句中文】{ev['zh']}"""
        messages = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": user}]
        print(f"[{i}/{len(todo)}] 第{item['number']}题")
        para, _ = client.chat_json(messages, max_tokens=1200)
        errs = check_pairs(para, ev["en"])
        if errs:
            retry = messages + [
                {"role": "assistant", "content": json.dumps(para, ensure_ascii=False)},
                {"role": "user", "content": "未通过校验:\n- " + "\n- ".join(errs)
                 + "\n注意 p 必须逐字复制原文句中的连续文字。请重新输出 JSON。"}]
            para, _ = client.chat_json(retry, max_tokens=1200)
            errs = check_pairs(para, ev["en"])
        if errs:
            print(f"  仍未通过: {errs}")
            fails.append((item["number"], errs))
        else:
            out["items"][str(item["number"])] = para
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=1)

    if fails:
        err_path = OUT_DIR / f"{args.passage_id}.para-errors.txt"
        with open(err_path, "w", encoding="utf-8") as f:
            for num, errs in fails:
                f.write(f"第{num}题:\n" + "\n".join("  - " + e for e in errs) + "\n")
        print(f"[!] {len(fails)} 题未通过 → {err_path}")
    print(f"完成:成功 {len(out['items'])} 题,失败 {len(fails)} 题")
    print(client.report())


if __name__ == "__main__":
    main()
