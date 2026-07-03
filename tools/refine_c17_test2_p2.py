"""Teacher-refine Cambridge IELTS 17 Test 2 Passage 2.

The draft generator creates usable question-bank JSON. This refinement layer is
hand-curated: cleaned English (fixing OCR artefacts against the PDF), Chinese
translation, grammar focus, sentence notes, and fixed phrases are written from
an IELTS teaching perspective rather than blindly imported from OCR.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test2-p2.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


# ---------------------------------------------------------------------------
# 1) Clean English (compared line-by-line against tmp/refine_pages page40/41).
#    - remove title fragment + section letters (A/B/C) glued into sentences
#    - rejoin split words ("I t"->"It", "T his"->"This", "ut"->"But", "y"->"By")
#    - restore curly quotes/apostrophes mangled to mojibake, Test-1 style
#    - drop the footnote text that leaked into sentence 16
# ---------------------------------------------------------------------------
EN_FIX = {
    1: "It took at least 3,000 years for humans to learn how to domesticate the wild tomato and cultivate it for food.",
    4: "This approach relies on the revolutionary CRISPR genome editing technique, in which changes are deliberately made to the DNA of a living cell, allowing genetic material to be added, removed or altered.",
    7: "This fast-track domestication could help make the world’s food supply healthier and far more resistant to diseases, such as the rust fungus devastating wheat crops.",
    8: "‘This could transform what we eat,’ says Jorg Kudla at the University of Munster in Germany, a member of the Brazilian team.",
    9: "‘There are 50,000 edible plants in the world, but 90 percent of our energy comes from just 15 crops.’ ‘We can now mimic the known domestication course of major crops like rice, maize, sorghum or others,’ says Caixia Gao of the Chinese Academy of Sciences in Beijing.",
    10: "‘Then we might try to domesticate plants that have never been domesticated.’ Wild tomatoes, which are native to the Andes region in South America, produce pea-sized fruits.",
    12: "But every time a single plant with a mutation is taken from a larger population for breeding, much genetic diversity is lost.",
    15: "By comparing the genomes of modern plants to those of their wild relatives, biologists have been working out what genetic changes occurred as plants were domesticated.",
    16: "The teams in Brazil and China have now used this knowledge to reintroduce these changes from scratch while maintaining or even enhancing the desirable traits of wild strains. Kudla’s team made six changes altogether.",
    18: "While the historical domestication of tomatoes reduced levels of the red pigment lycopene – thought to have potential health benefits – the team in Brazil managed to boost it instead.",
    20: "‘They are quite tasty,’ says Kudla.",
    21: "‘A little bit strong.",
    22: "And very aromatic.’ The team in China re-domesticated several strains of wild tomatoes with desirable traits lost in domesticated tomatoes.",
    27: "Groundcherries are already sold to a limited extent in the US but they are hard to produce because the plant has a sprawling growth habit and the small fruits fall off the branches when ripe.",
    29: "‘There’s potential for this to be a commercial crop,’ says Van Eck.",
    31: "This approach could boost the use of many obscure plants, says Jonathan Jones of the Sainsbury Lab in the UK.",
    33: "The three teams already have their eye on other plants that could be ‘catapulted into the mainstream’, including foxtail, oat-grass and cowpea.",
    35: "But Kudla didn’t want to reveal which species were in his team’s sights, because CRISPR has made the process so easy.",
    36: "‘Any one with the right skills could go to their lab and do this.’",
}


# ---------------------------------------------------------------------------
# 2) Cross-sentence multi-word phrases (clicked in the reading pane).
# ---------------------------------------------------------------------------
PHRASES = [
    w("domesticate the wild tomato", "phr.", "驯化野生番茄"),
    w("cultivate ... for food", "phr.", "培育……作食物"),
    w("CRISPR genome editing technique", "n.", "CRISPR 基因组编辑技术"),
    w("genetic material", "n.", "遗传物质"),
    w("fast-track domestication", "n.", "快速驯化"),
    w("be resistant to", "phr.", "对……有抗性"),
    w("genetic diversity", "n.", "遗传多样性"),
    w("desirable traits", "n.", "理想（合意）性状"),
    w("from scratch", "phr.", "从头开始"),
    w("salt tolerant", "adj.", "耐盐的"),
    w("growth habit", "n.", "生长习性"),
    w("regulatory approval", "n.", "监管审批"),
    w("staple crop", "n.", "主粮作物"),
    w("drought or heat tolerant", "phr.", "耐旱或耐热的"),
]


# ---------------------------------------------------------------------------
# 3) + 4) Per-sentence zh / grammar / words (covers every sentence id).
# ---------------------------------------------------------------------------
REFINED = {
    1: ("人类花了至少 3,000 年才学会如何驯化野生番茄并将其培育成食物。",
        "主干句 + 不定式作状语",
        "主干是 It took ... 3,000 years；It 为形式主语，真正内容在 for humans to learn ... 中；how to domesticate 与 cultivate 并列作 learn 的宾语。",
        [w("domesticate", "v.", "驯化"), w("cultivate", "v.", "培育；种植")]),
    2: ("如今，巴西和中国的两支独立团队在不到三年的时间里就把这件事又重做了一遍。",
        "主干句 + 时间状语",
        "主干 two separate teams have done it；all over again 意为“从头再来一遍”；in less than three years 作时间状语，与首句 3,000 年形成鲜明对比。",
        [w("separate", "adj.", "各自独立的"), w("all over again", "phr.", "重头再来一遍")]),
    3: ("而且他们在某些方面做得更好，因为重新驯化出的番茄比我们现在吃的更有营养。",
        "并列句 + as 原因状语从句",
        "主干 they have done it better；as 引导原因状语从句，its 主语 the re-domesticated tomatoes 与 the ones we eat 作比较；the ones 指代 tomatoes。",
        [w("re-domesticated", "adj.", "重新驯化的"), w("nutritious", "adj.", "有营养的")]),
    4: ("这种方法依赖革命性的 CRISPR 基因组编辑技术——该技术会有意改动活细胞的 DNA，从而实现遗传物质的添加、删除或改变。",
        "非限制性定语从句 + 分词状语",
        "主干 This approach relies on the technique；in which 引导定语从句修饰 technique；allowing ... 为现在分词作结果状语，其后 to be added, removed or altered 三个动词并列。",
        [w("genome", "n.", "基因组"), w("deliberately", "adv.", "故意地；有意地")]),
    5: ("这项技术不仅能改良现有作物，还能把成千上万种野生植物变成有用、诱人的食物。",
        "not only ... but also 并列 + 被动语态",
        "not only ... but (also) 连接两个并列谓语 could improve 与 could be used；后半句用被动 be used to turn ... into ...，强调技术的用途。",
        [w("existing", "adj.", "现有的"), w("appealing", "adj.", "有吸引力的")]),
    6: ("事实上，美国的第三支团队已经开始用番茄的一种近亲——地樱桃（groundcherry）——来做这件事。",
        "主干句 + 过去分词后置定语",
        "主干 a third team has already begun to do this；a relative of the tomato 后接 called the groundcherry（过去分词短语作定语，等于 which is called）。",
        [w("a relative of", "phr.", "……的近亲"), w("groundcherry", "n.", "地樱桃")]),
    7: ("这种快速驯化能帮助让全球粮食供应更健康，也远更能抵抗病害，例如正在摧毁小麦作物的锈菌。",
        "make + 宾补 + 现在分词定语",
        "主干 domestication could help make the food supply healthier and more resistant；healthier 与 more resistant 为并列宾补；devastating wheat crops 为现在分词短语修饰 the rust fungus。",
        [w("resistant", "adj.", "有抵抗力的"), w("devastate", "v.", "毁灭；重创")]),
    8: ("“这可能会改变我们的饮食，”德国明斯特大学的约尔格·库德拉（Jorg Kudla）说，他是巴西团队的一员。",
        "直接引语 + 同位语",
        "引语作 says 的宾语，主谓倒装 says Jorg Kudla；a member of the Brazilian team 为 Jorg Kudla 的同位语，补充其身份。",
        [w("transform", "v.", "彻底改变"), w("member", "n.", "成员")]),
    9: ("“世界上有 5 万种可食用植物，但我们 90% 的能量只来自 15 种作物。”北京中国科学院的高彩霞（Caixia Gao）说：“我们现在能够模仿水稻、玉米、高粱等主要作物已知的驯化历程。”",
        "两句直接引语衔接",
        "本处含两段引语：前一段 There are ... just 15 crops 收尾 Kudla 的话；后一段以 says Caixia Gao 倒装引出高彩霞的新话；mimic ... course 意为“复刻……历程”，常被题目改写为 copy/reproduce。",
        [w("edible", "adj.", "可食用的"), w("mimic", "v.", "模仿；复刻")]),
    10: ("“那样我们或许可以尝试去驯化那些从未被驯化过的植物。”原产于南美安第斯山区的野生番茄，结出的果实只有豌豆般大小。",
        "引语收尾 + 非限制性定语从句",
        "前半句引语收束高彩霞的话；后半句主干 Wild tomatoes produce pea-sized fruits，which are native to ... 为插入的非限制性定语从句，补充野生番茄的原产地。",
        [w("native to", "phr.", "原产于……的"), w("pea-sized", "adj.", "豌豆大小的")]),
    11: ("历经许多世代，阿兹特克人、印加人等民族通过挑选并培育遗传结构发生突变的植株来改造这种植物，这些突变带来了诸如果实更大等合意性状。",
        "介词短语状语 + 非限制性定语从句",
        "主干 peoples transformed the plant；by selecting and breeding ... 为方式状语；which resulted in ... 为非限制性定语从句，指前面“突变”所导致的结果。",
        [w("breed", "v.", "培育；繁殖"), w("mutation", "n.", "突变")]),
    12: ("但每当从一个较大的种群中取出单独一株带有突变的植株来育种，就会损失大量的遗传多样性。",
        "every time 引导时间状语从句 + 被动语态",
        "every time 引导时间状语从句（相当于 whenever），从句用被动 a single plant is taken；主句 much genetic diversity is lost 同样为被动，强调“多样性被损失”。",
        [w("population", "n.", "（生物）种群"), w("genetic diversity", "n.", "遗传多样性")]),
    13: ("而且有时候，那些合意的突变会连带出不太合意的性状。",
        "主干句",
        "主干 the desirable mutations come with less desirable traits；come with 意为“伴随而来”；desirable 与 less desirable 前后对照，是本篇的核心矛盾。",
        [w("desirable", "adj.", "合意的；理想的"), w("come with", "phr.", "伴随……而来")]),
    14: ("例如，为超市种植的番茄品种就已经丧失了大部分风味。",
        "主干句 + 过去分词定语",
        "主干 the tomato strains have lost much of their flavour；grown for supermarkets 为过去分词短语作后置定语，修饰 strains；此句对应“loss of flavour”一题。",
        [w("strain", "n.", "（动植物）品系；品种"), w("flavour", "n.", "风味")]),
    15: ("通过把现代植物的基因组与其野生近缘种的基因组相比较，生物学家一直在弄清楚植物在驯化过程中发生了哪些遗传变化。",
        "介词短语状语 + 宾语从句",
        "By comparing ... 为方式状语；主干 biologists have been working out ...；what genetic changes occurred 为 working out 的宾语从句；those 指代 the genomes。",
        [w("work out", "phr.", "弄清楚；推算出"), w("relative", "n.", "近缘种；亲缘物种")]),
    16: ("巴西和中国的团队如今已利用这些知识，从头重新引入这些变化，同时保持甚至强化野生品系的合意性状。库德拉的团队总共做了六处改动。",
        "目的状语 + while 让步/伴随状语",
        "第一句主干 The teams have used this knowledge to reintroduce ...；while maintaining or even enhancing ... 为分词状语，表“在……的同时”；第二句为 C 段首句，是独立短句。",
        [w("reintroduce", "v.", "重新引入"), w("enhance", "v.", "增强；提高")]),
    17: ("例如，他们通过编辑一个名为 FRUIT WEIGHT 的基因，把果实的大小增至三倍；又通过编辑另一个名为 MULTIFLORA 的基因，增加了每串番茄的数量。",
        "并列谓语 + by 方式状语",
        "两个并列谓语 tripled the size 与 increased the number，各自后接 by editing a gene 说明手段；triple 意为“使成三倍”，是数字题常考的表达。",
        [w("triple", "v.", "使增至三倍"), w("truss", "n.", "（果实的）串；序")]),
    18: ("尽管历史上对番茄的驯化降低了红色素番茄红素（被认为有潜在的健康益处）的含量，巴西团队却反而设法把它提高了。",
        "While 引导让步状语从句 + 破折号插入",
        "While 引导让步状语从句，主句为 the team managed to boost it instead；两个破折号之间 thought to have potential health benefits 为插入语，补充说明 lycopene。",
        [w("pigment", "n.", "色素"), w("boost", "v.", "提高；增强")]),
    19: ("野生番茄的番茄红素含量是栽培番茄的两倍，而新驯化出的品种更是达到五倍。",
        "分号并列 + 倍数比较",
        "分号连接两个结构对称的分句；twice as much ... as 与 five times as much 均为“倍数 + as much (as)”结构，作数字对比。",
        [w("cultivated", "adj.", "栽培的"), w("twice as much as", "phr.", "是……的两倍")]),
    20: ("“它们相当好吃，”库德拉说。",
        "直接引语 + 倒装",
        "引语作宾语，says Kudla 主谓倒装；quite 在此为“相当地”，程度略强于中文的“挺”。",
        [w("tasty", "adj.", "好吃的；美味的"), w("quite", "adv.", "相当地")]),
    21: ("“味道有点浓。",
        "省略式口语短句",
        "口语中省略主谓，完整为 (It is) a little bit strong；strong 在描述味道时指“味浓、味重”。",
        [w("a little bit", "phr.", "有一点点"), w("strong", "adj.", "（味道）浓的")]),
    22: ("而且非常芳香。”中国团队重新驯化了好几个野生番茄品系，这些品系带有已在栽培番茄身上丢失的合意性状。",
        "引语收尾 + 过去分词定语",
        "前半句 And very aromatic 收束库德拉的引语；后半句主干 The team re-domesticated several strains；lost in domesticated tomatoes 为过去分词短语作定语，修饰 desirable traits。",
        [w("aromatic", "adj.", "芳香的"), w("re-domesticate", "v.", "重新驯化")]),
    23: ("通过这种方式，他们成功培育出一个能抵抗名为“细菌性斑点病”这一常见病害的品系，而这种病害会重创产量。",
        "结果状语 + 非限制性定语从句",
        "主干 they managed to create a strain；resistant to ... 为形容词短语作后置定语修饰 strain；which can devastate yields 为非限制性定语从句，补充 disease 的危害。",
        [w("bacterial spot", "n.", "细菌性斑点病"), w("yield", "n.", "产量")]),
    24: ("他们还培育出另一个品系，它更耐盐，且维生素 C 含量更高。",
        "that 定语从句",
        "主干 They created another strain；that is more salt tolerant and has higher levels of vitamin C 为 that 引导的定语从句，破折号在此起补充强调作用。",
        [w("salt tolerant", "adj.", "耐盐的"), w("vitamin", "n.", "维生素")]),
    25: ("与此同时，纽约州博伊斯·汤普森研究所的乔伊斯·范·埃克（Joyce Van Eck）决定首次用同样的方法来驯化地樱桃（又称金浆果，学名 Physalis pruinosa）。",
        "主干句 + 不定式目的状语",
        "主干 Joyce Van Eck decided to use the same approach；to domesticate ... for the first time 为不定式作目的状语；括号中的拉丁学名为专有名词，翻译时保留。",
        [w("meanwhile", "adv.", "与此同时"), w("goldenberry", "n.", "金浆果")]),
    26: ("这种水果看起来与其近缘的灯笼果（学名 Physalis peruviana）很相似。",
        "主干句 + 分词作定语",
        "主干 This fruit looks similar to the Cape gooseberry；closely related 为过去分词短语作定语，修饰 Cape gooseberry；look similar to 意为“看起来像”。",
        [w("closely related", "phr.", "亲缘关系密切的"), w("gooseberry", "n.", "醋栗；灯笼果")]),
    27: ("地樱桃在美国已有小范围销售，但很难量产，因为这种植物生长蔓生散乱，而且小果实一成熟就会从枝上掉落。",
        "转折 + because 原因状语从句（含两个并列原因）",
        "主干 they are hard to produce；because 引导原因状语从句，其内部 the plant has ... 与 the small fruits fall off ... 为两个并列原因；when ripe 为省略式时间状语（= when they are ripe）。",
        [w("sprawling", "adj.", "蔓生的；散乱伸展的"), w("ripe", "adj.", "成熟的")]),
    28: ("范·埃克的团队已对这种植物进行了编辑，以增大果实、使其生长更紧凑，并防止果实掉落。",
        "目的状语（三个并列不定式）",
        "主干 Van Eck’s team has edited the plants；后接三项并列目的 to increase ... / make ... / to stop ...（并列时不定式符号 to 可省可留）；stop fruits dropping 为 stop + 宾语 + 动名词。",
        [w("compact", "adj.", "紧凑的；密实的"), w("stop ... dropping", "phr.", "防止……掉落")]),
    29: ("“这有潜力成为一种商业作物，”范·埃克说。",
        "直接引语（There’s 存在句）+ 倒装",
        "引语内部为 There’s potential for ... to be ...（“有……的潜力”句型）；主句 says Van Eck 主谓倒装。",
        [w("potential", "n.", "潜力；可能性"), w("commercial", "adj.", "商业的")]),
    30: ("但她补充说，把这项工作继续推进下去会代价高昂，因为需要为使用 CRISPR 技术支付许可费，并获得监管审批。",
        "宾语从句 + because 原因状语从句",
        "主干 she adds that ...；that 引导宾语从句，从句主干 taking the work further would be expensive（动名词短语作主语）；because of the need to ... 说明昂贵的原因。",
        [w("licence", "n.", "许可证；授权"), w("regulatory approval", "n.", "监管审批")]),
    31: ("英国塞恩斯伯里实验室的乔纳森·琼斯（Jonathan Jones）说，这种方法能够推动许多冷门植物的利用。",
        "直接引述 + 倒装",
        "本句为 says 后置的引述结构：引述内容 This approach could boost the use of many obscure plants 在前，says Jonathan Jones ... 在后（主谓倒装）；boost the use of 意为“推动……的使用”。",
        [w("boost", "v.", "推动；促进"), w("obscure", "adj.", "鲜为人知的；冷门的")]),
    32: ("但他认为，新食物很难受到农民和消费者的欢迎，以至于成为新的主粮作物。",
        "so ... that 结果状语从句 + he thinks 后置",
        "主干 it will be hard for new foods to grow so popular ...；so popular ... that they become new staple crops 为 so...that 结果结构；he thinks 后置，表明这是琼斯的判断（态度题信号）。",
        [w("consumer", "n.", "消费者"), w("staple crop", "n.", "主粮作物")]),
    33: ("这三支团队已经把目光投向了其他有望被“送入主流”的植物，包括狗尾草、燕麦草和豇豆。",
        "主干句 + that 定语从句",
        "主干 The three teams have their eye on other plants；that could be ‘catapulted into the mainstream’ 为定语从句修饰 plants；including ... 列举具体植物；have one’s eye on 意为“看中、盯上”。",
        [w("have one’s eye on", "phr.", "看中；盯上"), w("catapult", "v.", "把……猛地送入")]),
    34: ("高彩霞说，通过挑选耐旱或耐热的野生植物，我们就能培育出即便在地球变暖时也能茁壮生长的作物。",
        "方式状语 + 引述插入 + that 定语从句",
        "By choosing ... 为方式状语；says Gao 为插入的引述；主干 we could create crops；that will thrive ... 为定语从句修饰 crops；even as 意为“即便在……的时候”。",
        [w("drought", "n.", "干旱"), w("thrive", "v.", "茁壮成长；兴旺")]),
    35: ("但库德拉不愿透露他的团队盯上了哪些物种，因为 CRISPR 已经把这个过程变得如此简单。",
        "宾语从句 + because 原因状语从句",
        "主干 Kudla didn’t want to reveal ...；which species were in his team’s sights 为 reveal 的宾语从句；because 引导原因状语从句；in one’s sights 意为“在……的视线/目标之内”。",
        [w("reveal", "v.", "透露；揭示"), w("in one’s sights", "phr.", "在……的目标之内")]),
    36: ("“任何具备相应技能的人，都可以走进他们的实验室把这件事做出来。”",
        "直接引语 + 情态动词",
        "主干 Any one could go to their lab and do this；with the right skills 为介词短语作定语修饰 Any one；情态动词 could 在此表“完全有可能做到”，呼应上句“CRISPR 让过程变简单”。",
        [w("skill", "n.", "技能；本领"), w("the right", "phr.", "合适的；恰当的")]),
}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    data["quality"] = "teacher_refined"
    data["phrases"] = PHRASES

    ids = {s["id"] for s in data["sentences"]}
    missing = ids - set(REFINED)
    if missing:
        raise SystemExit(f"REFINED missing sentence ids: {sorted(missing)}")

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

    print(f"refined {PATH} ({len(data['sentences'])} sentences)")


if __name__ == "__main__":
    main()
