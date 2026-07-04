# -*- coding: utf-8 -*-
"""DeepSeek API 共用客户端(纯 stdlib)。

用法:
    from deepseek_client import DeepSeekClient
    client = DeepSeekClient()
    text, usage = client.chat([{"role": "user", "content": "你好"}])

配置读取 tools/config.local.json(已 gitignore,绝不提交):
    { "api_key": "sk-...", "base_url": "https://api.deepseek.com", "model": "deepseek-chat" }
"""
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
CONFIG_PATH = TOOLS_DIR / "config.local.json"

# deepseek-chat 定价(2026-07,元/百万token),仅用于估价显示
PRICE_IN = 1.0       # 输入(未命中缓存)
PRICE_IN_HIT = 0.1   # 输入(命中缓存)
PRICE_OUT = 2.0      # 输出


def load_config():
    if not CONFIG_PATH.exists():
        raise SystemExit(
            "缺少 tools/config.local.json — 请复制 config.local.json.example 并填入你的 DeepSeek API key"
        )
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    if not cfg.get("api_key") or "替换" in cfg.get("api_key", ""):
        raise SystemExit("config.local.json 中的 api_key 未填写")
    cfg.setdefault("base_url", "https://api.deepseek.com")
    cfg.setdefault("model", "deepseek-chat")
    return cfg


class DeepSeekClient:
    def __init__(self, temperature=0.3, max_retries=5):
        self.cfg = load_config()
        self.temperature = temperature
        self.max_retries = max_retries
        # 累计用量
        self.total_prompt = 0
        self.total_prompt_hit = 0
        self.total_completion = 0
        self.requests = 0

    def chat(self, messages, json_mode=False, max_tokens=4096, temperature=None):
        """发送对话请求,返回 (content_text, usage_dict)。429/5xx/网络错误指数退避重试。"""
        body = {
            "model": self.cfg["model"],
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        payload = json.dumps(body).encode("utf-8")
        url = self.cfg["base_url"].rstrip("/") + "/chat/completions"

        delay = 2
        last_err = None
        for attempt in range(self.max_retries):
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + self.cfg["api_key"],
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=180) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                usage = data.get("usage", {})
                self._track(usage)
                content = data["choices"][0]["message"]["content"]
                return content, usage
            except urllib.error.HTTPError as e:
                detail = ""
                try:
                    detail = e.read().decode("utf-8", "replace")[:300]
                except Exception:
                    pass
                if e.code in (429, 500, 502, 503, 504) and attempt < self.max_retries - 1:
                    print(f"  [retry] HTTP {e.code},{delay}s 后重试… {detail[:120]}")
                    time.sleep(delay)
                    delay = min(delay * 2, 32)
                    last_err = e
                    continue
                raise SystemExit(f"DeepSeek API 错误 HTTP {e.code}: {detail}")
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                if attempt < self.max_retries - 1:
                    print(f"  [retry] 网络错误 {e},{delay}s 后重试…")
                    time.sleep(delay)
                    delay = min(delay * 2, 32)
                    last_err = e
                    continue
                raise SystemExit(f"DeepSeek 网络错误(已重试 {self.max_retries} 次): {e}")
        raise SystemExit(f"DeepSeek 请求失败: {last_err}")

    def chat_json(self, messages, max_tokens=4096, temperature=None):
        """JSON 模式请求;解析失败自动带错误信息重试一次。返回 (obj, usage)。"""
        content, usage = self.chat(messages, json_mode=True, max_tokens=max_tokens,
                                   temperature=temperature)
        try:
            return json.loads(content), usage
        except json.JSONDecodeError as e:
            retry_messages = messages + [
                {"role": "assistant", "content": content},
                {"role": "user",
                 "content": f"你的输出不是合法 JSON(解析错误: {e})。请重新输出完整、合法的 JSON,不要包含任何其他文字。"},
            ]
            content, usage = self.chat(retry_messages, json_mode=True, max_tokens=max_tokens,
                                       temperature=temperature)
            return json.loads(content), usage

    def _track(self, usage):
        self.requests += 1
        self.total_prompt += usage.get("prompt_tokens", 0)
        self.total_prompt_hit += usage.get("prompt_cache_hit_tokens", 0)
        self.total_completion += usage.get("completion_tokens", 0)

    def report(self):
        miss = self.total_prompt - self.total_prompt_hit
        cost = (miss * PRICE_IN + self.total_prompt_hit * PRICE_IN_HIT
                + self.total_completion * PRICE_OUT) / 1_000_000
        return (f"[usage] 请求 {self.requests} 次 | 输入 {self.total_prompt} tok"
                f"(缓存命中 {self.total_prompt_hit}) | 输出 {self.total_completion} tok"
                f" | 估价 ≈ ¥{cost:.3f}")
