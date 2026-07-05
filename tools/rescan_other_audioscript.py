# -*- coding: utf-8 -*-
"""对 raw.json 里之前判 kind="other" 的页面二次判定:是否是 audioscript 独白/续页。

主流程 extract_listening_from_pdf.py 里对独白页(section 2 map/图表、section 4 讲座)
判定过严;这里用更宽松 prompt 挽救 audioscript continuation。

用法:
    py tools/rescan_other_audioscript.py c14 --batch 4
    py tools/rescan_other_audioscript.py c14 --pages 60-70    # 手动指定页范围
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qwen_client import QwenClient  # noqa: E402
from extract_listening_from_pdf import (  # noqa: E402
    PDF_NAME, PDF_BASE, render_pages, load_raw, save_raw,
)

SYSTEM_PROMPT = """你是雅思真题内容抽取器。给你若干页图像,请判定每页是否**属于听力原文(audioscript)**:

* 若整页是听力原文文本(不是题干/答案表/图表/目录),即便:
  - 没有 "Audioscripts" 页头
  - 没有说话人名字标注(独白型 section 2 map、section 4 讲座常见)
  - 没有 Q 数字标记
  - 只有大段连续段落文字
  → **仍应判为 kind="audioscript"**,把段落抽出来(speaker 可写 "LECTURER" 或 ""),尽力从段落内容推断 test 号和 section 号。

* 若页面**主要**是:题干、答题表格、答案列表、目录、扉页、写作/口语提示、图片,则 kind="other"。

输出严格 JSON:
{
  "pages": [
    {
      "page_seq": <1-based 序号>,
      "kind": "audioscript" | "other",
      "test": <1-4 或 null>,
      "section": <1-4 或 null>,
      "audioscript_segments": [
        {"speaker": "LECTURER" 或 "" 或 具体名字, "text": "…段落…", "answer_markers": []}
      ],
      "note": ""
    }
  ]
}

- 只输出 JSON,不允许 markdown 代码块或多余文字。
- 判断 test/section 号可参考:上下文提示(如页顶残留"Section 3")、内容主题、页数位置。若判不出填 null。"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book", choices=list(PDF_NAME.keys()))
    ap.add_argument("--pages", help="页面范围,如 60-70;不填=raw 里所有 kind=other 页")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--dpi", type=int, default=180)
    args = ap.parse_args()

    raw = load_raw(args.book)
    if args.pages:
        a, b = args.pages.split("-")
        target = list(range(int(a), int(b) + 1))
    else:
        target = sorted(int(pn) for pn, item in raw["pages"].items()
                        if item.get("kind") == "other")
    if not target:
        print("(无 other 页需要 rescan)")
        return 0

    print(f"[{args.book}] rescan {len(target)} 页 other → audioscript?")
    pages = []
    for pn in target:
        page_data = render_pages(args.book, pn, pn, args.dpi)
        pages.extend(page_data)

    client = QwenClient()
    fails = []
    upgraded = 0
    for i in range(0, len(pages), args.batch):
        chunk = pages[i:i + args.batch]
        page_nums = [pn for pn, _ in chunk]
        imgs = [b for _, b in chunk]
        user = (f"以下 {len(imgs)} 张图分别是剑桥雅思 PDF 的第 "
                f"{','.join(str(p) for p in page_nums)} 页。请按 system 判定并输出 JSON。")
        t0 = time.time()
        print(f"\n[{i//args.batch + 1}] p{page_nums} …", end=" ", flush=True)
        try:
            obj, _ = client.vl_json(images=imgs, system=SYSTEM_PROMPT,
                                    user=user, max_tokens=8192)
            elapsed = time.time() - t0
            pgs = obj.get("pages") or []
            print(f"{elapsed:.1f}s")
            for item in pgs:
                seq = item.get("page_seq")
                if not isinstance(seq, int) or seq < 1 or seq > len(page_nums):
                    continue
                real_pn = page_nums[seq - 1]
                item["page"] = real_pn
                if item.get("kind") == "audioscript" and item.get("audioscript_segments"):
                    raw["pages"][str(real_pn)] = item
                    upgraded += 1
                    n_seg = len(item["audioscript_segments"])
                    print(f"  ↑ p{real_pn}: other → audioscript t{item.get('test')}s{item.get('section')} ({n_seg} seg)")
                # kind="other" 保持不变
            save_raw(args.book, raw)
        except Exception as e:
            print(f"FAIL {type(e).__name__}: {e}")
            fails.append(page_nums)

    print(f"\n完成:{upgraded} 页 other → audioscript,{len(fails)} 批失败")
    print(client.report())
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
