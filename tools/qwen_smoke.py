# -*- coding: utf-8 -*-
"""DashScope Qwen-VL 冒烟测试:发一次真实图片请求,验证 key / 网络 / VL 模式。

用法: py tools/qwen_smoke.py
"""
import io
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qwen_client import QwenClient  # noqa: E402


def make_test_png():
    """用 pymupdf 造一张最小可读的 PNG(避免依赖 Pillow)。"""
    import fitz
    doc = fitz.open()
    page = doc.new_page(width=300, height=100)
    page.insert_text((20, 60), "Hello Qwen-VL Test", fontsize=24)
    pix = page.get_pixmap(dpi=150)
    return pix.tobytes("png")


def main():
    client = QwenClient()
    print(f"模型: {client.cfg['model']} | 端点: {client.cfg['base_url']}")

    t0 = time.time()
    img = make_test_png()
    obj, usage = client.vl_json(
        images=[img],
        system='你是一个 OCR 助手,只输出严格 JSON。',
        user='读出图片里的英文,返回 {"text": "..."} 。',
        max_tokens=100,
    )
    print(f"[VL] {time.time()-t0:.1f}s: {obj}")

    print(client.report())
    print("Qwen-VL 冒烟测试通过。")


if __name__ == "__main__":
    main()
