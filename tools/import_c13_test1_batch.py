"""Restore the completed Cambridge IELTS 13 Test 1 batch into the built-in library.

The source JSON files were retained in passages_archive when the library was
temporarily limited to Cambridge 14-19.  This importer keeps the archive as the
source of truth, normalises the current quality field, and rebuilds index rows
using the same counts as validate_data.py.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "data" / "passages_archive" / "pre_c14_19_seed"
PASSAGES = ROOT / "data" / "passages"
INDEX = ROOT / "data" / "index.json"
IDS = ["c13-test1-p1", "c13-test1-p2", "c13-test1-p3"]


def analysis_count(passage: dict) -> int:
    return sum(len(sentence.get("details", [])) or 1 for sentence in passage["sentences"])


def question_count(passage: dict) -> int:
    return sum(len(group.get("items", [])) for group in passage.get("questions", []))


def main() -> None:
    restored = []
    PASSAGES.mkdir(parents=True, exist_ok=True)

    for passage_id in IDS:
        source_path = ARCHIVE / f"{passage_id}.json"
        passage = json.loads(source_path.read_text(encoding="utf-8"))
        passage["quality"] = "teacher_refined"
        target_path = PASSAGES / source_path.name
        target_path.write_text(
            json.dumps(passage, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        restored.append(passage)

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    restored_ids = set(IDS)
    existing = [row for row in index.get("passages", []) if row.get("id") not in restored_ids]
    rows = [
        {
            "id": passage["id"],
            "source": passage["source"],
            "title": passage["title"],
            "sentence_count": analysis_count(passage),
            "question_count": question_count(passage),
            "quality": passage["quality"],
        }
        for passage in restored
    ]
    index["passages"] = rows + existing
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for row in rows:
        print(
            f"{row['id']}: {row['sentence_count']} 个精读单元, "
            f"{row['question_count']} 题"
        )


if __name__ == "__main__":
    main()
