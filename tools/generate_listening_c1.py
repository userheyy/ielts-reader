# -*- coding: utf-8 -*-
"""Generate Cambridge IELTS 1 listening JSON and normalized audio.

The four tests contain 41, 41, 42 and 42 questions. Source audio is split into
29 tracks; ``--import-audio`` joins them into the app's 16 standard Part files.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT.parent / "雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）"
PDF = PACK / "剑桥雅思真题1-19" / "【1】剑桥雅思真题1.pdf"
AUDIO_SOURCE = PACK / "剑桥雅思真题音频1-19" / "剑1"
DATA_DIR = ROOT / "data" / "listening"
AUDIO_DIR = ROOT / "media" / "audio"

TESTS = {
    1: {"question_pages": {1: (18, 19), 2: (20, 21), 3: (22, 23), 4: (24, 25)},
        "transcript_pages": (113, 118), "ranges": {1: (1, 10), 2: (11, 21), 3: (22, 31), 4: (32, 41)},
        "titles": {1: "Lost briefcase report", 2: "News headlines", 3: "Economics course orientation", 4: "Bachelor of Social Science orientation"}},
    2: {"question_pages": {1: (40, 40), 2: (41, 41), 3: (42, 43), 4: (44, 45)},
        "transcript_pages": (118, 124), "ranges": {1: (1, 10), 2: (11, 20), 3: (21, 32), 4: (33, 41)},
        "titles": {1: "Student accommodation", 2: "Choosing a bicycle", 3: "Banana growing in Australia", 4: "Vitamins and a balanced diet"}},
    3: {"question_pages": {1: (60, 61), 2: (62, 62), 3: (63, 63), 4: (64, 65)},
        "transcript_pages": (124, 130), "ranges": {1: (1, 12), 2: (13, 23), 3: (24, 32), 4: (33, 42)},
        "titles": {1: "Parking sticker application", 2: "Museum tour", 3: "The changing world of work", 4: "Space management in supermarkets"}},
    4: {"question_pages": {1: (81, 82), 2: (83, 83), 3: (84, 84), 4: (85, 85)},
        "transcript_pages": (129, 136), "ranges": {1: (1, 12), 2: (13, 21), 3: (22, 31), 4: (32, 42)},
        "titles": {1: "Students on campus", 2: "Student banking", 3: "Recycling aluminium cans", 4: "Sports Studies open day"}},
}

ANSWERS = {
    1: ["A", "C", "D", "D", "C", "Prescott", "41", "Fountain", "752239", "£65", "E", "F", "H", "$250 million", "roads / road system", "too late", "school children / boys", "3", "boats / pleasure craft", "pilot", "musical instruments", "A", "B", "C", "A", "talk / give a talk", "write up work", "can choose", "open book", "closed reserve", "vocational subjects / work / employment", "B", "C", "history and economics", "deadlines", "attendance", "B", "C", "B", "D", "A"],
    2: ["student accommodation / hostel", "awful food", "not friendly / kept to themselves", "lecturers too busy", "regular meetings / meetings with lecturers / fortnightly meetings", "family / homestay", "lot of noise / children made noise / difficult to study", "student house", "Bachelor of Computing", "reserve computer time", "mountain", "quality", "$2,000", "short / casual rides", "town riding / shopping", "serious touring", "similar / almost the same", "better quality components", "buying clothes", "frame", "B", "C", "D", "B", "one bunch", "15 months", "uphill / on hillsides", "lots of water / plenty of water", "plastic bags", "bananas / ones to ripen", "C", "D", "B", "D", "C", "cooking", "regular daily intake", "a variety", "the dark / the fridge / a cool place", "eat in moderation / not too much", "eat lots / eat most"],
    3: ["B", "D", "C", "A", "Richard Lee", "30 Enmore Road", "Newport", "Architecture", "LJX 058K", "Ford", "C", "front window / windscreen", "November 1991", "historic ships", "green arrows", "information desk", "stairs to climb / lots of stairs", "every hour", "Captain Cook", "the sea", "Australian artists / painters", "$70", "souvenirs", "B", "C", "D", "A", "law has changed / changes in law", "powerful computer programs", "from home computer", "hotels / hotel beds / rooms", "hire cars", "displays / products", "hidden TV cameras", "recorder / recording", "Spaceman", "position / shelf / spot / place", "walk past / ignore / pass", "at eye level / near customers' eyes", "hotspots", "special offers", "chocolates"],
    4: ["C", "A", "B", "D", "D", "Julia Perkins", "15 Waratah Road", "Brisbane", "to be advised / not connected / no phone / none", "first year Law", "C", "D", "Hope Street", "evidence", "passport", "current / student account", "chequebook", "withdraw / draw out / take out", "directly from / right out of", "permission of bank / permission from bank", "4.30 pm to 5 pm", "300 million", "paper clips", "magazine pages / pieces of paper / pages", "three times", "thicker", "label", "a dome", "flange", "25%", "scored opening", "a university lecture", "Sports Studies programme", "management", "top athletes", "makes winners / makes people win", "market forces", "other leisure activities", "entertainment / to be entertained", "exercise science", "fitness testing / body measurements", "cellular research / cellular change / body cells"],
}


def pages(doc, start, end):
    return "\n".join(doc[p - 1].get_text("text") for p in range(start, end + 1))


def clean_question_text(text):
    output = []
    for raw in text.replace("\x85", " ").splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line or re.fullmatch(r"\d{1,3}", line):
            continue
        if line.lower() == "listening" or re.fullmatch(r"Practice Test \d", line, re.I):
            continue
        output.append(line)
    return "\n".join(output)


def prompt_for_number(source, number):
    lines = source.splitlines()
    for i, line in enumerate(lines):
        if re.match(rf"^\(?{number}\)?(?:\s|\.|$)", line):
            chunk = [line]
            for nxt in lines[i + 1:i + 8]:
                if re.match(r"^\d{1,2}(?:\s|$)", nxt) and not nxt.startswith(str(number)):
                    break
                if nxt.startswith("Questions ") or nxt.startswith("SECTION "):
                    break
                chunk.append(nxt)
            return " ".join(chunk)[:900]
    match = re.search(rf"(.{{0,100}}\({number}\).{{0,180}})", source, re.S)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return f"Question {number}（请根据上方原书题目作答）"


def strip_transcript_noise(text):
    text = text.replace("\x85", " ").replace("", "'")
    # Printed answer markers are normally Q19, but older PDF text layers also
    # contain OCR-like variants such as QI9 or Ql9.
    text = re.sub(r"\bQ(?:s|[Il])?\s*\d+(?:\s+and\s+\d+)?\b", " ", text, flags=re.I)
    output = []
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line or re.fullmatch(r"\d{1,3}", line):
            continue
        if line in {"Tapescripts", "Answer keys", "Repeat", "Example"}:
            continue
        if re.fullmatch(r"Practice Test \d", line, re.I) or set(line) <= {"-"}:
            continue
        output.append(line)
    return "\n".join(output)


def split_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+(?=[A-Z'\"“])", text) if p.strip()]


def parse_segments(section_text, part):
    aliases = {k: v.strip().title() for k, v in re.findall(r"(?m)^([A-Z]{1,3})\s*=\s*([^\n]+)$", section_text)}
    text = strip_transcript_noise(section_text)
    turns, current, buffer = [], "", []

    def flush():
        nonlocal buffer
        speech = " ".join(buffer).strip()
        if speech:
            turns.append((aliases.get(current, current or "SPEAKER"), speech))
        buffer = []

    speaker_re = re.compile(r"^([A-Za-z][A-Za-z .'-]{0,35}):\s*(.*)$")
    named_speakers = {"speaker", "lecturer", "newsreader", "presenter", "interviewer", "tutor", "clerk"}
    for line in text.splitlines():
        if re.fullmatch(r"[A-Z]{1,3}\s*=\s*.+", line):
            continue
        match = speaker_re.match(line)
        label = match.group(1).strip() if match else ""
        speaker_label = bool(match) and (label.isupper() or label.lower() in named_speakers or label in aliases)
        if speaker_label:
            flush()
            current = label
            if match.group(2).strip():
                buffer.append(match.group(2).strip())
        elif not re.match(r"^(PRACTICE TEST|SECTION \d)", line, re.I):
            buffer.append(line)
    flush()

    units = turns if part in (1, 3) else [
        (speaker, sentence) for speaker, speech in turns for sentence in split_sentences(speech)
    ]
    return [{"id": i, "start": None, "speaker": speaker.upper(), "en": speech,
             "zh": "", "words": [], "answers": []}
            for i, (speaker, speech) in enumerate(units, 1)]


def transcript_sections(doc, test):
    # The PDF's visible page header is extracted after some body text.  Using
    # ``PRACTICE TEST n`` as a boundary therefore assigns the first dialogue of
    # Test 4 to Test 3.  The four real SECTION 1 headings are stable anchors.
    all_text = pages(doc, 113, 135)
    test_starts = list(re.finditer(r"SECTION\s+1\b", all_text, re.I))
    if len(test_starts) != 4:
        raise ValueError(f"Expected 4 listening test starts, found {len(test_starts)}")
    start = test_starts[test - 1].start()
    stop = test_starts[test].start() if test < 4 else len(all_text)
    text = all_text[start:stop]
    matches = list(re.finditer(r"SECTION\s+([1-4])\b", text, re.I))
    result = {}
    for i, match in enumerate(matches):
        part = int(match.group(1))
        if part in result:
            continue
        stop = next((later.start() for later in matches[i + 1:] if int(later.group(1)) != part), len(text))
        result[part] = text[match.end():stop]
    return result


def evidence_for_answer(segments, answer):
    for choice in answer.split("/"):
        core = re.sub(r"\([^)]*\)", "", choice)
        core = re.sub(r"[^A-Za-z0-9£$ ]", " ", core)
        core = re.sub(r"\s+", " ", core).strip().lower()
        if len(core) < 3 or re.fullmatch(r"[a-i]", core):
            continue
        for seg in segments:
            if core in seg["en"].lower():
                return seg["id"]
    return None


def build_part(doc, test, part, transcript):
    first, last = TESTS[test]["ranges"][part]
    qstart, qend = TESTS[test]["question_pages"][part]
    source = clean_question_text(pages(doc, qstart, qend))
    segments = parse_segments(transcript, part)
    items = []
    for number in range(first, last + 1):
        answer = ANSWERS[test][number - 1]
        evidence = evidence_for_answer(segments, answer)
        if evidence:
            segments[evidence - 1]["answers"].append(number)
        items.append({"number": number, "prompt": prompt_for_number(source, number),
                      "answer": answer, "evidence_segment": evidence, "paraphrase": None})
    pid = f"c1-test{test}-l{part}"
    return {"id": pid, "source": f"剑桥雅思1 · Test {test} · Part {part}",
            "title": TESTS[test]["titles"][part],
            "audio": f"media/audio/c1-test{test}-part{part}.mp3",
            "practice_unit": "speaker_turn" if part in (1, 3) else "sentence",
            "segments": segments,
            "questions": [{"title": f"Questions {first}–{last}", "type": "mixed",
                           "instructions": ["Complete the original Cambridge IELTS listening questions below."],
                           "source_text": source, "items": items}]}


def update_index(parts):
    path = DATA_DIR / "index.json"
    index = json.loads(path.read_text(encoding="utf-8"))
    old = [t for t in index.get("tests", []) if not str(t.get("id", "")).startswith("c1-test")]
    new = []
    for test in range(1, 5):
        plist = []
        for part in range(1, 5):
            data = parts[(test, part)]
            first, last = TESTS[test]["ranges"][part]
            plist.append({"id": data["id"], "part": part, "title": data["title"],
                          "question_range": f"{first}–{last}"})
        new.append({"id": f"c1-test{test}", "source": f"剑桥雅思1 · Test {test}", "parts": plist})
    index["tests"] = new + old
    path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def import_audio():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    list_dir = ROOT / "tmp" / "c1-audio-lists"
    list_dir.mkdir(parents=True, exist_ok=True)
    for test in range(1, 5):
        for part in range(1, 5):
            tracks = sorted(AUDIO_SOURCE.glob(f"Unit{test} Section{part}*.mp3"))
            if not tracks:
                raise SystemExit(f"Missing audio Unit{test} Section{part}")
            target = AUDIO_DIR / f"c1-test{test}-part{part}.mp3"
            listing = list_dir / f"c1-test{test}-part{part}.txt"
            listing.write_text("\n".join(f"file '{p.as_posix()}'" for p in tracks) + "\n", encoding="utf-8")
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
                            "-safe", "0", "-i", str(listing), "-ac", "1", "-b:a", "32k", str(target)], check=True)
            print(f"audio {target.name}: {len(tracks)} track(s)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--import-audio", action="store_true")
    args = parser.parse_args()
    if not PDF.exists():
        raise SystemExit(f"PDF not found: {PDF}")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    generated = {}
    for test in range(1, 5):
        sections = transcript_sections(doc, test)
        for part in range(1, 5):
            data = build_part(doc, test, part, sections[part])
            (DATA_DIR / f"{data['id']}.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            generated[(test, part)] = data
            print(f"{data['id']}: {len(data['segments'])} units, {len(data['questions'][0]['items'])} questions")
    doc.close()
    update_index(generated)
    if args.import_audio:
        import_audio()


if __name__ == "__main__":
    main()
