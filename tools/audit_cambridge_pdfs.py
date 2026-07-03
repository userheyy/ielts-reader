"""Audit Cambridge IELTS PDF text extractability for article-bank ingestion."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = Path(r"C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）\剑桥雅思真题1-19")
TARGETS = {
    "c14": BOOK_DIR / "【14】剑桥雅思真题14.pdf",
    "c15": BOOK_DIR / "【15】剑桥雅思真题15.pdf",
    "c16": BOOK_DIR / "【16】剑桥雅思真题16.pdf",
    "c17": BOOK_DIR / "【17】剑桥雅思真题17.pdf",
    "c18": BOOK_DIR / "【18】剑桥雅思真题18.pdf",
    "c19": BOOK_DIR / "剑19（A类）.pdf",
}
OUT = ROOT / "tmp" / "cambridge_pdf_audit.json"


def audit_one(path: Path):
    result = {"path": str(path), "exists": path.exists(), "pages": 0, "avg_text_len_first_40": 0, "reading_hits": [], "answer_key_hits": [], "needs_ocr": True}
    if not path.exists():
        return result
    with pdfplumber.open(path) as pdf:
        result["pages"] = len(pdf.pages)
        lengths = []
        for i, page in enumerate(pdf.pages[: min(40, len(pdf.pages))], 1):
            text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
            lengths.append(len(text))
            flat = " ".join(text.split())
            if re.search(r"R\s*E\s*A\s*D\s*I\s*N\s*G\s+P\s*A\s*S\s*S\s*A\s*G\s*E|READING PASSAGE|Reading Passage", flat, re.I):
                result["reading_hits"].append({"page": i, "sample": flat[:180]})
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
            flat = " ".join(text.split())
            if re.search(r"Listening and Reading answer keys|R\s*E\s*A\s*D\s*I\s*N\s*G", flat, re.I) and "Answer" in flat:
                result["answer_key_hits"].append({"page": i, "sample": flat[:180]})
        result["avg_text_len_first_40"] = round(sum(lengths) / max(1, len(lengths)), 1)
        result["needs_ocr"] = result["avg_text_len_first_40"] < 120 or len(result["reading_hits"]) < 3
    return result


def main():
    OUT.parent.mkdir(exist_ok=True)
    data = {book: audit_one(path) for book, path in TARGETS.items()}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    for book, info in data.items():
        print(book, "pages", info["pages"], "reading_hits", len(info["reading_hits"]), "needs_ocr", info["needs_ocr"])
    print(OUT)


if __name__ == "__main__":
    main()
