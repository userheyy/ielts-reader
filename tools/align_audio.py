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
    py -3 tools/align_audio.py --books c1                       # 指定册数
    py -3 tools/align_audio.py --books c2,c3,c4,c5              # 多册
    py -3 tools/align_audio.py c19-test1-l1 --model base        # 指定模型
    py -3 tools/align_audio.py c19-test1-l1 --dry-run           # 只报告,不写回

模型选择:base(默认,~74MB,快)/ small(~244MB,准)/ medium(~769MB,更准慢)
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "listening"
AUDIO_DIR = ROOT / "media" / "audio"

# Very short acknowledgements can be omitted by ASR even when the waveform is
# present. Keep the two verified anchors for the repaired C19T1P1 recording so
# a future alignment run does not move them into the adjacent sentence.
MANUAL_START_OVERRIDES = {
    "c19-test1-l1": {3: 120.0, 14: 222.0},
    # base.en 将 Hearst 误识别为 "Herst"，导致这一轮被插值到上一句
    # 中间；按原声的首词时间固定锚点，避免上一句被 next_start 截断。
    "c10-test1-l1": {27: 274.6},
}

_PUNCT_RE = re.compile(r"[.,!?;:\"'()\[\]{}…—–\-]+")
_TOKEN_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?|\d+")


def norm(word: str) -> str:
    text = (word or "").strip().lower()
    # Transcript overrides often use typographic apostrophes (that’s) while
    # ASR emits ASCII ones (that's); normalize both before token matching.
    text = text.replace("’", "'").replace("‘", "'")
    text = _PUNCT_RE.sub("", text)
    # Short acknowledgements are routinely transcribed as "okay" even when
    # the audioscript writes "OK". Treat them as the same anchor token.
    return "okay" if text == "ok" else text


def tokenize(text: str):
    """把原文拆成可用于词级对齐的 token。

    不能直接用 ``str.split``：像 ``self-drive``、``A-R-D-L-E-I-G-H``
    会在 Whisper 中被拆成多个词，直接比较会让匹配指针漂移到下一句。
    """
    text = (text or "").replace("’", "'").replace("‘", "'")
    return [norm(t) for t in _TOKEN_RE.findall(text) if norm(t)]


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


def decode_pcm(mp3: Path, sample_rate=16000):
    """把整段音频解成单声道 PCM，供句尾能量检测使用。"""
    try:
        import numpy as np

        raw = subprocess.check_output([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(mp3),
            "-ac", "1", "-ar", str(sample_rate), "-f", "s16le", "-",
        ])
        return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0, sample_rate
    except Exception as exc:
        print(f"    能量检测跳过: {exc}")
        return None, sample_rate


def extend_end_by_energy(end, start_time, next_start, pcm, sample_rate=16000):
    """用波形尾部能量补齐 ASR 偏短的句尾。

    Whisper 的词尾通常比真实发音短 0.1–0.3 秒（尤其是 /d/、/s/、/t/
    的释放音）。在当前句候选尾点附近扫描 20ms 能量帧，向后延到最后一
    个有声帧后的短保护区；同时严格留在下一句首词之前，避免把下一句
    的开头吞进来。
    """
    if end is None or pcm is None or start_time is None:
        return end
    # 即使下一句很远（中间可能夹着官方读题音频），也只在当前词尾
    # 附近扫描；不能把被省略的读题音频当成当前句的尾音。
    cap = float(end) + 0.8
    if next_start is not None and next_start > start_time:
        cap = min(cap, float(next_start) - 0.05)
    if cap <= float(end):
        return end
    import numpy as np

    frame = max(1, round(sample_rate * 0.02))
    hop = max(1, round(sample_rate * 0.01))
    lo = max(0, int((float(end) - 0.4) * sample_rate))
    hi = min(len(pcm), int(cap * sample_rate))
    if hi <= lo + frame:
        return end
    values = pcm[lo:hi]
    starts = np.arange(0, len(values) - frame + 1, hop)
    rms = np.sqrt(np.mean(values[starts[:, None] + np.arange(frame)] ** 2, axis=1))
    # 低于 0.008 的通常是编码底噪/呼吸尾巴；保留到有声帧后约 0.1s。
    active = np.flatnonzero(rms >= 0.008)
    if active.size == 0:
        return end
    last_frame_end = (lo + int(active[-1]) * hop + frame) / sample_rate
    extended = min(cap, last_frame_end + 0.10)
    return round(max(float(end), extended), 1)


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
    """全局搜索每段原文在 Whisper 词序列中的最佳位置。

    旧版只匹配去掉停用词后的 ``anchor``，遇到 ``Good morning`` 这类
    重复开头时，首个词稍微偏移就可能跳到下一轮发言；之后句尾也会
    跟着错位，出现“吞首词/留上一句尾音”。现在优先用原文第一词做
    候选，再在一个很小的窗口内顺序核对整句；只有首词漏识别时才退回
    旧的实词 anchor。
    """
    w_toks = [norm(x["w"]) for x in whisper_words]
    w_starts = [x["start"] for x in whisper_words]
    N = len(w_toks)

    result = []
    ptr = 0
    for i, seg in enumerate(tape_segments):
        target = tokenize(seg.get("en", ""))
        if not target:
            result.append(None)
            continue

        # 首词候选：每个目标词最多向后容忍 4 个 ASR 词，避免跨到下一轮。
        best_j = -1
        best_hits = -1
        best_skips = 10**9
        SEARCH_LIMIT = min(ptr + 300, N)
        for j in range(ptr, SEARCH_LIMIT):
            if w_toks[j] != target[0]:
                continue
            pos = j
            hits = 0
            skips = 0
            for token in target:
                found = None
                for kk in range(pos, min(pos + 5, N)):
                    if w_toks[kk] == token:
                        found = kk
                        break
                if found is None:
                    skips += 1
                    continue
                hits += 1
                pos = found + 1
            if (hits > best_hits) or (hits == best_hits and skips < best_skips):
                best_j, best_hits, best_skips = j, hits, skips
                if hits == len(target):
                    break

        # 首词漏识别时，退回原来的实词 anchor 搜索。
        if best_j < 0 or best_hits < min(2, len(target)):
            anchor = _seg_anchor(seg)
            fallback_j = -1
            fallback_score = 0
            fallback_first = -1
            for j in range(ptr, SEARCH_LIMIT):
                if not anchor or w_toks[j] != anchor[0]:
                    continue
                score, first_pos = _match_score(w_toks, j, anchor)
                if score > fallback_score:
                    fallback_score, fallback_j, fallback_first = score, j, first_pos
                    if score == len(anchor):
                        break
            if fallback_first >= 0 and fallback_score >= min(3, len(anchor)):
                best_j, best_hits = fallback_first, fallback_score

        threshold = 1 if len(target) <= 2 else max(2, min(4, round(len(target) * 0.25)))
        if best_j >= 0 and best_hits >= threshold:
            result.append(round(w_starts[best_j], 1))
            ptr = best_j + 1
        else:
            result.append(None)
            if verbose:
                print(f"  [miss] seg{i+1}: first={target[0] if target else ''} best_score={best_hits}")
    return result


def _full_target_tokens(seg):
    """返回句子的完整可匹配词序列。"""
    return tokenize(seg.get("en", "") or "")


def match_segment_end(seg, whisper_words, start_time, next_start=None):
    """用词级时间戳寻找句尾，避免直接被下一句 start 截断。

    起点已经由 anchor 对齐得到；这里从起点附近开始，按原文词序做宽松
    匹配，取最后一个命中词的 end，并留出约 0.25 秒尾音余量。短回应或
    ASR 漏词时返回 None，由前端回退到下一句起点。
    """
    if start_time is None or not whisper_words:
        return None
    target = _full_target_tokens(seg)
    if not target:
        return None
    # 起点是旧数据时，可能落在首词的中间（例如 Good 的 start 被写成
    # morning 的 start）。向前回看约 1 秒，确保首词仍能参与匹配。
    start_idx = 0
    for i, word in enumerate(whisper_words):
        if float(word.get("end", 0.0)) >= float(start_time) - 1.0:
            start_idx = i
            break

    # 句尾不能跨入下一句。留出极小余量给词尾，避免把下一句的首词
    # 当作当前句的尾巴。
    limit = len(whisper_words)
    if next_start is not None and next_start > float(start_time):
        limit = min(limit, next((i for i, w in enumerate(whisper_words)
                                 if float(w.get("start", 0.0)) >= float(next_start) + 0.08), limit))
    limit = min(limit, start_idx + max(32, len(target) * 4))

    # 在起点附近寻找“首词 + 顺序词列”的最佳候选。每个目标词最多
    # 向后容忍 4 个 ASR 词，既能跨过漏识别，也不会漂到下一轮发言。
    best = None
    for candidate in range(start_idx, min(limit, start_idx + 10)):
        if norm(whisper_words[candidate].get("w", "")) != target[0]:
            continue
        pos = candidate
        matched = []
        skips = 0
        for token in target:
            found = None
            for j in range(pos, min(pos + 5, limit)):
                if norm(whisper_words[j].get("w", "")) == token:
                    found = j
                    break
            if found is None:
                skips += 1
                continue
            matched.append(found)
            pos = found + 1
        score = len(matched)
        # 同样命中数时取更早的候选；录音里常有“题目示例/回放说明”
        # 重复复述，取后一个会把句尾拖到说明音频里。
        candidate_score = (score, -skips, -candidate)
        if best is None or candidate_score > best[0]:
            best = (candidate_score, matched)

    matched = best[1] if best else []
    # 长句允许少量漏词；只有一个命中词的句子不够可靠。
    minimum = 1 if len(target) <= 2 else max(2, min(4, round(len(target) * 0.25)))
    if len(matched) < minimum:
        return None
    end = float(whisper_words[matched[-1]].get("end", 0.0)) + 0.25
    if end <= float(start_time):
        return None
    # 不让一个句子的尾巴吞掉下一句的起点；若两句存在重叠，至少保留
    # 当前句的真实词尾，避免再次出现“还没读完就切掉”。
    if next_start is not None and next_start > float(start_time):
        end = min(end, max(float(start_time) + 0.35, float(next_start) - 0.05))
    if end <= float(start_time) + 0.15:
        return None
    return round(end, 1)


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


def process_one(model, pid: str, dry_run=False, ends_only=False):
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
    pcm, pcm_rate = decode_pcm(mp3)

    if ends_only:
        # 批量优化已存在的句首时间，不重新对齐 start，避免低型号 ASR
        # 把已经人工校准过的句首拖偏。
        aligned = [s.get("start") if isinstance(s.get("start"), (int, float)) else None for s in segs]
        hit = sum(1 for x in aligned if x is not None)
        new_starts = list(aligned)
        print(f"    句首: 保留现有时间 {hit}/{len(segs)} 段")
    else:
        t1 = time.time()
        aligned = align_segments(segs, whisper_words)
        hit = sum(1 for x in aligned if x is not None)
        new_starts = interp_missing(aligned, audio_duration=dur)
        interp = sum(1 for x, a in zip(new_starts, aligned) if x is not None and a is None)
        print(f"    对齐: {hit}/{len(segs)} 段直接命中 + {interp} 推算 (用时 {time.time()-t1:.2f}s)")

    # 先应用人工锚点，再用词级时间戳估计每句真正的结束时间。
    effective_starts = []
    for s, ns in zip(segs, new_starts):
        override = MANUAL_START_OVERRIDES.get(pid, {}).get(s.get("id"))
        # 即使是 --ends-only，句尾计算也必须使用人工锚点；否则一个
        # 已知的首词误识别仍会把上一句的尾音截到错误位置。
        effective_starts.append(override if override is not None else ns)
    new_ends = []
    end_hits = 0
    for i, (s, start) in enumerate(zip(segs, effective_starts)):
        old_end = s.get("end")
        # 重复/不递增的句首是旧数据里常见的尾部异常；找下一个真正
        # 更晚的句首作为上限，避免能量扫描被卡在同一时间点。
        next_start = dur
        if start is not None:
            for candidate in effective_starts[i + 1:]:
                if candidate is not None and candidate > float(start) + 0.05:
                    next_start = candidate
                    break
        end = match_segment_end(s, whisper_words, start, next_start)
        end = extend_end_by_energy(end, start, next_start, pcm, pcm_rate)
        # 如果本次 ASR 没有找到对应词，保留已有的人工/历史句尾，
        # 仍然让下面的统一边界保护对它生效；不能因为一次未命中
        # 就把原本可播放的句尾悄悄留成旧的越界值。
        if end is None and isinstance(s.get("end"), (int, float)):
            end = float(s["end"])
        # 所有时间统一保留 1 位小数；句尾最多到下一句的起点，
        # 这样不会吞入下一句，同时不会因 ``next_start - 0.05``
        # 的四舍五入把上一句错误地缩短一整格。
        if end is not None and next_start is not None and next_start > float(start or 0):
            safe_end = round(float(next_start), 1)
            end = min(float(end), safe_end)
            end = round(end, 1)
            # 极短回应可能和下一轮的旧句首落在同一百毫秒内。
            # 此时优先保留已有的完整句尾，稍后统一把下一句句首
            # 推到这里，避免为了满足旧句首而吞掉尾音。
            if (
                isinstance(old_end, (int, float))
                and end <= float(start or 0) + 0.15
                and float(old_end) > end
            ):
                end = round(float(old_end), 1)
        new_ends.append(end)
        if end is not None:
            end_hits += 1

    # 旧数据中偶尔会出现连续短回应的句首互相挤压。保持句首单调，
    # 并在上一句已有可靠句尾时把下一句推到该句尾；这只会调整冲突
    # 的边界，不会改变正常段落的人工校准时间。
    normalized_starts = list(effective_starts)
    for i in range(1, len(normalized_starts)):
        cur = normalized_starts[i]
        if cur is None:
            continue
        floor_start = normalized_starts[i - 1]
        prev_end = new_ends[i - 1]
        if isinstance(prev_end, (int, float)):
            floor_start = max(float(floor_start), float(prev_end)) if isinstance(floor_start, (int, float)) else float(prev_end)
        if isinstance(floor_start, (int, float)) and float(cur) < float(floor_start):
            normalized_starts[i] = round(float(floor_start), 1)
    print(f"    句尾: {end_hits}/{len(segs)} 段使用词级结束点")

    if dry_run:
        # 展示前 8 段的对比
        print(f"    ── 对比前 8 段(dry-run) ──")
        for i, (s, ns, end) in enumerate(zip(segs[:8], effective_starts[:8], new_ends[:8])):
            print(f"    seg{i+1}: start={ns} → end={end}  |  {s.get('en','')[:60]}")
        return {"hit": hit, "total": len(segs), "end_hits": end_hits}

    # 写回
    for s, ns, end in zip(segs, normalized_starts, new_ends):
        original_start = s.get("start")
        changed_conflict_start = (
            isinstance(original_start, (int, float))
            and isinstance(ns, (int, float))
            and abs(float(original_start) - float(ns)) >= 0.05
        )
        if ns is not None and (not ends_only or changed_conflict_start):
            s["start"] = ns
        if end is not None and ns is not None and end > ns + 0.15:
            s["end"] = end
    save_json(pid, data)
    print(f"    写回 {pid}.json [OK]")
    return {"hit": hit, "total": len(segs), "end_hits": end_hits}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pid", nargs="?", help="part id, e.g. c19-test1-l1")
    ap.add_argument("--all", action="store_true", help="跑全库")
    ap.add_argument(
        "--books",
        help="只处理指定册数，逗号分隔，如 c1 或 c2,c3,c4,c5",
    )
    ap.add_argument("--model", default="small", help="whisper 模型 (tiny/base/small/medium)")
    ap.add_argument("--dry-run", action="store_true", help="只报告,不写回")
    ap.add_argument(
        "--ends-only",
        action="store_true",
        help="只根据词级时间戳重算 end，保留 JSON 中已有的 start",
    )
    ap.add_argument("--device", default="cpu", help="cpu 或 cuda")
    ap.add_argument("--compute-type", default="int8", help="int8(默认,CPU)/ float16(GPU)")
    args = ap.parse_args()

    if not args.pid and not args.all and not args.books:
        ap.error("必须给 pid、--all 或 --books")
    if args.pid and (args.all or args.books):
        ap.error("pid、--all 和 --books 只能选择一种")
    if args.all and args.books:
        ap.error("--all 和 --books 只能选择一种")

    from faster_whisper import WhisperModel

    print(f"加载模型 {args.model} ({args.device}, {args.compute_type})...")
    t0 = time.time()
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    print(f"  模型加载 {time.time()-t0:.1f}s")

    if args.pid:
        process_one(model, args.pid, dry_run=args.dry_run, ends_only=args.ends_only)
        return

    # --all / --books
    import glob
    files = sorted(Path(p).stem for p in glob.glob(str(DATA_DIR / "c*-test*-l*.json")))
    if args.books:
        books = set()
        for raw in args.books.split(","):
            value = raw.strip().lower()
            if not value:
                continue
            if value.isdigit():
                value = f"c{value}"
            if not re.fullmatch(r"c\d+", value):
                ap.error(f"无效册数: {raw!r}，示例: c1,c2")
            books.add(value)
        files = [pid for pid in files if pid.split("-", 1)[0] in books]
        if not files:
            ap.error(f"未找到指定册数的数据: {args.books}")
    print(f"处理 {len(files)} 篇")
    stats = []
    for i, pid in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] {pid}")
        try:
            r = process_one(model, pid, dry_run=args.dry_run, ends_only=args.ends_only)
            if r: stats.append((pid, r))
        except Exception as e:
            print(f"  [ERR] {e}")

    print("\n============ 汇总 ============")
    total_hit = sum(x[1]["hit"] for x in stats)
    total_seg = sum(x[1]["total"] for x in stats)
    print(f"总命中: {total_hit}/{total_seg} = {100*total_hit/max(1,total_seg):.1f}%")
    total_end = sum(x[1].get("end_hits", 0) for x in stats)
    print(f"句尾命中: {total_end}/{total_seg} = {100*total_end/max(1,total_seg):.1f}%")


if __name__ == "__main__":
    main()
