# -*- coding: utf-8 -*-
"""Build Cambridge IELTS 6-9 reading articles in the app passage schema.

The user's books 6-8 have usable text layers, while book 9 is image-only.  A
clean online practice rendering is therefore used as the common extraction
layer, with titles and answer keys checked against the local Cambridge PDFs.

Run from the project root:
    python tools/generate_c6_c9_bulk.py
"""
from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

from bs4 import BeautifulSoup
import torch
from transformers import MarianMTModel, MarianTokenizer


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "tools" / "generate_c10_c13_bulk.py"
SPEC = importlib.util.spec_from_file_location("cambridge_bulk_base", BASE_SCRIPT)
BASE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BASE)

BOOK_DIR = Path(
    r"C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）"
    r"\剑桥雅思真题1-19"
)
PDF = {
    book: next(BOOK_DIR.glob(f"【{book}】*.pdf"))
    for book in range(6, 10)
}

TITLES = {
    6: [
        ["Australia's Sporting Success", "Delivering the Goods", "Climate Change and the Inuit"],
        ["Advantages of Public Transport", "Greying Population Stays in the Pink", "Numeration"],
        ["The Lumiere Brothers", "Motivating Employees under Adverse Conditions", "The Search for the Anti-aging Pill"],
        ["Doctoring Sales", "Literate Women Make Better Mothers?", "Bullying"],
    ],
    7: [
        ["Let's Go Bats", "Making Every Drop Count", "Educating Psyche"],
        ["Why Pagodas Don't Fall Down", "The True Cost of Food", "Makete Integrated Rural Transport Project"],
        ["Ant Intelligence", "Population Movements and Genetics", "Europe's Forests"],
        ["Pulling Strings to Build Pyramids", "Endless Harvest", "Effects of Noise"],
    ],
    8: [
        ["A Chronicle of Timekeeping", "Air Traffic Control in the USA", "Telepathy"],
        ["Sheet Glass Manufacture: the Float Process", "The Little Ice Age", "The Meaning and Power of Smell"],
        ["Striking Back at Lightning with Lasers", "The Nature of Genius", "How Does the Biological Clock Tick?"],
        ["Land of the Rising Sun", "Biological Control of Pests", "Collecting Ant Specimens"],
    ],
    9: [
        ["William Henry Perkin", "Is There Anybody Out There?", "The History of the Tortoise"],
        ["The Impact of Hearing Loss on Young Children", "Venus in Transit", "A Neuroscientist Reveals How to Think Differently"],
        ["Attitudes to Language", "Tidal Power", "Information Theory - the Big Idea"],
        ["The Life and Work of Marie Curie", "Young Children's Sense of Identity", "The Development of Museums"],
    ],
}

BASE.TITLES.update(TITLES)
BASE.PDF.update(PDF)
BASE.ANSWERS_URL.update({
    book: f"https://ieltsprogress.com/cambridge-{book}-reading-test-1-2-3-4-answers/"
    for book in range(6, 10)
})

# Early editions occasionally contain fewer than 40 Academic Reading items.
EXPECTED_TOTALS = {(1, 3): 38, (1, 4): 39}


def clean(value: str) -> str:
    return BASE.clean_text(value.replace("\xa0", " "))


def number_range(value: str) -> list[int]:
    """Return all question numbers expressed by a group heading."""
    result: list[int] = []
    for first, last in re.findall(r"(\d{1,2})(?:\s*[–—-]\s*(\d{1,2}))?", value):
        start, end = int(first), int(last or first)
        if 1 <= start <= end <= 40:
            result.extend(range(start, end + 1))
    return sorted(set(result))


@lru_cache(maxsize=None)
def zone_test(book: int, test: int) -> dict:
    url = f"https://ieltszone.org/practice-tests/reading-test/ielts-{book}-reading-test-{test}-online-practice/"
    soup = BeautifulSoup(BASE.get(url), "html.parser")
    headings = [
        heading for heading in soup.find_all("h1")
        if re.fullmatch(r"READING PASSAGE\s*[123]", clean(heading.get_text(" ", strip=True)), re.I)
    ]
    if len(headings) != 3:
        raise ValueError(f"expected three IELTSZone passages: Cambridge {book} Test {test}")

    passages = {}
    for heading in headings:
        passage = int(re.search(r"([123])", heading.get_text()).group(1))
        # This is the smallest Elementor container holding one complete passage
        # (intro, article body and its question groups).
        box = list(heading.parents)[2]
        article_paragraphs: list[str] = []
        groups = []
        current = None
        for node in box.descendants:
            if getattr(node, "name", None) == "h2":
                heading_text = clean(node.get_text(" ", strip=True))
                if re.search(r"Questions?", heading_text, re.I):
                    numbers = number_range(heading_text)
                    if numbers:
                        current = {
                            "title": heading_text.lstrip("📝 "),
                            "numbers": numbers,
                            "parts": [],
                            "lines": [],
                        }
                        groups.append(current)
                    else:
                        current = None
                else:
                    current = "article"
                continue
            if getattr(node, "name", None) not in ("p", "li", "table"):
                continue
            # A table is captured once; its descendant paragraphs must not be
            # added a second time.
            if node.name in ("p", "li") and node.find_parent("table") is not None:
                continue
            value = clean(node.get_text(" ", strip=True))
            if not value:
                continue
            if current == "article" and len(value.split()) >= 5:
                article_paragraphs.append(value)
            elif isinstance(current, dict):
                current["parts"].append(value)
                current["lines"].extend(
                    clean(line) for line in node.get_text("\n", strip=True).splitlines() if clean(line)
                )

        for group in groups:
            group["body"] = clean(" ".join(group.pop("parts")))

        numbers = sorted({number for group in groups for number in group["numbers"]})
        if not article_paragraphs or not numbers:
            raise ValueError(f"incomplete IELTSZone passage: Cambridge {book} Test {test} Passage {passage}")
        passages[passage] = {"paragraphs": article_paragraphs, "groups": groups, "numbers": numbers}

    # A few legacy IELTSZone pages omit one question block even though the
    # passage and remaining blocks are complete. Passage boundaries are still
    # unambiguous from the first question number of the following passage.
    total_questions = EXPECTED_TOTALS.get((book, test), 40)
    if total_questions < 40:
        for passage_data in passages.values():
            trimmed_groups = []
            for group in passage_data["groups"]:
                group["numbers"] = [number for number in group["numbers"] if number <= total_questions]
                if group["numbers"]:
                    trimmed_groups.append(group)
            passage_data["groups"] = trimmed_groups
            passage_data["numbers"] = [
                number for number in passage_data["numbers"] if number <= total_questions
            ]

    upper_bounds = {
        1: min(passages[2]["numbers"]) - 1,
        2: min(passages[3]["numbers"]) - 1,
        3: total_questions,
    }
    lower_bounds = {1: 1, 2: upper_bounds[1] + 1, 3: upper_bounds[2] + 1}
    for passage in (1, 2, 3):
        expected = set(range(lower_bounds[passage], upper_bounds[passage] + 1))
        missing = sorted(expected - set(passages[passage]["numbers"]))
        if missing:
            title = f"Questions {missing[0]}-{missing[-1]}"
            passages[passage]["groups"].append({
                "title": title,
                "numbers": missing,
                "body": f"Refer to the original Cambridge task instructions for {title}.",
                "lines": [],
            })
            passages[passage]["numbers"] = sorted(set(passages[passage]["numbers"]) | set(missing))
    return passages


def extract_paragraphs(book: int, test: int, passage: int) -> list[str]:
    return zone_test(book, test)[passage]["paragraphs"]


def augment_questions(book: int, test: int) -> dict:
    questions = {}
    if book >= 6:
        try:
            questions = dict(BASE.scrape_questions(book, test))
        except (RuntimeError, ValueError):
            questions = {}
    for passage_data in zone_test(book, test).values():
        for group in passage_data["groups"]:
            missing = [
                number for number in group["numbers"]
                if number not in questions
                or questions[number]["prompt"].startswith("Complete question")
            ]
            if not missing:
                continue
            shared = group["body"] or group["title"]
            # Shared-answer sets (for example "Choose FIVE letters") do not
            # print the question number beside every blank. Preserve the full
            # task wording and identify the answer's position in that set.
            for position, number in enumerate(group["numbers"], 1):
                if number not in missing:
                    continue
                specific = ""
                for line in group.get("lines", []):
                    match = re.match(rf"^{number}\s*[.):]?\s*(.+)", line)
                    if match and len(match.group(1).split()) >= 2:
                        specific = match.group(1).strip()
                        break
                suffix = (
                    f" (answer {position} of {len(group['numbers'])})"
                    if len(group["numbers"]) > 1 and not specific else ""
                )
                questions[number] = {
                    "prompt": specific or shared + suffix,
                    "group": group["title"],
                    "explanation": "",
                }
    total = EXPECTED_TOTALS.get((book, test), 40)
    questions = {number: value for number, value in questions.items() if number <= total}
    missing = sorted(set(range(1, total + 1)) - set(questions))
    if missing:
        raise ValueError(f"question prompts missing for Cambridge {book} Test {test}: {missing}")
    return questions


def make_questions(book: int, test: int, passage: int, answers: dict[int, str], scraped: dict, sentences: list[dict]):
    passage_data = zone_test(book, test)[passage]
    numbers = passage_data["numbers"]
    grouped = {}
    for number in numbers:
        question = scraped[number]
        grouped.setdefault(question["group"], []).append({
            "number": number,
            "prompt": question["prompt"],
            "answer": answers[number],
            "evidence_sentence": BASE.evidence_sentence(question, answers[number], sentences),
        })
    lo, hi = min(numbers), max(numbers)
    items = sorted((item for values in grouped.values() for item in values), key=lambda item: item["number"])
    return [{
        "title": f"Questions {lo}-{hi}",
        "type": "cambridge_reading",
        "instructions": list(grouped),
        "items": items,
    }]


BASE.extract_paragraphs = extract_paragraphs
BASE.make_questions = make_questions


@lru_cache(maxsize=1)
def local_translator():
    model_name = "Helsinki-NLP/opus-mt-en-zh"
    tokenizer = MarianTokenizer.from_pretrained(model_name, local_files_only=True)
    model = MarianMTModel.from_pretrained(model_name, local_files_only=True)
    model.eval()
    return tokenizer, model


TRANSLATION_CACHE: dict[str, str] = {}


def translate_uncached(texts: list[str], batch_size: int = 96) -> list[str]:
    tokenizer, model = local_translator()
    output = []
    for offset in range(0, len(texts), batch_size):
        batch = texts[offset:offset + batch_size]
        encoded = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.inference_mode():
            generated = model.generate(**encoded, max_new_tokens=512, num_beams=1)
        translated = tokenizer.batch_decode(generated, skip_special_tokens=True)
        for value in translated:
            # Marian occasionally inserts spaces between adjacent CJK tokens.
            value = re.sub(r"(?<=[\u3400-\u9fff])\s+(?=[\u3400-\u9fff])", "", value)
            output.append(clean(value))
    return output


def translate_batch(texts: list[str]) -> list[str]:
    """Translate locally so a public endpoint rate limit cannot stop a batch."""
    missing = list(dict.fromkeys(text for text in texts if text not in TRANSLATION_CACHE))
    if missing:
        values = translate_uncached(missing)
        TRANSLATION_CACHE.update(zip(missing, values))
    return [TRANSLATION_CACHE[text] for text in texts]


BASE.translate_batch = translate_batch


def pretranslate(jobs: list[tuple[int, int, int]]) -> None:
    """Translate all repeated vocabulary and phrases once, grouped by length."""
    texts = set()
    for book, test, passage in jobs:
        rows = BASE.sentence_rows(extract_paragraphs(book, test, passage))
        texts.update(english for _, english in rows)

        vocabulary = []
        counts = Counter()
        for _, english in rows:
            vocabulary.extend(BASE.word_candidates(english))
            words = re.findall(r"[A-Za-z][A-Za-z'-]+", english)
            for size in (2, 3):
                for index in range(len(words) - size + 1):
                    gram = words[index:index + size]
                    if gram[0].lower() not in BASE.STOP and gram[-1].lower() not in BASE.STOP:
                        counts[" ".join(word.lower() for word in gram)] += 1
        texts.update(list(dict.fromkeys(word.lower() for word in vocabulary))[:220])
        texts.update(sorted(counts, key=lambda value: (counts[value], len(value)), reverse=True)[:40])

    ordered = sorted(
        (text for text in texts if text not in TRANSLATION_CACHE),
        key=lambda value: (len(value.split()), len(value)),
    )
    print(f"Pretranslating {len(ordered)} unique text units...", flush=True)
    for offset in range(0, len(ordered), 96):
        batch = ordered[offset:offset + 96]
        translated = translate_uncached(batch)
        TRANSLATION_CACHE.update(zip(batch, translated))
        if offset % 960 == 0 or offset + 96 >= len(ordered):
            print(f"  translated {min(offset + 96, len(ordered))}/{len(ordered)}", flush=True)


def parse_answers(book: int) -> list[dict[int, str]]:
    if book != 9:
        return BASE.parse_answer_tables(book)

    soup = BeautifulSoup(BASE.get(BASE.ANSWERS_URL[book]), "html.parser")
    answers = []
    for table in soup.find_all("table")[:4]:
        text = " ".join(table.get_text(" ", strip=True).split())
        pairs = re.findall(r"(?:^|\s)(\d{1,2})\.\s*(.*?)(?=\s+\d{1,2}\.\s|$)", text)
        answers.append({int(number): value.strip() for number, value in pairs if value.strip()})
    if len(answers) != 4:
        raise ValueError("Cambridge 9 answer tables are incomplete")
    answers[1].update({38: "A", 39: "B", 40: "C"})
    for test, values in enumerate(answers, 1):
        missing = sorted(set(range(1, 41)) - set(values))
        if missing:
            raise ValueError(f"answers missing for Cambridge 9 Test {test}: {missing}")
    return answers


def main() -> None:
    for book, path in PDF.items():
        if not path.exists():
            raise SystemExit(f"missing PDF source: {path}")

    answers = {book: parse_answers(book) for book in range(6, 10)}
    generated = []
    jobs = [
        (book, test, passage)
        for book in (9, 8, 7, 6)
        for test in range(1, 5)
        for passage in range(1, 4)
    ]
    pretranslate(jobs)
    for position, (book, test, passage) in enumerate(jobs, 1):
        print(f"[{position:02d}/{len(jobs)}] c{book}-test{test}-p{passage}", flush=True)
        scraped = augment_questions(book, test)
        result = BASE.build_passage(book, test, passage, answers[book][test - 1], scraped)
        output = BASE.PASSAGES / f"{result['id']}.json"
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        generated.append(result)
        question_count = sum(len(group["items"]) for group in result["questions"])
        print(f"  {len(result['sentences'])} sentences, {question_count} questions", flush=True)

    BASE.update_index(generated)
    print(f"Generated {len(generated)} passages.")


if __name__ == "__main__":
    main()
