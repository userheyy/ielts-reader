# -*- coding: utf-8 -*-
"""
把 tools/quiz_batch_*.json 的题目幂等合并进 data/quiz-bank.json。

- 幂等：已存在的 word 自动跳过，可反复运行。
- 每题校验 6 个必填字段(word/pos/def/sentence/sentence_zh/explain)且 sentence 含 ___ 挖空。
- 追加后更新 meta.count；generated_batches 置为已合并的最大批号(由文件名 quiz_batch_NN 推断)。

用法:
    python tools/merge_quiz_batches.py            # 合并 tools/ 下所有 quiz_batch_*.json
    python tools/merge_quiz_batches.py 02 03      # 只合并指定批号
"""
import sys, io, os, json, re, glob

# Windows GBK 控制台下正常打印中文/emoji
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(ROOT, "data", "quiz-bank.json")
TOOLS = os.path.join(ROOT, "tools")
REQUIRED = ["word", "pos", "def", "sentence", "sentence_zh", "explain"]


def batch_files(selectors):
    """返回 [(batch_no:int, path)]，按批号升序。selectors 为空则取全部。"""
    out = []
    for p in glob.glob(os.path.join(TOOLS, "quiz_batch_*.json")):
        m = re.search(r"quiz_batch_(\d+)\.json$", os.path.basename(p))
        if not m:
            continue
        no = int(m.group(1))
        if selectors and str(no) not in selectors and m.group(1) not in selectors:
            continue
        out.append((no, p))
    return sorted(out)


def validate(q, where):
    for k in REQUIRED:
        if k not in q or not str(q[k]).strip():
            raise ValueError(f"{where}: 缺少/为空字段 {k} (word={q.get('word')})")
    if "___" not in q["sentence"]:
        raise ValueError(f"{where}: sentence 无 ___ 挖空 (word={q['word']})")


def main():
    selectors = set(sys.argv[1:])  # 如 "02" "2"；batch_files 里两种形式都比较

    with open(BANK, encoding="utf-8") as f:
        bank = json.load(f)
    questions = bank.get("questions", [])
    existing = {q["word"] for q in questions}

    added_total = 0
    merged_batch_nos = []
    for no, path in batch_files(selectors):
        with open(path, encoding="utf-8") as f:
            batch = json.load(f)
        added = 0
        for i, q in enumerate(batch):
            validate(q, f"{os.path.basename(path)}#{i}")
            if q["word"] in existing:
                continue
            questions.append({k: q[k] for k in REQUIRED})
            existing.add(q["word"])
            added += 1
        merged_batch_nos.append(no)
        added_total += added
        print(f"batch {no:02d} ({os.path.basename(path)}): 新增 {added} 题, 跳过 {len(batch)-added} 题(已存在)")

    bank["questions"] = questions
    bank.setdefault("meta", {})
    bank["meta"]["count"] = len(questions)
    if merged_batch_nos:
        bank["meta"]["generated_batches"] = max(
            bank["meta"].get("generated_batches", 0), max(merged_batch_nos)
        )

    with open(BANK, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"---\n合并完成：本次新增 {added_total} 题，题库现共 {len(questions)} 题，"
          f"generated_batches={bank['meta']['generated_batches']}")


if __name__ == "__main__":
    main()
