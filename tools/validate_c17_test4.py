"""Regression checks for the repaired Cambridge IELTS 17 Test 4 passages."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSAGES = ROOT / "data" / "passages"

EXPECTED = {
    "c17-test4-p1": {
        "paragraph_sizes": [6, 5, 1, 2, 3, 1, 2, 4, 2, 2, 7, 4],
        "first": "There are few places in the world where relations between agriculture and conservation are more strained.",
        "last": "‘If we give nature a hand, we can speed up the process of regeneration.’",
        "answers": ["FALSE", "FALSE", "NOT GIVEN", "TRUE", "NOT GIVEN", "TRUE", "droppings", "coffee", "mosquitoes", "protein", "unclean", "culture", "houses"],
        "evidence": [4, 6, 9, 15, 14, 16, 20, 24, 28, 30, 32, 33, 35],
    },
    "c17-test4-p2": {
        "paragraph_sizes": [3, 5, 6, 9, 7, 9],
        "first": "Over the last decade, a huge database about the lives of southwest German villagers between 1600 and 1900 has been compiled by a team led by Professor Sheilagh Ogilvie at Cambridge University’s Faculty of Economics.",
        "last": "If economic institutions are poorly set up, for instance, education can’t lead to growth.’",
        "answers": ["E", "A", "D", "F", "C", "descendants", "sermon", "fine", "innovation", "B", "E", "B", "D"],
        "evidence": [26, 2, 21, 33, 10, 16, 18, 21, 23, 7, 8, 36, 35],
    },
    "c17-test4-p3": {
        "paragraph_sizes": [10, 6, 5, 4, 11, 12, 4, 5],
        "first": "Next month, a chess player named Timur Gareyev will take on nearly 50 opponents at once.",
        "last": "I miss having an obsession.’",
        "answers": ["D", "E", "F", "B", "H", "E", "FALSE", "NOT GIVEN", "NOT GIVEN", "TRUE", "memory", "numbers", "communication", "visual"],
        "evidence": [23, 27, 42, 12, 56, 34, 3, 6, 12, 14, 37, 39, 45, 50],
    },
}


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> None:
    for passage_id, expected in EXPECTED.items():
        data = json.loads((PASSAGES / f"{passage_id}.json").read_text(encoding="utf-8"))
        sentences = data["sentences"]
        items = [item for group in data["questions"] for item in group["items"]]

        actual_sizes = []
        for para in range(1, max(row["para"] for row in sentences) + 1):
            actual_sizes.append(sum(row["para"] == para for row in sentences))
        if actual_sizes != expected["paragraph_sizes"]:
            fail(f"{passage_id}: paragraph sizes {actual_sizes} != {expected['paragraph_sizes']}")
        if sentences[0]["en"] != expected["first"] or sentences[-1]["en"] != expected["last"]:
            fail(f"{passage_id}: first/last sentence fingerprint mismatch")
        if [item["answer"] for item in items] != expected["answers"]:
            fail(f"{passage_id}: official answers changed")
        if [item["evidence_sentence"] for item in items] != expected["evidence"]:
            fail(f"{passage_id}: evidence mapping changed")

        sentence_text = {row["id"]: row["en"] for row in sentences}
        for item in items:
            evidence = item["evidence_sentence"]
            if evidence not in sentence_text:
                fail(f"{passage_id} Q{item['number']}: missing evidence sentence {evidence}")
            analysis = item.get("paraphrase")
            if not analysis or not analysis.get("pairs") or not analysis.get("explain"):
                fail(f"{passage_id} Q{item['number']}: incomplete answer analysis")
            for pair in analysis["pairs"]:
                if pair["p"].lower() not in sentence_text[evidence].lower():
                    fail(f"{passage_id} Q{item['number']}: quoted evidence is not in sentence {evidence}")

        print(f"OK {passage_id}: {len(sentences)} sentences, {len(actual_sizes)} paragraphs, {len(items)} questions")


if __name__ == "__main__":
    main()
