# -*- coding: utf-8 -*-
"""DeepSeek API 冒烟测试:发一条最小请求,验证 key/网络/JSON 模式。

用法: py tools/deepseek_smoke.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deepseek_client import DeepSeekClient  # noqa: E402


def main():
    client = DeepSeekClient()
    print(f"模型: {client.cfg['model']} | 端点: {client.cfg['base_url']}")

    t0 = time.time()
    text, usage = client.chat(
        [{"role": "user", "content": "回复两个字:在线"}], max_tokens=10)
    print(f"[1/2] 普通模式 ({time.time()-t0:.1f}s): {text!r}")

    t0 = time.time()
    obj, usage = client.chat_json(
        [{"role": "user",
          "content": '输出 JSON:{"status": "ok", "msg": "<10个字以内的中文问候>"}'}],
        max_tokens=50)
    print(f"[2/2] JSON 模式 ({time.time()-t0:.1f}s): {obj}")

    print(client.report())
    print("冒烟测试通过 ✔")


if __name__ == "__main__":
    main()
