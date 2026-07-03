"""Teacher-refine Cambridge IELTS 17 Test 4 Passage 1 — Bats to the rescue."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test4-p1.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


PHRASES = [
    w("insectivorous bats", "n.", "食虫蝙蝠"),
    w("pest control service", "n.", "害虫防治服务"),
    w("habitat modification", "n.", "栖息地改变"),
    w("ultrasonic recorders", "n.", "超声波记录仪"),
    w("feeding buzzes", "n.", "捕食嗡鸣（蝙蝠锁定猎物时发出的回声定位声）"),
    w("DNA barcoding", "n.", "DNA 条形码技术"),
    w("mutually beneficial relationship", "n.", "互利关系"),
    w("bat houses", "n.", "蝙蝠屋（供蝙蝠栖息的人工装置）"),
    w("state-of-the-art", "adj.", "最先进的"),
    w("run-off", "n.", "（水、养分等的）流失、径流"),
    w("insect pest", "n.", "害虫"),
    w("as well as", "phr.", "以及；除……之外"),
    w("not just ... but also ...", "phr.", "不仅……而且……"),
]


# 句id -> (zh, grammar.type, grammar.note, [words])
REFINED = {
    1: (
        "罗查和他的团队使用最先进的超声波记录仪，在 54 个地点录制了一千多段蝙蝠的“捕食嗡鸣”（即蝙蝠用来锁定猎物的回声定位声），以此确定这些蝙蝠最青睐的觅食地点。",
        "主干句 + 目的状语 + 插入语",
        "主干是 Rocha and his team used ... recorders to record ... buzzes；括号内 echolocation sequences ... 是对 'feeding buzzes' 的同位解释；in order to identify ... 作目的状语，说明录音的用途。",
        [w("state-of-the-art", "adj.", "最先进的"), w("feeding buzzes", "n.", "捕食嗡鸣")],
    ),
    2: (
        "随后，他们又采用 DNA 条形码技术，分析从各个地点的蝙蝠身上采集到的粪便。",
        "主干句 + 过去分词后置定语",
        "主干是 They used DNA barcoding techniques；to analyse droppings 作目的状语；collected from bats at the different sites 是过去分词短语，后置修饰 droppings，相当于一个省略了 which were 的定语从句。",
        [w("droppings", "n.", "（动物的）粪便"), w("DNA barcoding", "n.", "DNA 条形码技术")],
    ),
    3: (
        "录音显示，稻田上空的蝙蝠活动远远高于连绵森林中——平地稻田上空高出七倍，山坡田地上空更高出十六倍——这毫无疑问地表明，这些动物更偏爱在这些人造生态系统中觅食。",
        "宾语从句 + 破折号插入 + 分词结果状语",
        "主干是 The recordings revealed that ...；破折号之间 seven times higher ... and sixteen times higher ... 是对倍数的具体补充；句尾 leaving no doubt that ... 是现在分词短语作结果状语，得出结论。",
        [w("continuous forest", "n.", "连绵不断的森林"), w("forage", "v.", "觅食")],
    ),
    4: (
        "研究人员认为，蝙蝠之所以偏爱这些田地，是因为缺水和养分流失使这些作物更容易遭受虫害。",
        "宾语从句 + because 原因从句",
        "主干是 The researchers suggest that ...；that 从句里又套一个 because 原因状语从句，解释 favour 的原因；lack of water and nutrient run-off 是并列主语，make 是使役动词。",
        [w("susceptible", "adj.", "易受影响的；易感染的"), w("infestation", "n.", "（害虫等的）侵扰、大量滋生")],
    ),
    5: (
        "DNA 分析表明，全部六种蝙蝠都取食过在经济上举足轻重的害虫。",
        "宾语从句 + 过去完成时",
        "主干是 DNA analysis showed that ...；从句用 had fed on 过去完成时，表示取食发生在分析之前；economically important 修饰 insect pests，是题目常见的改写点。",
        [w("economically", "adv.", "在经济上"), w("feed on", "phr.", "以……为食")],
    ),
    6: (
        "虽然研究结果显示水稻种植从蝙蝠身上获益最大，但科学家们也发现有迹象表明，蝙蝠还在取食其他作物的害虫，包括黑枝小蠹（侵害咖啡树）、甘蔗蝉、澳洲坚果蛀虫，以及清醒虎斑虫（一种柑橘类害虫）。",
        "While 让步从句 + 同位语从句 + including 列举",
        "While 引导让步状语从句；主句是 the scientists also found indications；that the bats were consuming ... 是 indications 的同位语从句；including 后是并列的害虫名称列举，括号内各自补充说明其危害对象。",
        [w("consume", "v.", "吃掉；消耗"), w("infest", "v.", "（害虫等）大量出没、侵扰")],
    ),
    7: (
        "“蝙蝠作为害虫防治者的成效，已经在美国和加泰罗尼亚得到证实，”来自里斯本大学的论文合著者詹姆斯·肯普说。",
        "直接引语 + 现在完成被动",
        "引号内 The effectiveness ... has already been proven 是现在完成时的被动语态，强调“已被证实”；主句谓语 said 后倒装出主语 co-author James Kemp；from the University of Lisbon 补充其身份。",
        [w("effectiveness", "n.", "成效；有效性"), w("pest controller", "n.", "害虫防治者")],
    ),
    8: (
        "“但我们的研究首次证实了这一现象正发生在马达加斯加——在那里，农民和生态保护者双方的利害关系都极其重大。”当地人或许还有另一个理由感激这些蝙蝠。",
        "直接引语（含定语从句）+ 独立陈述句",
        "引语主干是 our study is the first to show this happening；where 引导非限制性定语从句，补充 Madagascar 的背景。引语结束后是独立的一句 Local people may have a further reason ...，为下一段的主旨句。",
        [w("stakes", "n.", "利害关系；风险"), w("grateful", "adj.", "感激的")],
    ),
    9: (
        "尽管这种动物常被认为会传播疾病，罗查和他的团队却发现证据表明，马达加斯加的蝙蝠不仅取食农作物害虫，还捕食蚊子（疟疾、裂谷热病毒和象皮病的传播媒介），以及传播河盲症的黑蝇。",
        "While 让步从句 + 同位语从句 + 破折号插入",
        "While 引导让步从句；主句是 Rocha and his team found evidence；that Malagasy bats feed ... 是 evidence 的同位语从句，内部用 not just ... but also ... 并列；破折号之间 carriers of ... 补充说明 mosquitoes；句尾 which spread river blindness 修饰 blackflies。",
        [w("carrier", "n.", "（疾病的）携带者、传播媒介"), w("not just ... but also ...", "phr.", "不仅……而且……")],
    ),
    10: (
        "罗查指出，这种关系其实相当复杂。",
        "宾语从句",
        "主干是 Rocha points out that ...；that 从句作 points out 的宾语，complicated 作表语，点明下文将展开的“复杂性”。",
        [w("point out", "phr.", "指出"), w("complicated", "adj.", "复杂的")],
    ),
    11: (
        "当食物匮乏时，蝙蝠便成为当地人重要的蛋白质来源。",
        "When 时间状语从句",
        "When food is scarce 是时间状语从句，交代条件；主句是 bats become a crucial source of protein；a source of protein 对应表格题的填空信息 protein。",
        [w("scarce", "adj.", "稀缺的；匮乏的"), w("crucial", "adj.", "至关重要的")],
    ),
    12: (
        "就连孩子们也会去捕猎它们。",
        "简单句（Even 强调）",
        "结构简单：主语 the children，谓语 will hunt，宾语 them（指蝙蝠）；句首 Even 起强调作用，突出连小孩都会捕猎，暗示当地人取食蝙蝠之普遍。",
        [w("hunt", "v.", "捕猎"), w("even", "adv.", "甚至（表强调）")],
    ),
    13: (
        "而且蝙蝠除了栖息在树上，有时也栖身于建筑物内，但在那里并不受欢迎，因为人们认为它们弄脏了这些建筑。",
        "as well as 并列 + but 转折 + because 原因从句",
        "as well as roosting in trees 是介词短语作状语，与 roost in buildings 形成对比；but 转折出 are not welcomed；because they make them unclean 说明不受欢迎的原因，两个 them 分别指“建筑”和“蝙蝠”。",
        [w("roost", "v./n.", "栖息；栖息处"), w("unclean", "adj.", "不洁的；肮脏的")],
    ),
    14: (
        "然而与此同时，蝙蝠又与神圣的洞穴和祖先联系在一起，因而被视为游走于两个世界之间的生灵，这使它们在当地人的文化中地位极为重要。",
        "so 结果连接 + which 非限制性定语从句",
        "主干是 they are associated with sacred caves and the ancestors；so 引出结果 they can be viewed as beings between worlds；句尾 which makes them very significant ... 是非限制性定语从句，指代前面整个内容，对应表格题的 culture。",
        [w("sacred", "adj.", "神圣的"), w("significant", "adj.", "重要的；意义重大的")],
    ),
    15: (
        "还有一个潜在问题：尽管这些蝙蝠正从农业中获益，但与此同时，森林砍伐正在减少它们可供栖息的场所，这可能对其种群数量产生长期影响。",
        "表语从句 + while 让步 + which 定语从句",
        "主干是 one potential problem is that ...；that 表语从句里 while 引导让步状语从句；主句是 deforestation is reducing the places；where they can roost 修饰 places；句尾 which could have long-term effects ... 指代前面整件事。",
        [w("deforestation", "n.", "森林砍伐"), w("long-term", "adj.", "长期的")],
    ),
    16: (
        "罗查说：“只要给予恰当的扶持，我们希望农民能通过安装蝙蝠屋来促进这种互利关系。”罗查和同事们相信，尽可能扩大蝙蝠种群，有助于提高作物产量、促进可持续的生计。",
        "直接引语 + 动名词主语宾语从句",
        "引语内 With the right help 作条件状语，主干是 we hope that farmers can promote ...，by installing bat houses 作方式状语。引语后是独立一句：宾语从句里 maximising bat populations 是动名词短语作主语，can help to boost ... and promote ... 为并列谓语。",
        [w("promote", "v.", "促进；推动"), w("sustainable", "adj.", "可持续的")],
    ),
    17: (
        "研究团队目前正呼吁开展进一步研究，以量化这一贡献。",
        "主干句 + 不定式目的状语",
        "主干是 The team is now calling for further research；to quantify this contribution 是不定式短语作目的状语，说明呼吁研究的意图；is now calling for 现在进行时强调当下正在进行。",
        [w("call for", "phr.", "呼吁；要求"), w("quantify", "v.", "量化；用数据说明")],
    ),
    18: (
        "“我非常乐观，”罗查说。",
        "直接引语 + 倒装",
        "引号内 I'm very optimistic 是完整的主系表结构；主句 says Rocha 采用主谓倒装，是引述时的常见写法。",
        [w("optimistic", "adj.", "乐观的")],
    ),
    19: (
        "“只要我们助大自然一臂之力，就能加快其自我恢复的进程。”",
        "If 条件状语从句",
        "If we give nature a hand 是条件状语从句，give ... a hand 是习语，意为“帮一把”；主句是 we can speed up the process of regeneration，regeneration 呼应全文“森林再生/恢复”的主题。",
        [w("give ... a hand", "phr.", "帮……一把"), w("regeneration", "n.", "再生；（生态的）恢复")],
    ),
}


EN_FIX = {
    # 删除黏进第 1 句的标题/副标题/题目说明/页眉乱码，只保留正文首句。
    1: (
        "Rocha and his team used state-of-the-art ultrasonic recorders to record over "
        "a thousand bat ‘feeding buzzes’ (echolocation sequences used by bats "
        "to target their prey) at 54 sites, in order to identify the favourite feeding "
        "spots of the bats."
    ),
}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    data["quality"] = "teacher_refined"
    data["phrases"] = PHRASES

    missing = [s["id"] for s in data["sentences"] if s["id"] not in REFINED]
    if missing:
        raise SystemExit(f"REFINED missing sentence ids: {missing}")

    for s in data["sentences"]:
        if s["id"] in EN_FIX:
            s["en"] = EN_FIX[s["id"]]
        zh, gtype, note, words = REFINED[s["id"]]
        s["zh"] = zh
        s["grammar"] = {"type": gtype, "note": note}
        s["words"] = words

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if INDEX.exists():
        idx = json.loads(INDEX.read_text(encoding="utf-8"))
        for row in idx.get("passages", []):
            if row.get("id") == data["id"]:
                row["quality"] = "teacher_refined"
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"refined {PATH}")


if __name__ == "__main__":
    main()
