# -*- coding: utf-8 -*-
"""Generate data/passages/c14-test1-p1.json (THE IMPORTANCE OF CHILDREN'S PLAY)."""
import json
import os

RSQUO = "’"
LSQUO = "‘"
RDQUO = "”"
LDQUO = "“"
DASH = "–"

sentences = [
    # Para 1
    {
        "id": 1,
        "para": 1,
        "en": "Brick by brick, six-year-old Alice is building a magical kingdom.",
        "zh": "六岁的爱丽丝正一块砖一块砖地搭建着一个魔法王国。",
        "grammar": {
            "type": "现在进行时 + 名词短语状语",
            "note": "主干 Alice is building a magical kingdom；Brick by brick 为名词短语作方式状语，表“一块砖接一块砖地”，置于句首起强调。"
        },
        "words": [
            {"w": "brick", "pos": "n.", "def": "砖块"},
            {"w": "magical", "pos": "adj.", "def": "魔法的；神奇的"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "Imagining fairy-tale turrets and fire-breathing dragons, wicked witches and gallant heroes, she" + RSQUO + "s creating an enchanting world.",
        "zh": "她想象着童话中的塔楼和喷火的巨龙、邪恶的女巫和英勇的英雄，正创造出一个迷人的世界。",
        "grammar": {
            "type": "现在分词状语 + 现在进行时",
            "note": "Imagining... 为现在分词短语作伴随状语；其宾语由 turrets and dragons, witches and heroes 两组并列名词短语构成；主句 she's creating an enchanting world。"
        },
        "words": [
            {"w": "turret", "pos": "n.", "def": "（城堡的）塔楼；角楼"},
            {"w": "gallant", "pos": "adj.", "def": "英勇的；豪侠的"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "Although she isn" + RSQUO + "t aware of it, this fantasy is helping her take her first steps towards her capacity for creativity and so it will have important repercussions in her adult life.",
        "zh": "尽管她自己并未意识到，这种幻想正帮助她迈出通向创造力的第一步，因而将对她的成年生活产生重要影响。",
        "grammar": {
            "type": "让步状语从句 + help sb do + so 结果",
            "note": "Although she isn't aware of it 为让步状语从句；主句 this fantasy is helping her take her first steps...，help sb (to) do 结构；and so it will have important repercussions 由 so 引出结果分句。"
        },
        "words": [
            {"w": "fantasy", "pos": "n.", "def": "幻想；想象"},
            {"w": "repercussion", "pos": "n.", "def": "（间接的）影响；反响"}
        ]
    },
    # Para 2
    {
        "id": 4,
        "para": 2,
        "en": "Minutes later, Alice has abandoned the kingdom in favour of playing schools with her younger brother.",
        "zh": "几分钟后，爱丽丝就抛下了那个王国，转而和弟弟玩起了“学校”的游戏。",
        "grammar": {
            "type": "现在完成时 + in favour of 短语",
            "note": "主干 Alice has abandoned the kingdom；in favour of playing schools with her younger brother 为介词短语作状语，in favour of 意为“转而选择、更喜欢”，其后接动名词。"
        },
        "words": [
            {"w": "abandon", "pos": "v.", "def": "抛弃；放弃"},
            {"w": "in favour of", "pos": "phr.", "def": "转而支持；更喜欢"}
        ]
    },
    {
        "id": 5,
        "para": 2,
        "en": "When she bosses him around as his " + LSQUO + "teacher" + RSQUO + ", she" + RSQUO + "s practising how to regulate her emotions through pretence.",
        "zh": "当她以“老师”的身份对弟弟发号施令时，她正在通过假扮来练习如何调节自己的情绪。",
        "grammar": {
            "type": "时间状语从句 + 宾语从句",
            "note": "When she bosses him around as his 'teacher' 为时间状语从句，boss sb around 意为“对某人指手画脚”；主句 she's practising how to regulate her emotions，how to... 为宾语；through pretence 为方式状语。"
        },
        "words": [
            {"w": "boss around", "pos": "phr.", "def": "对……发号施令；使唤"},
            {"w": "pretence", "pos": "n.", "def": "假装；假扮"}
        ]
    },
    {
        "id": 6,
        "para": 2,
        "en": "Later on, when they tire of this and settle down with a board game, she" + RSQUO + "s learning about the need to follow rules and take turns with a partner.",
        "zh": "再往后，当他们玩腻了这个、安静下来玩一局棋盘游戏时，她正在体会遵守规则、与同伴轮流行动的必要性。",
        "grammar": {
            "type": "时间状语从句 + 宾语 + 不定式定语",
            "note": "when they tire of this and settle down with a board game 为时间状语从句，tire of 与 settle down 两谓语并列；主句 she's learning about the need to follow rules and take turns，to follow rules and take turns 为不定式作 the need 的后置定语。"
        },
        "words": [
            {"w": "tire of", "pos": "phr.", "def": "对……感到厌倦"},
            {"w": "take turns", "pos": "phr.", "def": "轮流"}
        ]
    },
    # Para 3
    {
        "id": 7,
        "para": 3,
        "en": LSQUO + "Play in all its rich variety is one of the highest achievements of the human species," + RSQUO + " says Dr David Whitebread from the Faculty of Education at the University of Cambridge, UK.",
        "zh": "“形式丰富多样的游戏，是人类物种最高的成就之一，”英国剑桥大学教育学院的戴维·怀特布雷德博士说。",
        "grammar": {
            "type": "直接引语 + 主谓倒装",
            "note": "引语为主句 Play... is one of the highest achievements of the human species；says Dr David Whitebread... 为引述部分，主谓倒装（says + 主语）；from the Faculty of Education... 为介词短语作后置定语。"
        },
        "words": [
            {"w": "variety", "pos": "n.", "def": "多样性；种类"},
            {"w": "faculty", "pos": "n.", "def": "（大学的）学院；系"}
        ]
    },
    {
        "id": 8,
        "para": 3,
        "en": LSQUO + "It underpins how we develop as intellectual, problem-solving adults and is crucial to our success as a highly adaptable species." + RSQUO,
        "zh": "“它支撑着我们如何成长为善于思考、善于解决问题的成年人，对我们作为一个高度适应性物种的成功至关重要。”",
        "grammar": {
            "type": "宾语从句 + 并列谓语",
            "note": "主语 It 带两个并列谓语 underpins how we develop... 与 is crucial to our success...；how we develop as intellectual, problem-solving adults 为宾语从句；as a highly adaptable species 为方式状语。"
        },
        "words": [
            {"w": "underpin", "pos": "v.", "def": "支撑；巩固；作为……的基础"},
            {"w": "adaptable", "pos": "adj.", "def": "适应性强的；能适应的"}
        ]
    },
    {
        "id": 9,
        "para": 3,
        "en": "Recognising the importance of play is not new: over two millennia ago, the Greek philosopher Plato extolled its virtues as a means of developing skills for adult life, and ideas about play-based learning have been developing since the 19th century.",
        "zh": "认识到游戏的重要性并非新鲜事：两千多年前，希腊哲学家柏拉图就赞扬游戏是培养成年生活所需技能的一种手段，而关于游戏式学习的理念自19世纪以来一直在发展。",
        "grammar": {
            "type": "动名词主语 + 冒号 + and 并列",
            "note": "主句主语为动名词短语 Recognising the importance of play，谓语 is not new；冒号后为两个并列分句：Plato extolled its virtues as a means of...（一般过去时）与 ideas... have been developing since the 19th century（现在完成进行时）。"
        },
        "words": [
            {"w": "extol", "pos": "v.", "def": "颂扬；赞美"},
            {"w": "millennia", "pos": "n.", "def": "千年（millennium 的复数）"}
        ]
    },
    # Para 4
    {
        "id": 10,
        "para": 4,
        "en": "But we live in changing times, and Whitebread is mindful of a worldwide decline in play, pointing out that over half the people in the world now live in cities.",
        "zh": "但我们生活在一个变化的时代，怀特布雷德留意到全球范围内游戏的减少，他指出如今世界上一半以上的人口居住在城市。",
        "grammar": {
            "type": "并列句 + 现在分词状语 + 宾语从句",
            "note": "两个分句由 and 连接；后一分句 Whitebread is mindful of a worldwide decline in play，be mindful of 意为“留意、关注”；pointing out that... 为现在分词短语作伴随状语，that 引导宾语从句。"
        },
        "words": [
            {"w": "mindful", "pos": "adj.", "def": "留心的；注意的"},
            {"w": "decline", "pos": "n.", "def": "下降；减少；衰退"}
        ]
    },
    {
        "id": 11,
        "para": 4,
        "en": LSQUO + "The opportunities for free play, which I experienced almost every day of my childhood, are becoming increasingly scarce," + RSQUO + " he says.",
        "zh": "“自由游戏的机会——我童年时几乎每天都能体验到——正变得越来越稀少，”他说。",
        "grammar": {
            "type": "非限制性定语从句插入 + 现在进行时",
            "note": "主干 The opportunities for free play... are becoming increasingly scarce；which I experienced almost every day of my childhood 为非限制性定语从句，插在主语与谓语之间修饰 opportunities。"
        },
        "words": [
            {"w": "scarce", "pos": "adj.", "def": "稀少的；不足的"},
            {"w": "increasingly", "pos": "adv.", "def": "越来越；日益"}
        ]
    },
    {
        "id": 12,
        "para": 4,
        "en": "Outdoor play is curtailed by perceptions of risk to do with traffic, as well as parents" + RSQUO + " increased wish to protect their children from being the victims of crime, and by the emphasis on " + LSQUO + "earlier is better" + RSQUO + " which is leading to greater competition in academic learning and schools.",
        "zh": "户外游戏受到限制，原因既有与交通相关的风险认知、家长愈发希望保护孩子免遭犯罪侵害，也有对“越早越好”的强调——后者正导致学业学习和学校中更激烈的竞争。",
        "grammar": {
            "type": "被动语态 + by...as well as...and by... 并列 + 定语从句",
            "note": "主干 Outdoor play is curtailed by A, as well as B, and by C（被动，多重原因并列）：A=perceptions of risk to do with traffic，B=parents' increased wish to protect...，C=the emphasis on 'earlier is better'；which is leading to greater competition... 为定语从句修饰 the emphasis。"
        },
        "words": [
            {"w": "curtail", "pos": "v.", "def": "缩减；限制"},
            {"w": "perception", "pos": "n.", "def": "认知；看法"}
        ]
    },
    {
        "id": 13,
        "para": 4,
        "en": "International bodies like the United Nations and the European Union have begun to develop policies concerned with children" + RSQUO + "s right to play, and to consider implications for leisure facilities and educational programmes.",
        "zh": "联合国和欧盟等国际机构已开始制定关注儿童游戏权利的政策，并考虑其对休闲设施和教育项目的影响。",
        "grammar": {
            "type": "现在完成时 + 不定式并列 + 过去分词定语",
            "note": "主干 International bodies... have begun to develop policies... and to consider implications...，两个不定式 to develop 与 to consider 并列作 begun 的宾语；concerned with children's right to play 为过去分词短语作 policies 的后置定语。"
        },
        "words": [
            {"w": "body", "pos": "n.", "def": "机构；团体"},
            {"w": "implication", "pos": "n.", "def": "影响；可能的后果"}
        ]
    },
    {
        "id": 14,
        "para": 4,
        "en": "But what they often lack is the evidence to base policies on.",
        "zh": "但它们往往缺乏据以制定政策的证据。",
        "grammar": {
            "type": "主语从句 + 不定式定语",
            "note": "主语为 what they often lack（what 引导的主语从句），表语 the evidence；to base policies on 为不定式作后置定语修饰 evidence，base sth on 意为“把……建立在……之上”。"
        },
        "words": [
            {"w": "lack", "pos": "v.", "def": "缺乏；没有"},
            {"w": "evidence", "pos": "n.", "def": "证据；依据"}
        ]
    },
    # Para 5
    {
        "id": 15,
        "para": 5,
        "en": LSQUO + "The type of play we are interested in is child-initiated, spontaneous and unpredictable " + DASH + " but, as soon as you ask a five-year-old " + LDQUO + "to play" + RDQUO + ", then you as the researcher have intervened," + RSQUO + " explains Dr Sara Baker.",
        "zh": "“我们感兴趣的那种游戏是由儿童发起的、自发的、不可预测的——但只要你一让一个五岁孩子‘去玩’，那么作为研究者的你就已经介入了，”萨拉·贝克博士解释道。",
        "grammar": {
            "type": "省略关系词定语从句 + as soon as 时间从句 + 引述倒装",
            "note": "主语 The type of play (that) we are interested in 含省略关系词的定语从句；表语为三个并列形容词 child-initiated, spontaneous and unpredictable；破折号后 as soon as you ask... 为时间状语从句，主句 you... have intervened；explains Dr Sara Baker 为主谓倒装的引述。"
        },
        "words": [
            {"w": "spontaneous", "pos": "adj.", "def": "自发的；自然产生的"},
            {"w": "intervene", "pos": "v.", "def": "介入；干预"}
        ]
    },
    {
        "id": 16,
        "para": 5,
        "en": LSQUO + "And we want to know what the long-term impact of play is. It" + RSQUO + "s a real challenge." + RSQUO,
        "zh": "“而我们想知道游戏的长期影响是什么。这是一个真正的难题。”",
        "grammar": {
            "type": "宾语从句 + 主系表",
            "note": "前句 we want to know what the long-term impact of play is，what... 为宾语从句（陈述语序）；后句 It's a real challenge 为主系表结构。"
        },
        "words": [
            {"w": "long-term", "pos": "adj.", "def": "长期的"},
            {"w": "challenge", "pos": "n.", "def": "挑战；难题"}
        ]
    },
    # Para 6
    {
        "id": 17,
        "para": 6,
        "en": "Dr Jenny Gibson agrees, pointing out that although some of the steps in the puzzle of how and why play is important have been looked at, there is very little data on the impact it has on the child" + RSQUO + "s later life.",
        "zh": "珍妮·吉布森博士对此表示赞同，她指出，尽管游戏为何重要、如何重要这一谜题中的某些环节已被研究过，但关于游戏对孩子日后生活之影响的数据却少之又少。",
        "grammar": {
            "type": "现在分词状语 + 让步从句 + there be",
            "note": "主句 Dr Jenny Gibson agrees；pointing out that... 为现在分词状语，其宾语从句内含 although... have been looked at 让步从句；主句 there is very little data on the impact (that) it has on the child's later life，含省略关系词定语从句。"
        },
        "words": [
            {"w": "puzzle", "pos": "n.", "def": "谜；难题"},
            {"w": "data", "pos": "n.", "def": "数据；资料"}
        ]
    },
    {
        "id": 18,
        "para": 6,
        "en": "Now, thanks to the university" + RSQUO + "s new Centre for Research on Play in Education, Development and Learning (PEDAL), Whitebread, Baker, Gibson and a team of researchers hope to provide evidence on the role played by play in how a child develops.",
        "zh": "如今，得益于该校新成立的“游戏在教育、发展与学习中的研究中心”（PEDAL），怀特布雷德、贝克、吉布森以及一支研究团队希望能就游戏在儿童发展过程中所扮演的角色提供证据。",
        "grammar": {
            "type": "thanks to 状语 + 过去分词定语",
            "note": "thanks to the university's new Centre... (PEDAL) 为原因状语；主干 Whitebread, Baker, Gibson and a team... hope to provide evidence on the role；played by play in how a child develops 为过去分词短语作 the role 的后置定语。"
        },
        "words": [
            {"w": "thanks to", "pos": "phr.", "def": "多亏；由于"},
            {"w": "role", "pos": "n.", "def": "作用；角色"}
        ]
    },
    # Para 7
    {
        "id": 19,
        "para": 7,
        "en": LSQUO + "A strong possibility is that play supports the early development of children" + RSQUO + "s self-control," + RSQUO + " explains Baker.",
        "zh": "“一种很大的可能性是，游戏有助于儿童自我控制能力的早期发展，”贝克解释道。",
        "grammar": {
            "type": "表语从句 + 引述倒装",
            "note": "引语主干 A strong possibility is that...，that 引导表语从句；explains Baker 为主谓倒装引述。"
        },
        "words": [
            {"w": "possibility", "pos": "n.", "def": "可能性"},
            {"w": "self-control", "pos": "n.", "def": "自我控制；自制力"}
        ]
    },
    {
        "id": 20,
        "para": 7,
        "en": LSQUO + "This is our ability to develop awareness of our own thinking processes " + DASH + " it influences how effectively we go about undertaking challenging activities." + RSQUO,
        "zh": "“这是指我们培养对自身思维过程之觉察的能力——它影响着我们着手完成有挑战性的活动时的效率。”",
        "grammar": {
            "type": "主系表 + 破折号 + 宾语从句",
            "note": "This is our ability to develop awareness...，to develop... 为不定式定语；破折号后 it influences how effectively we go about undertaking challenging activities，how effectively... 为宾语从句，go about doing 意为“着手做”。"
        },
        "words": [
            {"w": "awareness", "pos": "n.", "def": "意识；觉察"},
            {"w": "undertake", "pos": "v.", "def": "着手；从事；承担"}
        ]
    },
    {
        "id": 21,
        "para": 7,
        "en": "In a study carried out by Baker with toddlers and young pre-schoolers, she found that children with greater self-control solved problems more quickly when exploring an unfamiliar set-up requiring scientific reasoning.",
        "zh": "在贝克针对学步儿童和学龄前幼儿开展的一项研究中，她发现自控力更强的孩子在探索一个需要科学推理的陌生装置时，解决问题的速度更快。",
        "grammar": {
            "type": "过去分词定语 + 宾语从句 + 时间状语",
            "note": "carried out by Baker with... 为过去分词短语修饰 a study；主句 she found that...，that 引导宾语从句；when exploring an unfamiliar set-up 为省略式时间状语从句，requiring scientific reasoning 为现在分词定语修饰 set-up。"
        },
        "words": [
            {"w": "toddler", "pos": "n.", "def": "学步的幼儿"},
            {"w": "reasoning", "pos": "n.", "def": "推理；推论"}
        ]
    },
    {
        "id": 22,
        "para": 7,
        "en": LSQUO + "This sort of evidence makes us think that giving children the chance to play will make them more successful problem-solvers in the long run." + RSQUO,
        "zh": "“这类证据让我们认为，给孩子玩耍的机会，从长远来看会使他们成为更成功的问题解决者。”",
        "grammar": {
            "type": "使役动词 make + 宾语从句 + 动名词主语",
            "note": "主干 This sort of evidence makes us think that...，make sb do 结构；that 引导 think 的宾语从句，从句主语为动名词短语 giving children the chance to play，谓语 will make them more successful problem-solvers；in the long run 意为“从长远看”。"
        },
        "words": [
            {"w": "in the long run", "pos": "phr.", "def": "从长远来看；终究"},
            {"w": "problem-solver", "pos": "n.", "def": "解决问题的人"}
        ]
    },
    # Para 8
    {
        "id": 23,
        "para": 8,
        "en": "If playful experiences do facilitate this aspect of development, say the researchers, it could be extremely significant for educational practices, because the ability to self-regulate has been shown to be a key predictor of academic performance.",
        "zh": "研究人员表示，如果游戏体验确实能促进这方面的发展，那么它对教育实践可能意义重大，因为自我调节能力已被证明是学业表现的一个关键预测因素。",
        "grammar": {
            "type": "条件从句 + 插入引述 + 原因从句",
            "note": "If playful experiences do facilitate... 为条件状语从句，do 为强调；say the researchers 为插入引述（主谓倒装）；主句 it could be extremely significant...；because... has been shown to be a key predictor 为原因状语从句（被动+不定式）。"
        },
        "words": [
            {"w": "facilitate", "pos": "v.", "def": "促进；使便利"},
            {"w": "predictor", "pos": "n.", "def": "预测因素；预示物"}
        ]
    },
    {
        "id": 24,
        "para": 8,
        "en": "Gibson adds: " + LSQUO + "Playful behaviour is also an important indicator of healthy social and emotional development." + RSQUO,
        "zh": "吉布森补充道：“爱玩的行为也是社会性和情感健康发展的一个重要标志。”",
        "grammar": {
            "type": "冒号引语 + 主系表",
            "note": "Gibson adds 为引述；冒号后引语 Playful behaviour is also an important indicator of...，为主系表结构，of healthy social and emotional development 为 indicator 的后置定语。"
        },
        "words": [
            {"w": "indicator", "pos": "n.", "def": "标志；指标"},
            {"w": "emotional", "pos": "adj.", "def": "情感的；情绪的"}
        ]
    },
    {
        "id": 25,
        "para": 8,
        "en": LSQUO + "In my previous research, I investigated how observing children at play can give us important clues about their well-being and can even be useful in the diagnosis of neurodevelopmental disorders like autism." + RSQUO,
        "zh": "“在我此前的研究中，我探究了观察儿童玩耍如何能为我们提供关于其身心健康的重要线索，甚至有助于诊断像自闭症这样的神经发育障碍。”",
        "grammar": {
            "type": "宾语从句 + 动名词主语 + 并列谓语",
            "note": "主句 I investigated how...，how 引导宾语从句；从句主语为动名词短语 observing children at play，带两个并列谓语 can give us important clues... 与 can even be useful in the diagnosis of...；like autism 为举例。"
        },
        "words": [
            {"w": "clue", "pos": "n.", "def": "线索；提示"},
            {"w": "diagnosis", "pos": "n.", "def": "诊断"}
        ]
    },
    # Para 9
    {
        "id": 26,
        "para": 9,
        "en": "Whitebread" + RSQUO + "s recent research has involved developing a play-based approach to supporting children" + RSQUO + "s writing.",
        "zh": "怀特布雷德近期的研究涉及开发一种以游戏为基础、用于支持儿童写作的方法。",
        "grammar": {
            "type": "现在完成时 + 动名词宾语",
            "note": "主干 Whitebread's recent research has involved developing a play-based approach，involve doing 结构；to supporting children's writing 为介词短语作 approach 的后置定语，此处 to 为介词。"
        },
        "words": [
            {"w": "involve", "pos": "v.", "def": "涉及；包含"},
            {"w": "approach", "pos": "n.", "def": "方法；途径"}
        ]
    },
    {
        "id": 27,
        "para": 9,
        "en": LSQUO + "Many primary school children find writing difficult, but we showed in a previous study that a playful stimulus was far more effective than an instructional one." + RSQUO,
        "zh": "“许多小学生觉得写作困难，但我们在此前的一项研究中表明，富有游戏性的刺激远比说教式的刺激有效。”",
        "grammar": {
            "type": "but 转折 + 宾语从句 + 比较结构",
            "note": "前句 Many primary school children find writing difficult，find sth adj 复合宾语；but 后 we showed... that...，that 引导宾语从句；从句内 a playful stimulus was far more effective than an instructional one，far 修饰比较级，one 替代 stimulus。"
        },
        "words": [
            {"w": "stimulus", "pos": "n.", "def": "刺激（物）；促进因素"},
            {"w": "instructional", "pos": "adj.", "def": "教学的；说明的"}
        ]
    },
    {
        "id": 28,
        "para": 9,
        "en": "Children wrote longer and better-structured stories when they first played with dolls representing characters in the story.",
        "zh": "当孩子们先用代表故事角色的玩偶玩耍之后，他们写出的故事更长、结构也更好。",
        "grammar": {
            "type": "时间状语从句 + 现在分词定语",
            "note": "主句 Children wrote longer and better-structured stories；when they first played with dolls 为时间状语从句；representing characters in the story 为现在分词短语作 dolls 的后置定语。"
        },
        "words": [
            {"w": "represent", "pos": "v.", "def": "代表；表示"},
            {"w": "structured", "pos": "adj.", "def": "有组织的；结构化的"}
        ]
    },
    {
        "id": 29,
        "para": 9,
        "en": "In the latest study, children first created their story with Lego, with similar results.",
        "zh": "在最新的研究中，孩子们先用乐高积木构思他们的故事，也得到了相似的结果。",
        "grammar": {
            "type": "一般过去时 + with 复合结构",
            "note": "主干 children first created their story with Lego；with similar results 为 with 引导的独立结构作伴随状语，表“并伴随相似的结果”。"
        },
        "words": [
            {"w": "create", "pos": "v.", "def": "创造；构思"},
            {"w": "similar", "pos": "adj.", "def": "相似的；类似的"}
        ]
    },
    {
        "id": 30,
        "para": 9,
        "en": LSQUO + "Many teachers commented that they had always previously had children saying they didn" + RSQUO + "t know what to write about. With the Lego building, however, not a single child said this through the whole year of the project." + RSQUO,
        "zh": "“许多老师评论说，以前总有孩子说他们不知道该写什么。然而，在用乐高搭建的过程中，整整一年的项目里没有一个孩子这么说过。”",
        "grammar": {
            "type": "宾语从句 + have sb doing + 否定倒装",
            "note": "前句 teachers commented that they had always previously had children saying...，have sb doing 表“让/使某人一直在做”，saying 后又接宾语从句 they didn't know what to write about；后句 not a single child said this 中 not a single 起强调否定作用。"
        },
        "words": [
            {"w": "comment", "pos": "v.", "def": "评论；发表意见"},
            {"w": "previously", "pos": "adv.", "def": "先前；以前"}
        ]
    },
    # Para 10
    {
        "id": 31,
        "para": 10,
        "en": "Whitebread, who directs PEDAL, trained as a primary school teacher in the early 1970s, when, as he describes, " + LSQUO + "the teaching of young children was largely a quiet backwater, untroubled by any serious intellectual debate or controversy." + RSQUO,
        "zh": "执掌 PEDAL 的怀特布雷德在20世纪70年代初接受培训成为一名小学教师，用他的话说，那时“幼儿教学在很大程度上是一潭平静的死水，没有任何严肃的学术辩论或争议来搅动它”。",
        "grammar": {
            "type": "非限制性定语从句 + when 时间从句 + 过去分词状语",
            "note": "主干 Whitebread... trained as a primary school teacher in the early 1970s；who directs PEDAL 为非限制性定语从句；when... 引导时间状语从句修饰 the early 1970s；as he describes 为插入语；untroubled by any serious... debate 为过去分词短语作 backwater 的补充状语。"
        },
        "words": [
            {"w": "backwater", "pos": "n.", "def": "死水；停滞落后之处"},
            {"w": "controversy", "pos": "n.", "def": "争论；争议"}
        ]
    },
    {
        "id": 32,
        "para": 10,
        "en": "Now, the landscape is very different, with hotly debated topics such as school starting age.",
        "zh": "如今，情况已大不相同，诸如入学年龄之类的话题被激烈地讨论着。",
        "grammar": {
            "type": "主系表 + with 复合结构",
            "note": "主干 the landscape is very different；with hotly debated topics such as school starting age 为 with 引导的独立结构作伴随状语，hotly debated 为过去分词作定语修饰 topics。"
        },
        "words": [
            {"w": "landscape", "pos": "n.", "def": "局面；形势；全景"},
            {"w": "hotly", "pos": "adv.", "def": "激烈地；热烈地"}
        ]
    },
    {
        "id": 33,
        "para": 10,
        "en": LSQUO + "Somehow the importance of play has been lost in recent decades. It" + RSQUO + "s regarded as something trivial, or even as something negative that contrasts with " + LDQUO + "work" + RDQUO + ". Let" + RSQUO + "s not lose sight of its benefits, and the fundamental contributions it makes to human achievements in the arts, sciences and technology. Let" + RSQUO + "s make sure children have a rich diet of play experiences." + RSQUO,
        "zh": "“不知何故，近几十年来游戏的重要性被忽视了。它被视为无关紧要的东西，甚至被看作与‘工作’相对立的负面事物。让我们别忽视它的益处，别忽视它对人类在艺术、科学和技术上之成就所作的根本性贡献。让我们确保孩子们能拥有丰富多样的游戏体验。”",
        "grammar": {
            "type": "被动语态 + 定语从句 + 祈使句 Let's",
            "note": "It's regarded as something trivial, or even as something negative，regard as 的被动式，两个 as 短语并列；that contrasts with 'work' 为定语从句；后两句均为 Let's (not)... 祈使结构，(that) it makes 为省略关系词定语从句修饰 contributions。"
        },
        "words": [
            {"w": "trivial", "pos": "adj.", "def": "琐碎的；微不足道的"},
            {"w": "lose sight of", "pos": "phr.", "def": "忽视；忘记；看不见"}
        ]
    }
]

questions = [
    {
        "title": "Questions 1" + DASH + "8",
        "type": "note_completion",
        "instructions": [
            "Complete the notes below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 1" + DASH + "8 on your answer sheet.",
            "Children" + RSQUO + "s play"
        ],
        "items": [
            {"number": 1, "prompt": "Uses of children" + RSQUO + "s play: building a " + LSQUO + "magical kingdom" + RSQUO + " may help develop 1 ____", "answer": "creativity", "evidence_sentence": 3},
            {"number": 2, "prompt": "board games involve 2 ____ and turn-taking", "answer": "rules", "evidence_sentence": 6},
            {"number": 3, "prompt": "Recent changes affecting children" + RSQUO + "s play: populations of 3 ____ have grown", "answer": "cities", "evidence_sentence": 10},
            {"number": 4, "prompt": "opportunities for free play are limited due to fear of 4 ____", "answer": "traffic", "evidence_sentence": 12},
            {"number": 5, "prompt": "opportunities for free play are limited due to fear of 5 ____", "answer": "crime", "evidence_sentence": 12},
            {"number": 6, "prompt": "increased 6 ____ in schools", "answer": "competition", "evidence_sentence": 12},
            {"number": 7, "prompt": "International policies on children" + RSQUO + "s play: it is difficult to find 7 ____ to support new policies", "answer": "evidence", "evidence_sentence": 14},
            {"number": 8, "prompt": "research needs to study the impact of play on the rest of the child" + RSQUO + "s 8 ____", "answer": "life", "evidence_sentence": 17}
        ]
    },
    {
        "title": "Questions 9" + DASH + "13",
        "type": "true_false_notgiven",
        "instructions": [
            "Do the following statements agree with the information given in Reading Passage 1?",
            "In boxes 9" + DASH + "13 on your answer sheet, write",
            "TRUE if the statement agrees with the information",
            "FALSE if the statement contradicts the information",
            "NOT GIVEN if there is no information on this"
        ],
        "items": [
            {"number": 9, "prompt": "Children with good self-control are known to be likely to do well at school later on.", "answer": "TRUE", "evidence_sentence": 23},
            {"number": 10, "prompt": "The way a child plays may provide information about possible medical problems.", "answer": "TRUE", "evidence_sentence": 25},
            {"number": 11, "prompt": "Playing with dolls was found to benefit girls" + RSQUO + " writing more than boys" + RSQUO + " writing.", "answer": "NOT GIVEN", "evidence_sentence": 28},
            {"number": 12, "prompt": "Children had problems thinking up ideas when they first created the story with Lego.", "answer": "FALSE", "evidence_sentence": 30},
            {"number": 13, "prompt": "People nowadays regard children" + RSQUO + "s play as less significant than they did in the past.", "answer": "TRUE", "evidence_sentence": 33}
        ]
    }
]

phrases = [
    {"w": "children" + RSQUO + "s play", "pos": "n.", "def": "儿童游戏；孩子的玩耍"},
    {"w": "free play", "pos": "n.", "def": "自由游戏（不受成人指导的玩耍）"},
    {"w": "play-based learning", "pos": "n.", "def": "游戏式学习；以游戏为基础的学习"},
    {"w": "self-control", "pos": "n.", "def": "自我控制；自制力"},
    {"w": "self-regulate", "pos": "v.", "def": "自我调节"},
    {"w": "academic performance", "pos": "n.", "def": "学业表现；学业成绩"},
    {"w": "problem-solving", "pos": "adj.", "def": "解决问题的"},
    {"w": "neurodevelopmental disorder", "pos": "n.", "def": "神经发育障碍"},
    {"w": "primary school", "pos": "n.", "def": "小学"},
    {"w": "board game", "pos": "n.", "def": "棋盘游戏"}
]

data = {
    "id": "c14-test1-p1",
    "source": "剑桥雅思14 · Test 1 · Passage 1",
    "title": "THE IMPORTANCE OF CHILDREN" + RSQUO + "S PLAY",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c14-test1-p1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
