# -*- coding: utf-8 -*-
"""从剑桥雅思 14-19 PDF 抽取 Writing Task 1/2 题目。

流程仿照 tools/extract_listening_from_pdf.py:
1) fitz 打开 PDF,遍历页面
2) 对每页给 Qwen-VL(qwen-vl-max)结构化,识别是否是 Writing 页
3) 输出 tools/out/writing/{book}.raw.json,累计所有识别到的 Writing 题
4) 合并入 data/writing/tasks.json(需人工审核 image_description 是否可用)
5) 每题另外用 DeepSeek 打 difficulty tag(入门/进阶/冲刺)

用法:
    py tools/extract_writing_from_pdf.py c14                # 全 c14
    py tools/extract_writing_from_pdf.py c14 --pages 30-60  # pilot 局部
    py tools/extract_writing_from_pdf.py c14 --batch 3      # 每次给 Qwen 几张图(默认 3)
    py tools/extract_writing_from_pdf.py c14 --resume       # 跳过 raw.json 已有的页
    py tools/extract_writing_from_pdf.py --grade-only c14   # 只跑难度分级(读现有 tasks.json)

Difficulty 分级规则(与 writing.html 筛选器对齐):
- Task 1:入门(单一 line/bar chart) / 进阶(table/pie/multi-chart) / 冲刺(process/map)
- Task 2:入门(agree-disagree 单一观点) / 进阶(discuss both views + opinion) /
         冲刺(problems+solutions 或 causes+effects)
"""
import argparse
import json
import sys
import time
from pathlib import Path

import fitz  # pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qwen_client import QwenClient  # noqa: E402
from deepseek_client import DeepSeekClient  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "tools" / "out" / "writing"
TASKS_PATH = ROOT / "data" / "writing" / "tasks.json"

PDF_BASE = Path(
    r"C:\Users\zuolu\Downloads\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）"
    r"\剑桥雅思真题1-19"
)
PDF_NAME = {
    "c14": "【14】剑桥雅思真题14.pdf",
    "c15": "【15】剑桥雅思真题15.pdf",
    "c16": "【16】剑桥雅思真题16.pdf",
    "c17": "【17】剑桥雅思真题17.pdf",
    "c18": "【18】剑桥雅思真题18.pdf",
    "c19": "剑19（A类）.pdf",
}

EXTRACT_SYSTEM = """你是雅思真题内容抽取器,专处理 IELTS Writing 题目页。

给你若干页图像,请判定每页是否是 Writing 题目页,若是则输出结构化 JSON。

# Writing 题目页特征
- Task 1(150 词题):有图表(line/bar/pie/table/process diagram/map/multiple charts)+ 说明段("Summarise the information by selecting and reporting the main features..." + "Write at least 150 words.")
- Task 2(250 词题):纯文字议论文题(agree/disagree / discuss both views / problem+solution / causes+effects)+ "Write at least 250 words."

# 输出严格 JSON(不要 markdown 代码块)
{
  "pages": [
    {
      "page_seq": <1-based 序号>,
      "is_writing": true/false,
      "task": 1|2|null,
      "test": <1-4 或 null,若能从页顶 heading 判>,
      "type": "line graph" | "bar chart" | "pie chart" | "table" | "process" | "map" | "multiple charts"  // Task 1 独有
            | "agree/disagree" | "discuss both views" | "problem/solution" | "causes/effects" | ""  // Task 2 独有
            | "",
      "prompt": "题干完整原文",
      "image_description": "Task 1 用:图表数据要点的文字描述(供无图版参考,类似 250-400 字描述所有数据线索);Task 2 留空"
    }
  ]
}

# 规则
- 每张输入图对应 pages[] 里一个对象,page_seq 顺序不变
- 若非 Writing 题目页(如 Listening / Reading / Answer key),is_writing=false,其他字段留空
- Task 1 的 image_description 要详细列出所有关键数据(时间轴、类别、数值、极值、比较关系),用户看不到图,靠这个描述写作
- 严格 JSON,不要 markdown / 注释 / 多余文本"""

GRADE_SYSTEM = """你是雅思 8 分 IELTS Writing examiner。给你一道 Writing 题目,判断难度并返回严格 JSON。

难度规则:
- Task 1:
  * 入门:单一图表(line graph 或 bar chart),1 组主要数据
  * 进阶:table / pie chart / multiple charts,2-3 组数据比较
  * 冲刺:process diagram / map,无数字,靠语言表达
- Task 2:
  * 入门:agree/disagree(单一观点)
  * 进阶:discuss both views + your opinion(双面讨论)
  * 冲刺:problem/solution 或 causes/effects(多要求 + 多段结构)

输出严格 JSON:
{"difficulty": "入门|进阶|冲刺", "reason": "一句话中文说明为何这个级别"}"""


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def render_pages(book, page_start, page_end, dpi):
    pdf_path = PDF_BASE / PDF_NAME[book]
    if not pdf_path.exists():
        raise SystemExit(f"未找到 PDF: {pdf_path}")
    doc = fitz.open(str(pdf_path))
    n = doc.page_count
    a, b = max(1, page_start), min(n, page_end)
    out = []
    for pn in range(a, b + 1):
        pix = doc[pn - 1].get_pixmap(dpi=dpi)
        out.append((pn, pix.tobytes("png")))
    doc.close()
    return out


def load_raw(book):
    p = OUT_DIR / f"{book}.raw.json"
    if p.exists():
        return load_json(p)
    return {"book": book, "pages": {}}


def save_raw(book, data):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / f"{book}.raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def parse_page_range(s, default_max=200):
    if not s:
        return 1, default_max
    if "-" in s:
        a, b = s.split("-", 1)
        return int(a), int(b)
    p = int(s)
    return p, p


def do_extract(args):
    p_start, p_end = parse_page_range(args.pages)
    print(f"[{args.book}] 渲染 p{p_start}-p{p_end} @ {args.dpi} dpi …")
    pages = render_pages(args.book, p_start, p_end, args.dpi)
    print(f"  共 {len(pages)} 页 → 每批 {args.batch} 张")

    raw = load_raw(args.book)
    if args.resume:
        pages = [(pn, b) for pn, b in pages if str(pn) not in raw["pages"]]
        print(f"  --resume: 剩余 {len(pages)} 页未抽")

    if args.dry_run:
        print("(dry-run)不发 API")
        return 0

    client = QwenClient()
    fails = []
    for i in range(0, len(pages), args.batch):
        chunk = pages[i:i + args.batch]
        page_nums = [pn for pn, _ in chunk]
        imgs = [b for _, b in chunk]
        user = (f"以下 {len(imgs)} 张图对应剑桥雅思 PDF 第 "
                f"{','.join(str(p) for p in page_nums)} 页。按 system 输出严格 JSON。")
        t0 = time.time()
        print(f"\n[{i // args.batch + 1}] p{page_nums} …", end=" ", flush=True)
        try:
            obj, _ = client.vl_json(images=imgs, system=EXTRACT_SYSTEM,
                                    user=user, max_tokens=8192)
            elapsed = time.time() - t0
            pgs = obj.get("pages") or []
            hit = sum(1 for p in pgs if p.get("is_writing"))
            print(f"{elapsed:.1f}s · {len(pgs)} 页 · Writing 命中 {hit}")
            for item in pgs:
                seq = item.get("page_seq")
                if not isinstance(seq, int) or seq < 1 or seq > len(page_nums):
                    continue
                real = page_nums[seq - 1]
                item["page"] = real
                raw["pages"][str(real)] = item
            save_raw(args.book, raw)
        except Exception as e:
            print(f"FAIL {type(e).__name__}: {e}")
            fails.append(page_nums)

    hits = sum(1 for p in raw["pages"].values() if p.get("is_writing"))
    print(f"\n完成:{len(raw['pages'])} 页扫描,{hits} 页命中 Writing → {OUT_DIR}/{args.book}.raw.json")
    if fails:
        print(f"[!] 失败批 {fails}")
    print(client.report())
    return 0 if not fails else 1


def do_merge(args):
    """把 tools/out/writing/{book}.raw.json 里 is_writing=true 的题合并进 data/writing/tasks.json。"""
    tasks = load_json(TASKS_PATH)
    existing_ids = set(
        [t.get("id") for t in tasks.get("task1", [])] +
        [t.get("id") for t in tasks.get("task2", [])])
    added_t1 = added_t2 = 0
    for book in ([args.book] if args.book else PDF_NAME.keys()):
        rawp = OUT_DIR / f"{book}.raw.json"
        if not rawp.exists():
            print(f"  {book}: 无 raw.json,跳过")
            continue
        raw = load_json(rawp)
        # 按 test 号分组,每 test 应该恰好 1 个 Task 1 + 1 个 Task 2
        test_bucket = {}
        for pn, item in sorted(raw["pages"].items(), key=lambda kv: int(kv[0])):
            if not item.get("is_writing"):
                continue
            t = item.get("test")
            task = item.get("task")
            if t is None or task not in (1, 2):
                continue
            test_bucket.setdefault((t, task), []).append(item)
        for (t, task), items in test_bucket.items():
            # 若一 test 同一 task 抽到多页(题干横跨 2 页),挑最长 prompt
            best = max(items, key=lambda x: len(x.get("prompt", "") or ""))
            id_ = f"{book}-test{t}-t{task}"
            if id_ in existing_ids:
                continue
            entry = {
                "id": id_,
                "source": f"剑桥雅思{book[1:]} · Test {t}",
                "book_ref": f"剑桥雅思{book[1:]}真题 Test {t} Writing Task {task}",
                "type" if task == 1 else "topic": best.get("type", ""),
                "prompt": best.get("prompt", ""),
                "difficulty": "",  # 由 do_grade 填
            }
            if task == 1 and best.get("image_description"):
                entry["image_hint"] = best["image_description"]
            key = f"task{task}"
            tasks.setdefault(key, []).append(entry)
            existing_ids.add(id_)
            if task == 1: added_t1 += 1
            else: added_t2 += 1
    with open(TASKS_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    print(f"合并:Task 1 新增 {added_t1} 道,Task 2 新增 {added_t2} 道 → {TASKS_PATH}")


def do_grade(args):
    """用 DeepSeek 给所有 difficulty 未填的题打级(便宜,~0.005 元/题)。"""
    tasks = load_json(TASKS_PATH)
    client = DeepSeekClient()
    graded = 0
    for key in ("task1", "task2"):
        for entry in tasks.get(key, []):
            if entry.get("difficulty"):
                continue
            task_num = 1 if key == "task1" else 2
            user = (f"【题型】Task {task_num}" +
                    (f" · {entry.get('type', '')}" if task_num == 1 else f" · {entry.get('topic', '')}") +
                    f"\n【题干】{entry['prompt']}")
            try:
                obj, _ = client.chat_json(
                    [{"role": "system", "content": GRADE_SYSTEM},
                     {"role": "user", "content": user}], max_tokens=200)
                d = obj.get("difficulty")
                if d in ("入门", "进阶", "冲刺"):
                    entry["difficulty"] = d
                    entry["_diff_reason"] = obj.get("reason", "")
                    graded += 1
                    print(f"  {entry['id']}: {d}")
            except Exception as e:
                print(f"  {entry['id']}: FAIL {e}")
    with open(TASKS_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    print(f"打级完成:{graded} 题 → {TASKS_PATH}")
    print(client.report())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book", nargs="?", choices=list(PDF_NAME.keys()), default=None)
    ap.add_argument("--pages", help="页面范围,如 30-60(1-based);空=全 PDF")
    ap.add_argument("--batch", type=int, default=3)
    ap.add_argument("--dpi", type=int, default=180)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--merge", action="store_true", help="不抽,只把 raw.json 合并到 tasks.json")
    ap.add_argument("--grade-only", action="store_true", help="不抽,只对 tasks.json 里未打级的题跑 DeepSeek 难度分级")
    args = ap.parse_args()
    if args.grade_only:
        return do_grade(args)
    if args.merge:
        return do_merge(args)
    if not args.book:
        ap.error("需要指定 book(或用 --merge / --grade-only)")
    do_extract(args)
    print("\n下一步:python tools/extract_writing_from_pdf.py --merge --grade-only")


if __name__ == "__main__":
    sys.exit(main())
