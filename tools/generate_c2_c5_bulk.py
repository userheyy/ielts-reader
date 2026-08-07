# -*- coding: utf-8 -*-
"""Build Cambridge IELTS 2-5 reading articles in the app passage schema."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "tools" / "generate_c6_c9_bulk.py"
SPEC = importlib.util.spec_from_file_location("cambridge_6_9_builder", BASE_SCRIPT)
BUILDER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BUILDER)

BOOK_DIR = Path(
    r"C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）"
    r"\剑桥雅思真题1-19"
)
PDF = {book: next(BOOK_DIR.glob(f"【{book}】*.pdf")) for book in range(2, 6)}

TITLES = {
    2: [
        ["Airports on Water", "Changing Our Understanding of Health", "Children's Thinking"],
        ["Implementing the Cycle of Success: A Case Study", "Language", "What Is a Port City?"],
        ["Absenteeism in Nursing: A Longitudinal Study", "The Motor Car", "The Keyless Society"],
        ["Green Wave Washes over Mainstream Shopping", "Great Concern in Europe", "In Search of the Holy Grail"],
    ],
    3: [
        ["The Rocket - From East to West", "The Risks of Cigarette Smoke", "The Scientific Method"],
        ["A Remarkable Beetle", "Environmental Management", "The Concept of Role Theory"],
        ["The Department of Ethnography", "Secrets of the Forest", "Highs and Lows"],
        ["Air Pollution", "Votes for Women", "Measuring Organisational Performance"],
    ],
    4: [
        ["Tropical Rainforests", "What Do Whales Feel?", "Visual Symbols and the Blind"],
        ["Lost for Words", "Alternative Medicine in Australia", "Play Is a Serious Business"],
        ["Micro-enterprise Credit for Street Youth", "Obtaining Linguistic Data", "Volcanoes - Earth-shattering News"],
        ["How Much Higher? How Much Faster?", "The Nature and Aims of Archaeology", "The Problem of Scarce Resources"],
    ],
    5: [
        ["Johnson's Dictionary", "Nature or Nurture?", "The Truth about the Environment"],
        ["Bakelite - The Birth of Modern Plastics", "What's So Funny?", "The Birth of Scientific English"],
        ["Early Childhood Education", "Disappearing Delta", "The Return of Artificial Intelligence"],
        ["The Impact of Wilderness Tourism", "Flawed Beauty: the Problem with Toughened Glass", "The Effects of Light on Plant and Animal Species"],
    ],
}

BUILDER.BASE.TITLES.update(TITLES)
BUILDER.BASE.PDF.update(PDF)
BUILDER.BASE.ANSWERS_URL.update({
    book: f"https://ieltsprogress.com/cambridge-{book}-reading-test-1-2-3-4-answers/"
    for book in range(2, 6)
})


def questions_for_test(book: int, test: int) -> dict:
    questions = BUILDER.augment_questions(book, test)
    if (book, test) == (3, 2):
        overrides = {
            9: "Complete the beetle table: preferred climate of the Spanish species.",
            10: "Complete the beetle table: start of the active period for the Spanish species.",
            11: "Complete the beetle table: number of generations per year for the Spanish species.",
            12: "Complete the beetle table: preferred climate of the South African ball roller.",
            13: "Complete the beetle table: complementary species for the South African ball roller.",
        }
        for number, prompt in overrides.items():
            questions[number] = {
                "prompt": prompt,
                "group": "Questions 9-13",
                "explanation": "",
            }
    for question in questions.values():
        if len(question["prompt"]) > 900:
            shortened = question["prompt"][:880].rsplit(" ", 1)[0]
            question["prompt"] = shortened + " ..."
    return questions


def load_existing_translation_cache() -> None:
    """Reuse translations already stored in the current article library."""
    for path in BUILDER.BASE.PASSAGES.glob("c*-test*-p*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for sentence in data.get("sentences", []):
            if sentence.get("en") and sentence.get("zh"):
                BUILDER.TRANSLATION_CACHE.setdefault(sentence["en"], sentence["zh"])
            for word in sentence.get("words", []):
                if word.get("w") and word.get("def") and word["def"] != "重点词汇":
                    BUILDER.TRANSLATION_CACHE.setdefault(word["w"].lower(), word["def"])
        for phrase in data.get("phrases", []):
            if phrase.get("w") and phrase.get("def") and phrase["def"] != "重点表达":
                BUILDER.TRANSLATION_CACHE.setdefault(phrase["w"].lower(), phrase["def"])


def main() -> None:
    for book, path in PDF.items():
        if not path.exists():
            raise SystemExit(f"missing PDF source: {path}")

    answers = {book: BUILDER.BASE.parse_answer_tables(book) for book in range(2, 6)}
    jobs = [
        (book, test, passage)
        for book in (5, 4, 3, 2)
        for test in range(1, 5)
        for passage in range(1, 4)
    ]
    load_existing_translation_cache()
    print(f"Loaded {len(BUILDER.TRANSLATION_CACHE)} existing translations.", flush=True)
    BUILDER.pretranslate(jobs)

    generated = []
    for position, (book, test, passage) in enumerate(jobs, 1):
        print(f"[{position:02d}/{len(jobs)}] c{book}-test{test}-p{passage}", flush=True)
        result = BUILDER.BASE.build_passage(
            book,
            test,
            passage,
            answers[book][test - 1],
            questions_for_test(book, test),
        )
        output = BUILDER.BASE.PASSAGES / f"{result['id']}.json"
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        generated.append(result)
        question_count = sum(len(group["items"]) for group in result["questions"])
        print(f"  {len(result['sentences'])} sentences, {question_count} questions", flush=True)

    BUILDER.BASE.update_index(generated)
    print(f"Generated {len(generated)} passages.")


if __name__ == "__main__":
    main()
