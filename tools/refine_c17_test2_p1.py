"""Teacher-refine Cambridge IELTS 17 Test 2 Passage 1 — The Dead Sea Scrolls.

Notes on structure changes (see report):
- EN fix on sentence 1: strip the leading title "The Dead Sea Scrolls ".
- Sentence 16 in the draft merged TWO real sentences with a stray page number "2":
  (a) "Along with biblical texts, ... Old Testament." and
  (b) "The writing on the Dead Sea Scrolls is mostly ... called 'papyrus'."
  These are split into two sentences, so the passage grows from 32 -> 33 sentences.
  All ids >= 17 are shifted +1; index.json sentence_count and the one affected
  question evidence_sentence (28 -> 29) are updated accordingly.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test2-p1.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


PHRASES = [
    w("the Dead Sea Scrolls", "phr.", "死海古卷"),
    w("stumble across", "phr.", "偶然发现"),
    w("antiquities dealer", "phr.", "古董商"),
    w("make up", "phr.", "构成；组成"),
    w("the subject of debate", "phr.", "争论的话题"),
    w("be thought to", "phr.", "被认为……"),
    w("fall out of use", "phr.", "不再使用；被废弃"),
    w("the Old Testament", "phr.", "（圣经）旧约"),
    w("still in existence", "phr.", "现存的；仍存在的"),
    w("the Copper Scroll", "phr.", "铜卷"),
    w("the passage of time", "phr.", "时间的流逝"),
    w("date back to", "phr.", "可追溯到"),
    w("provide insight into", "phr.", "让人深入了解"),
    w("piece together / reassemble", "phr.", "拼合；重新组装"),
]


# Corrected English (only where the draft text was wrong).
EN_FIX = {
    1: "In late 1946 or early 1947, three Bedouin teenagers were tending their goats and sheep near the ancient settlement of Qumran, located on the northwest shore of the Dead Sea in what is now known as the West Bank.",
    # Old id 16 -> split. Keep only the first real sentence here; the papyrus
    # sentence moves to a new sentence inserted after it (see NEW_SENTENCE).
    16: "Along with biblical texts, the scrolls include documents about sectarian regulations and religious writings that do not appear in the Old Testament.",
}


# The new sentence to insert directly after old id 16 (the "papyrus" sentence
# that had been glued onto the end of sentence 16). It becomes the new id 17;
# every original sentence from old id 17 onward shifts up by one.
NEW_SENTENCE_EN = (
    "The writing on the Dead Sea Scrolls is mostly in black or occasionally red ink, "
    "and the scrolls themselves are nearly all made of either parchment (animal skin) "
    "or an early form of paper called 'papyrus'."
)
NEW_SENTENCE_PARA = 3
NEW_SENTENCE_REFINED = (
    "死海古卷上的文字大多是黑色墨水，偶尔也用红色墨水；卷轴本身则几乎全部由羊皮纸（动物皮）或一种被称为“纸莎草”（papyrus）的早期纸张制成。",
    "并列句 + 分号连接",
    "分号连接两个并列分句：前句主干是 The writing ... is ... in ink，后句主干是 the scrolls ... are ... made of ...；either ... or ... 给出两种材质，made of 表“由……制成”。",
    [w("parchment", "n.", "羊皮纸"), w("papyrus", "n.", "纸莎草（纸）")],
)


# REFINED keyed by the sentence's ORIGINAL draft id.
# (zh, grammar type, grammar note, words)
REFINED = {
    1: ("1946 年底或 1947 年初，三名贝都因少年正在死海西北岸——如今被称为约旦河西岸——的古代聚落库姆兰附近放牧羊群。", "过去分词短语作后置定语", "主干是 three Bedouin teenagers were tending their goats and sheep；located on ... 是过去分词短语，作 Qumran 的后置定语；in what is now known as the West Bank 是 what 引导的名词性从句作介词 in 的宾语。", [w("tend", "v.", "照料；照看（牲畜）"), w("settlement", "n.", "聚落；定居点")]),
    2: ("其中一名年轻的牧羊人把一块石头扔进悬崖边的一个洞口，惊讶地听到了东西破碎的声音。", "并列谓语 + 不定式作状语", "主语 One of these young shepherds 带两个并列谓语 tossed 与 was surprised；to hear a shattering sound 是不定式，说明惊讶的原因/内容。", [w("toss", "v.", "扔；抛"), w("shattering", "adj.", "破碎的；令人震惊的")]),
    3: ("后来，他和同伴进入洞穴，无意中发现了一批大陶罐，其中有七个装着写有文字的卷轴。", "非限制性定语从句（介词 + which）", "主干是 He and his companions ... entered ... and stumbled across a collection of large clay jars；seven of which ... 是“数词 + of which”引导的非限制性定语从句，补充说明 jars。", [w("stumble across", "phr.", "偶然发现"), w("clay jar", "n.", "陶罐")]),
    4: ("这些少年把七卷卷轴带到附近一座城镇，在那里以很少的一笔钱卖给了当地一位古董商。", "where 引导定语从句 + 被动语态", "主干是 The teenagers took the seven scrolls to a nearby town；where they were sold ... 是 where 引导的定语从句修饰 town，从句内 were sold 是被动语态。", [w("for a small sum", "phr.", "以一小笔钱"), w("antiquities dealer", "phr.", "古董商")]),
    5: ("这一发现的消息传开后，贝都因人和考古学家最终又从附近 10 个洞穴中挖出了数以万计的卷轴残片；这些残片合起来构成了 800 到 900 份手稿。", "并列句 + 分号补充", "分号前是 and 连接的两个并列分句（Word ... spread 与 Bedouins and archaeologists ... unearthed ...）；分号后 together they make up ... 补充说明残片汇总后的数量。", [w("unearth", "v.", "挖掘出；发掘"), w("make up", "phr.", "构成；组成")]),
    6: ("很快人们就清楚地认识到，这是有史以来最伟大的考古发现之一。", "it 形式主语 + that 主语从句", "It 是形式主语，真正主语是 that this was one of the greatest archaeological discoveries ever made；ever made 是过去分词短语修饰 discoveries，表“迄今做出的”。", [w("archaeological", "adj.", "考古的"), w("discovery", "n.", "发现")]),
    7: ("死海古卷写于大约 2000 年前的公元前 150 年至公元 70 年之间，其起源至今仍是学术界争论的话题。", "非限制性定语从句插入主干", "主干是 The origin ... is still the subject of scholarly debate；which were written ... 70 CE 是插入在主谓之间的非限制性定语从句，补充说明 the Dead Sea Scrolls 的成书年代。", [w("origin", "n.", "起源"), w("scholarly", "adj.", "学术的；学者的")]),
    8: ("根据主流理论，它们出自一群人之手——这群人一直居住在该地区，直到公元 70 年前后罗马军队摧毁了这处聚落。", "定语从句 + until 时间状语从句", "主干是 they are the work of a population；that inhabited the area ... 是定语从句修饰 population，从句内又含 until 引导的时间状语从句 until Roman troops destroyed the settlement。", [w("prevailing", "adj.", "占主导的；流行的"), w("inhabit", "v.", "居住于")]),
    9: ("那时该地区被称为犹地亚（Judea），人们认为这些居民属于一个名为艾赛尼派（Essenes）的群体，那是一个虔诚的犹太教派。", "并列句 + 同位语", "and 连接两个分句；后一分句主干是 the people are thought to have belonged to a group，are thought to have belonged 是“被认为曾属于”；a devout Jewish sect 是 the Essenes 的同位语。", [w("be thought to", "phr.", "被认为……"), w("devout", "adj.", "虔诚的")]),
    10: ("死海古卷上的文字大多是希伯来文，其中一些残片用的是这种字母表的古老版本，据信这种字母在公元前五世纪就已不再使用。", "with 复合结构 + 过去分词定语", "主干是 The majority of the texts ... are in Hebrew；with some fragments written ... 是 with 复合结构表伴随；thought to have fallen out of use ... 是过去分词短语修饰 version。", [w("fall out of use", "phr.", "不再使用；被废弃"), w("alphabet", "n.", "字母表")]),
    11: ("但除此之外还有其他语言。", "There be 句型", "简单的 There be 句型；as well 相当于 too，强调“除希伯来文外也有别的语言”，But 承接上句作转折。", [w("as well", "phr.", "也；同样")]),
    12: ("有些卷轴用的是阿拉姆语——从公元前六世纪到公元 70 年耶路撒冷被围城期间，该地区许多居民都讲这种语言。", "同位语 + 过去分词后置定语", "主干是 Some scrolls are in Aramaic；the language spoken by ... 是 Aramaic 的同位语，spoken by many inhabitants ... 是过去分词短语作 the language 的后置定语。", [w("inhabitant", "n.", "居民"), w("siege", "n.", "围攻；围城")]),
    13: ("此外，还有若干文本收录了希伯来文《圣经》的希腊文译本。", "主谓宾结构 + In addition 承接", "主干是 several texts feature translations；of the Hebrew Bible into Greek 说明译本的方向（把希伯来文《圣经》译成希腊文）；In addition 表递进补充。", [w("feature", "v.", "以……为特色；收录"), w("translation", "n.", "译本；翻译")]),
    14: ("死海古卷包含《圣经·旧约》中除《以斯帖记》外每一卷书的残片。", "主谓宾 + except for 排除", "主干是 The Dead Sea Scrolls include fragments；from every book of the Old Testament 说明残片来源；except for the Book of Esther 用 except for 表“唯独排除”。", [w("except for", "phr.", "除……之外"), w("the Old Testament", "phr.", "（圣经）旧约")]),
    15: ("库姆兰手稿中唯一完整保存下来的希伯来文《圣经》书卷是《以赛亚书》；这份抄本可追溯到公元前一世纪，被认为是现存最早的《圣经》手稿。", "分号并列 + 过去分词后置定语", "分号连接两句。前句主干是 The only entire book ... is Isaiah，preserved among ... 是过去分词短语修饰 book；后句主干是 this copy ... is considered ...，dated to the first century BCE 作插入的过去分词修饰 copy。", [w("preserve", "v.", "保存；保留"), w("still in existence", "phr.", "现存的")]),
    # id 16 keeps only the first sentence after EN_FIX.
    16: ("除《圣经》文本外，这些卷轴还包含一些关于教派规章的文件以及《旧约》中没有的宗教著作。", "along with 引导 + 定语从句", "主干是 the scrolls include documents ... and religious writings；Along with biblical texts 是介词短语作状语；that do not appear in the Old Testament 是定语从句修饰 religious writings。", [w("sectarian", "adj.", "教派的；宗派的"), w("regulation", "n.", "规章；条例")]),
    17: ("唯一的例外是编号为 3Q15 的卷轴，它由铜和锡的合金制成。", "非限制性定语从句", "主干是 The only exception is the scroll；numbered 3Q15 是过去分词短语修饰 scroll；which was created out of ... 是非限制性定语从句，补充说明其材质。", [w("exception", "n.", "例外"), w("a combination of", "phr.", "……的组合")]),
    18: ("这份卷轴被称为“铜卷”，其特点是把字母凿刻在金属上——正如一些人所推测的，也许是为了更好地抵御时间的侵蚀。", "过去分词短语作状语 + 目的状语", "Known as the Copper Scroll 是过去分词短语作状语；主干是 this curious document features letters；chiselled onto metal 修饰 letters；破折号后 to better withstand ... 是不定式表目的，as some have theorized 为插入语。", [w("chisel", "v.", "凿；雕刻"), w("withstand", "v.", "抵御；经受住")]),
    19: ("作为库姆兰最引人入胜的手稿之一，它像是一张古代藏宝图，列出了数十处金银窖藏。", "同位语前置 + 定语从句", "句首 One of the most intriguing manuscripts from Qumran 是同位语，指代主语 this；主干是 this is a sort of ancient treasure map；that lists ... 是定语从句修饰 map。", [w("intriguing", "adj.", "引人入胜的；耐人寻味的"), w("cache", "n.", "（隐藏物的）窖藏；贮藏处")]),
    20: ("它使用非常规的词汇和古怪的拼写，描述了 64 个据说藏有为妥善保存而埋下的财宝的地下藏匿点。", "现在分词作状语 + 定语从句", "Using an unconventional vocabulary and odd spelling 是现在分词短语作方式状语；主干是 it describes 64 underground hiding places；that supposedly contain riches ... 是定语从句修饰 hiding places，buried for safekeeping 修饰 riches。", [w("unconventional", "adj.", "非常规的"), w("safekeeping", "n.", "妥善保管")]),
    21: ("这些窖藏无一被找回，很可能是因为罗马人在公元一世纪劫掠了犹地亚。", "现在完成时被动 + because 原因状语从句", "主干是 None of these hoards have been recovered，为现在完成时的被动语态；possibly because ... 是 because 引导的原因状语从句，possibly 表推测语气。", [w("hoard", "n.", "（贮藏的）大量财物"), w("pillage", "v.", "劫掠；抢劫")]),
    22: ("按照各种不同的假说，这些财宝或属于当地人，或在第二圣殿被毁前被抢救出来，又或者从一开始就根本不存在。", "三重并列谓语（or 连接）", "主语 the treasure 后接三个由 or 连接的并列谓语：belonged to ... / was rescued ... / never existed ...；before its destruction 是时间状语，to begin with 意为“一开始；本来”。", [w("hypothesis", "n.", "假说；假设（复数 hypotheses）"), w("to begin with", "phr.", "起初；一开始")]),
    23: ("有些死海古卷经历了一番有趣的辗转。", "现在完成时主谓结构", "主干是 Some of the Dead Sea Scrolls have been on interesting journeys；have been on journeys 用现在完成时，比喻这些卷轴的流转经历，起到本段总起句的作用。", [w("journey", "n.", "旅程；（此处喻）辗转经历")]),
    24: ("1948 年，一位名叫马尔·塞缪尔（Mar Samuel）的叙利亚东正教大主教从耶路撒冷一位兼做古董生意的鞋匠手中，以不到 100 美元的价格买下了最初七卷中的四卷。", "现在分词短语作结果状语", "主干是 a Syrian Orthodox archbishop ... acquired four of the original seven scrolls；known as Mar Samuel 是过去分词短语修饰 archbishop；paying less than $100 for them 是现在分词短语，说明伴随/结果。", [w("acquire", "v.", "获得；购得"), w("archbishop", "n.", "大主教")]),
    25: ("随后他前往美国，向包括耶鲁大学在内的多所大学兜售这些卷轴，但未能成功。", "并列谓语 + 副词否定", "主干是 He ... travelled ... and ... offered them ...，两个谓语由 and 连接；unsuccessfully 是副词，前置强调“兜售未果”；including Yale 举例说明 universities。", [w("offer", "v.", "提供；（此处）兜售"), w("including", "prep.", "包括")]),
    26: ("最终，在 1954 年，他在商业报纸《华尔街日报》上——在“杂项待售”栏目下——登了一则广告，广告写道：“现有可追溯到至少公元前 200 年的《圣经》手稿出售。", "定语从句 + 直接引语", "主干是 he placed an advertisement；破折号中的 under the category ... 是插入的介词短语；that read: ... 是定语从句修饰 advertisement，read 在此意为“（文字）写着”，冒号后引出广告原文。", [w("advertisement", "n.", "广告"), w("date back to", "phr.", "可追溯到")]),
    27: ("这将是个人或团体馈赠给教育或宗教机构的理想礼物。”所幸，以色列考古学家兼政治家伊盖尔·亚丁（Yigael Yadin）出面谈成了这笔收购，把这些卷轴带回了耶路撒冷，它们至今仍留存于此。", "引语收尾 + where 定语从句", "前半句是广告引语的结尾；后半句主干是 Yigael Yadin negotiated their purchase and brought the scrolls back to Jerusalem；where they remain to this day 是 where 引导的定语从句修饰 Jerusalem。", [w("negotiate", "v.", "（通过谈判）达成；商定"), w("statesman", "n.", "政治家")]),
    28: ("2017 年，海法大学的研究人员修复并破译了最后几份尚未翻译的卷轴之一。", "并列谓语主谓宾结构", "主干是 researchers ... restored and deciphered one of the last untranslated scrolls，restored 与 deciphered 是并列谓语；untranslated 是过去分词作定语，表“尚未翻译的”。", [w("restore", "v.", "修复；复原"), w("decipher", "v.", "破译；解读")]),
    29: ("该校的埃什巴尔·拉特森（Eshbal Ratson）和乔纳森·本-多夫（Jonathan Ben-Dov）花了一年时间重新拼合构成这份卷轴的 60 块残片。", "定语从句修饰宾语", "主干是 Eshbal Ratson and Jonathan Ben-Dov spent one year reassembling the 60 fragments；spent ... doing 表“花时间做某事”；that make up the scroll 是定语从句修饰 fragments。", [w("reassemble", "v.", "重新拼合；重新组装"), w("fragment", "n.", "残片；碎片")]),
    30: ("这份卷轴是从羊皮纸上一段编码文字中破译出来的，它让人得以深入了解书写者所属的群体，以及他们当时可能使用的 364 天历法。", "过去分词短语作状语 + 定语从句", "Deciphered from a band of coded text on parchment 是过去分词短语作状语；主干是 the find provides insight into the community ... and the ... calendar；who wrote it 与 they would have used 分别是修饰 community 和 calendar 的定语从句。", [w("provide insight into", "phr.", "让人深入了解"), w("coded", "adj.", "编码的；用密码写的")]),
    31: ("这份卷轴列举了标志季节更替的各种庆典，并详述了从另一份死海古卷中已知的两项年度宗教活动。", "并列谓语 + 定语从句", "主干是 The scroll names celebrations ... and details two yearly religious events，names 与 details 是并列谓语（details 在此为动词“详述”）；that indicate shifts in seasons 是定语从句修饰 celebrations；known from ... 是过去分词短语修饰 events。", [w("indicate", "v.", "表明；显示"), w("yearly", "adj.", "每年的；一年一度的")]),
    32: ("如今仅剩另一份已知的卷轴尚未翻译。", "主系表结构（remain + 形容词）", "主干是 Only one more known scroll remains untranslated；remain 是系动词，后接形容词 untranslated 作表语，表“仍处于未翻译的状态”，呼应全文结尾。", [w("remain", "v.", "仍然是；保持（某状态）"), w("untranslated", "adj.", "未翻译的")]),
}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    data["quality"] = "teacher_refined"
    data["phrases"] = PHRASES

    old_sentences = data["sentences"]

    # Build the new sentence list, splitting old id 16 into two sentences and
    # renumbering everything after it by +1.
    new_sentences = []
    for s in old_sentences:
        old_id = s["id"]

        # Apply EN fixes.
        if old_id in EN_FIX:
            s["en"] = EN_FIX[old_id]

        zh, gtype, note, words = REFINED[old_id]
        s["zh"] = zh
        s["grammar"] = {"type": gtype, "note": note}
        s["words"] = words

        # Renumber: ids <= 16 keep their id; ids >= 17 shift +1.
        s["id"] = old_id if old_id <= 16 else old_id + 1
        new_sentences.append(s)

        # Insert the split-out "papyrus" sentence right after old id 16 as new id 17.
        if old_id == 16:
            nzh, ngtype, nnote, nwords = NEW_SENTENCE_REFINED
            new_sentences.append({
                "id": 17,
                "para": NEW_SENTENCE_PARA,
                "en": NEW_SENTENCE_EN,
                "zh": nzh,
                "grammar": {"type": ngtype, "note": nnote},
                "words": nwords,
            })

    data["sentences"] = new_sentences

    # Shift question evidence_sentence values >= 17 by +1 to keep them pointing
    # at the same physical sentence after renumbering.
    for q in data.get("questions", []):
        for item in q.get("items", []):
            ev = item.get("evidence_sentence")
            if isinstance(ev, int) and ev >= 17:
                item["evidence_sentence"] = ev + 1

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Update index.json: quality + sentence_count (32 -> 33).
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    for row in idx.get("passages", []):
        if row.get("id") == data["id"]:
            row["quality"] = "teacher_refined"
            row["sentence_count"] = len(new_sentences)
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"refined {PATH} -> {len(new_sentences)} sentences")


if __name__ == "__main__":
    main()
