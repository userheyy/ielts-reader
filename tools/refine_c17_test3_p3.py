"""Teacher-refine Cambridge IELTS 17 Test 3 Passage 3.

The draft `en` was extracted from the PDF text layer and was badly scrambled:
sentences from different paragraphs were merged and reordered, the title +
reviewer byline were glued into sentence 1, curly quotes/apostrophes came
through as mojibake, and footnote / page-header text leaked into the body.

There is no clean 33-sentence segmentation of the real article, so this script
rebuilds the passage from the true PDF text into 40 natural sentences
(paragraphs 1-10 matching the PDF), rewrites zh/grammar/words for every
sentence, adds phrases, fixes the question evidence_sentence pointers to the new
numbering, and updates index.json (sentence_count 33 -> 40).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test3-p3.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


# ---------------------------------------------------------------------------
# Clean English, rebuilt from the PDF. Curly quotes/apostrophes throughout.
# 40 sentences, paragraphs 1-10.
# ---------------------------------------------------------------------------
SENTENCES = [
    # para 1
    (1, 1, "Katharine L. Shester reviews a book by Jason Barr about the development of New York City."),
    # para 2
    (2, 2, "In Building the Skyline, Jason Barr takes the reader through a detailed history of New York City."),
    (3, 2, "The book combines geology, history, economics, and a lot of data to explain why business clusters developed where they did and how the early decisions of workers and firms shaped the skyline we see today."),
    (4, 2, "Building the Skyline is organized into two distinct parts."),
    (5, 2, "The first is primarily historical and addresses New York’s settlement and growth from 1609 to 1900; the second deals primarily with the 20th century and is a compilation of chapters commenting on different aspects of New York’s urban development."),
    (6, 2, "The tone and organization of the book changes somewhat between the first and second parts, as the latter chapters incorporate aspects of Barr’s related research papers."),
    # para 3
    (7, 3, "Barr begins chapter one by taking the reader on a ‘helicopter time-machine’ ride – giving a fascinating account of how the New York landscape in 1609 might have looked from the sky."),
    (8, 3, "He then moves on to a subterranean walking tour of the city, indicating the location of rock and water below the subsoil, before taking the reader back to the surface."),
    (9, 3, "His love of the city comes through as he describes various fun facts about the location of the New York residence of early 19th-century vice-president Aaron Burr as well as a number of legends about the city."),
    # para 4
    (10, 4, "Chapters two and three take the reader up to the Civil War (1861–1865), with chapter two focusing on the early development of land and the implementation of a grid system in 1811."),
    (11, 4, "Chapter three focuses on land use before the Civil War."),
    (12, 4, "Both chapters are informative and well researched and set the stage for the economic analysis that comes later in the book."),
    (13, 4, "I would have liked Barr to expand upon his claim that existing tenements* prevented skyscrapers in certain neighborhoods because ‘likely no skyscraper developer was interested in performing the necessary “slum clearance”’."),
    (14, 4, "Later in the book, Barr makes the claim that the depth of bedrock** was not a limiting factor for developers, as foundation costs were a small fraction of the cost of development."),
    (15, 4, "At first glance, it is not obvious why slum clearance would be limiting, while more expensive foundations would not."),
    # para 5
    (16, 5, "Chapter four focuses on immigration and the location of neighborhoods and tenements in the late 19th century."),
    (17, 5, "Barr identifies four primary immigrant enclaves and analyzes their locations in terms of the amenities available in the area."),
    (18, 5, "Most of these enclaves were located on the least valuable land, between the industries located on the waterfront and the wealthy neighborhoods bordering Central Park."),
    # para 6
    (19, 6, "Part two of the book begins with a discussion of the economics of skyscraper height."),
    (20, 6, "In chapter five, Barr distinguishes between engineering height, economic height, and developer height — where engineering height is the tallest building that can be safely made at a given time, economic height is the height that is most efficient from society’s point of view, and developer height is the actual height chosen by the developer, who is attempting to maximize return on investment."),
    # para 7
    (21, 7, "Chapter five also has an interesting discussion of the technological advances that led to the construction of skyscrapers."),
    (22, 7, "For example, the introduction of iron and steel skeletal frames made thick, load-bearing walls unnecessary, expanding the usable square footage of buildings and increasing the use of windows and availability of natural light."),
    (23, 7, "Chapter six then presents data on building height throughout the 20th century and uses regression analysis to ‘predict’ building construction."),
    (24, 7, "While less technical than the research paper on which the chapter is based, it is probably more technical than would be preferred by a general audience."),
    # para 8
    (25, 8, "Chapter seven tackles the ‘bedrock myth’, the assumption that the absence of bedrock close to the surface between Downtown and Midtown New York is the reason for skyscrapers not being built between the two urban centers."),
    (26, 8, "Rather, Barr argues that while deeper bedrock does increase foundation costs, these costs were neither prohibitively high nor were they large compared to the overall cost of building a skyscraper."),
    (27, 8, "What I enjoyed the most about this chapter was Barr’s discussion of how foundations are actually built."),
    (28, 8, "He describes the use of caissons, which enable workers to dig down for considerable distances, often below the water table, until they reach bedrock."),
    (29, 8, "Barr’s thorough technological history discusses not only how caissons work, but also the dangers involved."),
    (30, 8, "While this chapter references empirical research papers, it is a relatively easy read."),
    # para 9
    (31, 9, "Chapters eight and nine focus on the birth of Midtown and the building boom of the 1920s."),
    (32, 9, "Chapter eight contains lengthy discussions of urban economic theory that may serve as a distraction to readers primarily interested in New York."),
    (33, 9, "However, they would be well-suited for undergraduates learning about the economics of cities."),
    (34, 9, "In the next chapter, Barr considers two of the primary explanations for the building boom of the 1920s — the first being exuberance, and the second being financing."),
    (35, 9, "He uses data to assess the viability of these two explanations and finds that supply and demand factors explain much of the development of the 1920s; though it enabled the boom, cheap credit was not, he argues, the primary cause."),
    # para 10
    (36, 10, "In the final chapter (chapter 10), Barr discusses another of his empirical papers that estimates Manhattan land values from the mid-19th century to the present day."),
    (37, 10, "The data work that went into these estimations is particularly impressive."),
    (38, 10, "Toward the end of the chapter, Barr assesses ‘whether skyscrapers are a cause or an effect of high land values’."),
    (39, 10, "He finds that changes in land values predict future building height, but the reverse is not true."),
    (40, 10, "The book ends with an epilogue, in which Barr discusses the impact of climate change on the city and makes policy suggestions for New York going forward."),
]


# ---------------------------------------------------------------------------
# Cross-sentence multi-word phrases.
# ---------------------------------------------------------------------------
PHRASES = [
    w("Building the Skyline", "n.", "《建设天际线》（书名）"),
    w("business cluster", "n.", "商业集群"),
    w("urban development", "n.", "城市发展"),
    w("set the stage for", "phr.", "为……做铺垫；为……奠定基础"),
    w("slum clearance", "n.", "贫民窟清理（拆除旧房、腾出用地）"),
    w("limiting factor", "n.", "限制性因素"),
    w("a small fraction of", "phr.", "……的一小部分"),
    w("immigrant enclave", "n.", "移民聚居区"),
    w("load-bearing wall", "n.", "承重墙"),
    w("regression analysis", "n.", "回归分析"),
    w("water table", "n.", "地下水位"),
    w("building boom", "n.", "建筑热潮"),
    w("supply and demand", "n.", "供给与需求"),
    w("land value", "n.", "土地价值"),
]


# ---------------------------------------------------------------------------
# REFINED = { id: (zh, gtype, note, [words]) }  — covers all 40 sentences.
# ---------------------------------------------------------------------------
REFINED = {
    1: (
        "凯瑟琳·L·谢斯特 (Katharine L. Shester) 评论了贾森·巴尔 (Jason Barr) 所著的一本关于纽约市发展的书。",
        "简单句（书评引语）",
        "全句主干 Katharine L. Shester reviews a book；about the development of New York City 作后置定语修饰 book，交代评论对象。这行是整篇书评的引子。",
        [w("review", "v.", "评论；评述")],
    ),
    2: (
        "在《建设天际线》一书中，贾森·巴尔带领读者详尽地回顾了纽约市的历史。",
        "介词短语状语 + 主谓宾",
        "句首 In Building the Skyline 是地点/范围状语；主干是 Jason Barr takes the reader through a detailed history。take sb through sth 意为“带某人梳理／通览某事”。",
        [w("take sb through", "phr.", "带某人梳理／逐一讲解")],
    ),
    3: (
        "本书融合了地质学、历史、经济学以及大量数据，用以解释商业集群为何会在其所在之处形成，以及工人和企业的早期决策如何塑造了我们今天看到的天际线。",
        "主谓宾 + 目的状语 + 两个并列宾语从句",
        "主干 The book combines...；to explain 是目的状语，其后接 why... 和 how... 两个并列的宾语从句；where they did 相当于 where they developed，避免重复。这句概括全书主题，常对应“涵盖多种因素”的题目改写。",
        [w("combine", "v.", "结合；融合"), w("firm", "n.", "公司；企业")],
    ),
    4: (
        "《建设天际线》一书分为两个截然不同的部分。",
        "被动语态",
        "is organized into 为被动结构，强调结构安排；distinct 意为“各不相同的”，为下一句分述两部分做铺垫。",
        [w("distinct", "adj.", "截然不同的；清晰的")],
    ),
    5: (
        "第一部分主要偏历史，讲述纽约自1609年至1900年的定居与发展；第二部分则主要聚焦20世纪，是就纽约城市发展不同方面加以评述的章节合集。",
        "分号并列 + 现在分词定语",
        "分号连接两个并列分句，分述 the first 与 the second；后半句 commenting on... 为现在分词短语作定语，修饰 chapters。分号前后的对比常是配对／判断题的定位点。",
        [w("settlement", "n.", "定居；聚居地"), w("compilation", "n.", "汇编；合集")],
    ),
    6: (
        "全书第一部分和第二部分的基调与结构略有不同，因为后面几章融入了巴尔相关研究论文的内容。",
        "主句 + as 原因状语从句",
        "主干 The tone and organization... changes；as 引导原因状语从句，说明变化的缘由；the latter chapters 指“后面的（第二部分）章节”。",
        [w("tone", "n.", "基调；语气"), w("incorporate", "v.", "纳入；融入")],
    ),
    7: (
        "巴尔在第一章开篇带领读者展开一场“直升机时光机”之旅——生动地描绘了1609年从空中俯瞰纽约会是怎样一番景象。",
        "主干 + 破折号后现在分词补充",
        "主干 Barr begins chapter one by taking the reader on a ride；破折号后 giving a fascinating account of... 是现在分词短语，对前面动作作补充说明；how... might have looked 是 account of 的宾语从句。fascinating（引人入胜）与题目“lacks interest（乏味）”正好相反。",
        [w("fascinating", "adj.", "引人入胜的；极有趣的"), w("account", "n.", "描述；叙述")],
    ),
    8: (
        "随后，他带读者进行一次地下漫步，指出地表土层之下岩石与水的位置，最后再把读者带回地面。",
        "主干 + 现在分词状语 + before 时间状语",
        "主干 He then moves on to a walking tour；indicating... 是现在分词作伴随状语；before taking the reader back 是时间状语，交代动作先后顺序。",
        [w("subterranean", "adj.", "地下的"), w("subsoil", "n.", "（表土之下的）底土")],
    ),
    9: (
        "他描述了有关19世纪初副总统亚伦·伯尔 (Aaron Burr) 纽约住所所在位置的种种趣闻，以及关于这座城市的许多传说，字里行间流露出他对纽约的热爱。",
        "主句 + as 方式/时间状语从句",
        "主干 His love of the city comes through（他对城市的热爱显露出来）；as 引导状语从句，说明这份热爱是“在他描述……时”体现出来的；A as well as B 连接两个并列宾语。come through 意为“（情感等）显露、流露”。",
        [w("come through", "phr.", "（情感、品质）显露出来"), w("legend", "n.", "传说")],
    ),
    10: (
        "第二章和第三章把读者带到南北战争 (1861–1865) 时期，其中第二章聚焦土地的早期开发和1811年网格式街道系统的实施。",
        "主句 + with 复合结构",
        "主干 Chapters two and three take the reader up to the Civil War；with chapter two focusing on... 是 with 复合结构（with + 名词 + 现在分词），补充说明第二章的具体内容。",
        [w("implementation", "n.", "实施；执行"), w("grid system", "n.", "网格式（棋盘式）道路系统")],
    ),
    11: (
        "第三章重点探讨南北战争之前的土地利用。",
        "简单句",
        "主干 Chapter three focuses on land use；before the Civil War 为时间状语，与上一句共同界定这两章的时间范围。",
        [w("land use", "n.", "土地利用")],
    ),
    12: (
        "这两章内容翔实、研究扎实，为本书后文的经济分析做了铺垫。",
        "并列谓语 + 定语从句",
        "主语 Both chapters 后接并列表语 informative 和 (are) well researched，第二个 are 省略；再并列谓语 set the stage for...；that comes later in the book 是定语从句修饰 economic analysis。set the stage for 意为“为……做铺垫”，正对应题目 prepare the reader well。",
        [w("informative", "adj.", "信息量大的；内容翔实的"), w("well researched", "phr.", "研究充分的")],
    ),
    13: (
        "我本希望巴尔能进一步阐述他的一个观点：某些街区已有的廉租公寓阻碍了摩天大楼的兴建，因为“很可能没有哪个摩天大楼开发商愿意去做必要的‘贫民窟清理’”。",
        "would have liked + 宾补 + 同位语从句",
        "主干 I would have liked Barr to expand upon his claim：would have liked 表示过去未能实现的期望，Barr 是宾语，to expand upon... 是宾语补足语。that existing tenements prevented... 不是定语从句，而是解释 claim 具体内容的同位语从句；because 引出巴尔转述的理由。这句是作者提出的疑问，常对应“指出分析中的问题”。",
        [w("would have liked sb to do", "phr.", "本希望某人做某事（但未实现）"), w("expand upon", "phr.", "详加阐述；进一步展开"), w("tenement", "n.", "廉租公寓；旧式多户住宅")],
    ),
    14: (
        "在书的后文，巴尔提出一个观点：基岩的深度并不是开发商面临的限制性因素，因为地基成本只占开发总成本的一小部分。",
        "主句 + 同位语从句 + as 原因状语",
        "主干 Barr makes the claim；that the depth of bedrock was not a limiting factor 是解释 claim 的同位语从句；as foundation costs were... 是原因状语从句。此句与第13句的“slum clearance 有限制作用”形成对照，是作者质疑的两端。",
        [w("bedrock", "n.", "基岩（松软土层下的坚硬岩石）"), w("limiting factor", "n.", "限制性因素")],
    ),
    15: (
        "乍看之下，人们并不清楚为何贫民窟清理会构成限制，而成本更高的地基却不会。",
        "形式主语 it + why 主语从句 + while 对比",
        "it is not obvious 用 it 作形式主语，真正主语是 why slum clearance would be limiting；while more expensive foundations would not 是对比状语，其后省略了 be limiting。这句点出巴尔前后说法的不一致，正是作者指出的“分析中的潜在问题”。",
        [w("at first glance", "phr.", "乍看之下；初看起来"), w("obvious", "adj.", "明显的；显而易见的")],
    ),
    16: (
        "第四章聚焦19世纪末的移民，以及各个社区和廉租公寓的分布位置。",
        "简单句 + 并列宾语",
        "主干 Chapter four focuses on immigration and the location...；in the late 19th century 为时间状语。immigration 与 the location of neighborhoods and tenements 是 on 后的两个并列宾语。",
        [w("immigration", "n.", "移民（现象、过程）"), w("neighborhood", "n.", "街区；社区")],
    ),
    17: (
        "巴尔辨识出四个主要的移民聚居区，并结合该地区可获得的生活设施来分析它们的选址。",
        "并列谓语",
        "主语 Barr 带两个并列谓语 identifies 和 analyzes；in terms of the amenities available 是方式状语（依据什么来分析），available 后置修饰 amenities。amenities（便利设施）是题目 lack of amenities 的关键改写词。",
        [w("enclave", "n.", "聚居区；飞地"), w("amenities", "n.", "（生活）便利设施")],
    ),
    18: (
        "这些聚居区大多位于最不值钱的地块上，夹在滨水一带的工业区与环绕中央公园的富人区之间。",
        "被动语态 + 过去分词定语",
        "主干 Most of these enclaves were located on the least valuable land（被动）；between... and... 补充位置；located on the waterfront 是过去分词短语，后置修饰 industries。“位于最不值钱、夹在工业与富人区之间”与题目“集中在港口附近”不一致，是 NO 的定位句。",
        [w("valuable", "adj.", "值钱的；有价值的"), w("waterfront", "n.", "滨水区；水边地带")],
    ),
    19: (
        "本书第二部分以对摩天大楼高度的经济学讨论开篇。",
        "简单句",
        "主干 Part two of the book begins with a discussion；of the economics of skyscraper height 层层后置修饰 discussion，点明第二部分的切入点。",
        [w("economics", "n.", "经济学；经济因素"), w("skyscraper", "n.", "摩天大楼")],
    ),
    20: (
        "在第五章，巴尔区分了工程高度、经济高度和开发商高度——工程高度指在特定时期能安全建造的最高建筑，经济高度指从社会角度看最有效率的高度，而开发商高度则是开发商实际选定的高度，因为开发商力图实现投资回报最大化。",
        "破折号后 where 引导的多重并列从句",
        "主干 Barr distinguishes between A, B, and C；破折号后 where 引导说明性从句，用三个并列分句分别给三种“高度”下定义；结尾 who is attempting to... 是非限制性定语从句，解释开发商的动机。三种高度的区分是本段核心概念。",
        [w("distinguish between", "phr.", "区分；辨别"), w("maximize", "v.", "使最大化"), w("return on investment", "n.", "投资回报")],
    ),
    21: (
        "第五章还对推动摩天大楼建造的技术进步进行了有趣的讨论。",
        "主谓宾 + 定语从句",
        "主干 Chapter five also has an interesting discussion；that led to the construction of skyscrapers 是定语从句，修饰 technological advances，指出这些进步的作用。",
        [w("technological advance", "n.", "技术进步"), w("construction", "n.", "建造；施工")],
    ),
    22: (
        "例如，铁和钢骨架的引入使厚重的承重墙变得没有必要，从而扩大了建筑的可用面积，并增加了窗户的使用和自然采光。",
        "主谓宾补 + 现在分词结果状语",
        "主干 the introduction... made thick, load-bearing walls unnecessary（made + 宾语 + 宾补 unnecessary）；expanding... and increasing... 是两个并列的现在分词短语，作结果状语，说明由此带来的变化。",
        [w("skeletal frame", "n.", "骨架结构；框架"), w("square footage", "n.", "（建筑）面积")],
    ),
    23: (
        "第六章接着给出20世纪建筑高度的数据，并运用回归分析来“预测”建筑的建造情况。",
        "并列谓语",
        "主语 Chapter six 带两个并列谓语 presents 和 uses；to ‘predict’ building construction 是目的状语。predict 加引号，暗示这只是一种带保留意味的“预测”。",
        [w("present", "v.", "呈现；给出（数据等）"), w("regression analysis", "n.", "回归分析")],
    ),
    24: (
        "尽管这一章不如它所依据的研究论文那样专业，但对一般读者来说恐怕仍然偏技术化了。",
        "while 让步状语 + 比较级",
        "句首 While less technical than... 是让步状语（省略 it is）；主句 it is probably more technical than would be preferred by a general audience，than 引导比较从句。“比一般读者所愿意接受的更技术化”正对应题目“太专业，不适合多数读者”。",
        [w("technical", "adj.", "专业性强的；技术性的"), w("general audience", "n.", "普通读者；大众读者")],
    ),
    25: (
        "第七章处理“基岩神话”，即认为纽约下城与中城之间地表附近缺乏基岩，是这两个城区之间没有建起摩天大楼的原因这一假设。",
        "主谓宾 + 同位语 + 同位语从句",
        "主干 Chapter seven tackles the ‘bedrock myth’；the assumption... 是 bedrock myth 的同位语；that the absence of bedrock... is the reason... 又是解释 assumption 的同位语从句。这个“假设”正是下文要反驳的对象，对应 summary 中“缺乏基岩不能解释摩天大楼缺席于特定区域”。",
        [w("tackle", "v.", "处理；应对（问题）"), w("assumption", "n.", "假设；设想")],
    ),
    26: (
        "相反，巴尔认为，尽管更深的基岩确实会增加地基成本，但这些成本既不至于高得让人却步，与建造一座摩天大楼的总成本相比也算不上高。",
        "宾语从句 + while 让步 + neither...nor 并列",
        "主干 Barr argues that...；that 从句内 while deeper bedrock does increase... 是让步状语（does 表强调）；主句 these costs were neither prohibitively high nor were they large，neither...nor 连接两项，第二项 nor were they 发生部分倒装。这句是对第25句“基岩神话”的反驳。",
        [w("prohibitively", "adv.", "高得令人却步地"), w("compared to", "phr.", "与……相比")],
    ),
    27: (
        "这一章中我最喜欢的，是巴尔关于地基究竟如何建造的讨论。",
        "what 主语从句 + 主系表",
        "What I enjoyed the most about this chapter 是 what 引导的主语从句，作全句主语；was Barr’s discussion... 是系表结构；of how foundations are actually built 是介词 of 后的宾语从句。",
        [w("foundation", "n.", "地基；基础"), w("actually", "adv.", "实际上；真正地")],
    ),
    28: (
        "他描述了沉箱的使用——沉箱能让工人向下挖掘相当长的距离，常常深入地下水位之下，直到触及基岩。",
        "主句 + 非限制性定语从句 + until 从句",
        "主干 He describes the use of caissons；which enable workers to dig down... 是非限制性定语从句，说明沉箱的作用；until they reach bedrock 是时间状语从句，交代挖掘的终点。dig down for considerable distances 正对应 summary 中的“deep excavations（深挖）”。",
        [w("caisson", "n.", "沉箱（水下施工用的箱形结构）"), w("considerable", "adj.", "相当大的；可观的")],
    ),
    29: (
        "巴尔详尽的技术史不仅讲了沉箱如何运作，还谈到了其中涉及的种种危险。",
        "not only...but also 并列宾语",
        "主干 Barr’s thorough technological history discusses...；discusses 后接 not only how... but also the dangers involved 两个并列宾语；involved 后置修饰 dangers。the dangers（危险）正对应 summary 中的“associated risks（相关风险）”。",
        [w("thorough", "adj.", "详尽的；彻底的"), w("involved", "adj.", "涉及的；有关的")],
    ),
    30: (
        "尽管本章引用了实证研究论文，读起来却相对轻松。",
        "while 让步状语从句",
        "While this chapter references empirical research papers 是让步状语从句；主句 it is a relatively easy read。references 在此作动词，意为“引用、提及”。",
        [w("empirical", "adj.", "实证的；以观察／实验为依据的"), w("an easy read", "phr.", "读起来轻松的读物")],
    ),
    31: (
        "第八章和第九章聚焦中城的兴起和20世纪20年代的建筑热潮。",
        "简单句 + 并列宾语",
        "主干 Chapters eight and nine focus on...；the birth of Midtown 与 the building boom of the 1920s 是 on 后的两个并列宾语，点明这两章的主题。",
        [w("birth", "n.", "兴起；诞生"), w("building boom", "n.", "建筑热潮")],
    ),
    32: (
        "第八章包含大量关于城市经济理论的冗长讨论，对主要关注纽约本身的读者来说，这些讨论可能会分散注意力。",
        "主谓宾 + 定语从句",
        "主干 Chapter eight contains lengthy discussions；that may serve as a distraction to... 是定语从句，修饰 discussions；readers 后接过去分词 interested in New York 作定语。“分散注意力／只对部分人有吸引力”对应题目“对某些人吸引力有限”。",
        [w("lengthy", "adj.", "冗长的；过长的"), w("distraction", "n.", "分散注意力的事物")],
    ),
    33: (
        "不过，这些讨论对于学习城市经济学的本科生来说会非常合适。",
        "however 转折 + 主系表",
        "However 表转折，与上一句的“分散注意力”形成对照；主干 they would be well-suited for undergraduates；learning about the economics of cities 是现在分词短语，修饰 undergraduates。作者借此说明这些内容“换个读者群就很合适”。",
        [w("well-suited", "adj.", "非常合适的；很适合的"), w("undergraduate", "n.", "本科生")],
    ),
    34: (
        "下一章里，巴尔考察了对20世纪20年代建筑热潮的两种主要解释——一种是市场的过度乐观情绪，另一种是融资因素。",
        "主谓宾 + 破折号后并列同位语",
        "主干 Barr considers two of the primary explanations；破折号后 the first being exuberance, and the second being financing 是两个并列的独立主格结构，分别点明这两种解释。exuberance 此处指市场“过度乐观、狂热”的情绪。",
        [w("exuberance", "n.", "（市场的）狂热；过度乐观"), w("financing", "n.", "融资；资金筹措")],
    ),
    35: (
        "他用数据评估这两种解释的可信度，发现供求因素解释了20世纪20年代的大部分发展；他认为，廉价信贷虽然助推了这波热潮，却并非首要原因。",
        "并列谓语 + 分号 + he argues 插入语",
        "主干 He uses data to assess... and finds that...，assess 与 finds 并列，finds 后接 that 宾语从句；分号后 though it enabled the boom 是让步状语，cheap credit was not... the primary cause 是主句，he argues 为插入语。“廉价信贷不是首因”是本段的判断题定位点。",
        [w("viability", "n.", "可行性；成立的可能性"), w("cheap credit", "n.", "廉价信贷（低息借贷）")],
    ),
    36: (
        "在最后一章（第10章），巴尔讨论了他的另一篇实证论文，该论文估算了曼哈顿从19世纪中叶至今的土地价值。",
        "主谓宾 + 定语从句",
        "主干 Barr discusses another of his empirical papers；that estimates Manhattan land values... 是定语从句，修饰 papers，说明论文内容；from the mid-19th century to the present day 是时间范围状语。",
        [w("empirical paper", "n.", "实证论文"), w("estimate", "v.", "估算；估计")],
    ),
    37: (
        "为这些估算所做的数据处理工作尤其令人印象深刻。",
        "主系表 + 定语从句",
        "主语 The data work，后接定语从句 that went into these estimations（投入到这些估算中的）；主干为 The data work... is particularly impressive。这句正是作者对该章“最欣赏之处”，对应题目“最令谢斯特印象深刻的是对该主题的研究方式”。",
        [w("go into", "phr.", "被投入到；用于"), w("impressive", "adj.", "令人印象深刻的")],
    ),
    38: (
        "在这一章接近尾声处，巴尔评估了“摩天大楼究竟是高地价的成因还是结果”。",
        "主谓宾 + whether 宾语从句",
        "主干 Barr assesses...；引号内 whether skyscrapers are a cause or an effect of high land values 是 whether 引导的宾语从句，提出一个因果方向的问题；Toward the end of the chapter 为地点/时间状语。",
        [w("assess", "v.", "评估；判断"), w("cause or effect", "phr.", "成因还是结果（因果关系）")],
    ),
    39: (
        "他发现，土地价值的变化能预测未来的建筑高度，但反过来却不成立。",
        "宾语从句 + but 转折",
        "主干 He finds that...；that 从句内 changes in land values predict future building height 是前半，but the reverse is not true 是后半转折，the reverse 指“反方向（用建筑高度预测地价）”。这句给出因果的单向结论。",
        [w("predict", "v.", "预测；预示"), w("the reverse", "n.", "相反的情况；反过来")],
    ),
    40: (
        "全书以一篇结语收尾，巴尔在其中讨论了气候变化对这座城市的影响，并就纽约今后的发展提出政策建议。",
        "主句 + in which 非限制性定语从句",
        "主干 The book ends with an epilogue；in which... 是非限制性定语从句，修饰 epilogue，其内 Barr discusses... and makes... 为并列谓语；going forward 意为“今后、往后”，修饰 policy suggestions for New York。",
        [w("epilogue", "n.", "结语；尾声"), w("going forward", "phr.", "今后；从现在起")],
    ),
}


# New evidence_sentence pointers under the rebuilt 40-sentence numbering.
EVIDENCE = {
    27: 3, 28: 15, 29: 24, 30: 32, 31: 37,
    32: 7, 33: 12, 34: 16, 35: 17,
    36: 25, 37: 26, 38: 26, 39: 28, 40: 29,
}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))

    data["quality"] = "teacher_refined"
    data["phrases"] = PHRASES

    # Rebuild sentences entirely (draft slots were unusable / scrambled).
    new_sentences = []
    for sid, para, en in SENTENCES:
        zh, gtype, note, words = REFINED[sid]
        new_sentences.append({
            "id": sid,
            "para": para,
            "en": en,
            "zh": zh,
            "grammar": {"type": gtype, "note": note},
            "words": words,
        })
    assert len(new_sentences) == 40, len(new_sentences)
    data["sentences"] = new_sentences

    # Fix question evidence_sentence pointers to the new numbering.
    for q in data.get("questions", []):
        for item in q.get("items", []):
            n = item.get("number")
            if n in EVIDENCE:
                item["evidence_sentence"] = EVIDENCE[n]

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Update index.json: sentence_count 33 -> 40, quality.
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    for row in idx.get("passages", []):
        if row.get("id") == data["id"]:
            row["quality"] = "teacher_refined"
            row["sentence_count"] = len(new_sentences)
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"refined {PATH} -> {len(new_sentences)} sentences")


if __name__ == "__main__":
    main()
