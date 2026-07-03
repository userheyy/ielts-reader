"""Generate draft JSONs for Cambridge IELTS 17 Tests 2-4.

This is the first layer only: OCR/PDF text is used as a reviewed source draft,
with answers from the official answer key. Files remain marked `draft_raw`
until a teacher-refinement script upgrades translation/grammar/phrases.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp" / "c17_pages"
PASSAGES = ROOT / "data" / "passages"
INDEX = ROOT / "data" / "index.json"


BOOK = {
    "c17-test2-p1": {
        "source": "剑桥雅思17 · Test 2 · Passage 1",
        "title": "The Dead Sea Scrolls",
        "file": "test2.txt",
        "start": "The Dead Sea Scrolls",
        "end": "Questions 1–5",
        "answers": ["rock", "cave", "clay", "Essenes", "Hebrew", "NOT GIVEN", "FALSE", "TRUE", "TRUE", "FALSE", "FALSE", "TRUE", "NOT GIVEN"],
    },
    "c17-test2-p2": {
        "source": "剑桥雅思17 · Test 2 · Passage 2",
        "title": "A second attempt at domesticating the tomato",
        "file": "test2.txt",
        "start": "A second attempt at domesticating the tomato",
        "end": "Questions 14–18",
        "answers": ["C", "B", "E", "A", "C", "B", "D", "A", "C", "A", "flavour", "size", "salt"],
        "q_offset": 14,
    },
    "c17-test2-p3": {
        "source": "剑桥雅思17 · Test 2 · Passage 3",
        "title": "Insight or evolution?",
        "file": "test2.txt",
        "start": "Insight or evolution?",
        "end": "Questions 27–31",
        "answers": ["D", "A", "A", "C", "A", "NO", "NOT GIVEN", "YES", "NO", "NOT GIVEN", "F", "D", "E", "B"],
        "q_offset": 27,
    },
    "c17-test3-p1": {
        "source": "剑桥雅思17 · Test 3 · Passage 1",
        "title": "The thylacine",
        "file": "test3.txt",
        "start": "The thylacine",
        "end": "Questions 1–5",
        "answers": ["carnivorous", "scent", "pouch", "fossil", "habitat", "TRUE", "FALSE", "NOT GIVEN", "FALSE", "NOT GIVEN", "FALSE", "TRUE", "NOT GIVEN"],
    },
    "c17-test3-p2": {
        "source": "剑桥雅思17 · Test 3 · Passage 2",
        "title": "Palm oil",
        "file": "test3.txt",
        "start": "Palm oil",
        "end": "Questions 14–20",
        "answers": ["F", "G", "A", "H", "B", "E", "C", "B", "C", "solid", "(Sumatran) orangutan / orang-utan", "carbon stocks", "biodiversity"],
        "q_offset": 14,
    },
    "c17-test3-p3": {
        "source": "剑桥雅思17 · Test 3 · Passage 3",
        "title": "Building the Skyline: The Birth and Growth of Manhattan’s Skyscrapers",
        "file": "test3.txt",
        "start": "Building the Skyline",
        "end": "Questions 27–31",
        "answers": ["D", "B", "C", "D", "C", "NO", "YES", "NOT GIVEN", "NO", "H", "D", "I", "B", "F"],
        "q_offset": 27,
    },
    "c17-test4-p1": {
        "source": "剑桥雅思17 · Test 4 · Passage 1",
        "title": "Bats to the rescue",
        "file": "test4.txt",
        "start": "Bats to the rescue",
        "end": "Questions 1–6",
        "answers": ["FALSE", "FALSE", "NOT GIVEN", "TRUE", "NOT GIVEN", "TRUE", "droppings", "coffee", "mosquitoes", "protein", "unclean", "culture", "houses"],
    },
    "c17-test4-p2": {
        "source": "剑桥雅思17 · Test 4 · Passage 2",
        "title": "Does education fuel economic growth?",
        "file": "test4.txt",
        "start": "Does education fuel economic growth?",
        "end": "Questions 14–18",
        "answers": ["E", "A", "D", "F", "C", "descendants", "sermon", "fine", "innovation", "B", "E", "B", "D"],
        "q_offset": 14,
    },
    "c17-test4-p3": {
        "source": "剑桥雅思17 · Test 4 · Passage 3",
        "title": "The history of the tortoise",
        "file": "test4.txt",
        "start": "The history of the tortoise",
        "end": "Questions 27–32",
        "answers": ["D", "E", "F", "B", "H", "E", "FALSE", "NOT GIVEN", "NOT GIVEN", "TRUE", "memory", "numbers", "communication", "visual"],
        "q_offset": 27,
        "fallback_start": "Gareyev",
    },
}


def clean_text(text: str) -> str:
    text = text.replace("R E A D I N G P A S S A G E", "")
    text = re.sub(r"===== PAGE \d+ =====", " ", text)
    text = re.sub(r"\bp\. \d+\b", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_between(file: str, start: str, end: str, fallback_start: str | None = None) -> str:
    raw = (TMP / file).read_text(encoding="utf-8")
    s = raw.find(start)
    if s < 0 and fallback_start:
        s = raw.find(fallback_start)
    if s < 0:
        raise ValueError(f"start not found: {start}")
    e = raw.find(end, s)
    if e < 0:
        e = len(raw)
    body = raw[s:e]
    return clean_text(body)


def split_sentences(text: str):
    text = re.sub(r"^[A-H]\s+", "", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z‘'\"(])", text)
    return [p.strip() for p in parts if len(p.strip()) > 20]


def sentence_units(text: str):
    units = []
    for i, sent in enumerate(split_sentences(text), 1):
        units.append({
            "id": i,
            "para": max(1, 1 + (i - 1) // 6),
            "en": sent,
            "zh": "（待老师精修翻译）",
            "grammar": {
                "type": "待老师精修",
                "note": "本句来自 PDF/OCR 底稿，已入库用于练题；翻译、语法和短语将在逐篇精修阶段由雅思老师视角补齐。"
            },
            "words": []
        })
    return units


def question_groups(answers, q_offset=1):
    items = []
    for i, answer in enumerate(answers, q_offset):
        items.append({
            "number": i,
            "prompt": f"Question {i}（题干待老师精修；可先用于答案核对）",
            "answer": answer,
            "evidence_sentence": 1,
        })
    return [{
        "title": f"Questions {q_offset}-{q_offset + len(answers) - 1} · Draft question bank",
        "type": "draft_mixed",
        "instructions": ["题干将在精修阶段补齐；当前版本先提供标准答案核对。"],
        "items": items,
    }]


def make_passage(pid: str, info: dict):
    body = extract_between(info["file"], info["start"], info["end"], info.get("fallback_start"))
    return {
        "id": pid,
        "source": info["source"],
        "title": info["title"],
        "quality": "draft_raw",
        "analysis_unit": "sentence",
        "sentences": sentence_units(body),
        "questions": question_groups(info["answers"], info.get("q_offset", 1)),
    }


def write_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_index(passages):
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    rows = {p["id"]: p for p in idx.get("passages", [])}
    order = [p["id"] for p in idx.get("passages", [])]
    for p in passages:
        rows[p["id"]] = {
            "id": p["id"],
            "source": p["source"],
            "title": p["title"],
            "sentence_count": len(p["sentences"]),
            "question_count": sum(len(g["items"]) for g in p.get("questions", [])),
        }
        if p["id"] not in order:
            order.append(p["id"])
    idx["passages"] = [rows[i] for i in order if i in rows]
    write_json(INDEX, idx)


def main():
    PASSAGES.mkdir(parents=True, exist_ok=True)
    made = []
    for pid, info in BOOK.items():
        p = make_passage(pid, info)
        made.append(p)
        write_json(PASSAGES / f"{pid}.json", p)
        print(pid, len(p["sentences"]), "sentences", sum(len(g["items"]) for g in p["questions"]), "questions")
    update_index(made)


if __name__ == "__main__":
    main()
