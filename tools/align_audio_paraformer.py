# -*- coding: utf-8 -*-
"""用阿里 Paraformer 云端 ASR 自动打点听力 segments[].start。

比 whisper small 更专业:paraformer-v2 是阿里语音团队的专用 ASR 模型,
中英文都好,词级时间戳精度高。

流程:
  1. mp3 URL 提交给 dashscope 异步 task(用 GitHub Pages 上的音频 URL)
  2. 轮询到成功,取 transcription_url 下载 JSON
  3. 抽出 word-level 时间戳,复用 align_audio.py 的对齐算法
  4. 更新 segments[].start

前置:
  - config.local.json 里的 dashscope_key(已配置)
  - mp3 必须已 push 到 GitHub Pages(线上可访问)—— 或者传本地也支持 file:// ?
    实测 paraformer file_urls 必须 http(s),所以走 GitHub Pages CDN

用法:
    py -3 tools/align_audio_paraformer.py c14-test1-l1
    py -3 tools/align_audio_paraformer.py c14-test1-l1 --dry-run
    py -3 tools/align_audio_paraformer.py --all
    py -3 tools/align_audio_paraformer.py --all --workers 4   # 并行 4 个
"""
import argparse
import glob
import json
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "listening"
CONFIG_PATH = ROOT / "tools" / "config.local.json"

# GitHub Pages 上的音频 URL 前缀(用户已 push)
AUDIO_URL_PREFIX = "https://userheyy.github.io/ielts-reader/media/audio/"

DASHSCOPE_BASE = "https://dashscope.aliyuncs.com"
SUBMIT_URL = DASHSCOPE_BASE + "/api/v1/services/audio/asr/transcription"
TASK_URL_TMPL = DASHSCOPE_BASE + "/api/v1/tasks/{task_id}"

# 复用现有对齐函数
sys.path.insert(0, str(Path(__file__).parent))
from align_audio import (  # noqa: E402
    align_segments,
    interp_missing,
    load_json,
    save_json,
)


def load_key():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    key = cfg.get("dashscope_key")
    if not key or key.startswith("sk-替换"):
        raise SystemExit("config.local.json 缺 dashscope_key")
    return key


def _http(url, data=None, headers=None, method="GET", timeout=60, retries=4):
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:500]
            # 4xx 一般不重试;429/5xx 会重试
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                wait = 3 * (attempt + 1)
                print(f"    [http retry {attempt+1}/{retries}] HTTP {e.code},{wait}s...")
                time.sleep(wait)
                last = e
                continue
            raise SystemExit(f"HTTP {e.code} {url}: {body}")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = e
            if attempt < retries - 1:
                wait = 5 * (attempt + 1)
                print(f"    [http retry {attempt+1}/{retries}] {type(e).__name__}: {e}; {wait}s...")
                time.sleep(wait)
                continue
    raise SystemExit(f"HTTP 失败(重试 {retries} 次): {last}")


def submit_task(key, file_urls):
    """提交异步 ASR job,返回 task_id"""
    body = json.dumps({
        "model": "paraformer-v2",
        "input": {"file_urls": file_urls},
        "parameters": {
            "channel_id": [0],
            "language_hints": ["en"],
        },
    }).encode("utf-8")
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    resp = _http(SUBMIT_URL, data=body, headers=headers, method="POST", timeout=90)
    out = resp.get("output", {})
    task_id = out.get("task_id")
    if not task_id:
        raise SystemExit(f"提交失败: {resp}")
    return task_id


def poll_task(key, task_id, max_wait=600, interval=3):
    """轮询直到 SUCCEEDED/FAILED,返回 output"""
    headers = {"Authorization": "Bearer " + key}
    t0 = time.time()
    while time.time() - t0 < max_wait:
        resp = _http(TASK_URL_TMPL.format(task_id=task_id), headers=headers, timeout=60)
        out = resp.get("output", {})
        status = out.get("task_status")
        if status == "SUCCEEDED":
            return out
        if status == "FAILED":
            raise SystemExit(f"Task {task_id} FAILED: {out}")
        time.sleep(interval)
    raise SystemExit(f"Task {task_id} 超时({max_wait}s)")


def download_transcription(url, timeout=60, retries=4):
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = e
            wait = 3 * (attempt + 1)
            print(f"  [dl retry {attempt+1}/{retries}] {e},{wait}s 后重试")
            time.sleep(wait)
    raise SystemExit(f"下载 transcription_url 失败: {last}")


def extract_sentences(transcription):
    """paraformer 天然分句,返回 [{text, start}],以及 duration(秒)。"""
    sents = []
    duration_ms = 0
    for trans in transcription.get("transcripts", []):
        for sentence in trans.get("sentences", []):
            begin = sentence.get("begin_time")
            end = sentence.get("end_time", begin or 0)
            if begin is None:
                continue
            if end > duration_ms:
                duration_ms = end
            sents.append({
                "text": (sentence.get("text") or "").strip(),
                "start": begin / 1000.0,
            })
    return sents, duration_ms / 1000.0


import re as _re
import difflib as _difflib

_NORM_RE = _re.compile(r"[^a-z0-9\s]+")


def _normalize(text):
    return _NORM_RE.sub(" ", (text or "").lower()).strip()


_EXAMPLE_MARKERS = [
    "now we shall begin",
    "listen carefully and answer",
    "you should answer the questions as you listen",
    "the recording will be played once only",
    "so taylor has been written",  # 通用 example 讲解结尾
]


def _find_dialog_start(para_norm):
    """找到 example / introduction 结束的位置,返回真题对话的起始 para 索引。"""
    last_marker = -1
    for i, text in enumerate(para_norm):
        for m in _EXAMPLE_MARKERS:
            if m in text:
                last_marker = i
                break
    return last_marker + 1  # marker 之后才是真题


def align_by_sentences(tape_segments, para_sentences,
                       skip_para_cost=0.4, threshold=0.35):
    """全局 DP 对齐 tape → paraformer sentence。

    先滤除 IELTS example / introduction 区(用固定 marker),
    再对剩下的 para 做 DP 对齐。允许"跳过"para(播音员解说),
    每个 tape seg 必须匹配一个 para sent。低于 threshold 的匹配视为 None。
    """
    T = len(tape_segments)
    P = len(para_sentences)
    if T == 0 or P == 0:
        return [None] * T

    tape_norm = [_normalize(seg.get("en", "")) for seg in tape_segments]
    para_norm_all = [_normalize(s["text"]) for s in para_sentences]

    # 滤除 IELTS example/introduction 部分
    dialog_start = _find_dialog_start(para_norm_all)
    para_norm = para_norm_all[dialog_start:]
    para_offset = dialog_start
    P = len(para_norm)
    if P == 0:  # 保底:标记误滤,回退到全部
        para_norm = para_norm_all
        para_offset = 0
        P = len(para_norm)

    # 预算相似度矩阵。短句(1-3 词)易被 ratio 低估,兜底 substring 匹配
    sim = [[0.0] * P for _ in range(T)]
    for i in range(T):
        if not tape_norm[i]:
            continue
        t = tape_norm[i]
        t_len = len(t.split())
        m = _difflib.SequenceMatcher(None, t)
        for j in range(P):
            m.set_seq2(para_norm[j])
            r = m.ratio()
            if t_len <= 3 and t and t in para_norm[j]:
                r = max(r, 0.75)  # 短 tape 完整出现在 para 里,视为强命中
            sim[i][j] = r

    INF = float("inf")
    dp = [[INF] * (P + 1) for _ in range(T + 1)]
    back = [[0] * (P + 1) for _ in range(T + 1)]  # 0=start,1=match,2=skip_para
    dp[0][0] = 0.0
    for j in range(1, P + 1):
        dp[0][j] = j * skip_para_cost
        back[0][j] = 2

    for i in range(1, T + 1):
        for j in range(1, P + 1):
            # 跳过 para[j-1]
            cost_sp = dp[i][j - 1] + skip_para_cost
            # 匹配 tape[i-1] ↔ para[j-1]
            cost_m = dp[i - 1][j - 1] + (1 - sim[i - 1][j - 1])
            if cost_m <= cost_sp:
                dp[i][j] = cost_m
                back[i][j] = 1
            else:
                dp[i][j] = cost_sp
                back[i][j] = 2

    # 结尾:必须 i=T,j 任意(尾部剩余 para 都可跳过)
    best_j = min(range(P + 1), key=lambda j: dp[T][j])

    # 回溯每个 tape seg 匹配到哪个 para sent
    match_j = [-1] * T
    i, j = T, best_j
    while i > 0 and j > 0:
        if back[i][j] == 1:
            match_j[i - 1] = j - 1
            i -= 1
            j -= 1
        else:
            j -= 1
    while i > 0:  # 起始溢出(异常)
        i -= 1

    result = []
    for i in range(T):
        j = match_j[i]
        if j >= 0 and sim[i][j] >= threshold:
            # 加回 para_offset 映射到原始 para_sentences 索引
            result.append(round(para_sentences[j + para_offset]["start"], 1))
        else:
            result.append(None)
    return result


def process_one(key, pid: str, dry_run=False):
    data = load_json(pid)
    segs = data.get("segments", [])
    if not segs:
        print(f"[skip] {pid}: no segments")
        return None

    audio_rel = data.get("audio", "").replace("\\", "/")
    fname = audio_rel.split("/")[-1]
    audio_url = AUDIO_URL_PREFIX + fname

    cache_dir = ROOT / "tools" / "out"
    cache_dir.mkdir(exist_ok=True)
    cache_fp = cache_dir / f"{pid}.paraformer.json"

    t0 = time.time()
    if cache_fp.exists():
        print(f"[{pid}] 复用缓存 {cache_fp.name}")
        with open(cache_fp, encoding="utf-8") as f:
            trans = json.load(f)
    else:
        print(f"[{pid}] 提交 {fname}...")
        task_id = submit_task(key, [audio_url])
        print(f"  task {task_id[:16]}...")
        out = poll_task(key, task_id)
        result_url = out["results"][0]["transcription_url"]
        trans = download_transcription(result_url)
        with open(cache_fp, "w", encoding="utf-8") as f:
            json.dump(trans, f, ensure_ascii=False, indent=2)
    para_sents, dur = extract_sentences(trans)
    t_asr = time.time() - t0
    print(f"  paraformer: {len(para_sents)} 句 / 音频 {dur:.1f}s / 用时 {t_asr:.1f}s")

    aligned = align_by_sentences(segs, para_sents)
    hit = sum(1 for x in aligned if x is not None)
    new_starts = interp_missing(aligned, audio_duration=dur)
    interp = sum(1 for x, a in zip(new_starts, aligned) if x is not None and a is None)
    print(f"  对齐: {hit}/{len(segs)} 段直接命中 + {interp} 推算")

    if dry_run:
        print("  ── 对比前 8 段(dry-run) ──")
        for i, (s, ns) in enumerate(zip(segs[:8], new_starts[:8])):
            print(f"  seg{i+1}: old={s.get('start')} → new={ns}  |  {s.get('en','')[:60]}")
        return {"hit": hit, "total": len(segs)}

    for s, ns in zip(segs, new_starts):
        if ns is not None:
            s["start"] = ns
    save_json(pid, data)
    print(f"  写回 {pid}.json ✔")
    return {"hit": hit, "total": len(segs)}


def batch_transcribe(key, pids, batch_size=16):
    """批量提交多个 pid 到 paraformer,返回 {pid: transcription_json}。
    只对没有缓存的 pid 提交;有缓存的直接读盘。
    """
    cache_dir = ROOT / "tools" / "out"
    cache_dir.mkdir(exist_ok=True)

    results = {}
    to_submit = []  # [(pid, audio_url)]
    for pid in pids:
        cache_fp = cache_dir / f"{pid}.paraformer.json"
        if cache_fp.exists():
            with open(cache_fp, encoding="utf-8") as f:
                results[pid] = json.load(f)
        else:
            data = load_json(pid)
            audio_rel = data.get("audio", "").replace("\\", "/")
            fname = audio_rel.split("/")[-1]
            to_submit.append((pid, AUDIO_URL_PREFIX + fname))

    if not to_submit:
        print(f"全部 {len(pids)} 篇复用缓存")
        return results

    print(f"提交 {len(to_submit)} 篇到 paraformer(每批 {batch_size})...")
    for batch_start in range(0, len(to_submit), batch_size):
        batch = to_submit[batch_start:batch_start + batch_size]
        urls = [u for _, u in batch]
        pids_in_batch = [p for p, _ in batch]
        print(f"  批 [{batch_start + 1}-{batch_start + len(batch)}] 提交...")
        task_id = submit_task(key, urls)
        print(f"    task {task_id[:16]}...  轮询...")
        out = poll_task(key, task_id, max_wait=1800, interval=5)
        for pid, res in zip(pids_in_batch, out.get("results", [])):
            if res.get("subtask_status") == "SUCCEEDED":
                trans = download_transcription(res["transcription_url"])
                cache_fp = cache_dir / f"{pid}.paraformer.json"
                with open(cache_fp, "w", encoding="utf-8") as f:
                    json.dump(trans, f, ensure_ascii=False, indent=2)
                results[pid] = trans
                print(f"    ✔ {pid}")
            else:
                print(f"    ✗ {pid}: {res.get('subtask_status')} {res.get('message', '')}")
    return results


def align_from_cache(pid, trans, dry_run=False):
    data = load_json(pid)
    segs = data.get("segments", [])
    if not segs:
        return None
    para_sents, dur = extract_sentences(trans)
    aligned = align_by_sentences(segs, para_sents)
    hit = sum(1 for x in aligned if x is not None)
    new_starts = interp_missing(aligned, audio_duration=dur)
    interp = sum(1 for x, a in zip(new_starts, aligned) if x is not None and a is None)
    if not dry_run:
        for s, ns in zip(segs, new_starts):
            if ns is not None:
                s["start"] = ns
        save_json(pid, data)
    return {"hit": hit, "total": len(segs), "interp": interp}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pid", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--batch-size", type=int, default=16,
                    help="paraformer 单次提交多少个 URL(默认 16)")
    args = ap.parse_args()

    if not args.pid and not args.all:
        ap.error("给 pid 或 --all")

    key = load_key()

    if args.pid:
        process_one(key, args.pid, dry_run=args.dry_run)
        return

    files = sorted(Path(p).stem for p in glob.glob(str(DATA_DIR / "c*-test*-l*.json")))
    print(f"总共 {len(files)} 篇")
    trans_map = batch_transcribe(key, files, batch_size=args.batch_size)

    print(f"\n=== 对齐 & 写回 ===")
    stats = []
    for pid in files:
        if pid not in trans_map:
            print(f"  [skip] {pid}: 无转写")
            continue
        try:
            r = align_from_cache(pid, trans_map[pid], dry_run=args.dry_run)
            if r:
                stats.append((pid, r))
                print(f"  {pid}: {r['hit']}/{r['total']} 直接 + {r['interp']} 推算")
        except Exception as e:
            print(f"  [ERR] {pid}: {e}")

    print("\n============ 汇总 ============")
    total_hit = sum(x[1]["hit"] for x in stats)
    total_seg = sum(x[1]["total"] for x in stats)
    print(f"总命中: {total_hit}/{total_seg} = "
          f"{100 * total_hit / max(1, total_seg):.1f}%")


if __name__ == "__main__":
    main()
