# -*- coding: utf-8 -*-
"""Generate data/passages/c18-test3-p3.json (The case for mixed-ability classes)."""
import json
import os

RSQUO = "’"
LSQUO = "‘"
DASH = "–"

sentences = [
    # Paragraph 1
    {
        "id": 1,
        "para": 1,
        "en": "Picture this scene.",
        "zh": "想象一下这样的场景。",
        "grammar": {
            "type": "祈使句",
            "note": "为祈使句 Picture this scene，picture 此处作动词，表“想象、设想”，用于引出下文描述。"
        },
        "words": [
            {"w": "picture", "pos": "v.", "def": "想象；设想"},
            {"w": "scene", "pos": "n.", "def": "场景；情景"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "It" + RSQUO + "s an English literature lesson in a UK school, and the teacher has just read an extract from Shakespeare" + RSQUO + "s Romeo and Juliet with a class of 15-year-olds.",
        "zh": "这是英国一所学校的英语文学课，老师刚刚给一个十五岁学生的班级朗读了莎士比亚《罗密欧与朱丽叶》中的一段选文。",
        "grammar": {
            "type": "并列句 + 现在完成时",
            "note": "前句 It" + RSQUO + "s an English literature lesson in a UK school 为主系表；后句 the teacher has just read an extract from Shakespeare" + RSQUO + "s Romeo and Juliet 为现在完成时；with a class of 15-year-olds 为伴随状语。"
        },
        "words": [
            {"w": "extract", "pos": "n.", "def": "节选；摘录"},
            {"w": "literature", "pos": "n.", "def": "文学"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "He" + RSQUO + "s given some of the students copies of No Fear Shakespeare, a kid-friendly translation of the original.",
        "zh": "他给部分学生发了《无惧莎士比亚》，这是原著的一种适合孩子阅读的译本。",
        "grammar": {
            "type": "现在完成时 + 双宾语 + 同位语",
            "note": "主干 He" + RSQUO + "s given some of the students copies of No Fear Shakespeare，为现在完成时双宾语结构；a kid-friendly translation of the original 为 No Fear Shakespeare 的同位语。"
        },
        "words": [
            {"w": "copy", "pos": "n.", "def": "（书籍的）一本；副本"},
            {"w": "kid-friendly", "pos": "adj.", "def": "适合儿童的"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "For three students, even these literacy demands are beyond them.",
        "zh": "对三名学生来说，即便是这些阅读要求也超出了他们的能力。",
        "grammar": {
            "type": "主系表 + 状语前置",
            "note": "主干是 even these literacy demands are beyond them，be beyond sb 表“超出某人能力”；For three students 为状语前置。"
        },
        "words": [
            {"w": "literacy", "pos": "n.", "def": "读写能力"},
            {"w": "demand", "pos": "n.", "def": "要求；需求"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "Another girl simply can" + RSQUO + "t focus and he gives her pens and paper to draw with.",
        "zh": "还有一个女孩就是无法集中注意力，于是他给了她纸笔用来画画。",
        "grammar": {
            "type": "并列句 + 不定式定语",
            "note": "两个分句由 and 连接；前句 Another girl simply can" + RSQUO + "t focus；后句 he gives her pens and paper to draw with，to draw with 为不定式作定语修饰 pens and paper。"
        },
        "words": [
            {"w": "focus", "pos": "v.", "def": "集中注意力"},
            {"w": "simply", "pos": "adv.", "def": "简直；就是"}
        ]
    },
    {
        "id": 6,
        "para": 1,
        "en": "The teacher can ask the No Fear group to identify the key characters and maybe provide a tentative plot summary.",
        "zh": "老师可以让阅读《无惧莎士比亚》的那组学生辨认主要人物，或许再让他们给出一个初步的情节梗概。",
        "grammar": {
            "type": "ask sb to do + 并列不定式",
            "note": "主干 The teacher can ask the No Fear group to identify the key characters and maybe provide a tentative plot summary，ask sb to do 结构，to identify... 和 (to) provide... 两个不定式并列。"
        },
        "words": [
            {"w": "identify", "pos": "v.", "def": "辨认；确认"},
            {"w": "tentative", "pos": "adj.", "def": "初步的；试探性的"}
        ]
    },
    {
        "id": 7,
        "para": 1,
        "en": "He can ask most of the class about character development, and five of them might be able to support their statements with textual evidence.",
        "zh": "他可以就人物塑造向班上大多数学生提问，而其中五名学生也许能用文本证据来支持他们的说法。",
        "grammar": {
            "type": "并列句",
            "note": "两个分句由 and 连接；前句 He can ask most of the class about character development；后句 five of them might be able to support their statements with textual evidence，support A with B 表“用B支持A”。"
        },
        "words": [
            {"w": "character development", "pos": "phr.", "def": "人物塑造；角色发展"},
            {"w": "textual", "pos": "adj.", "def": "文本的；原文的"}
        ]
    },
    {
        "id": 8,
        "para": 1,
        "en": "Now two curious students are wondering whether Shakespeare advocates living a life of moderation or one of passionate engagement.",
        "zh": "此时，两名充满好奇的学生正在思考：莎士比亚提倡的是过一种节制的生活，还是一种充满激情投入的生活。",
        "grammar": {
            "type": "现在进行时 + whether 宾语从句",
            "note": "主干 two curious students are wondering whether...，whether 引导宾语从句，advocate 后接动名词 living a life of moderation，or one of passionate engagement 中 one 指代 a life。"
        },
        "words": [
            {"w": "advocate", "pos": "v.", "def": "提倡；主张"},
            {"w": "moderation", "pos": "n.", "def": "节制；适度"}
        ]
    },
    # Paragraph 2
    {
        "id": 9,
        "para": 2,
        "en": "As a teacher myself, I" + RSQUO + "d think my lesson would be going rather well if the discussion went as described above.",
        "zh": "作为一名教师，如果课堂讨论能像上面所描述的那样进行，我会觉得我这堂课上得相当不错。",
        "grammar": {
            "type": "if 虚拟条件句 + 身份状语",
            "note": "As a teacher myself 为身份状语；主句 I" + RSQUO + "d think my lesson would be going rather well；if the discussion went as described above 为与现在事实相反的虚拟条件从句，as described above 为方式状语。"
        },
        "words": [
            {"w": "discussion", "pos": "n.", "def": "讨论"},
            {"w": "describe", "pos": "v.", "def": "描述"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "But wouldn" + RSQUO + "t this kind of class work better if there weren" + RSQUO + "t such a huge gap between the top and the bottom?",
        "zh": "但如果尖子生和差生之间没有如此巨大的差距，这样的课堂难道不会效果更好吗？",
        "grammar": {
            "type": "否定疑问 + if 虚拟条件句",
            "note": "主句 wouldn" + RSQUO + "t this kind of class work better 为否定疑问句；if there weren" + RSQUO + "t such a huge gap between the top and the bottom 为与现在事实相反的虚拟条件从句。"
        },
        "words": [
            {"w": "gap", "pos": "n.", "def": "差距；鸿沟"},
            {"w": "huge", "pos": "adj.", "def": "巨大的"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": "If we put all the kids who needed literacy support into one class, and all the students who want to discuss the virtue of moderation into another?",
        "zh": "如果我们把所有需要读写辅导的孩子分到一个班，把所有想讨论“节制之美德”的学生分到另一个班呢？",
        "grammar": {
            "type": "if 条件句（省略主句）+ 定语从句",
            "note": "为省略主句的 if 条件句，承接上句语气；who needed literacy support 与 who want to discuss the virtue of moderation 为定语从句分别修饰 kids 和 students；into one class... into another 表分班。"
        },
        "words": [
            {"w": "support", "pos": "n.", "def": "支持；辅导"},
            {"w": "virtue", "pos": "n.", "def": "美德；优点"}
        ]
    },
    # Paragraph 3
    {
        "id": 12,
        "para": 3,
        "en": "The practice of " + LSQUO + "streaming" + RSQUO + ", or " + LSQUO + "tracking" + RSQUO + ", involves separating students into classes depending on their diagnosed levels of attainment.",
        "zh": "所谓“分流”或“分轨”的做法，是指根据学生被评定的学业水平把他们分到不同的班级。",
        "grammar": {
            "type": "主谓宾 + 动名词宾语 + 状语",
            "note": "主干 The practice of " + LSQUO + "streaming" + RSQUO + ", or " + LSQUO + "tracking" + RSQUO + ", involves separating students into classes，involve 后接动名词 separating；depending on their diagnosed levels of attainment 为状语，表依据。"
        },
        "words": [
            {"w": "streaming", "pos": "n.", "def": "（按能力）分流；分班"},
            {"w": "attainment", "pos": "n.", "def": "学业成就；造诣"}
        ]
    },
    {
        "id": 13,
        "para": 3,
        "en": "At a macro level, it requires the establishment of academically selective schools for the brightest students, and comprehensive schools for the rest.",
        "zh": "在宏观层面上，它要求为最聪明的学生设立择优录取的学校，而为其余学生设立综合学校。",
        "grammar": {
            "type": "主谓宾 + 并列宾语",
            "note": "主干 it requires the establishment of academically selective schools... and comprehensive schools...，两个 schools 短语并列；At a macro level 为状语，for the brightest students / for the rest 分别说明对象。"
        },
        "words": [
            {"w": "selective", "pos": "adj.", "def": "择优的；选择性的"},
            {"w": "comprehensive school", "pos": "phr.", "def": "综合中学（不按成绩筛选）"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": "Within schools, it means selecting students into a " + LSQUO + "stream" + RSQUO + " of general ability, or " + LSQUO + "sets" + RSQUO + " of subject-specific ability.",
        "zh": "在学校内部，它意味着按综合能力把学生分入某个“流”，或按具体学科能力把他们分入若干“组”。",
        "grammar": {
            "type": "主谓宾 + 动名词宾语",
            "note": "主干 it means selecting students into a " + LSQUO + "stream" + RSQUO + "... or " + LSQUO + "sets" + RSQUO + "...，mean 后接动名词 selecting，两个介词短语 into a stream of general ability 与 (into) sets of subject-specific ability 并列；Within schools 为状语。"
        },
        "words": [
            {"w": "general ability", "pos": "phr.", "def": "综合能力；一般能力"},
            {"w": "subject-specific", "pos": "adj.", "def": "特定学科的"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "The practice is intuitively appealing to almost every stakeholder.",
        "zh": "这种做法对几乎每一个利益相关方来说，从直觉上都颇具吸引力。",
        "grammar": {
            "type": "主系表",
            "note": "主干是 The practice is intuitively appealing to almost every stakeholder；intuitively 作状语修饰 appealing，be appealing to 表“对……有吸引力”。"
        },
        "words": [
            {"w": "intuitively", "pos": "adv.", "def": "直觉地；凭直觉"},
            {"w": "stakeholder", "pos": "n.", "def": "利益相关者"}
        ]
    },
    # Paragraph 4
    {
        "id": 16,
        "para": 4,
        "en": "I have heard the mixed-ability model attacked by way of analogy: a group hike.",
        "zh": "我曾听人用一个类比来抨击混合能力（教学）模式：一次集体徒步。",
        "grammar": {
            "type": "have sth done + 冒号补充",
            "note": "主干 I have heard the mixed-ability model attacked，have sth done 表“听到某物被……”，attacked 为过去分词作宾补；by way of analogy 为方式状语；冒号后 a group hike 为对 analogy 的具体补充。"
        },
        "words": [
            {"w": "analogy", "pos": "n.", "def": "类比；比拟"},
            {"w": "hike", "pos": "n.", "def": "徒步；远足"}
        ]
    },
    {
        "id": 17,
        "para": 4,
        "en": "The fittest in the group take the lead and set a brisk pace, only to have to stop and wait every 20 minutes.",
        "zh": "队伍中体力最好的人一马当先、步伐轻快，结果却每隔20分钟就不得不停下来等待。",
        "grammar": {
            "type": "并列谓语 + only to 结果状语",
            "note": "主干 The fittest in the group take the lead and set a brisk pace，两个谓语并列，The fittest 为“the+形容词”指一类人；only to have to stop and wait 为 only to do 结构，表出乎意料的结果。"
        },
        "words": [
            {"w": "take the lead", "pos": "phr.", "def": "带头；领先"},
            {"w": "brisk", "pos": "adj.", "def": "轻快的；敏捷的"}
        ]
    },
    {
        "id": 18,
        "para": 4,
        "en": "This is frustrating, and their enthusiasm wanes.",
        "zh": "这令人沮丧，于是他们的热情逐渐消退。",
        "grammar": {
            "type": "并列句",
            "note": "两个分句由 and 连接；前句 This is frustrating 为主系表；后句 their enthusiasm wanes，wane 表“减弱、衰退”。"
        },
        "words": [
            {"w": "enthusiasm", "pos": "n.", "def": "热情；热忱"},
            {"w": "wane", "pos": "v.", "def": "减弱；衰退"}
        ]
    },
    {
        "id": 19,
        "para": 4,
        "en": "Meanwhile, the slowest ones are not only embarrassed but physically struggling to keep up.",
        "zh": "与此同时，走得最慢的人不仅感到难堪，而且在体力上也难以跟上。",
        "grammar": {
            "type": "not only...but... 并列",
            "note": "主干 the slowest ones are not only embarrassed but physically struggling to keep up，not only...but... 连接两个表语成分；Meanwhile 为状语；keep up 表“跟上”。"
        },
        "words": [
            {"w": "embarrassed", "pos": "adj.", "def": "尴尬的；难堪的"},
            {"w": "struggle", "pos": "v.", "def": "挣扎；艰难地做"}
        ]
    },
    {
        "id": 20,
        "para": 4,
        "en": "What" + RSQUO + "s worse, they never get a long enough break.",
        "zh": "更糟的是，他们从来得不到足够长的休息。",
        "grammar": {
            "type": "主谓宾 + 评注插入",
            "note": "What" + RSQUO + "s worse 为评注性插入语，表“更糟的是”；主句 they never get a long enough break，enough 后置修饰 long。"
        },
        "words": [
            {"w": "break", "pos": "n.", "def": "休息；间歇"},
            {"w": "what" + RSQUO + "s worse", "pos": "phr.", "def": "更糟的是"}
        ]
    },
    {
        "id": 21,
        "para": 4,
        "en": "They honestly just want to quit. Hiking, they feel, is not for them.",
        "zh": "老实说，他们只想放弃。他们觉得徒步不适合自己。",
        "grammar": {
            "type": "主谓宾 + 插入语",
            "note": "第一句 They honestly just want to quit 为简单句；第二句 Hiking is not for them，they feel 为插入的评述语，be not for sb 表“不适合某人”。"
        },
        "words": [
            {"w": "quit", "pos": "v.", "def": "放弃；退出"},
            {"w": "honestly", "pos": "adv.", "def": "老实说；坦白讲"}
        ]
    },
    # Paragraph 5
    {
        "id": 22,
        "para": 5,
        "en": "Mixed-ability classes bore students, frustrate parents and burn out teachers.",
        "zh": "混合能力班级让学生厌烦、让家长沮丧、让老师精疲力竭。",
        "grammar": {
            "type": "主谓 + 并列宾语",
            "note": "主语 Mixed-ability classes 带三个并列谓语：bore students、frustrate parents、burn out teachers，burn out 表“使精疲力竭”。"
        },
        "words": [
            {"w": "bore", "pos": "v.", "def": "使厌烦"},
            {"w": "burn out", "pos": "phr.", "def": "使精疲力竭；使耗尽精力"}
        ]
    },
    {
        "id": 23,
        "para": 5,
        "en": "The brightest ones will never summit Mount Qomolangma, and the stragglers won" + RSQUO + "t enjoy the lovely stroll in the park they are perhaps more suited to.",
        "zh": "最聪明的人永远登不上珠穆朗玛峰，而掉队的人也享受不到他们或许更适合的、在公园里惬意的漫步。",
        "grammar": {
            "type": "并列句 + 省略关系词定语从句",
            "note": "两个分句由 and 连接；前句 The brightest ones will never summit Mount Qomolangma；后句 the stragglers won" + RSQUO + "t enjoy the lovely stroll in the park，they are perhaps more suited to 为省略关系词的定语从句修饰 stroll。"
        },
        "words": [
            {"w": "straggler", "pos": "n.", "def": "掉队者；落伍者"},
            {"w": "stroll", "pos": "n.", "def": "漫步；散步"}
        ]
    },
    {
        "id": 24,
        "para": 5,
        "en": "Individuals suffer at the demands of the collective, mediocrity prevails.",
        "zh": "个体在集体的要求之下受苦，平庸之风盛行。",
        "grammar": {
            "type": "并列分句",
            "note": "两个分句由逗号连接：Individuals suffer at the demands of the collective 和 mediocrity prevails，prevail 表“盛行、占上风”。"
        },
        "words": [
            {"w": "collective", "pos": "n.", "def": "集体"},
            {"w": "mediocrity", "pos": "n.", "def": "平庸；平庸之辈"}
        ]
    },
    {
        "id": 25,
        "para": 5,
        "en": "So: is learning like hiking?",
        "zh": "那么：学习真的像徒步吗？",
        "grammar": {
            "type": "一般疑问句",
            "note": "So: 引出反问，is learning like hiking 为一般疑问句，用于承上启下、引发思考。"
        },
        "words": [
            {"w": "learning", "pos": "n.", "def": "学习"},
            {"w": "like", "pos": "prep.", "def": "像；如同"}
        ]
    },
    # Paragraph 6
    {
        "id": 26,
        "para": 6,
        "en": "The current pedagogical paradigm is arguably that of constructivism, which emerged out of the work of psychologist Lev Vygotsky.",
        "zh": "当前的教学范式可以说是建构主义，它源于心理学家列夫·维果茨基的研究。",
        "grammar": {
            "type": "主系表 + 非限定性定语从句",
            "note": "主干 The current pedagogical paradigm is... that of constructivism，that 指代 paradigm，arguably 为状语；which emerged out of the work of psychologist Lev Vygotsky 为非限定性定语从句修饰 constructivism。"
        },
        "words": [
            {"w": "pedagogical", "pos": "adj.", "def": "教学的；教育学的"},
            {"w": "constructivism", "pos": "n.", "def": "建构主义"}
        ]
    },
    {
        "id": 27,
        "para": 6,
        "en": "In the 1930s, Vygotsky emphasised the importance of targeting a student" + RSQUO + "s specific " + LSQUO + "zone of proximal development" + RSQUO + " (ZPD).",
        "zh": "20世纪30年代，维果茨基强调了针对学生特定的“最近发展区”（ZPD）的重要性。",
        "grammar": {
            "type": "主谓宾 + 动名词宾语",
            "note": "主干 Vygotsky emphasised the importance of targeting a student" + RSQUO + "s specific " + LSQUO + "zone of proximal development" + RSQUO + "，of 后接动名词 targeting；In the 1930s 为时间状语。"
        },
        "words": [
            {"w": "emphasise", "pos": "v.", "def": "强调"},
            {"w": "zone of proximal development", "pos": "phr.", "def": "最近发展区（ZPD）"}
        ]
    },
    {
        "id": 28,
        "para": 6,
        "en": "This is the gap between what they can achieve only with support " + DASH + " teachers, textbooks, worked examples, parents and so on " + DASH + " and what they can achieve independently.",
        "zh": "这就是学生只有在支持之下（教师、教科书、例题、家长等等）所能达到的水平，与他们独立所能达到的水平之间的差距。",
        "grammar": {
            "type": "主系表 + between...and... + 破折号插入",
            "note": "主干 This is the gap between what they can achieve only with support and what they can achieve independently，between A and B 结构，两个 what 引导宾语从句；破折号内 teachers, textbooks... 为对 support 的举例插入。"
        },
        "words": [
            {"w": "worked example", "pos": "phr.", "def": "例题；解题示范"},
            {"w": "independently", "pos": "adv.", "def": "独立地"}
        ]
    },
    {
        "id": 29,
        "para": 6,
        "en": "The purpose of teaching is to provide and then gradually remove this " + LSQUO + "scaffolding" + RSQUO + " until they are autonomous.",
        "zh": "教学的目的在于提供、然后逐步撤除这种“脚手架”，直到学生能够自主学习。",
        "grammar": {
            "type": "主系表 + 不定式表语 + until 状语从句",
            "note": "主干 The purpose of teaching is to provide and then gradually remove this " + LSQUO + "scaffolding" + RSQUO + "，两个不定式动词 provide 和 remove 并列作表语；until they are autonomous 为时间状语从句。"
        },
        "words": [
            {"w": "scaffolding", "pos": "n.", "def": "脚手架；（教学中的）支持支架"},
            {"w": "autonomous", "pos": "adj.", "def": "自主的；独立自主的"}
        ]
    },
    {
        "id": 30,
        "para": 6,
        "en": "If we accept this model, it follows that streaming students with similar ZPDs would be an efficient and effective solution.",
        "zh": "如果我们接受这一模式，那么随之而来的结论就是：把最近发展区相近的学生分到一起将是一种高效而有效的解决办法。",
        "grammar": {
            "type": "if 条件从句 + it follows that 主语从句",
            "note": "If we accept this model 为条件状语从句；主句 it follows that...，it follows that 表“由此得出”，that streaming students with similar ZPDs would be an efficient and effective solution 为主语从句。"
        },
        "words": [
            {"w": "efficient", "pos": "adj.", "def": "高效的"},
            {"w": "it follows that", "pos": "phr.", "def": "由此可见；随之得出"}
        ]
    },
    {
        "id": 31,
        "para": 6,
        "en": "And that forcing everyone on the same hike " + DASH + " regardless of aptitude " + DASH + " would be madness.",
        "zh": "而且，不顾资质差异强迫所有人走同一条徒步路线，将会是一种疯狂之举。",
        "grammar": {
            "type": "省略主句的主语从句 + 破折号插入",
            "note": "承接上句 it follows，本句 that forcing everyone on the same hike... would be madness 为并列的主语从句，forcing everyone on the same hike 为动名词短语；破折号内 regardless of aptitude 为让步插入语。"
        },
        "words": [
            {"w": "regardless of", "pos": "phr.", "def": "不管；不顾"},
            {"w": "aptitude", "pos": "n.", "def": "天资；才能"}
        ]
    },
    # Paragraph 7
    {
        "id": 32,
        "para": 7,
        "en": "Despite all this, there is limited empirical evidence to suggest that streaming results in better outcomes for students.",
        "zh": "尽管有这一切（理论），能够表明分流会给学生带来更好结果的实证证据却很有限。",
        "grammar": {
            "type": "让步状语 + there be + 不定式定语 + 宾语从句",
            "note": "Despite all this 为让步状语；主干 there is limited empirical evidence；to suggest that streaming results in better outcomes 为不定式作定语修饰 evidence，that 引导宾语从句，result in 表“导致”。"
        },
        "words": [
            {"w": "empirical", "pos": "adj.", "def": "实证的；经验的"},
            {"w": "outcome", "pos": "n.", "def": "结果；成效"}
        ]
    },
    {
        "id": 33,
        "para": 7,
        "en": "Professor John Hattie, director of the Melbourne Education Research Institute, notes that " + LSQUO + "tracking has minimal effects on learning outcomes" + RSQUO + ".",
        "zh": "墨尔本教育研究所所长约翰·哈蒂教授指出，“分轨对学习成效的影响微乎其微”。",
        "grammar": {
            "type": "同位语 + 宾语从句",
            "note": "主干 Professor John Hattie... notes that...，director of the Melbourne Education Research Institute 为同位语；that 引导宾语从句 tracking has minimal effects on learning outcomes。"
        },
        "words": [
            {"w": "minimal", "pos": "adj.", "def": "极小的；最低限度的"},
            {"w": "effect", "pos": "n.", "def": "影响；效果"}
        ]
    },
    {
        "id": 34,
        "para": 7,
        "en": "What is more, streaming appears to significantly " + DASH + " and negatively " + DASH + " affect those students assigned to the lowest sets.",
        "zh": "更重要的是，分流似乎会对那些被分到最低组别的学生产生显著的——而且是负面的——影响。",
        "grammar": {
            "type": "评注插入 + 破折号插入 + 过去分词定语",
            "note": "What is more 为评注插入语；主干 streaming appears to significantly... affect those students，破折号内 and negatively 为插入的补充；assigned to the lowest sets 为过去分词短语修饰 students。"
        },
        "words": [
            {"w": "significantly", "pos": "adv.", "def": "显著地"},
            {"w": "assign", "pos": "v.", "def": "分配；分派"}
        ]
    },
    {
        "id": 35,
        "para": 7,
        "en": "These students tend to have much higher representation of low socioeconomic class.",
        "zh": "这些学生中来自低社会经济阶层的比例往往要高得多。",
        "grammar": {
            "type": "主谓宾",
            "note": "主干 These students tend to have much higher representation of low socioeconomic class，tend to do 表“往往”，much 修饰比较级 higher，representation 此处表“占比、代表比例”。"
        },
        "words": [
            {"w": "representation", "pos": "n.", "def": "（占的）比例；代表"},
            {"w": "socioeconomic", "pos": "adj.", "def": "社会经济的"}
        ]
    },
    {
        "id": 36,
        "para": 7,
        "en": "Less significant is the small benefit for those lucky clever students in the higher sets.",
        "zh": "而处于较高组别的那些幸运聪明的学生所获得的微小益处，则没那么显著。",
        "grammar": {
            "type": "表语前置倒装",
            "note": "本句为表语前置引起的倒装，正常语序为 The small benefit for those lucky clever students in the higher sets is less significant，Less significant 提前以强调对比。"
        },
        "words": [
            {"w": "benefit", "pos": "n.", "def": "益处；好处"},
            {"w": "clever", "pos": "adj.", "def": "聪明的"}
        ]
    },
    {
        "id": 37,
        "para": 7,
        "en": "The overall result is that the smart stay smart and the dumb get dumber, further entrenching the social divide.",
        "zh": "总的结果是聪明的人依旧聪明，愚笨的人愈发愚笨，从而进一步固化了社会分化。",
        "grammar": {
            "type": "表语从句 + 现在分词结果状语",
            "note": "主干 The overall result is that...，that 引导表语从句，含并列 the smart stay smart and the dumb get dumber（the+形容词 表一类人）；further entrenching the social divide 为现在分词作结果状语。"
        },
        "words": [
            {"w": "entrench", "pos": "v.", "def": "使根深蒂固；巩固"},
            {"w": "divide", "pos": "n.", "def": "分歧；分化"}
        ]
    },
    # Paragraph 8
    {
        "id": 38,
        "para": 8,
        "en": "In the latest update of Hattie" + RSQUO + "s influential meta-analysis of factors influencing student achievement, one of the most significant factors is the teachers" + RSQUO + " estimate of achievement.",
        "zh": "在哈蒂那项颇具影响力的、关于影响学生成绩之因素的元分析的最新更新中，最重要的因素之一是教师对（学生）成绩的预估。",
        "grammar": {
            "type": "现在分词定语 + 主系表",
            "note": "主干 one of the most significant factors is the teachers" + RSQUO + " estimate of achievement；In the latest update of Hattie" + RSQUO + "s influential meta-analysis 为状语，influencing student achievement 为现在分词修饰 factors。"
        },
        "words": [
            {"w": "meta-analysis", "pos": "n.", "def": "元分析；荟萃分析"},
            {"w": "estimate", "pos": "n.", "def": "估计；预估"}
        ]
    },
    {
        "id": 39,
        "para": 8,
        "en": "Streaming students by diagnosed achievement automatically limits what the teacher feels the student is capable of.",
        "zh": "按评定的成绩对学生进行分流，会自动限制教师对该学生能力的判断。",
        "grammar": {
            "type": "动名词主语 + 宾语从句",
            "note": "主语 Streaming students by diagnosed achievement 为动名词短语；谓语 automatically limits，宾语 what the teacher feels the student is capable of 为宾语从句，be capable of 表“有能力做”。"
        },
        "words": [
            {"w": "automatically", "pos": "adv.", "def": "自动地；必然地"},
            {"w": "be capable of", "pos": "phr.", "def": "能够；有能力"}
        ]
    },
    {
        "id": 40,
        "para": 8,
        "en": "Meanwhile, in a mixed environment, teachers" + RSQUO + " estimates need to be more diverse and flexible.",
        "zh": "与此同时，在混合的环境中，教师的预估需要更加多样和灵活。",
        "grammar": {
            "type": "主系表",
            "note": "主干 teachers" + RSQUO + " estimates need to be more diverse and flexible；Meanwhile 与 in a mixed environment 为状语。"
        },
        "words": [
            {"w": "diverse", "pos": "adj.", "def": "多样的；多种多样的"},
            {"w": "flexible", "pos": "adj.", "def": "灵活的"}
        ]
    },
    # Paragraph 9 (peer learning + conclusion)
    {
        "id": 41,
        "para": 9,
        "en": "While streaming might seem to help teachers effectively target a student" + RSQUO + "s ZPD, it can underestimate the importance of peer-to-peer learning.",
        "zh": "尽管分流看似能帮助教师有效地针对学生的最近发展区，它却可能低估了同伴之间相互学习的重要性。",
        "grammar": {
            "type": "while 让步状语从句 + 主句",
            "note": "While streaming might seem to help teachers effectively target a student" + RSQUO + "s ZPD 为让步状语从句；主句 it can underestimate the importance of peer-to-peer learning。"
        },
        "words": [
            {"w": "underestimate", "pos": "v.", "def": "低估"},
            {"w": "peer-to-peer", "pos": "adj.", "def": "同伴之间的；点对点的"}
        ]
    },
    {
        "id": 42,
        "para": 9,
        "en": "A crucial aspect of constructivist theory is the role of the MKO " + DASH + " " + LSQUO + "more-knowledgeable other" + RSQUO + " " + DASH + " in knowledge construction.",
        "zh": "建构主义理论的一个关键方面，是“知识更丰富者”（MKO）在知识建构中所扮演的角色。",
        "grammar": {
            "type": "主系表 + 破折号同位语",
            "note": "主干 A crucial aspect of constructivist theory is the role of the MKO... in knowledge construction；破折号内 " + LSQUO + "more-knowledgeable other" + RSQUO + " 为 MKO 的同位解释。"
        },
        "words": [
            {"w": "crucial", "pos": "adj.", "def": "关键的；至关重要的"},
            {"w": "more-knowledgeable other", "pos": "phr.", "def": "知识更丰富者（MKO）"}
        ]
    },
    {
        "id": 43,
        "para": 9,
        "en": "While teachers are traditionally the MKOs in classrooms, the value of knowledgeable student peers must not go unrecognised either.",
        "zh": "尽管传统上教师是课堂中的“知识更丰富者”，但见多识广的同学同伴的价值也决不应被忽视。",
        "grammar": {
            "type": "while 让步状语从句 + 主句",
            "note": "While teachers are traditionally the MKOs in classrooms 为让步状语从句；主句 the value of knowledgeable student peers must not go unrecognised either，go unrecognised 表“不被认可”，either 用于否定句表“也”。"
        },
        "words": [
            {"w": "peer", "pos": "n.", "def": "同龄人；同伴"},
            {"w": "unrecognised", "pos": "adj.", "def": "未被认可的；被忽视的"}
        ]
    },
    {
        "id": 44,
        "para": 9,
        "en": "I find it amazing to watch students get over an idea to their peers in ways that I would never think of.",
        "zh": "我觉得，看着学生用我永远想不到的方式把一个概念讲给同伴听，实在令人惊叹。",
        "grammar": {
            "type": "it 形式宾语 + 定语从句",
            "note": "主干 I find it amazing to watch students get over an idea to their peers，it 为形式宾语，to watch... 为真正宾语，watch sb do 结构，get over 此处表“讲清楚、使理解”；that I would never think of 为定语从句修饰 ways。"
        },
        "words": [
            {"w": "get over", "pos": "phr.", "def": "把（意思）讲清楚；使被理解"},
            {"w": "amazing", "pos": "adj.", "def": "令人惊叹的"}
        ]
    },
    {
        "id": 45,
        "para": 9,
        "en": "They operate with different language tools and different social tools from teachers and, having just learnt it themselves, they possess similar cognitive structures to their struggling classmates.",
        "zh": "他们运用着与教师不同的语言工具和社交工具，而且由于自己也刚刚学会，他们与那些学得吃力的同学拥有相似的认知结构。",
        "grammar": {
            "type": "并列句 + 现在分词状语",
            "note": "前半 They operate with different language tools and different social tools from teachers；后半 they possess similar cognitive structures to their struggling classmates，having just learnt it themselves 为现在分词短语作原因状语。"
        },
        "words": [
            {"w": "cognitive", "pos": "adj.", "def": "认知的"},
            {"w": "possess", "pos": "v.", "def": "拥有；具有"}
        ]
    },
    {
        "id": 46,
        "para": 9,
        "en": "There is also something exciting about passing on skills and knowledge that you yourself have just mastered " + DASH + " a certain pride and zeal, a certain freshness to the interaction between " + LSQUO + "teacher" + RSQUO + " and " + LSQUO + "learner" + RSQUO + " that is often lost by the expert for whom the steps are obvious and the joy of discovery forgotten.",
        "zh": "把自己刚刚掌握的技能和知识传授出去，也有某种令人兴奋之处——一种别样的自豪与热忱，一种“教者”与“学者”互动中的别样新鲜感，而这种新鲜感在那些觉得步骤显而易见、早已忘却发现之乐的专家身上往往已经消失。",
        "grammar": {
            "type": "there be + 定语从句 + 破折号同位语 + 定语从句",
            "note": "主干 There is also something exciting about passing on skills and knowledge，that you yourself have just mastered 为定语从句修饰 skills and knowledge；破折号后 a certain pride and zeal, a certain freshness... 为 something 的同位补充，that is often lost by the expert 为定语从句，for whom the steps are obvious 为介词提前定语从句。"
        },
        "words": [
            {"w": "zeal", "pos": "n.", "def": "热情；热忱"},
            {"w": "master", "pos": "v.", "def": "掌握；精通"}
        ]
    },
    {
        "id": 47,
        "para": 9,
        "en": "Having a variety of different abilities in a collaborative learning environment provides valuable resources for helping students meet their learning needs, not to mention improving their communication and social skills.",
        "zh": "在协作学习的环境中拥有各种不同的能力，为帮助学生满足其学习需求提供了宝贵的资源，更不用说还能提升他们的沟通与社交能力了。",
        "grammar": {
            "type": "动名词主语 + not to mention 状语",
            "note": "主语 Having a variety of different abilities in a collaborative learning environment 为动名词短语；谓语 provides valuable resources for helping students meet their learning needs；not to mention improving their communication and social skills 为插入状语，表“更不用说”。"
        },
        "words": [
            {"w": "collaborative", "pos": "adj.", "def": "协作的；合作的"},
            {"w": "not to mention", "pos": "phr.", "def": "更不用说"}
        ]
    },
    {
        "id": 48,
        "para": 9,
        "en": "And today, more than ever, we need the many to flourish " + DASH + " not suffer at the expense of a few bright stars.",
        "zh": "而如今，我们比以往任何时候都更需要让大多数人蓬勃发展——而不是为了少数几颗璀璨的明星而牺牲他们。",
        "grammar": {
            "type": "主谓宾 + 破折号对比",
            "note": "主干 we need the many to flourish，the many 指“大多数人”，need sth to do 结构；破折号后 not suffer at the expense of a few bright stars 与 flourish 对比，at the expense of 表“以……为代价”。"
        },
        "words": [
            {"w": "flourish", "pos": "v.", "def": "繁荣；蓬勃发展"},
            {"w": "at the expense of", "pos": "phr.", "def": "以……为代价"}
        ]
    },
    {
        "id": 49,
        "para": 9,
        "en": "Once a year, I go on a hike with my class, a mixed bunch of students.",
        "zh": "每年一次，我都会和我的班级——一群能力各异的学生——一起去徒步。",
        "grammar": {
            "type": "主谓 + 同位语",
            "note": "主干 I go on a hike with my class；Once a year 为频率状语；a mixed bunch of students 为 my class 的同位语。"
        },
        "words": [
            {"w": "bunch", "pos": "n.", "def": "一群；一伙"},
            {"w": "mixed", "pos": "adj.", "def": "混合的；各异的"}
        ]
    },
    {
        "id": 50,
        "para": 9,
        "en": "It is challenging. The fittest students realise they need to encourage the reluctant.",
        "zh": "这很有挑战性。体力最好的学生会意识到，他们需要去鼓励那些不情愿的同学。",
        "grammar": {
            "type": "主系表 + 宾语从句",
            "note": "第一句 It is challenging 为主系表（It 斜体表强调）；第二句 The fittest students realise they need to encourage the reluctant，realise 后接省略 that 的宾语从句，the reluctant 为“the+形容词”表一类人。"
        },
        "words": [
            {"w": "challenging", "pos": "adj.", "def": "有挑战性的"},
            {"w": "reluctant", "pos": "adj.", "def": "不情愿的；勉强的"}
        ]
    },
    {
        "id": 51,
        "para": 9,
        "en": "There are lookouts who report back, and extra items to carry for others. We make it " + DASH + " together.",
        "zh": "有负责瞭望、回来报告情况的人，也有要替别人多背的物品。我们最终做到了——一起做到的。",
        "grammar": {
            "type": "there be + 定语从句 + 破折号强调",
            "note": "前句 There are lookouts who report back, and extra items to carry for others，who report back 为定语从句，to carry for others 为不定式定语；后句 We make it together，破折号后 together 起强调作用，make it 表“成功、做到”。"
        },
        "words": [
            {"w": "lookout", "pos": "n.", "def": "瞭望者；放哨的人"},
            {"w": "make it", "pos": "phr.", "def": "成功；做到"}
        ]
    }
]

questions = [
    {
        "title": "Questions 27" + DASH + "30",
        "type": "multiple_choice",
        "instructions": [
            "Choose the correct letter, A, B, C or D.",
            "Write the correct letter in boxes 27" + DASH + "30 on your answer sheet."
        ],
        "items": [
            {"number": 27, "prompt": "The writer describes the Romeo and Juliet lesson in order to demonstrate A how few students are interested in literature. B how a teacher handles a range of learning needs. C how unsuitable Shakespeare is for most teenagers. D how weaker students can disrupt their classmates" + RSQUO + " learning.", "answer": "B", "evidence_sentence": 4},
            {"number": 28, "prompt": "What does the writer say about streaming in the third paragraph? A It has a very broad appeal. B It favours cleverer students. C It is relatively simple to implement. D It works better in some schools than others.", "answer": "A", "evidence_sentence": 15},
            {"number": 29, "prompt": "What idea is suggested by the reference to Mount Qomolangma in the fifth paragraph? A students following unsuitable paths B students attempting interesting tasks C students not achieving their full potential D students not being aware of their limitations", "answer": "C", "evidence_sentence": 23},
            {"number": 30, "prompt": "What does the word " + LSQUO + "scaffolding" + RSQUO + " in the sixth paragraph refer to? A the factors which prevent a student from learning effectively B the environment where most of a student" + RSQUO + "s learning takes place C the assistance given to a student in their initial stages of learning D the setting of appropriate learning targets for a student" + RSQUO + "s aptitude", "answer": "C", "evidence_sentence": 29}
        ]
    },
    {
        "title": "Questions 31" + DASH + "35",
        "type": "summary_completion",
        "instructions": [
            "Complete the summary using the list of phrases, A" + DASH + "I, below.",
            "Write the correct letter, A" + DASH + "I, in boxes 31" + DASH + "35 on your answer sheet.",
            "Is streaming effective?",
            "A wrong classes",
            "B lower expectations",
            "C average learners",
            "D bottom sets",
            "E brightest pupils",
            "F disadvantaged backgrounds",
            "G weaker students",
            "H higher achievements",
            "I positive impressions"
        ],
        "items": [
            {"number": 31, "prompt": "According to Professor John Hattie of the Melbourne Education Research Institute, there is very little indication that streaming leads to 31 ____ .", "answer": "H", "evidence_sentence": 33},
            {"number": 32, "prompt": "He points out that, in schools which use streaming, the most significant impact is on those students placed in the 32 ____ , ...", "answer": "D", "evidence_sentence": 34},
            {"number": 33, "prompt": "... especially where a large proportion of them have 33 ____ .", "answer": "F", "evidence_sentence": 35},
            {"number": 34, "prompt": "Meanwhile, for the 34 ____ , there appears to be only minimal advantage.", "answer": "E", "evidence_sentence": 36},
            {"number": 35, "prompt": "A further issue is that teachers tend to have 35 ____ of students in streamed groups.", "answer": "B", "evidence_sentence": 39}
        ]
    },
    {
        "title": "Questions 36" + DASH + "40",
        "type": "yes_no_notgiven",
        "instructions": [
            "Do the following statements agree with the views of the writer in Reading Passage 3?",
            "In boxes 36" + DASH + "40 on your answer sheet, write",
            "YES if the statement agrees with the views of the writer",
            "NO if the statement contradicts the views of the writer",
            "NOT GIVEN if it is impossible to say what the writer thinks about this"
        ],
        "items": [
            {"number": 36, "prompt": "The Vygotsky model of education supports the concept of a mixed-ability class.", "answer": "NO", "evidence_sentence": 30},
            {"number": 37, "prompt": "Some teachers are uncertain about allowing students to take on MKO roles in the classroom.", "answer": "NOT GIVEN", "evidence_sentence": 43},
            {"number": 38, "prompt": "It can be rewarding to teach knowledge which you have only recently acquired.", "answer": "YES", "evidence_sentence": 46},
            {"number": 39, "prompt": "The priority should be to ensure that the highest-achieving students attain their goals.", "answer": "NO", "evidence_sentence": 48},
            {"number": 40, "prompt": "Taking part in collaborative outdoor activities with teachers and classmates can improve student outcomes in the classroom.", "answer": "NOT GIVEN", "evidence_sentence": 49}
        ]
    }
]

phrases = [
    {"w": "mixed-ability class", "pos": "n.", "def": "混合能力班级（学生能力参差）"},
    {"w": "streaming / tracking", "pos": "n.", "def": "（按能力）分流/分轨"},
    {"w": "No Fear Shakespeare", "pos": "n.", "def": "《无惧莎士比亚》（莎剧现代英语对照读本）"},
    {"w": "constructivism", "pos": "n.", "def": "建构主义"},
    {"w": "zone of proximal development (ZPD)", "pos": "n.", "def": "最近发展区"},
    {"w": "scaffolding", "pos": "n.", "def": "（教学）支架；脚手架"},
    {"w": "more-knowledgeable other (MKO)", "pos": "n.", "def": "知识更丰富者"},
    {"w": "peer-to-peer learning", "pos": "n.", "def": "同伴互学"},
    {"w": "meta-analysis", "pos": "n.", "def": "元分析；荟萃分析"},
    {"w": "Mount Qomolangma", "pos": "n.", "def": "珠穆朗玛峰"}
]

data = {
    "id": "c18-test3-p3",
    "source": "剑桥雅思18 · Test 3 · Passage 3",
    "title": "The case for mixed-ability classes",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c18-test3-p3.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
