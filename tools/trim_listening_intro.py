# -*- coding: utf-8 -*-
"""一次性移除听力录音开头的考试引导语，并重新编号正文句子。

只对明确指定的 Part 执行，避免把全库的录音说明误当作正文批量删除。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "listening"


def trim(pid: str, keep_from_id: int) -> None:
    path = DATA_DIR / f"{pid}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    original = data.get("segments", [])
    kept = [seg for seg in original if int(seg.get("id", 0)) >= keep_from_id]
    if not kept:
        raise ValueError(f"{pid}: no segment remains after {keep_from_id}")
    offset = keep_from_id - 1
    for seg in kept:
        seg["id"] = int(seg["id"]) - offset
    for group in data.get("questions", []):
        for item in group.get("items", []):
            evidence = item.get("evidence_segment")
            if isinstance(evidence, int):
                item["evidence_segment"] = evidence - offset if evidence >= keep_from_id else None
    data["segments"] = kept
    data["practice_start"] = kept[0].get("start")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{pid}: removed {len(original) - len(kept)} intro segments; kept {len(kept)}")


if __name__ == "__main__":
    trim("c10-test1-l2", 6)
