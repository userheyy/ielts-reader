# -*- coding: utf-8 -*-
"""Build all Cambridge IELTS 1 Academic Reading articles."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "tools" / "generate_c2_c5_bulk.py"
SPEC = importlib.util.spec_from_file_location("cambridge_2_5_builder", BASE_SCRIPT)
BUILDER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BUILDER)

BOOK_DIR = Path(
    r"C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）"
    r"\剑桥雅思真题1-19"
)
PDF = next(BOOK_DIR.glob("【1】*.pdf"))
TITLES = [[
    "A Spark, a Flint: How Fire Leapt to Life",
    "Zoo Conservation Programmes",
    "Architecture - Reaching for the Sky",
], [
    "Right- and Left-handedness in Humans",
    "Migratory Beekeeping",
    "Tourism",
], [
    "Spoken Corpus Comes to Life",
    "Moles Happy as Homes Go Underground",
    "A Workaholic Economy",
], [
    "Glass: Capturing the Dance of Light",
    "Why Some Women Cross the Finish Line Ahead of Men",
    "Population Viability Analysis",
]]

BUILDER.BUILDER.BASE.TITLES[1] = TITLES
BUILDER.BUILDER.BASE.PDF[1] = PDF
BUILDER.BUILDER.BASE.ANSWERS_URL[1] = (
    "https://ieltsprogress.com/cambridge-1-reading-test-1-2-3-4-answers/"
)


def parse_answers() -> list[dict[int, str]]:
    soup = BeautifulSoup(
        BUILDER.BUILDER.BASE.get(BUILDER.BUILDER.BASE.ANSWERS_URL[1]),
        "html.parser",
    )
    expected = [40, 40, 38, 39]
    tests = []
    for test, (table, total) in enumerate(zip(soup.find_all("table")[:4], expected), 1):
        text = " ".join(table.get_text(" ", strip=True).split())
        pairs = re.findall(r"(?:^|\s)(\d{1,2})\.\s*(.*?)(?=\s+\d{1,2}\.\s|$)", text)
        answers = {
            int(number): answer.strip()
            for number, answer in pairs
            if answer.strip() and 1 <= int(number) <= total
        }
        missing = sorted(set(range(1, total + 1)) - set(answers))
        if missing:
            raise ValueError(f"answers missing for Cambridge 1 Test {test}: {missing}")
        tests.append(answers)
    return tests


def main() -> None:
    if not PDF.exists():
        raise SystemExit(f"missing PDF source: {PDF}")
    answers = parse_answers()
    jobs = [(1, test, passage) for test in range(1, 5) for passage in range(1, 4)]
    BUILDER.load_existing_translation_cache()
    print(
        f"Loaded {len(BUILDER.BUILDER.TRANSLATION_CACHE)} existing translations.",
        flush=True,
    )
    BUILDER.BUILDER.pretranslate(jobs)

    generated = []
    for position, (book, test, passage) in enumerate(jobs, 1):
        print(f"[{position:02d}/{len(jobs)}] c1-test{test}-p{passage}", flush=True)
        result = BUILDER.BUILDER.BASE.build_passage(
            book,
            test,
            passage,
            answers[test - 1],
            BUILDER.BUILDER.augment_questions(book, test),
        )
        output = BUILDER.BUILDER.BASE.PASSAGES / f"{result['id']}.json"
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        generated.append(result)
        question_count = sum(len(group["items"]) for group in result["questions"])
        print(f"  {len(result['sentences'])} sentences, {question_count} questions", flush=True)

    BUILDER.BUILDER.BASE.update_index(generated)
    print(f"Generated {len(generated)} passages.")


if __name__ == "__main__":
    main()
