"""Generate draft article JSONs for Cambridge IELTS 17 Test 1.

This script builds the first usable layer of the question bank:
- English passage text
- sentence units
- question prompts
- standard answers
- approximate evidence locations

Chinese translation, grammar notes, and curated vocab are intentionally marked
as draft placeholders, so they can be refined batch by batch without blocking
the larger 14-19 library build.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
PDF = Path(r"C:\Users\11386\Desktop\雅思\雅思备考必备｜剑雅1-19真题合集+独家解析+听力原声（高清PDF+音频）\剑桥雅思真题1-19\【17】剑桥雅思真题17.pdf")
PASSAGES = ROOT / "data" / "passages"
INDEX = ROOT / "data" / "index.json"


def clean_join(lines):
    text = " ".join(x.strip() for x in lines if x.strip())
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" - ", " - ")
    return text.strip()


def extract_page_lines(pdf, page_no):
    text = pdf.pages[page_no - 1].extract_text(x_tolerance=1, y_tolerance=3) or ""
    return [x.strip() for x in text.splitlines() if x.strip()]


def paragraph_units(paragraphs):
    units = []
    sid = 1
    for para_no, para in enumerate(paragraphs, 1):
        para = re.sub(r"\s+", " ", para).strip()
        if not para:
            continue
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z‘'\"(])", para)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            units.append({
                "id": sid,
                "para": para_no,
                "en": part,
                "zh": "（待精修翻译）",
                "grammar": {
                    "type": "待精修",
                    "note": "已完成原文切句与题目入库；本句翻译和语法拆解将在精修阶段补充。"
                },
                "words": []
            })
            sid += 1
    return units


def p1_text(pdf):
    p16 = extract_page_lines(pdf, 16)
    p17 = extract_page_lines(pdf, 17)
    start = p16.index("In the first half of the 1800s, London’s population grew at an astonishing rate, and the central")
    p16_body = p16[start:]
    p17_body = [x for x in p17 if x not in {"Reading", "17"}]
    text = "\n".join(p16_body + p17_body)
    paras = [
        "In the first half of the 1800s, London’s population grew at an astonishing rate, and the central area became increasingly congested. In addition, the expansion of the overground railway network resulted in more and more passengers arriving in the capital. However, in 1846, a Royal Commission decided that the railways should not be allowed to enter the City, the capital’s historic and business centre. The result was that the overground railway stations formed a ring around the City. The area within consisted of poorly built, overcrowded slums and the streets were full of horse-drawn traffic. Crossing the City became a nightmare. It could take an hour and a half to travel 8 km by horse-drawn carriage or bus. Numerous schemes were proposed to resolve these problems, but few succeeded.",
        "Amongst the most vocal advocates for a solution to London’s traffic problems was Charles Pearson, who worked as a solicitor for the City of London. He saw both social and economic advantages in building an underground railway that would link the overground railway stations together and clear London slums at the same time. His idea was to relocate the poor workers who lived in the inner-city slums to newly constructed suburbs, and to provide cheap rail travel for them to get to work. Pearson’s ideas gained support amongst some businessmen and in 1851 he submitted a plan to Parliament. It was rejected, but coincided with a proposal from another group for an underground connecting line, which Parliament passed.",
        "The two groups merged and established the Metropolitan Railway Company in August 1854. The company’s plan was to construct an underground railway line from the Great Western Railway’s station at Paddington to the edge of the City at Farringdon Street - a distance of almost 5 km. The organisation had difficulty in raising the funding for such a radical and expensive scheme, not least because of the critical articles printed by the press. Objectors argued that the tunnels would collapse under the weight of traffic overhead, buildings would be shaken and passengers would be poisoned by the emissions from the train engines. However, Pearson and his partners persisted.",
        "The GWR, aware that the new line would finally enable them to run trains into the heart of the City, invested almost £250,000 in the scheme. Eventually, over a five-year period, £1m was raised. The chosen route ran beneath existing main roads to minimise the expense of demolishing buildings. Originally scheduled to be completed in 21 months, the construction of the underground line took three years. It was built just below street level using a technique known as ‘cut and cover’. A trench about ten metres wide and six metres deep was dug, and the sides temporarily held up with timber beams. Brick walls were then constructed, and finally a brick arch was added to create a tunnel. A two-metre-deep layer of soil was laid on top of the tunnel and the road above rebuilt.",
        "The Metropolitan line, which opened on 10 January 1863, was the world’s first underground railway. On its first day, almost 40,000 passengers were carried between Paddington and Farringdon, the journey taking about 18 minutes. By the end of the Metropolitan’s first year of operation, 9.5 million journeys had been made.",
        "Even as the Metropolitan began operation, the first extensions to the line were being authorised; these were built over the next five years, reaching Moorgate in the east of London and Hammersmith in the west. The original plan was to pull the trains with steam locomotives, using firebricks in the boilers to provide steam, but these engines were never introduced. Instead, the line used specially designed locomotives that were fitted with water tanks in which steam could be condensed. However, smoke and fumes remained a problem, even though ventilation shafts were added to the tunnels.",
        "Despite the extension of the underground railway, by the 1880s, congestion on London’s streets had become worse. The problem was partly that the existing underground lines formed a circuit around the centre of London and extended to the suburbs, but did not cross the capital’s centre. The ‘cut and cover’ method of construction was not an option in this part of the capital. The only alternative was to tunnel deep underground.",
        "Although the technology to create these tunnels existed, steam locomotives could not be used in such a confined space. It wasn’t until the development of a reliable electric motor, and a means of transferring power from the generator to a moving train, that the world’s first deep-level electric railway, the City & South London, became possible. The line opened in 1890, and ran from the City to Stockwell, south of the River Thames. The trains were made up of three carriages and driven by electric engines. The carriages were narrow and had tiny windows just below the roof because it was thought that passengers would not want to look out at the tunnel walls. The line was not without its problems, mainly caused by an unreliable power supply. Although the City & South London Railway was a great technical achievement, it did not make a profit. Then, in 1900, the Central London Railway, known as the ‘Tuppenny Tube’, began operation using new electric locomotives. It was very popular and soon afterwards new railways and extensions were added to the growing tube network. By 1907, the heart of today’s Underground system was in place.",
    ]
    return paras


def p2_text():
    return [
        "Stadiums are among the oldest forms of urban architecture: vast stadiums where the public could watch sporting events were at the centre of western city life as far back as the ancient Greek and Roman Empires, well before the construction of the great medieval cathedrals and the grand 19th- and 20th-century railway stations which dominated urban skylines in later eras. Today, however, stadiums are regarded with growing scepticism. Construction costs can soar above £1 billion, and stadiums finished for major events such as the Olympic Games or the FIFA World Cup have notably fallen into disuse and disrepair. But this need not be the case. History shows that stadiums can drive urban development and adapt to the culture of every age. Even today, architects and planners are finding new ways to adapt the mono-functional sports arenas which became emblematic of modernisation during the 20th century.",
        "The amphitheatre of Arles in southwest France, with a capacity of 25,000 spectators, is perhaps the best example of just how versatile stadiums can be. Built by the Romans in 90 AD, it became a fortress with four towers after the fifth century, and was then transformed into a village containing more than 200 houses. With the growing interest in conservation during the 19th century, it was converted back into an arena for the staging of bullfights, thereby returning the structure to its original use as a venue for public spectacles. Another example is the imposing arena of Verona in northern Italy, with space for 30,000 spectators, which was built 60 years before the Arles amphitheatre and 40 years before Rome’s famous Colosseum. It has endured the centuries and is currently considered one of the world’s prime sites for opera, thanks to its outstanding acoustics.",
        "The area in the centre of the Italian town of Lucca, known as the Piazza dell’Anfiteatro, is yet another impressive example of an amphitheatre becoming absorbed into the fabric of the city. The site evolved in a similar way to Arles and was progressively filled with buildings from the Middle Ages until the 19th century, variously used as houses, a salt depot and a prison. But rather than reverting to an arena, it became a market square, designed by Romanticist architect Lorenzo Nottolini. Today, the ruins of the amphitheatre remain embedded in the various shops and residences surrounding the public square.",
        "There are many similarities between modern stadiums and the ancient amphitheatres intended for games. But some of the flexibility was lost at the beginning of the 20th century, as stadiums were developed using new products such as steel and reinforced concrete, and made use of bright lights for night-time matches. Many such stadiums are situated in suburban areas, designed for sporting use only and surrounded by parking lots. These factors mean that they may not be as accessible to the general public, require more energy to run and contribute to urban heat.",
        "But many of today’s most innovative architects see scope for the stadium to help improve the city. Among the current strategies, two seem to be having particular success: the stadium as an urban hub, and as a power plant. There’s a growing trend for stadiums to be equipped with public spaces and services that serve a function beyond sport, such as hotels, retail outlets, conference centres, restaurants and bars, children’s playgrounds and green space. Creating mixed-use developments such as this reinforces compactness and multi-functionality, making more efficient use of land and helping to regenerate urban spaces. This opens the space up to families and a wider cross-section of society, instead of catering only to sportspeople and supporters. There have been many examples of this in the UK: the mixed-use facilities at Wembley and Old Trafford have become a blueprint for many other stadiums in the world.",
        "The phenomenon of stadiums as power stations has arisen from the idea that energy problems can be overcome by integrating interconnected buildings by means of a smart grid, which is an electricity supply network that uses digital communications technology to detect and react to local changes in usage, without significant energy losses. Stadiums are ideal for these purposes, because their canopies have a large surface area for fitting photovoltaic panels and rise high enough to make use of micro wind turbines. Freiburg Mage Solar Stadium in Germany is the first of a new wave of stadiums as power plants, which also includes the Amsterdam Arena and the Kaohsiung Stadium. The latter, inaugurated in 2009, has 8,844 photovoltaic panels producing up to 1.14 GWh of electricity annually. This reduces the annual output of carbon dioxide by 660 tons and supplies up to 80 percent of the surrounding area when the stadium is not in use. This is proof that a stadium can serve its city, and have a decidedly positive impact in terms of reduction of CO2 emissions.",
        "Sporting arenas have always been central to the life and culture of cities. In every era, the stadium has acquired new value and uses: from military fortress to residential village, public space to theatre and most recently a field for experimentation in advanced engineering. The stadium of today now brings together multiple functions, thus helping cities to create a sustainable future.",
    ]


def p3_text():
    return [
        "Charles Spencer’s latest book, To Catch a King, tells us the story of the hunt for King Charles II in the six weeks after his resounding defeat at the Battle of Worcester in September 1651. And what a story it is. After his father was executed by the Parliamentarians in 1649, the young Charles II sacrificed one of the very principles his father had died for and did a deal with the Scots, thereby accepting Presbyterianism as the national religion in return for being crowned King of Scots. His arrival in Edinburgh prompted the English Parliamentary army to invade Scotland in a pre-emptive strike. This was followed by a Scottish invasion of England. The two sides finally faced one another at Worcester in the west of England in 1651. After being comprehensively defeated on the meadows outside the city by the Parliamentarian army, the 21-year-old king found himself the subject of a national manhunt, with a huge sum offered for his capture. Over the following six weeks he managed, through a series of heart-poundingly close escapes, to evade the Parliamentarians before seeking refuge in France. For the next nine years, the penniless and defeated Charles wandered around Europe with only a small group of loyal supporters.",
        "Years later, after his restoration as king, the 50-year-old Charles II requested a meeting with the writer and diarist Samuel Pepys. His intention when asking Pepys to commit his story to paper was to ensure that this most extraordinary episode was never forgotten. Over two three-hour sittings, the king related to him in great detail his personal recollections of the six weeks he had spent as a fugitive. As the king and secretary settled down, Charles commenced his story: ‘After the battle was so absolutely lost as to be beyond hope of recovery, I began to think of the best way of saving myself.’",
        "One of the joys of Spencer’s book, a result not least of its use of Charles II’s own narrative as well as those of his supporters, is just how close the reader gets to the action. The day-by-day retelling of the fugitives’ doings provides delicious details: the cutting of the king’s long hair with agricultural shears, the use of walnut leaves to dye his pale skin, and the day Charles spent lying on a branch of the great oak tree in Boscobel Wood as the Parliamentary soldiers scoured the forest floor below. Spencer draws out both the humour - such as the preposterous refusal of Charles’s friend Henry Wilmot to adopt disguise on the grounds that it was beneath his dignity - and the emotional tension when the secret of the king’s presence was cautiously revealed to his supporters.",
        "Charles’s adventures after losing the Battle of Worcester hide the uncomfortable truth that whilst almost everyone in England had been appalled by the execution of his father, they had not welcomed the arrival of his son with the Scots army, but had instead firmly bolted their doors. This was partly because he rode at the head of what looked like a foreign invasion force and partly because, after almost a decade of civil war, people were desperate to avoid it beginning again. This makes it all the more interesting that Charles II himself loved the story so much ever after. As well as retelling it to anyone who would listen, causing eye-rolling among courtiers, he set in train a series of initiatives to memorialise it. There was to be a new order of chivalry, the Knights of the Royal Oak. A series of enormous oil paintings depicting the episode were produced, including a two-metre-wide canvas of Boscobel Wood and a set of six similarly enormous paintings of the king on the run. In 1660, Charles II commissioned the artist John Michael Wright to paint a flying squadron of cherubs carrying an oak tree to the heavens on the ceiling of his bedchamber. It is hard to imagine many other kings marking the lowest point in their life so enthusiastically, or indeed pulling off such an escape in the first place.",
        "Charles Spencer is the perfect person to pass the story on to a new generation. His pacey, readable prose steers deftly clear of modern idioms and elegantly brings to life the details of the great tale. He has even-handed sympathy for both the fugitive king and the fierce republican regime that hunted him, and he succeeds in his desire to explore far more of the background of the story than previous books on the subject have done. Indeed, the opening third of the book is about how Charles II found himself at Worcester in the first place, which for some will be reason alone to read To Catch a King.",
        "The tantalising question left, in the end, is that of what it all meant. Would Charles II have been a different king had these six weeks never happened? The days and nights spent in hiding must have affected him in some way. Did the need to assume disguises, to survive on wit and charm alone, to use trickery and subterfuge to escape from tight corners help form him? This is the one area where the book doesn’t quite hit the mark. Instead its depiction of Charles II in his final years as an ineffective, pleasure-loving monarch doesn’t do justice to the man, or to the complexity of his character. But this one niggle aside, To Catch a King is an excellent read, and those who come to it knowing little of the famous tale will find they have a treat in store.",
    ]


def passage(pid, source, title, paragraphs, questions):
    return {
        "id": pid,
        "source": source,
        "title": title,
        "quality": "draft_raw",
        "analysis_unit": "sentence",
        "sentences": paragraph_units(paragraphs),
        "questions": questions,
    }


def qgroup(title, type_, instructions, items):
    return {"title": title, "type": type_, "instructions": instructions, "items": items}


P1_Q = [
    qgroup("Questions 1-6 · Note completion", "note_completion",
           ["Complete the notes below.", "Choose ONE WORD ONLY from the passage for each answer."],
           [
               {"number": 1, "prompt": "The ___ of London increased rapidly between 1800 and 1850.", "answer": "population", "evidence_sentence": 1},
               {"number": 2, "prompt": "Building the railway would make it possible to move people to better housing in the ___.", "answer": "suburbs", "evidence_sentence": 11},
               {"number": 3, "prompt": "A number of ___ agreed with Pearson’s idea.", "answer": "businessmen", "evidence_sentence": 12},
               {"number": 4, "prompt": "The company initially had problems getting the ___ needed for the project.", "answer": "funding", "evidence_sentence": 16},
               {"number": 5, "prompt": "Negative articles about the project appeared in the ___.", "answer": "press", "evidence_sentence": 16},
               {"number": 6, "prompt": "With the completion of the brick arch, the tunnel was covered with ___.", "answer": "soil", "evidence_sentence": 26},
           ]),
    qgroup("Questions 7-13 · TRUE / FALSE / NOT GIVEN", "true_false_not_given",
           ["Do the following statements agree with the information given in Reading Passage 1?"],
           [
               {"number": 7, "prompt": "Other countries had built underground railways before the Metropolitan line opened.", "answer": "FALSE", "evidence_sentence": 27},
               {"number": 8, "prompt": "More people than predicted travelled on the Metropolitan line on the first day.", "answer": "NOT GIVEN", "evidence_sentence": 28},
               {"number": 9, "prompt": "The use of ventilation shafts failed to prevent pollution in the tunnels.", "answer": "TRUE", "evidence_sentence": 32},
               {"number": 10, "prompt": "A different approach from the ‘cut and cover’ technique was required in London’s central area.", "answer": "TRUE", "evidence_sentence": 35},
               {"number": 11, "prompt": "The windows on City & South London trains were at eye level.", "answer": "FALSE", "evidence_sentence": 40},
               {"number": 12, "prompt": "The City & South London Railway was a financial success.", "answer": "FALSE", "evidence_sentence": 42},
               {"number": 13, "prompt": "Trains on the ‘Tuppenny Tube’ nearly always ran on time.", "answer": "NOT GIVEN", "evidence_sentence": 43},
           ]),
]

P2_Q = [
    qgroup("Questions 14-17 · Matching information", "matching_information",
           ["Reading Passage 2 has seven sections, A-G.", "Which section contains the following information?"],
           [
               {"number": 14, "prompt": "a mention of negative attitudes towards stadium building projects", "answer": "A", "evidence_sentence": 3},
               {"number": 15, "prompt": "figures demonstrating the environmental benefits of a certain stadium", "answer": "F", "evidence_sentence": 27},
               {"number": 16, "prompt": "examples of the wide range of facilities available at some new stadiums", "answer": "E", "evidence_sentence": 21},
               {"number": 17, "prompt": "reference to the disadvantages of the stadiums built during a certain era", "answer": "D", "evidence_sentence": 17},
           ]),
    qgroup("Questions 18-22 · Summary completion", "summary_completion",
           ["Complete the summary below.", "Choose ONE WORD ONLY from the passage for each answer."],
           [
               {"number": 18, "prompt": "The amphitheatre of Arles was converted first into a ___.", "answer": "fortress", "evidence_sentence": 8},
               {"number": 19, "prompt": "It finally became an arena where spectators could watch ___.", "answer": "bullfights", "evidence_sentence": 9},
               {"number": 20, "prompt": "The arena in Verona is famous today as a venue where ___ is performed.", "answer": "opera", "evidence_sentence": 11},
               {"number": 21, "prompt": "Lucca’s amphitheatre was used for the storage of ___.", "answer": "salt", "evidence_sentence": 13},
               {"number": 22, "prompt": "It is now a market square with ___ and homes incorporated into the remains.", "answer": "shops", "evidence_sentence": 15},
           ]),
    qgroup("Questions 23-26 · Multiple answers", "multiple_answers",
           ["Choose TWO letters, A-E."],
           [
               {"number": 23, "prompt": "Negative feature of twentieth-century stadiums mentioned in Section D.", "answer": "C", "evidence_sentence": 17},
               {"number": 24, "prompt": "Negative feature of twentieth-century stadiums mentioned in Section D.", "answer": "D", "evidence_sentence": 16},
               {"number": 25, "prompt": "Advantage of modern stadium design mentioned by the writer.", "answer": "B", "evidence_sentence": 22},
               {"number": 26, "prompt": "Advantage of modern stadium design mentioned by the writer.", "answer": "E", "evidence_sentence": 25},
           ]),
]

P3_Q = [
    qgroup("Questions 27-31 · Summary completion", "summary_completion",
           ["Complete the summary using the list of phrases, A-J."],
           [
               {"number": 27, "prompt": "Charles II then formed a ___ with the Scots.", "answer": "H", "evidence_sentence": 4},
               {"number": 28, "prompt": "He abandoned an important ___ held by his father.", "answer": "J", "evidence_sentence": 4},
               {"number": 29, "prompt": "The battle led to a ___ for the Parliamentarians.", "answer": "F", "evidence_sentence": 8},
               {"number": 30, "prompt": "A ___ was offered for Charles’s capture.", "answer": "B", "evidence_sentence": 9},
               {"number": 31, "prompt": "He eventually managed to reach the ___ of continental Europe.", "answer": "D", "evidence_sentence": 10},
           ]),
    qgroup("Questions 32-35 · YES / NO / NOT GIVEN", "yes_no_not_given",
           ["Do the following statements agree with the claims of the writer in Reading Passage 3?"],
           [
               {"number": 32, "prompt": "Charles chose Pepys for the task because he considered him to be trustworthy.", "answer": "NOT GIVEN", "evidence_sentence": 11},
               {"number": 33, "prompt": "Charles’s personal recollection of the escape lacked sufficient detail.", "answer": "NO", "evidence_sentence": 13},
               {"number": 34, "prompt": "Charles indicated to Pepys that he had planned his escape before the battle.", "answer": "NO", "evidence_sentence": 14},
               {"number": 35, "prompt": "The inclusion of Charles’s account is a positive aspect of the book.", "answer": "YES", "evidence_sentence": 15},
           ]),
    qgroup("Questions 36-40 · Multiple choice", "multiple_choice",
           ["Choose the correct letter, A, B, C or D."],
           [
               {"number": 36, "prompt": "What is the reviewer’s main purpose in the first paragraph?", "answer": "B", "evidence_sentence": 1},
               {"number": 37, "prompt": "Why does the reviewer include examples of the fugitives’ behaviour in the third paragraph?", "answer": "C", "evidence_sentence": 16},
               {"number": 38, "prompt": "What point does the reviewer make about Charles II in the fourth paragraph?", "answer": "A", "evidence_sentence": 24},
               {"number": 39, "prompt": "What does the reviewer say about Charles Spencer in the fifth paragraph?", "answer": "B", "evidence_sentence": 29},
               {"number": 40, "prompt": "When the reviewer says the book ‘doesn’t quite hit the mark’, she is making the point that...", "answer": "D", "evidence_sentence": 34},
           ]),
]


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_index(items):
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    existing = {p["id"]: p for p in idx.get("passages", [])}
    order = [p["id"] for p in idx.get("passages", [])]
    for p in items:
        row = {
            "id": p["id"],
            "source": p["source"],
            "title": p["title"],
            "sentence_count": len(p["sentences"]),
            "question_count": sum(len(g["items"]) for g in p.get("questions", [])),
        }
        existing[p["id"]] = row
        if p["id"] not in order:
            order.append(p["id"])
    idx["passages"] = [existing[i] for i in order if i in existing]
    write_json(INDEX, idx)


def main():
    PASSAGES.mkdir(parents=True, exist_ok=True)
    with pdfplumber.open(PDF) as pdf:
        p1_paras = p1_text(pdf)

    items = [
        passage("c17-test1-p1", "剑桥雅思17 · Test 1 · Passage 1", "The development of the London underground railway", p1_paras, P1_Q),
        passage("c17-test1-p2", "剑桥雅思17 · Test 1 · Passage 2", "Stadiums: past, present and future", p2_text(), P2_Q),
        passage("c17-test1-p3", "剑桥雅思17 · Test 1 · Passage 3", "To catch a king", p3_text(), P3_Q),
    ]
    for item in items:
        write_json(PASSAGES / f"{item['id']}.json", item)
        print(item["id"], len(item["sentences"]), "sentences")
    update_index(items)


if __name__ == "__main__":
    main()
