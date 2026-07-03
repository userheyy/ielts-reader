"""在 PDF 中按关键词(通常文章标题)定位页码(0基)。
用法: python tools/find_page.py "<pdf路径>" "AIRPORTS ON WATER"
输出匹配到的页码及该页字符数。
"""
import sys
import pdfplumber

def main():
    pdf_path, keyword = sys.argv[1], sys.argv[2]
    with pdfplumber.open(pdf_path) as pdf:
        hits = []
        for i, pg in enumerate(pdf.pages):
            t = pg.extract_text() or ""
            if keyword.lower() in t.lower():
                hits.append((i, len(t), round(pg.width), round(pg.height)))
        if not hits:
            print(f"未找到 '{keyword}'"); sys.exit(1)
        for i, n, w, h in hits:
            print(f"页码(0基)={i}  字符数={n}  页宽高={w}x{h}")

if __name__ == "__main__":
    main()
