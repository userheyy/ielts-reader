# -*- coding: utf-8 -*-
"""Generate data/passages/c14-test1-p2.json (The growth of bike-sharing schemes around the world)."""
import json
import os

RSQUO = "’"
LSQUO = "‘"
DASH = "–"
PCT = "%"

sentences = [
    # Para A (1)
    {
        "id": 1,
        "para": 1,
        "en": "The original idea for an urban bike-sharing scheme dates back to a summer" + RSQUO + "s day in Amsterdam in 1965.",
        "zh": "城市共享单车计划最初的构想可以追溯到1965年阿姆斯特丹的一个夏日。",
        "grammar": {
            "type": "date back to 固定短语",
            "note": "主干 The original idea... dates back to a summer's day；date back to 意为“追溯到”，为不及物动词短语，后接时间。"
        },
        "words": [
            {"w": "date back to", "pos": "phr.", "def": "追溯到；始于"},
            {"w": "scheme", "pos": "n.", "def": "计划；方案"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "Provo, the organisation that came up with the idea, was a group of Dutch activists who wanted to change society.",
        "zh": "普罗沃——提出这一构想的组织——是一群想要改变社会的荷兰活动人士。",
        "grammar": {
            "type": "同位语 + 双重定语从句",
            "note": "the organisation that came up with the idea 为 Provo 的同位语，内含定语从句；主句表语 a group of Dutch activists，其后 who wanted to change society 为定语从句修饰 activists。"
        },
        "words": [
            {"w": "activist", "pos": "n.", "def": "积极分子；活动人士"},
            {"w": "come up with", "pos": "phr.", "def": "提出；想出"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "They believed the scheme, which was known as the Witte Fietsenplan, was an answer to the perceived threats of air pollution and consumerism.",
        "zh": "他们相信，这项被称为“白色自行车计划”的方案，是对空气污染和消费主义这两大被察觉到的威胁的一种回应。",
        "grammar": {
            "type": "宾语从句 + 非限制性定语从句插入",
            "note": "主干 They believed the scheme... was an answer to...，believed 后为省略 that 的宾语从句；which was known as the Witte Fietsenplan 为非限制性定语从句，插在从句主语与谓语之间。"
        },
        "words": [
            {"w": "consumerism", "pos": "n.", "def": "消费主义"},
            {"w": "perceived", "pos": "adj.", "def": "被感知到的；被认为的"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "In the centre of Amsterdam, they painted a small number of used bikes white.",
        "zh": "在阿姆斯特丹市中心，他们把少量旧自行车漆成了白色。",
        "grammar": {
            "type": "paint + 宾语 + 宾补",
            "note": "主干 they painted a small number of used bikes white；white 为形容词作宾语补足语，paint sth + 颜色 表“把某物漆成某色”。"
        },
        "words": [
            {"w": "used", "pos": "adj.", "def": "用过的；二手的"},
            {"w": "a small number of", "pos": "phr.", "def": "少量的"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "They also distributed leaflets describing the dangers of cars and inviting people to use the white bikes.",
        "zh": "他们还散发传单，讲述汽车的危害，并邀请人们使用这些白色自行车。",
        "grammar": {
            "type": "现在分词定语并列",
            "note": "主干 They also distributed leaflets；describing the dangers of cars 与 inviting people to use the white bikes 为两个并列的现在分词短语作 leaflets 的后置定语。"
        },
        "words": [
            {"w": "distribute", "pos": "v.", "def": "分发；散发"},
            {"w": "leaflet", "pos": "n.", "def": "传单；宣传页"}
        ]
    },
    {
        "id": 6,
        "para": 1,
        "en": "The bikes were then left unlocked at various locations around the city, to be used by anyone in need of transport.",
        "zh": "随后这些自行车被不上锁地停放在城市各处，供任何需要交通工具的人使用。",
        "grammar": {
            "type": "被动语态 + 不定式目的",
            "note": "主干 The bikes were then left unlocked（被动，unlocked 作宾补）；to be used by anyone in need of transport 为不定式的被动式作目的状语，in need of 意为“需要”。"
        },
        "words": [
            {"w": "unlocked", "pos": "adj.", "def": "未上锁的"},
            {"w": "in need of", "pos": "phr.", "def": "需要"}
        ]
    },
    # Para B (2)
    {
        "id": 7,
        "para": 2,
        "en": "Luud Schimmelpennink, a Dutch industrial engineer who still lives and cycles in Amsterdam, was heavily involved in the original scheme.",
        "zh": "吕德·希默尔彭宁克是一位至今仍在阿姆斯特丹生活并骑车的荷兰工业工程师，他深度参与了最初的方案。",
        "grammar": {
            "type": "同位语 + 定语从句",
            "note": "a Dutch industrial engineer... 为 Luud Schimmelpennink 的同位语，其中 who still lives and cycles in Amsterdam 为定语从句；主句 (主语) was heavily involved in the original scheme。"
        },
        "words": [
            {"w": "industrial", "pos": "adj.", "def": "工业的"},
            {"w": "be involved in", "pos": "phr.", "def": "参与；涉及"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "He recalls how the scheme succeeded in attracting a great deal of attention " + DASH + " particularly when it came to publicising Provo" + RSQUO + "s aims " + DASH + " but struggled to get off the ground.",
        "zh": "他回忆道，这项方案如何成功地吸引了大量关注——尤其是在宣传普罗沃的宗旨方面——但却难以真正启动。",
        "grammar": {
            "type": "宾语从句 + but 并列谓语 + 破折号插入",
            "note": "主干 He recalls how...，how 引导宾语从句；从句内 the scheme succeeded in... but struggled to get off the ground，两谓语由 but 并列；两破折号间 particularly when it came to publicising Provo's aims 为插入状语，when it comes to 意为“谈到、涉及”。"
        },
        "words": [
            {"w": "get off the ground", "pos": "phr.", "def": "开始；顺利起步"},
            {"w": "publicise", "pos": "v.", "def": "宣传；公布"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "The police were opposed to Provo" + RSQUO + "s initiatives and almost as soon as the white bikes were distributed around the city, they removed them.",
        "zh": "警方反对普罗沃的种种举措，而几乎在白色自行车刚被分发到城市各处时，他们就把车收走了。",
        "grammar": {
            "type": "并列句 + as soon as 时间从句",
            "note": "前一分句 The police were opposed to Provo's initiatives，be opposed to 意为“反对”；and 连接后一分句；almost as soon as the white bikes were distributed... 为时间状语从句，主句 they removed them。"
        },
        "words": [
            {"w": "be opposed to", "pos": "phr.", "def": "反对"},
            {"w": "initiative", "pos": "n.", "def": "倡议；新举措"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "However, for Schimmelpennink and for bike-sharing schemes in general, this was just the beginning.",
        "zh": "然而，对希默尔彭宁克以及对共享单车计划整体而言，这仅仅是个开端。",
        "grammar": {
            "type": "主系表 + 并列介词状语",
            "note": "However 转折；for Schimmelpennink and for bike-sharing schemes in general 为并列介词短语作状语；主干 this was just the beginning；in general 意为“总体上”。"
        },
        "words": [
            {"w": "in general", "pos": "phr.", "def": "总体上；一般而言"},
            {"w": "beginning", "pos": "n.", "def": "开端；起点"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": LSQUO + "The first Witte Fietsenplan was just a symbolic thing," + RSQUO + " he says. " + LSQUO + "We painted a few bikes white, that was all. Things got more serious when I became a member of the Amsterdam city council two years later." + RSQUO,
        "zh": "“第一个白色自行车计划只是一件象征性的事情，”他说。“我们把几辆自行车漆成了白色，仅此而已。两年后当我成为阿姆斯特丹市议会议员时，事情才变得更严肃起来。”",
        "grammar": {
            "type": "直接引语 + 时间状语从句",
            "note": "多句直接引语；末句 Things got more serious when I became a member of the Amsterdam city council，when 引导时间状语从句；two years later 为时间状语。"
        },
        "words": [
            {"w": "symbolic", "pos": "adj.", "def": "象征性的"},
            {"w": "city council", "pos": "n.", "def": "市议会"}
        ]
    },
    # Para C (3)
    {
        "id": 12,
        "para": 3,
        "en": "Schimmelpennink seized this opportunity to present a more elaborate Witte Fietsenplan to the city council.",
        "zh": "希默尔彭宁克抓住这个机会，向市议会提交了一份更为详尽的白色自行车计划。",
        "grammar": {
            "type": "seize opportunity to do",
            "note": "主干 Schimmelpennink seized this opportunity；to present a more elaborate Witte Fietsenplan to the city council 为不定式作目的状语/定语，说明抓住机会去做的事。"
        },
        "words": [
            {"w": "seize", "pos": "v.", "def": "抓住；抓取"},
            {"w": "elaborate", "pos": "adj.", "def": "详尽的；复杂精细的"}
        ]
    },
    {
        "id": 13,
        "para": 3,
        "en": LSQUO + "My idea was that the municipality of Amsterdam would distribute 10,000 white bikes over the city, for everyone to use," + RSQUO + " he explains.",
        "zh": "“我的设想是，阿姆斯特丹市政当局在全城分发一万辆白色自行车，供所有人使用，”他解释道。",
        "grammar": {
            "type": "表语从句 + for sb to do",
            "note": "引语主干 My idea was that...，that 引导表语从句；for everyone to use 为“for + 逻辑主语 + 不定式”结构，表分发自行车的目的。"
        },
        "words": [
            {"w": "municipality", "pos": "n.", "def": "市政当局；自治市"},
            {"w": "distribute", "pos": "v.", "def": "分发；分配"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": LSQUO + "I made serious calculations. It turned out that a white bicycle " + DASH + " per person, per kilometre " + DASH + " would cost the municipality only 10" + PCT + " of what it contributed to public transport per person per kilometre." + RSQUO,
        "zh": "“我做了认真的测算。结果表明，一辆白色自行车——按人均、每公里计算——花费市政当局的成本，仅为它在公共交通上按人均每公里投入的10%。",
        "grammar": {
            "type": "It turned out that 宾语从句 + of what 从句",
            "note": "It turned out that... 为“结果表明”，that 引导主语从句；从句内 a white bicycle would cost the municipality only 10% of what it contributed to...，what 引导介词宾语从句；两破折号间 per person, per kilometre 为插入状语。"
        },
        "words": [
            {"w": "calculation", "pos": "n.", "def": "计算；测算"},
            {"w": "turn out", "pos": "phr.", "def": "结果是；证明是"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "Nevertheless, the council unanimously rejected the plan.",
        "zh": "尽管如此，市议会还是一致否决了该计划。",
        "grammar": {
            "type": "让步副词 + 主谓宾",
            "note": "Nevertheless 为让步转折副词；主干 the council unanimously rejected the plan；unanimously 意为“一致地”，修饰 rejected。"
        },
        "words": [
            {"w": "nevertheless", "pos": "adv.", "def": "尽管如此；然而"},
            {"w": "unanimously", "pos": "adv.", "def": "一致地；无异议地"}
        ]
    },
    {
        "id": 16,
        "para": 3,
        "en": LSQUO + "They said that the bicycle belongs to the past. They saw a glorious future for the car," + RSQUO + " says Schimmelpennink. But he was not in the least discouraged.",
        "zh": "“他们说自行车属于过去。他们看到的是汽车的辉煌未来，”希默尔彭宁克说。但他丝毫没有气馁。",
        "grammar": {
            "type": "直接引语 + not in the least 强调否定",
            "note": "引语两句为一般现在时/过去时陈述；末句 he was not in the least discouraged，not in the least 意为“一点也不”，强调否定；discouraged 为形容词表“气馁的”。"
        },
        "words": [
            {"w": "glorious", "pos": "adj.", "def": "辉煌的；光荣的"},
            {"w": "not in the least", "pos": "phr.", "def": "一点也不；毫不"}
        ]
    },
    # Para D (4)
    {
        "id": 17,
        "para": 4,
        "en": "Schimmelpennink never stopped believing in bike-sharing, and in the mid-90s, two Danes asked for his help to set up a system in Copenhagen.",
        "zh": "希默尔彭宁克从未停止过对共享单车的信念；而在90年代中期，两名丹麦人请他帮忙在哥本哈根建立一套系统。",
        "grammar": {
            "type": "并列句 + stop doing",
            "note": "前一分句 Schimmelpennink never stopped believing in bike-sharing，stop doing 表“停止做某事”；and 连接后一分句 two Danes asked for his help to set up a system，to set up... 为不定式作目的状语。"
        },
        "words": [
            {"w": "Dane", "pos": "n.", "def": "丹麦人"},
            {"w": "set up", "pos": "phr.", "def": "建立；创立"}
        ]
    },
    {
        "id": 18,
        "para": 4,
        "en": "The result was the world" + RSQUO + "s first large-scale bike-share programme.",
        "zh": "其成果便是世界上第一个大规模的共享单车项目。",
        "grammar": {
            "type": "主系表",
            "note": "主干 The result was the world's first large-scale bike-share programme；large-scale 为复合形容词作定语，意为“大规模的”。"
        },
        "words": [
            {"w": "large-scale", "pos": "adj.", "def": "大规模的"},
            {"w": "programme", "pos": "n.", "def": "项目；方案；计划"}
        ]
    },
    {
        "id": 19,
        "para": 4,
        "en": "It worked on a deposit: " + LSQUO + "You dropped a coin in the bike and when you returned it, you got your money back." + RSQUO,
        "zh": "它以押金方式运作：“你往车里投一枚硬币，等你还车时，就能把钱取回来。”",
        "grammar": {
            "type": "冒号解释 + 时间状语从句",
            "note": "主句 It worked on a deposit；冒号后引语说明运作方式，含 when you returned it 时间状语从句；get one's money back 意为“把钱要回、退回”。"
        },
        "words": [
            {"w": "deposit", "pos": "n.", "def": "押金；保证金"},
            {"w": "return", "pos": "v.", "def": "归还；返回"}
        ]
    },
    {
        "id": 20,
        "para": 4,
        "en": "After setting up the Danish system, Schimmelpennink decided to try his luck again in the Netherlands " + DASH + " and this time he succeeded in arousing the interest of the Dutch Ministry of Transport.",
        "zh": "在建立起丹麦的系统之后，希默尔彭宁克决定在荷兰再碰碰运气——而这一次他成功引起了荷兰交通部的兴趣。",
        "grammar": {
            "type": "时间状语 + 破折号 and 并列",
            "note": "After setting up the Danish system 为介词短语作时间状语；主句 Schimmelpennink decided to try his luck again；破折号后 and this time he succeeded in arousing the interest of...，succeed in doing 结构。"
        },
        "words": [
            {"w": "try one" + RSQUO + "s luck", "pos": "phr.", "def": "碰运气；试一试"},
            {"w": "arouse", "pos": "v.", "def": "引起；激起"}
        ]
    },
    {
        "id": 21,
        "para": 4,
        "en": LSQUO + "Times had changed," + RSQUO + " he recalls. " + LSQUO + "People had become more environmentally conscious, and the Danish experiment had proved that bike-sharing was a real possibility." + RSQUO,
        "zh": "“时代已经变了，”他回忆道。“人们变得更有环保意识，而丹麦的实验已经证明共享单车是切实可行的。”",
        "grammar": {
            "type": "过去完成时 + 宾语从句",
            "note": "引语多用过去完成时（had changed / had become / had proved）表在过去某点之前发生；末句 the Danish experiment had proved that...，that 引导宾语从句。"
        },
        "words": [
            {"w": "environmentally conscious", "pos": "phr.", "def": "有环保意识的"},
            {"w": "experiment", "pos": "n.", "def": "实验；试验"}
        ]
    },
    {
        "id": 22,
        "para": 4,
        "en": "A new Witte Fietsenplan was launched in 1999 in Amsterdam.",
        "zh": "1999年，一项新的白色自行车计划在阿姆斯特丹启动。",
        "grammar": {
            "type": "被动语态",
            "note": "主干 A new Witte Fietsenplan was launched（被动）；in 1999 与 in Amsterdam 分别为时间、地点状语。"
        },
        "words": [
            {"w": "launch", "pos": "v.", "def": "启动；发起；推出"},
            {"w": "new", "pos": "adj.", "def": "新的"}
        ]
    },
    {
        "id": 23,
        "para": 4,
        "en": "However, riding a white bike was no longer free; it cost one guilder per trip and payment was made with a chip card developed by the Dutch bank Postbank.",
        "zh": "然而，骑白色自行车不再免费了；每次骑行需花费一荷兰盾，付款通过荷兰邮政银行开发的一种芯片卡完成。",
        "grammar": {
            "type": "分号并列 + 过去分词定语",
            "note": "分号连接三个分句；riding a white bike 为动名词主语；末句 payment was made with a chip card（被动），developed by the Dutch bank Postbank 为过去分词短语作 chip card 的后置定语。"
        },
        "words": [
            {"w": "guilder", "pos": "n.", "def": "荷兰盾（旧荷兰货币）"},
            {"w": "chip card", "pos": "n.", "def": "芯片卡"}
        ]
    },
    {
        "id": 24,
        "para": 4,
        "en": "Schimmelpennink designed conspicuous, sturdy white bikes locked in special racks which could be opened with the chip card " + DASH + " the plan started with 250 bikes, distributed over five stations.",
        "zh": "希默尔彭宁克设计了醒目、结实的白色自行车，它们锁在专用车架里，可用芯片卡开启——该计划以250辆自行车起步，分布在五个站点。",
        "grammar": {
            "type": "过去分词定语 + 定语从句 + 破折号补充",
            "note": "主干 Schimmelpennink designed conspicuous, sturdy white bikes；locked in special racks 为过去分词定语，which could be opened with the chip card 为定语从句修饰 racks；破折号后为补充说明，distributed over five stations 为过去分词短语作定语。"
        },
        "words": [
            {"w": "conspicuous", "pos": "adj.", "def": "显眼的；引人注目的"},
            {"w": "sturdy", "pos": "adj.", "def": "结实的；坚固的"}
        ]
    },
    # Para E (5)
    {
        "id": 25,
        "para": 5,
        "en": "Theo Molenaar, who was a system designer for the project, worked alongside Schimmelpennink.",
        "zh": "西奥·莫勒纳尔是该项目的系统设计师，他与希默尔彭宁克并肩工作。",
        "grammar": {
            "type": "非限制性定语从句",
            "note": "主干 Theo Molenaar... worked alongside Schimmelpennink；who was a system designer for the project 为非限制性定语从句修饰 Theo Molenaar；alongside 意为“与……一起、并肩”。"
        },
        "words": [
            {"w": "alongside", "pos": "prep.", "def": "与……一起；在……旁边"},
            {"w": "designer", "pos": "n.", "def": "设计师"}
        ]
    },
    {
        "id": 26,
        "para": 5,
        "en": LSQUO + "I remember when we were testing the bike racks, he announced that he had already designed better ones. But of course, we had to go through with the ones we had." + RSQUO,
        "zh": "“我记得，当我们在测试车架时，他就宣布自己已经设计出了更好的车架。但我们当然只能将就用现有的那些。”",
        "grammar": {
            "type": "宾语从句 + 时间从句 + 省略关系词定语从句",
            "note": "I remember (that) when we were testing the bike racks, he announced that...，含时间状语从句与两层宾语从句；末句 the ones (that) we had 为省略关系词定语从句，go through with 意为“将……进行到底、坚持用”。"
        },
        "words": [
            {"w": "announce", "pos": "v.", "def": "宣布；宣告"},
            {"w": "go through with", "pos": "phr.", "def": "把……进行到底；坚持完成"}
        ]
    },
    {
        "id": 27,
        "para": 5,
        "en": "The system, however, was prone to vandalism and theft.",
        "zh": "然而，这套系统很容易遭到蓄意破坏和偷窃。",
        "grammar": {
            "type": "be prone to 结构",
            "note": "主干 The system... was prone to vandalism and theft；however 为插入转折；be prone to 意为“易于遭受、有……倾向”，后接名词。"
        },
        "words": [
            {"w": "be prone to", "pos": "phr.", "def": "易于；有……倾向"},
            {"w": "vandalism", "pos": "n.", "def": "蓄意破坏（公物）"}
        ]
    },
    {
        "id": 28,
        "para": 5,
        "en": LSQUO + "After every weekend there would always be a couple of bikes missing," + RSQUO + " Molenaar says. " + LSQUO + "I really have no idea what people did with them, because they could instantly be recognised as white bikes." + RSQUO,
        "zh": "“每个周末过后，总会有几辆自行车不见踪影，”莫勒纳尔说。“我真的不知道人们把它们弄到哪去了，因为它们一眼就能被认出是白色自行车。”",
        "grammar": {
            "type": "there be + 宾语从句 + 原因从句被动",
            "note": "首句 there would always be a couple of bikes missing，missing 为形容词作后置定语；I have no idea what people did with them，what... 为宾语从句；because they could instantly be recognised as white bikes 为原因状语从句（被动）。"
        },
        "words": [
            {"w": "instantly", "pos": "adv.", "def": "立即；马上"},
            {"w": "recognise", "pos": "v.", "def": "认出；识别"}
        ]
    },
    {
        "id": 29,
        "para": 5,
        "en": "But the biggest blow came when Postbank decided to abolish the chip card, because it wasn" + RSQUO + "t profitable.",
        "zh": "但最沉重的打击出现在邮政银行决定取消芯片卡之时，因为它无利可图。",
        "grammar": {
            "type": "时间状语从句 + 原因从句",
            "note": "主句 the biggest blow came；when Postbank decided to abolish the chip card 为时间状语从句；because it wasn't profitable 为原因状语从句。"
        },
        "words": [
            {"w": "blow", "pos": "n.", "def": "打击；挫折"},
            {"w": "abolish", "pos": "v.", "def": "废除；取消"}
        ]
    },
    {
        "id": 30,
        "para": 5,
        "en": LSQUO + "That chip card was pivotal to the system," + RSQUO + " Molenaar says. " + LSQUO + "To continue the project we would have needed to set up another system, but the business partner had lost interest." + RSQUO,
        "zh": "“那张芯片卡对整个系统至关重要，”莫勒纳尔说。“要继续这个项目，我们就得另建一套系统，但商业合作伙伴已经失去了兴趣。”",
        "grammar": {
            "type": "be pivotal to + 虚拟语气",
            "note": "首句 That chip card was pivotal to the system，be pivotal to 意为“对……至关重要”；末句 To continue the project we would have needed to...，would have needed 为对过去的虚拟推测；but the business partner had lost interest。"
        },
        "words": [
            {"w": "pivotal", "pos": "adj.", "def": "关键的；核心的"},
            {"w": "lose interest", "pos": "phr.", "def": "失去兴趣"}
        ]
    },
    # Para F (6)
    {
        "id": 31,
        "para": 6,
        "en": "Schimmelpennink was disappointed, but " + DASH + " characteristically " + DASH + " not for long.",
        "zh": "希默尔彭宁克感到失望，但——一如他的性格——失望并没有持续太久。",
        "grammar": {
            "type": "主系表 + 破折号插入 + 省略",
            "note": "主干 Schimmelpennink was disappointed；but not for long 为省略结构（=but he was not disappointed for long）；两破折号间 characteristically 为插入副词，意为“一贯地、符合其性格地”。"
        },
        "words": [
            {"w": "disappointed", "pos": "adj.", "def": "失望的"},
            {"w": "characteristically", "pos": "adv.", "def": "典型地；一贯地"}
        ]
    },
    {
        "id": 32,
        "para": 6,
        "en": "In 2002 he got a call from the French advertising corporation JC Decaux, who wanted to set up his bike-sharing scheme in Vienna.",
        "zh": "2002年，他接到法国广告公司德高集团的来电，该公司想在维也纳推行他的共享单车方案。",
        "grammar": {
            "type": "非限制性定语从句",
            "note": "主干 he got a call from the French advertising corporation JC Decaux；who wanted to set up his bike-sharing scheme in Vienna 为非限制性定语从句修饰 JC Decaux（以 who 指代公司/其人）。"
        },
        "words": [
            {"w": "corporation", "pos": "n.", "def": "公司；企业"},
            {"w": "advertising", "pos": "n.", "def": "广告业；广告"}
        ]
    },
    {
        "id": 33,
        "para": 6,
        "en": LSQUO + "That went really well. After Vienna, they set up a system in Lyon. Then in 2007, Paris followed. That was a decisive moment in the history of bike-sharing." + RSQUO,
        "zh": "“那次进展非常顺利。继维也纳之后，他们又在里昂建立了系统。接着在2007年，巴黎也跟进了。那是共享单车史上一个决定性的时刻。”",
        "grammar": {
            "type": "简单句并列引语",
            "note": "引语由数个简单句构成，时间线索 After Vienna / Then in 2007 推进；末句 That was a decisive moment in the history of bike-sharing 为主系表。"
        },
        "words": [
            {"w": "decisive", "pos": "adj.", "def": "决定性的；关键的"},
            {"w": "follow", "pos": "v.", "def": "跟随；效仿"}
        ]
    },
    {
        "id": 34,
        "para": 6,
        "en": "The huge and unexpected success of the Parisian bike-sharing programme, which now boasts more than 20,000 bicycles, inspired cities all over the world to set up their own schemes, all modelled on Schimmelpennink" + RSQUO + "s.",
        "zh": "巴黎共享单车项目取得的巨大而出人意料的成功——如今它拥有超过两万辆自行车——激励了全世界的城市建立自己的方案，而这些方案都以希默尔彭宁克的方案为蓝本。",
        "grammar": {
            "type": "非限制性定语从句 + inspire sb to do + 过去分词状语",
            "note": "主干 The huge and unexpected success... inspired cities... to set up their own schemes；which now boasts more than 20,000 bicycles 为非限制性定语从句；all modelled on Schimmelpennink's 为过去分词短语作补充状语，be modelled on 意为“以……为蓝本”。"
        },
        "words": [
            {"w": "boast", "pos": "v.", "def": "拥有（值得自豪的事物）；夸耀"},
            {"w": "be modelled on", "pos": "phr.", "def": "以……为范本/蓝本"}
        ]
    },
    {
        "id": 35,
        "para": 6,
        "en": LSQUO + "It" + RSQUO + "s wonderful that this happened," + RSQUO + " he says. " + LSQUO + "But financially I didn" + RSQUO + "t really benefit from it, because I never filed for a patent." + RSQUO,
        "zh": "“这一切能够发生真是太好了，”他说。“但从经济上讲，我并没有真正从中获益，因为我从未申请过专利。”",
        "grammar": {
            "type": "形式主语 it + 原因从句",
            "note": "首句 It's wonderful that this happened，it 为形式主语，that this happened 为真正主语；末句 I didn't really benefit from it, because I never filed for a patent，because 引导原因状语从句，file for a patent 意为“申请专利”。"
        },
        "words": [
            {"w": "benefit from", "pos": "phr.", "def": "从……中获益"},
            {"w": "patent", "pos": "n.", "def": "专利"}
        ]
    },
    # Para G (7)
    {
        "id": 36,
        "para": 7,
        "en": "In Amsterdam today, 38" + PCT + " of all trips are made by bike and, along with Copenhagen, it is regarded as one of the two most cycle-friendly capitals in the world " + DASH + " but the city never got another Witte Fietsenplan.",
        "zh": "如今在阿姆斯特丹，所有出行中有38%是骑自行车完成的，它与哥本哈根一道被视为世界上最适合骑行的两座首都之一——但这座城市再也没能迎来另一个白色自行车计划。",
        "grammar": {
            "type": "并列句 + 被动语态 + 破折号转折",
            "note": "前半 38% of all trips are made by bike（被动）；and it is regarded as one of the two most cycle-friendly capitals，along with Copenhagen 为插入状语；破折号后 but the city never got another Witte Fietsenplan 为转折。"
        },
        "words": [
            {"w": "cycle-friendly", "pos": "adj.", "def": "适合骑自行车的"},
            {"w": "capital", "pos": "n.", "def": "首都"}
        ]
    },
    {
        "id": 37,
        "para": 7,
        "en": "Molenaar believes this may be because everybody in Amsterdam already has a bike.",
        "zh": "莫勒纳尔认为，这或许是因为阿姆斯特丹的每个人都已经有了一辆自行车。",
        "grammar": {
            "type": "宾语从句 + 表语从句(because)",
            "note": "主干 Molenaar believes (that) this may be because...；表语由 because 引导的从句充当，说明原因。"
        },
        "words": [
            {"w": "believe", "pos": "v.", "def": "认为；相信"},
            {"w": "already", "pos": "adv.", "def": "已经"}
        ]
    },
    {
        "id": 38,
        "para": 7,
        "en": "Schimmelpennink, however, cannot see that this changes Amsterdam" + RSQUO + "s need for a bike-sharing scheme.",
        "zh": "然而，希默尔彭宁克并不认为这会改变阿姆斯特丹对共享单车方案的需求。",
        "grammar": {
            "type": "宾语从句",
            "note": "主干 Schimmelpennink... cannot see that...，that this changes Amsterdam's need for a bike-sharing scheme 为宾语从句；however 为插入转折。"
        },
        "words": [
            {"w": "need", "pos": "n.", "def": "需求；需要"},
            {"w": "change", "pos": "v.", "def": "改变"}
        ]
    },
    {
        "id": 39,
        "para": 7,
        "en": LSQUO + "People who travel on the underground don" + RSQUO + "t carry their bikes around. But often they need additional transport to reach their final destination." + RSQUO,
        "zh": "“乘坐地铁的人不会随身带着自行车。但他们往往需要额外的交通工具来抵达最终目的地。”",
        "grammar": {
            "type": "定语从句 + 不定式目的",
            "note": "首句 People who travel on the underground don't carry their bikes around，who... 为定语从句修饰 People；末句 they need additional transport to reach their final destination，to reach... 为不定式作目的状语。"
        },
        "words": [
            {"w": "underground", "pos": "n.", "def": "地铁"},
            {"w": "destination", "pos": "n.", "def": "目的地"}
        ]
    },
    {
        "id": 40,
        "para": 7,
        "en": "Although he thinks it is strange that a city like Amsterdam does not have a successful bike-sharing scheme, he is optimistic about the future.",
        "zh": "尽管他觉得像阿姆斯特丹这样的城市竟然没有一个成功的共享单车方案很奇怪，但他对未来持乐观态度。",
        "grammar": {
            "type": "让步状语从句 + 形式主语",
            "note": "Although he thinks it is strange that... 为让步状语从句，其中 it 为形式主语，that a city like Amsterdam does not have... 为真正主语；主句 he is optimistic about the future。"
        },
        "words": [
            {"w": "optimistic", "pos": "adj.", "def": "乐观的"},
            {"w": "strange", "pos": "adj.", "def": "奇怪的"}
        ]
    },
    {
        "id": 41,
        "para": 7,
        "en": LSQUO + "In the " + RSQUO + "60s we didn" + RSQUO + "t stand a chance because people were prepared to give their lives to keep cars in the city. But that mentality has totally changed. Today everybody longs for cities that are not dominated by cars." + RSQUO,
        "zh": "“在60年代，我们毫无机会，因为人们愿意豁出性命也要把汽车留在城市里。但那种心态已经彻底改变。如今人人都渴望城市不再被汽车所主宰。”",
        "grammar": {
            "type": "原因从句 + 转折 + 定语从句",
            "note": "首句 we didn't stand a chance because people were prepared to give their lives to keep cars in the city，because 引导原因从句，stand a chance 意为“有机会”；末句 everybody longs for cities that are not dominated by cars，that... 为定语从句修饰 cities，long for 意为“渴望”。"
        },
        "words": [
            {"w": "mentality", "pos": "n.", "def": "心态；思维方式"},
            {"w": "long for", "pos": "phr.", "def": "渴望；盼望"}
        ]
    }
]

questions = [
    {
        "title": "Questions 14" + DASH + "18",
        "type": "matching_information",
        "instructions": [
            "Reading Passage 2 has seven paragraphs, A" + DASH + "G.",
            "Which paragraph contains the following information?",
            "Write the correct letter, A" + DASH + "G, in boxes 14" + DASH + "18 on your answer sheet.",
            "NB You may use any letter more than once."
        ],
        "items": [
            {"number": 14, "prompt": "a description of how people misused a bike-sharing scheme", "answer": "E", "evidence_sentence": 28},
            {"number": 15, "prompt": "an explanation of why a proposed bike-sharing scheme was turned down", "answer": "C", "evidence_sentence": 16},
            {"number": 16, "prompt": "a reference to a person being unable to profit from their work", "answer": "F", "evidence_sentence": 35},
            {"number": 17, "prompt": "an explanation of the potential savings a bike-sharing scheme would bring", "answer": "C", "evidence_sentence": 14},
            {"number": 18, "prompt": "a reference to the problems a bike-sharing scheme was intended to solve", "answer": "A", "evidence_sentence": 3}
        ]
    },
    {
        "title": "Questions 19 and 20",
        "type": "multiple_choice_two",
        "instructions": [
            "Choose TWO letters, A" + DASH + "E.",
            "Write the correct letters in boxes 19 and 20 on your answer sheet.",
            "Which TWO of the following statements are made in the text about the Amsterdam bike-sharing scheme of 1999?",
            "A It was initially opposed by a government department.",
            "B It failed when a partner in the scheme withdrew support.",
            "C It aimed to be more successful than the Copenhagen scheme.",
            "D It was made possible by a change in people" + RSQUO + "s attitudes.",
            "E It attracted interest from a range of bike designers."
        ],
        "items": [
            {"number": 19, "prompt": "Which TWO statements are made about the Amsterdam bike-sharing scheme of 1999? (first answer)", "answer": "B", "evidence_sentence": 29},
            {"number": 20, "prompt": "Which TWO statements are made about the Amsterdam bike-sharing scheme of 1999? (second answer)", "answer": "D", "evidence_sentence": 21}
        ]
    },
    {
        "title": "Questions 21 and 22",
        "type": "multiple_choice_two",
        "instructions": [
            "Choose TWO letters, A" + DASH + "E.",
            "Write the correct letters in boxes 21 and 22 on your answer sheet.",
            "Which TWO of the following statements are made in the text about Amsterdam today?",
            "A The majority of residents would like to prevent all cars from entering the city.",
            "B There is little likelihood of the city having another bike-sharing scheme.",
            "C More trips in the city are made by bike than by any other form of transport.",
            "D A bike-sharing scheme would benefit residents who use public transport.",
            "E The city has a reputation as a place that welcomes cyclists."
        ],
        "items": [
            {"number": 21, "prompt": "Which TWO statements are made about Amsterdam today? (first answer)", "answer": "D", "evidence_sentence": 39},
            {"number": 22, "prompt": "Which TWO statements are made about Amsterdam today? (second answer)", "answer": "E", "evidence_sentence": 36}
        ]
    },
    {
        "title": "Questions 23" + DASH + "26",
        "type": "summary_completion",
        "instructions": [
            "Complete the summary below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 23" + DASH + "26 on your answer sheet.",
            "The first urban bike-sharing scheme"
        ],
        "items": [
            {"number": 23, "prompt": "The first bike-sharing scheme was the idea of the Dutch group Provo. The people who belonged to this group were 23 ____ .", "answer": "activists", "evidence_sentence": 2},
            {"number": 24, "prompt": "They were concerned about damage to the environment and about 24 ____ , and believed that the bike-sharing scheme would draw attention to these issues.", "answer": "consumerism", "evidence_sentence": 3},
            {"number": 25, "prompt": "As well as painting some bikes white, they handed out 25 ____ that condemned the use of cars.", "answer": "leaflets", "evidence_sentence": 5},
            {"number": 26, "prompt": "However, the scheme was not a great success: almost as quickly as Provo left the bikes around the city, the 26 ____ took them away.", "answer": "police", "evidence_sentence": 9}
        ]
    }
]

phrases = [
    {"w": "bike-sharing scheme", "pos": "n.", "def": "共享单车计划"},
    {"w": "urban", "pos": "adj.", "def": "城市的；市区的"},
    {"w": "public transport", "pos": "n.", "def": "公共交通"},
    {"w": "city council", "pos": "n.", "def": "市议会"},
    {"w": "chip card", "pos": "n.", "def": "芯片卡"},
    {"w": "large-scale", "pos": "adj.", "def": "大规模的"},
    {"w": "file for a patent", "pos": "phr.", "def": "申请专利"},
    {"w": "cycle-friendly", "pos": "adj.", "def": "适合骑自行车的"},
    {"w": "get off the ground", "pos": "phr.", "def": "开始；顺利起步"},
    {"w": "the Witte Fietsenplan", "pos": "n.", "def": "白色自行车计划（荷兰语）"}
]

data = {
    "id": "c14-test1-p2",
    "source": "剑桥雅思14 · Test 1 · Passage 2",
    "title": "The growth of bike-sharing schemes around the world",
    "subtitle": "How Dutch engineer Luud Schimmelpennink helped to devise urban bike-sharing schemes",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c14-test1-p2.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
