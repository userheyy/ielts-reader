# -*- coding: utf-8 -*-
"""Generate Cambridge IELTS 2-8 listening data from the official books.

The old books use several incompatible PDF layouts, so this importer keeps a
small per-book page map while sharing question, answer, transcript and audio
normalisation logic.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT.parent / "雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）"
PDF_DIR = PACK / "剑桥雅思真题1-19"
AUDIO_ROOT = PACK / "剑桥雅思真题音频1-19"
DATA_DIR = ROOT / "data" / "listening"
AUDIO_DIR = ROOT / "media" / "audio"

CONFIG = {
    2: {
        "pdf": "【2】剑桥雅思真题2.pdf",
        "question_starts": [2, 14, 25, 36],
        "transcript_pages": (61, 70),
        "answer_pages": [71, 72, 73, 74],
        "sort_text": False,
    },
    3: {
        "pdf": "【3】剑桥雅思真题3.pdf",
        "question_starts": [12, 34, 58, 80],
        "transcript_pages": (131, 152),
        "answer_pages": [153, 155, 157, 159],
        "sort_text": True,
    },
    4: {
        "pdf": "【4】剑桥雅思真题4.pdf",
        "question_starts": [11, 35, 58, 82],
        "transcript_pages": (131, 152),
        "answer_pages": [153, 155, 157, 159],
        "sort_text": True,
    },
    5: {
        "pdf": "【5】剑桥雅思真题5.pdf",
        "question_starts": [11, 33, 56, 79],
        "transcript_pages": (129, 152),
        "answer_pages": [153, 155, 157, 159],
        "sort_text": True,
    },
    6: {
        "pdf": "【6】剑桥雅思真题6.pdf",
        "question_starts": [11, 34, 56, 79],
        "transcript_pages": (128, 151),
        "answer_pages": [152, 154, 156, 158],
        "sort_text": True,
    },
    7: {
        "pdf": "【7】剑桥雅思真题7.pdf",
        "question_starts": [15, 38, 61, 86],
        "transcript_pages": (134, 156),
        "answer_pages": [157, 159, 161, 163],
        "sort_text": True,
    },
    8: {
        "pdf": "【8】剑桥雅思真题8.pdf",
        "question_starts": [9, 32, 55, 80],
        "transcript_pages": (129, 150),
        "answer_pages": [151, 153, 155, 157],
        "sort_text": True,
    },
}

SECTION_RE = re.compile(r"(?:\bS|~)\s*E\s*C\s*T(?:\s*I)?\s*O\s*N\s*([1-4I])\b", re.I)
READING_RE = re.compile(r"\bREAD\s*I\s*NG\s+(?:PASSAGE\s*[I1]|READ\s*I\s*NG\s+PASSAGE)", re.I)
QMARK_RE = re.compile(r"\bQ\s*([0-9IlJSO](?:\s*[0-9IlJSO]){0,2})\b", re.I)

ANSWER_OVERRIDES = {
    # Cambridge 4 Test 3 places answers 21-22 at the foot of the left PDF
    # column even though their Section 3 heading is in the right column.
    (4, 3): {21: "A", 22: "B", 23: "C", 24: "A", 25: "B", 26: "A",
             27: "C", 28: "B", 29: "B", 30: "B"},
}

# Cambridge 2 uses a landscape, multi-column text layer with several answers
# represented only as vector artwork.  These values are transcribed from its
# official answer-key pages; grouped choices retain all accepted orders.
C2_ANSWERS = {
    1: [
        "Black", "2085", "9456 1309", "2020BD", "July", "B", "D", "F",
        "$25 / twenty-five dollars", "next week / in a week / one week / the following week",
        "route book", "900 miles / nine hundred miles", "North Africa", "A", "C", "B", "C", "E", "B", "D",
        "Friday", "Biology", "57 books / fifty-seven books", "43 books / forty-three books", "Wednesday",
        "records lectures / uses a tape recorder", "skimming", "The French Revolution", "Why study history?",
        "animal language", "four-month certificate course", "current employment / job", "one-year diploma",
        "none / no prior qualifications", "six-month certificate course", "C", "F", "B", "G", "D",
    ],
    2: [
        "B", "A", "fridge / refrigerator", "stereo system", "books", "$184 / 184 dollars", "Murray", "16C",
        "South Hills", "English / British", "B", "north", "second floor", "room number", "8 pm and 7 am",
        "fire doors / emergency doors", "laundry / washing", "balconies", "meal times", "elected floor seniors",
        "newspapers", "maps", "radios", "television / TV", "computers", "B", "B", "C", "A", "B", "A",
        "training", "technology", "cool and wet", "wool and timber", "fertile soil / fertile land",
        "high quality vegetables", "warm and wet", "800 / eight hundred", "B",
    ],
    3: [
        "B", "C", "A", "B", "A / E", "A / C", "C / E", "B", "C", "B",
        "A / C / E / G", "A / C / E / G", "A / C / E / G", "A / C / E / G", "B / E", "B / E",
        "C", "A", "A", "B", "21 May", "18,000-20,000", "research methods", "draft plan", "conduct research",
        "March to May", "A", "A", "C", "B", "C", "B", "C", "B", "B", "C", "A", "B / D / E",
        "B / D / E", "B / D / E",
    ],
    4: [
        "16 Rose Lane", "27 June", "broken door / door broken", "C", "no locks", "bathroom light", "A",
        "kitchen curtains", "B", "1 pm and 5 pm", "B", "C", "waterfalls", "11 am", "Spotlight tour",
        "walking boots", "long trousers", "socks", "snakes", "plants", "B", "B", "A", "C", "C",
        "check your work / revise", "record", "a friend", "general interest", "dictionary", "B", "A", "A",
        "B", "C", "B", "A", "C", "B", "C",
    ],
}
for _test, _values in C2_ANSWERS.items():
    if len(_values) != 40:
        raise RuntimeError(f"Cambridge 2 Test {_test} answer count is {len(_values)}")
    ANSWER_OVERRIDES[(2, _test)] = {i + 1: value for i, value in enumerate(_values)}

QUESTION_SOURCE_OVERRIDES = {
    # The supplied Cambridge 2 PDF/DOCX both omit this original question page.
    # Keep the Part present and visibly flag the source gap instead of silently
    # dropping Questions 31-40 or inventing question wording.
    (2, 2, 4): (
        "SECTION 4\nQuestions 31-40\n"
        "The original Cambridge IELTS 2 Test 2 Section 4 question page is missing "
        "from the supplied PDF and DOCX. Official answers and the complete official "
        "tapescript are included in this Part."
    ),
}

INCOMPLETE_AUDIO_IDS = {
    "c2-test3-l4",
    "c2-test4-l1",
    "c2-test4-l2",
    "c2-test4-l3",
    "c2-test4-l4",
}


def page_text(doc, page_num, sort_text):
    try:
        return doc[page_num - 1].get_text("text", sort=sort_text)
    except Exception as exc:
        raise ValueError(f"failed to extract PDF page {page_num}: {exc}") from exc


def pages_text(doc, start, end, sort_text):
    return "\n".join(page_text(doc, p, sort_text) for p in range(start, end + 1))


def section_number(value):
    return 1 if value.upper() == "I" else int(value)


def split_sections(text):
    matches = list(SECTION_RE.finditer(text))
    result = {}
    for i, match in enumerate(matches):
        part = section_number(match.group(1))
        if part in result:
            continue
        stop = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        result[part] = text[match.start():stop]
    return result


def clean_question_text(text):
    output = []
    for raw in text.replace("\x85", " ").splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line or re.fullmatch(r"\d{1,3}", line):
            continue
        if re.fullmatch(r"(?:Listening|Test\s*[1-4])", line, re.I):
            continue
        output.append(line)
    return "\n".join(output)


def question_sections(doc, book, test):
    cfg = CONFIG[book]
    start = cfg["question_starts"][test - 1]
    chunks = []
    for page_num in range(start, min(start + 10, doc.page_count + 1)):
        text = page_text(doc, page_num, cfg["sort_text"])
        reading = READING_RE.search(text)
        if reading:
            text = text[:reading.start()]
            if text.strip():
                chunks.append(text)
            break
        chunks.append(text)
    sections = split_sections("\n".join(chunks))
    for (override_book, override_test, part), source in QUESTION_SOURCE_OVERRIDES.items():
        if override_book == book and override_test == test and part not in sections:
            sections[part] = source
    if set(sections) != {1, 2, 3, 4}:
        raise ValueError(f"c{book} test{test}: question sections {sorted(sections)}")
    return {part: clean_question_text(text) for part, text in sections.items()}


def prompt_for_number(source, number):
    lines = source.splitlines()
    patterns = [
        re.compile(rf"^\(?{number}\)?(?:\s|\.|$)"),
        re.compile(rf".*\({number}\).*"),
    ]
    for pattern in patterns:
        for i, line in enumerate(lines):
            if not pattern.match(line):
                continue
            chunk = [line]
            for nxt in lines[i + 1:i + 8]:
                if re.match(r"^\d{1,2}(?:\s|$)", nxt) and not nxt.startswith(str(number)):
                    break
                if re.match(r"^(?:Questions|SECTION)\b", nxt, re.I):
                    break
                chunk.append(nxt)
            return " ".join(chunk)[:900]
    return f"Question {number}（请根据上方原书题目作答）"


def decode_qmark(raw):
    table = str.maketrans({"I": "1", "i": "1", "l": "1", "J": "1", "j": "1",
                           "S": "5", "s": "5", "O": "0", "o": "0"})
    value = re.sub(r"\s+", "", raw).translate(table)
    return int(value) if value.isdigit() and 1 <= int(value) <= 40 else None


def protect_qmarks(text):
    def repl(match):
        number = decode_qmark(match.group(1))
        return f" [[Q{number}]] " if number else " "
    return QMARK_RE.sub(repl, text)


def clean_transcript_lines(text):
    text = protect_qmarks(text.replace("\x85", " ").replace("", "'").replace("�", ""))
    text = re.sub(r"\b(?:Example|Repeat)\b", " ", text, flags=re.I)
    output = []
    for raw in text.splitlines():
        line = raw.rstrip()
        compact = re.sub(r"\s+", " ", line).strip()
        if not compact or re.fullmatch(r"\d{1,3}", compact):
            continue
        if re.fullmatch(r"(?:Tape ?scripts?|Audio Scripts?|Test\s*[1-4I]|SECTION\s*[1-4I]|Repeat|Example)", compact, re.I):
            continue
        output.append(line)
    return output


def split_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+(?=(?:\[\[Q\d+\]\]\s*)?[A-Z'\"“])", text) if p.strip()]


def parse_segments(section_text, part):
    lines = clean_transcript_lines(section_text)
    turns, current, buffer = [], "", []

    def flush():
        nonlocal buffer
        speech = re.sub(r"\s+", " ", " ".join(buffer)).strip()
        if speech:
            turns.append((current or "SPEAKER", speech))
        buffer = []

    colon_re = re.compile(r"^\s*([A-Za-z][A-Za-z0-9 .'-]{0,35})\s*:\s*(.*)$")
    spaced_re = re.compile(r"^\s*([A-Z][A-Z0-9 .'-]{1,30})\s{2,}(.+)$")
    label_re = re.compile(r"^[A-Z][A-Z0-9 .'-]{0,30}$")
    for raw in lines:
        match = colon_re.match(raw) or spaced_re.match(raw)
        if match:
            flush()
            current = re.sub(r"\s+", " ", match.group(1)).strip()
            speech = match.group(2).strip()
            if speech:
                buffer.append(speech)
            continue
        compact = re.sub(r"\s+", " ", raw).strip()
        if label_re.fullmatch(compact) and len(compact.split()) <= 4:
            flush()
            current = compact
            continue
        buffer.append(compact)
    flush()

    raw_units = turns if part in (1, 3) else [
        (speaker, sentence) for speaker, speech in turns for sentence in split_sentences(speech)
    ]
    result = []
    for speaker, speech in raw_units:
        markers = sorted({int(n) for n in re.findall(r"\[\[Q(\d+)\]\]", speech)})
        speech = re.sub(r"\s*\[\[Q\d+\]\]\s*", " ", speech)
        speech = re.sub(r"\s+", " ", speech).strip()
        if not speech:
            continue
        result.append({"id": len(result) + 1, "start": None, "speaker": speaker.upper(),
                       "en": speech, "zh": "", "words": [], "answers": markers})
    return result


def transcript_sections(doc, book):
    cfg = CONFIG[book]
    text = pages_text(doc, *cfg["transcript_pages"], cfg["sort_text"])
    starts = [m for m in SECTION_RE.finditer(text) if section_number(m.group(1)) == 1]
    if len(starts) != 4:
        raise ValueError(f"c{book}: expected 4 transcript starts, found {len(starts)}")
    result = {}
    for test in range(1, 5):
        begin = starts[test - 1].start()
        end = starts[test].start() if test < 4 else len(text)
        sections = split_sections(text[begin:end])
        if set(sections) != {1, 2, 3, 4}:
            raise ValueError(f"c{book} test{test}: transcript sections {sorted(sections)}")
        result[test] = sections
    return result


def parse_num(token):
    value = token.strip().replace("l", "1").replace("I", "1")
    return int(value) if value.isdigit() else None


def clean_answer(raw):
    value = re.sub(r"\s+", " ", raw).strip(" .")
    value = re.sub(r"\b(?:IN (?:EITHER|ANY) ORDER|BOTH REQUIRED FOR ONE MARK|MUST STATE ALL THREE)\b", " ", value, flags=re.I)
    value = re.sub(r"\bNOT\b.*$", "", value, flags=re.I)
    value = re.sub(r"\bACCEPT\b", "/", value, flags=re.I)
    value = re.sub(r"\s+I\s+", " / ", value)
    value = value.replace("//", "/")
    value = re.sub(r"\s*/\s*", " / ", value)
    value = re.sub(r"\s+", " ", value).strip(" /.;")
    # Multiple-choice answer keys often append an explanation after the letter.
    mc = re.match(r"^([A-Ha-h])(?:\s*/\s*|\s+)(?:[A-Za-z(].*)$", value)
    if mc:
        return mc.group(1).upper()
    return value


def parse_answer_section(text, first, last):
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]
    entries = {}
    expected = first
    current_numbers = []
    current_body = []

    def flush():
        nonlocal current_numbers, current_body
        if not current_numbers:
            return
        answer = clean_answer(" ".join(current_body))
        for number in current_numbers:
            entries[number] = answer
        current_numbers, current_body = [], []

    pattern = re.compile(r"^([0-9Il]{1,2})(?:\s*(?:-|–|&|and)\s*([0-9Il]{1,2}))?\s*(.*)$", re.I)
    for line in lines:
        match = pattern.match(line)
        start = parse_num(match.group(1)) if match else None
        end = parse_num(match.group(2)) if match and match.group(2) else start
        if start == expected and end is not None and start <= end <= last:
            flush()
            current_numbers = list(range(start, end + 1))
            current_body = [match.group(3)] if match.group(3).strip() else []
            expected = end + 1
        elif current_numbers:
            current_body.append(line)
    flush()
    return entries


def answer_sections(doc, book, test):
    page_num = CONFIG[book]["answer_pages"][test - 1]
    page = doc[page_num - 1]
    width, height = page.rect.width, page.rect.height
    if book == 2:
        # Landscape page: Listening occupies the left half of a four-column page.
        left = page.get_text("text", clip=fitz.Rect(0, 0, width * 0.25, height), sort=True)
        right = page.get_text("text", clip=fitz.Rect(width * 0.25, 0, width * 0.5, height), sort=True)
    else:
        left = page.get_text("text", clip=fitz.Rect(0, 0, width * 0.5, height), sort=True)
        right = page.get_text("text", clip=fitz.Rect(width * 0.5, 0, width, height), sort=True)
    result = {}
    for part, column in ((1, left), (2, left), (3, right), (4, right)):
        matches = list(re.finditer(rf"Section\s*{part if part != 1 else '[1I]'}\s*,?\s*Questions", column, re.I))
        if not matches:
            continue
        start = matches[0].end()
        next_heading = re.search(r"Section\s*[1-4I]\s*,?\s*Questions|If you score", column[start:], re.I)
        stop = start + next_heading.start() if next_heading else len(column)
        first, last = (part - 1) * 10 + 1, part * 10
        result.update(parse_answer_section(column[start:stop], first, last))
    result.update(ANSWER_OVERRIDES.get((book, test), {}))
    return result


def evidence_for_answer(segments, answer):
    for choice in re.split(r"\s*/\s*", answer):
        core = re.sub(r"\([^)]*\)", "", choice)
        core = re.sub(r"[^A-Za-z0-9£$ ]", " ", core)
        core = re.sub(r"\s+", " ", core).strip().lower()
        if len(core) < 3 or re.fullmatch(r"[a-h]", core):
            continue
        for seg in segments:
            if core in seg["en"].lower():
                return seg["id"]
    return None


def build_part(book, test, part, source, transcript, answers):
    first, last = (part - 1) * 10 + 1, part * 10
    segments = parse_segments(transcript, part)
    for segment in segments:
        segment["answers"] = [n for n in segment["answers"] if first <= n <= last]
    items = []
    for number in range(first, last + 1):
        answer = answers.get(number, "")
        evidence = next((s["id"] for s in segments if number in s["answers"]), None)
        if evidence is None and answer:
            evidence = evidence_for_answer(segments, answer)
        if evidence is not None:
            target = next(s for s in segments if s["id"] == evidence)
            if number not in target["answers"]:
                target["answers"].append(number)
                target["answers"].sort()
        items.append({"number": number, "prompt": prompt_for_number(source, number),
                      "answer": answer, "evidence_segment": evidence, "paraphrase": None})
    pid = f"c{book}-test{test}-l{part}"
    result = {
        "id": pid,
        "source": f"剑桥雅思{book} · Test {test} · Part {part}",
        "title": f"Listening Part {part}",
        "audio": None if pid in INCOMPLETE_AUDIO_IDS else f"media/audio/c{book}-test{test}-part{part}.mp3",
        "practice_unit": (
            "speaker_turn"
            if part in (1, 3) and len({s.get("speaker") for s in segments if s.get("speaker")}) >= 2
            else "sentence"
        ),
        "segments": segments,
        "questions": [{"title": f"Questions {first}–{last}", "type": "mixed",
                       "instructions": ["Complete the original Cambridge IELTS listening questions below."],
                       "source_text": source, "items": items}],
    }
    if pid in INCOMPLETE_AUDIO_IDS:
        result["audio_issue"] = (
            "原始资料中的音频缺失或不完整，暂时不能进行播放和逐句跟读。"
        )
    return result


def update_index(generated):
    path = DATA_DIR / "index.json"
    index = json.loads(path.read_text(encoding="utf-8"))
    replaced = {f"c{book}-test" for book in generated}
    old = [t for t in index.get("tests", []) if not any(str(t.get("id", "")).startswith(p) for p in replaced)]
    new = []
    for book in sorted(generated):
        for test in range(1, 5):
            parts = []
            for part in range(1, 5):
                data = generated[book][(test, part)]
                first, last = (part - 1) * 10 + 1, part * 10
                parts.append({"id": data["id"], "part": part, "title": data["title"],
                              "question_range": f"{first}–{last}"})
            new.append({"id": f"c{book}-test{test}", "source": f"剑桥雅思{book} · Test {test}", "parts": parts})
    # Keep the library in numerical book order.
    combined = old + new
    combined.sort(key=lambda t: (int(re.match(r"c(\d+)", str(t.get("id", "c999"))).group(1)), str(t.get("id"))))
    index["tests"] = combined
    path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def track_number(path):
    match = re.search(r"第(\d+)期", path.name)
    return int(match.group(1)) if match else 0


def source_tracks(book, test, part):
    folder = AUDIO_ROOT / f"剑{book}"
    if book in (2, 3):
        return sorted(folder.glob(f"*Test{test}({part}-*.mp3"), key=track_number)
    if book in (4, 5):
        direct = folder / f"C{book}T{test}S{part}.mp3"
        return [direct] if direct.exists() else []
    if book == 6:
        direct = folder / f"Test{test}-s{part}.mp3"
        return [direct] if direct.exists() else []
    if book == 7:
        direct = folder / f"Test{test}.Section{part}.mp3"
        return [direct] if direct.exists() else []
    if book == 8:
        matches = [p for p in folder.glob(f"Test {test} Section*.mp3")
                   if re.search(rf"Section\s*{part}(?:\s|\.|$)", p.name, re.I)]
        return matches[:1]
    return []


def import_audio(books):
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    list_dir = ROOT / "tmp" / "c2-c5-audio-lists"
    list_dir.mkdir(parents=True, exist_ok=True)
    missing = []
    for book in books:
        for test in range(1, 5):
            for part in range(1, 5):
                tracks = source_tracks(book, test, part)
                if not tracks:
                    missing.append(f"c{book}-test{test}-part{part}")
                    print(f"audio missing: c{book}-test{test}-part{part}")
                    continue
                target = AUDIO_DIR / f"c{book}-test{test}-part{part}.mp3"
                listing = list_dir / f"c{book}-test{test}-part{part}.txt"
                listing.write_text("\n".join(f"file '{p.as_posix()}'" for p in tracks) + "\n", encoding="utf-8")
                subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
                                "-safe", "0", "-i", str(listing), "-ac", "1", "-b:a", "32k", str(target)], check=True)
                print(f"audio {target.name}: {len(tracks)} track(s)")
    return missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--books", default="2,3,4,5", help="comma-separated book numbers")
    parser.add_argument("--import-audio", action="store_true")
    args = parser.parse_args()
    books = sorted({int(x.strip().lstrip("cC")) for x in args.books.split(",") if x.strip()})
    if any(book not in CONFIG for book in books):
        raise SystemExit("This generator supports Cambridge IELTS 2-8 only")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    generated = {}
    for book in books:
        doc = fitz.open(PDF_DIR / CONFIG[book]["pdf"])
        transcripts = transcript_sections(doc, book)
        generated[book] = {}
        for test in range(1, 5):
            questions = question_sections(doc, book, test)
            answers = answer_sections(doc, book, test)
            missing_answers = [n for n in range(1, 41) if not answers.get(n)]
            if missing_answers:
                print(f"WARN c{book} test{test}: missing answers {missing_answers}")
            for part in range(1, 5):
                data = build_part(book, test, part, questions[part], transcripts[test][part], answers)
                (DATA_DIR / f"{data['id']}.json").write_text(
                    json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
                generated[book][(test, part)] = data
                print(f"{data['id']}: {len(data['segments'])} units / 10 questions")
        doc.close()
    update_index(generated)
    if args.import_audio:
        missing = import_audio(books)
        if missing:
            print("Missing source audio: " + ", ".join(missing))


if __name__ == "__main__":
    main()
