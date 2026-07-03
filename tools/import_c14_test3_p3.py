# -*- coding: utf-8 -*-
"""Generate data/passages/c14-test3-p3.json (The power of play)."""
import json
import os

RSQUO = "’"
LSQUO = "‘"
DASH = "–"
PCT = "%"

sentences = [
    # Para 1
    {
        "id": 1,
        "para": 1,
        "en": "Virtually every child, the world over, plays.",
        "zh": "几乎每一个孩子，无论在世界哪个角落，都会玩耍。",
        "grammar": {
            "type": "主谓 + 插入状语",
            "note": "主干 every child... plays；the world over 为插入状语，意为“全世界、到处”；Virtually 意为“几乎”。"
        },
        "words": [
            {"w": "virtually", "pos": "adv.", "def": "几乎；实际上"},
            {"w": "the world over", "pos": "phr.", "def": "全世界；到处"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "The drive to play is so intense that children will do so in any circumstances, for instance when they have no real toys, or when parents do not actively encourage the behavior.",
        "zh": "玩耍的冲动如此强烈，以至于孩子们在任何情况下都会玩——例如，在他们没有真正的玩具时，或在父母并不积极鼓励这种行为时。",
        "grammar": {
            "type": "so...that 结果状语从句 + when 从句并列",
            "note": "The drive to play is so intense that... 为 so...that... 结果结构；that 从句内 children will do so in any circumstances，do so 替代 play；两个 when 引导的时间状语从句并列举例。"
        },
        "words": [
            {"w": "intense", "pos": "adj.", "def": "强烈的；剧烈的"},
            {"w": "circumstance", "pos": "n.", "def": "情况；环境"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "In the eyes of a young child, running, pretending, and building are fun.",
        "zh": "在幼儿的眼中，奔跑、假装扮演和搭建都是有趣的。",
        "grammar": {
            "type": "动名词并列主语",
            "note": "主语为并列动名词 running, pretending, and building；谓语 are fun；In the eyes of a young child 为状语，意为“在幼儿看来”。"
        },
        "words": [
            {"w": "pretend", "pos": "v.", "def": "假装；扮演"},
            {"w": "in the eyes of", "pos": "phr.", "def": "在……看来"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "Researchers and educators know that these playful activities benefit the development of the whole child across social, cognitive, physical, and emotional domains.",
        "zh": "研究人员和教育工作者知道，这些游戏活动有益于儿童在社会、认知、身体和情感各个领域的全面发展。",
        "grammar": {
            "type": "宾语从句",
            "note": "主干 Researchers and educators know that...；从句 these playful activities benefit the development of the whole child；across social, cognitive, physical, and emotional domains 为范围状语。"
        },
        "words": [
            {"w": "benefit", "pos": "v.", "def": "有益于；使受益"},
            {"w": "domain", "pos": "n.", "def": "领域；范围"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "Indeed, play is such an instrumental component to healthy child development that the United Nations High Commission on Human Rights (1989) recognized play as a fundamental right of every child.",
        "zh": "事实上，游戏对儿童的健康发展是如此重要的一个组成部分，以至于联合国人权事务高级专员公署（1989）承认游戏是每个儿童的一项基本权利。",
        "grammar": {
            "type": "such...that 结果状语从句",
            "note": "play is such an instrumental component... that... 为 such...that... 结果结构；that 从句 the United Nations... recognized play as a fundamental right，recognize A as B 结构；instrumental 意为“起重要作用的”。"
        },
        "words": [
            {"w": "instrumental", "pos": "adj.", "def": "起重要作用的；有帮助的"},
            {"w": "fundamental", "pos": "adj.", "def": "基本的；根本的"}
        ]
    },
    # Para 2
    {
        "id": 6,
        "para": 2,
        "en": "Yet, while experts continue to expound a powerful argument for the importance of play in children" + RSQUO + "s lives, the actual time children spend playing continues to decrease.",
        "zh": "然而，尽管专家们不断阐述强有力的论据来说明游戏在儿童生活中的重要性，孩子们实际用于玩耍的时间却在持续减少。",
        "grammar": {
            "type": "while 让步/对比从句 + 省略关系词定语从句",
            "note": "while experts continue to expound a powerful argument for... 为 while 引导的对比状语从句；主句 the actual time... continues to decrease，(that) children spend playing 为省略关系词定语从句修饰 time。"
        },
        "words": [
            {"w": "expound", "pos": "v.", "def": "详细阐述；解释"},
            {"w": "decrease", "pos": "v.", "def": "减少；下降"}
        ]
    },
    {
        "id": 7,
        "para": 2,
        "en": "Today, children play eight hours less each week than their counterparts did two decades ago (Elkind 2008).",
        "zh": "如今，孩子们每周玩耍的时间比二十年前的同龄人少了八个小时（埃尔金德，2008）。",
        "grammar": {
            "type": "比较结构 than",
            "note": "主干 children play eight hours less each week than their counterparts did...，than 引出比较对象，did 替代 played；counterpart 意为“同类、对应的人”。"
        },
        "words": [
            {"w": "counterpart", "pos": "n.", "def": "对应的人（物）；同类"},
            {"w": "decade", "pos": "n.", "def": "十年"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "Under pressure of rising academic standards, play is being replaced by test preparation in kindergartens and grade schools, and parents who aim to give their preschoolers a leg up are led to believe that flashcards and educational " + LSQUO + "toys" + RSQUO + " are the path to success.",
        "zh": "在学业标准不断提高的压力下，在幼儿园和小学里，游戏正被应试准备所取代；而那些想让学龄前孩子抢占先机的父母，被诱导相信识字卡片和教育性“玩具”才是通往成功的道路。",
        "grammar": {
            "type": "现在进行时被动 + and 并列 + 定语从句 + 宾语从句",
            "note": "前一分句 play is being replaced by test preparation（现在进行时被动）；Under pressure of... 为状语；and 后 parents who aim to give their preschoolers a leg up are led to believe that...，who... 为定语从句，that... 为宾语从句，give sb a leg up 意为“助某人一臂之力”。"
        },
        "words": [
            {"w": "kindergarten", "pos": "n.", "def": "幼儿园"},
            {"w": "a leg up", "pos": "phr.", "def": "助力；有利的开端"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "Our society has created a false dichotomy between play and learning.",
        "zh": "我们的社会在游戏与学习之间制造了一种错误的二分对立。",
        "grammar": {
            "type": "现在完成时",
            "note": "主干 Our society has created a false dichotomy；between play and learning 为后置定语，dichotomy 意为“二分、对立”。"
        },
        "words": [
            {"w": "dichotomy", "pos": "n.", "def": "二分；对立"},
            {"w": "false", "pos": "adj.", "def": "错误的；虚假的"}
        ]
    },
    # Para 3
    {
        "id": 10,
        "para": 3,
        "en": "Through play, children learn to regulate their behavior, lay the foundations for later learning in science and mathematics, figure out the complex negotiations of social relationships, build a repertoire of creative problem-solving skills, and so much more.",
        "zh": "通过游戏，孩子们学会调节自己的行为，为日后科学和数学的学习打下基础，弄懂社会关系中复杂的协商之道，积累一整套富有创造性的问题解决技能，以及更多其他方面。",
        "grammar": {
            "type": "并列谓语（多个不定式动作）",
            "note": "主干 children learn to regulate... lay... figure out... build... and so much more，learn to 后接一系列并列动词短语；Through play 为方式状语；lay the foundations for 意为“为……打基础”。"
        },
        "words": [
            {"w": "regulate", "pos": "v.", "def": "调节；控制"},
            {"w": "repertoire", "pos": "n.", "def": "全部技能；（可表演的）全部节目"}
        ]
    },
    {
        "id": 11,
        "para": 3,
        "en": "There is also an important role for adults in guiding children through playful learning opportunities.",
        "zh": "在引导孩子把握游戏式学习的机会方面，成年人也扮演着重要的角色。",
        "grammar": {
            "type": "there be + 介词短语状语",
            "note": "主干 There is also an important role for adults；in guiding children through playful learning opportunities 为介词短语作状语，说明成人角色的具体方面。"
        },
        "words": [
            {"w": "role", "pos": "n.", "def": "角色；作用"},
            {"w": "guide", "pos": "v.", "def": "引导；指导"}
        ]
    },
    # Para 4
    {
        "id": 12,
        "para": 4,
        "en": "Full consensus on a formal definition of play continues to elude the researchers and theorists who study it.",
        "zh": "对于游戏的正式定义，研究者和理论家们至今仍未能达成完全的共识。",
        "grammar": {
            "type": "elude + 定语从句",
            "note": "主干 Full consensus on a formal definition of play continues to elude the researchers and theorists，elude 意为“使难以理解/得到”，此处直译“共识一直躲避着研究者”，即“研究者一直无法达成共识”；who study it 为定语从句。"
        },
        "words": [
            {"w": "consensus", "pos": "n.", "def": "共识；一致意见"},
            {"w": "elude", "pos": "v.", "def": "使困惑；难以被……理解/获得"}
        ]
    },
    {
        "id": 13,
        "para": 4,
        "en": "Definitions range from discrete descriptions of various types of play such as physical, construction, language, or symbolic play (Miller & Almon 2009), to lists of broad criteria, based on observations and attitudes, that are meant to capture the essence of all play behaviors (e.g. Rubin et al. 1983).",
        "zh": "这些定义有的是对身体游戏、建构游戏、语言游戏或象征性游戏等各类游戏的具体描述（米勒和阿尔蒙，2009），有的则是一系列宽泛的标准——基于观察和态度而制定，意在把握所有游戏行为的本质（如鲁宾等，1983）。",
        "grammar": {
            "type": "range from...to... + 过去分词定语 + 定语从句",
            "note": "主干 Definitions range from A to B，range from...to... 意为“范围从……到……”；A=discrete descriptions of various types of play，B=lists of broad criteria；based on observations and attitudes 为过去分词定语，that are meant to capture the essence of all play behaviors 为定语从句修饰 criteria。"
        },
        "words": [
            {"w": "discrete", "pos": "adj.", "def": "分立的；各自独立的"},
            {"w": "criteria", "pos": "n.", "def": "标准；准则（criterion 的复数）"}
        ]
    },
    # Para 5
    {
        "id": 14,
        "para": 5,
        "en": "A majority of the contemporary definitions of play focus on several key criteria.",
        "zh": "当代关于游戏的定义大多聚焦于几项关键标准。",
        "grammar": {
            "type": "主谓宾",
            "note": "主干 A majority of the contemporary definitions of play focus on several key criteria；focus on 意为“聚焦于”。"
        },
        "words": [
            {"w": "majority", "pos": "n.", "def": "大多数"},
            {"w": "contemporary", "pos": "adj.", "def": "当代的"}
        ]
    },
    {
        "id": 15,
        "para": 5,
        "en": "The founder of the National Institute for Play, Stuart Brown, has described play as " + LSQUO + "anything that spontaneously is done for its own sake" + RSQUO + ".",
        "zh": "国家游戏研究所的创始人斯图尔特·布朗将游戏描述为“任何自发地、为其自身之故而做的事情”。",
        "grammar": {
            "type": "describe as + 定语从句",
            "note": "主干 Stuart Brown has described play as 'anything...'，describe A as B 结构；that spontaneously is done for its own sake 为定语从句修饰 anything，for its own sake 意为“为其自身之故”。"
        },
        "words": [
            {"w": "founder", "pos": "n.", "def": "创始人"},
            {"w": "spontaneously", "pos": "adv.", "def": "自发地；自然地"}
        ]
    },
    {
        "id": 16,
        "para": 5,
        "en": "More specifically, he says it " + LSQUO + "appears purposeless, produces pleasure and joy, [and] leads one to the next stage of mastery" + RSQUO + " (as quoted in Tippett 2008).",
        "zh": "更具体地说，他说游戏“看似漫无目的，能带来愉悦和快乐，并引领人进入下一阶段的精熟”（引自蒂皮特，2008）。",
        "grammar": {
            "type": "宾语从句 + 三并列谓语",
            "note": "主干 he says (that) it appears purposeless, produces pleasure and joy, [and] leads one to the next stage of mastery，宾语从句内三个并列谓语；as quoted in Tippett 2008 为插入引用说明。"
        },
        "words": [
            {"w": "purposeless", "pos": "adj.", "def": "无目的的；漫无目的的"},
            {"w": "mastery", "pos": "n.", "def": "精通；掌握"}
        ]
    },
    {
        "id": 17,
        "para": 5,
        "en": "Similarly, Miller and Almon (2009) say that play includes " + LSQUO + "activities that are freely chosen and directed by children and arise from intrinsic motivation" + RSQUO + ".",
        "zh": "类似地，米勒和阿尔蒙（2009）说，游戏包括“那些由孩子自由选择和主导、并源于内在动机的活动”。",
        "grammar": {
            "type": "宾语从句 + 定语从句",
            "note": "主干 Miller and Almon say that play includes 'activities...'；that are freely chosen and directed by children and arise from intrinsic motivation 为定语从句修饰 activities，含三个并列谓语（被动 chosen/directed 与主动 arise）。"
        },
        "words": [
            {"w": "intrinsic", "pos": "adj.", "def": "内在的；固有的"},
            {"w": "arise from", "pos": "phr.", "def": "源于；由……引起"}
        ]
    },
    {
        "id": 18,
        "para": 5,
        "en": "Often, play is defined along a continuum as more or less playful using the following set of behavioral and dispositional criteria (e.g. Rubin et al. 1983).",
        "zh": "游戏常常被沿着一个连续体、以下列这组行为和性情标准来界定其游戏性的强弱（如鲁宾等，1983）。",
        "grammar": {
            "type": "被动语态 + 现在分词状语",
            "note": "主干 play is defined along a continuum as more or less playful（被动）；using the following set of... criteria 为现在分词状语表方式；continuum 意为“连续体”。"
        },
        "words": [
            {"w": "continuum", "pos": "n.", "def": "连续体；连续统一体"},
            {"w": "dispositional", "pos": "adj.", "def": "性情的；倾向的"}
        ]
    },
    # Para 6 (criteria list, condensed)
    {
        "id": 19,
        "para": 6,
        "en": "Play is pleasurable: Children must enjoy the activity or it is not play. It is intrinsically motivated: Children engage in play simply for the satisfaction the behavior itself brings.",
        "zh": "游戏是令人愉悦的：孩子必须享受这项活动，否则它就不算游戏。游戏是由内在动机驱动的：孩子参与游戏，仅仅是为了行为本身所带来的满足感。",
        "grammar": {
            "type": "冒号解释 + or 结果",
            "note": "首句 Children must enjoy the activity or it is not play，or 表“否则”；后句 Children engage in play simply for the satisfaction (that) the behavior itself brings，含省略关系词定语从句修饰 satisfaction。"
        },
        "words": [
            {"w": "pleasurable", "pos": "adj.", "def": "令人愉悦的"},
            {"w": "engage in", "pos": "phr.", "def": "参与；从事"}
        ]
    },
    {
        "id": 20,
        "para": 6,
        "en": "It has no extrinsically motivated function or goal. Play is process oriented: When children play, the means are more important than the ends.",
        "zh": "它没有由外在动机驱动的功能或目标。游戏是过程导向的：当孩子玩耍时，手段比结果更重要。",
        "grammar": {
            "type": "冒号解释 + when 时间从句 + 比较",
            "note": "首句 It has no extrinsically motivated function or goal；后句 When children play 为时间状语从句，主句 the means are more important than the ends，means（手段）与 ends（目的）对照。"
        },
        "words": [
            {"w": "extrinsically", "pos": "adv.", "def": "外在地；非本质地"},
            {"w": "process oriented", "pos": "phr.", "def": "过程导向的"}
        ]
    },
    {
        "id": 21,
        "para": 6,
        "en": "It is freely chosen, spontaneous and voluntary. If a child is pressured, they will likely not think of the activity as play.",
        "zh": "游戏是自由选择的、自发的和自愿的。如果一个孩子受到压力，他们很可能就不会把这项活动视为游戏。",
        "grammar": {
            "type": "并列表语 + if 条件从句",
            "note": "首句 It is freely chosen, spontaneous and voluntary，三并列表语；后句 If a child is pressured 为条件状语从句，主句 they will likely not think of the activity as play，think of A as B 结构。"
        },
        "words": [
            {"w": "voluntary", "pos": "adj.", "def": "自愿的；主动的"},
            {"w": "pressure", "pos": "v.", "def": "对……施压"}
        ]
    },
    {
        "id": 22,
        "para": 6,
        "en": "Play is actively engaged: Players must be physically and/or mentally involved in the activity. Play is non-literal. It involves make-believe.",
        "zh": "游戏是需要积极投入的：玩耍者必须在身体和／或心理上参与到活动之中。游戏是非现实的，它涉及假想扮演。",
        "grammar": {
            "type": "冒号解释 + 简单句",
            "note": "首句 Players must be physically and/or mentally involved in the activity；末两句 Play is non-literal. It involves make-believe，non-literal 意为“非字面的、非现实的”，make-believe 意为“假想、扮演”。"
        },
        "words": [
            {"w": "non-literal", "pos": "adj.", "def": "非字面的；非现实的"},
            {"w": "make-believe", "pos": "n.", "def": "假想；假扮"}
        ]
    },
    # Para 7
    {
        "id": 23,
        "para": 7,
        "en": "According to this view, children" + RSQUO + "s playful behaviors can range in degree from 0" + PCT + " to 100" + PCT + " playful.",
        "zh": "按照这种观点，孩子们的游戏行为在程度上可以从0%到100%的游戏性之间变化。",
        "grammar": {
            "type": "range from...to... 结构",
            "note": "主干 children's playful behaviors can range in degree from 0% to 100% playful；According to this view 为状语；range from...to... 表程度范围。"
        },
        "words": [
            {"w": "range", "pos": "v.", "def": "（在一定范围内）变化"},
            {"w": "degree", "pos": "n.", "def": "程度；度"}
        ]
    },
    {
        "id": 24,
        "para": 7,
        "en": "Rubin and colleagues did not assign greater weight to any one dimension in determining playfulness; however, other researchers have suggested that process orientation and a lack of obvious functional purpose may be the most important aspects of play (e.g. Pellegrini 2009).",
        "zh": "鲁宾及其同事在判定游戏性时，并未赋予任何单一维度更大的权重；然而，其他研究者提出，过程导向和缺乏明显的功能目的，可能才是游戏最重要的方面（如佩莱格里尼，2009）。",
        "grammar": {
            "type": "分号并列 + however + 宾语从句",
            "note": "前句 Rubin and colleagues did not assign greater weight to any one dimension；分号后 however, other researchers have suggested that...，that process orientation and a lack of obvious functional purpose may be the most important aspects 为宾语从句；assign weight to 意为“赋予权重”。"
        },
        "words": [
            {"w": "assign", "pos": "v.", "def": "分配；赋予"},
            {"w": "dimension", "pos": "n.", "def": "维度；方面"}
        ]
    },
    # Para 8
    {
        "id": 25,
        "para": 8,
        "en": "From the perspective of a continuum, play can thus blend with other motives and attitudes that are less playful, such as work.",
        "zh": "从连续体的视角看，游戏因此可以与其他游戏性较弱的动机和态度（例如工作）相融合。",
        "grammar": {
            "type": "定语从句",
            "note": "主干 play can thus blend with other motives and attitudes；that are less playful 为定语从句修饰 motives and attitudes，such as work 为举例；From the perspective of a continuum 为状语。"
        },
        "words": [
            {"w": "perspective", "pos": "n.", "def": "视角；观点"},
            {"w": "blend with", "pos": "phr.", "def": "与……融合"}
        ]
    },
    {
        "id": 26,
        "para": 8,
        "en": "Unlike play, work is typically not viewed as enjoyable and it is extrinsically motivated (i.e. it is goal oriented).",
        "zh": "与游戏不同，工作通常不被视为令人愉悦的，而且它是由外在动机驱动的（即它是目标导向的）。",
        "grammar": {
            "type": "介词短语状语 + 并列句",
            "note": "Unlike play 为介词短语作状语；主句为并列句 work is typically not viewed as enjoyable and it is extrinsically motivated；括号内 i.e. it is goal oriented 为补充解释。"
        },
        "words": [
            {"w": "enjoyable", "pos": "adj.", "def": "令人愉快的"},
            {"w": "goal oriented", "pos": "phr.", "def": "目标导向的"}
        ]
    },
    {
        "id": 27,
        "para": 8,
        "en": "Researcher Joan Goodman (1994) suggested that hybrid forms of work and play are not a detriment to learning; rather, they can provide optimal contexts for learning.",
        "zh": "研究者琼·古德曼（1994）提出，工作与游戏的混合形式并不有损于学习；相反，它们能为学习提供最理想的情境。",
        "grammar": {
            "type": "宾语从句 + rather 对比",
            "note": "主干 Joan Goodman suggested that...；宾语从句 hybrid forms of work and play are not a detriment to learning；rather, they can provide optimal contexts for learning，rather 表转折对比，a detriment to 意为“对……的损害”。"
        },
        "words": [
            {"w": "hybrid", "pos": "adj.", "def": "混合的；杂交的"},
            {"w": "optimal", "pos": "adj.", "def": "最理想的；最佳的"}
        ]
    },
    {
        "id": 28,
        "para": 8,
        "en": "For example, a child may be engaged in a difficult, goal-directed activity set up by their teacher, but they may still be actively engaged and intrinsically motivated.",
        "zh": "例如，一个孩子可能正在从事一项由老师安排的、有难度的、目标明确的活动，但他们仍然可能是积极投入且受内在动机驱动的。",
        "grammar": {
            "type": "过去分词定语 + but 转折",
            "note": "前一分句 a child may be engaged in a difficult, goal-directed activity；set up by their teacher 为过去分词定语修饰 activity；but 后 they may still be actively engaged and intrinsically motivated。"
        },
        "words": [
            {"w": "goal-directed", "pos": "adj.", "def": "目标导向的"},
            {"w": "engaged", "pos": "adj.", "def": "投入的；忙于……的"}
        ]
    },
    {
        "id": 29,
        "para": 8,
        "en": "At this mid-point between play and work, the child" + RSQUO + "s motivation, coupled with guidance from an adult, can create robust opportunities for playful learning.",
        "zh": "在游戏与工作之间的这个中间点上，孩子的动机再加上成人的引导，能够为游戏式学习创造出强有力的机会。",
        "grammar": {
            "type": "coupled with 插入 + 主谓宾",
            "note": "主干 the child's motivation... can create robust opportunities for playful learning；coupled with guidance from an adult 为过去分词短语作插入状语，coupled with 意为“加上、连同”；robust 意为“强有力的”。"
        },
        "words": [
            {"w": "coupled with", "pos": "phr.", "def": "加上；连同"},
            {"w": "robust", "pos": "adj.", "def": "强健的；强有力的"}
        ]
    },
    # Para 9
    {
        "id": 30,
        "para": 9,
        "en": "Critically, recent research supports the idea that adults can facilitate children" + RSQUO + "s learning while maintaining a playful approach in interactions known as " + LSQUO + "guided play" + RSQUO + " (Fisher et al. 2011).",
        "zh": "至关重要的是，近期的研究支持这样一种观点：成年人能够在被称为“引导式游戏”的互动中，一边保持游戏化的方式，一边促进孩子的学习（费希尔等，2011）。",
        "grammar": {
            "type": "同位语从句 + while 状语 + 过去分词定语",
            "note": "主干 recent research supports the idea；that adults can facilitate children's learning 为同位语从句；while maintaining a playful approach in interactions 为 while 引导的伴随状语；known as 'guided play' 为过去分词定语修饰 interactions。"
        },
        "words": [
            {"w": "facilitate", "pos": "v.", "def": "促进；使便利"},
            {"w": "guided play", "pos": "n.", "def": "引导式游戏"}
        ]
    },
    {
        "id": 31,
        "para": 9,
        "en": "The adult" + RSQUO + "s role in play varies as a function of their educational goals and the child" + RSQUO + "s developmental level (Hirsch-Pasek et al. 2009).",
        "zh": "成年人在游戏中的角色，会随其教育目标和孩子的发展水平而变化（赫希-帕塞克等，2009）。",
        "grammar": {
            "type": "as a function of 结构",
            "note": "主干 The adult's role in play varies；as a function of their educational goals and the child's developmental level，as a function of 意为“随……而变化、取决于”。"
        },
        "words": [
            {"w": "vary", "pos": "v.", "def": "变化；不同"},
            {"w": "developmental", "pos": "adj.", "def": "发展的；成长的"}
        ]
    },
    # Para 10
    {
        "id": 32,
        "para": 10,
        "en": "Guided play takes two forms.",
        "zh": "引导式游戏有两种形式。",
        "grammar": {
            "type": "主谓宾",
            "note": "极简单句，主干 Guided play takes two forms；take forms 意为“采取……形式”。"
        },
        "words": [
            {"w": "form", "pos": "n.", "def": "形式；形态"},
            {"w": "take", "pos": "v.", "def": "采取；呈现"}
        ]
    },
    {
        "id": 33,
        "para": 10,
        "en": "At a very basic level, adults can enrich the child" + RSQUO + "s environment by providing objects or experiences that promote aspects of a curriculum.",
        "zh": "在最基础的层面上，成年人可以通过提供有助于课程某些方面的物品或体验，来丰富孩子的环境。",
        "grammar": {
            "type": "by 方式状语 + 定语从句",
            "note": "主干 adults can enrich the child's environment；by providing objects or experiences 为方式状语；that promote aspects of a curriculum 为定语从句修饰 objects or experiences。"
        },
        "words": [
            {"w": "enrich", "pos": "v.", "def": "丰富；使充实"},
            {"w": "curriculum", "pos": "n.", "def": "课程"}
        ]
    },
    {
        "id": 34,
        "para": 10,
        "en": "In the more direct form of guided play, parents or other adults can support children" + RSQUO + "s play by joining in the fun as a co-player, raising thoughtful questions, commenting on children" + RSQUO + "s discoveries, or encouraging further exploration or new facets to the child" + RSQUO + "s activity.",
        "zh": "在更为直接的引导式游戏形式中，父母或其他成年人可以支持孩子的游戏——作为共同玩伴一起参与其中，提出发人深省的问题，对孩子的发现加以评论，或鼓励孩子对其活动做进一步的探索或开拓新的方面。",
        "grammar": {
            "type": "by + 动名词并列",
            "note": "主干 parents or other adults can support children's play；by joining in the fun..., raising..., commenting on..., or encouraging... 为 by 引导的方式状语，含四个并列动名词短语；as a co-player 为身份状语。"
        },
        "words": [
            {"w": "co-player", "pos": "n.", "def": "共同玩伴；一起玩的人"},
            {"w": "facet", "pos": "n.", "def": "方面；层面"}
        ]
    },
    {
        "id": 35,
        "para": 10,
        "en": "Although playful learning can be somewhat structured, it must also be child-centered (Nicolopolou et al. 2006). Play should stem from the child" + RSQUO + "s own desire.",
        "zh": "尽管游戏式学习可以在一定程度上有结构，它也必须是以孩子为中心的（尼科洛普卢等，2006）。游戏应当源自孩子自己的意愿。",
        "grammar": {
            "type": "让步状语从句 + stem from",
            "note": "Although playful learning can be somewhat structured 为让步状语从句；主句 it must also be child-centered；末句 Play should stem from the child's own desire，stem from 意为“源于”。"
        },
        "words": [
            {"w": "child-centered", "pos": "adj.", "def": "以孩子为中心的"},
            {"w": "stem from", "pos": "phr.", "def": "源于；起源于"}
        ]
    },
    # Para 11
    {
        "id": 36,
        "para": 11,
        "en": "Both free and guided play are essential elements in a child-centered approach to playful learning.",
        "zh": "自由游戏和引导式游戏，都是以孩子为中心的游戏式学习方法中不可或缺的要素。",
        "grammar": {
            "type": "both...and 并列主语",
            "note": "主干 Both free and guided play are essential elements，both...and... 并列主语；in a child-centered approach to playful learning 为后置定语/状语。"
        },
        "words": [
            {"w": "essential", "pos": "adj.", "def": "必不可少的；本质的"},
            {"w": "element", "pos": "n.", "def": "要素；成分"}
        ]
    },
    {
        "id": 37,
        "para": 11,
        "en": "Intrinsically motivated free play provides the child with true autonomy, while guided play is an avenue through which parents and educators can provide more targeted learning experiences.",
        "zh": "由内在动机驱动的自由游戏赋予孩子真正的自主性，而引导式游戏则是父母和教育者据以提供更有针对性学习体验的一种途径。",
        "grammar": {
            "type": "while 对比从句 + through which 定语从句",
            "note": "主句 Intrinsically motivated free play provides the child with true autonomy，provide sb with sth 结构；while guided play is an avenue 为对比状语从句；through which parents and educators can provide... 为定语从句修饰 avenue。"
        },
        "words": [
            {"w": "autonomy", "pos": "n.", "def": "自主；自治"},
            {"w": "avenue", "pos": "n.", "def": "途径；方法"}
        ]
    },
    {
        "id": 38,
        "para": 11,
        "en": "In either case, play should be actively engaged, it should be predominantly child-directed, and it must be fun.",
        "zh": "无论哪种情况，游戏都应当是积极投入的，都应当以孩子为主导，而且都必须是有趣的。",
        "grammar": {
            "type": "三并列分句",
            "note": "三个并列分句 play should be actively engaged / it should be predominantly child-directed / it must be fun；In either case 为状语，意为“无论哪种情况”；predominantly 意为“主要地”。"
        },
        "words": [
            {"w": "predominantly", "pos": "adv.", "def": "主要地；占主导地"},
            {"w": "child-directed", "pos": "adj.", "def": "以孩子为主导的"}
        ]
    }
]

questions = [
    {
        "title": "Questions 27" + DASH + "31",
        "type": "matching_people",
        "instructions": [
            "Look at the following statements (Questions 27" + DASH + "31) and the list of researchers below.",
            "Match each statement with the correct researcher, A" + DASH + "G.",
            "Write the correct letter, A" + DASH + "G, in boxes 27" + DASH + "31 on your answer sheet.",
            "A Elkind",
            "B Miller & Almon",
            "C Rubin et al.",
            "D Stuart Brown",
            "E Pellegrini",
            "F Joan Goodman",
            "G Hirsch-Pasek et al."
        ],
        "items": [
            {"number": 27, "prompt": "Play can be divided into a number of separate categories.", "answer": "B", "evidence_sentence": 13},
            {"number": 28, "prompt": "Adults" + RSQUO + " intended goals affect how they play with children.", "answer": "G", "evidence_sentence": 31},
            {"number": 29, "prompt": "Combining work with play may be the best way for children to learn.", "answer": "F", "evidence_sentence": 27},
            {"number": 30, "prompt": "Certain elements of play are more significant than others.", "answer": "E", "evidence_sentence": 24},
            {"number": 31, "prompt": "Activities can be classified on a scale of playfulness.", "answer": "C", "evidence_sentence": 18}
        ]
    },
    {
        "title": "Questions 32" + DASH + "36",
        "type": "yes_no_notgiven",
        "instructions": [
            "Do the following statements agree with the claims of the writer in Reading Passage 3?",
            "In boxes 32" + DASH + "36 on your answer sheet, write",
            "YES if the statement agrees with the claims of the writer",
            "NO if the statement contradicts the claims of the writer",
            "NOT GIVEN if it is impossible to say what the writer thinks about this"
        ],
        "items": [
            {"number": 32, "prompt": "Children need toys in order to play.", "answer": "NO", "evidence_sentence": 2},
            {"number": 33, "prompt": "It is a mistake to treat play and learning as separate types of activities.", "answer": "YES", "evidence_sentence": 9},
            {"number": 34, "prompt": "Play helps children to develop their artistic talents.", "answer": "NOT GIVEN", "evidence_sentence": 10},
            {"number": 35, "prompt": "Researchers have agreed on a definition of play.", "answer": "NO", "evidence_sentence": 12},
            {"number": 36, "prompt": "Work and play differ in terms of whether or not they have a target.", "answer": "YES", "evidence_sentence": 26}
        ]
    },
    {
        "title": "Questions 37" + DASH + "40",
        "type": "summary_completion",
        "instructions": [
            "Complete the summary below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 37" + DASH + "40 on your answer sheet.",
            "Guided play"
        ],
        "items": [
            {"number": 37, "prompt": "Alternatively, an adult can play with a child and develop the play, for instance by 37 ____ the child to investigate different aspects of their game.", "answer": "encouraging", "evidence_sentence": 34},
            {"number": 38, "prompt": "Adults can help children to learn through play, and may make the activity rather structured, but it should still be based on the child" + RSQUO + "s 38 ____ to play.", "answer": "desire", "evidence_sentence": 35},
            {"number": 39, "prompt": "Play without the intervention of adults gives children real 39 ____ ;", "answer": "autonomy", "evidence_sentence": 37},
            {"number": 40, "prompt": "with adults, play can be 40 ____ at particular goals.", "answer": "targeted", "evidence_sentence": 37}
        ]
    }
]

phrases = [
    {"w": "guided play", "pos": "n.", "def": "引导式游戏"},
    {"w": "free play", "pos": "n.", "def": "自由游戏"},
    {"w": "playful learning", "pos": "n.", "def": "游戏式学习"},
    {"w": "intrinsic motivation", "pos": "n.", "def": "内在动机"},
    {"w": "process oriented", "pos": "phr.", "def": "过程导向的"},
    {"w": "child-centered", "pos": "adj.", "def": "以孩子为中心的"},
    {"w": "make-believe", "pos": "n.", "def": "假想；假扮"},
    {"w": "a leg up", "pos": "phr.", "def": "助力；有利的开端"},
    {"w": "stem from", "pos": "phr.", "def": "源于；起源于"},
    {"w": "as a function of", "pos": "phr.", "def": "随……而变化；取决于"}
]

data = {
    "id": "c14-test3-p3",
    "source": "剑桥雅思14 · Test 3 · Passage 3",
    "title": "The power of play",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c14-test3-p3.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
