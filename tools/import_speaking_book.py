# -*- coding: utf-8 -*-
"""从口语参考书籍(如 Collins IELTS Speaking)抽 IELTS Speaking Task 样题,
合并进 data/speaking/tasks.json,带 book_ref 溯源。

Collins Speaking 是教材形式(不是纯题库),每章混编:
- Exam Technique 板块(考试技巧,跳过)
- Grammar / Vocabulary Lesson(不是题目,跳过)
- **IELTS Speaking Task**(样题 Part 1/2/3,本脚本要抽的)

用法:
    py tools/import_speaking_book.py "path/to/book.pdf" --name collins
    py tools/import_speaking_book.py "path/to/book.pdf" --name collins --pages 10-30
    py tools/import_speaking_book.py --merge --name collins   # 抽完后合并到 tasks.json
"""
import argparse
import json
import sys
import time
from pathlib import Path

import fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qwen_client import QwenClient  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "tools" / "out" / "speaking-books"
TASKS_PATH = ROOT / "data" / "speaking" / "tasks.json"

EXTRACT_SYSTEM = """你是 IELTS 口语题库抽取器。给你若干页图像,每页可能:
- 包含 IELTS Speaking Task 样题(通常有 "IELTS Speaking Task Part 1/2/3" 或 "Speaking Practice" 之类标题)
- 只是词汇/语法 lesson(跳过)
- 只是 exam technique 讲解(跳过)

# 输出严格 JSON(不要 markdown 代码块)
{
  "pages": [
    {
      "page_seq": <1-based 序号>,
      "has_task": true/false,
      "part": 1|2|3|null,
      "topic": "话题名(如 Work, Hometown, A useful skill)",
      "questions": ["Q1", "Q2", ...],       // Part 1/3 用
      "cue": "You should say:\\n- ...\\n- ...",  // Part 2 用,4 行 you should say 提示
      "book_page_hint": "书里的页号 / 章节(若截图角落可见)"
    }
  ]
}

# 规则
- Part 1:短问答,每题 30-45 秒。questions 是 3-5 个短问句
- Part 2:Cue card,cue 字段完整保留 "You should say:" + 4 项子提示
- Part 3:深入讨论,questions 是 3-5 个 abstract/discussion 问题
- 若一页含多个 Part 混合,只输出主要那个;若无 Speaking Task 内容,has_task=false 其他字段留空
- 严格 JSON,不允许 markdown"""


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def render_pages(pdf_path, page_start, page_end, dpi):
    doc = fitz.open(pdf_path)
    n = doc.page_count
    a, b = max(1, page_start), min(n, page_end)
    out = []
    for pn in range(a, b + 1):
        pix = doc[pn - 1].get_pixmap(dpi=dpi)
        out.append((pn, pix.tobytes("png")))
    doc.close()
    return out


def load_raw(name):
    p = OUT_DIR / f"{name}.raw.json"
    if p.exists():
        return load_json(p)
    return {"book": name, "pages": {}}


def save_raw(name, data):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / f"{name}.raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def parse_range(s, default_max=1000):
    if not s:
        return 1, default_max
    if "-" in s:
        a, b = s.split("-", 1)
        return int(a), int(b)
    p = int(s)
    return p, p


def do_extract(args):
    a, b = parse_range(args.pages)
    print(f"[{args.name}] 渲染 p{a}-p{b} @ {args.dpi} dpi …")
    pages = render_pages(args.pdf, a, b, args.dpi)
    print(f"  共 {len(pages)} 页 → 每批 {args.batch} 张")

    raw = load_raw(args.name)
    if args.resume:
        pages = [(pn, b_) for pn, b_ in pages if str(pn) not in raw["pages"]]
        print(f"  --resume: 剩余 {len(pages)} 页未抽")

    if args.dry_run:
        print("(dry-run,不发 API)")
        return 0

    client = QwenClient()
    fails = []
    for i in range(0, len(pages), args.batch):
        chunk = pages[i:i + args.batch]
        page_nums = [pn for pn, _ in chunk]
        imgs = [pn_bytes[1] for pn_bytes in chunk]
        user = f"以下 {len(imgs)} 张图对应书籍的第 {','.join(str(p) for p in page_nums)} 页。按 system 输出严格 JSON。"
        t0 = time.time()
        print(f"\n[{i // args.batch + 1}] p{page_nums} …", end=" ", flush=True)
        try:
            obj, _ = client.vl_json(images=imgs, system=EXTRACT_SYSTEM, user=user, max_tokens=8192)
            elapsed = time.time() - t0
            pgs = obj.get("pages") or []
            hit = sum(1 for p in pgs if p.get("has_task"))
            print(f"{elapsed:.1f}s · {len(pgs)} 页 · Task 命中 {hit}")
            for item in pgs:
                seq = item.get("page_seq")
                if not isinstance(seq, int) or seq < 1 or seq > len(page_nums):
                    continue
                real = page_nums[seq - 1]
                item["page"] = real
                raw["pages"][str(real)] = item
            save_raw(args.name, raw)
        except Exception as e:
            print(f"FAIL {type(e).__name__}: {e}")
            fails.append(page_nums)

    hits = sum(1 for p in raw["pages"].values() if p.get("has_task"))
    print(f"\n完成:{len(raw['pages'])} 页扫描,{hits} 页命中 → {OUT_DIR}/{args.name}.raw.json")
    if fails:
        print(f"[!] 失败批 {fails}")
    print(client.report())


def do_merge(args):
    tasks = load_json(TASKS_PATH)
    rawp = OUT_DIR / f"{args.name}.raw.json"
    if not rawp.exists():
        print(f"未找到 {rawp}")
        return
    raw = load_json(rawp)
    existing_ids = set()
    for k in ("part1", "part2", "part3"):
        for t in tasks.get(k, []):
            existing_ids.add(t.get("id"))
    added = {"part1": 0, "part2": 0, "part3": 0}
    for pn_str, item in sorted(raw["pages"].items(), key=lambda kv: int(kv[0])):
        if not item.get("has_task"):
            continue
        part = item.get("part")
        if part not in (1, 2, 3):
            continue
        topic = (item.get("topic") or "").strip()
        if not topic:
            continue
        # ID:书名 + 页号(保证唯一,同书不同页可能同 topic 但内容异)
        id_ = f"{args.name}-p{item.get('page')}-p{part}"
        if id_ in existing_ids:
            continue
        book_ref = f"《{args.name}》 p{item.get('page')}" + (f" {item['book_page_hint']}" if item.get("book_page_hint") else "")
        entry = {
            "id": id_,
            "topic": topic,
            "book_ref": book_ref,
        }
        if part == 2:
            entry["cue"] = item.get("cue") or ""
        else:
            entry["questions"] = item.get("questions") or []
            if part == 3:
                entry["related_to"] = ""  # 后续可人工关联
        key = f"part{part}"
        tasks.setdefault(key, []).append(entry)
        existing_ids.add(id_)
        added[key] += 1
    with open(TASKS_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    print(f"合并:P1 +{added['part1']} · P2 +{added['part2']} · P3 +{added['part3']}")
    print(f"总量:P1 {len(tasks.get('part1', []))} · P2 {len(tasks.get('part2', []))} · P3 {len(tasks.get('part3', []))}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", nargs="?", help="书籍 PDF 路径(--merge 时可不填)")
    ap.add_argument("--name", required=True, help="书名标识,如 collins / wanglu / speaking-vip")
    ap.add_argument("--pages", help="页面范围,如 10-50")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--dpi", type=int, default=140)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--merge", action="store_true", help="不抽,只把 raw.json 合并进 tasks.json")
    args = ap.parse_args()

    if args.merge:
        return do_merge(args)
    if not args.pdf:
        ap.error("需要 pdf 路径(或用 --merge)")
    do_extract(args)
    print("\n下一步:python tools/import_speaking_book.py --merge --name " + args.name)


if __name__ == "__main__":
    sys.exit(main())
