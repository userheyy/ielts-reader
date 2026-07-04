# -*- coding: utf-8 -*-
"""从《语法俱乐部》(旋元佑) epub 提取结构化知识库 → data/local/grammar-book.json

用法:
  py tools/extract_grammar_book.py --epub "E:\\下载\\语法俱乐部-旋元佑.epub" --outline   # 只打印章节树核对
  py tools/extract_grammar_book.py --epub "E:\\下载\\语法俱乐部-旋元佑.epub"             # 正式提取

纯 stdlib(zipfile + html.parser)。版权内容仅限本地个人学习,产物已被 .gitignore 忽略。

epub 实际结构(text00000-3.html, UTF-8 XHTML, legacy font 标签),经 --outline 核对后的解析规则:
- 篇(part):    独占段 + 全彩色 + <font size=6> + 文字以"第X篇"开头(共 3 篇)
- 章(chapter): 独占段 + 全彩色 + (size=5 或 6) + 文字以"第X章"开头(共 23 章;
               注意第 14 章没有下划线、第 16 章拆成"之一/之二/之三"三段标题——
               遇到与当前章同号的标题时并入当前章,标题转为一个 section)
- 节(section): 独占段、全彩色、无下划线、不超过 40 字:
               * size=4/5(前三章用 5,后面用 4)→ 节标题
               * 无 size 但颜色为 blue → 节标题(第 4 章起的主要小节样式)
               * 其余颜色(teal/#F60/green/purple/...)或带编号("1."开头/冒号结尾)
                 → 小标题块 {t:"h"},保留在正文流里,不进目录
- 普通 <p> → 正文段 {t:"p"};段内 font color=red/blue 的词 → 该节 concepts
- 英文字母占比 >60% 且字母数≥8 的段 → 例句 {t:"ex"};中文译文多数与英文同段
  (从第一个汉字处切分),少数在紧邻下一段(短中文段兜底吸收)
- 纯 "S V O C"/"先行词 关系从句" 之类的对位标注行(含连续 \\xa0 空白列)→ 丢弃
"""
import argparse
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

CJK = r"一-鿿"
RE_CJK = re.compile(f"[{CJK}]")
RE_LETTER = re.compile(r"[A-Za-z]")
# 中日韩文字与全角标点(用于去掉它们之间被换行引入的空格)
CJK_PUNCT = CJK + r"　-〿＀-￯「」『』"
RE_CJK_GAP = re.compile(f"(?<=[{CJK_PUNCT}])\\s+(?=[{CJK_PUNCT}])")
RE_ALIGN = re.compile(r"^[\sSVOC()（）＋+]+$")     # 例句下方的 S/V/O/C 对位行
RE_COLRUN = re.compile(r"[^\S\n]{3,}")             # 连续 3+ 空白 = 对位排版列
RE_PART = re.compile(r"^第([一二三四五六七八九十百零\d]+)篇")
RE_CHAP = re.compile(r"^第([一二三四五六七八九十百零\d]+)章")
RE_NUM_ENUM = re.compile(r"^\d+\s*[、．.]")         # "1." / "2、" 开头
RE_ANY_ENUM = re.compile(r"^([一二三四五六七八九十]+|\d+|[A-Z]|[IVX]+)\s*[、．.]")

CN_DIGIT = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
            "六": 6, "七": 7, "八": 8, "九": 9}


def cn2int(s):
    """中文数字(到 99 够用)或阿拉伯数字 → int"""
    s = s.strip()
    if s.isdigit():
        return int(s)
    if "十" in s:
        left, _, right = s.partition("十")
        tens = CN_DIGIT.get(left, 1) if left else 1
        ones = CN_DIGIT.get(right, 0) if right else 0
        return tens * 10 + ones
    val = 0
    for ch in s:
        val = val * 10 + CN_DIGIT.get(ch, 0)
    return val


def norm(s):
    """空白归一:压缩连续空白;去掉汉字/全角标点之间的空格;修掉英文标点前的空格。"""
    s = s.replace(" ", " ")
    s = re.sub(r"\s+", " ", s)
    s = RE_CJK_GAP.sub("", s)
    s = re.sub(r"\s+([.,;:!?’”)\]])", r"\1", s)
    return s.strip()


def pretty_title(t):
    """章/篇标题里"第X章"后补个空格,显示更清楚。"""
    return re.sub(r"^(第[一二三四五六七八九十百零\d]+[篇章])\s*", r"\1 ", t)


class Piece:
    __slots__ = ("size", "color", "under", "text")

    def __init__(self, size, color, under, text):
        self.size, self.color, self.under, self.text = size, color, under, text


class BookParser(HTMLParser):
    """把每个 <p> 收集为带样式信息(font size/color、是否下划线)的文字片段列表。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.font_stack = []
        self.u_depth = 0
        self.in_p = False
        self.pieces = None
        self.paras = []  # [[Piece,...], ...]

    def _cur(self):
        return self.font_stack[-1] if self.font_stack else (None, None)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "font":
            psize, pcolor = self._cur()
            self.font_stack.append((a.get("size", psize), a.get("color", pcolor)))
        elif tag == "u":
            self.u_depth += 1
        elif tag == "p":
            self.in_p = True
            self.pieces = []

    def handle_endtag(self, tag):
        if tag == "font":
            if self.font_stack:
                self.font_stack.pop()
        elif tag == "u":
            self.u_depth = max(0, self.u_depth - 1)
        elif tag == "p":
            if self.pieces is not None:
                self.paras.append(self.pieces)
            self.in_p = False
            self.pieces = None

    def handle_data(self, data):
        if self.in_p and data:
            size, color = self._cur()
            self.pieces.append(Piece(size, color, self.u_depth > 0, data))


def raw_text(pieces):
    return "".join(p.text for p in pieces)


def classify(pieces):
    """返回 (kind, payload):
    kind ∈ part / chapter / section / heading / body / skip
    """
    raw = raw_text(pieces)
    text = norm(raw)
    if not text:
        return "skip", None
    solid = [p for p in pieces if norm(p.text)]
    all_colored = solid and all(p.color for p in solid)
    no_under = not any(p.under for p in solid)
    sizes = {p.size for p in solid}

    # 篇/章:独占彩色段 + "第X篇/第X章"开头(第14章无下划线,故不要求 <u>)
    if all_colored and len(text) <= 30:
        m = RE_PART.match(text)
        if m and "6" in sizes:
            return "part", (cn2int(m.group(1)), pretty_title(text))
        m = RE_CHAP.match(text)
        if m and sizes & {"5", "6"}:
            return "chapter", (cn2int(m.group(1)), pretty_title(text))

    # 节标题 / 小标题:独占彩色段
    if all_colored and len(text) <= 60:
        colors = {(p.color or "").lower() for p in solid}
        if len(text) <= 40 and not text.endswith(("：", ":")):
            # 罗马数字编号(I. II. III.)是第 4/5 章的主小节样式(带下划线也算)
            if re.match(r"^[IVX]{1,4}[．.]\s*", text):
                return "section", text
            if no_under:
                if sizes & {"4", "5"} and not RE_NUM_ENUM.match(text) \
                        and not (RE_ANY_ENUM.match(text) and len(text) > 15):
                    return "section", text
                if colors == {"blue"} and not sizes & {"4", "5", "6"} \
                        and not RE_ANY_ENUM.match(text):
                    return "section", text
        return "heading", text

    # 对位标注行:纯 S/V/O/C,或含 3+ 连续空白排版列的短行(如"先行词  关系从句")
    if RE_ALIGN.match(text):
        return "skip", None
    stripped = raw.replace(" ", " ").strip()
    if len(text) <= 30 and RE_COLRUN.search(stripped):
        return "skip", None
    return "body", (raw, text)


def is_example(text):
    letters = len(RE_LETTER.findall(text))
    cjk = len(RE_CJK.findall(text))
    return letters >= 8 and letters / (letters + cjk) > 0.6


def split_example(raw):
    """英文例句段:从第一个汉字处切开 → (en, zh);再把 zh 里的对位标注尾巴剪掉。"""
    m = RE_CJK.search(raw)
    if not m:
        return norm(raw), ""
    en = norm(raw[: m.start()])
    zh_raw = raw[m.start():].replace(" ", " ")
    # 译文后若还有 3+ 连续空白,后面是"先行词 关系从句"之类的排版标注 → 剪掉
    cut = RE_COLRUN.search(zh_raw)
    if cut:
        zh_raw = zh_raw[: cut.start()]
    return en, norm(zh_raw)


def collect_concepts(pieces):
    """正文段里 red/blue 彩字 → concepts(按顿号/逗号拆开)。"""
    out = []
    for p in pieces:
        if (p.color or "").lower() in ("red", "blue") and norm(p.text):
            for w in re.split(r"[、，,;；。]", norm(p.text)):
                w = w.strip()
                if 1 < len(w) <= 20 and w not in out:
                    out.append(w)
    return out


def build(epub_path):
    zf = zipfile.ZipFile(epub_path)
    names = [n for n in zf.namelist() if re.search(r"text\d+\.html?$", n)]
    names.sort()

    parts = []
    cur_part = cur_chap = cur_sec = None
    pending_ex = None  # 上一个无中文译文的例句,等紧邻短中文段兜底

    def ensure_section(title=None):
        nonlocal cur_sec
        if cur_chap is None:
            return None  # 章之外的杂段(封面/版权页等)丢弃
        if cur_sec is None or title is not None:
            idx = len(cur_chap["sections"]) + 1
            cur_sec = {
                "anchor": f'{cur_chap["anchor"]}.s{idx}',
                "title": title if title is not None else "引言",
                "concepts": [],
                "blocks": [],
            }
            cur_chap["sections"].append(cur_sec)
        return cur_sec

    for name in names:
        parser = BookParser()
        parser.feed(zf.read(name).decode("utf-8"))
        for pieces in parser.paras:
            kind, payload = classify(pieces)
            if kind == "skip":
                continue
            if kind == "part":
                num, title = payload
                cur_part = {"part": num, "title": title, "chapters": []}
                parts.append(cur_part)
                cur_chap = cur_sec = None
                pending_ex = None
            elif kind == "chapter":
                num, title = payload
                if cur_chap is not None and cur_chap["ch"] == num:
                    # 同号章标题(第十六章 关系从句之一/之二/之三)→ 并入当前章,转为节
                    sub = re.sub(r"^第[一二三四五六七八九十百零\d]+章\s*", "", title)
                    ensure_section(sub or title)
                    pending_ex = None
                    continue
                cur_chap = {"ch": num, "title": title,
                            "anchor": f"ch{num}", "sections": []}
                if cur_part is None:
                    cur_part = {"part": 0, "title": "(未分篇)", "chapters": []}
                    parts.append(cur_part)
                cur_part["chapters"].append(cur_chap)
                cur_sec = None
                pending_ex = None
            elif kind == "section":
                ensure_section(payload)
                pending_ex = None
            elif kind == "heading":
                sec = ensure_section()
                if sec is not None:
                    sec["blocks"].append({"t": "h", "zh": payload})
                pending_ex = None
            else:  # body
                raw, text = payload
                sec = ensure_section()
                if sec is None:
                    continue
                if is_example(text):
                    en, zh = split_example(raw)
                    blk = {"t": "ex", "en": en, "zh": zh}
                    sec["blocks"].append(blk)
                    pending_ex = blk if not zh else None
                else:
                    # 兜底:上一段是无译文例句,本段是紧邻的短中文段 → 当译文
                    if (pending_ex is not None and len(text) <= 50
                            and not RE_LETTER.search(text[:2])):
                        pending_ex["zh"] = text
                        pending_ex = None
                        continue
                    pending_ex = None
                    sec["blocks"].append({"t": "p", "zh": text})
                    for c in collect_concepts(pieces):
                        if c not in sec["concepts"]:
                            sec["concepts"].append(c)
    # 清理:空"引言"节直接删;其它空节把标题降级为上一节末尾的小标题块(保持阅读顺序)
    for part in parts:
        for ch in part["chapters"]:
            kept = []
            for s in ch["sections"]:
                if not s["blocks"] and not s["concepts"]:
                    if s["title"] != "引言" and kept:
                        kept[-1]["blocks"].append({"t": "h", "zh": s["title"]})
                    continue
                kept.append(s)
            ch["sections"] = kept
            for i, s in enumerate(ch["sections"], 1):
                s["anchor"] = f'{ch["anchor"]}.s{i}'
    return parts


def outline(parts):
    n_ch = n_sec = n_ex = n_p = 0
    for part in parts:
        print(f'第{part["part"]}篇  {part["title"]}')
        for ch in part["chapters"]:
            n_ch += 1
            secs = ch["sections"]
            n_sec += len(secs)
            print(f'  [{ch["anchor"]}] {ch["title"]}  ({len(secs)} 节)')
            for s in secs:
                ps = sum(1 for b in s["blocks"] if b["t"] == "p")
                ex = sum(1 for b in s["blocks"] if b["t"] == "ex")
                n_p += ps
                n_ex += ex
                print(f'    [{s["anchor"]}] {s["title"]}  (正文{ps} 例句{ex} 概念{len(s["concepts"])})')
    print(f"\n合计: {len(parts)} 篇 {n_ch} 章 {n_sec} 节 | 正文段 {n_p} | 例句 {n_ex}")


def main():
    ap = argparse.ArgumentParser(description="提取《语法俱乐部》epub → grammar-book.json")
    ap.add_argument("--epub", required=True, help="epub 文件路径")
    ap.add_argument("--outline", action="store_true", help="只打印章节树供核对,不写文件")
    ap.add_argument("--out", default=None, help="输出路径(默认 data/local/grammar-book.json)")
    args = ap.parse_args()

    epub = Path(args.epub)
    if not epub.exists():
        print(f"找不到 epub: {epub}", file=sys.stderr)
        sys.exit(1)

    parts = build(epub)

    if args.outline:
        outline(parts)
        return

    root = Path(__file__).resolve().parent.parent
    out_path = Path(args.out) if args.out else root / "data" / "local" / "grammar-book.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "meta": {
            "title": "语法俱乐部",
            "author": "旋元佑",
            "extracted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "notice": "版权内容,仅限本地个人学习,禁止提交或分发",
        },
        "parts": parts,
    }
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    n_sec = sum(len(c["sections"]) for p in parts for c in p["chapters"])
    n_ex = sum(1 for p in parts for c in p["chapters"] for s in c["sections"]
               for b in s["blocks"] if b["t"] == "ex")
    print(f"已写入 {out_path}  ({len(parts)} 篇 / "
          f"{sum(len(p['chapters']) for p in parts)} 章 / {n_sec} 节 / 例句 {n_ex})")


if __name__ == "__main__":
    main()
