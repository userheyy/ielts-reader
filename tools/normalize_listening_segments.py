# -*- coding: utf-8 -*-
"""Normalize listening practice units.

Dialogue parts are practised by speaker turn: consecutive fragments spoken by
the same person are merged into one unit. Monologues stay sentence based.

This reverses the old "split every punctuation sentence" behaviour that made a
single answer from one speaker appear as several artificial practice rows.

Usage:
    py tools/normalize_listening_segments.py --dry-run
    py tools/normalize_listening_segments.py --only c14-test1-l1
    py tools/normalize_listening_segments.py
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "listening"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def is_dialogue(part_id, segments):
    # IELTS Part 1 and Part 3 are conversations. Part 2 and Part 4 are
    # monologues; occasional extra speaker labels there are extraction noise.
    if not (str(part_id).endswith("-l1") or str(part_id).endswith("-l3")):
        return False
    speakers = {
        str(seg.get("speaker") or "").strip().upper()
        for seg in segments
        if str(seg.get("speaker") or "").strip()
    }
    return len(speakers) >= 2


def merge_words(groups):
    out = []
    seen = set()
    for words in groups:
        for word in words or []:
            key = (
                str(word.get("w") or "").strip().lower(),
                str(word.get("pos") or "").strip().lower(),
                str(word.get("def") or "").strip(),
            )
            if not key[0] or key in seen:
                continue
            seen.add(key)
            out.append(word)
    return out


def merge_dialogue_turns(data):
    old_segments = data.get("segments") or []
    if not is_dialogue(data.get("id"), old_segments):
        return data, {"dialogue": False, "old": len(old_segments), "new": len(old_segments)}

    turns = []
    for seg in old_segments:
        speaker = str(seg.get("speaker") or "").strip()
        if turns and turns[-1][0] == speaker:
            turns[-1][1].append(seg)
        else:
            turns.append((speaker, [seg]))

    old_to_new = {}
    new_segments = []
    for speaker, group in turns:
        new_id = len(new_segments) + 1
        for seg in group:
            old_to_new[seg.get("id")] = new_id

        starts = [seg.get("start") for seg in group if isinstance(seg.get("start"), (int, float))]
        answers = sorted({n for seg in group for n in (seg.get("answers") or []) if isinstance(n, int)})
        english = " ".join(str(seg.get("en") or "").strip() for seg in group).strip()
        chinese = " ".join(str(seg.get("zh") or "").strip() for seg in group if str(seg.get("zh") or "").strip()).strip()
        new_segments.append({
            "id": new_id,
            "start": starts[0] if starts else None,
            "speaker": speaker,
            "en": english,
            "zh": chinese,
            "words": merge_words(seg.get("words") for seg in group),
            "answers": answers,
        })

    for question_group in data.get("questions") or []:
        for item in question_group.get("items") or []:
            old_evidence = item.get("evidence_segment")
            if old_evidence in old_to_new:
                item["evidence_segment"] = old_to_new[old_evidence]

    data["segments"] = new_segments
    data["practice_unit"] = "speaker_turn"
    return data, {"dialogue": True, "old": len(old_segments), "new": len(new_segments)}


def process(path, dry_run=False):
    data = load_json(path)
    data, stats = merge_dialogue_turns(data)
    if stats["dialogue"] and not dry_run:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="Comma-separated part ids")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    wanted = {x.strip() for x in (args.only or "").split(",") if x.strip()}
    files = sorted(DATA_DIR.glob("c*-test*-l*.json"))
    if wanted:
        files = [path for path in files if path.stem in wanted]

    dialogue_count = 0
    old_total = 0
    new_total = 0
    for path in files:
        stats = process(path, dry_run=args.dry_run)
        if stats["dialogue"]:
            dialogue_count += 1
            old_total += stats["old"]
            new_total += stats["new"]
            print(f"{path.stem}: {stats['old']} -> {stats['new']} speaker turns")

    suffix = " [dry-run]" if args.dry_run else ""
    print(f"Dialogue parts: {dialogue_count}; units: {old_total} -> {new_total}{suffix}")


if __name__ == "__main__":
    main()
