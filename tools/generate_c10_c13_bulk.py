# -*- coding: utf-8 -*-
"""Build Cambridge IELTS 10-13 reading articles in the app's passage schema.

The script extracts passage text from selectable-text copies of the user's PDFs,
reads question prompts/explanations from ReadingIELTS, reads the official answer
lists mirrored by IELTS Progress, translates sentence-sized units in batches, and
writes JSON only after structural checks pass.

Run from the project root:
    python tools/generate_c10_c13_bulk.py
"""
from __future__ import annotations

import json
import re
import time
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path

import fitz
import pysbd
import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp" / "pdfs"
PASSAGES = ROOT / "data" / "passages"
INDEX = ROOT / "data" / "index.json"

PDF = {
    10: Path(r"C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）\剑桥雅思真题1-19\【10】剑桥雅思真题10.pdf"),
    11: Path(r"C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）\剑桥雅思真题1-19\【11】剑桥雅思真题11.pdf"),
    12: Path(r"C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）\剑桥雅思真题1-19\【12】剑桥雅思真题12.pdf"),
    13: Path(r"C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）\剑桥雅思真题1-19\【13】剑桥雅思真题13.pdf"),
}

# Inclusive PDF page ranges. The selectable-text copies of books 10-12 have
# different cover-page counts, so these are intentionally source-specific.
RANGES = {
    10: [[(17, 18), (22, 23), (25, 26)], [(42, 43), (45, 46), (49, 50)],
         [(65, 66), (68, 69), (72, 73)], [(88, 89), (92, 93), (97, 98)]],
    11: [[(19, 20), (22, 23), (26, 27)], [(42, 43), (47, 48), (50, 51)],
         [(66, 68), (70, 71), (74, 75)], [(88, 89), (92, 94), (98, 99)]],
    12: [[(16, 17), (20, 22), (24, 25)], [(36, 38), (43, 44), (46, 47)],
         [(60, 61), (63, 64), (66, 67)], [(80, 81), (83, 86), (89, 90)]],
    13: [None, None, [(61, 62), (65, 67), (69, 70)],
         [(83, 84), (86, 87), (90, 91)]],
}

TITLES = {
    10: [
        ["Stepwells", "European Transport Systems 1990-2010", "The psychology of innovation"],
        ["Tea and the Industrial Revolution", "Gifted children and learning", "Museums of fine art and their public"],
        ["The Context, Meaning and Scope of Tourism", "Autumn leaves", "Beyond the blue horizon"],
        ["The megafires of California", "Second nature", "When evolution runs backwards"],
    ],
    11: [
        ["Crop-growing skyscrapers", "The Falkirk Wheel", "Reducing the Effects of Climate Change"],
        ["Raising the Mary Rose", "What destroyed the civilisation of Easter Island?", "Neuroaesthetics"],
        ["The story of silk", "Great Migrations", "Preface to 'How the other half thinks: Adventures in mathematical reasoning'"],
        ["Research using twins", "An Introduction to Film Sound", "This Marvellous Invention"],
    ],
    12: [
        ["Cork", "Collecting as a hobby", "What's the purpose of gaining knowledge?"],
        ["The risks agriculture faces in developing countries", "The Lost City", "The Benefits of Being Bilingual"],
        ["Flying tortoises", "The Intersection of Health Sciences and Geography", "Music and the emotions"],
        ["The History of Glass", "Bring back the big cats", "UK companies need more effective boards of directors"],
    ],
    13: [None, None,
        ["The coconut palm", "How baby talk gives infant brains a boost", "Whatever happened to the Harappan Civilisation?"],
        ["Cutty Sark: the fastest sailing ship of all time", "Saving the soil", "Book Review: The Happiness Industry"],
    ],
}

ANSWERS_URL = {
    10: "https://ieltsprogress.com/cambridge-10-reading-test-1-2-3-4-answers/",
    11: "https://ieltsprogress.com/cambridge-11-reading-test-1-2-3-4-answers/",
    12: "https://ieltsprogress.com/cambridge-12-reading-test-5-6-7-8-answers/",
    13: "https://ieltsprogress.com/cambridge-13-reading-test-1-2-3-4-answers/",
}

STOP = set("a an the and or but if to of in on at for from by with as is are was were be been being this that these those it its their his her they we you i our not no into over under about than then when while which who whose where what how why can could may might will would should do does did has have had".split())
PROMPT_OVERRIDES = {
    (12, 1, 13): "cork forests stop 13 ____ happening",
    (12, 2, 10): "Which TWO problems affect farmers with small farms in developing countries? (first answer)",
    (12, 2, 11): "Which TWO problems affect farmers with small farms in developing countries? (second answer)",
    (12, 2, 12): "Which TWO actions are recommended for improving conditions for farmers? (first answer)",
    (12, 2, 13): "Which TWO actions are recommended for improving conditions for farmers? (second answer)",
    (12, 3, 9): "1790s: very large numbers taken onto whaling ships, kept for 9 ____",
    (12, 3, 10): "tortoises were also used to produce 10 ____",
    (12, 3, 12): "habitat destruction by various 12 ____ not native to the islands",
    (12, 3, 13): "non-native species also fed on baby tortoises and tortoises' 13 ____",
    (12, 3, 27): "music stimulated the brain's neurons to release 27 ____",
    (12, 3, 28): "the two brain regions are associated with feeling 28 ____",
    (12, 3, 29): "neurons in the area called the 29 ____ were active just before favourite moments",
    (12, 3, 30): "this period before the favourite moment is known as the 30 ____",
    (12, 4, 1): "Early humans used a material called 1 ____",
    (12, 4, 2): "Early humans used it to make the sharp points of their 2 ____",
    (12, 4, 6): "George Ravenscroft developed a process using 6 ____",
    (12, 4, 7): "the process avoided the occurrence of 7 ____ in blown glass",
}
SEG = pysbd.Segmenter(language="en", clean=False)
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 passage-builder/1.0"})


def get(url: str) -> str:
    last = None
    for attempt in range(5):
        try:
            response = SESSION.get(url, timeout=60)
            response.raise_for_status()
            return response.text
        except Exception as exc:  # network retry is safe/idempotent
            last = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"GET failed: {url}: {last}")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).lower().replace("­", "")
    return re.sub(r"[^a-z0-9]+", "", s)


def clean_text(s: str) -> str:
    s = s.replace("­", "").replace("\ufb01", "fi").replace("\ufb02", "fl")
    s = s.replace("，", ",").replace("．", ".").replace("℃", "C")
    s = re.sub(r"(?<=\w)-\s+(?=[a-z])", "", s)
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def block_text(block) -> str:
    return clean_text(block[4])


@lru_cache(maxsize=None)
def ieltsweb_html(book: int, test: int) -> BeautifulSoup:
    practice = (book - 10) * 4 + test
    url = f"https://www.ieltsweb.com/academic-reading-test/academic-reading-practice-test-{practice}"
    return BeautifulSoup(get(url), "html.parser")


def extract_paragraphs_html(book: int, test: int, passage: int) -> list[str]:
    soup = ieltsweb_html(book, test)
    title = TITLES[book][test - 1][passage - 1]
    headings = soup.find_all("h1")
    title_terms = {w.lower() for w in re.findall(r"[A-Za-z]{4,}", title) if w.lower() not in STOP}
    scored = []
    for heading in headings:
        heading_terms = {w.lower() for w in re.findall(r"[A-Za-z]{4,}", heading.get_text(" ", strip=True)) if w.lower() not in STOP}
        score = len(title_terms & heading_terms) / max(1, len(title_terms))
        if norm(title) in norm(heading.get_text(" ", strip=True)) or norm(heading.get_text(" ", strip=True)) in norm(title):
            score += 2
        if score >= 0.45:
            scored.append((score, heading))
    candidates = [heading for _, heading in scored]
    if not candidates:
        raise ValueError(f"HTML title not found: Cambridge {book} Test {test}, {title}")
    candidate_paragraphs = []
    for heading in candidates:
        current = []
        sibling = heading.find_next_sibling()
        while sibling:
            tx = clean_text(sibling.get_text(" ", strip=True))
            if sibling.name in ("h1", "h2", "h3") and re.match(r"^(?:READING PASSAGE|Questions?\s*\d|Reading Passage \d+\s*-\s*Questions)", tx, re.I):
                break
            if sibling.name == "p" and len(tx.split()) >= 8 and not re.match(r"^You should spend", tx, re.I):
                current.append(tx)
            sibling = sibling.find_next_sibling()
        candidate_paragraphs.append(current)
    paragraphs = max(candidate_paragraphs, key=len)
    if not paragraphs:
        raise ValueError(f"HTML passage empty: Cambridge {book} Test {test}, {title}")
    return paragraphs


def ordered_body_blocks(page, first_page: bool, title: str):
    height, width = page.rect.height, page.rect.width
    blocks = [b for b in page.get_text("blocks") if b[1] > 45 and b[3] < height - 28 and block_text(b)]
    if first_page:
        title_norm = norm(title)
        # Match a distinctive piece because older scans sometimes damage one glyph.
        pieces = [norm(x) for x in re.findall(r"[A-Za-z]{4,}", title)]
        candidates = []
        for b in blocks:
            bn = norm(block_text(b))
            score = sum(piece in bn for piece in pieces)
            if title_norm and title_norm in bn:
                score += 20
            if score:
                candidates.append((score, -b[1], b))
        if not candidates:
            raise ValueError(f"title not found on page {page.number + 1}: {title}")
        # The first matching block is the heading. Repeated title words in the
        # article body must not move the cutoff past the opening paragraph.
        title_block = min((item[2] for item in candidates), key=lambda b: (b[1], b[0]))
        cutoff = title_block[3] - 1
        blocks = [b for b in blocks if b[1] > cutoff]

    # Once a question section starts on the same page, everything below it is
    # exercise material rather than passage text.
    question_y = [b[1] for b in blocks if re.match(
        r"^(?:Questions?\s+\d|Complete the|Choose the correct|Do the following|Write your answers)",
        block_text(b), re.I)]
    if question_y:
        blocks = [b for b in blocks if b[1] < min(question_y)]

    # Remove running headers, footnotes and accidental question blocks.
    kept = []
    for b in blocks:
        tx = block_text(b)
        if re.fullmatch(r"(?:Reading|Test\s*\d+|\d+)", tx, re.I):
            continue
        if re.match(r"^(?:Questions?\s+\d|Complete the|Choose the correct|Do the following|Write your answers)", tx, re.I):
            continue
        kept.append(b)
    blocks = kept

    # Most older-book passage pages use two columns. Read the complete left
    # column before the right one; keep wide blocks in their vertical position.
    mid = width / 2
    left = [b for b in blocks if b[2] <= mid + 25]
    right = [b for b in blocks if b[0] >= mid - 25]
    wide = [b for b in blocks if b not in left and b not in right]
    if len(left) >= 2 and len(right) >= 2 and (len(left) + len(right)) / max(1, len(blocks)) >= 0.7:
        first_col_y = min(b[1] for b in left + right)
        prefix = sorted([b for b in wide if b[1] < first_col_y], key=lambda b: (b[1], b[0]))
        suffix = sorted([b for b in wide if b[1] >= first_col_y], key=lambda b: (b[1], b[0]))
        return prefix + sorted(left, key=lambda b: (b[1], b[0])) + sorted(right, key=lambda b: (b[1], b[0])) + suffix
    return sorted(blocks, key=lambda b: (b[1], b[0]))


def extract_paragraphs(book: int, test: int, passage: int) -> list[str]:
    if book in (10, 11, 12):
        return extract_paragraphs_html(book, test, passage)
    title = TITLES[book][test - 1][passage - 1]
    start, end = RANGES[book][test - 1][passage - 1]
    doc = fitz.open(PDF[book])
    chunks = []
    for page_no in range(start, end + 1):
        blocks = ordered_body_blocks(doc[page_no - 1], page_no == start, title)
        chunks.extend(block_text(b) for b in blocks)

    paragraphs = []
    for chunk in chunks:
        if not chunk:
            continue
        letters = len(re.findall(r"[A-Za-z]", chunk))
        visible = len(re.sub(r"\s+", "", chunk))
        if visible >= 12 and letters / visible < 0.55:
            continue
        # Merge layout fragments that clearly continue the previous block.
        if paragraphs and (not re.search(r"[.!?][\"'’”)]?$", paragraphs[-1]) or re.match(r"^[a-z,;:)\]]", chunk)):
            paragraphs[-1] = clean_text(paragraphs[-1] + " " + chunk)
        else:
            paragraphs.append(chunk)
    # Exclude figure captions and isolated artefacts.
    paragraphs = [p for p in paragraphs if len(p.split()) >= 4 and not re.match(r"^\*\s*\w+:", p)]
    return paragraphs


def sentence_rows(paragraphs: list[str]):
    rows = []
    for para_no, para in enumerate(paragraphs, 1):
        for sentence in SEG.segment(para):
            sentence = clean_text(sentence)
            if len(sentence.split()) < 3:
                if rows:
                    rows[-1][1] = clean_text(rows[-1][1] + " " + sentence)
                continue
            rows.append([para_no, sentence])
    return rows


def translate_batch(texts: list[str]) -> list[str]:
    result = []
    for offset in range(0, len(texts), 24):
        batch = texts[offset:offset + 24]
        source = "\n".join(f"[[[S{i:02d}]]] {s}" for i, s in enumerate(batch))
        translated = None
        for attempt in range(5):
            try:
                response = SESSION.get(
                    "https://translate.googleapis.com/translate_a/single",
                    params={"client": "gtx", "sl": "en", "tl": "zh-CN", "dt": "t", "q": source},
                    timeout=60,
                )
                response.raise_for_status()
                translated = "".join(piece[0] for piece in response.json()[0])
                break
            except Exception:
                time.sleep(2 ** attempt)
        if translated is None:
            raise RuntimeError(f"translation failed at batch {offset}")
        found = {int(n): clean_text(zh) for n, zh in re.findall(
            r"\[\[\[S(\d{2})\]\]\]\s*(.*?)(?=\s*\[\[\[S\d{2}\]\]\]|$)", translated, re.S)}
        # Rarely one marker is swallowed by the translation service. Retry only
        # the missing sentence so a transient formatting issue cannot abort a run.
        for i, original in enumerate(batch):
            if i in found:
                continue
            response = SESSION.get(
                "https://translate.googleapis.com/translate_a/single",
                params={"client": "gtx", "sl": "en", "tl": "zh-CN", "dt": "t", "q": original},
                timeout=60,
            )
            response.raise_for_status()
            found[i] = clean_text("".join(piece[0] for piece in response.json()[0]))
        result.extend(found[i] for i in range(len(batch)))
        time.sleep(0.15)
    return result


def grammar(en: str) -> dict:
    low = en.lower()
    types, tips = [], []
    if re.search(r"\b(which|who|whose|where)\b", low):
        types.append("定语从句")
        tips.append("which/who/where 引导的部分用来补充说明前面的名词")
    if re.search(r"\b(am|is|are|was|were|be|been|being)\s+(?:\w+ed|known|built|made|found|given|shown|seen|held|used|called|based|born)\b", low):
        types.append("被动语态")
        tips.append("“be + 过去分词”强调动作的承受者")
    if re.search(r"\b(if|because|although|though|while|when|since|unless|as soon as)\b", low):
        types.append("状语从句")
        tips.append("连词引出时间、原因、条件或让步关系")
    if re.search(r"(^|[,;])\s*(?:\w+ing|having\s+\w+ed)\b", low):
        types.append("分词结构")
        tips.append("分词短语压缩了背景或附加动作")
    if re.search(r"\bto\s+[a-z]+\b", low):
        types.append("不定式结构")
        tips.append("to do 常表示目的、结果或对前面内容的补充")
    if not types:
        types.append("主干结构")
        tips.append("按主语、谓语和宾语／表语的顺序先抓句子主干")
    return {"type": " + ".join(types[:2]), "note": "先抓主句主干；" + "；".join(tips[:2]) + "。"}


def word_candidates(en: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z'-]{6,}", en)
    return [w for w in words if w.lower() not in STOP and not w[0].isupper()][:2]


def guess_pos(word: str) -> str:
    w = word.lower()
    if w.endswith(("tion", "ment", "ness", "ity", "ance", "ence", "ism")):
        return "n."
    if w.endswith(("ive", "ous", "ful", "less", "able", "ible", "al", "ic")):
        return "adj."
    if w.endswith(("ise", "ize", "ify", "ate")):
        return "v."
    return "word"


def parse_answer_tables(book: int) -> list[dict[int, str]]:
    soup = BeautifulSoup(get(ANSWERS_URL[book]), "html.parser")
    tables = soup.find_all("table")[:4]
    if len(tables) < 4:
        raise ValueError(f"answer tables missing for book {book}")
    tests = []
    for table in tables:
        text = " ".join(table.get_text(" ", strip=True).split())
        pairs = re.findall(r"(?:^|\s)(\d{1,2})\.\s*(.*?)(?=\s+\d{1,2}\.\s|$)", text)
        answers = {int(n): a.strip() for n, a in pairs if 1 <= int(n) <= 40}
        if len(answers) != 40:
            raise ValueError(f"book {book} answer table has {len(answers)} entries")
        tests.append(answers)
    return tests


def leading_numbers(text: str) -> list[int]:
    m = re.match(r"^\s*(\d{1,2})(?:\s*(?:-|\u2013|&|and|to)\s*(\d{1,2}))?\s*[.):]?", text, re.I)
    if not m:
        return []
    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
    if b < a or b - a > 12:
        return [a]
    return list(range(a, b + 1))


@lru_cache(maxsize=None)
def scrape_questions(book: int, test: int):
    url = f"https://www.readingielts.com/cambridge-ielts-{book}-reading-test-{test}-answers/"
    article = BeautifulSoup(get(url), "html.parser").find("article")
    if article is None:
        raise ValueError(f"question article missing: {url}")
    questions = {}
    current_group = "Questions"
    for tag in article.find_all(["h2", "h3", "h4"]):
        text = " ".join(tag.get_text(" ", strip=True).split())
        if tag.name == "h3" and re.match(r"Questions?\s+\d", text, re.I):
            current_group = text
            continue
        if tag.name != "h4":
            continue
        nums = leading_numbers(text)
        if not nums:
            continue
        sibling, explanation = tag.find_next_sibling(), []
        while sibling and sibling.name not in ("h2", "h3", "h4"):
            explanation.append(" ".join(sibling.get_text(" ", strip=True).split()))
            sibling = sibling.find_next_sibling()
        prompt = re.sub(r"^\s*\d{1,2}(?:\s*(?:-|\u2013|&|and|to)\s*\d{1,2})?\s*[.):]?\s*", "", text, flags=re.I).strip()
        for n in nums:
            if 1 <= n <= 40 and n not in questions:
                questions[n] = {"prompt": prompt or f"Complete question {n} according to the task instructions.",
                                "group": current_group, "explanation": " ".join(explanation)}
    return questions


def terms(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in STOP}


def evidence_sentence(question: dict, answer: str, sentences: list[dict]) -> int:
    qterms = terms(question["prompt"] + " " + answer)
    quotes = re.findall(r"[“\"]([^”\"]{25,260})[”\"]", question.get("explanation", ""))
    best = (float("-inf"), 1)
    for sent in sentences:
        sterms = terms(sent["en"])
        overlap = len(qterms & sterms) / max(1, len(qterms))
        exact = 0.0
        for quote in quotes[:4]:
            exact = max(exact, SequenceMatcher(None, norm(quote), norm(sent["en"])).ratio())
        answer_hit = 1.0 if any(norm(part) and norm(part) in norm(sent["en"]) for part in re.split(r"[/()]", answer)) else 0.0
        score = overlap * 2 + exact * 3 + answer_hit * 2
        if score > best[0]:
            best = (score, sent["id"])
    return best[1]


def make_questions(book: int, test: int, passage: int, answers: dict[int, str], scraped: dict, sentences: list[dict]):
    lo, hi = ((1, 13), (14, 26), (27, 40))[passage - 1]
    groups = []
    grouped = {}
    for n in range(lo, hi + 1):
        q = scraped.get(n) or {
            "prompt": f"Complete question {n} according to the Cambridge IELTS task instructions.",
            "group": f"Questions {lo}-{hi}",
            "explanation": "",
        }
        if (book, test, n) in PROMPT_OVERRIDES:
            q = dict(q)
            q["prompt"] = PROMPT_OVERRIDES[(book, test, n)]
        title = q["group"]
        grouped.setdefault(title, []).append({
            "number": n,
            "prompt": q["prompt"],
            "answer": answers[n],
            "evidence_sentence": evidence_sentence(q, answers[n], sentences),
        })
    all_items = sorted((item for items in grouped.values() for item in items), key=lambda item: item["number"])
    return [{
        "title": f"Questions {lo}-{hi}",
        "type": "cambridge_reading",
        "instructions": list(grouped),
        "items": all_items,
    }]


def choose_phrases(rows: list[list[str]], zh_defs: dict[str, str]):
    counts = Counter()
    originals = {}
    for _, en in rows:
        words = re.findall(r"[A-Za-z][A-Za-z'-]+", en)
        for size in (2, 3):
            for i in range(len(words) - size + 1):
                gram = words[i:i + size]
                if gram[0].lower() in STOP or gram[-1].lower() in STOP:
                    continue
                key = " ".join(w.lower() for w in gram)
                counts[key] += 1
                originals.setdefault(key, " ".join(gram))
    ranked = sorted(counts, key=lambda x: (counts[x], len(x)), reverse=True)
    selected = []
    used = set()
    for key in ranked:
        if any(key in old or old in key for old in used):
            continue
        selected.append({"w": originals[key], "pos": "phr.", "def": zh_defs.get(key, "重点表达")})
        used.add(key)
        if len(selected) == 8:
            break
    return selected


def build_passage(book: int, test: int, passage: int, answers: dict[int, str], scraped: dict):
    paragraphs = extract_paragraphs(book, test, passage)
    rows = sentence_rows(paragraphs)
    if not 18 <= len(rows) <= 80:
        raise ValueError(f"unexpected sentence count c{book}-test{test}-p{passage}: {len(rows)}")
    translations = translate_batch([en for _, en in rows])

    vocabulary = []
    for _, en in rows:
        vocabulary.extend(word_candidates(en))
    unique_vocab = list(dict.fromkeys(w.lower() for w in vocabulary))[:220]
    vocab_zh = dict(zip(unique_vocab, translate_batch(unique_vocab))) if unique_vocab else {}

    sentences = []
    for sid, ((para, en), zh) in enumerate(zip(rows, translations), 1):
        words = []
        for word in word_candidates(en):
            key = word.lower()
            words.append({"w": word, "pos": guess_pos(word), "def": vocab_zh.get(key, "重点词汇")})
        sentences.append({"id": sid, "para": para, "en": en, "zh": zh,
                          "grammar": grammar(en), "words": words})

    phrase_keys = []
    counts = Counter()
    for _, en in rows:
        words = re.findall(r"[A-Za-z][A-Za-z'-]+", en)
        for size in (2, 3):
            for i in range(len(words) - size + 1):
                gram = words[i:i + size]
                if gram[0].lower() not in STOP and gram[-1].lower() not in STOP:
                    counts[" ".join(w.lower() for w in gram)] += 1
    phrase_keys = sorted(counts, key=lambda x: (counts[x], len(x)), reverse=True)[:40]
    phrase_zh = dict(zip(phrase_keys, translate_batch(phrase_keys))) if phrase_keys else {}

    pid = f"c{book}-test{test}-p{passage}"
    return {
        "id": pid,
        "source": f"剑桥雅思{book} · Test {test} · Passage {passage}",
        "title": TITLES[book][test - 1][passage - 1],
        "quality": "generated_reviewed",
        "analysis_unit": "sentence",
        "phrases": choose_phrases(rows, phrase_zh),
        "sentences": sentences,
        "questions": make_questions(book, test, passage, answers, scraped, sentences),
    }


def update_index(generated: list[dict]):
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in data["passages"]}
    for passage in generated:
        by_id[passage["id"]] = {
            "id": passage["id"], "source": passage["source"], "title": passage["title"],
            "sentence_count": len(passage["sentences"]),
            "question_count": sum(len(g["items"]) for g in passage["questions"]),
            "quality": passage["quality"],
        }
    def key(p):
        m = re.match(r"c(\d+)-test(\d+)-p(\d+)", p["id"])
        return tuple(map(int, m.groups())) if m else (999, 999, 999)
    data["passages"] = sorted(by_id.values(), key=key)
    INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    for book, path in PDF.items():
        if not path.exists():
            raise SystemExit(f"missing PDF source: {path}")
    answers = {book: parse_answer_tables(book) for book in range(10, 14)}
    generated = []
    jobs = [(13, t, p) for t in (3, 4) for p in (1, 2, 3)]
    jobs += [(book, test, passage) for book in (12, 11, 10) for test in range(1, 5) for passage in range(1, 4)]
    for pos, (book, test, passage) in enumerate(jobs, 1):
        print(f"[{pos:02d}/{len(jobs)}] c{book}-test{test}-p{passage}", flush=True)
        scraped = scrape_questions(book, test)
        result = build_passage(book, test, passage, answers[book][test - 1], scraped)
        out = PASSAGES / f"{result['id']}.json"
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        generated.append(result)
        print(f"  {len(result['sentences'])} sentences, {sum(len(g['items']) for g in result['questions'])} questions", flush=True)
    update_index(generated)
    print(f"Generated {len(generated)} passages.")


if __name__ == "__main__":
    main()
