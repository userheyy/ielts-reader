# -*- coding: utf-8 -*-
"""Generate data/passages/c18-test1-p3.json (Conquering Earth's space junk problem)."""
import json
import os

RSQUO = "’"
LSQUO = "‘"
DASH = "–"

sentences = [
    # Section A (para 1)
    {
        "id": 1,
        "para": 1,
        "en": "Last year, commercial companies, military and civil departments and amateurs sent more than 400 satellites into orbit, over four times the yearly average in the previous decade.",
        "zh": "去年，商业公司、军方和民用部门以及业余爱好者把400多颗卫星送入了轨道，是此前十年年均数量的四倍多。",
        "grammar": {
            "type": "并列主语 + 同位语补充",
            "note": "主语为并列的 commercial companies, military and civil departments and amateurs；谓语 sent more than 400 satellites into orbit；over four times the yearly average in the previous decade 为名词短语作同位语，补充说明数量之多。"
        },
        "words": [
            {"w": "satellite", "pos": "n.", "def": "卫星"},
            {"w": "amateur", "pos": "n.", "def": "业余爱好者"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "Numbers could rise even more sharply if leading space companies follow through on plans to deploy hundreds to thousands of large constellations of satellites to space in the next few years.",
        "zh": "如果领先的航天公司在未来几年里切实落实其部署数百乃至数千个大型卫星星座的计划，这一数字还可能急剧攀升。",
        "grammar": {
            "type": "if 条件状语从句 + 不定式定语",
            "note": "主句 Numbers could rise even more sharply；if leading space companies follow through on plans... 为条件状语从句，follow through on 表“落实、贯彻”；to deploy hundreds to thousands of large constellations 为不定式作定语修饰 plans。"
        },
        "words": [
            {"w": "deploy", "pos": "v.", "def": "部署；调度"},
            {"w": "constellation", "pos": "n.", "def": "（卫星）星座；星群"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "All that traffic can lead to disaster.",
        "zh": "所有这些“交通流量”都可能酿成灾难。",
        "grammar": {
            "type": "主谓宾",
            "note": "主干是 All that traffic can lead to disaster；lead to 表“导致”；traffic 此处指太空中往来的航天器与碎片。"
        },
        "words": [
            {"w": "traffic", "pos": "n.", "def": "交通；（往来的）流量"},
            {"w": "disaster", "pos": "n.", "def": "灾难"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "Ten years ago, a US commercial Iridium satellite smashed into an inactive Russian communications satellite called Cosmos-2251, creating thousands of new pieces of space shrapnel that now threaten other satellites in low Earth orbit " + DASH + " the zone stretching up to 2,000 kilometres in altitude.",
        "zh": "十年前，一颗美国商用铱星撞上了一颗名为“宇宙-2251”的失效俄罗斯通信卫星，产生了数千块新的太空碎片，这些碎片如今威胁着近地轨道上的其他卫星——近地轨道是指高度可达2,000公里的区域。",
        "grammar": {
            "type": "过去分词定语 + 现在分词结果状语 + 定语从句 + 破折号同位语",
            "note": "主干是 a US commercial Iridium satellite smashed into an inactive Russian communications satellite；called Cosmos-2251 为过去分词修饰 satellite；creating thousands of new pieces of space shrapnel 为现在分词作结果状语，that now threaten... 为定语从句；破折号后 the zone stretching up to 2,000 kilometres 为 low Earth orbit 的同位语。"
        },
        "words": [
            {"w": "shrapnel", "pos": "n.", "def": "碎片；弹片"},
            {"w": "altitude", "pos": "n.", "def": "高度；海拔"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "Altogether, there are roughly 20,000 human-made objects in orbit, from working satellites to small rocket pieces.",
        "zh": "总共算起来，轨道上大约有20,000个人造物体，从正在运行的卫星到小型火箭残片，无所不有。",
        "grammar": {
            "type": "there be + from...to... 范围状语",
            "note": "主干是 there are roughly 20,000 human-made objects in orbit；from working satellites to small rocket pieces 为 from...to... 结构，说明这些物体的范围。"
        },
        "words": [
            {"w": "human-made", "pos": "adj.", "def": "人造的；人为的"},
            {"w": "roughly", "pos": "adv.", "def": "大约"}
        ]
    },
    {
        "id": 6,
        "para": 1,
        "en": "And satellite operators can" + RSQUO + "t steer away from every potential crash, because each move consumes time and fuel that could otherwise be used for the spacecraft" + RSQUO + "s main job.",
        "zh": "而且卫星运营方无法躲开每一次潜在的碰撞，因为每一次机动都会消耗时间和燃料，而这些本可以用于航天器的主要任务。",
        "grammar": {
            "type": "原因状语从句 + 定语从句",
            "note": "主句 satellite operators can" + RSQUO + "t steer away from every potential crash；because each move consumes time and fuel 为原因状语从句；that could otherwise be used for the spacecraft" + RSQUO + "s main job 为定语从句修饰 fuel，otherwise 表“否则、本来”。"
        },
        "words": [
            {"w": "steer", "pos": "v.", "def": "驾驶；使转向"},
            {"w": "fuel", "pos": "n.", "def": "燃料"}
        ]
    },
    # Section B (para 2)
    {
        "id": 7,
        "para": 2,
        "en": "Concern about space junk goes back to the beginning of the satellite era, but the number of objects in orbit is rising so rapidly that researchers are investigating new ways of attacking the problem.",
        "zh": "对太空垃圾的担忧可以追溯到卫星时代之初，但轨道上物体的数量增长得如此之快，以至于研究人员正在探索应对这一问题的新方法。",
        "grammar": {
            "type": "转折并列 + so...that... 结果状语从句",
            "note": "but 连接转折；后半 the number of objects... is rising so rapidly that...，so...that... 引导结果状语从句；attacking the problem 中 attack 表“着手解决”。"
        },
        "words": [
            {"w": "space junk", "pos": "phr.", "def": "太空垃圾"},
            {"w": "investigate", "pos": "v.", "def": "调查；研究"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "Several teams are trying to improve methods for assessing what is in orbit, so that satellite operators can work more efficiently in ever-more-crowded space.",
        "zh": "有若干团队正努力改进评估轨道上有哪些物体的方法，以便卫星运营方能在越来越拥挤的太空中更高效地运作。",
        "grammar": {
            "type": "宾语从句 + 目的状语从句",
            "note": "主干 Several teams are trying to improve methods for assessing what is in orbit，what is in orbit 为 assessing 的宾语从句；so that satellite operators can work more efficiently 为目的状语从句；ever-more-crowded 表“越来越拥挤的”。"
        },
        "words": [
            {"w": "assess", "pos": "v.", "def": "评估；评定"},
            {"w": "efficiently", "pos": "adv.", "def": "高效地"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "Some researchers are now starting to compile a massive data set that includes the best possible information on where everything is in orbit.",
        "zh": "一些研究人员如今开始汇编一个庞大的数据集，其中包含关于轨道上一切物体位置的尽可能最佳的信息。",
        "grammar": {
            "type": "定语从句 + 介词短语",
            "note": "主干是 Some researchers are now starting to compile a massive data set；that includes the best possible information 为定语从句修饰 data set；on where everything is in orbit 为介词短语，where 引导宾语从句。"
        },
        "words": [
            {"w": "compile", "pos": "v.", "def": "汇编；编制"},
            {"w": "massive", "pos": "adj.", "def": "庞大的；巨大的"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "Others are developing taxonomies of space debris " + DASH + " working on measuring properties such as the shape and size of an object, so that satellite operators know how much to worry about what" + RSQUO + "s coming their way.",
        "zh": "另一些人则在建立太空碎片的分类体系——致力于测量物体的形状、大小等属性，以便卫星运营方了解对于正朝自己飞来的东西该有多担心。",
        "grammar": {
            "type": "现在分词状语 + 目的状语从句 + 宾语从句",
            "note": "主干 Others are developing taxonomies of space debris；破折号后 working on measuring properties... 为现在分词短语作补充说明；so that satellite operators know how much to worry about... 为目的状语从句，what" + RSQUO + "s coming their way 为宾语从句。"
        },
        "words": [
            {"w": "taxonomy", "pos": "n.", "def": "分类法；分类体系"},
            {"w": "property", "pos": "n.", "def": "属性；性质"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": "The alternative, many say, is unthinkable.",
        "zh": "许多人说，另一种结局是不堪设想的。",
        "grammar": {
            "type": "主系表 + 插入语",
            "note": "主干是 The alternative is unthinkable；many say 为插入的引述语；alternative 指“不采取行动的另一种可能”。"
        },
        "words": [
            {"w": "alternative", "pos": "n.", "def": "替代方案；另一可能"},
            {"w": "unthinkable", "pos": "adj.", "def": "不堪设想的；难以想象的"}
        ]
    },
    {
        "id": 12,
        "para": 2,
        "en": "Just a few uncontrolled space crashes could generate enough debris to set off a runaway cascade of fragments, rendering near-Earth space unusable.",
        "zh": "仅仅几次失控的太空碰撞，就可能产生足够多的碎片，从而引发一连串失控蔓延的碎片连锁反应，使近地空间变得无法使用。",
        "grammar": {
            "type": "不定式结果状语 + 现在分词结果状语",
            "note": "主干是 Just a few uncontrolled space crashes could generate enough debris；to set off a runaway cascade of fragments 为不定式表结果，set off 表“引发”；rendering near-Earth space unusable 为现在分词作结果状语，render sth adj. 表“使……变得”。"
        },
        "words": [
            {"w": "cascade", "pos": "n.", "def": "连锁反应；层叠倾泻"},
            {"w": "render", "pos": "v.", "def": "使成为；使变得"}
        ]
    },
    {
        "id": 13,
        "para": 2,
        "en": LSQUO + "If we go on like this, we will reach a point of no return," + RSQUO + " says Carolin Frueh, an astrodynamical researcher at Purdue University in West Lafayette, Indiana.",
        "zh": "“如果我们继续这样下去，就会到达一个无法挽回的临界点，”印第安纳州西拉法叶普渡大学的天体动力学研究员卡罗琳·弗吕厄说。",
        "grammar": {
            "type": "直接引语 + if 条件从句 + 引述倒装同位语",
            "note": "引号内 If we go on like this 为条件状语从句，主句 we will reach a point of no return；says Carolin Frueh 为主谓倒装的引述句，an astrodynamical researcher at Purdue University... 为 Frueh 的同位语。"
        },
        "words": [
            {"w": "a point of no return", "pos": "phr.", "def": "无法回头的临界点"},
            {"w": "astrodynamical", "pos": "adj.", "def": "天体动力学的"}
        ]
    },
    # Section C (para 3)
    {
        "id": 14,
        "para": 3,
        "en": "Even as our ability to monitor space objects increases, so too does the total number of items in orbit.",
        "zh": "即便我们监测太空物体的能力在不断增强，轨道上物体的总数也在同步增加。",
        "grammar": {
            "type": "as 让步状语从句 + so 倒装呼应",
            "note": "Even as our ability to monitor space objects increases 为 as 引导的时间/让步状语从句；主句 so too does the total number of items in orbit 为 so + 助动词 + 主语 的部分倒装，表“……也如此”。"
        },
        "words": [
            {"w": "monitor", "pos": "v.", "def": "监测；监控"},
            {"w": "increase", "pos": "v.", "def": "增加；增长"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "That means companies, governments and other players in space are collaborating in new ways to avoid a shared threat.",
        "zh": "这意味着，太空领域的公司、政府和其他参与方正以新的方式展开合作，以避免共同面临的威胁。",
        "grammar": {
            "type": "宾语从句 + 不定式目的状语",
            "note": "主干 That means...，后接省略 that 的宾语从句 companies, governments and other players... are collaborating in new ways；to avoid a shared threat 为不定式作目的状语。"
        },
        "words": [
            {"w": "collaborate", "pos": "v.", "def": "合作；协作"},
            {"w": "threat", "pos": "n.", "def": "威胁"}
        ]
    },
    {
        "id": 16,
        "para": 3,
        "en": "International groups such as the Inter-Agency Space Debris Coordination Committee have developed guidelines on space sustainability.",
        "zh": "机构间空间碎片协调委员会等国际组织已经制定了关于太空可持续性的指导方针。",
        "grammar": {
            "type": "主谓宾 + 举例",
            "note": "主干是 International groups... have developed guidelines on space sustainability；such as the Inter-Agency Space Debris Coordination Committee 举例修饰 groups。"
        },
        "words": [
            {"w": "guideline", "pos": "n.", "def": "指导方针；准则"},
            {"w": "sustainability", "pos": "n.", "def": "可持续性"}
        ]
    },
    {
        "id": 17,
        "para": 3,
        "en": "Those include inactivating satellites at the end of their useful life by venting pressurised materials or leftover fuel that might lead to explosions.",
        "zh": "这些方针包括：在卫星使用寿命结束时，通过排放可能引发爆炸的加压物质或剩余燃料，使卫星失效。",
        "grammar": {
            "type": "动名词宾语 + 方式状语 + 定语从句",
            "note": "主干是 Those include inactivating satellites at the end of their useful life；by venting pressurised materials or leftover fuel 为方式状语；that might lead to explosions 为定语从句修饰 materials or fuel。"
        },
        "words": [
            {"w": "inactivate", "pos": "v.", "def": "使失效；使不活动"},
            {"w": "vent", "pos": "v.", "def": "排放；排出"}
        ]
    },
    {
        "id": 18,
        "para": 3,
        "en": "The intergovernmental groups also advise lowering satellites deep enough into the atmosphere that they will burn up or disintegrate within 25 years.",
        "zh": "这些政府间组织还建议，把卫星降到大气层足够深处，使其在25年内烧毁或解体。",
        "grammar": {
            "type": "动名词宾语 + so...that 隐含结果",
            "note": "主干是 The intergovernmental groups also advise lowering satellites；deep enough into the atmosphere that they will burn up or disintegrate 中 enough... that... 表“足够深以至于”，that 引导结果状语从句。"
        },
        "words": [
            {"w": "atmosphere", "pos": "n.", "def": "大气层"},
            {"w": "disintegrate", "pos": "v.", "def": "解体；碎裂"}
        ]
    },
    {
        "id": 19,
        "para": 3,
        "en": "But so far, only about half of all missions have abided by this 25-year goal, says Holger Krag, head of the European Space Agency" + RSQUO + "s space-debris office in Darmstadt, Germany.",
        "zh": "但到目前为止，所有任务中只有大约一半遵守了这一25年目标，欧洲空间局位于德国达姆施塔特的空间碎片办公室负责人霍尔格·克拉格说。",
        "grammar": {
            "type": "现在完成时 + 引述倒装同位语",
            "note": "主干 only about half of all missions have abided by this 25-year goal，abide by 表“遵守”；says Holger Krag 为引述倒装，head of the European Space Agency" + RSQUO + "s space-debris office... 为其同位语；so far 为时间状语。"
        },
        "words": [
            {"w": "abide by", "pos": "phr.", "def": "遵守；遵循"},
            {"w": "mission", "pos": "n.", "def": "任务；使命"}
        ]
    },
    {
        "id": 20,
        "para": 3,
        "en": "Operators of the planned large constellations of satellites say they will be responsible stewards in their enterprises in space, but Krag worries that problems could increase, despite their best intentions.",
        "zh": "计划中的大型卫星星座的运营方表示，他们在太空事业中会做负责任的管理者，但克拉格担心，尽管他们抱有良好意愿，问题仍可能加剧。",
        "grammar": {
            "type": "宾语从句 + 转折 + 让步状语",
            "note": "前半 Operators... say（后接省略 that 的宾语从句）they will be responsible stewards；but Krag worries that problems could increase 为转折，that 引导宾语从句；despite their best intentions 为让步状语。"
        },
        "words": [
            {"w": "steward", "pos": "n.", "def": "管理者；管家"},
            {"w": "intention", "pos": "n.", "def": "意图；打算"}
        ]
    },
    {
        "id": 21,
        "para": 3,
        "en": LSQUO + "What happens to those that fail or go bankrupt?" + RSQUO + " he asks.",
        "zh": "“那些失败或破产的公司会怎么样呢？”他问道。",
        "grammar": {
            "type": "直接引语特殊疑问句 + 定语从句",
            "note": "引号内为特殊疑问句 What happens to those...；that fail or go bankrupt 为定语从句修饰 those（指那些运营公司）；he asks 为引述句。"
        },
        "words": [
            {"w": "bankrupt", "pos": "adj.", "def": "破产的"},
            {"w": "fail", "pos": "v.", "def": "失败；倒闭"}
        ]
    },
    {
        "id": 22,
        "para": 3,
        "en": LSQUO + "They are probably not going to spend money to remove their satellites from space." + RSQUO,
        "zh": "“他们多半不会花钱把自己的卫星从太空中清除掉。”",
        "grammar": {
            "type": "直接引语 + 不定式目的状语",
            "note": "引号内 They are probably not going to spend money，be going to 表将来；to remove their satellites from space 为不定式作目的状语。"
        },
        "words": [
            {"w": "remove", "pos": "v.", "def": "移除；清除"},
            {"w": "probably", "pos": "adv.", "def": "很可能；大概"}
        ]
    },
    # Section D (para 4)
    {
        "id": 23,
        "para": 4,
        "en": "In theory, given the vastness of space, satellite operators should have plenty of room for all these missions to fly safely without ever nearing another object.",
        "zh": "从理论上讲，鉴于太空之广袤，卫星运营方本应有充足的空间让所有这些任务安全飞行，而永远不会靠近另一个物体。",
        "grammar": {
            "type": "独立分词状语 + 不定式目的",
            "note": "In theory 为状语；given the vastness of space 为 given 引导的原因状语（表“考虑到”）；主干 satellite operators should have plenty of room；for all these missions to fly safely 为不定式复合结构；without ever nearing another object 为方式状语。"
        },
        "words": [
            {"w": "vastness", "pos": "n.", "def": "广袤；辽阔"},
            {"w": "in theory", "pos": "phr.", "def": "理论上"}
        ]
    },
    {
        "id": 24,
        "para": 4,
        "en": "So some scientists are tackling the problem of space junk by trying to find out where all the debris is to a high degree of precision.",
        "zh": "因此，一些科学家正在着手解决太空垃圾问题，办法是设法极其精确地弄清所有碎片的位置。",
        "grammar": {
            "type": "方式状语 + 宾语从句",
            "note": "主干是 some scientists are tackling the problem of space junk；by trying to find out... 为方式状语；where all the debris is 为 find out 的宾语从句；to a high degree of precision 表“达到很高的精度”。"
        },
        "words": [
            {"w": "tackle", "pos": "v.", "def": "处理；着手解决"},
            {"w": "precision", "pos": "n.", "def": "精确；精度"}
        ]
    },
    {
        "id": 25,
        "para": 4,
        "en": "That would alleviate the need for many of the unnecessary manoeuvres that are carried out to avoid potential collisions.",
        "zh": "这将减少许多为躲避潜在碰撞而实施的不必要机动的需求。",
        "grammar": {
            "type": "定语从句 + 不定式目的",
            "note": "主干是 That would alleviate the need for many of the unnecessary manoeuvres；that are carried out 为定语从句修饰 manoeuvres；to avoid potential collisions 为不定式作目的状语。"
        },
        "words": [
            {"w": "alleviate", "pos": "v.", "def": "减轻；缓解"},
            {"w": "manoeuvre", "pos": "n.", "def": "机动；调遣动作"}
        ]
    },
    {
        "id": 26,
        "para": 4,
        "en": LSQUO + "If you knew precisely where everything was, you would almost never have a problem," + RSQUO + " says Marlon Sorge, a space-debris specialist at the Aerospace Corporation in El Segundo, California.",
        "zh": "“如果你能精确知道每样东西的位置，你就几乎不会遇到问题，”加利福尼亚州埃尔塞贡多航空航天公司的空间碎片专家马龙·索格说。",
        "grammar": {
            "type": "虚拟条件句 + 引述倒装同位语",
            "note": "引号内为与现在事实相反的虚拟条件句：If you knew... , you would almost never have a problem，从句用过去式、主句用 would + 动词原形；says Marlon Sorge 为引述倒装，a space-debris specialist... 为其同位语。"
        },
        "words": [
            {"w": "precisely", "pos": "adv.", "def": "精确地"},
            {"w": "specialist", "pos": "n.", "def": "专家"}
        ]
    },
    # Section E (para 5)
    {
        "id": 27,
        "para": 5,
        "en": "The field is called space traffic management, because it" + RSQUO + "s similar to managing traffic on the roads or in the air.",
        "zh": "这一领域被称为“太空交通管理”，因为它类似于管理道路或空中的交通。",
        "grammar": {
            "type": "被动语态 + 原因状语从句",
            "note": "主干是 The field is called space traffic management，为被动语态；because it" + RSQUO + "s similar to managing traffic... 为原因状语从句，be similar to 表“类似于”。"
        },
        "words": [
            {"w": "field", "pos": "n.", "def": "领域"},
            {"w": "similar to", "pos": "phr.", "def": "与……相似"}
        ]
    },
    {
        "id": 28,
        "para": 5,
        "en": "Think about a busy day at an airport, says Moriba Jah, an astrodynamicist at the University of Texas at Austin: planes line up in the sky, landing and taking off close to one another in a carefully choreographed routine.",
        "zh": "德克萨斯大学奥斯汀分校的天体动力学家莫里巴·贾说，想象一下机场繁忙的一天：飞机在空中排起长队，彼此靠得很近地起降，如同一套精心编排的程式。",
        "grammar": {
            "type": "祈使引语 + 引述倒装同位语 + 现在分词状语",
            "note": "Think about a busy day at an airport 为祈使句引语；says Moriba Jah 为引述倒装，an astrodynamicist... 为同位语；冒号后 planes line up in the sky 为具体说明，landing and taking off close to one another 为现在分词作伴随状语。"
        },
        "words": [
            {"w": "line up", "pos": "phr.", "def": "排队；排成一行"},
            {"w": "choreograph", "pos": "v.", "def": "精心编排"}
        ]
    },
    {
        "id": 29,
        "para": 5,
        "en": "Air-traffic controllers know the location of the planes down to one metre in accuracy.",
        "zh": "空中交通管制员能以精确到一米的准确度掌握飞机的位置。",
        "grammar": {
            "type": "主谓宾 + 程度状语",
            "note": "主干是 Air-traffic controllers know the location of the planes；down to one metre in accuracy 为程度状语，表“精确到一米”。"
        },
        "words": [
            {"w": "controller", "pos": "n.", "def": "管制员；控制者"},
            {"w": "accuracy", "pos": "n.", "def": "准确性；精度"}
        ]
    },
    {
        "id": 30,
        "para": 5,
        "en": "The same can" + RSQUO + "t be said for space debris.",
        "zh": "但对于太空碎片，情况就不同了。",
        "grammar": {
            "type": "被动语态惯用句",
            "note": "The same can" + RSQUO + "t be said for... 为固定表达，意为“对……却不能这么说、情况并非如此”，为被动结构。"
        },
        "words": [
            {"w": "debris", "pos": "n.", "def": "碎片；残骸"},
            {"w": "the same", "pos": "phr.", "def": "同样（的情况）"}
        ]
    },
    {
        "id": 31,
        "para": 5,
        "en": "Not all objects in orbit are known, and even those included in databases are not tracked consistently.",
        "zh": "并非所有在轨物体都为人所知，而且即便是那些已录入数据库的物体，也没有得到持续的跟踪。",
        "grammar": {
            "type": "部分否定 + 并列句 + 过去分词定语",
            "note": "前句 Not all objects in orbit are known 为部分否定；and even those... are not tracked consistently 为并列句，included in databases 为过去分词短语修饰 those。"
        },
        "words": [
            {"w": "database", "pos": "n.", "def": "数据库"},
            {"w": "consistently", "pos": "adv.", "def": "持续地；一贯地"}
        ]
    },
    # Section F (para 6)
    {
        "id": 32,
        "para": 6,
        "en": "An additional problem is that there is no authoritative catalogue that accurately lists the orbits of all known space debris.",
        "zh": "另一个问题是，目前没有一份权威的名录能够准确列出所有已知太空碎片的轨道。",
        "grammar": {
            "type": "表语从句 + 定语从句",
            "note": "主干 An additional problem is that...，that 引导表语从句，从句主干 there is no authoritative catalogue；that accurately lists the orbits of all known space debris 为定语从句修饰 catalogue。"
        },
        "words": [
            {"w": "authoritative", "pos": "adj.", "def": "权威的"},
            {"w": "catalogue", "pos": "n.", "def": "目录；名录"}
        ]
    },
    {
        "id": 33,
        "para": 6,
        "en": "Jah illustrates this with a web-based database that he has developed.",
        "zh": "贾用他自己开发的一个网络数据库来说明这一点。",
        "grammar": {
            "type": "主谓宾 + 定语从句",
            "note": "主干是 Jah illustrates this with a web-based database；that he has developed 为定语从句修饰 database。"
        },
        "words": [
            {"w": "illustrate", "pos": "v.", "def": "说明；举例说明"},
            {"w": "web-based", "pos": "adj.", "def": "基于网络的"}
        ]
    },
    {
        "id": 34,
        "para": 6,
        "en": "It draws on several sources, such as catalogues maintained by the US and Russian governments, to visualise where objects are in space.",
        "zh": "它借助多种来源——例如美国和俄罗斯政府维护的名录——来直观呈现物体在太空中的位置。",
        "grammar": {
            "type": "主谓宾 + 举例 + 不定式目的",
            "note": "主干是 It draws on several sources，draw on 表“利用、借助”；such as catalogues maintained by... 举例，maintained 为过去分词修饰 catalogues；to visualise where objects are in space 为不定式作目的状语，where 引导宾语从句。"
        },
        "words": [
            {"w": "draw on", "pos": "phr.", "def": "利用；依靠"},
            {"w": "visualise", "pos": "v.", "def": "使可视化；直观呈现"}
        ]
    },
    {
        "id": 35,
        "para": 6,
        "en": "When he types in an identifier for a particular space object, the database draws a purple line to designate its orbit.",
        "zh": "当他输入某个特定太空物体的标识符时，数据库便会画出一条紫色的线来标示它的轨道。",
        "grammar": {
            "type": "when 时间状语从句 + 不定式目的",
            "note": "When he types in an identifier for a particular space object 为时间状语从句；主句 the database draws a purple line；to designate its orbit 为不定式作目的状语。"
        },
        "words": [
            {"w": "identifier", "pos": "n.", "def": "标识符；识别码"},
            {"w": "designate", "pos": "v.", "def": "标示；指定"}
        ]
    },
    {
        "id": 36,
        "para": 6,
        "en": "Only this doesn" + RSQUO + "t quite work for a number of objects, such as a Russian rocket body designated in the database as object number 32280.",
        "zh": "只不过对于一些物体，这种做法并不太奏效，比如在数据库中被标记为32280号的一个俄罗斯火箭箭体。",
        "grammar": {
            "type": "转折句 + 举例 + 过去分词定语",
            "note": "主干是 Only this doesn" + RSQUO + "t quite work for a number of objects，Only 此处作副词表转折“只不过”；such as a Russian rocket body 举例，designated in the database as object number 32280 为过去分词短语修饰 rocket body。"
        },
        "words": [
            {"w": "rocket body", "pos": "phr.", "def": "火箭箭体；火箭残骸主体"},
            {"w": "quite", "pos": "adv.", "def": "（用于否定）完全；十分"}
        ]
    },
    {
        "id": 37,
        "para": 6,
        "en": "When Jah enters that number, the database draws two purple lines: the US and Russian sources contain two completely different orbits for the same object.",
        "zh": "当贾输入这个编号时，数据库画出了两条紫色的线：美国和俄罗斯的数据源对同一物体给出了两条完全不同的轨道。",
        "grammar": {
            "type": "when 时间状语从句 + 冒号解释",
            "note": "When Jah enters that number 为时间状语从句；主句 the database draws two purple lines；冒号后 the US and Russian sources contain two completely different orbits 解释原因。"
        },
        "words": [
            {"w": "enter", "pos": "v.", "def": "输入；键入"},
            {"w": "source", "pos": "n.", "def": "来源；数据源"}
        ]
    },
    {
        "id": 38,
        "para": 6,
        "en": "Jah says that it is almost impossible to tell which is correct, unless a third source of information made it possible to cross-correlate.",
        "zh": "贾说，几乎不可能判断哪一条是正确的，除非有第三方信息来源使交叉比对成为可能。",
        "grammar": {
            "type": "宾语从句 + it 形式主语 + unless 条件从句",
            "note": "主干 Jah says that...，that 引导宾语从句；从句 it is almost impossible to tell which is correct，it 为形式主语，which is correct 为 tell 的宾语从句；unless a third source... made it possible to cross-correlate 为 unless 条件状语从句。"
        },
        "words": [
            {"w": "cross-correlate", "pos": "v.", "def": "交叉比对；相互印证"},
            {"w": "impossible", "pos": "adj.", "def": "不可能的"}
        ]
    },
    {
        "id": 39,
        "para": 6,
        "en": "Jah describes himself as a space environmentalist: " + LSQUO + "I want to make space a place that is safe to operate, that is free and useful for generations to come." + RSQUO,
        "zh": "贾把自己描述为一名“太空环保主义者”：“我想把太空变成一个可以安全运作的地方，一个对子孙后代自由而有用的地方。”",
        "grammar": {
            "type": "describe A as B + 冒号引语 + 并列定语从句",
            "note": "主干 Jah describes himself as a space environmentalist，describe A as B 结构；冒号后为直接引语 I want to make space a place，make sth a place 为复合宾语；两个 that... 定语从句并列修饰 place，generations to come 表“子孙后代”。"
        },
        "words": [
            {"w": "environmentalist", "pos": "n.", "def": "环保主义者"},
            {"w": "generations to come", "pos": "phr.", "def": "子孙后代；未来世代"}
        ]
    },
    {
        "id": 40,
        "para": 6,
        "en": "Until that happens, he argues, the space community will continue devolving into a tragedy in which all spaceflight operators are polluting a common resource.",
        "zh": "他认为，在这一天到来之前，太空界将继续沦为一场悲剧——在这场悲剧中，所有航天运营方都在污染着一种共有的资源。",
        "grammar": {
            "type": "时间状语从句 + 插入引述 + 定语从句",
            "note": "Until that happens 为时间状语从句；he argues 为插入引述；主句 the space community will continue devolving into a tragedy，devolve into 表“退化为”；in which all spaceflight operators are polluting a common resource 为定语从句修饰 tragedy。"
        },
        "words": [
            {"w": "devolve", "pos": "v.", "def": "退化；沦为"},
            {"w": "common resource", "pos": "phr.", "def": "共有资源；公共资源"}
        ]
    }
]

questions = [
    {
        "title": "Questions 27" + DASH + "31",
        "type": "matching_information",
        "instructions": [
            "Reading Passage 3 has six sections, A" + DASH + "F.",
            "Which section contains the following information?",
            "Write the correct letter, A" + DASH + "F, in boxes 27" + DASH + "31 on your answer sheet."
        ],
        "items": [
            {"number": 27, "prompt": "a reference to the cooperation that takes place to try and minimise risk", "answer": "C", "evidence_sentence": 15},
            {"number": 28, "prompt": "an explanation of a person" + RSQUO + "s aims", "answer": "F", "evidence_sentence": 39},
            {"number": 29, "prompt": "a description of a major collision that occurred in space", "answer": "A", "evidence_sentence": 4},
            {"number": 30, "prompt": "a comparison between tracking objects in space and the efficiency of a transportation system", "answer": "E", "evidence_sentence": 28},
            {"number": 31, "prompt": "a reference to efforts to classify space junk", "answer": "B", "evidence_sentence": 10}
        ]
    },
    {
        "title": "Questions 32" + DASH + "35",
        "type": "summary_completion",
        "instructions": [
            "Complete the summary below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 32" + DASH + "35 on your answer sheet.",
            "The Inter-Agency Space Debris Coordination Committee"
        ],
        "items": [
            {"number": 32, "prompt": "The committee gives advice on how the 32 ____ of space can be achieved.", "answer": "sustainability", "evidence_sentence": 16},
            {"number": 33, "prompt": "The committee advises that when satellites are no longer active, any unused 33 ____ or pressurised material that could cause 34 ____ should be removed.", "answer": "fuel", "evidence_sentence": 17},
            {"number": 34, "prompt": "... any unused fuel or pressurised material that could cause 34 ____ should be removed.", "answer": "explosions", "evidence_sentence": 17},
            {"number": 35, "prompt": "Holger Krag points out that the operators that become 35 ____ are unlikely to prioritise removing their satellites from space.", "answer": "bankrupt", "evidence_sentence": 21}
        ]
    },
    {
        "title": "Questions 36" + DASH + "40",
        "type": "matching_features",
        "instructions": [
            "Look at the following statements (Questions 36" + DASH + "40) and the list of people below.",
            "Match each statement with the correct person, A, B, C or D.",
            "Write the correct letter, A, B, C or D, in boxes 36" + DASH + "40 on your answer sheet.",
            "NB You may use any letter more than once.",
            "List of People",
            "A Carolin Frueh",
            "B Holger Krag",
            "C Marlon Sorge",
            "D Moriba Jah"
        ],
        "items": [
            {"number": 36, "prompt": "Knowing the exact location of space junk would help prevent any possible danger.", "answer": "C", "evidence_sentence": 26},
            {"number": 37, "prompt": "Space should be available to everyone and should be preserved for the future.", "answer": "D", "evidence_sentence": 39},
            {"number": 38, "prompt": "A recommendation regarding satellites is widely ignored.", "answer": "B", "evidence_sentence": 19},
            {"number": 39, "prompt": "There is conflicting information about where some satellites are in space.", "answer": "D", "evidence_sentence": 37},
            {"number": 40, "prompt": "There is a risk we will not be able to undo the damage that occurs in space.", "answer": "A", "evidence_sentence": 13}
        ]
    }
]

phrases = [
    {"w": "space junk", "pos": "n.", "def": "太空垃圾"},
    {"w": "space debris", "pos": "n.", "def": "太空碎片；空间碎片"},
    {"w": "low Earth orbit", "pos": "n.", "def": "近地轨道"},
    {"w": "space traffic management", "pos": "n.", "def": "太空交通管理"},
    {"w": "Inter-Agency Space Debris Coordination Committee", "pos": "n.", "def": "机构间空间碎片协调委员会"},
    {"w": "European Space Agency", "pos": "n.", "def": "欧洲空间局（ESA）"},
    {"w": "a point of no return", "pos": "phr.", "def": "无法回头的临界点"},
    {"w": "constellation of satellites", "pos": "n.", "def": "卫星星座"},
    {"w": "space environmentalist", "pos": "n.", "def": "太空环保主义者"},
    {"w": "common resource", "pos": "n.", "def": "共有资源"}
]

data = {
    "id": "c18-test1-p3",
    "source": "剑桥雅思18 · Test 1 · Passage 3",
    "title": "Conquering Earth" + RSQUO + "s space junk problem",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "subtitle": "Satellites, rocket shards and collision debris are creating major traffic risks in orbit around the planet. Researchers are working to reduce these threats",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c18-test1-p3.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
