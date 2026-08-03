"""Repair Cambridge IELTS 17 Test 4 reading passages and evidence mappings.

The original Test 4 import dropped page 81 (the first 18 sentences of Passage 1),
used extraction chunks instead of printed sections for Passage 2, and left several
question explanations pointing at unrelated sentences.  This migration rebuilds
the affected sentence arrays from the printed PDF and is intentionally idempotent.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSAGES = ROOT / "data" / "passages"
INDEX = ROOT / "data" / "index.json"


def word(w: str, pos: str, definition: str) -> dict:
    return {"w": w, "pos": pos, "def": definition}


def sentence(
    en: str,
    zh: str,
    grammar_type: str,
    grammar_note: str,
    words: list[dict],
) -> dict:
    return {
        "en": en,
        "zh": zh,
        "grammar": {"type": grammar_type, "note": grammar_note},
        "words": words,
    }


P1_MISSING = [
    sentence(
        "There are few places in the world where relations between agriculture and conservation are more strained.",
        "世界上很少有地方像马达加斯加这样，农业与自然保护之间的关系如此紧张。",
        "There be + 定语从句 + 比较级",
        "主干是 There are few places；where 引导定语从句修饰 places；more strained 表示农业与自然保护之间的关系更为紧张。",
        [word("strained", "adj.", "紧张的；关系不和的")],
    ),
    sentence(
        "Madagascar’s forests are being converted to agricultural land at a rate of one percent every year.",
        "马达加斯加的森林正以每年 1% 的速度被改造成农业用地。",
        "现在进行时被动语态",
        "主干是 forests are being converted to agricultural land；现在进行时的被动语态强调这一变化仍在持续；at a rate of 交代速度。",
        [word("convert", "v.", "转变；改造"), word("at a rate of", "phr.", "以……的速度")],
    ),
    sentence(
        "Much of this destruction is fuelled by the cultivation of the country’s main staple crop: rice.",
        "这种破坏在很大程度上是由该国主要粮食作物——水稻——的种植所推动的。",
        "被动语态 + 冒号解释",
        "主干是 Much of this destruction is fuelled by the cultivation；冒号后的 rice 解释 main staple crop，fuel 在此表示“促使、推动”。",
        [word("cultivation", "n.", "种植；耕作"), word("staple crop", "n.", "主要粮食作物")],
    ),
    sentence(
        "And a key reason for this destruction is that insect pests are destroying vast quantities of what is grown by local subsistence farmers, leading them to clear forest to create new paddy fields.",
        "造成这种破坏的一个关键原因是，害虫毁掉了当地自给农户种植的大量作物，迫使他们清除森林来开辟新的稻田。",
        "表语从句 + what 从句 + 分词结果状语",
        "主干是 a key reason is that ...；that 引导表语从句；what is grown 是介词 of 的宾语从句；leading them to clear ... 表示害虫毁坏作物造成的结果。",
        [word("subsistence farmer", "n.", "自给农户"), word("paddy field", "n.", "稻田")],
    ),
    sentence(
        "The result is devastating habitat and biodiversity loss on the island, but not all species are suffering.",
        "其结果是岛上栖息地和生物多样性遭到严重破坏，但并非所有物种都在受害。",
        "并列句 + 部分否定",
        "but 连接两个转折分句；not all species 是部分否定，意为“并非所有物种”，不能理解为“所有物种都没有受害”。",
        [word("devastating", "adj.", "破坏性极大的"), word("biodiversity", "n.", "生物多样性")],
    ),
    sentence(
        "In fact, some of the island’s insectivorous bats are currently thriving and this has important implications for farmers and conservationists alike.",
        "事实上，岛上的一些食虫蝙蝠目前正繁衍兴旺，这对农民和自然保护工作者都有重要意义。",
        "并列句 + 指代",
        "and 连接 bats are thriving 与 this has implications；this 指前面“部分食虫蝙蝠正在兴旺”这一事实；alike 表示两类人同样受影响。",
        [word("insectivorous", "adj.", "食虫的"), word("implication", "n.", "可能的影响；意义")],
    ),
    sentence(
        "Enter University of Cambridge zoologist Ricardo Rocha.",
        "这时，剑桥大学动物学家里卡多·罗查走进了人们的视野。",
        "叙事性倒装",
        "Enter 放在句首用于引出新人物，相当于 Ricardo Rocha enters the story；不是命令句。",
        [word("zoologist", "n.", "动物学家")],
    ),
    sentence(
        "He’s passionate about conservation, and bats.",
        "他热衷于自然保护，也热爱研究蝙蝠。",
        "主系表 + 并列宾语",
        "主干是 He is passionate about ...；conservation 与 bats 并列作介词 about 的宾语，逗号用于强调 bats。",
        [word("be passionate about", "phr.", "热衷于；对……充满热情")],
    ),
    sentence(
        "More specifically, he’s interested in how bats are responding to human activity and deforestation in particular.",
        "更具体地说，他尤其关注蝙蝠如何应对人类活动，特别是森林砍伐。",
        "介词宾语从句",
        "how bats are responding ... 是介词 in 的宾语从句；in particular 强调 deforestation 是研究重点。",
        [word("deforestation", "n.", "森林砍伐"), word("in particular", "phr.", "尤其；特别")],
    ),
    sentence(
        "Rocha’s new study shows that several species of bats are giving Madagascar’s rice farmers a vital pest control service by feasting on plagues of insects.",
        "罗查的新研究表明，数种蝙蝠通过大量捕食成群害虫，为马达加斯加稻农提供了至关重要的害虫防治服务。",
        "宾语从句 + 双宾语 + by doing",
        "shows 后接 that 宾语从句；give farmers a service 是双宾语结构；by feasting on ... 说明提供防虫服务的方式。",
        [word("pest control", "n.", "害虫防治"), word("feast on", "phr.", "大量食用；尽情享用")],
    ),
    sentence(
        "And this, he believes, can ease the financial pressure on farmers to turn forest into fields.",
        "他认为，这可以减轻农民把森林改成农田所承受的经济压力。",
        "插入语 + 不定式后置修饰",
        "主干是 this can ease the financial pressure；he believes 是插入语；to turn forest into fields 后置说明 pressure 的具体内容。",
        [word("ease", "v.", "缓解；减轻"), word("financial pressure", "n.", "经济压力")],
    ),
    sentence(
        "Bats comprise roughly one-fifth of all mammal species in Madagascar and thirty-six recorded bat species are native to the island, making it one of the most important regions for conservation of this animal group anywhere in the world.",
        "蝙蝠约占马达加斯加全部哺乳动物物种的五分之一，已记录的 36 种蝙蝠均为该岛原生物种，使这里成为全球保护这一动物类群最重要的地区之一。",
        "并列句 + 分词结果状语",
        "and 连接 Bats comprise ... 与 species are native ...；making it ... 是现在分词结果状语，it 指 Madagascar。",
        [word("comprise", "v.", "构成；占"), word("be native to", "phr.", "原产于")],
    ),
    sentence(
        "Co-leading an international team of scientists, Rocha found that several species of indigenous bats are taking advantage of habitat modification to hunt insects swarming above the country’s rice fields.",
        "罗查与他人共同带领一支国际科学家团队，发现数种本土蝙蝠正利用栖息地变化，捕食在该国稻田上空成群飞舞的昆虫。",
        "分词状语 + 宾语从句 + 分词定语",
        "Co-leading ... 作伴随状语；found 后接 that 宾语从句；swarming above ... 是现在分词短语，后置修饰 insects。",
        [word("indigenous", "adj.", "本土的；土生土长的"), word("habitat modification", "n.", "栖息地改变")],
    ),
    sentence(
        "They include the Malagasy mouse-eared bat, Major’s long-fingered bat, the Malagasy white-bellied free-tailed bat and Peters’ wrinkle-lipped bat.",
        "它们包括马达加斯加鼠耳蝠、马氏长指蝠、马达加斯加白腹犬吻蝠和彼得斯皱唇蝠。",
        "主谓宾 + 并列列举",
        "They 指上句的数种本土蝙蝠；include 后并列列出四个物种，题目只说明其中包含哪些物种，并未比较其常见程度。",
        [word("mouse-eared bat", "n.", "鼠耳蝠"), word("free-tailed bat", "n.", "犬吻蝠；游离尾蝠")],
    ),
    sentence(
        "‘These winner species are providing a valuable free service to Madagascar as biological pest suppressors,’ says Rocha.",
        "“这些胜出物种正作为生物害虫抑制者，为马达加斯加提供宝贵的免费服务，”罗查说。",
        "直接引语 + as 身份补语",
        "引语主干是 These species are providing a service；as biological pest suppressors 说明蝙蝠发挥作用的身份。",
        [word("suppressor", "n.", "抑制者；控制因素"), word("valuable", "adj.", "宝贵的；有价值的")],
    ),
    sentence(
        "‘We found that six species of bat are preying on rice pests, including the paddy swarming caterpillar and grass webworm.",
        "“我们发现有六种蝙蝠正在捕食水稻害虫，其中包括稻纵卷叶螟幼虫和草地螟。",
        "宾语从句 + including 列举",
        "found 后接 that 宾语从句；prey on 表示“捕食”；including 后列出两种具体水稻害虫，直接对应第 6 题。",
        [word("prey on", "phr.", "捕食"), word("caterpillar", "n.", "毛虫；蛾蝶幼虫")],
    ),
    sentence(
        "The damage which these insects cause puts the island’s farmers under huge financial pressure and that encourages deforestation.’",
        "这些昆虫造成的损害让岛上的农民承受巨大的经济压力，而这又助长了森林砍伐。”",
        "定语从句 + 并列句",
        "which these insects cause 修饰 The damage；put ... under pressure 表示“使……承受压力”；that 指前述经济压力，并与 encourages 构成第二个分句。",
        [word("put ... under pressure", "phr.", "使……承受压力"), word("encourage", "v.", "促使；助长")],
    ),
    sentence(
        "The study, now published in the journal Agriculture, Ecosystems and Environment, set out to investigate the feeding activity of insectivorous bats in the farmland bordering the Ranomafana National Park in the southeast of the country.",
        "这项现已发表于《农业、生态系统与环境》期刊的研究，旨在调查该国东南部拉努马法纳国家公园周边农田中食虫蝙蝠的觅食活动。",
        "过去分词插入语 + set out to do",
        "now published ... 是过去分词插入语，补充研究的发表信息；主干是 The study set out to investigate ...；bordering ... 后置修饰 farmland。",
        [word("set out to", "phr.", "着手；旨在"), word("border", "v.", "与……接壤；位于……边缘")],
    ),
]


P1_SPLITS = {
    26: sentence(
        "‘But our study is the first to show this happening in Madagascar, where the stakes for both farmers and conservationists are so high.’",
        "“但我们的研究首次证实了这一现象正发生在马达加斯加——在那里，农民和自然保护者双方都利害攸关。”",
        "直接引语 + where 定语从句",
        "主干是 our study is the first to show ...；where 引导非限制性定语从句，补充说明 Madagascar 的情形。",
        [word("stakes", "n.", "利害关系；风险")],
    ),
    27: sentence(
        "Local people may have a further reason to be grateful to their bats.",
        "当地人或许还有另一个理由感谢这些蝙蝠。",
        "主谓宾 + 不定式定语",
        "主干是 Local people may have a further reason；to be grateful ... 后置修饰 reason，并引出蝙蝠减少疾病传播的益处。",
        [word("be grateful to", "phr.", "感激；感谢")],
    ),
    35: sentence(
        "Rocha says, ‘With the right help, we hope that farmers can promote this mutually beneficial relationship by installing bat houses.’",
        "罗查说：“只要给予恰当帮助，我们希望农民能通过安装蝙蝠屋来促进这种互利关系。”",
        "直接引语 + 宾语从句 + by doing",
        "With the right help 作条件背景；hope 后接 that 宾语从句；by installing bat houses 说明促进互利关系的方式。",
        [word("mutually beneficial", "adj.", "互利的"), word("bat house", "n.", "蝙蝠屋")],
    ),
    36: sentence(
        "Rocha and his colleagues believe that maximising bat populations can help to boost crop yields and promote sustainable livelihoods.",
        "罗查及其同事认为，尽可能扩大蝙蝠种群有助于提高作物产量，并促进可持续生计。",
        "宾语从句 + 动名词主语",
        "believe 后接 that 宾语从句；从句中 maximising bat populations 是动名词短语作主语；boost 与 promote 并列。",
        [word("crop yield", "n.", "作物产量"), word("sustainable livelihood", "n.", "可持续生计")],
    ),
}


P2_SPLITS = {
    5: sentence(
        "But, if you look back through history, there’s no evidence that having a high literacy rate made a country industrialise earlier.’",
        "但如果回顾历史，就会发现没有证据表明高识字率能使一个国家更早实现工业化。”",
        "条件状语从句 + There be + 同位语从句",
        "if 引导条件状语从句；主句是 there is no evidence；that 引导同位语从句，说明 evidence 的具体内容。",
        [word("literacy rate", "n.", "识字率"), word("industrialise", "v.", "实现工业化")],
    ),
    6: sentence(
        "Between 1600 and 1900, England had only mediocre literacy rates by European standards, yet its economy grew fast and it was the first country to industrialise.",
        "1600 至 1900 年间，按欧洲标准衡量，英格兰的识字率只能算一般，但其经济增长迅速，而且是第一个实现工业化的国家。",
        "转折并列句 + 不定式定语",
        "yet 连接识字率一般与经济增长迅速的反差；and 再并列 it was the first country；to industrialise 修饰 country。",
        [word("mediocre", "adj.", "平庸的；一般的"), word("by ... standards", "phr.", "按……标准")],
    ),
    15: sentence(
        "Ogilvie and her team have been building the vast database of material possessions on top of their full demographic reconstruction of the people who lived in these two German communities.",
        "奥格尔维及其团队在完整重建这两个德国社区人口资料的基础上，一直在建立庞大的物质财产数据库。",
        "现在完成进行时 + 定语从句",
        "主干是 Ogilvie and her team have been building the database；on top of 表示“在……基础上”；who lived ... 修饰 people。",
        [word("demographic", "adj.", "人口统计的"), word("reconstruction", "n.", "重建；复原")],
    ),
    16: sentence(
        "‘We can follow the same people – and their descendants – across 300 years of educational and economic change,’ she says.",
        "“我们可以追踪同一批人及其后代，了解他们经历的 300 年教育与经济变迁，”她说。",
        "直接引语 + 破折号插入",
        "引语主干是 We can follow the same people；破折号中的 and their descendants 补充追踪对象；across 300 years 交代时间跨度。",
        [word("descendant", "n.", "后代；后裔")],
    ),
}


def clone(old: list[dict], old_id: int, new_id: int, para: int, en: str | None = None) -> dict:
    row = deepcopy(old[old_id - 1])
    row["id"] = new_id
    row["para"] = para
    if en is not None:
        row["en"] = en
    return row


def make_row(spec: dict, sid: int, para: int) -> dict:
    return {"id": sid, "para": para, **deepcopy(spec)}


def rebuild_p1(data: dict) -> None:
    if len(data["sentences"]) == 39 and data["sentences"][0]["en"].startswith("There are few places"):
        return
    old = data["sentences"]
    if len(old) != 19 or not old[0]["en"].startswith("Rocha and his team used"):
        raise ValueError("c17-test4-p1 is not in the expected pre-repair state")

    rows = [make_row(spec, sid, para) for sid, (spec, para) in enumerate(
        zip(P1_MISSING, [1] * 6 + [2] * 5 + [3] + [4] * 2 + [5] * 3 + [6]), start=1
    )]
    mapping = {
        19: (1, 7), 20: (2, 7), 21: (3, 8), 22: (4, 8), 23: (5, 8), 24: (6, 8),
        25: (7, 9), 28: (9, 10), 29: (10, 11), 30: (11, 11), 31: (12, 11),
        32: (13, 11), 33: (14, 11), 34: (15, 11), 37: (17, 12), 38: (18, 12),
        39: (19, 12),
    }
    for sid in range(19, 40):
        if sid in P1_SPLITS:
            para = 9 if sid == 26 else 10 if sid == 27 else 11 if sid == 35 else 12
            rows.append(make_row(P1_SPLITS[sid], sid, para))
        else:
            old_id, para = mapping[sid]
            rows.append(clone(old, old_id, sid, para))
    data["sentences"] = rows


def rebuild_p2(data: dict) -> None:
    if len(data["sentences"]) == 39 and data["sentences"][0]["en"].startswith("Over the last decade"):
        return
    old = data["sentences"]
    if len(old) != 38 or old[0]["en"] != "Does education fuel economic growth?":
        raise ValueError("c17-test4-p2 is not in the expected pre-repair state")

    mapping = {
        1: 2, 2: 3, 3: 4, 4: 5,
        7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14,
        17: 16, 18: 17, 19: 18, 20: 19, 21: 20, 22: 21, 23: 22,
        24: 23, 25: 24, 26: 25, 27: 26, 28: 27, 29: 28, 30: 29,
        31: 30, 32: 31, 33: 32, 34: 33, 35: 34, 36: 35, 37: 36, 38: 37, 39: 38,
    }
    rows = []
    for sid in range(1, 40):
        para = 1 if sid <= 3 else 2 if sid <= 8 else 3 if sid <= 14 else 4 if sid <= 23 else 5 if sid <= 30 else 6
        if sid in P2_SPLITS:
            rows.append(make_row(P2_SPLITS[sid], sid, para))
        else:
            fixed_en = None
            if sid == 11:
                fixed_en = old[mapping[sid] - 1]["en"].replace("education- related", "education-related")
            rows.append(clone(old, mapping[sid], sid, para, fixed_en))
    data["sentences"] = rows


def paraphrase(pairs: list[tuple[str, str, str, str]], trap: str, explain: str) -> dict:
    return {
        "pairs": [{"q": q, "p": p, "kind": kind, "note": note} for q, p, kind, note in pairs],
        "trap": trap,
        "explain": explain,
    }


def apply_question_fixes(data: dict, fixes: dict[int, tuple[int, dict]]) -> None:
    items = {item["number"]: item for group in data.get("questions", []) for item in group.get("items", [])}
    if set(fixes) - set(items):
        raise ValueError(f"{data['id']} is missing questions {sorted(set(fixes) - set(items))}")
    for number, (evidence, analysis) in fixes.items():
        items[number]["evidence_sentence"] = evidence
        items[number]["paraphrase"] = analysis


def normalise_sentence_key_order(data: dict) -> None:
    """Keep generated JSON aligned with the repository's established schema order."""
    ordered = []
    preferred = ("id", "para", "en", "zh", "grammar", "words")
    for source in data["sentences"]:
        row = {key: source[key] for key in preferred}
        row.update({key: value for key, value in source.items() if key not in preferred})
        ordered.append(row)
    data["sentences"] = ordered


P1_QUESTIONS = {
    1: (4, paraphrase(
        [("forests are being destroyed by attacks from insects", "insect pests are destroying vast quantities of what is grown", "neg", "害虫直接毁坏的是农作物；随后是农民清林开田，并非昆虫直接袭击森林。")],
        "看到 insects 和 destruction 就选 TRUE，会忽略受害对象从 crops 被偷换成 forests。",
        "原文说明害虫毁坏作物，农民因此清除森林。题干却说森林被昆虫袭击而毁，因果链和受害对象均被改写错误，所以选 FALSE。")),
    2: (6, paraphrase(
        [("has badly affected", "are currently thriving", "neg", "题干称受到严重伤害，原文却说部分食虫蝙蝠目前繁衍兴旺。")],
        "上一句出现 habitat loss，但要继续读转折后的 not all species 和 thriving。",
        "原文明确说部分食虫蝙蝠并未受重创，反而正在兴旺，与题干相反，所以选 FALSE。")),
    3: (9, paraphrase(
        [("carried out studies of bats", "interested in how bats are responding to human activity and deforestation", "para", "原文交代罗查的研究兴趣，但没有说明他是否在世界不同地区做过研究。")],
        "不能把研究地点很多或研究兴趣广泛推断成“在世界不同地区研究过”。",
        "原文只介绍罗查研究蝙蝠如何应对人类活动和毁林，没有提供其全球研究经历，故选 NOT GIVEN。")),
    4: (15, paraphrase(
        [("becoming useful to farmers", "providing a valuable free service to Madagascar as biological pest suppressors", "para", "蝙蝠利用改变后的稻田栖息环境捕食害虫，为当地农业提供免费的生物防治服务。")],
        "useful 没有原词复现，而是由 free service 和 pest suppressors 具体说明。",
        "前文说明本土蝙蝠利用栖息地变化到稻田捕食昆虫，本句说明这种行为为农业提供宝贵服务，题干概括正确，选 TRUE。")),
    5: (14, paraphrase(
        [("The Malagasy mouse-eared bat", "They include the Malagasy mouse-eared bat", "verbatim", "原文只把鼠耳蝠列为其中一种，没有与其他本土蝙蝠比较数量或常见程度。")],
        "被列举不等于“比其他物种更常见”。",
        "原文列出四种蝙蝠，但没有任何物种数量或常见程度的比较，因此选 NOT GIVEN。")),
    6: (16, paraphrase(
        [("feed on", "preying on rice pests, including the paddy swarming caterpillar and grass webworm", "para", "prey on 与 feed on 同义，且两种害虫均被原文直接列出。")],
        "may 表示可能性，不要求原文说每只蝙蝠都一定捕食。",
        "原文明确发现六种蝙蝠捕食包括这两类在内的水稻害虫，题干一致，选 TRUE。")),
    7: (20, paraphrase(
        [("DNA analysis", "DNA barcoding techniques", "syn", "题目用概括说法，原文给出具体的 DNA 条形码技术。"), ("bat ___", "droppings collected from bats", "para", "分析对象是从蝙蝠处收集的粪便。")],
        "不要填 sites；sites 是采集地点，不是 DNA 分析的对象。",
        "原文为 analyse droppings collected from bats，且题目限填一词，因此答案是 droppings。")),
    8: (24, paraphrase(
        [("___", "coffee plants", "verbatim", "表格把作物名称 coffee plants 压缩为一词空格。")],
        "black twig borer 是害虫名称，题目要填的是它危害的作物。",
        "原文列出 black twig borer (which infests coffee plants)，与 rice、sugarcane、nuts、fruit 并列的作物是 coffee。")),
    9: (28, paraphrase(
        [("prevent the spread of disease by eating ___", "mosquitoes", "para", "原文说明蝙蝠吃携带多种疾病的蚊子。")],
        "malaria 等是疾病名称，blackflies 已在空格后给出。",
        "与 blackflies 并列、且会传播疾病的猎物是 mosquitoes。")),
    10: (30, paraphrase(
        [("food rich in ___", "source of protein", "para", "题目把“蛋白质来源”改写为“富含蛋白质的食物”。")],
        "source 是句型词，空格要填营养成分。",
        "原文说蝙蝠是当地人的 a crucial source of protein，故填 protein。")),
    11: (32, paraphrase(
        [("the buildings where they roost become ___", "make them unclean", "para", "them 指代 buildings，结果是建筑物变得 unclean。")],
        "不要把 not welcomed 填入；题目问建筑物变得怎样。",
        "原文直接说蝙蝠 make them unclean，限填一词，答案为 unclean。")),
    12: (33, paraphrase(
        [("play an important role in local ___", "very significant in the culture of the people", "para", "important role 对应 very significant，local 对应 of the people。")],
        "sacred caves 和 ancestors 是文化关联的具体内容，不是空格所需的上位概念。",
        "原文说蝙蝠在当地人的 culture 中非常重要，因此填 culture。")),
    13: (35, paraphrase(
        [("provide special ___", "installing bat houses", "para", "provide 对应 installing，special facilities 对应 bat houses。")],
        "题目限填一词，不能填写 bat houses 两个词。",
        "原文建议农民安装 bat houses；空格前已有 special，故只填 houses。")),
}


P2_QUESTIONS = {
    14: (26, paraphrase(
        [("individuals with a fairly consistent income", "different people with the same level of wealth over a period of time", "para", "consistent income 被研究设计中的 same level of wealth 概括。")],
        "题目用 income，原文用更宽泛的 wealth，并以 hold wealth constant 描述方法。",
        "E 段解释要控制财富水平不变，再追踪不同个体，正是题干所述研究需要，答案为 E。")),
    15: (2, paraphrase(
        [("sources the database has been compiled from", "court records, guild ledgers, parish registers, village censuses, tax lists", "para", "原文连续列出数据库所用档案来源。")],
        "不要把后文的 possessions 当作数据库来源；那是某类清单里的内容。",
        "A 段列举 court records、guild ledgers、parish registers 等资料来源，答案为 A。")),
    16: (21, paraphrase(
        [("refusal to obey an order", "continued taking jobs reserved for male guild members", "para", "continued 表明 Juliana 在受斥责后仍继续违反行会规定。")],
        "关键不是第一次被 reprimanded，而是之后 continued，体现拒绝服从。",
        "D 段叙述 Juliana 被斥责后仍继续接只留给男性会员的工作，答案为 D。")),
    17: (33, paraphrase(
        [("a region being particularly suited to research", "German-speaking central Europe is an excellent laboratory for testing theories of economic growth", "para", "excellent laboratory 表示该地区特别适合用来检验理论。")],
        "laboratory 在这里是比喻，不是实际实验室。",
        "F 段明确称德语区中欧是检验经济增长理论的 excellent laboratory，答案为 F。")),
    18: (10, paraphrase(
        [("items included in a list of personal possessions", "badger skins to Bibles, sewing machines to scarlet bodices", "para", "原文列举个人财产清单中的具体物品。")],
        "A 段列的是档案种类；C 段才列个人物品。",
        "C 段列出獾皮、圣经、缝纫机和猩红色紧身胸衣，答案为 C。")),
    19: (16, paraphrase(
        [("as well as those of their ___", "their descendants", "verbatim", "their descendants 直接对应空格。"), ("over a 300-year period", "across 300 years", "syn", "时间范围同义改写。")],
        "same people 与 descendants 是两组并列追踪对象，空格填后者。",
        "原文是 follow the same people – and their descendants – across 300 years，故填 descendants。")),
    20: (18, paraphrase(
        [("reprimanded for reading", "chastised in 1707 for reading books in church instead of listening to the sermon", "para", "reprimanded 对应 chastised，paying attention 对应 listening。")],
        "church 是地点，题目问她们本该听什么。",
        "原文说她们读书而没有听 sermon，因此填 sermon。")),
    21: (21, paraphrase(
        [("given a ___ as a punishment", "told to pay a fine", "para", "惩罚方式是缴纳罚款。")],
        "one third of a servant’s annual wage 是罚款额度，不是答案。",
        "原文明确 told to pay a fine，限填一词，答案为 fine。")),
    22: (23, paraphrase(
        [("prevent ___", "held back even the simplest industrial innovation", "para", "prevent 对应 held back，空格对应 innovation。")],
        "同句前半部分 already 对应 stop skilled people from working；空格应取后半部分。",
        "行会既阻止人们使用技能，也阻碍 industrial innovation，故填 innovation。")),
    23: (7, paraphrase(
        [("literacy rates in Germany ... were very good", "Germany and Scandinavia had excellent literacy rates", "para", "very good 对应 excellent。")],
        "题目问作者在 B 段作出的陈述，不是问识字率是否带来增长。",
        "B 段明确说德国和斯堪的纳维亚识字率 excellent，所以选 B。")),
    24: (8, paraphrase(
        [("Economic growth can help to improve literacy rates", "growth increases education", "para", "improve literacy rates 是 increases education 的具体化表达。")],
        "注意因果方向：原文否定“教育导致增长”的证据充分，却说“增长促进教育”的证据很多。",
        "B 段明确写 there is plenty of evidence that growth increases education，所以选 E。")),
    25: (36, paraphrase(
        [("opposed to people moving to an area for work", "blocked labour migration", "para", "people moving for work 对应 labour migration，opposed 对应 blocked。")],
        "migration 在这里是劳动力流动，不只是跨国移民。",
        "F 段说行会 blocked labour migration，因此选 B。")),
    26: (35, paraphrase(
        [("opposed practices that threatened their control over a trade", "legislated against anything that undermined their monopolies", "para", "threatened control 对应 undermined monopolies。")],
        "merchant associations 与 guilds 并列，但题目概括的是它们维护垄断控制的共同做法。",
        "F 段说明行会和商人协会立法反对任何削弱其垄断的事物，因此选 D。")),
}


P3_QUESTION_FIXES = {
    29: (42, paraphrase(
        [("skill is limited to chess", "didn’t find anything other than playing chess that he seems to be supremely gifted at", "para", "other than playing chess 表明未发现他在其他标准任务上有同等天赋。")],
        "not exceptional on standard tests 是前句概括，后句更直接限定其突出天赋只在国际象棋。",
        "F 段研究者说除下棋外没有发现他特别擅长的事，答案为 F。")),
    30: (12, paraphrase(
        [("why Gareyev’s skill is of interest to scientists", "In the hope of understanding how he and others like him can perform such mental feats", "para", "科学家研究他，是为了理解这种非凡脑力表现如何实现。")],
        "beyond the chess-playing community 只说明兴趣超出棋坛，下一句才交代科学研究目的。",
        "B 段说明 UCLA 研究者希望理解这种 mental feats 的机制，所以答案为 B。")),
    36: (14, paraphrase(
        [("Good chess players are likely to be able to play blindfold chess", "not a far reach for most accomplished players", "para", "not a far reach 表示对大多数高水平棋手并非难以企及。")],
        "题干的 likely 并非说人人一定能做到，而是概括 most accomplished players。",
        "原文明确说闭眼下棋对多数高水平棋手并非遥不可及，题干一致，选 TRUE。")),
}


def save(data: dict) -> None:
    path = PASSAGES / f"{data['id']}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    p1 = json.loads((PASSAGES / "c17-test4-p1.json").read_text(encoding="utf-8"))
    p2 = json.loads((PASSAGES / "c17-test4-p2.json").read_text(encoding="utf-8"))
    p3 = json.loads((PASSAGES / "c17-test4-p3.json").read_text(encoding="utf-8"))

    rebuild_p1(p1)
    rebuild_p2(p2)
    normalise_sentence_key_order(p1)
    normalise_sentence_key_order(p2)
    apply_question_fixes(p1, P1_QUESTIONS)
    apply_question_fixes(p2, P2_QUESTIONS)
    apply_question_fixes(p3, P3_QUESTION_FIXES)

    save(p1)
    save(p2)
    save(p3)

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    counts = {p["id"]: len(p["sentences"]) for p in (p1, p2, p3)}
    for row in index.get("passages", []):
        if row.get("id") in counts:
            row["sentence_count"] = counts[row["id"]]
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("repaired c17-test4 passages:", ", ".join(f"{pid}={count}" for pid, count in counts.items()))


if __name__ == "__main__":
    main()
