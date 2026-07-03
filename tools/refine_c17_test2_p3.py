"""Teacher-refine Cambridge IELTS 17 Test 2 Passage 3 — 'Insight or evolution?'."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test2-p3.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


PHRASES = [
    w("result from", "phr.", "源于；由……造成"),
    w("conventional wisdom", "n.", "传统观点；普遍看法"),
    w("place weight on", "phr.", "重视；看重"),
    w("trial and error", "n.", "反复试验；试错"),
    w("set aside", "phr.", "撇开；把……放在一边"),
    w("pave the way for", "phr.", "为……铺平道路"),
    w("give the lie to", "phr.", "揭穿……的谎言；证明……不实"),
    w("Law of Effect", "n.", "效果律"),
    w("Law of Natural Selection", "n.", "自然选择律"),
    w("On the Origin of Species", "n.", "《物种起源》"),
    w("refrain from", "phr.", "克制；避免（做某事）"),
    w("intelligent design", "n.", "智能设计（论）"),
]


# Cleaned English where the draft had extraction errors.
EN_FIX = {
    # s1: was the pasted title "Insight or evolution?" — repurpose this slot to the
    # italic sub-heading that actually appears under the title in the PDF.
    1: "Two scientists consider the origins of discoveries and other innovative behavior.",
    # s2: strip the sub-heading that was glued in front of the real first body sentence.
    2: "Scientific discovery is popularly believed to result from the sheer genius of such intellectual stars as naturalist Charles Darwin and theoretical physicist Albert Einstein.",
    # s20: remove the stray '2' artifact that had been inserted between two sentences.
    20: "If mutations prove beneficial, then the animal or the scientific theory will continue to thrive and perhaps reproduce. Support for this evolutionary view of behavioral innovation comes from many domains.",
}


# id -> (zh, grammar type, grammar note, [words])
REFINED = {
    1: (
        "两位科学家探讨了各种发现以及其他创新行为的起源。",
        "主谓宾主干句（副标题）",
        "主干是 Two scientists consider the origins；of discoveries and other innovative behavior 是 origins 的后置定语，交代全文议题。",
        [w("origin", "n.", "起源；由来"), w("innovative", "adj.", "创新的")],
    ),
    2: (
        "人们普遍认为，科学发现源自查尔斯·达尔文这类博物学家和阿尔伯特·爱因斯坦这类理论物理学家的纯粹天赋。",
        "被动语态 + 不定式作补足",
        "主干是 Scientific discovery is believed to result from...（is believed 为被动）；such ... as 引出举例；naturalist、theoretical physicist 分别是两位人物的同位语头衔。",
        [w("sheer", "adj.", "纯粹的；完全的"), w("naturalist", "n.", "博物学家")],
    ),
    3: (
        "我们看待这些对科学的独特贡献时，往往忽视了当事人此前的经历，以及那些名气更小的前辈们所付出的努力。",
        "主谓宾 + 并列宾语",
        "主干是 Our view ... disregards A and B；两个宾语 the person's prior experience 与 the efforts of their lesser-known predecessors 并列，是常被题目改写的点。",
        [w("disregard", "v.", "忽视；不理会"), w("predecessor", "n.", "前辈；前人")],
    ),
    4: (
        "传统观点还非常看重灵感在推动突破性科学成就中的作用，仿佛想法会自发地蹦进某人脑中——而且一出现就完整成形、即可派上用场。",
        "主干 + as if 虚拟比喻",
        "主干是 Conventional wisdom places great weight on insight；as if 引导比喻从句，破折号后的 fully formed and functional 补充说明 ideas 的状态。",
        [w("spontaneously", "adv.", "自发地；不由自主地"), w("breakthrough", "adj.", "突破性的")],
    ),
    5: (
        "这种观点或许有一定道理，但也仅止于此。",
        "There be 存在句",
        "There may be some limited truth to this view 直译为“对这一观点可能存在有限的真实性”；limited 是关键限定词，暗示作者随后要转折反驳。",
        [w("limited", "adj.", "有限的")],
    ),
    6: (
        "然而，我们认为这种观点在很大程度上曲解了科学发现的真正本质，也曲解了人类众多其他领域中创造力与创新的本质。",
        "宾语从句 + as well as 并列",
        "believe 后接 that 宾语从句；misrepresents 的宾语由 the real nature of scientific discovery 与 as well as that of...（that 指代 nature）并列构成，however 标志与上句的转折。",
        [w("misrepresent", "v.", "歪曲；误传"), w("realm", "n.", "领域；范围")],
    ),
    7: (
        "撇开达尔文和爱因斯坦这样的伟人不谈——他们的巨大贡献自当受到赞颂——我们认为，创新更像是一个反复试验的过程：前进两步，有时会伴随后退一步，还可能向左或向右挪动一步乃至几步。",
        "现在分词状语 + where 定语从句",
        "Setting aside... 为分词状语，破折号中的 whose 从句补充说明两位伟人；主干是 we suggest that innovation is ...；where 引导定语从句修饰 process，用步伐的比喻描述试错。",
        [w("monumental", "adj.", "巨大的；不朽的"), w("duly", "adv.", "适当地；应当地")],
    ),
    8: (
        "这种关于人类创新的进化式看法，削弱了“创造性天才”的观念，同时承认科学进步具有累积的性质。",
        "主谓 + 并列谓语",
        "主干是 This ... view undermines the notion ... and recognizes the ... nature；undermines 与 recognizes 两个谓语并列，点出作者立场的两个方面。",
        [w("undermine", "v.", "削弱；动摇"), w("cumulative", "adj.", "累积的；渐增的")],
    ),
    9: (
        "不妨看看一位默默无闻的科学家：约翰·尼科尔森，他是20世纪10年代的一位数学物理学家，曾假设外层空间存在“原始元素”。",
        "冒号引出同位语 + who 定语从句",
        "Consider 为祈使句，冒号后 John Nicholson 是 one scientist 的同位语；who postulated... 是定语从句，进一步说明尼科尔森的主张。",
        [w("unheralded", "adj.", "未被宣扬的；默默无闻的"), w("postulate", "v.", "假设；假定")],
    ),
    10: (
        "通过对这些“原始元素”原子的重量进行不同数量的组合，尼科尔森能够推算出当时已知元素周期表中所有元素的重量。",
        "介词短语状语 + 主谓宾",
        "By combining... 是方式状语（动名词短语）；主干是 Nicholson could recover the weights；the then-known 是复合形容词，修饰 periodic table。",
        [w("recover", "v.", "重新得到；推算出"), w("periodic table", "n.", "元素周期表")],
    ),
    11: (
        "考虑到尼科尔森对“原始元素”存在与否的判断是错的——它们其实并不存在——这些成就就更加引人注目了。",
        "given the fact that 让步 + 冒号解释",
        "主干是 These successes are all the more noteworthy；given the fact that... 引出让步背景，冒号后的 they do not actually exist 进一步解释他错在何处。",
        [w("noteworthy", "adj.", "值得注意的；显著的"), w("all the more", "phr.", "更加；愈发")],
    ),
    12: (
        "然而，在他那些常常异想天开的理论和天马行空的猜想之中，尼科尔森也提出了一种关于原子结构的新颖理论。",
        "插入状语 + 主谓宾",
        "Yet 表转折；amid his ... theories and wild speculations 是介词短语作状语，插在主谓之间；主干是 Nicholson also proposed a novel theory。",
        [w("fanciful", "adj.", "异想天开的；不切实际的"), w("speculation", "n.", "猜测；推断")],
    ),
    13: (
        "现代原子理论之父、诺贝尔奖得主尼尔斯·玻尔，正是从这个有趣的想法出发，构想出了他如今声名远扬的原子模型。",
        "同位语 + 不定式表目的",
        "主干是 Niels Bohr jumped off from this idea；the Nobel prize-winning father... 是 Bohr 的同位语；to conceive... 为不定式，说明其“起跳”的结果/目的。",
        [w("conceive", "v.", "构想；想出"), w("jump off from", "phr.", "以……为出发点")],
    ),
    14: (
        "我们该如何理解这个故事呢？",
        "特殊疑问句（be to 结构）",
        "What are we to make of...? 用 be + to do 表示“应当/该怎样”；make of 意为“理解、看待”，此句起承上启下的设问作用。",
        [w("make of", "phr.", "理解；看待")],
    ),
    15: (
        "人们或许会简单地得出结论：科学是一项集体的、累积式的事业。",
        "主谓 + that 宾语从句",
        "主干是 One might conclude that...；that 引导宾语从句，collective 和 cumulative 两个并列形容词点明科学事业的性质。",
        [w("collective", "adj.", "集体的；共同的"), w("enterprise", "n.", "事业；事业心")],
    ),
    16: (
        "这或许没错，但从中还能挖掘出更深一层的洞见。",
        "but 转折 + 不定式作后置定语",
        "That may be true 承接上句；but 转折引出主干 there may be a deeper insight；to be gleaned 为不定式被动式，作 insight 的后置定语（“有待挖掘的”）。",
        [w("glean", "v.", "（逐渐）收集；挖掘"), w("insight", "n.", "洞见；深刻理解")],
    ),
    17: (
        "我们提出，科学在不断演化，就如同动物物种的演化一样。",
        "宾语从句 + much as 比较状语",
        "propose 后接 that 宾语从句 science is constantly evolving；much as species of animals do 是比较状语从句（do 替代 evolve），把科学发展类比为生物进化。",
        [w("constantly", "adv.", "不断地；持续地"), w("much as", "phr.", "正如；就像")],
    ),
    18: (
        "在生物系统中，生物体可能会表现出源自随机基因突变的新特征。",
        "主谓宾 + that 定语从句",
        "主干是 organisms may display new characteristics；that result from random genetic mutations 是定语从句，修饰 characteristics，说明新特征的来源。",
        [w("organism", "n.", "生物体；有机体"), w("mutation", "n.", "突变；变异")],
    ),
    19: (
        "同样地，想法上随机、任意或偶然的“突变”，也可能为科学进步铺平道路。",
        "类比状语 + 主谓宾",
        "In the same way 承接上句的生物类比；主干是 mutations of ideas may help pave the way；random, arbitrary or accidental 三个并列形容词强调这种变化并非刻意为之。",
        [w("arbitrary", "adj.", "任意的；随意的"), w("accidental", "adj.", "偶然的；意外的")],
    ),
    20: (
        "如果这些突变被证明是有益的，那么这种动物或这套科学理论就会继续繁荣发展，甚至得以“繁衍”。对这种行为创新进化观的支持，来自许多不同领域。",
        "if 条件句 + 独立主谓句",
        "第一句是 if 条件句：If mutations prove beneficial 为条件，主句 the animal or the theory will thrive and reproduce 为结果。第二句主干是 Support ... comes from many domains，为下文举例作铺垫。",
        [w("beneficial", "adj.", "有益的；有利的"), w("thrive", "v.", "繁荣；兴旺")],
    ),
    21: (
        "以美国赛马运动中一项影响深远的创新为例。",
        "祈使句",
        "Consider one example... 为祈使结构，用于引出下文的具体案例；of an influential innovation in US horseracing 是 example 的后置定语。",
        [w("influential", "adj.", "有影响力的"), w("horseracing", "n.", "赛马运动")],
    ),
    22: (
        "所谓“阿西-杜西”式的马镫置法——骑手左脚马镫比右脚最多低出25厘米——据信能在椭圆形赛道转弯时带来重要的速度优势。",
        "主谓 + in which 定语从句（被动）",
        "主干是 The ... stirrup placement is believed to confer ... advantages（is believed 为被动）；in which 引导定语从句解释这种置法的具体做法；when turning 是时间状语。",
        [w("stirrup", "n.", "马镫"), w("confer", "v.", "授予；带来")],
    ),
    23: (
        "它是由一位相对默默无闻、名叫杰基·韦斯特罗普的骑师发明的。",
        "被动语态 + 过去分词短语",
        "主干是 It was developed by a jockey（被动语态）；named Jackie Westrope 是过去分词短语，作 jockey 的后置定语。",
        [w("jockey", "n.", "（职业）赛马骑师"), w("relatively", "adv.", "相对地；比较地")],
    ),
    24: (
        "难道韦斯特罗普做过系统的研究，或翻查过大量影像资料，精心谋划要跑赢对手吗？",
        "倒装疑问句（Had + 主语）",
        "Had Westrope conducted... 是 had 提前的一般疑问句（过去完成时）；conducted 与 examined 两个动词并列；in a shrewd plan to outrun 说明其假想的目的。",
        [w("methodical", "adj.", "有条理的；系统的"), w("shrewd", "adj.", "精明的；机敏的")],
    ),
    25: (
        "他难道预见到了骑“阿西-杜西”式所能带来的速度优势吗？答案是否定的。",
        "倒装疑问句 + that 定语从句",
        "又一个 Had he foreseen...? 的过去完成时疑问句；that would be conferred 是定语从句修饰 advantage（此处 that 作从句主语）。PDF 中紧随其后的 “No.” 是作者的自答。",
        [w("foresee", "v.", "预见；预料"), w("advantage", "n.", "优势；好处")],
    ),
    26: (
        "他腿部受了伤，以致无法完全弯曲左膝。",
        "主谓宾 + which 非限定性定语从句",
        "主干是 He suffered a leg injury；which left him unable to... 是非限定性定语从句，修饰整件“受伤”的事，说明其后果。",
        [w("injury", "n.", "受伤；损伤"), w("bend", "v.", "使弯曲")],
    ),
    27: (
        "他这一（骑姿）改变，恰好与左转弯性能的提升不谋而合。",
        "主谓 + 介词短语",
        "主干是 His modification happened to coincide with...；just happened to 强调纯属巧合，而非刻意设计——这正是全文“试错/偶然”论点的关键例证。",
        [w("modification", "n.", "改动；改良"), w("coincide with", "phr.", "与……同时发生；相符")],
    ),
    28: (
        "这促使众多骑手迅速而广泛地采用“阿西-杜西”骑法，这种骑术风格一直延续到今天的纯血马比赛中。",
        "主谓宾 + which 定语从句",
        "主干是 This led to the ... adoption of riding acey-deucy；a racing style which continues... 是同位语加 which 定语从句，说明这一骑法沿用至今。",
        [w("widespread", "adj.", "广泛的；普遍的"), w("thoroughbred", "n.", "纯血马；良种马")],
    ),
    29: (
        "还有大量其他故事表明，崭新的进步可以来自错误、意外事故，也可以来自纯粹的机缘巧合——一种幸运的偶然。",
        "主谓 + that 宾语从句 + 破折号同位",
        "主干是 Plenty of other stories show that...；宾语从句里 fresh advances can arise from A, B, and C；破折号后的 a happy accident 是对 serendipity 的同位解释。",
        [w("misadventure", "n.", "不幸的遭遇；意外事故"), w("serendipity", "n.", "机缘巧合；意外发现的运气")],
    ),
    30: (
        "例如，20世纪70年代初，3M公司的两名员工各自遇到了一个难题：斯宾塞·西尔弗手上有一款产品——一种黏性极弱的胶水——却派不上用场；而他的同事阿特·弗莱正苦于如何在赞美诗集里贴上临时书签又不损坏书页。",
        "冒号列举 + while 对比",
        "主干是 two employees each had a problem；冒号后用 while 对照两人各自的困境；两处破折号分别插入对 product 的说明和补足信息。",
        [w("affix", "v.", "贴上；附加"), w("sticky", "adj.", "黏的；有黏性的")],
    ),
    31: (
        "这两个难题的解决方案，就是那款设计精妙绝伦、又大获成功的“便利贴”的诞生。",
        "主系表结构",
        "主干是 The solution ... was the invention of ... note；brilliantly simple yet phenomenally successful 用 yet 连接两个看似矛盾的评价，强调其“简单却极成功”。",
        [w("phenomenally", "adv.", "非凡地；惊人地"), w("invention", "n.", "发明；创造")],
    ),
    32: (
        "这类例子戳穿了一种说法——即人类的创造力和发明，靠的是那些足智多谋、善于设计的头脑。",
        "主谓宾 + that 同位语从句",
        "主干是 Such examples give lie to the claim；that ingenious ... minds are responsible for... 是 claim 的同位语从句，give the lie to 意为“证明……是假的”。",
        [w("ingenious", "adj.", "巧妙的；足智多谋的"), w("be responsible for", "phr.", "对……负责；是……的原因")],
    ),
    33: (
        "起作用的，可能是些远为平淡、机械的力量——这些力量从根本上与科学规律相连。",
        "主谓 + 分号 + that 定语从句",
        "主干是 Far more banal and mechanical forces may be at work；分号后 forces that are ... connected to the laws of science 用 that 定语从句进一步限定这些“力量”的性质。",
        [w("banal", "adj.", "平庸的；陈腐的"), w("at work", "phr.", "在起作用；在运转")],
    ),
    34: (
        "洞见、创造力和天才这些概念常被人提起，却依旧含混不清、科学价值存疑——尤其当我们想到柏拉图、达·芬奇、莎士比亚、贝多芬、伽利略、牛顿、开普勒、居里、巴斯德和爱迪生等人那多样而持久的贡献时。",
        "并列谓语 + when 时间/条件状语从句",
        "主干是 The notions ... are invoked, but they remain vague and of ... utility；especially when one considers... 是状语从句，用一长串人名举例来质疑这些概念的解释力。",
        [w("invoke", "v.", "援引；提及"), w("enduring", "adj.", "持久的；经久不衰的")],
    ),
    35: (
        "这些概念只是给人类创新的演化贴上了标签，却并未加以解释。",
        "rather than 对比结构",
        "主干是 These notions merely label ... the evolution；label rather than explain 用 rather than 构成对比，点出“只命名、不解释”正是作者对旧概念的核心批评。",
        [w("label", "v.", "贴标签；归类"), w("evolution", "n.", "演化；演变")],
    ),
    36: (
        "我们需要另一种思路，而恰好有一个颇具前景的备选方案。",
        "并列句",
        "两个分句由 and 并列：前句 We need another approach 表明需求，后句 there is a promising candidate 用 There be 句型引出下文将要介绍的“效果律”。",
        [w("promising", "adj.", "有前途的；有希望的"), w("candidate", "n.", "候选者；备选方案")],
    ),
    37: (
        "效果律由心理学家爱德华·桑代克于1898年提出，那时距查尔斯·达尔文发表其关于生物进化的开创性著作《物种起源》已约40年。",
        "被动语态 + 同位语 + 时间状语",
        "主干是 The Law of Effect was advanced by ... Thorndike（被动）；some 40 years after Charles Darwin published... 是时间状语，On the Origin of Species 是 work 的同位语。",
        [w("advance", "v.", "提出（理论）；推进"), w("groundbreaking", "adj.", "开创性的；突破性的")],
    ),
    38: (
        "这一简单的定律认为，生物体倾向于重复成功的行为，而避免去做那些不成功的行为。",
        "主谓 + that 宾语从句",
        "主干是 This simple law holds that...；hold 意为“认为、主张”；宾语从句里 tend to repeat ... and to refrain from... 两个不定式并列，构成对比。",
        [w("refrain from", "phr.", "克制；避免（做某事）"), w("tend to", "phr.", "倾向于；往往会")],
    ),
    39: (
        "正如达尔文的自然选择律一样，效果律所涉及的完全是一个变异与选择的机械过程，其中并无任何预设的最终目标。",
        "比较状语 + 主谓宾",
        "Just like Darwin's Law of Natural Selection 是比较状语；主干是 the Law of Effect involves a ... process of variation and selection；without any end objective in sight 是介词短语，强调“无目的性”。",
        [w("variation", "n.", "变异；变化"), w("objective", "n.", "目标；目的")],
    ),
    40: (
        "当然，人类创新的起源还有待深入研究。",
        "主谓宾主干句",
        "主干是 the origin ... demands much further study；Of course 为插入语，承认作者立场尚需佐证；demands 在此意为“需要”。",
        [w("demand", "v.", "需要；要求"), w("further", "adj.", "进一步的；更多的")],
    ),
    41: (
        "尤其是，效果律所依据的“原材料”从何而来，其了解程度还不如自然选择律所依据的基因突变来得清楚。",
        "not as ... as 比较 + 双重 on which 定语从句",
        "主干是 the provenance ... is not as clearly known as that of the genetic mutations（that 指代 provenance）；两个 on which 定语从句分别修饰 raw material 和 mutations，形成对照。",
        [w("provenance", "n.", "起源；出处"), w("raw material", "n.", "原材料")],
    ),
    42: (
        "新奇想法和行为的产生，也许并非完全随机，而是受到既往成败的制约——既包括当事人本人（如玻尔）的成败，也包括前辈（如尼科尔森）的成败。",
        "not ... but 转折 + 破折号补充",
        "主干是 The generation ... may not be entirely random, but constrained by...；not ... but 构成对比；破折号后的 of the current individual ... or of predecessors 说明“成败”的来源。",
        [w("constrained", "adj.", "受约束的；受限制的"), w("generation", "n.", "产生；生成")],
    ),
    43: (
        "现在似乎正是时候，去摒弃“智能设计”和“天才”这类幼稚的观念，转而以科学的方式探究创造性行为的真正起源。",
        "主系表 + 并列不定式（for + 动名词）",
        "主干是 The time seems right for A and for B；两个 for + 动名词短语（abandoning... 与 exploring...）并列，构成作者的呼吁式收尾。",
        [w("abandon", "v.", "放弃；摒弃"), w("naive", "adj.", "天真的；幼稚的")],
    ),
}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    data["quality"] = "teacher_refined"
    data["phrases"] = PHRASES

    missing = [s["id"] for s in data["sentences"] if s["id"] not in REFINED]
    if missing:
        raise SystemExit(f"REFINED missing ids: {missing}")

    for s in data["sentences"]:
        if s["id"] in EN_FIX:
            s["en"] = EN_FIX[s["id"]]
        zh, gtype, note, words = REFINED[s["id"]]
        s["zh"] = zh
        s["grammar"] = {"type": gtype, "note": note}
        s["words"] = words

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    for row in idx.get("passages", []):
        if row.get("id") == data["id"]:
            row["quality"] = "teacher_refined"
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"refined {PATH} ({len(data['sentences'])} sentences)")


if __name__ == "__main__":
    main()
