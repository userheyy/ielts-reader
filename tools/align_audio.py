# -*- coding: utf-8 -*-
"""用 faster-whisper 自动打点听力 segments[].start。

流程:
  1. 用 whisper 转写 mp3,得到 word-level 时间戳
  2. 对 tapescript 里每个 segment 的 en,在 whisper 词序列里做**滑动指针**匹配,
     取该段前 N 个词首次连贯匹配处的第一词 start 作为 seg.start
  3. 未匹配到的段保持 None(或用前后插值,可后续增强)

用法:
    py -3 tools/align_audio.py c19-test1-l1                     # 单篇
    py -3 tools/align_audio.py --all                            # 全库
    py -3 tools/align_audio.py c19-test1-l1 --model base        # 指定模型
    py -3 tools/align_audio.py c19-test1-l1 --dry-run           # 只报告,不写回

模型选择:base(默认,~74MB,快)/ small(~244MB,准)/ medium(~769MB,更准慢)
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "listening"
AUDIO_DIR = ROOT / "media" / "audio"

_PUNCT_RE = re.compile(r"[.,!?;:\"'()\[\]{}…—–\-]+")


def norm(word: str) -> str:
    return _PUNCT_RE.sub("", (word or "").strip().lower())


def load_json(pid: str) -> dict:
    fp = DATA_DIR / f"{pid}.json"
    with open(fp, encoding="utf-8") as f:
        return json.load(f)


def save_json(pid: str, data: dict) -> None:
    fp = DATA_DIR / f"{pid}.json"
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def audio_path(data: dict) -> Path:
    rel = data.get("audio", "")
    p = ROOT / rel
    return p if p.exists() else None


def transcribe(model, mp3: Path):
    """返回 whisper words: [{w, start, end}]"""
    segments, info = model.transcribe(
        str(mp3),
        word_timestamps=True,
        language="en",
        beam_size=5,
        vad_filter=False,          # 关闭 VAD:短句(如 "Good morning")会被过滤掉
        condition_on_previous_text=False,  # 减少幻觉/漏识别
    )
    words = []
    for seg in segments:
        if seg.words:
            for w in seg.words:
                if w.start is None:
                    continue
                words.append({"w": w.word.strip(), "start": float(w.start), "end": float(w.end)})
    return words, float(info.duration or 0.0)


def _seg_anchor(seg):
    """seg 的锚点词序列(去掉停用词后前几个实词)。"""
    STOP = {"a","an","the","and","or","but","so","of","to","in","on","at","for","is","are","was","were","be","been","being","i","you","he","she","it","we","they","this","that","these","those","have","has","had","do","does","did","will","would","can","could","'s","'re","'ve","'ll","'d","'m","'t"}
    en = seg.get("en", "") or ""
    all_toks = [norm(t) for t in en.split() if norm(t)]
    content = [t for t in all_toks if t not in STOP and len(t) >= 2]
    # 优先返回实词锚点,若太少则退回全部前几词
    if len(content) >= 3:
        return content[:5]
    return all_toks[:5]


def _match_score(w_toks, j, anchor, window=8):
    """从 w_toks[j] 开始向后找 anchor,允许小范围乱序/漏词。返回(命中数, anchor[0] 的位置)。"""
    end = min(j + window + len(anchor), len(w_toks))
    hits = 0
    first_pos = -1
    k = j
    for a in anchor:
        found = -1
        for kk in range(k, min(k + window, end)):
            if w_toks[kk] == a:
                found = kk
                break
        if found >= 0:
            hits += 1
            if first_pos < 0:
                first_pos = found
            k = found + 1
    return hits, first_pos


def align_segments(tape_segments, whisper_words, verbose=False):
    """全局搜索每段 anchor 在 whisper 里的最佳位置(要求单调推进)。

    对每段:在 [ptr, N) 范围内找 anchor 匹配分最高的位置;分不够就 None,不推进 ptr。
    """
    w_toks = [norm(x["w"]) for x in whisper_words]
    w_starts = [x["start"] for x in whisper_words]
    N = len(w_toks)

    result = []
    ptr = 0
    for i, seg in enumerate(tape_segments):
        anchor = _seg_anchor(seg)
        if not anchor:
            result.append(None)
            continue

        best_j = -1
        best_score = 0
        best_first = -1
        # 全序列搜索(允许 whisper 漏识别导致 tape 与 whisper 不同步)
        SEARCH_LIMIT = min(ptr + 300, N)  # 不搜太远
        for j in range(ptr, SEARCH_LIMIT):
            if w_toks[j] != anchor[0]:
                continue  # 快速跳过:首词不匹配的位置
            score, first_pos = _match_score(w_toks, j, anchor)
            if score > best_score:
                best_score = score
                best_j = j
                best_first = first_pos
                if score == len(anchor):
                    break

        # 需要至少匹配 3 个词(或 anchor 全部,如果 anchor 更短)
        threshold = min(3, len(anchor))
        if best_first >= 0 and best_score >= threshold:
            result.append(round(w_starts[best_first], 1))
            ptr = best_first + 1
        else:
            result.append(None)
            if verbose:
                print(f"  [miss] seg{i+1}: anchor={anchor} best_score={best_score}")
    return result


def interp_missing(starts, audio_duration=None):
    """用前后邻居 + 边界推算补齐 None。

    - 中间 None:线性插值
    - 头部 None(dialogue 开头 whisper 常漏):用第一个命中点前推,间距按剩余段平均
    - 尾部 None:用最后一个命中点后推,间距按 audio_duration 或估计
    """
    n = len(starts)
    out = list(starts)

    # ── 中间线性插值
    for i in range(n):
        if out[i] is not None:
            continue
        L = i - 1
        while L >= 0 and out[L] is None:
            L -= 1
        R = i + 1
        while R < n and out[R] is None:
            R += 1
        if L >= 0 and R < n and out[L] is not None and out[R] is not None:
            span = out[R] - out[L]
            steps = R - L
            out[i] = round(out[L] + span * (i - L) / steps, 1)

    # ── 头部推算:从第一个命中点回退
    first_hit = next((i for i, x in enumerate(out) if x is not None), None)
    if first_hit is not None and first_hit > 0:
        # 后续命中点估计平均步长
        follow_hits = [i for i in range(first_hit + 1, n) if out[i] is not None][:5]
        if follow_hits:
            avg_step = (out[follow_hits[-1]] - out[first_hit]) / (follow_hits[-1] - first_hit)
            avg_step = max(1.0, min(6.0, avg_step))  # 每句 1-6s 之间
        else:
            avg_step = 3.0
        for i in range(first_hit - 1, -1, -1):
            v = out[first_hit] - avg_step * (first_hit - i)
            out[i] = round(max(0.0, v), 1)

    # ── 尾部推算:从最后一个命中点往后
    last_hit = next((i for i in range(n - 1, -1, -1) if out[i] is not None), None)
    if last_hit is not None and last_hit < n - 1:
        prev_hits = [i for i in range(last_hit - 1, -1, -1) if out[i] is not None][:5]
        if prev_hits:
            avg_step = (out[last_hit] - out[prev_hits[-1]]) / (last_hit - prev_hits[-1])
            avg_step = max(1.0, min(6.0, avg_step))
        else:
            avg_step = 3.0
        for i in range(last_hit + 1, n):
            v = out[last_hit] + avg_step * (i - last_hit)
            if audio_duration:
                v = min(v, audio_duration)
            out[i] = round(v, 1)

    return out


def process_one(model, pid: str, dry_run=False):
    data = load_json(pid)
    segs = data.get("segments", [])
    if not segs:
        print(f"  [skip] {pid}: no segments")
        return None
    mp3 = audio_path(data)
    if not mp3:
        print(f"  [skip] {pid}: audio missing ({data.get('audio')})")
        return None

    t0 = time.time()
    print(f"  转写 {mp3.name}...")
    whisper_words, dur = transcribe(model, mp3)
    t_asr = time.time() - t0
    print(f"    whisper: {len(whisper_words)} 词 / 音频 {dur:.1f}s / 用时 {t_asr:.1f}s")

    t1 = time.time()
    aligned = align_segments(segs, whisper_words)
    hit = sum(1 for x in aligned if x is not None)
    new_starts = interp_missing(aligned, audio_duration=dur)
    interp = sum(1 for x, a in zip(new_starts, aligned) if x is not None and a is None)
    print(f"    对齐: {hit}/{len(segs)} 段直接命中 + {interp} 推算 (用时 {time.time()-t1:.2f}s)")

    if dry_run:
        # 展示前 8 段的对比
        print(f"    ── 对比前 8 段(dry-run) ──")
        for i, (s, ns) in enumerate(zip(segs[:8], new_starts[:8])):
            print(f"    seg{i+1}: old={s.get('start')} → new={ns}  |  {s.get('en','')[:60]}")
        return {"hit": hit, "total": len(segs)}

    # 写回
    for s, ns in zip(segs, new_starts):
        if ns is not None:
            s["start"] = ns
    save_json(pid, data)
    print(f"    写回 {pid}.json ✔")
    return {"hit": hit, "total": len(segs)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pid", nargs="?", help="part id, e.g. c19-test1-l1")
    ap.add_argument("--all", action="store_true", help="跑全库")
    ap.add_argument("--model", default="small", help="whisper 模型 (tiny/base/small/medium)")
    ap.add_argument("--dry-run", action="store_true", help="只报告,不写回")
    ap.add_argument("--device", default="cpu", help="cpu 或 cuda")
    ap.add_argument("--compute-type", default="int8", help="int8(默认,CPU)/ float16(GPU)")
    args = ap.parse_args()

    if not args.pid and not args.all:
        ap.error("必须给 pid 或 --all")

    from faster_whisper import WhisperModel

    print(f"加载模型 {args.model} ({args.device}, {args.compute_type})...")
    t0 = time.time()
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    print(f"  模型加载 {time.time()-t0:.1f}s")

    if args.pid:
        process_one(model, args.pid, dry_run=args.dry_run)
        return

    # --all
    import glob
    files = sorted(Path(p).stem for p in glob.glob(str(DATA_DIR / "c*-test*-l*.json")))
    print(f"处理 {len(files)} 篇")
    stats = []
    for i, pid in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] {pid}")
        try:
            r = process_one(model, pid, dry_run=args.dry_run)
            if r: stats.append((pid, r))
        except Exception as e:
            print(f"  [ERR] {e}")

    print("\n============ 汇总 ============")
    total_hit = sum(x[1]["hit"] for x in stats)
    total_seg = sum(x[1]["total"] for x in stats)
    print(f"总命中: {total_hit}/{total_seg} = {100*total_hit/max(1,total_seg):.1f}%")


if __name__ == "__main__":
    main()
