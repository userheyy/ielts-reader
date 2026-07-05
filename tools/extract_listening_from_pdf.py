# -*- coding: utf-8 -*-
"""用 Qwen-VL 从剑桥雅思真题 PDF 抽取:听力原文 + 题目 + 答案 key。

输出:tools/out/listening/{book}.raw.json,累积每页识别结果,后续由
gen_listening_transcript.py 汇总成 data/listening/{id}.json。

用法:
    py tools/extract_listening_from_pdf.py c14                # 全 c14
    py tools/extract_listening_from_pdf.py c14 --pages 100-105 # pilot
    py tools/extract_listening_from_pdf.py c14 --batch 3      # 每次几张图给 Qwen(默认 3)
    py tools/extract_listening_from_pdf.py c14 --resume       # 跳过 raw.json 已有的页
    py tools/extract_listening_from_pdf.py c14 --dry-run      # 只渲染 + 打印 prompt,不发 API
"""
import argparse
import io
import json
import os
import sys
import time
from pathlib import Path

import fitz  # pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qwen_client import QwenClient  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "tools" / "out" / "listening"

PDF_BASE = Path(
    r"C:\Users\zuolu\Downloads\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）"
    r"\剑桥雅思真题1-19"
)

# 每册 PDF 文件名(观察 Downloads 目录整理)
PDF_NAME = {
    "c14": "【14】剑桥雅思真题14.pdf",
    "c15": "【15】剑桥雅思真题15.pdf",
    "c16": "【16】剑桥雅思真题16.pdf",
    "c17": "【17】剑桥雅思真题17.pdf",
    "c18": "【18】剑桥雅思真题18.pdf",
    "c19": "剑19（A类）.pdf",
}

SYSTEM_PROMPT = """你是雅思真题内容抽取器。给你若干页图像,请识别每页属于什么类型并按严格 JSON 输出。

# 页面类型 kind
- "audioscript":内容是听力原文。特征之一:页顶或右上角有 "Audioscripts" / "AUDIOSCRIPTS" 字样;
  或页面充满带说话人名字的对白(CARLA:/ROB:/OFFICER: 等);
  或**独白型**(section 4 常见):没有对白 speaker 标签,只有大段连续段落文字,前面可能有 "SECTION 4" 大字标题;
  或 **audioscript 续页**:接续上一页的听力原文,没有 Audioscripts 页头也没有 speaker 标签,但通篇是自然段+右侧偶有 Q 数字标记。
  只要页面主体明显是听力原文文本(而非题目/答案表),都归为 audioscript。
- "question":题干页。顶部标题如 "LISTENING" / "SECTION 1" / "PART 1" / "READING PASSAGE" / "Test X"。含 Questions 1-40 的题目文本、图表、表格、选项等。
- "answer_key":顶部有 "Answer key" / "Answer Keys" 字样,内容是编号 + 答案列表。
- "other":目录、写作、口语、图片扉页等。

# 输出 JSON(严格,不要 markdown 代码块)
{
  "pages": [
    {
      "page_seq": <本次输入图片的序号,从 1 开始>,
      "kind": "audioscript|question|answer_key|other",
      "test": <1-4 或 null>,
      "section": <1-4 或 null,仅 audioscript 用;若无法判断填 null>,
      "audioscript_segments": [
        {"speaker": "CARLA", "text": "…完整段落…", "answer_markers": [24, 25]}
      ],
      "question_items": [
        {"number": 23, "topic": "listening", "prompt": "…题干…", "hint": "form/table/multi/etc"}
      ],
      "answer_entries": [
        {"number": 1, "topic": "listening", "answer": "Canadian"}
      ],
      "note": ""
    }
  ]
}

# 规则(重要,严格遵守)
- 每张输入图对应 pages[] 里一个对象,page_seq 顺序不变。
- **重要 topic 字段**(区分听力题 vs 阅读题,同 test 内二者共享 1-40 编号):
  * question_items 里每题必须标 topic="listening" 或 "reading":
    - 题干中含 "text" / "passage" / "TRUE/FALSE/NOT GIVEN" / "the writer" / "the author" / 段落字母(A, B, C, D 匹配段落)→ reading
    - 页面 heading 含 "LISTENING" / "SECTION 1-4" / "Part 1-4" (含表格/表单/图形完成)/ 题干含"you hear"→ listening
    - 若判断不了,用页面标题最强证据判断
  * answer_key 页里题号会重复(1-40 出现两次:一次听力、一次阅读)。answer_entries[].topic 必须标出。
    通常答案页布局:先 "Test X Listening" + 1-40 答案,再 "Test X Reading" + 1-40 答案。以最近的 heading 为准。
- audioscript_segments.speaker:
  * 对白页写实际说话人(如 CARLA, ROB, TUTOR, OFFICER)。
  * **独白页**(Section 4 常见)统一写 "LECTURER";若能看出是男/女则用 "MAN"/"WOMAN"。
  * **绝不允许**把 "SECTION 4" / "SECTION 3" 之类的分节标题当作 speaker;它们是章节头,不是说话人。
  * 续页无 speaker 标签时,若段落属于连续独白,speaker 仍写 "LECTURER" 或写 ""(空串,由下游合并到上一段)。
- audioscript_segments.text:原文完整段落(可换行合并成一行,不加省略号)。
- answer_markers:只在段落末尾/右侧有 Q 数字时填,值为整数数组;没有留空数组。
- 若一页整页都是听力原文续文(没有 Audioscripts 页头也没有 Q 标记),仍归 kind="audioscript",section 可填 null(下游按上下文推断)。
- 若识别不出 kind,填 "other";其他字段可留空数组或 null。
- 严格 JSON,不允许 markdown、注释、多余文本。"""


def render_pages(book, page_start, page_end, dpi):
    """渲染 [page_start, page_end] 范围的页面,返回 [(page_num, png_bytes)]。
    page_num 是 1-based。"""
    pdf_path = PDF_BASE / PDF_NAME[book]
    if not pdf_path.exists():
        raise SystemExit(f"未找到 PDF: {pdf_path}")
    doc = fitz.open(str(pdf_path))
    n = doc.page_count
    a = max(1, page_start)
    b = min(n, page_end)
    results = []
    for pn in range(a, b + 1):
        page = doc[pn - 1]  # 0-based index
        pix = page.get_pixmap(dpi=dpi)
        results.append((pn, pix.tobytes("png")))
    doc.close()
    return results


def parse_page_range(s, default_max=200):
    if not s:
        return 1, default_max
    if "-" in s:
        a, b = s.split("-", 1)
        return int(a), int(b)
    p = int(s)
    return p, p


def load_raw(book):
    p = OUT_DIR / f"{book}.raw.json"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {"book": book, "pages": {}}


def save_raw(book, data):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUT_DIR / f"{book}.raw.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book", choices=list(PDF_NAME.keys()))
    ap.add_argument("--pages", help="页面范围,如 100-110(1-based,含端点)。空=全 PDF")
    ap.add_argument("--batch", type=int, default=3, help="每次给 Qwen 的图片数")
    ap.add_argument("--dpi", type=int, default=180)
    ap.add_argument("--resume", action="store_true", help="跳过已在 raw.json 中的页")
    ap.add_argument("--dry-run", action="store_true", help="只渲染 + 打印,不发 API")
    args = ap.parse_args()

    p_start, p_end = parse_page_range(args.pages)

    print(f"[{args.book}] 渲染 p{p_start}-p{p_end} @ {args.dpi} dpi …")
    pages = render_pages(args.book, p_start, p_end, args.dpi)
    print(f"  共 {len(pages)} 页 → 每批 {args.batch} 张")

    raw = load_raw(args.book)
    if args.resume:
        pages = [(pn, b) for pn, b in pages if str(pn) not in raw["pages"]]
        print(f"  --resume: 剩余 {len(pages)} 页未抽")

    if args.dry_run:
        print("(dry-run)不发 API。示例 system prompt 前 200:")
        print(SYSTEM_PROMPT[:200])
        return 0

    client = QwenClient()
    fails = []
    for i in range(0, len(pages), args.batch):
        chunk = pages[i:i + args.batch]
        page_nums = [pn for pn, _ in chunk]
        imgs = [b for _, b in chunk]
        user = (f"以下 {len(imgs)} 张图分别对应剑桥雅思 PDF 的第 "
                f"{','.join(str(p) for p in page_nums)} 页。请按 system 指定输出严格 JSON。")
        t0 = time.time()
        print(f"\n[{i//args.batch + 1}] p{page_nums} …", end=" ", flush=True)
        try:
            obj, usage = client.vl_json(images=imgs, system=SYSTEM_PROMPT,
                                        user=user, max_tokens=8192)
            elapsed = time.time() - t0
            pgs = obj.get("pages") or []
            print(f"{elapsed:.1f}s · {len(pgs)} 页解析")
            # 用 page_seq 对应到真实 page 号
            for item in pgs:
                seq = item.get("page_seq")
                if not isinstance(seq, int) or seq < 1 or seq > len(page_nums):
                    print(f"  [!] page_seq {seq!r} 越界,跳过")
                    continue
                real_pn = page_nums[seq - 1]
                item["page"] = real_pn
                raw["pages"][str(real_pn)] = item
            save_raw(args.book, raw)  # 每 batch 存一次
        except SystemExit as e:
            print(f"FAIL {e}")
            fails.append(page_nums)
        except Exception as e:
            print(f"FAIL {type(e).__name__}: {e}")
            fails.append(page_nums)

    print(f"\n完成:抽 {len(raw['pages'])} 页 → {OUT_DIR}/{args.book}.raw.json")
    if fails:
        print(f"[!] 失败批 {fails}")
    print(client.report())
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
