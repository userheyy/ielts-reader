"""把 PDF 指定页高清渲染为 PNG,可选按 x 比例裁成竖条(便于读清多栏)。
用法:
  python tools/render_page.py "<pdf>" <page0based> <out_dir> [scale] [ncols]
- scale 默认 4.0
- ncols 默认 1(不切栏);>1 时把页面按等宽切成 ncols 张竖条图(仅用于"看清",抄录顺序由人判断)
输出: out_dir/page{page}_full.png,以及若 ncols>1 则 page{page}_col{k}.png
"""
import sys, os
import pypdfium2 as pdfium

def main():
    pdf_path = sys.argv[1]
    page_no = int(sys.argv[2])
    out_dir = sys.argv[3]
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
    ncols = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    os.makedirs(out_dir, exist_ok=True)
    pdf = pdfium.PdfDocument(pdf_path)
    page = pdf[page_no]
    img = page.render(scale=scale).to_pil()
    W, H = img.size
    full = os.path.join(out_dir, f"page{page_no}_full.png")
    img.save(full)
    print("saved", full, img.size)
    if ncols > 1:
        colw = W / ncols
        for k in range(ncols):
            crop = img.crop((int(k * colw), 0, int((k + 1) * colw), H))
            p = os.path.join(out_dir, f"page{page_no}_col{k+1}.png")
            crop.save(p)
            print("saved", p, crop.size)

if __name__ == "__main__":
    main()
