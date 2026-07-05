# -*- coding: utf-8 -*-
"""DashScope (Qwen-VL) API 共用客户端 — 走 OpenAI 兼容接口。

用法:
    from qwen_client import QwenClient
    c = QwenClient()
    obj, usage = c.vl_json(
        images=[png_bytes_1, png_bytes_2],
        system="…",
        user="…",
        max_tokens=8192)

配置读取 tools/config.local.json:
    { "dashscope_key": "sk-…",
      "dashscope_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "dashscope_model": "qwen-vl-max-latest" }
"""
import base64
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
CONFIG_PATH = TOOLS_DIR / "config.local.json"

# qwen-vl-max 定价(2026-07 参考,元 / 千 token)
PRICE_IN = 0.02
PRICE_OUT = 0.06


def load_config():
    if not CONFIG_PATH.exists():
        raise SystemExit("缺少 tools/config.local.json")
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    key = cfg.get("dashscope_key") or cfg.get("dashscope_api_key")
    if not key:
        raise SystemExit("config.local.json 缺 dashscope_key")
    return {
        "api_key": key,
        "base_url": cfg.get("dashscope_base_url",
                            "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        "model": cfg.get("dashscope_model", "qwen-vl-max-latest"),
    }


def _image_item(png_bytes):
    """构造 chat/completions 兼容格式的图片消息片段。"""
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return {
        "type": "image_url",
        "image_url": {"url": f"data:image/png;base64,{b64}"},
    }


class QwenClient:
    def __init__(self, temperature=0.1, max_retries=5):
        self.cfg = load_config()
        self.temperature = temperature
        self.max_retries = max_retries
        self.total_prompt = 0
        self.total_completion = 0
        self.requests = 0

    def chat(self, messages, max_tokens=4096, json_mode=False, temperature=None):
        body = {
            "model": self.cfg["model"],
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
            "max_tokens": max_tokens,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        url = self.cfg["base_url"].rstrip("/") + "/chat/completions"

        delay = 2
        for attempt in range(self.max_retries):
            req = urllib.request.Request(
                url,
                data=payload,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + self.cfg["api_key"],
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                usage = data.get("usage", {}) or {}
                self._track(usage)
                content = data["choices"][0]["message"]["content"]
                return content, usage
            except urllib.error.HTTPError as e:
                detail = ""
                try:
                    detail = e.read().decode("utf-8", "replace")[:400]
                except Exception:
                    pass
                if e.code in (429, 500, 502, 503, 504) and attempt < self.max_retries - 1:
                    print(f"  [retry] HTTP {e.code},{delay}s 后重试… {detail[:120]}")
                    time.sleep(delay)
                    delay = min(delay * 2, 64)
                    continue
                raise SystemExit(f"Qwen HTTP {e.code}: {detail}")
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                if attempt < self.max_retries - 1:
                    print(f"  [retry] 网络错误 {e},{delay}s 后重试…")
                    time.sleep(delay)
                    delay = min(delay * 2, 64)
                    continue
                raise SystemExit(f"Qwen 网络错误(已重试 {self.max_retries} 次): {e}")
        raise SystemExit("Qwen 请求失败")

    def vl_json(self, images, system, user, max_tokens=8192, temperature=None):
        """图片(PNG bytes list)+ 文本 → JSON。校验解析失败自动带错误重试一次。"""
        content = [_image_item(img) for img in images]
        content.append({"type": "text", "text": user})
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": content},
        ]
        raw, usage = self.chat(messages, max_tokens=max_tokens, json_mode=True,
                               temperature=temperature)
        try:
            return json.loads(raw), usage
        except json.JSONDecodeError as e:
            retry = messages + [
                {"role": "assistant", "content": raw},
                {"role": "user", "content": [
                    {"type": "text",
                     "text": f"你的输出不是合法 JSON(解析错误: {e})。请重新输出完整、合法的 JSON,不要包含任何其它文字。"}
                ]},
            ]
            raw, usage = self.chat(retry, max_tokens=max_tokens, json_mode=True,
                                   temperature=temperature)
            return json.loads(raw), usage

    def _track(self, usage):
        self.requests += 1
        self.total_prompt += usage.get("prompt_tokens", 0) or 0
        self.total_completion += usage.get("completion_tokens", 0) or 0

    def report(self):
        cost = (self.total_prompt / 1000 * PRICE_IN
                + self.total_completion / 1000 * PRICE_OUT)
        return (f"[qwen] 请求 {self.requests} · 输入 {self.total_prompt} tok · "
                f"输出 {self.total_completion} tok · 估价 ≈ {cost:.2f} 元")
