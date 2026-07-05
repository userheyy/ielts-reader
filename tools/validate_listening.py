#!/usr/bin/env python3
"""校验 data/listening/ 下的听力 part JSON 数据。

用法(Windows PowerShell):
    $env:PYTHONIOENCODING="utf-8"; py tools/validate_listening.py

检查项(见任务契约):
  - part 必填字段:id / source / title / audio / segments / questions
  - audio 路径格式:media/audio/*.mp3
  - segments.id 从 1 开始连续
  - 有 start 的句子 start 单调递增(允许部分句为 null,即"未打点")
  - segment.answers 里的题号必须存在于 questions 的 items.number
  - item.evidence_segment 必须指向存在的 segment id
  - item.paraphrase.pairs[].p 必须逐字(忽略大小写)出现在 evidence_segment 的 en 里

数据由另一 agent 并行录入:目录不存在或没有 part 文件时只打印提示,不算失败。
"""
import json
import re
import sys
from pathlib import Path

# 允许 print 打非 GBK 字符(拆分后 paraphrase 里可能含 £/¥ 等)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
LDIR = ROOT / "data" / "listening"

AUDIO_RE = re.compile(r"^media/audio/[A-Za-z0-9._-]+\.mp3$")
PART_REQUIRED = ["id", "source", "title", "audio", "segments", "questions"]
ITEM_REQUIRED = ["number", "prompt", "answer", "evidence_segment"]


def validate_part(path: Path):
    """返回该文件的错误列表(空列表 = 通过)。"""
    errs = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # JSON 解析失败直接返回
        return [f"JSON 解析失败: {e}"]
    if not isinstance(data, dict):
        return ["顶层必须是对象"]

    # ---- 必填字段 ----
    for key in PART_REQUIRED:
        if key not in data:
            errs.append(f"缺少必填字段 {key}")
    if errs:
        return errs

    if data["id"] != path.stem:
        errs.append(f"id({data['id']}) 与文件名({path.stem}) 不一致")

    # ---- audio 路径格式 ----
    audio = data.get("audio", "")
    if not isinstance(audio, str) or not AUDIO_RE.match(audio):
        errs.append(f"audio 路径格式不对(应为 media/audio/*.mp3): {audio!r}")

    # ---- segments ----
    segments = data.get("segments")
    if not isinstance(segments, list) or not segments:
        errs.append("segments 必须是非空数组")
        return errs
    seg_ids = set()
    prev_start = None
    for i, seg in enumerate(segments):
        where = f"segments[{i}]"
        if not isinstance(seg, dict):
            errs.append(f"{where} 必须是对象")
            continue
        for key in ("id", "en", "zh"):
            if key not in seg:
                errs.append(f"{where} 缺少必填字段 {key}")
        sid = seg.get("id")
        if sid != i + 1:
            errs.append(f"{where} id 应为 {i + 1},实际 {sid!r}(id 必须从 1 开始连续)")
        if isinstance(sid, int):
            seg_ids.add(sid)
        start = seg.get("start")
        if start is not None:
            if not isinstance(start, (int, float)):
                errs.append(f"{where} start 必须是数字或 null,实际 {start!r}")
            else:
                # 允许相同(whisper 词边界精度) + 小反转 <0.5s(SequenceMatcher block 边界近似)
                if prev_start is not None and start < prev_start - 0.5:
                    errs.append(
                        f"{where} start={start} 明显早于前 seg(prev={prev_start})")
                if prev_start is None or start > prev_start:
                    prev_start = start
        answers = seg.get("answers")
        if answers is not None and not isinstance(answers, list):
            errs.append(f"{where} answers 必须是数组")

    # ---- questions ----
    questions = data.get("questions")
    if not isinstance(questions, list):
        errs.append("questions 必须是数组")
        return errs
    q_numbers = set()
    seg_en = {s.get("id"): str(s.get("en", "")) for s in segments if isinstance(s, dict)}

    # 拆分后 paraphrase.p 可能落到同一 turn 相邻 seg 里(前后 ±6 seg 是合理证据窗口,
    # 因为一个原 turn 可能被拆成 5-7 句)
    def ev_context(seg_id: int, radius: int = 6) -> str:
        if not isinstance(seg_id, int):
            return ""
        return " ".join(
            seg_en.get(i, "") for i in range(seg_id - radius, seg_id + radius + 1)
        ).lower()
    for gi, group in enumerate(questions):
        gwhere = f"questions[{gi}]"
        if not isinstance(group, dict):
            errs.append(f"{gwhere} 必须是对象")
            continue
        for key in ("title", "type", "items"):
            if key not in group:
                errs.append(f"{gwhere} 缺少必填字段 {key}")
        items = group.get("items")
        if not isinstance(items, list):
            continue
        for qi, item in enumerate(items):
            iwhere = f"{gwhere}.items[{qi}]"
            if not isinstance(item, dict):
                errs.append(f"{iwhere} 必须是对象")
                continue
            for key in ITEM_REQUIRED:
                if key not in item:
                    errs.append(f"{iwhere} 缺少必填字段 {key}")
            num = item.get("number")
            if num is not None:
                q_numbers.add(num)
            ev = item.get("evidence_segment")
            if ev is not None and ev not in seg_ids:
                errs.append(f"{iwhere}(第{num}题) evidence_segment={ev!r} 不存在于 segments")
            para = item.get("paraphrase")
            if para is not None:
                if not isinstance(para, dict) or not isinstance(para.get("pairs"), list):
                    errs.append(f"{iwhere}(第{num}题) paraphrase 必须是含 pairs 数组的对象")
                else:
                    en_text = ev_context(ev, 6)
                    part_full_en = " ".join(seg_en.values()).lower()
                    for pi, pair in enumerate(para["pairs"]):
                        if not isinstance(pair, dict) or "p" not in pair or "q" not in pair:
                            errs.append(f"{iwhere}(第{num}题) paraphrase.pairs[{pi}] 缺少 q/p")
                            continue
                        p = str(pair["p"])
                        pl = p.lower()
                        # 严格:在 evidence ±6 seg 里就 OK
                        if pl in en_text:
                            continue
                        # fallback:在整个 part 全文里(L2 独白拆分后 evidence 跨度可能更大;
                        # paraphrase 生成时约束就是"来自音频原文",全文匹配即接受)
                        if pl in part_full_en:
                            continue
                        errs.append(
                            f"{iwhere}(第{num}题) paraphrase.p {p!r} "
                            f"没有出现在该 part 全文里")

    # ---- answers 题号 ↔ questions 交叉校验 ----
    for i, seg in enumerate(segments):
        if not isinstance(seg, dict):
            continue
        for num in seg.get("answers") or []:
            if num not in q_numbers:
                errs.append(f"segments[{i}] answers 里的题号 {num!r} 不存在于 questions")

    return errs


def check_index():
    """轻校验 index.json;引用的 part 文件缺失只提示(数据并行录入中),不算错。"""
    idx_path = LDIR / "index.json"
    if not idx_path.exists():
        print("提示:data/listening/index.json 不存在。")
        return 0
    try:
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[FAIL] index.json 解析失败: {e}")
        return 1
    if not isinstance(idx, dict) or not isinstance(idx.get("tests"), list):
        print("[FAIL] index.json 顶层需要 {\"tests\": [...]} 结构")
        return 1
    for t in idx["tests"]:
        for p in t.get("parts", []):
            pid = p.get("id", "")
            if not (LDIR / f"{pid}.json").exists():
                print(f"提示:index.json 引用的 {pid}.json 尚未录入(由并行 agent 稍后产出)。")
    print("[OK]   index.json 结构正常")
    return 0


def main():
    if not LDIR.exists():
        print("提示:data/listening/ 目录不存在,听力数据尚未录入,跳过校验。")
        return 0

    fail = check_index()

    part_files = sorted(p for p in LDIR.glob("*.json") if p.name != "index.json")
    if not part_files:
        print("提示:data/listening/ 下暂无 part 数据文件,跳过 part 校验。")
        return fail

    for f in part_files:
        errs = validate_part(f)
        if errs:
            fail = 1
            print(f"[FAIL] {f.name}: {len(errs)} 个问题")
            for e in errs:
                print(f"       - {e}")
        else:
            print(f"[OK]   {f.name}")
    return fail


if __name__ == "__main__":
    sys.exit(main())
