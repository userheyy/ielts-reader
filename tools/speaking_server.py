# -*- coding: utf-8 -*-
"""口语练习专用本地服务器:
- 默认端口 8123
- GET *:静态文件服务(同 python -m http.server,项目根目录)
- POST /whisper:接收音频文件(multipart/form-data 里的 audio 字段或原始 body),
  用 faster-whisper 转写,返回 {transcript, duration_sec, language, segments}

替代 start.bat 里的 `python -m http.server`——除了原有静态服务,多加口语录音转写端点。

用法:
    py tools/speaking_server.py                # 端口 8123
    py tools/speaking_server.py --port 8123
    py tools/speaking_server.py --model small.en   # 默认 small.en(int8 CPU 10x realtime)
"""
import argparse
import io
import json
import os
import re
import sys
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


# 手写 multipart/form-data 解析(Python 3.13+ 移除了 cgi 模块)。
# 只支持一次上传一个字段;够用于 POST /whisper 的 audio 字段。
_BOUNDARY_RE = re.compile(r'boundary=(?:"([^"]+)"|([^;]+))', re.IGNORECASE)
_NAME_RE = re.compile(r'name="([^"]*)"')
_FILENAME_RE = re.compile(r'filename="([^"]*)"')


def parse_multipart_audio(body: bytes, ctype_header: str):
    """从 multipart 请求体里抽出 name="audio" 字段的 (content_bytes, filename)。找不到返回 (None, None)。"""
    m = _BOUNDARY_RE.search(ctype_header or "")
    if not m:
        return None, None
    boundary = (m.group(1) or m.group(2) or "").strip()
    if not boundary:
        return None, None
    delim = ("--" + boundary).encode()
    parts = body.split(delim)
    for part in parts:
        part = part.strip(b"\r\n")
        if not part or part == b"--":
            continue
        i = part.find(b"\r\n\r\n")
        if i < 0:
            continue
        headers_bytes = part[:i]
        content = part[i + 4:]
        content = content.rstrip(b"\r\n")
        try:
            headers_str = headers_bytes.decode("utf-8", "replace")
        except Exception:
            continue
        name_m = _NAME_RE.search(headers_str)
        if not name_m or name_m.group(1) != "audio":
            continue
        fn_m = _FILENAME_RE.search(headers_str)
        return content, (fn_m.group(1) if fn_m else "")
    return None, None

ROOT = Path(__file__).resolve().parent.parent  # 项目根 = ielts-reader/

# 全局单例:延迟加载,避免起服务时就吃 model
_MODEL = None
_MODEL_LOCK = threading.Lock()
_MODEL_NAME = "small.en"


def get_model():
    global _MODEL
    if _MODEL is None:
        with _MODEL_LOCK:
            if _MODEL is None:
                from faster_whisper import WhisperModel  # noqa: E402
                print(f"[speaking-server] 加载 faster-whisper {_MODEL_NAME} (int8 CPU) …", flush=True)
                _MODEL = WhisperModel(_MODEL_NAME, device="cpu", compute_type="int8")
                print("[speaking-server] 模型就绪", flush=True)
    return _MODEL


class Handler(SimpleHTTPRequestHandler):
    """静态文件走父类,加一个 POST /whisper 端点。"""

    def log_message(self, fmt, *args):
        # 静默默认 stderr access log,只留自定义日志
        pass

    def do_POST(self):
        if self.path.rstrip("/") == "/whisper":
            self._handle_whisper()
        else:
            self.send_error(404, "Only POST /whisper is supported")

    def _handle_whisper(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length <= 0:
            self._json({"error": "empty body"}, 400)
            return
        ctype = self.headers.get("Content-Type", "")
        try:
            if ctype.lower().startswith("multipart/"):
                body = self.rfile.read(length)
                audio_bytes, fn = parse_multipart_audio(body, ctype)
                if audio_bytes is None:
                    self._json({"error": "missing 'audio' field in multipart body"}, 400)
                    return
                suffix = os.path.splitext(fn or "")[1] or ".webm"
            else:
                audio_bytes = self.rfile.read(length)
                suffix = ".webm"

            if not audio_bytes or len(audio_bytes) < 64:
                self._json({"error": "audio too small"}, 400)
                return

            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
                f.write(audio_bytes)
                tmp_path = f.name

            try:
                model = get_model()
                segments, info = model.transcribe(
                    tmp_path, beam_size=1, vad_filter=True,
                    language="en", word_timestamps=False,
                )
                segs = []
                text_parts = []
                for s in segments:
                    txt = (s.text or "").strip()
                    if not txt:
                        continue
                    segs.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": txt})
                    text_parts.append(txt)
                full_text = " ".join(text_parts).strip()
                self._json({
                    "transcript": full_text,
                    "duration_sec": round(info.duration, 2),
                    "language": info.language,
                    "segments": segs,
                })
                print(f"[whisper] {info.duration:.1f}s audio → {len(segs)} segs / {len(full_text)} chars", flush=True)
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
        except Exception as e:
            self._json({"error": f"{type(e).__name__}: {e}"}, 500)

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        # 同源无需 CORS,但保留兜底(方便本地 file:// 或跨端口调试)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("IELTS_PORT", 8123)))
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--model", default="small.en", help="tiny.en / base.en / small.en / medium.en")
    args = ap.parse_args()

    global _MODEL_NAME
    _MODEL_NAME = args.model

    handler_cls = partial(Handler, directory=str(ROOT))
    with ThreadingHTTPServer((args.host, args.port), handler_cls) as httpd:
        print(f"[speaking-server] 静态目录: {ROOT}", flush=True)
        print(f"[speaking-server] 监听 http://{args.host}:{args.port}", flush=True)
        print(f"[speaking-server]   GET   /**             静态文件", flush=True)
        print(f"[speaking-server]   POST  /whisper        音频转写(multipart audio 字段 或 raw body)", flush=True)
        print(f"[speaking-server] Whisper 模型将在首个 POST /whisper 时懒加载 ({_MODEL_NAME}).", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[speaking-server] 停止", flush=True)


if __name__ == "__main__":
    sys.exit(main())
