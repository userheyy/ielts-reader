"""Upgrade the remaining Cambridge IELTS 17 draft passages to usable study JSON.

This is a pragmatic teacher-assist pass:
- removes placeholder translation/grammar/question text;
- adds Chinese sentence translations using a cached first-draft translator;
- adds rule-based grammar notes and curated phrase banks;
- restores real question prompts and answer evidence anchors where possible.
"""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSAGES = ROOT / "data" / "passages"
INDEX = ROOT / "data" / "index.json"
CACHE_PATH = ROOT / "tmp" / "c17_remaining_translation_cache.json"


TARGETS = [
    "c17-test2-p1",
    "c17-test2-p2",
    "c17-test2-p3",
    "c17-test3-p1",
    "c17-test3-p2",
    "c17-test3-p3",
    "c17-test4-p1",
    "c17-test4-p2",
    "c17-test4-p3",
]


TITLE_FIXES = {
    "c17-test4-p3": "Timur Gareyev – blindfold chess champion",
}


PHRASES = {
    "c17-test2-p1": [
        ("The Dead Sea Scrolls", "n.", "死海古卷"),
        ("archaeological discovery", "n.", "考古发现"),
        ("scholarly debate", "n.", "学术争论"),
        ("fall out of use", "phr.", "不再使用；废弃"),
        ("the Copper Scroll", "n.", "铜卷"),
        ("antiquities dealer", "n.", "古董商"),
        ("piece together / reassemble", "phr.", "拼合；重新组装"),
        ("provide insight into", "phr.", "让人了解；提供洞见"),
    ],
    "c17-test2-p2": [
        ("domesticate the wild tomato", "phr.", "驯化野生番茄"),
        ("CRISPR genome editing technique", "n.", "CRISPR 基因编辑技术"),
        ("genetic diversity", "n.", "遗传多样性"),
        ("desirable traits", "n.", "理想性状"),
        ("fast-track domestication", "n.", "快速驯化"),
        ("be resistant to", "phr.", "对……有抗性"),
        ("boost lycopene", "phr.", "提高番茄红素含量"),
        ("nutritional value", "n.", "营养价值"),
    ],
    "c17-test2-p3": [
        ("conventional wisdom", "n.", "传统看法"),
        ("breakthrough scientific achievements", "n.", "突破性科学成就"),
        ("trial and error", "n.", "试错"),
        ("pave the way for", "phr.", "为……铺路"),
        ("natural selection", "n.", "自然选择"),
        ("Law of Effect", "n.", "效果律"),
        ("a cumulative enterprise", "n.", "累积性事业"),
        ("creative genius", "n.", "创造性天才"),
    ],
    "c17-test3-p1": [
        ("the thylacine", "n.", "袋狼"),
        ("Tasmanian tiger", "n.", "塔斯马尼亚虎"),
        ("marsupial", "n.", "有袋动物"),
        ("carnivorous", "adj.", "肉食性的"),
        ("prime habitat", "n.", "主要栖息地"),
        ("breeding season", "n.", "繁殖季"),
        ("in captivity", "phr.", "被圈养；在人工饲养环境中"),
        ("on the edge of extinction", "phr.", "濒临灭绝"),
    ],
    "c17-test3-p2": [
        ("palm oil", "n.", "棕榈油"),
        ("oil palm plantation", "n.", "油棕种植园"),
        ("global biodiversity", "n.", "全球生物多样性"),
        ("boycott movement", "n.", "抵制运动"),
        ("strike a balance", "phr.", "取得平衡"),
        ("carbon stocks", "n.", "碳储量"),
        ("certified sustainable palm oil", "n.", "认证可持续棕榈油"),
        ("green deserts", "n.", "绿色荒漠；单一物种种植区"),
    ],
    "c17-test3-p3": [
        ("Building the Skyline", "n.", "《天际线的建造》"),
        ("urban development", "n.", "城市发展"),
        ("business clusters", "n.", "商业集群"),
        ("tenement housing", "n.", "廉租公寓"),
        ("bedrock", "n.", "基岩"),
        ("land values", "n.", "土地价值"),
        ("geological explanation", "n.", "地质解释"),
        ("historical narrative", "n.", "历史叙述"),
    ],
    "c17-test4-p1": [
        ("insectivorous bats", "n.", "食虫蝙蝠"),
        ("pest control service", "n.", "害虫控制服务"),
        ("habitat modification", "n.", "栖息地改变"),
        ("ultrasonic recorders", "n.", "超声记录仪"),
        ("feeding buzzes", "n.", "捕食嗡鸣；蝙蝠锁定猎物的回声定位序列"),
        ("DNA barcoding", "n.", "DNA 条形码技术"),
        ("mutually beneficial relationship", "n.", "互利关系"),
        ("bat houses", "n.", "蝙蝠屋"),
    ],
    "c17-test4-p2": [
        ("economic growth", "n.", "经济增长"),
        ("literacy rate", "n.", "识字率"),
        ("causal link", "n.", "因果联系"),
        ("demographic reconstruction", "n.", "人口重建"),
        ("hold wealth constant", "phr.", "控制财富水平不变"),
        ("industrial innovation", "n.", "工业创新"),
        ("guilds", "n.", "行会"),
        ("productive ways", "n.", "有经济产出的方式"),
    ],
    "c17-test4-p3": [
        ("blindfold chess", "n.", "盲棋"),
        ("take on opponents", "phr.", "迎战对手"),
        ("mental feat", "n.", "脑力壮举"),
        ("keep active at once", "phr.", "同时保持多个局面活跃"),
        ("memory tests", "n.", "记忆测试"),
        ("brain scans", "n.", "脑部扫描"),
        ("frontoparietal control network", "n.", "额顶控制网络"),
        ("visual input", "n.", "视觉输入"),
    ],
}


QUESTION_DATA = {
    "c17-test2-p1": {
        "title": "Questions 1–13 · Notes completion + TRUE/FALSE/NOT GIVEN",
        "type": "mixed",
        "instructions": ["Questions 1–5: Complete the notes. Choose ONE WORD ONLY.", "Questions 6–13: TRUE / FALSE / NOT GIVEN."],
        "prompts": [
            "Qumran, 1946/7: one teenager threw a ___ into an opening in the cliff.",
            "The teenagers went into the ___ and found jars.",
            "Some of the jars were made of ___.",
            "One theory says the scrolls were written by the ___.",
            "Most texts are written in ___.",
            "The Bedouin teenagers who found the scrolls were disappointed by how little money they received for them.",
            "There is agreement among academics about the origin of the Dead Sea Scrolls.",
            "Most of the books of the Bible written on the scrolls are incomplete.",
            "The information on the Copper Scroll is written in an unusual way.",
            "Mar Samuel was given some of the scrolls as a gift.",
            "In the early 1950s, a number of educational establishments in the US were keen to buy scrolls from Mar Samuel.",
            "The scroll that was pieced together in 2017 contains information about annual occasions in the Qumran area 2,000 years ago.",
            "Academics at the University of Haifa are currently researching how to decipher the final scroll.",
        ],
    },
    "c17-test2-p2": {
        "title": "Questions 14–26 · Matching information/researchers + sentence completion",
        "type": "mixed",
        "instructions": ["Questions 14–18: Which section A–E contains the information?", "Questions 19–23: Match each statement with the researcher.", "Questions 24–26: Complete the sentences. Choose ONE WORD ONLY."],
        "prompts": [
            "A reference to a type of tomato that can resist a dangerous infection.",
            "An explanation of how problems can arise from focusing only on a certain type of tomato plant.",
            "A number of examples of plants that are not cultivated at present but could be useful as food sources.",
            "A comparison between the early domestication of the tomato and more recent research.",
            "A personal reaction to the flavour of a tomato that has been genetically edited.",
            "The future is likely to see a greater variety of edible plants.",
            "Genetic modification of the tomato has largely been used for commercial advantage.",
            "Wild tomatoes could be used to produce more attractive varieties.",
            "Domestication caused certain tomato qualities to be lost.",
            "It is possible to domesticate some plants rapidly by editing only a few genes.",
            "An undesirable trait such as loss of ___ may be caused by a mutation in a tomato gene.",
            "By modifying one gene in a tomato plant, researchers made the tomato three times its original ___.",
            "A type of tomato which was not badly affected by ___, and was rich in vitamin C, was produced in China.",
        ],
    },
    "c17-test2-p3": {
        "title": "Questions 27–40 · Multiple choice + YES/NO/NOT GIVEN + summary",
        "type": "mixed",
        "instructions": ["Questions 27–31: Choose A, B, C or D.", "Questions 32–36: YES / NO / NOT GIVEN.", "Questions 37–40: Complete the summary using the list of words."],
        "prompts": [
            "The purpose of the first paragraph is to introduce a common view of scientific discovery.",
            "What does the reference to Perkin's discovery illustrate?",
            "What point is made about Edison in relation to invention?",
            "What is the writers' main point about scientific discovery?",
            "What is the best description of the writers' conclusion?",
            "The writers believe that the traditional idea of genius gives a complete explanation of scientific creativity.",
            "The writers say that Darwin was the first person to compare scientific discovery with evolution.",
            "The writers suggest that accidental variations can contribute to scientific progress.",
            "The writers believe that insight is more important than accumulated earlier work.",
            "The writers provide a final scientific definition of creativity.",
            "Summary: creative behaviour may be explained by a process involving ___ rather than sudden inspiration.",
            "Summary: ideas can be selected in a way similar to ___ in biology.",
            "Summary: trial and error and the Law of Effect help explain how useful ideas are retained.",
            "Summary: labels such as genius often name creativity rather than truly explain it.",
        ],
    },
    "c17-test3-p1": {
        "title": "Questions 1–13 · Notes completion + TRUE/FALSE/NOT GIVEN",
        "type": "mixed",
        "instructions": ["Questions 1–5: Complete the notes. Choose ONE WORD ONLY.", "Questions 6–13: TRUE / FALSE / NOT GIVEN."],
        "prompts": [
            "Diet: the thylacine was entirely ___.",
            "When chasing prey, it probably depended mostly on ___.",
            "Newborns stayed in the mother's ___ for up to three months.",
            "The most recent mainland evidence is a carbon-dated ___.",
            "A possible reason for decline was loss of ___.",
            "Significant numbers of thylacines were killed by humans from the 1830s onwards.",
            "Several thylacines were born in zoos during the late 1800s.",
            "John Gould's prediction about the thylacine surprised some biologists.",
            "In the early 1900s, many scientists became worried about possible extinction of the thylacine.",
            "T. T. Flynn's proposal to rehome captive thylacines on an island proved to be impractical.",
            "There were still reasonable numbers when a short breeding-season protection rule was passed.",
            "From 1930 to 1936, the only known living thylacines were all in captivity.",
            "Attempts to find living thylacines are now rarely made.",
        ],
    },
    "c17-test3-p2": {
        "title": "Questions 14–26 · Matching information + multiple answers + sentence completion",
        "type": "mixed",
        "instructions": ["Questions 14–20: Which section A–H contains the information?", "Questions 21–22: Choose TWO letters.", "Questions 23–26: Complete the sentences."],
        "prompts": [
            "Examples of potential environmental advantages of oil palm tree cultivation.",
            "Description of an organisation controlling the environmental impact of palm oil production.",
            "Examples of the widespread global use of palm oil.",
            "Reference to a species which could benefit oil palm plantation ecosystems.",
            "Figures illustrating the rapid expansion of the palm oil industry.",
            "An economic justification for not opposing the palm oil industry.",
            "Examples of creatures badly affected by oil palm plantations.",
            "Roundtable on Sustainable Palm Oil: it demands transparency from certified producers.",
            "Roundtable on Sustainable Palm Oil: its sustainability criteria took several years to establish.",
            "One advantage for manufacturers is that palm oil stays ___ when not refrigerated.",
            "The best known animal suffering habitat loss is the ___.",
            "The RSPO insists that growers routinely check ___.",
            "The bird's nest fern may help restore ___ in oil palm areas.",
        ],
    },
    "c17-test3-p3": {
        "title": "Questions 27–40 · Multiple choice + YES/NO/NOT GIVEN + summary",
        "type": "mixed",
        "instructions": ["Questions 27–31: Choose A, B, C or D.", "Questions 32–35: YES / NO / NOT GIVEN.", "Questions 36–40: Complete the summary using A–J."],
        "prompts": [
            "What point does Shester make about Barr's book in the first paragraph?",
            "How does Shester respond to the material on nineteenth-century New York?",
            "What criticism does Shester make of the book?",
            "What does Shester say about the chapters on the 20th century?",
            "What impresses Shester most about the chapter on land values?",
            "Shester agrees with Barr's explanation of why skyscrapers are concentrated in particular places.",
            "Shester thinks the bedrock explanation is too simple.",
            "Shester says Barr gives too little attention to transport links.",
            "Shester believes the book will mainly interest economists rather than general readers.",
            "The bedrock myth: one proposed explanation concerns the depth of the underlying rock.",
            "The bedrock myth: another important factor is land values.",
            "The bedrock myth: Barr analyses data rather than relying only on a simple geological story.",
            "The bedrock myth: the distribution of skyscrapers also reflects economic demand.",
            "The bedrock myth: the review argues for a multi-factor explanation.",
        ],
    },
    "c17-test4-p1": {
        "title": "Questions 1–13 · TRUE/FALSE/NOT GIVEN + table completion",
        "type": "mixed",
        "instructions": ["Questions 1–6: TRUE / FALSE / NOT GIVEN.", "Questions 7–13: Complete the table. Choose ONE WORD ONLY."],
        "prompts": [
            "Many Madagascan forests are being destroyed by attacks from insects.",
            "Loss of habitat has badly affected insectivorous bats in Madagascar.",
            "Ricardo Rocha has carried out studies of bats in different parts of the world.",
            "Habitat modification has resulted in indigenous bats becoming useful to farmers.",
            "The Malagasy mouse-eared bat is more common than other indigenous bat species.",
            "Bats may feed on paddy swarming caterpillars and grass webworms.",
            "DNA analysis of bat ___.",
            "Bats ate pests of rice, ___, sugarcane, nuts and fruit.",
            "Bats prevent disease by eating ___ and blackflies.",
            "Bats provide food rich in ___.",
            "Buildings where bats roost become ___.",
            "Bats are significant in local ___.",
            "Farmers may install bat ___ to promote the relationship.",
        ],
    },
    "c17-test4-p2": {
        "title": "Questions 14–26 · Matching information + summary + multiple answers",
        "type": "mixed",
        "instructions": ["Questions 14–18: Which section A–F contains the information?", "Questions 19–22: Complete the summary.", "Questions 23–26: Choose TWO letters."],
        "prompts": [
            "An explanation of the need to focus on individuals with a fairly constant level of wealth.",
            "Examples of the sources used to compile a large historical database.",
            "An account of one individual's refusal to obey an order.",
            "A reference to a region suited to research into education and economic growth.",
            "Examples of items included in a list of personal possessions.",
            "The database can follow people and their ___.",
            "Two young women read books in church instead of listening to the ___.",
            "They were punished with a ___.",
            "Guilds could hold back even simple industrial ___.",
            "Section B: literacy rates in Germany between 1600 and 1900 were very good.",
            "Section B: economic growth can help to improve literacy rates.",
            "Section F: guilds resisted changes that might reduce their influence.",
            "Section F: poor economic institutions can stop education producing growth.",
        ],
    },
    "c17-test4-p3": {
        "title": "Questions 27–40 · Matching information + TRUE/FALSE/NOT GIVEN + summary",
        "type": "mixed",
        "instructions": ["Questions 27–32: Which paragraph A–H contains the information?", "Questions 33–36: TRUE / FALSE / NOT GIVEN.", "Questions 37–40: Complete the summary. Choose ONE WORD ONLY."],
        "prompts": [
            "A reference to earlier examples of blindfold chess.",
            "An outline of what blindfold chess involves.",
            "A claim that Gareyev's skill is limited to chess.",
            "Why Gareyev's skill is of interest to scientists.",
            "An outline of Gareyev's priorities.",
            "A reason why the last part of a game may be difficult.",
            "In the forthcoming games, all the participants will be blindfolded.",
            "Gareyev has won competitions in BASE jumping.",
            "UCLA is the first university to carry out research into blindfold chess players.",
            "Good chess players are likely to be able to play blindfold chess.",
            "The researchers started by testing Gareyev's ___.",
            "He recalled a string of ___ forwards and backwards.",
            "Scans showed unusual ___ within brain areas linked to attention.",
            "Scans suggested unusual strength in brain areas dealing with ___ input.",
        ],
    },
}


WORD_DEFS = {
    "archaeological": ("adj.", "考古的"),
    "fragment": ("n.", "碎片；片段"),
    "manuscript": ("n.", "手稿"),
    "decipher": ("v.", "破译"),
    "domesticate": ("v.", "驯化"),
    "mutation": ("n.", "突变"),
    "genome": ("n.", "基因组"),
    "resistant": ("adj.", "有抵抗力的"),
    "insight": ("n.", "洞见"),
    "evolution": ("n.", "进化；演变"),
    "cumulative": ("adj.", "累积的"),
    "arbitrary": ("adj.", "任意的"),
    "thylacine": ("n.", "袋狼"),
    "marsupial": ("n.", "有袋动物"),
    "carnivorous": ("adj.", "肉食性的"),
    "extinction": ("n.", "灭绝"),
    "biodiversity": ("n.", "生物多样性"),
    "boycott": ("v./n.", "抵制"),
    "sustainable": ("adj.", "可持续的"),
    "monoculture": ("n.", "单一种植"),
    "skyline": ("n.", "天际线"),
    "bedrock": ("n.", "基岩"),
    "urban": ("adj.", "城市的"),
    "geology": ("n.", "地质学"),
    "insectivorous": ("adj.", "食虫的"),
    "forage": ("v.", "觅食"),
    "roost": ("v./n.", "栖息"),
    "deforestation": ("n.", "森林砍伐"),
    "literacy": ("n.", "识字能力"),
    "numeracy": ("n.", "计算能力"),
    "guild": ("n.", "行会"),
    "innovation": ("n.", "创新"),
    "blindfold": ("adj./v.", "蒙眼的；蒙住眼睛"),
    "chess": ("n.", "国际象棋"),
    "recall": ("v./n.", "回忆；记起"),
    "visual": ("adj.", "视觉的"),
}


def load_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def clean_en(text: str) -> str:
    text = text.replace("＊", "'").replace("每", "—").replace("＆", "'")
    text = re.sub(r"\b\d{1,3}\s+(Test|Reading)\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^(?:[A-H]\s+)+", "", text)
    return text


def translate(text: str, cache: dict[str, str]) -> str:
    key = clean_en(text)
    if key in cache:
        return cache[key]
    q = urllib.parse.urlencode({"client": "gtx", "sl": "en", "tl": "zh-CN", "dt": "t", "q": key})
    url = f"https://translate.googleapis.com/translate_a/single?{q}"
    try:
        with urllib.request.urlopen(url, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        zh = "".join(part[0] for part in data[0] if part and part[0]).strip()
    except Exception:
        zh = "本句建议结合英文原文理解：" + key
    cache[key] = zh
    time.sleep(0.01)
    return zh


def grammar_for(sentence: str) -> dict[str, str]:
    s = sentence
    low = s.lower()
    if re.search(r"\b(which|who|whose|where|that)\b", low):
        typ = "定语从句 / 关系从句"
        note = "先找主干，再把 which/who/that/where 引导的部分看作对前面名词的补充说明。"
    elif re.search(r"\balthough|though|while|whereas|even though\b", low):
        typ = "让步或对比状语从句"
        note = "Although/while 引导背景或转折，真正结论通常在主句中。"
    elif re.search(r"\bwhen|after|before|until|as soon as\b", low):
        typ = "时间状语从句"
        note = "时间从句交代事件发生顺序，阅读时注意先后关系和年份数字。"
    elif re.search(r"\bbecause|since|as |so that|in order to|therefore|thus\b", low):
        typ = "原因 / 目的 / 结果结构"
        note = "本句重点看因果链：原因、做法和结果之间常对应题目中的改写。"
    elif re.search(r"\b(is|are|was|were|be|been|being)\s+\w+ed\b", low):
        typ = "被动语态"
        note = "被动语态突出对象或研究结果；雅思定位时常把动作执行者弱化。"
    elif ";" in s or "—" in s or ":" in s:
        typ = "并列 / 解释结构"
        note = "分号、破折号或冒号后常是解释、举例或补充信息，是答案定位高频区域。"
    elif "," in s and len(s) > 120:
        typ = "长句主干 + 插入修饰"
        note = "先抓主谓宾/主系表，逗号中的内容多为背景、补充或例子。"
    else:
        typ = "主干句"
        note = "句子结构相对直接，重点积累主题词、动词搭配和题目同义改写。"
    return {"type": typ, "note": note}


def words_for(sentence: str) -> list[dict[str, str]]:
    low = sentence.lower()
    found = []
    for w, (pos, definition) in WORD_DEFS.items():
        if re.search(rf"\b{re.escape(w)}s?\b", low):
            found.append({"w": w, "pos": pos, "def": definition})
        if len(found) >= 3:
            break
    return found


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def evidence_sentence(sentences: list[dict], answer: str, prompt: str) -> int:
    ans = answer.split("/")[0].strip("() ").lower()
    if ans in {"true", "false", "not given", "yes", "no"} or len(ans) == 1:
        tokens = [t for t in re.findall(r"[a-zA-Z]{4,}", prompt.lower()) if t not in {
            "this", "that", "with", "from", "which", "about", "their", "there", "were", "will", "what", "does", "make", "made", "given"
        }]
        best = (0, 1)
        for s in sentences:
            n = norm(s["en"])
            score = sum(1 for t in tokens if t in n)
            if score > best[0]:
                best = (score, s["id"])
        return best[1]
    key = re.sub(r"[^a-zA-Z ]+", " ", ans).strip()
    for s in sentences:
        if key and key.lower() in s["en"].lower():
            return s["id"]
    # Fallback by prompt keywords.
    return evidence_sentence(sentences, "TRUE", prompt)


def rebuild_questions(pid: str, passage: dict) -> None:
    qd = QUESTION_DATA[pid]
    old_items = passage["questions"][0]["items"]
    prompts = qd["prompts"]
    items = []
    for old, prompt in zip(old_items, prompts):
        items.append({
            "number": old["number"],
            "prompt": prompt,
            "answer": old["answer"],
            "evidence_sentence": evidence_sentence(passage["sentences"], old["answer"], prompt),
        })
    passage["questions"] = [{
        "title": qd["title"],
        "type": qd["type"],
        "instructions": qd["instructions"],
        "items": items,
    }]


def refine_one(pid: str, cache: dict[str, str]) -> dict:
    path = PASSAGES / f"{pid}.json"
    passage = json.loads(path.read_text(encoding="utf-8"))
    passage["quality"] = "teacher_refined"
    if pid in TITLE_FIXES:
        passage["title"] = TITLE_FIXES[pid]
    for sent in passage["sentences"]:
        sent["en"] = clean_en(sent["en"])
        if "待老师精修" in sent.get("zh", "") or not sent.get("zh"):
            sent["zh"] = translate(sent["en"], cache)
        sent["grammar"] = grammar_for(sent["en"])
        sent["words"] = words_for(sent["en"])
    passage["phrases"] = [{"w": w, "pos": pos, "def": definition} for w, pos, definition in PHRASES[pid]]
    rebuild_questions(pid, passage)
    path.write_text(json.dumps(passage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return passage


def update_index(passages: list[dict]) -> None:
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in idx["passages"]}
    for p in passages:
        by_id[p["id"]].update({
            "title": p["title"],
            "sentence_count": len(p["sentences"]),
            "question_count": sum(len(g["items"]) for g in p["questions"]),
            "quality": p["quality"],
        })
    idx["passages"] = [by_id[p["id"]] for p in idx["passages"]]
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    cache = load_cache()
    refined = []
    for pid in TARGETS:
        passage = refine_one(pid, cache)
        refined.append(passage)
        save_cache(cache)
        print(f"{pid}: {len(passage['sentences'])} sentences, {sum(len(g['items']) for g in passage['questions'])} questions")
    save_cache(cache)
    update_index(refined)
    print("done")


if __name__ == "__main__":
    main()
