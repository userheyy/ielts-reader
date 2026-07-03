"""Teacher-refine Cambridge IELTS 17 Test 4 Passage 2: Does education fuel economic growth?"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test4-p2.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


PHRASES = [
    w("economic growth", "n.", "经济增长"),
    w("literacy rate", "n.", "识字率"),
    w("causal link", "n.", "因果联系"),
    w("cross-country analysis", "n.", "跨国（对比）分析"),
    w("demographic reconstruction", "n.", "人口重建（还原历史人口结构）"),
    w("hold wealth constant", "phr.", "控制财富水平不变"),
    w("industrial innovation", "n.", "工业创新"),
    w("tipping point", "n.", "临界点；引爆点"),
    w("far from straightforward", "phr.", "远非简单明了"),
    w("hold back", "phr.", "阻碍；妨碍"),
    w("guild", "n.", "行会（工匠或商人组成、监管本行业的组织）"),
]


# EN fixes: only where the draft merged in headers/footnotes/section letters or lost text.
EN_FIX = {
    # sentence 14 had the guild footnote, the "Test 4" page header, the section letter "D"
    # and the first sentence of paragraph D all glued onto the end. Strip all of that;
    # keep only the real end-of-paragraph-C sentence.
    14: "According to Ogilvie, the database provides multiple indicators for the same individuals, making it possible to analyse links between literacy, numeracy, wealth, and industriousness, for individual women and men over the long term.",
    # the opening sentence of paragraph D ("Ogilvie and her team have been building...") had been
    # swallowed by sentence 14's garbage. Restore it by prepending it to sentence 15 so no body
    # text is lost and the sentence count stays at 38.
    15: "Ogilvie and her team have been building the vast database of material possessions on top of their full demographic reconstruction of the people who lived in these two German communities. ‘We can follow the same people – and their descendants – across 300 years of educational and economic change,’ she says.",
}


# Full rewrite: {id: (zh, gtype, note, [words])}
REFINED = {
    1: (
        "教育能否推动经济增长？",
        "标题设问",
        "全文标题，用一般疑问句形式提出核心议题：education（教育）与 economic growth（经济增长）之间是否存在推动关系；fuel 在此作动词，表“助长、驱动”。",
        [w("fuel", "v.", "助长；驱动"), w("economic growth", "n.", "经济增长")],
    ),
    2: (
        "过去十年间，剑桥大学经济学院希拉·奥格尔维（Sheilagh Ogilvie）教授领衔的团队，编制了一个关于 1600 至 1900 年间德国西南部村民生活的庞大数据库。",
        "被动语态 + 过去分词短语作后置定语",
        "主干是 a huge database... has been compiled（被动语态，强调数据库本身而非施动者）；about the lives of... 修饰 database；led by... 是过去分词短语作后置定语，修饰 a team。",
        [w("compile", "v.", "编制；汇编"), w("database", "n.", "数据库")],
    ),
    3: (
        "它包括法庭记录、行会账簿、教区登记册、村庄人口普查、纳税清单，以及最新增补的 9,000 份手写清单——这些清单列出了三个世纪以来普通男女所拥有的逾百万件个人物品。",
        "主谓宾 + 破折号插入补充",
        "主干是 It includes... 后接一串并列宾语；两个破折号之间的 the most recent addition 是插入语，补充说明紧随其后的 9,000 handwritten inventories；listing... 是现在分词短语，说明这些清单的内容。",
        [w("guild", "n.", "行会"), w("inventory", "n.", "清单；财产清册")],
    ),
    4: (
        "奥格尔维 30 年前在两个德国社区的档案里发现了这些清单，她相信这些清单或许能解答一个长期困扰经济学家的难题：教育与一国经济增长之间缺乏因果关系的证据。",
        "非限制性定语从句 + 冒号解释",
        "主干是 Ogilvie... believes they may hold the answer；who discovered... 是插入的非限制性定语从句，补充奥格尔维的背景；that has long puzzled economists 修饰 conundrum；冒号后的名词短语 the lack of evidence... 具体解释 conundrum 到底是什么。",
        [w("conundrum", "n.", "难题；谜题"), w("causal link", "n.", "因果联系")],
    ),
    5: (
        "正如奥格尔维所解释的：“教育帮助我们更高效地工作、发明更好的技术、赚得更多……它对经济增长想必是至关重要的吧？",
        "As 引导方式状语 + 直接引语内的设问",
        "As Ogilvie explains 是方式状语，引出后面的直接引语；引语主干是 Education helps us to...，后接三个并列不定式 work / invent / earn；破折号省略号后的 surely it must be critical...? 用反问表达“看似理所当然”的推断。",
        [w("productively", "adv.", "高效地；富有成效地"), w("critical", "adj.", "至关重要的")],
    ),
    6: (
        "但是，如果你回顾历史，就会发现没有任何证据表明高识字率能让一个国家更早实现工业化。”1600 至 1900 年间，按欧洲标准衡量，英国的识字率仅属中等，其经济却增长迅速，还成为第一个实现工业化的国家。",
        "条件状语从句 + 让步转折（yet）",
        "引语部分主干是 there's no evidence that...，that 引导同位语从句解释 evidence 的内容，其中 having a high literacy rate 是动名词作主语；引语结束后另起一句，主干是 England had... literacy rates，yet 引出转折——识字率中等，经济却增长快、工业化早。",
        [w("literacy rate", "n.", "识字率"), w("mediocre", "adj.", "平庸的；中等的")],
    ),
    7: (
        "而同一时期，德国和斯堪的纳维亚地区识字率极高，经济增长却很缓慢，工业化也来得晚。",
        "并列句（but 转折对比）",
        "本句与上一句形成对照：主干是 Germany and Scandinavia had excellent literacy rates，but 之后 their economies grew slowly and they industrialised late 是并列谓语，说明高识字率并未带来快速增长——这正是常被出题改写的“反例”。",
        [w("literacy rate", "n.", "识字率"), w("industrialise", "v.", "（使）工业化")],
    ),
    8: (
        "“现代的跨国对比分析也很难找到教育促进经济增长的证据，尽管有大量证据表明是经济增长带动了教育，”她补充道。",
        "宾语从句 + even though 让步状语从句",
        "引语主干是 analyses have struggled to find evidence；that education causes economic growth 是同位语从句说明 evidence 内容；even though 引导让步从句，点出因果方向恰恰相反——是 growth increases education，这一“方向倒置”是理解全文的关键。",
        [w("cross-country analysis", "n.", "跨国对比分析"), w("struggle to", "phr.", "难以；费力去做")],
    ),
    9: (
        "在奥格尔维正在分析的这些手写清单中，记录着人们在结婚、再婚和离世时所拥有的财产。",
        "完全倒装句 + 定语从句",
        "本句是地点状语前置引起的完全倒装：正常语序为 the belongings of women and men... are in the handwritten inventories；that Ogilvie is analysing 是定语从句修饰 inventories；at marriage, remarriage and death 说明记录财产的三个人生时点。",
        [w("belongings", "n.", "财物；所有物"), w("remarriage", "n.", "再婚")],
    ),
    10: (
        "从獾皮到《圣经》，从缝纫机到猩红色的紧身胸衣——村民们全部的世俗家当都被囊括其中。",
        "破折号前置列举 + 被动语态主干",
        "破折号前用 From... to..., ... to... 结构罗列各式物品，起铺陈作用；破折号后才是句子主干 the villagers' entire worldly goods are included（被动语态），强调“无所不包”。",
        [w("worldly goods", "phr.", "世俗财产；家当"), w("bodice", "n.", "紧身胸衣")],
    ),
    11: (
        "农具和手工工具的清单揭示了经济活动；书籍以及钢笔、石板等与教育相关的物品的拥有情况，则暗示了人们的学习方式。",
        "分号并列的两个分句",
        "分号连接两个结构平行的分句：前句主干 Inventories... reveal economic activities，后句主干 ownership... suggests how people learned；suggests 后接 how 引导的宾语从句。分号常是信息并列点，也是出题定位高频处。",
        [w("agricultural equipment", "n.", "农业设备"), w("slate", "n.", "石板（旧时书写用）")],
    ),
    12: (
        "此外，数据库中收录的纳税清单记录了农场、作坊、资产与债务的价值；签名以及人们对自己年龄的估算，反映出识字与算术水平；法庭记录则揭示了扼杀工业发展的种种障碍（如行会*的活动）。",
        "分号并列的三个分句 + 括号举例",
        "In addition 承接上文继续举例；三个由分号隔开的分句结构平行（tax lists record... / signatures and... estimates indicate... / court records reveal...）；included in the database 是过去分词短语修饰 tax lists；括号内 such as... 举例说明 obstacles。",
        [w("numeracy", "n.", "计算能力；算术能力"), w("stifle", "v.", "扼杀；抑制")],
    ),
    13: (
        "以往的研究通常只用一种方式把教育和经济增长挂钩——也许是看有没有学校和印刷机，或看入学率，又或看能否签写自己的名字。",
        "主干 + 破折号后同位列举",
        "主干是 Previous studies had just one way of linking education with economic growth；破折号后用 the presence of...  or... or... 列举“那一种方式”可能的几种具体形式，是对 one way 的同位补充；这种“单一指标”与下文奥格尔维的“多重指标”形成对比。",
        [w("enrolment", "n.", "入学（人数）；注册"), w("printing press", "n.", "印刷机")],
    ),
    14: (
        "奥格尔维指出，该数据库能为同一批人提供多重指标，从而得以就每一位女性和男性，长期追踪其识字、算术、财富与勤勉程度之间的关联。",
        "主干 + 现在分词短语表结果",
        "主干是 the database provides multiple indicators for the same individuals；making it possible to analyse links... 是现在分词短语作结果状语，其中 it 是形式宾语，真正宾语是 to analyse links...；between literacy, numeracy, wealth, and industriousness 说明所比较的四类指标。",
        [w("indicator", "n.", "指标"), w("industriousness", "n.", "勤勉；勤奋")],
    ),
    15: (
        "奥格尔维和她的团队在对这两个德国社区居民所做的完整人口重建之上，进一步构建了这个庞大的物质财产数据库。她说：“我们能够追踪同一批人——以及他们的后代——跨越 300 年的教育与经济变迁。”",
        "现在完成进行时 + 直接引语",
        "第一句主干是 Ogilvie and her team have been building the vast database（现在完成进行时，强调持续进行的工作），on top of... 表“在……的基础之上”，who lived in... 修饰 the people；第二句为直接引语，两处破折号之间 and their descendants 是插入补充，与题目考点 descendants 对应。",
        [w("demographic reconstruction", "n.", "人口重建"), w("descendant", "n.", "后代；后裔")],
    ),
    16: (
        "一个个鲜活的人生就这样在他们眼前徐徐展开。",
        "现在完成时短句",
        "结构简短：主干是 Individual lives have unfolded；before their eyes 是地点状语，形象地表达“研究者仿佛亲眼见证”；unfold 在此比喻人生像画卷一样逐渐铺展。",
        [w("unfold", "v.", "展开；徐徐呈现")],
    ),
    17: (
        "比如那两位 24 岁的姑娘安娜·雷吉娜（Ana Regina）和玛格达莱娜·里特米勒林（Magdalena Riethmüllerin）的故事——她们在 1707 年因在教堂里看书、而非聆听布道，遭到了训诫。",
        "名词短语 + 非限制性定语从句",
        "本句以名词短语 Stories like that of... 起首（that 指代 the story，避免重复）；who were chastised... 是非限制性定语从句，交代二人被训诫的原因；instead of listening to the sermon 用 instead of 表对比——sermon 正是题目所考的词。",
        [w("chastise", "v.", "训诫；责罚"), w("sermon", "n.", "布道；讲道")],
    ),
    18: (
        "“这说明她们在离校之后至少又坚持提升了十年的阅读能力，”奥格尔维解释道。",
        "宾语从句 + 时间状语",
        "引语主干是 This tells us (that) they were continuing to develop their reading skills，tells 后省略了 that 引导的宾语从句；at least a decade after leaving school 是时间状语，说明“离校后仍持续学习”，据此推断当时识字并非止步于学校。",
        [w("continue to", "phr.", "继续（做）"), w("at least", "phr.", "至少")],
    ),
    19: (
        "数据库还披露了朱莉安娜·施韦克赫特（Juliana Schweickherdt）的案例：她是住在黑森林小镇维尔德贝格（Wildberg）的一位 50 岁未婚女子，1752 年被当地织工行会申斥，罪名是“违反行会条例织布、梳理羊毛”。",
        "主干 + 非限制性定语从句",
        "主干是 The database reveals the case of Juliana Schweickherdt；a 50-year-old spinster... 是同位语，进一步说明她的身份，其中 living in... 是现在分词短语作定语；who was reprimanded... 是非限制性定语从句，for 引出被申斥的原因，引号内是行会给出的“罪名”。",
        [w("spinster", "n.", "老处女；未婚女子"), w("reprimand", "v.", "申斥；谴责")],
    ),
    20: (
        "当朱莉安娜继续承接那些专属于男性行会成员的活计时，她被传唤到行会法庭，并被勒令缴纳一笔相当于仆人年薪三分之一的罚款。",
        "When 时间状语从句 + 被动语态并列谓语",
        "When 引导时间状语从句 When Juliana continued taking jobs...，reserved for male guild members 是过去分词短语修饰 jobs；主句主干为被动语态的并列谓语 she was summoned... and told to pay a fine；equivalent to... 修饰 fine，说明罚款数额——fine 是题目考点。",
        [w("summon", "v.", "传唤；召唤"), w("equivalent to", "phr.", "相当于")],
    ),
    21: (
        "以今天的标准看，这不过是小小的一次抗命，却折射出一个时代——在德国乃至别处，法律都限制着人们进入劳动力市场。",
        "并列句（but 转折）+ when 定语从句",
        "两个分句由 but 连接：前句 It was a small act of defiance（by today's standards 是状语），后句 it reflects a time；when laws... regulated people's access... 是定语从句修饰 a time，说明那是个“法律管制就业”的年代。",
        [w("defiance", "n.", "违抗；反抗"), w("access to", "phr.", "进入……的权利/机会")],
    ),
    22: (
        "行会的垄断地位不仅使人们无法施展技能，甚至连最简单的工业创新也横加阻挠。",
        "not only... but also 递进",
        "主干是 The dominance of guilds prevented... but also held back...；not only... but also... 是递进结构，从“妨碍个人发挥技能”递进到“阻碍工业创新”，程度加深；even the simplest 强调“连最基本的创新都被压制”。innovation 是题目考点。",
        [w("dominance", "n.", "支配地位；主导"), w("industrial innovation", "n.", "工业创新")],
    ),
    23: (
        "奥格尔维表示，项目的数据采集阶段已经完成，如今“是时候提出那些重大问题了”。",
        "并列主干 + according to 插入语",
        "两个分句由 and 连接：前句 The data-gathering phase has been completed（现在完成时被动语态，表阶段收尾），后句 it is time 'to ask the big questions'（it is time to do 表“该做某事了”）；according to Ogilvie 是插入语，标明这是她的说法。",
        [w("data-gathering", "n.", "数据采集"), w("phase", "n.", "阶段")],
    ),
    24: (
        "考察教育是否促进经济增长的一种方法，是“把财富水平固定下来”。",
        "不定式作主语补足语",
        "主干是 One way... is to 'hold wealth constant'；to look at whether... 是不定式短语作 One way 的后置定语，whether 引导宾语从句；系动词 is 后的不定式 to hold... 作表语，hold... constant 是“hold + 宾语 + 形容词”结构，意为“使……保持不变”。",
        [w("hold wealth constant", "phr.", "控制财富水平不变"), w("cause", "v.", "导致；引起")],
    ),
    25: (
        "这意味着要在一段时间内，追踪一批财富水平相同的不同人的人生轨迹。",
        "动名词作宾语",
        "主干是 This involves following the lives...；involve 后接动名词 following 作宾语；with the same level of wealth 是介词短语作定语，修饰 different people；over a period of time 是时间状语。此句解释上一句“hold wealth constant”具体怎么操作。",
        [w("involve", "v.", "涉及；需要"), w("over a period of time", "phr.", "在一段时间内")],
    ),
    26: (
        "一旦财富保持恒定，就有可能查明教育是否与某些行为有关，比如种植新作物，或采用缝纫机之类的工业创新。",
        "If 条件状语从句 + 宾语从句",
        "If wealth is constant 是条件状语从句；主句 it is possible to discover whether... 中 it 是形式主语，真正主语是不定式 to discover...；whether 引导宾语从句，was linked to A or (to) B 是并列结构，for example / like 引出例子。",
        [w("cultivation", "n.", "种植；栽培"), w("adoption", "n.", "采用；采纳")],
    ),
    27: (
        "团队还将追问：究竟是教育的哪个方面，促使人们更多地投身于生产性与创新性的活动。",
        "宾语从句（what 引导）",
        "主干是 The team will ask what aspect of education helped...；what aspect of education 是宾语从句的主语；helped people engage more with... 中 help sb (to) do 省略了 to，engage with 意为“参与、投入”。此句提出下文一连串具体设问的总纲。",
        [w("aspect", "n.", "方面"), w("engage with", "phr.", "参与；投入")],
    ),
    28: (
        "比如说，起作用的到底是识字能力、算术能力、藏书量，还是受教育的年限？",
        "省略式并列疑问句",
        "本句承接上句 what aspect，用一般疑问句列举可能的“方面”：Was it, for instance, A, B, C, D? 主干 Was it，后面并列若干名词短语；for instance 是插入语，表举例。这类罗列常被改写成题目选项。",
        [w("literacy", "n.", "识字能力"), w("numeracy", "n.", "计算能力")],
    ),
    29: (
        "是否存在一个必须跨过的门槛值——一个引爆点——达到之后才会影响经济表现？",
        "定语从句 + 破折号同位语",
        "主干是 Was there a threshold level？（there be 句型的疑问式）；a tipping point 是破折号内的同位语，形象解释 threshold level；that needed to be reached 是定语从句修饰 threshold level，to affect economic performance 是不定式表目的/结果。",
        [w("threshold", "n.", "门槛；临界值"), w("tipping point", "n.", "引爆点；临界点")],
    ),
    30: (
        "奥格尔维希望在未来几年里，开始为这些问题找到答案。",
        "主干句 + 不定式作宾语",
        "结构简明：主干是 Ogilvie hopes to start finding answers；hope to do 表“希望做某事”，start doing 表“开始做某事”；over the next few years 是时间状语，呼应上文项目“数据已备、正待分析”的阶段。",
        [w("hope to", "phr.", "希望（做）"), w("over the next few years", "phr.", "在未来几年里")],
    ),
    31: (
        "她说，有一点已经很清楚：教育与经济增长之间的关系，远非简单明了。",
        "主干 + 冒号解释",
        "主干是 One thing is already clear；she says 是插入语；冒号后 the relationship... is far from straightforward 具体说明“已经清楚的那件事”是什么；far from 意为“远非、绝不”，是强调“不简单”的常用表达。",
        [w("far from straightforward", "phr.", "远非简单明了"), w("relationship", "n.", "关系")],
    ),
    32: (
        "“说德语的中欧地区，是检验经济增长理论的绝佳实验室，”她解释道。",
        "主系表 + 比喻",
        "引语是一个主系表结构：主干 German-speaking central Europe is an excellent laboratory；for testing theories of economic growth 是介词短语作定语，说明这个“实验室”用于什么；laboratory 在此为比喻，指“理想的研究样本地”。",
        [w("laboratory", "n.", "实验室"), w("theory", "n.", "理论")],
    ),
    33: (
        "1600 至 1900 年间，那里的识字率和藏书量都很高，可这一地区却始终贫穷。",
        "并列句（and yet 转折）",
        "两个分句由 and yet 连接，形成鲜明反差：前句 literacy rates and book ownership were high，后句 the region remained poor；and yet 强调“高教育水平与贫穷并存”，正是全文用来质疑“教育必然带来增长”的核心证据。",
        [w("literacy rate", "n.", "识字率"), w("book ownership", "n.", "藏书（拥有）情况")],
    ),
    34: (
        "还有一个情况是：当地行会和商人协会势力极大，会立法抵制一切损害其垄断利益的事物。",
        "It was the case that + 定语从句",
        "It was also the case that... 是形式主语句型，that 引导真正的主语从句；从句主干 local guilds and merchant associations were powerful and legislated against anything；that undermined their monopolies 是定语从句修饰 anything，说明它们抵制什么。",
        [w("merchant association", "n.", "商人协会"), w("monopoly", "n.", "垄断")],
    ),
    35: (
        "在这一地区的各个村庄里，行会阻断劳动力流动，并抵制任何可能削弱自身影响力的变革。",
        "并列谓语 + 定语从句",
        "主干是 guilds blocked labour migration and resisted changes（and 连接两个并列谓语）；In villages throughout the region 是地点状语；that might reduce their influence 是定语从句修饰 changes，说明行会所抵制的“变革”是哪一类——这与题目 25“反对为工作而迁移”直接对应。",
        [w("labour migration", "n.", "劳动力迁移/流动"), w("resist", "v.", "抵制；反抗")],
    ),
    36: (
        "“早期研究结果表明，教育对经济的潜在益处，可能被其他障碍所压制，而这对当今也具有借鉴意义，”奥格尔维说。",
        "宾语从句 + 被动语态",
        "引语主干是 Early findings suggest that...，that 引导宾语从句；从句主干 the potential benefits... can be held back by other barriers 是被动语态，held back 意为“被阻碍、被压制”；and this has implications for today 是并列分句，把历史结论引向现实启示。",
        [w("hold back", "phr.", "阻碍；压制"), w("implications", "n.", "影响；启示")],
    ),
    37: (
        "“如今人们在发展中国家投入巨资改善教育，但假如种种限制阻止人们——尤其是妇女和穷人——以经济上有产出的方式运用所受的教育，这笔投入就可能无法转化为经济增长。",
        "被动语态主干 + if 条件状语从句",
        "主干是 Huge amounts are spent improving education（被动语态，are spent doing 表“被花在做某事上”）；but 后 this spending can fail to deliver economic growth 是转折；if restrictions block people from using... 是条件状语从句，block sb from doing 表“阻止某人做某事”，两处破折号之间 especially women and the poor 是插入补充。",
        [w("developing countries", "n.", "发展中国家"), w("deliver", "v.", "带来；实现")],
    ),
    38: (
        "举例来说，如果经济制度建设得不健全，教育就无法带来增长。”",
        "If 条件状语从句 + 主句",
        "If economic institutions are poorly set up 是条件状语从句，set up 意为“建立、构建”，poorly set up 即“建得不好”；主句 education can't lead to growth 点明结论；for instance 是插入语。全句为奥格尔维的收束之语，强调“制度”是教育转化为增长的前提。",
        [w("economic institutions", "n.", "经济制度/机构"), w("lead to", "phr.", "导致；带来")],
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

    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    for row in idx.get("passages", []):
        if row.get("id") == data["id"]:
            row["quality"] = "teacher_refined"
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"refined {PATH}")


if __name__ == "__main__":
    main()
