# -*- coding: utf-8 -*-
"""Generate the three teacher-refined reading passages from Cambridge IELTS 13 Test 2.

Source pages: Cambridge IELTS 13 PDF pages 39-51; answer key page 122.
Run from the project root with: python tools/import_c13_test2.py
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSAGES_DIR = ROOT / "data" / "passages"
INDEX_PATH = ROOT / "data" / "index.json"


def W(w: str, pos: str, definition: str) -> dict:
    return {"w": w, "pos": pos, "def": definition}


def build_sentences(rows: list[tuple]) -> list[dict]:
    sentences = []
    for sid, row in enumerate(rows, 1):
        para, en, zh, grammar_type, grammar_note, words = row
        sentences.append({
            "id": sid,
            "para": para,
            "en": en,
            "zh": zh,
            "grammar": {"type": grammar_type, "note": grammar_note},
            "words": list(words),
        })
    return sentences


def S(para: int, en: str, zh: str, grammar_type: str, grammar_note: str, *words: dict) -> tuple:
    return para, en, zh, grammar_type, grammar_note, words


P1_ROWS = [
    S(1, "Cinnamon is a sweet, fragrant spice produced from the inner bark of trees of the genus Cinnamomum, which is native to the Indian sub-continent.",
      "肉桂是一种带有甜香气味的香料，取自樟属树木的内层树皮；这种树原产于印度次大陆。",
      "过去分词定语 + 非限制性定语从句", "produced from... 修饰 spice；which is native to... 补充说明 genus Cinnamomum。",
      W("fragrant", "adj.", "芳香的"), W("inner bark", "n.", "内层树皮")),
    S(1, "It was known in biblical times, and is mentioned in several books of the Bible, both as an ingredient that was mixed with oils for anointing people's bodies, and also as a token indicating friendship among lovers and friends.",
      "早在《圣经》时代，人们就知道肉桂；《圣经》中有几卷书都提到它，既把它写成与油混合、用于涂抹身体的配料，也把它当作爱人和朋友之间表达情谊的信物。",
      "并列被动 + both...and...", "was known 与 is mentioned 并列；both as...and also as... 说明肉桂的两种用途；that was mixed... 修饰 ingredient。",
      W("anoint", "v.", "涂油于；施以涂油礼"), W("token", "n.", "表示；信物")),
    S(1, "In ancient Rome, mourners attending funerals burnt cinnamon to create a pleasant scent.",
      "在古罗马，参加葬礼的哀悼者会燃烧肉桂，让现场产生宜人的香气。",
      "现在分词定语 + 不定式目的状语", "attending funerals 修饰 mourners；to create... 说明燃烧肉桂的目的。",
      W("mourner", "n.", "哀悼者"), W("scent", "n.", "气味；香味")),
    S(1, "Most often, however, the spice found its primary use as an additive to food and drink.",
      "不过，肉桂最主要的用途还是作为食品和饮料的添加物。",
      "简单句 + 插入语", "however 为转折插入语；find its use as... 表示“被用作……”。",
      W("additive", "n.", "添加物；添加剂")),
    S(1, "In the Middle Ages, Europeans who could afford the spice used it to flavour food, particularly meat, and to impress those around them with their ability to purchase an expensive condiment from the ‘exotic’ East.",
      "中世纪时，买得起肉桂的欧洲人用它给食物调味，尤其是肉类；他们还借此向周围的人显示，自己有能力购买来自“异域”东方的昂贵调味品。",
      "定语从句 + 并列不定式", "who could afford the spice 修饰 Europeans；to flavour 与 to impress 并列，说明 used it 的两个目的。",
      W("condiment", "n.", "调味品"), W("exotic", "adj.", "异国的；来自远方的")),
    S(1, "At a banquet, a host would offer guests a plate with various spices piled upon it as a sign of the wealth at his or her disposal.",
      "宴会上，主人会端给客人一只堆放着各种香料的盘子，以此显示自己拥有的财富。",
      "with 复合结构 + 介词短语", "with various spices piled upon it 修饰 a plate；as a sign of... 表示这样做所传达的含义。",
      W("banquet", "n.", "宴会"), W("at one's disposal", "phr.", "可供某人使用；由某人支配")),
    S(1, "Cinnamon was also reported to have health benefits, and was thought to cure various ailments, such as indigestion.",
      "据说肉桂还有保健作用，并被认为可以治疗消化不良等多种疾病。",
      "并列被动 + 不定式", "was reported to have 与 was thought to cure 为两个并列的被动结构；such as 引出例子。",
      W("ailment", "n.", "小病；疾病"), W("indigestion", "n.", "消化不良")),

    S(2, "Toward the end of the Middle Ages, the European middle classes began to desire the lifestyle of the elite, including their consumption of spices.",
      "中世纪末期，欧洲中产阶级开始向往上层阶级的生活方式，其中也包括他们消费香料的习惯。",
      "begin to do + 介词短语", "began to desire 为主句谓语；including... 补充 lifestyle of the elite 的具体内容。",
      W("elite", "n.", "上层阶级；精英"), W("consumption", "n.", "消费；消耗")),
    S(2, "This led to a growth in demand for cinnamon and other spices.",
      "这使人们对肉桂和其他香料的需求增加。",
      "lead to + 名词", "This 指代上一句的社会变化；lead to 表示“导致”，to 为介词。",
      W("lead to", "phr.", "导致"), W("demand for", "phr.", "对……的需求")),
    S(2, "At that time, cinnamon was transported by Arab merchants, who closely guarded the secret of the source of the spice from potential rivals.",
      "当时，肉桂由阿拉伯商人运输，他们严密保守香料产地的秘密，不让潜在竞争者知道。",
      "被动语态 + 非限制性定语从句", "was transported 为被动；who... 补充说明 Arab merchants；guard...from... 表示防止信息落入他人之手。",
      W("merchant", "n.", "商人"), W("potential rival", "n.", "潜在竞争者")),
    S(2, "They took it from India, where it was grown, on camels via an overland route to the Mediterranean.",
      "他们用骆驼把产自印度的肉桂沿陆路运到地中海地区。",
      "where 定语从句 + 方式状语", "where it was grown 补充说明 India；on camels 和 via an overland route 都说明运输方式。",
      W("overland route", "n.", "陆路"), W("Mediterranean", "n.", "地中海地区")),
    S(2, "Their journey ended when they reached Alexandria.",
      "他们抵达亚历山大港后，这段陆路行程便结束了。",
      "when 时间状语从句", "主句为 Their journey ended；when 从句说明结束的时间。",
      W("Alexandria", "n.", "亚历山大港")),
    S(2, "European traders sailed there to purchase their supply of cinnamon, then brought it back to Venice.",
      "欧洲商人航行到那里购买肉桂，随后再把肉桂运回威尼斯。",
      "不定式目的状语 + 并列谓语", "to purchase... 说明 sailed there 的目的；sailed 与 brought 为先后发生的两个动作。",
      W("supply", "n.", "供应量；货源"), W("Venice", "n.", "威尼斯")),
    S(2, "The spice then travelled from that great trading city to markets all around Europe.",
      "肉桂随后从这座重要的贸易城市运往欧洲各地的市场。",
      "简单句", "from...to... 交代香料运输的起点和目的地。",
      W("trading city", "n.", "贸易城市")),
    S(2, "Because the overland trade route allowed for only small quantities of the spice to reach Europe, and because Venice had a virtual monopoly of the trade, the Venetians could set the price of cinnamon exorbitantly high.",
      "由于陆路贸易只能把少量肉桂运到欧洲，而且威尼斯实际上垄断了这项贸易，威尼斯人便可以把肉桂价格定得极高。",
      "两个 because 原因从句", "两个 because 从句并列说明原因；主句 the Venetians could set... 给出结果；set the price high 为宾语加补语。",
      W("virtual monopoly", "n.", "实际上的垄断"), W("exorbitantly", "adv.", "高得离谱地")),
    S(2, "These prices, coupled with the increasing demand, spurred the search for new routes to Asia by Europeans eager to take part in the spice trade.",
      "高昂的价格加上不断增长的需求，促使渴望参与香料贸易的欧洲人寻找通往亚洲的新航线。",
      "过去分词插入语 + 形容词短语定语", "coupled with... 补充主语 These prices；eager to take part... 修饰 Europeans；spur 表示“促使”。",
      W("spur", "v.", "促使；刺激"), W("take part in", "phr.", "参与")),

    S(3, "Seeking the high profits promised by the cinnamon market, Portuguese traders arrived on the island of Ceylon in the Indian Ocean toward the end of the 15th century.",
      "为了获取肉桂市场所带来的高额利润，葡萄牙商人在15世纪末抵达印度洋上的锡兰岛。",
      "现在分词目的状语 + 过去分词定语", "Seeking... 表示到达锡兰的目的；promised by the cinnamon market 修饰 high profits。",
      W("Ceylon", "n.", "锡兰（今斯里兰卡）"), W("high profit", "n.", "高额利润")),
    S(3, "Before Europeans arrived on the island, the state had organized the cultivation of cinnamon.",
      "欧洲人来到岛上之前，当地政府已经组织起肉桂种植。",
      "before 时间从句 + 过去完成时", "Before 从句给出时间参照；had organized 表示该行动在欧洲人到达前已经完成。",
      W("cultivation", "n.", "种植；栽培")),
    S(3, "People belonging to the ethnic group called the Salagama would peel the bark off young shoots of the cinnamon plant in the rainy season, when the wet bark was more pliable.",
      "雨季时，萨拉伽马族人会剥下肉桂嫩枝的树皮，因为此时湿润的树皮更柔韧，便于处理。",
      "分词定语 + when 定语从句", "belonging to... 和 called... 都修饰 People；when... 补充说明 rainy season；would 表示过去经常进行的动作。",
      W("ethnic group", "n.", "族群"), W("pliable", "adj.", "柔韧的；易弯曲的")),
    S(3, "During the peeling process, they curled the bark into the ‘stick’ shape still associated with the spice today.",
      "剥皮过程中，他们把树皮卷成条状，也就是今天人们仍会联想到肉桂的形状。",
      "过去分词定语", "associated with the spice today 修饰 the ‘stick’ shape；curl...into... 表示“把……卷成……”。",
      W("curl", "v.", "卷曲；使卷成"), W("peeling", "n.", "剥皮过程")),
    S(3, "The Salagama then gave the finished product to the king as a form of tribute.",
      "萨拉伽马族人随后把成品交给国王，作为贡品。",
      "give 双宾语 + as 短语", "gave the finished product to the king 为 give sth to sb；as a form of tribute 说明用途。",
      W("tribute", "n.", "贡品；贡税")),
    S(3, "When the Portuguese arrived, they needed to increase production significantly, and so enslaved many other members of the Ceylonese native population, forcing them to work in cinnamon harvesting.",
      "葡萄牙人到来后需要大幅提高产量，于是奴役了许多锡兰原住民，强迫他们采收肉桂。",
      "when 时间从句 + 现在分词结果状语", "needed 与 enslaved 为主句中的先后动作；forcing them to work... 说明奴役造成的结果。",
      W("enslave", "v.", "奴役"), W("harvesting", "n.", "采收；收获")),
    S(3, "In 1518, the Portuguese built a fort on Ceylon, which enabled them to protect the island, so helping them to develop a monopoly in the cinnamon trade and generate very high profits.",
      "1518年，葡萄牙人在锡兰修建了一座堡垒，使他们能够守住岛屿，并由此垄断肉桂贸易，赚取高额利润。",
      "非限制性定语从句 + 分词结果状语", "which 指代修建堡垒这件事；enable sb to do 表示“使某人能够做”；so helping... 说明进一步结果。",
      W("fort", "n.", "堡垒"), W("enable", "v.", "使能够")),
    S(3, "In the late 16th century, for example, they enjoyed a tenfold profit when shipping cinnamon over a journey of eight days from Ceylon to India.",
      "例如在16世纪末，他们把肉桂从锡兰运到印度，航程只有八天，却能获得十倍利润。",
      "when 省略从句", "when shipping... 相当于 when they shipped...；tenfold 表示“十倍的”。",
      W("tenfold", "adj.", "十倍的"), W("ship", "v.", "运输；装运")),

    S(4, "When the Dutch arrived off the coast of southern Asia at the very beginning of the 17th century, they set their sights on displacing the Portuguese as kings of cinnamon.",
      "17世纪初，荷兰人来到南亚沿海后，便决心取代葡萄牙人，成为肉桂贸易的主导者。",
      "when 时间从句 + 动名词宾语", "When 从句说明时间；set their sights on 后接动名词 displacing，表示“决心实现”。",
      W("set one's sights on", "phr.", "决心争取；把目标定在"), W("displace", "v.", "取代")),
    S(4, "The Dutch allied themselves with Kandy, an inland kingdom on Ceylon.",
      "荷兰人与锡兰内陆王国康提结盟。",
      "同位语", "an inland kingdom on Ceylon 是 Kandy 的同位语；ally oneself with 表示“与……结盟”。",
      W("ally with", "phr.", "与……结盟"), W("inland", "adj.", "内陆的")),
    S(4, "In return for payments of elephants and cinnamon, they protected the native king from the Portuguese.",
      "当地国王以大象和肉桂作为报酬，荷兰人则保护他免受葡萄牙人的威胁。",
      "介词短语状语", "In return for... 表示交换条件；protect sb from... 表示“保护某人免受……伤害”。",
      W("in return for", "phr.", "作为对……的回报")),
    S(4, "By 1640, the Dutch broke the 150-year Portuguese monopoly when they overran and occupied their factories.",
      "到1640年，荷兰人攻占葡萄牙人的工厂，打破了葡萄牙长达150年的垄断。",
      "when 时间从句 + 并列谓语", "when they overran and occupied... 说明垄断被打破的具体事件；overran 与 occupied 并列。",
      W("overrun", "v.", "攻占；侵占"), W("monopoly", "n.", "垄断")),
    S(4, "By 1658, they had permanently expelled the Portuguese from the island, thereby gaining control of the lucrative cinnamon trade.",
      "到1658年，荷兰人已把葡萄牙人彻底赶出该岛，从而控制了利润丰厚的肉桂贸易。",
      "过去完成时 + 分词结果状语", "had expelled 表示截至1658年已完成；thereby gaining... 说明这一行动的结果。",
      W("expel", "v.", "驱逐"), W("lucrative", "adj.", "利润丰厚的")),

    S(5, "In order to protect their hold on the market, the Dutch, like the Portuguese before them, treated the native inhabitants harshly.",
      "为了保住市场控制权，荷兰人和此前的葡萄牙人一样，严酷地对待当地居民。",
      "不定式目的状语 + 插入比较", "In order to... 表目的；like the Portuguese before them 为插入的比较成分。",
      W("hold on the market", "n.", "对市场的控制"), W("harshly", "adv.", "严酷地")),
    S(5, "Because of the need to boost production and satisfy Europe's ever-increasing appetite for cinnamon, the Dutch began to alter the harvesting practices of the Ceylonese.",
      "为了提高产量并满足欧洲不断增长的肉桂需求，荷兰人开始改变锡兰人的采收方式。",
      "because of 原因状语 + 并列不定式", "Because of 后接名词 the need；to boost 与 satisfy 并列修饰 need；began to alter 为主句谓语。",
      W("boost", "v.", "提高；促进"), W("appetite for", "n.", "对……的强烈需求")),
    S(5, "Over time, the supply of cinnamon trees on the island became nearly exhausted, due to systematic stripping of the bark.",
      "由于人们有计划地不断剥取树皮，岛上的肉桂树逐渐接近枯竭。",
      "主系表 + 原因状语", "became nearly exhausted 为系表结构；due to... 说明树木枯竭的原因。",
      W("exhausted", "adj.", "耗尽的；枯竭的"), W("systematic", "adj.", "有计划的；系统的")),
    S(5, "Eventually, the Dutch began cultivating their own cinnamon trees to supplement the diminishing number of wild trees available for use.",
      "最后，荷兰人开始自行种植肉桂树，以补充数量不断减少的野生树木。",
      "动名词宾语 + 不定式目的状语", "began cultivating 表示“开始种植”；to supplement... 表目的；available for use 修饰 wild trees。",
      W("supplement", "v.", "补充"), W("diminishing", "adj.", "不断减少的")),

    S(6, "Then, in 1796, the English arrived on Ceylon, thereby displacing the Dutch from their control of the cinnamon monopoly.",
      "1796年，英国人来到锡兰，取代荷兰人控制了肉桂垄断贸易。",
      "分词结果状语", "thereby displacing... 说明英国人到来产生的结果；displace sb from... 表示把某人从某位置取代。",
      W("thereby", "adv.", "从而；因此")),
    S(6, "By the middle of the 19th century, production of cinnamon reached 1,000 tons a year, after a lower grade quality of the spice became acceptable to European tastes.",
      "到19世纪中叶，品质较低的肉桂也开始被欧洲消费者接受，肉桂年产量达到1,000吨。",
      "after 时间状语从句", "主句说明产量；after 从句说明低等级肉桂被接受这一先行变化；became acceptable 为系表结构。",
      W("lower grade", "adj.", "等级较低的"), W("taste", "n.", "喜好；口味")),
    S(6, "By that time, cinnamon was being grown in other parts of the Indian Ocean region and in the West Indies, Brazil, and Guyana.",
      "到那时，印度洋其他地区以及西印度群岛、巴西和圭亚那也开始种植肉桂。",
      "过去进行时被动", "was being grown 表示在当时正在扩展中的被动动作；两个 in 短语列出种植地区。",
      W("West Indies", "n.", "西印度群岛"), W("Guyana", "n.", "圭亚那")),
    S(6, "Not only was a monopoly of cinnamon becoming impossible, but the spice trade overall was diminishing in economic potential, and was eventually superseded by the rise of trade in coffee, tea, chocolate, and sugar.",
      "肉桂垄断不仅已无法维持，整个香料贸易的经济价值也在下降，并最终被咖啡、茶、巧克力和糖贸易的兴起所取代。",
      "not only 倒装 + 并列被动", "Not only 位于句首，引起 was a monopoly... 倒装；but 后有 was diminishing 与 was superseded 两个并列谓语。",
      W("economic potential", "n.", "经济潜力；经济价值"), W("supersede", "v.", "取代")),
]


def make_passage_1() -> dict:
    return {
        "id": "c13-test2-p1",
        "source": "剑桥雅思13 · Test 2 · Passage 1",
        "title": "Bringing cinnamon to Europe",
        "quality": "teacher_refined",
        "analysis_unit": "sentence",
        "phrases": [
            W("inner bark", "n.", "内层树皮"),
            W("spice trade", "n.", "香料贸易"),
            W("overland route", "n.", "陆路"),
            W("virtual monopoly", "n.", "实际上的垄断"),
            W("set one's sights on", "phr.", "决心争取；把目标定在"),
            W("in return for", "phr.", "作为对……的回报"),
        ],
        "sentences": build_sentences(P1_ROWS),
        "questions": [
            {
                "title": "Questions 1-9 · Note completion",
                "type": "note_completion",
                "instructions": [
                    "Complete the notes below.",
                    "Choose ONE WORD ONLY from the passage for each answer.",
                    "The Early History of Cinnamon",
                ],
                "items": [
                    {"number": 1, "prompt": "Biblical times: added to 1 ____", "answer": "oils", "evidence_sentence": 2},
                    {"number": 2, "prompt": "used to show 2 ____ between people", "answer": "friendship", "evidence_sentence": 2},
                    {"number": 3, "prompt": "Ancient Rome: used for its sweet smell at 3 ____", "answer": "funerals", "evidence_sentence": 3},
                    {"number": 4, "prompt": "Middle Ages: was an indication of a person's 4 ____", "answer": "wealth", "evidence_sentence": 6},
                    {"number": 5, "prompt": "known as a treatment for 5 ____ and other health problems", "answer": "indigestion", "evidence_sentence": 7},
                    {"number": 6, "prompt": "grown in 6 ____", "answer": "India", "evidence_sentence": 11},
                    {"number": 7, "prompt": "merchants used 7 ____ to bring it to the Mediterranean", "answer": "camels", "evidence_sentence": 11},
                    {"number": 8, "prompt": "arrived in the Mediterranean at 8 ____", "answer": "Alexandria", "evidence_sentence": 12},
                    {"number": 9, "prompt": "traders took it to 9 ____ and sold it to destinations around Europe", "answer": "Venice", "evidence_sentence": 13},
                ],
            },
            {
                "title": "Questions 10-13 · TRUE / FALSE / NOT GIVEN",
                "type": "true_false_notgiven",
                "instructions": ["Do the following statements agree with the information given in Reading Passage 1?"],
                "items": [
                    {"number": 10, "prompt": "The Portuguese had control over the cinnamon trade in Ceylon throughout the 16th century.", "answer": "TRUE", "evidence_sentence": 23},
                    {"number": 11, "prompt": "The Dutch took over the cinnamon trade from the Portuguese as soon as they arrived in Ceylon.", "answer": "FALSE", "evidence_sentence": 28},
                    {"number": 12, "prompt": "The trees planted by the Dutch produced larger quantities of cinnamon than the wild trees.", "answer": "NOT GIVEN", "evidence_sentence": 33},
                    {"number": 13, "prompt": "The spice trade maintained its economic importance during the 19th century.", "answer": "FALSE", "evidence_sentence": 37},
                ],
            },
        ],
    }


P2_ROWS = [
    S(1, "Oxytocin is a chemical, a hormone produced in the pituitary gland in the brain.",
      "催产素是一种化学物质，也是一种由脑垂体产生的激素。",
      "同位语 + 过去分词定语", "a hormone... 是 a chemical 的同位语；produced in... 修饰 hormone。",
      W("oxytocin", "n.", "催产素"), W("pituitary gland", "n.", "脑垂体")),
    S(1, "It was through various studies focusing on animals that scientists first became aware of the influence of oxytocin.",
      "科学家最初正是通过多项动物研究，才认识到催产素的作用。",
      "强调句 + 分词定语", "It was...that... 为强调句，强调 through various studies；focusing on animals 修饰 studies。",
      W("become aware of", "phr.", "认识到；意识到"), W("influence", "n.", "影响；作用")),
    S(1, "They discovered that it helps reinforce the bonds between prairie voles, which mate for life, and triggers the motherly behaviour that sheep show towards their newborn lambs.",
      "他们发现，催产素可以加强终生配偶制草原田鼠之间的联系，还会触发母羊照顾新生羔羊的母性行为。",
      "宾语从句 + 两个定语从句", "that 引导 discovered 的宾语从句；helps reinforce 与 triggers 并列；which 修饰 prairie voles，that 修饰 motherly behaviour。",
      W("reinforce", "v.", "加强；巩固"), W("prairie vole", "n.", "草原田鼠")),
    S(1, "It is also released by women in childbirth, strengthening the attachment between mother and baby.",
      "女性分娩时也会释放催产素，从而加强母亲与婴儿之间的依恋。",
      "被动语态 + 分词结果状语", "is released 为被动；strengthening... 说明催产素释放产生的结果。",
      W("childbirth", "n.", "分娩"), W("attachment", "n.", "依恋；情感联系")),
    S(1, "Few chemicals have as positive a reputation as oxytocin, which is sometimes referred to as the ‘love hormone’.",
      "很少有化学物质能像催产素一样享有如此正面的名声；它有时被称为“爱情激素”。",
      "as...as 比较 + 非限制性定语从句", "as positive a reputation as 为同级比较；which 补充说明 oxytocin；refer to...as... 表示“把……称为……”。",
      W("reputation", "n.", "名声；声誉"), W("refer to as", "phr.", "把……称为……")),
    S(1, "One sniff of it can, it is claimed, make a person more trusting, empathetic, generous and cooperative.",
      "据称，只吸入一次催产素，就能让人更信任他人、更有同理心，也更慷慨、更愿意合作。",
      "插入语 + make 复合结构", "it is claimed 为插入语；make a person + 四个并列形容词，表示使人发生变化。",
      W("empathetic", "adj.", "有同理心的"), W("cooperative", "adj.", "愿意合作的")),
    S(1, "It is time, however, to revise this wholly optimistic view.",
      "不过，现在应该修正这种完全乐观的看法了。",
      "It is time to do", "It 为形式主语，to revise... 是真正内容；however 为转折插入语。",
      W("revise", "v.", "修正；重新考虑"), W("optimistic", "adj.", "乐观的")),
    S(1, "A new wave of studies has shown that its effects vary greatly depending on the person and the circumstances, and it can impact on our social interactions for worse as well as for better.",
      "新一轮研究表明，催产素的作用会因人和情境而有很大差异；它既可能改善社会交往，也可能使其恶化。",
      "宾语从句 + 分词状语 + 并列句", "that 引导 shown 的宾语从句；depending on... 说明变化条件；and 连接另一个分句；for worse as well as for better 表示好坏两面。",
      W("circumstance", "n.", "情境；情况"), W("social interaction", "n.", "社会交往")),

    S(2, "Oxytocin's role in human behaviour first emerged in 2005.",
      "催产素在人类行为中的作用于2005年首次受到关注。",
      "简单句", "主语为 Oxytocin's role in human behaviour；emerged 表示“显现、受到注意”。",
      W("emerge", "v.", "显现；出现")),
    S(2, "In a groundbreaking experiment, Markus Heinrichs and his colleagues at the University of Freiburg, Germany, asked volunteers to do an activity in which they could invest money with an anonymous person who was not guaranteed to be honest.",
      "德国弗赖堡大学的 Markus Heinrichs 及其同事开展了一项开创性实验：他们让志愿者参加一种投资活动，交易对象是身份不明、也不能保证诚实的人。",
      "双层定语从句 + ask sb to do", "asked volunteers to do... 为主干；in which 修饰 activity；who was not guaranteed... 修饰 an anonymous person。",
      W("groundbreaking", "adj.", "开创性的"), W("anonymous", "adj.", "匿名的；身份不明的")),
    S(2, "The team found that participants who had sniffed oxytocin via a nasal spray beforehand invested more money than those who received a placebo instead.",
      "研究团队发现，事先通过鼻喷剂吸入催产素的参与者，比接受安慰剂的参与者投入了更多资金。",
      "宾语从句 + 定语从句 + 比较", "that 引导 found 的宾语从句；两个 who 从句分别修饰 participants 和 those；more...than... 构成比较。",
      W("nasal spray", "n.", "鼻喷剂"), W("placebo", "n.", "安慰剂")),
    S(2, "The study was the start of research into the effects of oxytocin on human interactions.",
      "这项研究开启了对催产素如何影响人际交往的探索。",
      "主系表结构", "The study 为主语，was 为系动词；research into... 说明研究对象。",
      W("research into", "n.", "对……的研究")),
    S(2, "‘For eight years, it was quite a lonesome field,’ Heinrichs recalls.",
      "Heinrichs 回忆说：“八年里，这一直是一个相当冷清的研究领域。”",
      "直接引语", "引语为主系表结构；Heinrichs recalls 说明说话者。",
      W("lonesome", "adj.", "冷清的；少有人参与的")),
    S(2, "‘Now, everyone is interested.’",
      "“现在，人人都对此感兴趣。”",
      "简单句", "everyone 作主语，is interested 为系表结构；语境中省略了 interested in oxytocin。"),
    S(2, "These follow-up studies have shown that after a sniff of the hormone, people become more charitable, better at reading emotions on others' faces and at communicating constructively in arguments.",
      "后续研究表明，吸入催产素后，人会更愿意行善，也更善于从他人面部读取情绪，并能在争论中进行建设性沟通。",
      "宾语从句 + 并列表语", "that 引导 shown 的宾语从句；charitable、better at reading...、better at communicating... 为并列表语，后两个共用 better at。",
      W("charitable", "adj.", "乐善好施的"), W("constructively", "adv.", "建设性地")),
    S(2, "Together, the results fuelled the view that oxytocin universally enhanced the positive aspects of our social nature.",
      "这些结果共同强化了一种看法：催产素会普遍增强人类社会性的积极方面。",
      "同位语从句", "that 从句解释 the view 的具体内容；fuelled 表示研究结果推动了这一看法。",
      W("fuel", "v.", "加强；推动"), W("social nature", "n.", "社会性")),

    S(3, "Then, after a few years, contrasting findings began to emerge.",
      "几年后，与上述结论相反的发现开始出现。",
      "简单句", "after a few years 为时间状语；contrasting findings 是主语。",
      W("contrasting", "adj.", "形成对比的；相反的")),
    S(3, "Simone Shamay-Tsoory at the University of Haifa, Israel, found that when volunteers played a competitive game, those who inhaled the hormone showed more pleasure when they beat other players, and felt more envy when others won.",
      "以色列海法大学的 Simone Shamay-Tsoory 发现，在竞争性游戏中，吸入催产素的志愿者击败别人时更高兴，别人获胜时则更嫉妒。",
      "宾语从句 + 多个时间从句", "that 引导 found 的宾语从句；when volunteers... 说明实验情境；who inhaled... 修饰 those；后两个 when 分别说明愉悦和嫉妒出现的时间。",
      W("competitive", "adj.", "竞争性的"), W("envy", "n.", "嫉妒")),
    S(3, "What's more, administering oxytocin also has sharply contrasting outcomes depending on a person's disposition.",
      "此外，使用催产素会因人的性格倾向不同而产生截然相反的结果。",
      "动名词主语 + 分词状语", "administering oxytocin 为动名词主语；depending on... 说明结果取决于什么。",
      W("administer", "v.", "给予（药物）"), W("disposition", "n.", "性格；性情")),
    S(3, "Jennifer Bartz from Mount Sinai School of Medicine, New York, found that it improves people's ability to read emotions, but only if they are not very socially adept to begin with.",
      "纽约西奈山医学院的 Jennifer Bartz 发现，催产素能提高人们识别情绪的能力，但只对原本不太擅长社交的人有效。",
      "宾语从句 + if 条件从句", "that 引导 found 的宾语从句；but only if... 限定这一效果成立的条件；to begin with 表示“原本”。",
      W("adept", "adj.", "熟练的；擅长的"), W("to begin with", "phr.", "原本；起初")),
    S(3, "Her research also shows that oxytocin in fact reduces cooperation in subjects who are particularly anxious or sensitive to rejection.",
      "她的研究还显示，对特别焦虑或很怕被拒绝的受试者来说，催产素实际上会降低合作意愿。",
      "宾语从句 + 定语从句", "that 引导 shows 的宾语从句；who... 修饰 subjects；anxious 与 sensitive 并列。",
      W("subject", "n.", "受试者"), W("sensitive to rejection", "phr.", "对拒绝很敏感")),

    S(4, "Another discovery is that oxytocin's effects vary depending on who we are interacting with.",
      "另一项发现是，催产素的作用还会因互动对象不同而改变。",
      "表语从句 + 宾语从句", "that 引导表语从句；who we are interacting with 作 depending on 的宾语。",
      W("interact with", "phr.", "与……互动")),
    S(4, "Studies conducted by Carolyn DeClerck of the University of Antwerp, Belgium, revealed that people who had received a dose of oxytocin actually became less cooperative when dealing with complete strangers.",
      "比利时安特卫普大学 Carolyn DeClerck 的研究显示，接受一剂催产素的人在面对完全陌生的人时，反而更不愿意合作。",
      "过去分词定语 + 宾语从句", "conducted by... 修饰 Studies；that 引导 revealed 的宾语从句；when dealing... 为省略式时间从句。",
      W("dose", "n.", "一剂；剂量"), W("complete stranger", "n.", "完全陌生的人")),
    S(4, "Meanwhile, Carsten De Dreu at the University of Amsterdam in the Netherlands discovered that volunteers given oxytocin showed favouritism: Dutch men became quicker to associate positive words with Dutch names than with foreign ones, for example.",
      "与此同时，荷兰阿姆斯特丹大学的 Carsten De Dreu 发现，接受催产素的志愿者会表现出偏袒。例如，荷兰男性会更快地把正面词语与荷兰名字而不是外国名字联系起来。",
      "宾语从句 + 过去分词定语 + 冒号解释", "that 引导 discovered 的宾语从句；given oxytocin 修饰 volunteers；冒号后给出 favouritism 的例子；than 构成比较。",
      W("favouritism", "n.", "偏袒；偏爱"), W("associate with", "phr.", "把……与……联系起来")),
    S(4, "According to De Dreu, oxytocin drives people to care for those in their social circles and defend them from outside dangers.",
      "De Dreu 认为，催产素会促使人们关心自己社交圈中的人，并保护他们免受外部危险。",
      "drive sb to do + 并列动词", "drives people to care for... and defend... 中 care 与 defend 并列，共用 to。",
      W("social circle", "n.", "社交圈"), W("defend from", "phr.", "保护……免受……")),
    S(4, "So, it appears that oxytocin strengthens biases, rather than promoting general goodwill, as was previously thought.",
      "因此，催产素似乎会加强偏见，而不是像过去认为的那样普遍增进善意。",
      "It appears that + rather than", "It 为形式主语，that 从句是真正内容；rather than 后接动名词；as was previously thought 为方式比较从句。",
      W("bias", "n.", "偏见；偏向"), W("goodwill", "n.", "善意")),

    S(5, "There were signs of these subtleties from the start.",
      "这些细微差异其实从一开始就已有迹象。",
      "There be 句型", "There were 表示存在；of these subtleties 修饰 signs。",
      W("subtlety", "n.", "细微差异；微妙之处")),
    S(5, "Bartz has recently shown that in almost half of the existing research results, oxytocin influenced only certain individuals or in certain circumstances.",
      "Bartz 最近指出，在现有研究结果中，近一半显示催产素只影响某些人，或只在某些情境下产生影响。",
      "宾语从句 + 并列限定", "that 引导 shown 的宾语从句；only certain individuals 与 in certain circumstances 从对象和情境两方面限定作用。",
      W("existing", "adj.", "现有的"), W("individual", "n.", "个人；个体")),
    S(5, "Where once researchers took no notice of such findings, now a more nuanced understanding of oxytocin's effects is propelling investigations down new lines.",
      "研究人员过去忽视这类结果，如今对催产素作用的理解更细致了，也由此推动研究转向新的方向。",
      "where 对比从句 + 现在进行时", "Where once... 与 now... 形成今昔对比；is propelling 表示正在推动；down new lines 表示沿新方向。",
      W("nuanced", "adj.", "细致而有层次的"), W("propel", "v.", "推动")),
    S(5, "To Bartz, the key to understanding what the hormone does lies in pinpointing its core function rather than in cataloguing its seemingly endless effects.",
      "Bartz 认为，理解这种激素的关键在于找出它的核心功能，而不是罗列它似乎无穷无尽的作用。",
      "what 宾语从句 + lie in doing", "what the hormone does 作 understanding 的宾语；the key lies in... 为主干；pinpointing 与 cataloguing 由 rather than 对比。",
      W("pinpoint", "v.", "准确找出"), W("catalogue", "v.", "分类列举")),
    S(5, "There are several hypotheses which are not mutually exclusive.",
      "目前有几种假说，它们彼此并不排斥。",
      "There be + 定语从句", "which are not mutually exclusive 修饰 hypotheses，表示这些解释可以同时成立。",
      W("hypothesis", "n.", "假说"), W("mutually exclusive", "adj.", "互相排斥的")),
    S(5, "Oxytocin could help to reduce anxiety and fear.",
      "催产素可能有助于减轻焦虑和恐惧。",
      "情态动词 + help to do", "could 表示一种可能解释；help to reduce 表示“有助于减少”。",
      W("anxiety", "n.", "焦虑")),
    S(5, "Or it could simply motivate people to seek out social connections.",
      "也可能只是促使人们主动寻找社会联系。",
      "motivate sb to do", "could 表可能性；motivate people to seek out... 表示促使人去寻找。",
      W("seek out", "phr.", "主动寻找")),
    S(5, "She believes that oxytocin acts as a chemical spotlight that shines on social clues - a shift in posture, a flicker of the eyes, a dip in the voice - making people more attuned to their social environment.",
      "她认为，催产素像一束化学聚光灯，会突出姿势变化、眼神闪动、音调下降等社交线索，使人更敏锐地感知周围的社交环境。",
      "宾语从句 + 定语从句 + 分词结果状语", "that 引导 believes 的宾语从句；that shines... 修饰 spotlight；破折号中列举 social clues；making... 说明结果。",
      W("attuned to", "adj.", "敏锐感知；与……协调"), W("posture", "n.", "姿势")),
    S(5, "This would explain why it makes us more likely to look others in the eye and improves our ability to identify emotions.",
      "这可以解释为什么催产素会让我们更愿意直视他人，也会提高我们识别情绪的能力。",
      "why 宾语从句 + 并列谓语", "why 从句作 explain 的宾语；makes 与 improves 为从句中的并列谓语；make us more likely to do 为复合结构。",
      W("look someone in the eye", "phr.", "直视某人"), W("identify", "v.", "识别")),
    S(5, "But it could also make things worse for people who are overly sensitive or prone to interpreting social cues in the worst light.",
      "但对过度敏感、容易把社交线索往最坏处理解的人来说，催产素也可能使情况变得更糟。",
      "make 复合结构 + 定语从句", "make things worse 为 make + 宾语 + 补语；who... 修饰 people；sensitive 与 prone 并列。",
      W("prone to", "adj.", "容易……的"), W("in the worst light", "phr.", "从最坏的角度")),

    S(6, "Perhaps we should not be surprised that the oxytocin story has become more perplexing.",
      "催产素的研究结论变得更加复杂难解，我们或许不该感到意外。",
      "情感形容词 + that 从句", "that 从句说明 surprised 的具体原因；has become 为现在完成时。",
      W("perplexing", "adj.", "令人困惑的；复杂难解的")),
    S(6, "The hormone is found in everything from octopuses to sheep, and its evolutionary roots stretch back half a billion years.",
      "从章鱼到绵羊，许多动物体内都有这种激素；它的进化根源可以追溯到五亿年前。",
      "并列句 + from...to...", "and 连接两个独立分句；from octopuses to sheep 表示范围；stretch back 表示追溯到。",
      W("evolutionary root", "n.", "进化根源"), W("stretch back", "phr.", "追溯到")),
    S(6, "‘It's a very simple and ancient molecule that has been co-opted for many different functions,’ says Sue Carter at the University of Illinois, Chicago, USA.",
      "美国伊利诺伊大学芝加哥分校的 Sue Carter 说：“这是一种非常简单而古老的分子，后来被借用于许多不同功能。”",
      "定语从句 + 引述倒装", "that has been co-opted... 修饰 molecule；says Sue Carter 为引述中的主谓倒装。",
      W("molecule", "n.", "分子"), W("co-opt", "v.", "改作他用；吸收利用")),
    S(6, "‘It affects primitive parts of the brain like the amygdala, so it's going to have many effects on just about everything.’",
      "“它会影响杏仁核等大脑原始区域，所以几乎会对一切产生多方面作用。”",
      "so 结果并列句", "so 连接原因与结果；like the amygdala 举例说明 primitive parts of the brain。",
      W("primitive", "adj.", "原始的"), W("amygdala", "n.", "杏仁核")),
    S(6, "Bartz agrees.",
      "Bartz 也同意这一看法。",
      "简单句", "agree 的具体内容承接前文。"),
    S(6, "‘Oxytocin probably does some very basic things, but once you add our higher-order thinking and social situations, these basic processes could manifest in different ways depending on individual differences and context.’",
      "“催产素可能只完成一些很基础的工作，但一旦加入人类的高级思维和社会情境，这些基础过程便可能因个体差异和具体环境而呈现出不同结果。”",
      "but 转折 + once 条件/时间从句", "but 连接转折；once you add... 表示条件；depending on... 说明表现方式取决于个体和语境。",
      W("higher-order thinking", "n.", "高级思维"), W("manifest", "v.", "表现；显现")),
]


def make_passage_2() -> dict:
    return {
        "id": "c13-test2-p2",
        "source": "剑桥雅思13 · Test 2 · Passage 2",
        "title": "Oxytocin",
        "subtitle": "The positive and negative effects of the chemical known as the ‘love hormone’",
        "quality": "teacher_refined",
        "analysis_unit": "sentence",
        "phrases": [
            W("pituitary gland", "n.", "脑垂体"),
            W("love hormone", "n.", "爱情激素"),
            W("nasal spray", "n.", "鼻喷剂"),
            W("social interaction", "n.", "社会交往"),
            W("social circle", "n.", "社交圈"),
            W("mutually exclusive", "adj.", "互相排斥的"),
        ],
        "sentences": build_sentences(P2_ROWS),
        "questions": [
            {
                "title": "Questions 14-17 · Matching information",
                "type": "matching_information",
                "instructions": [
                    "Reading Passage 2 has six paragraphs, A-F.",
                    "Which paragraph contains the following information?",
                    "NB You may use any letter more than once.",
                ],
                "items": [
                    {"number": 14, "prompt": "reference to research showing the beneficial effects of oxytocin on people", "answer": "B", "evidence_sentence": 15},
                    {"number": 15, "prompt": "reasons why the effects of oxytocin are complex", "answer": "F", "evidence_sentence": 42},
                    {"number": 16, "prompt": "mention of a period in which oxytocin attracted little scientific attention", "answer": "B", "evidence_sentence": 13},
                    {"number": 17, "prompt": "reference to people ignoring certain aspects of their research data", "answer": "E", "evidence_sentence": 29},
                ],
            },
            {
                "title": "Questions 18-20 · Matching researchers",
                "type": "matching_features",
                "instructions": [
                    "Match each research finding with the correct researcher, A-F.",
                    "A Markus Heinrichs · B Simone Shamay-Tsoory · C Jennifer Bartz",
                    "D Carolyn DeClerck · E Carsten De Dreu · F Sue Carter",
                ],
                "items": [
                    {"number": 18, "prompt": "People are more trusting when affected by oxytocin.", "answer": "A", "evidence_sentence": 11},
                    {"number": 19, "prompt": "Oxytocin increases people's feelings of jealousy.", "answer": "B", "evidence_sentence": 18},
                    {"number": 20, "prompt": "The effect of oxytocin varies from one type of person to another.", "answer": "C", "evidence_sentence": 20},
                ],
            },
            {
                "title": "Questions 21-26 · Summary completion",
                "type": "summary_completion",
                "instructions": ["Complete the summary below.", "Choose ONE WORD ONLY from the passage for each answer.", "Oxytocin research"],
                "items": [
                    {"number": 21, "prompt": "The earliest findings about oxytocin and bonding came from research involving 21 ____.", "answer": "animals", "evidence_sentence": 2},
                    {"number": 22, "prompt": "It was also discovered that humans produce oxytocin during 22 ____.", "answer": "childbirth", "evidence_sentence": 4},
                    {"number": 23, "prompt": "Participants were given either oxytocin or a 23 ____.", "answer": "placebo", "evidence_sentence": 11},
                    {"number": 24, "prompt": "At the University of Haifa participants took part in a 24 ____.", "answer": "game", "evidence_sentence": 18},
                    {"number": 25, "prompt": "The University of Antwerp study showed people's lack of willingness to help 25 ____.", "answer": "strangers", "evidence_sentence": 23},
                    {"number": 26, "prompt": "People given oxytocin considered familiar 26 ____ to have more positive associations.", "answer": "names", "evidence_sentence": 24},
                ],
            },
        ],
    }


P3_ROWS = [
    S(1, "Most managers can identify the major trends of the day.",
      "大多数管理者都能识别当下的主要趋势。",
      "简单句", "主语 Most managers，谓语 can identify，宾语 the major trends of the day。",
      W("identify", "v.", "识别；发现"), W("trend", "n.", "趋势")),
    S(1, "But in the course of conducting research in a number of industries and working directly with companies, we have discovered that managers often fail to recognize the less obvious but profound ways these trends are influencing consumers' aspirations, attitudes, and behaviors.",
      "但我们在多个行业开展研究并直接与企业合作时发现，管理者往往没有看出：这些趋势正以不太明显却影响深远的方式，改变消费者的愿望、态度和行为。",
      "宾语从句 + 省略关系词的定语从句", "that 引导 discovered 的宾语从句；these trends are influencing... 是省略关系词的定语从句，修饰 ways；less obvious but profound 为并列形容词。",
      W("profound", "adj.", "影响深远的"), W("aspiration", "n.", "愿望；抱负")),
    S(1, "This is especially true of trends that managers view as peripheral to their core markets.",
      "对于那些被管理者视为与核心市场关系不大的趋势，这种情况尤其常见。",
      "定语从句 + view as", "that... 修饰 trends；view A as B 表示“把 A 看作 B”；This 指代上一句所说的忽视现象。",
      W("peripheral", "adj.", "次要的；外围的"), W("core market", "n.", "核心市场")),

    S(2, "Many ignore trends in their innovation strategies or adopt a wait-and-see approach and let competitors take the lead.",
      "许多管理者在创新战略中忽视趋势，或者采取观望态度，让竞争对手抢先行动。",
      "并列谓语 + let sb do", "ignore 与 adopt 由 or 连接；adopt 与 let 由 and 连接；let competitors take 不带 to。",
      W("wait-and-see", "adj.", "观望的"), W("take the lead", "phr.", "取得领先；率先行动")),
    S(2, "At a minimum, such responses mean missed profit opportunities.",
      "轻则，这些做法会让企业错失盈利机会。",
      "简单句", "At a minimum 表示至少会出现的后果；missed profit opportunities 为宾语。",
      W("at a minimum", "phr.", "至少；轻则")),
    S(2, "At the extreme, they can jeopardize a company by ceding to rivals the opportunity to transform the industry.",
      "重则，企业把改造行业的机会让给对手，甚至可能危及自身。",
      "by doing 方式状语 + 不定式定语", "by ceding... 说明 jeopardize 的方式；to transform the industry 修饰 opportunity。",
      W("jeopardize", "v.", "危及"), W("cede", "v.", "让出；割让")),
    S(2, "The purpose of this article is twofold: to spur managers to think more expansively about how trends could engender new value propositions in their core markets, and to provide some high-level advice on how to make market research and product development personnel more adept at analyzing and exploiting trends.",
      "本文有两个目的：促使管理者更广泛地思考趋势如何在核心市场中催生新的价值主张；并就如何提高市场研究和产品开发人员分析、利用趋势的能力，提供一些总体建议。",
      "冒号解释 + 两个并列不定式", "to spur... 与 to provide... 并列解释 twofold；两个 how 从句分别作 about 和 on 的宾语；make personnel more adept 为复合结构。",
      W("engender", "v.", "产生；促成"), W("value proposition", "n.", "价值主张")),

    S(3, "One strategy, known as ‘infuse and augment’, is to design a product or service that retains most of the attributes and functions of existing products in the category but adds others that address the needs and desires unleashed by a major trend.",
      "第一种策略称为“注入并扩充”：设计一项产品或服务，保留该品类现有产品的大部分特点和功能，同时增加能够满足某项重大趋势所激发的新需求与愿望的特点。",
      "过去分词插入语 + 多层定语从句", "known as... 修饰 strategy；that retains...but adds... 修饰 product or service；that address... 修饰 others；unleashed... 修饰 needs and desires。",
      W("infuse", "v.", "注入"), W("augment", "v.", "扩充；增加")),
    S(3, "A case in point is the Poppy range of handbags, which the firm Coach created in response to the economic downturn of 2008.",
      "蔻驰公司为应对2008年的经济衰退而推出 Poppy 系列手袋，这就是一个典型案例。",
      "非限制性定语从句", "which... 修饰 the Poppy range of handbags；in response to 表示产品推出的背景和原因。",
      W("a case in point", "phr.", "恰当的例子；典型案例"), W("economic downturn", "n.", "经济衰退")),
    S(3, "The Coach brand had been a symbol of opulence and luxury for nearly 70 years, and the most obvious reaction to the downturn would have been to lower prices.",
      "近70年来，蔻驰一直是富足与奢华的象征；面对经济衰退，最直接的反应本来会是降价。",
      "过去完成时 + would have done", "and 连接两个分句；had been 说明此前长期状态；would have been 表示在当时看来可能采取的做法。",
      W("opulence", "n.", "富足；奢华"), W("lower prices", "phr.", "降低价格")),
    S(3, "However, that would have risked cheapening the brand's image.",
      "然而，这样做可能会损害品牌的高端形象。",
      "would have done + risk doing", "that 指代降价；would have risked 表示可能后果；risk 后接动名词 cheapening。",
      W("cheapen", "v.", "使显得廉价；贬低")),
    S(3, "Instead, they initiated a consumer-research project which revealed that customers were eager to lift themselves and the country out of tough times.",
      "他们转而开展消费者研究，结果发现顾客希望自己和国家都能走出艰难时期。",
      "定语从句 + 宾语从句", "which revealed... 修饰 project；that 引导 revealed 的宾语从句；be eager to do 表示迫切希望。",
      W("initiate", "v.", "启动；发起"), W("lift out of", "phr.", "使摆脱")),
    S(3, "Using these insights, Coach launched the lower-priced Poppy handbags, which were in vibrant colors, and looked more youthful and playful than conventional Coach products.",
      "蔻驰根据这些研究发现推出了价格较低的 Poppy 手袋，采用鲜艳配色，外观比传统蔻驰产品更年轻、更活泼。",
      "分词状语 + 非限制性定语从句", "Using these insights 表示依据；which... 补充说明 handbags；were 与 looked 为并列谓语；more...than... 构成比较。",
      W("insight", "n.", "深入认识；研究发现"), W("vibrant", "adj.", "鲜艳的；充满活力的")),
    S(3, "Creating the sub-brand allowed Coach to avert an across-the-board price cut.",
      "创立这一子品牌，使蔻驰避免了全线降价。",
      "动名词主语 + allow sb to do", "Creating the sub-brand 作主语；allow Coach to avert... 表示使公司能够避免。",
      W("avert", "v.", "避免；防止"), W("across-the-board", "adj.", "全面的；全线的")),
    S(3, "In contrast to the many companies that responded to the recession by cutting prices, Coach saw the new consumer mindset as an opportunity for innovation and renewal.",
      "许多公司以降价应对经济衰退，蔻驰则不同，它把消费者的新心态视为创新和更新的机会。",
      "对比状语 + 定语从句 + see as", "In contrast to... 引出对比；that responded... 修饰 companies；see A as B 表示“把 A 看作 B”。",
      W("recession", "n.", "经济衰退"), W("renewal", "n.", "更新；复兴")),

    S(4, "A further example of this strategy was supermarket Tesco's response to consumers' growing concerns about the environment.",
      "这一策略的另一个例子，是超市企业乐购对消费者日益关注环境问题所作的回应。",
      "主系表结构", "A further example 为主语；Tesco's response... 为表语；about the environment 修饰 concerns。",
      W("concern", "n.", "关注；担忧")),
    S(4, "With that in mind, Tesco, one of the world's top five retailers, introduced its Greener Living program, which demonstrates the company's commitment to protecting the environment by involving consumers in ways that produce tangible results.",
      "考虑到这一点，全球五大零售商之一乐购推出“绿色生活”计划，让消费者参与能产生实际效果的环保行动，以此表明公司的环保承诺。",
      "同位语 + 非限制性定语从句", "one of... 是 Tesco 的同位语；which 修饰 program；by involving... 说明展示承诺的方式；that produce... 修饰 ways。",
      W("retailer", "n.", "零售商"), W("tangible", "adj.", "实际可见的；明确的")),
    S(4, "For example, Tesco customers can accumulate points for such activities as reusing bags, recycling cans and printer cartridges, and buying home-insulation materials.",
      "例如，乐购顾客重复使用购物袋、回收易拉罐和打印机墨盒，或购买家庭保温材料，都可以累积积分。",
      "such as 举例 + 并列动名词", "such activities as 后列出 reusing、recycling、buying 三项并列活动。",
      W("accumulate", "v.", "积累"), W("insulation", "n.", "保温；隔热材料")),
    S(4, "Like points earned on regular purchases, these green points can be redeemed for cash.",
      "与日常购物所得积分一样，这些绿色积分可以兑换现金。",
      "过去分词定语 + 被动语态", "earned on regular purchases 修饰 points；can be redeemed 为情态动词被动语态。",
      W("redeem", "v.", "兑换")),
    S(4, "Tesco has not abandoned its traditional retail offerings but augmented its business with these innovations, thereby infusing its value proposition with a green streak.",
      "乐购没有放弃传统零售业务，而是用这些创新扩充业务，从而在其价值主张中加入环保内容。",
      "not...but... + 分词结果状语", "has not abandoned 与 (has) augmented 形成转折；thereby infusing... 说明扩充业务的结果。",
      W("retail offering", "n.", "零售产品与服务"), W("green streak", "n.", "环保特色")),

    S(5, "A more radical strategy is ‘combine and transcend’.",
      "一种更激进的策略是“结合并超越”。",
      "主系表结构", "A more radical strategy 为主语；引号内名称作表语。",
      W("radical", "adj.", "激进的；彻底的"), W("transcend", "v.", "超越")),
    S(5, "This entails combining aspects of the product's existing value proposition with attributes addressing changes arising from a trend, to create a novel experience - one that may land the company in an entirely new market space.",
      "这种策略把产品现有价值主张的部分内容，与针对趋势变化的新特点结合起来，创造一种新体验；这种体验可能把公司带入全新的市场空间。",
      "entail doing + 分词定语 + 同位语", "entails 后接 combining；addressing... 修饰 attributes，arising... 修饰 changes；to create 表目的；one 是 experience 的同位语，that 修饰 one。",
      W("entail", "v.", "涉及；必然包括"), W("novel", "adj.", "新颖的")),
    S(5, "At first glance, spending resources to incorporate elements of a seemingly irrelevant trend into one's core offerings sounds like it's hardly worthwhile.",
      "乍看之下，投入资源，把一个似乎不相关的趋势纳入核心产品，好像并不值得。",
      "动名词主语 + sound like", "spending resources... 为主语；to incorporate... 说明资源用于何处；it's hardly worthwhile 作 like 的宾语从句。",
      W("at first glance", "phr.", "乍看之下"), W("incorporate into", "phr.", "把……纳入……")),
    S(5, "But consider Nike's move to integrate the digital revolution into its reputation for high-performance athletic footwear.",
      "但可以看看耐克的做法：它把数字革命融入自己在高性能运动鞋领域的声誉。",
      "祈使句 + 不定式定语", "consider 为祈使句谓语；to integrate... 修饰 Nike's move；integrate A into B 表示“把 A 融入 B”。",
      W("integrate", "v.", "整合；融入"), W("athletic footwear", "n.", "运动鞋")),
    S(5, "In 2006, they teamed up with technology company Apple to launch Nike+, a digital sports kit comprising a sensor that attaches to the running shoe and a wireless receiver that connects to the user's iPod.",
      "2006年，耐克与科技公司苹果合作推出 Nike+。这套数字运动设备包括一个安装在跑鞋上的传感器，以及一个连接用户 iPod 的无线接收器。",
      "不定式目的状语 + 同位语 + 定语从句", "to launch... 表合作目的；a digital sports kit 是 Nike+ 的同位语；comprising... 修饰 kit；两个 that 从句分别修饰 sensor 和 receiver。",
      W("team up with", "phr.", "与……合作"), W("wireless receiver", "n.", "无线接收器")),
    S(5, "By combining Nike's original value proposition for amateur athletes with one for digital consumers, the Nike+ sports kit and web interface moved the company from a focus on athletic apparel to a new plane of engagement with its customers.",
      "Nike+ 把耐克面向业余运动者的原有价值主张，与面向数字产品消费者的价值主张结合起来，使公司从专注运动服饰，转向与顾客建立一种新的互动关系。",
      "By doing 方式状语 + from...to...", "By combining... 说明方式；one 指代 value proposition；moved the company from...to... 表示定位转变。",
      W("amateur athlete", "n.", "业余运动者"), W("engagement", "n.", "互动；联系")),

    S(6, "A third approach, known as ‘counteract and reaffirm’, involves developing products or services that stress the values traditionally associated with the category in ways that allow consumers to oppose - or at least temporarily escape from - the aspects of trends they view as undesirable.",
      "第三种方法称为“抵消并重申”：开发强调该品类传统价值的产品或服务，让消费者能够对抗，或至少暂时摆脱，他们认为不理想的趋势影响。",
      "过去分词插入语 + 多层定语从句", "known as... 修饰 approach；involves 后接 developing；that stress... 修饰 products or services；that allow... 修饰 ways；they view as undesirable 修饰 aspects。",
      W("counteract", "v.", "抵消；对抗"), W("reaffirm", "v.", "重申；再次肯定")),
    S(6, "A product that accomplished this is the ME2, a video game created by Canada's iToys.",
      "加拿大 iToys 公司开发的视频游戏 ME2，就是采用这种方法的产品。",
      "定语从句 + 同位语", "that accomplished this 修饰 A product；a video game... 是 ME2 的同位语；created by... 修饰 game。",
      W("accomplish", "v.", "完成；实现")),
    S(6, "By reaffirming the toy category's association with physical play, the ME2 counteracted some of the widely perceived negative impacts of digital gaming devices.",
      "ME2 重新强调玩具与身体活动之间的联系，从而抵消了人们普遍认为数字游戏设备会带来的一些负面影响。",
      "By doing 方式状语 + 过去分词定语", "By reaffirming... 说明抵消负面影响的方式；widely perceived 修饰 negative impacts。",
      W("physical play", "n.", "身体活动型游戏"), W("perceived", "adj.", "被认为的")),
    S(6, "Like other handheld games, the device featured a host of exciting interactive games, a full-color LCD screen, and advanced 3D graphics.",
      "与其他掌上游戏机一样，这款设备提供多种互动游戏、全彩液晶屏和先进的三维图像。",
      "介词短语比较 + 并列宾语", "Like other handheld games 作比较状语；featured 后接三项并列内容。",
      W("handheld", "adj.", "手持式的；掌上的"), W("a host of", "phr.", "许多；大量")),
    S(6, "What set it apart was that it incorporated the traditional physical component of children's play: it contained a pedometer, which tracked and awarded points for physical activity (walking, running, biking, skateboarding, climbing stairs).",
      "它的独特之处在于加入了儿童游戏中传统的身体活动部分：设备内置计步器，能记录走路、跑步、骑车、滑板和爬楼梯等活动，并按活动量给分。",
      "what 主语从句 + that 表语从句", "What set it apart 作主语；that 从句作表语；冒号后解释 physical component；which 修饰 pedometer，并带 tracked 和 awarded 两个谓语。",
      W("set apart", "phr.", "使与众不同"), W("pedometer", "n.", "计步器")),
    S(6, "The child could use the points to enhance various virtual skills needed for the video game.",
      "儿童可以用这些积分提升电子游戏中需要的各种虚拟技能。",
      "use sth to do + 过去分词定语", "to enhance... 说明积分的用途；needed for the video game 修饰 virtual skills。",
      W("enhance", "v.", "提升；增强"), W("virtual", "adj.", "虚拟的")),
    S(6, "The ME2, introduced in mid-2008, catered to kids' huge desire to play video games while countering the negatives, such as associations with lack of exercise and obesity.",
      "ME2 于2008年年中推出，它既满足儿童玩电子游戏的强烈愿望，也抵消了电子游戏与缺乏运动、肥胖等问题之间的负面联系。",
      "过去分词插入语 + while doing", "introduced in mid-2008 补充 ME2；while countering... 表示在满足需求的同时抵消负面影响；such as 引出例子。",
      W("cater to", "phr.", "迎合；满足"), W("obesity", "n.", "肥胖")),

    S(7, "Once you have gained perspective on how trend-related changes in consumer opinions and behaviors impact on your category, you can determine which of our three innovation strategies to pursue.",
      "了解与趋势有关的消费者观点和行为变化会怎样影响你的产品品类后，就可以判断应采用三种创新策略中的哪一种。",
      "once 时间/条件从句 + wh-不定式", "Once 从句给出前提；how... 作 on 的宾语；which...to pursue 作 determine 的宾语。",
      W("gain perspective on", "phr.", "了解；形成认识"), W("pursue", "v.", "采用；实行")),
    S(7, "When your category's basic value proposition continues to be meaningful for consumers influenced by the trend, the infuse-and-augment strategy will allow you to reinvigorate the category.",
      "如果某项趋势没有削弱品类基本价值主张对消费者的意义，就可以采用“注入并扩充”策略，为该品类增添活力。",
      "when 条件从句 + 过去分词定语", "When 从句表示适用条件；influenced by the trend 修饰 consumers；allow you to reinvigorate 为 allow sb to do。",
      W("reinvigorate", "v.", "使恢复活力")),
    S(7, "If analysis reveals an increasing disparity between your category and consumers' new focus, your innovations need to transcend the category to integrate the two worlds.",
      "如果分析显示品类与消费者的新关注点越来越脱节，创新就需要超越原有品类，把两个领域结合起来。",
      "if 条件从句 + 不定式目的状语", "If 从句给出条件；need to transcend 为主句谓语；to integrate... 说明超越品类的目的。",
      W("disparity", "n.", "差异；脱节"), W("transcend", "v.", "超越")),
    S(7, "Finally, if aspects of the category clash with undesired outcomes of a trend, such as associations with unhealthy lifestyles, there is an opportunity to counteract those changes by reaffirming the core values of your category.",
      "最后，如果该品类的某些方面与趋势带来的不良结果相冲突，例如会让人联想到不健康的生活方式，就可以通过重申品类的核心价值来抵消这种变化。",
      "if 条件从句 + There be", "if 从句说明第三种策略的适用条件；such as 引出例子；to counteract... 修饰 opportunity；by reaffirming... 说明方法。",
      W("clash with", "phr.", "与……冲突"), W("undesired", "adj.", "不希望出现的")),

    S(8, "Trends - technological, economic, environmental, social, or political - that affect how people perceive the world around them and shape what they expect from products and services present firms with unique opportunities for growth.",
      "技术、经济、环境、社会或政治趋势会影响人们理解周围世界的方式，也会塑造他们对产品和服务的期待；这些趋势为企业带来独特的增长机会。",
      "定语从句 + 两个宾语从句", "破折号中列举 trends 的类型；that 引导定语从句，affect 与 shape 并列；how 与 what 从句分别作宾语；主句谓语为 present。",
      W("perceive", "v.", "理解；感知"), W("present with", "phr.", "给……带来；使面对")),
]


def make_passage_3() -> dict:
    return {
        "id": "c13-test2-p3",
        "source": "剑桥雅思13 · Test 2 · Passage 3",
        "title": "MAKING THE MOST OF TRENDS",
        "subtitle": "Experts from Harvard Business School give advice to managers",
        "quality": "teacher_refined",
        "analysis_unit": "sentence",
        "phrases": [
            W("value proposition", "n.", "价值主张"),
            W("wait-and-see approach", "n.", "观望态度"),
            W("infuse and augment", "phr.", "注入并扩充"),
            W("combine and transcend", "phr.", "结合并超越"),
            W("counteract and reaffirm", "phr.", "抵消并重申"),
            W("economic downturn", "n.", "经济衰退"),
        ],
        "sentences": build_sentences(P3_ROWS),
        "questions": [
            {
                "title": "Questions 27-31 · Multiple choice",
                "type": "multiple_choice",
                "instructions": ["Choose the correct letter, A, B, C or D."],
                "items": [
                    {"number": 27, "prompt": "In the first paragraph, the writer says that most managers: A fail to spot the key consumer trends; B focus only on principal trends; C misinterpret research data; D are unaware of the significant impact trends have on consumers' lives.", "answer": "D", "evidence_sentence": 2},
                    {"number": 28, "prompt": "Coach was anxious to: A follow competitors; B maintain all prices; C safeguard its luxury-goods reputation; D modify the entire look of its brand.", "answer": "C", "evidence_sentence": 11},
                    {"number": 29, "prompt": "What point is made about Tesco's Greener Living programme? A It did not require Tesco to modify its core business; B it attracted a more eco-conscious clientele; C its main aim was awareness; D Tesco had done it before.", "answer": "A", "evidence_sentence": 20},
                    {"number": 30, "prompt": "What does the writer suggest about Nike's strategy? A extremely risky; B only affordable for a major company; C impossible in the past; D it might appear to have few obvious benefits.", "answer": "D", "evidence_sentence": 23},
                    {"number": 31, "prompt": "What was original about the ME2? A sports-industry technology; B appeal to fitness-minded youth; C use of colourful 3D graphics; D a handheld game addressing concerns about unhealthy lifestyles.", "answer": "D", "evidence_sentence": 31},
                ],
            },
            {
                "title": "Questions 32-37 · Matching companies",
                "type": "matching_features",
                "instructions": [
                    "Match each statement with the correct company, A-D.",
                    "A Coach · B Tesco · C Nike · D iToys",
                    "NB You may use any letter more than once.",
                ],
                "items": [
                    {"number": 32, "prompt": "It turned the notion that its products could have harmful effects to its own advantage.", "answer": "D", "evidence_sentence": 29},
                    {"number": 33, "prompt": "It extended its offering by collaborating with another manufacturer.", "answer": "C", "evidence_sentence": 25},
                    {"number": 34, "prompt": "It implemented an incentive scheme to demonstrate its corporate social responsibility.", "answer": "B", "evidence_sentence": 18},
                    {"number": 35, "prompt": "It discovered that customers had a positive attitude towards dealing with difficult circumstances.", "answer": "A", "evidence_sentence": 12},
                    {"number": 36, "prompt": "It responded to a growing lifestyle trend in an unrelated product sector.", "answer": "C", "evidence_sentence": 25},
                    {"number": 37, "prompt": "It successfully avoided having to charge its customers less for its core products.", "answer": "A", "evidence_sentence": 14},
                ],
            },
            {
                "title": "Questions 38-40 · Matching sentence endings",
                "type": "sentence_endings",
                "instructions": [
                    "Complete each sentence with the correct ending, A-D.",
                    "A employ a combination of strategies to maintain your consumer base.",
                    "B identify the most appropriate innovation strategy to use.",
                    "C emphasise your brand's traditional values with the counteract-and-reaffirm strategy.",
                    "D use the combine-and-transcend strategy to integrate the two worlds.",
                ],
                "items": [
                    {"number": 38, "prompt": "If there are any trend-related changes impacting on your category, you should...", "answer": "B", "evidence_sentence": 34},
                    {"number": 39, "prompt": "If a current trend highlights a negative aspect of your category, you should...", "answer": "C", "evidence_sentence": 37},
                    {"number": 40, "prompt": "If the consumers' new focus has an increasing lack of connection with your offering, you should...", "answer": "D", "evidence_sentence": 36},
                ],
            },
        ],
    }


def index_row(passage: dict) -> dict:
    return {
        "id": passage["id"],
        "source": passage["source"],
        "title": passage["title"],
        "sentence_count": len(passage["sentences"]),
        "question_count": sum(len(group["items"]) for group in passage.get("questions", [])),
        "quality": passage["quality"],
    }


EXPECTED_ANSWERS = {
    1: "oils", 2: "friendship", 3: "funerals", 4: "wealth", 5: "indigestion",
    6: "India", 7: "camels", 8: "Alexandria", 9: "Venice", 10: "TRUE",
    11: "FALSE", 12: "NOT GIVEN", 13: "FALSE", 14: "B", 15: "F", 16: "B",
    17: "E", 18: "A", 19: "B", 20: "C", 21: "animals", 22: "childbirth",
    23: "placebo", 24: "game", 25: "strangers", 26: "names", 27: "D", 28: "C",
    29: "A", 30: "D", 31: "D", 32: "D", 33: "C", 34: "B", 35: "A",
    36: "C", 37: "A", 38: "B", 39: "C", 40: "D",
}


def validate_batch(passages: list[dict]) -> None:
    actual_answers = {}
    for passage in passages:
        sentences = passage["sentences"]
        assert [sentence["id"] for sentence in sentences] == list(range(1, len(sentences) + 1))
        assert all(sentence["en"] and sentence["zh"] for sentence in sentences)
        assert all(sentence["grammar"]["type"] and sentence["grammar"]["note"] for sentence in sentences)
        for group in passage["questions"]:
            for item in group["items"]:
                evidence = item["evidence_sentence"]
                assert 1 <= evidence <= len(sentences)
                actual_answers[item["number"]] = item["answer"]
                if item["number"] in {*range(1, 10), *range(21, 27)}:
                    assert item["answer"].lower() in sentences[evidence - 1]["en"].lower()
    assert actual_answers == EXPECTED_ANSWERS


def update_index(passages: list[dict]) -> None:
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    incoming_ids = {passage["id"] for passage in passages}
    existing = [row for row in index.get("passages", []) if row.get("id") not in incoming_ids]

    insert_at = 0
    for i, row in enumerate(existing):
        if row.get("id", "").startswith("c13-"):
            insert_at = i + 1
    rows = [index_row(passage) for passage in passages]
    index["passages"] = existing[:insert_at] + rows + existing[insert_at:]
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    passages = [make_passage_1(), make_passage_2(), make_passage_3()]
    validate_batch(passages)
    PASSAGES_DIR.mkdir(parents=True, exist_ok=True)
    for passage in passages:
        path = PASSAGES_DIR / f"{passage['id']}.json"
        path.write_text(json.dumps(passage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"{passage['id']}: {len(passage['sentences'])} 个精读单元, "
            f"{sum(len(group['items']) for group in passage['questions'])} 题"
        )
    update_index(passages)


if __name__ == "__main__":
    main()
