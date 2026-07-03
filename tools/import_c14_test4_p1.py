# -*- coding: utf-8 -*-
"""Generate data/passages/c14-test4-p1.json (The secret of staying young)."""
import json
import os

RSQUO = "’"
LSQUO = "‘"
DASH = "–"

sentences = [
    # Para 1
    {
        "id": 1,
        "para": 1,
        "en": "Pheidole dentata, a native ant of the south-eastern U.S., isn" + RSQUO + "t immortal.",
        "zh": "齿突大头蚁（Pheidole dentata）是美国东南部的一种本土蚂蚁，它并非长生不死。",
        "grammar": {
            "type": "同位语 + 主系表",
            "note": "主干 Pheidole dentata... isn't immortal；a native ant of the south-eastern U.S. 为 Pheidole dentata 的同位语；immortal 意为“不朽的、长生不死的”。"
        },
        "words": [
            {"w": "native", "pos": "adj.", "def": "本地的；原产的"},
            {"w": "immortal", "pos": "adj.", "def": "不朽的；长生不死的"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "But scientists have found that it doesn" + RSQUO + "t seem to show any signs of aging.",
        "zh": "但科学家们发现，它似乎并不表现出任何衰老的迹象。",
        "grammar": {
            "type": "宾语从句",
            "note": "主干 scientists have found that...；从句 it doesn't seem to show any signs of aging；show signs of 意为“显示出……的迹象”。"
        },
        "words": [
            {"w": "sign", "pos": "n.", "def": "迹象；征兆"},
            {"w": "aging", "pos": "n.", "def": "衰老；老化"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "Old worker ants can do everything just as well as the youngsters, and their brains appear just as sharp.",
        "zh": "年老的工蚁能把一切事情做得和年轻工蚁一样好，它们的大脑看起来也同样敏锐。",
        "grammar": {
            "type": "as...as 比较 + 并列句",
            "note": "两分句由 and 连接；前句 Old worker ants can do everything just as well as the youngsters，just as...as 表“和……一样”；后句 their brains appear just as sharp。"
        },
        "words": [
            {"w": "worker ant", "pos": "n.", "def": "工蚁"},
            {"w": "sharp", "pos": "adj.", "def": "敏锐的；灵敏的"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": LSQUO + "We get a picture that these ants really don" + RSQUO + "t decline," + RSQUO + " says Ysabel Giraldo, who studied the ants for her doctoral thesis at Boston University.",
        "zh": "“我们得到的印象是，这些蚂蚁确实不会衰退，”伊莎贝尔·吉拉尔多说，她曾在波士顿大学为其博士论文研究这些蚂蚁。",
        "grammar": {
            "type": "宾语从句 + 引述倒装 + 非限制性定语从句",
            "note": "引语 We get a picture that these ants really don't decline，that 引导同位语从句说明 picture；says Ysabel Giraldo 为主谓倒装引述；who studied the ants for her doctoral thesis... 为非限制性定语从句。"
        },
        "words": [
            {"w": "decline", "pos": "v.", "def": "衰退；下降"},
            {"w": "doctoral thesis", "pos": "n.", "def": "博士论文"}
        ]
    },
    # Para 2
    {
        "id": 5,
        "para": 2,
        "en": "Such age-defying feats are rare in the animal kingdom.",
        "zh": "这样违抗衰老的本领，在动物界中是罕见的。",
        "grammar": {
            "type": "主系表",
            "note": "主干 Such age-defying feats are rare in the animal kingdom；age-defying 为复合形容词“抗衰老的”，feat 意为“本领、壮举”。"
        },
        "words": [
            {"w": "age-defying", "pos": "adj.", "def": "抗衰老的；违抗年龄的"},
            {"w": "feat", "pos": "n.", "def": "本领；壮举"}
        ]
    },
    {
        "id": 6,
        "para": 2,
        "en": "Naked mole rats can live for almost 30 years and stay fit for nearly their entire lives. They can still reproduce even when old, and they never get cancer.",
        "zh": "裸鼹鼠可以活近30年，并且在几乎整个一生中都保持健康。它们即使年老也仍能繁殖，而且从不患癌症。",
        "grammar": {
            "type": "并列谓语 + when 让步",
            "note": "首句 Naked mole rats can live for almost 30 years and stay fit...，两并列谓语；后句 They can still reproduce even when old，even when old 为省略式让步状语（=even when they are old）。"
        },
        "words": [
            {"w": "naked mole rat", "pos": "n.", "def": "裸鼹鼠"},
            {"w": "reproduce", "pos": "v.", "def": "繁殖；生育"}
        ]
    },
    {
        "id": 7,
        "para": 2,
        "en": "But the vast majority of animals deteriorate with age just like people do.",
        "zh": "但绝大多数动物都会像人一样随着年龄增长而衰退。",
        "grammar": {
            "type": "just like 状语从句",
            "note": "主干 the vast majority of animals deteriorate with age；just like people do 为方式状语从句，do 替代 deteriorate with age。"
        },
        "words": [
            {"w": "deteriorate", "pos": "v.", "def": "恶化；衰退"},
            {"w": "the vast majority of", "pos": "phr.", "def": "绝大多数的"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "Like the naked mole rat, ants are social creatures that usually live in highly organised colonies.",
        "zh": "与裸鼹鼠一样，蚂蚁是群居生物，通常生活在高度有组织的群落中。",
        "grammar": {
            "type": "介词短语状语 + 定语从句",
            "note": "Like the naked mole rat 为介词短语作状语；主干 ants are social creatures；that usually live in highly organised colonies 为定语从句修饰 creatures。"
        },
        "words": [
            {"w": "social creature", "pos": "n.", "def": "群居生物；社会性生物"},
            {"w": "colony", "pos": "n.", "def": "群落；聚居地"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": LSQUO + "It" + RSQUO + "s this social complexity that makes P. dentata useful for studying aging in people," + RSQUO + " says Giraldo, now at the California Institute of Technology.",
        "zh": "“正是这种社会复杂性，使得齿突大头蚁对研究人类的衰老很有用，”如今在加州理工学院任职的吉拉尔多说。",
        "grammar": {
            "type": "强调句 It is...that... + 引述倒装",
            "note": "引语 It's this social complexity that makes P. dentata useful for... 为 It is...that... 强调结构，强调 this social complexity；says Giraldo 为引述倒装，now at the California Institute of Technology 为其身份补充。"
        },
        "words": [
            {"w": "complexity", "pos": "n.", "def": "复杂性"},
            {"w": "institute", "pos": "n.", "def": "研究所；学院"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "Humans are also highly social, a trait that has been connected to healthier aging.",
        "zh": "人类也是高度社会性的，而这一特征已被认为与更健康的衰老有关。",
        "grammar": {
            "type": "同位语 + 定语从句",
            "note": "主干 Humans are also highly social；a trait 为对前句的同位概括，that has been connected to healthier aging 为定语从句修饰 a trait（现在完成时被动）。"
        },
        "words": [
            {"w": "trait", "pos": "n.", "def": "特征；特性"},
            {"w": "be connected to", "pos": "phr.", "def": "与……有关联"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": "By contrast, most animal studies of aging use mice, worms or fruit flies, which all lead much more isolated lives.",
        "zh": "相比之下，大多数关于衰老的动物研究使用的是小鼠、蠕虫或果蝇，而这些动物过的都是孤立得多的生活。",
        "grammar": {
            "type": "对比状语 + 非限制性定语从句",
            "note": "By contrast 表对比；主干 most animal studies of aging use mice, worms or fruit flies；which all lead much more isolated lives 为非限制性定语从句修饰前述三种动物，much 修饰比较级 more isolated。"
        },
        "words": [
            {"w": "by contrast", "pos": "phr.", "def": "相比之下"},
            {"w": "isolated", "pos": "adj.", "def": "孤立的；隔绝的"}
        ]
    },
    # Para 3
    {
        "id": 12,
        "para": 3,
        "en": "In the lab, P. dentata worker ants typically live for around 140 days.",
        "zh": "在实验室里，齿突大头蚁的工蚁通常能活大约140天。",
        "grammar": {
            "type": "主谓 + 状语",
            "note": "主干 P. dentata worker ants typically live for around 140 days；In the lab 为地点状语；for around 140 days 为时间状语。"
        },
        "words": [
            {"w": "typically", "pos": "adv.", "def": "通常；一般"},
            {"w": "lab", "pos": "n.", "def": "实验室（laboratory 的缩写）"}
        ]
    },
    {
        "id": 13,
        "para": 3,
        "en": "Giraldo focused on ants at four age ranges: 20 to 22 days, 45 to 47 days, 95 to 97 days and 120 to 122 days.",
        "zh": "吉拉尔多聚焦于四个年龄段的蚂蚁：20至22天、45至47天、95至97天和120至122天。",
        "grammar": {
            "type": "focus on + 冒号列举",
            "note": "主干 Giraldo focused on ants at four age ranges；冒号后为四个并列的年龄区间，具体说明 four age ranges。"
        },
        "words": [
            {"w": "focus on", "pos": "phr.", "def": "聚焦于；集中于"},
            {"w": "range", "pos": "n.", "def": "范围；区间"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": "Unlike all previous studies, which only estimated how old the ants were, her work tracked the ants from the time the pupae became adults, so she knew their exact ages.",
        "zh": "与所有以往只是估算蚂蚁年龄的研究不同，她的研究从蛹变为成虫之时就开始追踪这些蚂蚁，因此她知道它们确切的年龄。",
        "grammar": {
            "type": "介词短语状语 + 非限制性定语从句 + so 结果",
            "note": "Unlike all previous studies 为介词短语作状语，which only estimated how old the ants were 为非限制性定语从句；主句 her work tracked the ants from the time (when) the pupae became adults；so she knew their exact ages 为结果分句。"
        },
        "words": [
            {"w": "estimate", "pos": "v.", "def": "估计；估算"},
            {"w": "pupae", "pos": "n.", "def": "蛹（pupa 的复数）"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "Then she put them through a range of tests.",
        "zh": "然后，她让它们接受了一系列测试。",
        "grammar": {
            "type": "put through 短语",
            "note": "主干 she put them through a range of tests；put sb/sth through 意为“使经历、让……接受”；a range of 意为“一系列”。"
        },
        "words": [
            {"w": "put through", "pos": "phr.", "def": "使经历；让……接受（考验）"},
            {"w": "a range of", "pos": "phr.", "def": "一系列；一批"}
        ]
    },
    # Para 4
    {
        "id": 16,
        "para": 4,
        "en": "Giraldo watched how well the ants took care of the young of the colony, recording how often each ant attended to, carried and fed them.",
        "zh": "吉拉尔多观察了这些蚂蚁照顾群落幼虫的情况，记录下每只蚂蚁照料、搬运和喂食它们的频率。",
        "grammar": {
            "type": "宾语从句 + 现在分词状语",
            "note": "主干 Giraldo watched how well the ants took care of the young，how well... 为宾语从句；recording how often each ant attended to, carried and fed them 为现在分词状语，how often... 为其宾语从句，含三个并列谓语。"
        },
        "words": [
            {"w": "take care of", "pos": "phr.", "def": "照顾；照料"},
            {"w": "attend to", "pos": "phr.", "def": "照料；处理"}
        ]
    },
    {
        "id": 17,
        "para": 4,
        "en": "She compared how well 20-day-old and 95-day-old ants followed the telltale scent that the insects usually leave to mark a trail to food.",
        "zh": "她比较了20天大和95天大的蚂蚁在多大程度上能循着这种揭示性气味前进——昆虫通常会留下这种气味来标记通往食物的路径。",
        "grammar": {
            "type": "宾语从句 + 定语从句 + 不定式目的",
            "note": "主干 She compared how well... ants followed the telltale scent，how well... 为宾语从句；that the insects usually leave 为定语从句修饰 scent；to mark a trail to food 为不定式目的状语。"
        },
        "words": [
            {"w": "telltale", "pos": "adj.", "def": "泄露真相的；揭示性的"},
            {"w": "scent", "pos": "n.", "def": "气味；香味"}
        ]
    },
    {
        "id": 18,
        "para": 4,
        "en": "She tested how ants responded to light and also measured how active they were by counting how often ants in a small dish walked across a line.",
        "zh": "她测试了蚂蚁对光的反应，还通过计算小碟中蚂蚁穿过一条线的频率来测量它们的活跃程度。",
        "grammar": {
            "type": "并列谓语 + 宾语从句 + by 方式状语",
            "note": "主语 She 带两并列谓语 tested how ants responded to light 与 measured how active they were，两个 how 引导宾语从句；by counting how often ants... walked across a line 为方式状语。"
        },
        "words": [
            {"w": "respond to", "pos": "phr.", "def": "对……作出反应"},
            {"w": "measure", "pos": "v.", "def": "测量；衡量"}
        ]
    },
    {
        "id": 19,
        "para": 4,
        "en": "And she experimented with how ants react to live prey: a tethered fruit fly.",
        "zh": "她还试验了蚂蚁如何对活猎物——一只被拴住的果蝇——作出反应。",
        "grammar": {
            "type": "宾语从句 + 冒号同位",
            "note": "主干 she experimented with how ants react to live prey，how... 为宾语从句；冒号后 a tethered fruit fly 为 live prey 的同位说明，tethered 意为“被拴住的”。"
        },
        "words": [
            {"w": "prey", "pos": "n.", "def": "猎物"},
            {"w": "tethered", "pos": "adj.", "def": "被拴住的"}
        ]
    },
    {
        "id": 20,
        "para": 4,
        "en": "Giraldo expected the older ants to perform poorly in all these tasks.",
        "zh": "吉拉尔多原本预期年老的蚂蚁在所有这些任务中都会表现不佳。",
        "grammar": {
            "type": "expect sb to do",
            "note": "主干 Giraldo expected the older ants to perform poorly，expect sb to do 结构；in all these tasks 为状语。"
        },
        "words": [
            {"w": "expect", "pos": "v.", "def": "预期；期望"},
            {"w": "perform", "pos": "v.", "def": "表现；执行"}
        ]
    },
    {
        "id": 21,
        "para": 4,
        "en": "But the elderly insects were all good caretakers and trail-followers" + DASH + "the 95-day-old ants could track the scent even longer than their younger counterparts.",
        "zh": "但这些年老的昆虫全都是出色的照料者和循迹者——95天大的蚂蚁甚至能比它们更年轻的同类追踪气味更久。",
        "grammar": {
            "type": "破折号补充 + 比较结构",
            "note": "主干 the elderly insects were all good caretakers and trail-followers；破折号后 the 95-day-old ants could track the scent even longer than their younger counterparts，even 修饰比较级 longer。"
        },
        "words": [
            {"w": "elderly", "pos": "adj.", "def": "年老的"},
            {"w": "caretaker", "pos": "n.", "def": "照料者；看护人"}
        ]
    },
    {
        "id": 22,
        "para": 4,
        "en": "They all responded to light well, and the older ants were more active.",
        "zh": "它们都对光反应良好，而且年老的蚂蚁更为活跃。",
        "grammar": {
            "type": "并列句",
            "note": "两分句由 and 连接：They all responded to light well 与 the older ants were more active。"
        },
        "words": [
            {"w": "active", "pos": "adj.", "def": "活跃的；活动的"},
            {"w": "respond", "pos": "v.", "def": "反应；回应"}
        ]
    },
    {
        "id": 23,
        "para": 4,
        "en": "And when it came to reacting to prey, the older ants attacked the poor fruit fly just as aggressively as the young ones did, flaring their mandibles or pulling at the fly" + RSQUO + "s legs.",
        "zh": "而在对猎物作出反应时，年老的蚂蚁攻击那只可怜的果蝇时和年轻蚂蚁一样凶猛，它们张开上颚，或拉扯果蝇的腿。",
        "grammar": {
            "type": "when 时间从句 + as...as 比较 + 现在分词状语",
            "note": "when it came to reacting to prey 为时间状语从句，when it comes to 意为“谈到、涉及”；主句 the older ants attacked the poor fruit fly just as aggressively as the young ones did；flaring their mandibles or pulling at the fly's legs 为现在分词状语。"
        },
        "words": [
            {"w": "aggressively", "pos": "adv.", "def": "凶猛地；有攻击性地"},
            {"w": "mandible", "pos": "n.", "def": "（昆虫的）上颚；下颌"}
        ]
    },
    # Para 5
    {
        "id": 24,
        "para": 5,
        "en": "Then Giraldo compared the brains of 20-day-old and 95-day-old ants, identifying any cells that were close to death.",
        "zh": "接着，吉拉尔多比较了20天大和95天大蚂蚁的大脑，找出任何濒临死亡的细胞。",
        "grammar": {
            "type": "现在分词状语 + 定语从句",
            "note": "主干 Giraldo compared the brains of...；identifying any cells 为现在分词状语，that were close to death 为定语从句修饰 cells。"
        },
        "words": [
            {"w": "identify", "pos": "v.", "def": "识别；找出"},
            {"w": "cell", "pos": "n.", "def": "细胞"}
        ]
    },
    {
        "id": 25,
        "para": 5,
        "en": "She saw no major differences with age, nor was there any difference in the location of the dying cells, showing that age didn" + RSQUO + "t seem to affect specific brain functions.",
        "zh": "她没有发现随年龄出现的重大差异，垂死细胞的位置也没有任何不同，这表明年龄似乎并不影响特定的脑功能。",
        "grammar": {
            "type": "nor 倒装 + 现在分词状语 + 宾语从句",
            "note": "前句 She saw no major differences with age；nor was there any difference... 为 nor 引起的部分倒装；showing that age didn't seem to affect specific brain functions 为现在分词状语，that... 为宾语从句。"
        },
        "words": [
            {"w": "location", "pos": "n.", "def": "位置；地点"},
            {"w": "affect", "pos": "v.", "def": "影响"}
        ]
    },
    {
        "id": 26,
        "para": 5,
        "en": "Ants and other insects have structures in their brains called mushroom bodies, which are important for processing information, learning and memory.",
        "zh": "蚂蚁和其他昆虫的大脑中有一种叫作蕈形体的结构，它对于处理信息、学习和记忆都很重要。",
        "grammar": {
            "type": "过去分词定语 + 非限制性定语从句",
            "note": "主干 Ants and other insects have structures in their brains；called mushroom bodies 为过去分词定语修饰 structures；which are important for processing information, learning and memory 为非限制性定语从句。"
        },
        "words": [
            {"w": "structure", "pos": "n.", "def": "结构"},
            {"w": "mushroom body", "pos": "n.", "def": "蕈形体（昆虫脑内结构）"}
        ]
    },
    {
        "id": 27,
        "para": 5,
        "en": "She also wanted to see if aging affects the density of synaptic complexes within these structures" + DASH + "regions where neurons come together.",
        "zh": "她还想弄清衰老是否会影响这些结构内突触复合体的密度——突触复合体即神经元汇聚的区域。",
        "grammar": {
            "type": "if 宾语从句 + 破折号同位 + where 定语从句",
            "note": "主干 She also wanted to see if...，if aging affects the density of synaptic complexes 为宾语从句；破折号后 regions where neurons come together 为 synaptic complexes 的同位解释，where... 为定语从句。"
        },
        "words": [
            {"w": "density", "pos": "n.", "def": "密度"},
            {"w": "neuron", "pos": "n.", "def": "神经元"}
        ]
    },
    {
        "id": 28,
        "para": 5,
        "en": "Again, the answer was no.",
        "zh": "答案同样是否定的。",
        "grammar": {
            "type": "主系表",
            "note": "极简单句，主干 the answer was no；Again 为衔接副词，指“再一次”。"
        },
        "words": [
            {"w": "answer", "pos": "n.", "def": "答案；回答"},
            {"w": "again", "pos": "adv.", "def": "再一次；又"}
        ]
    },
    {
        "id": 29,
        "para": 5,
        "en": "What was more, the old ants didn" + RSQUO + "t experience any drop in the levels of either serotonin or dopamine" + DASH + "brain chemicals whose decline often coincides with aging.",
        "zh": "更重要的是，年老的蚂蚁在血清素或多巴胺的水平上都没有出现任何下降——而这两种脑化学物质的减少往往与衰老同时发生。",
        "grammar": {
            "type": "either...or... + 破折号同位 + whose 定语从句",
            "note": "主干 the old ants didn't experience any drop in the levels of either serotonin or dopamine，either...or... 并列；破折号后 brain chemicals whose decline often coincides with aging 为同位语加 whose 定语从句；What was more 为插入语。"
        },
        "words": [
            {"w": "serotonin", "pos": "n.", "def": "血清素；5-羟色胺"},
            {"w": "coincide with", "pos": "phr.", "def": "与……同时发生；相符"}
        ]
    },
    {
        "id": 30,
        "para": 5,
        "en": "In humans, for example, a decrease in serotonin has been linked to Alzheimer" + RSQUO + "s disease.",
        "zh": "例如在人类身上，血清素的减少已被认为与阿尔茨海默病有关。",
        "grammar": {
            "type": "现在完成时被动",
            "note": "主干 a decrease in serotonin has been linked to Alzheimer's disease（现在完成时被动）；In humans, for example 为状语与举例。"
        },
        "words": [
            {"w": "decrease", "pos": "n.", "def": "减少；下降"},
            {"w": "be linked to", "pos": "phr.", "def": "与……相关联"}
        ]
    },
    # Para 6
    {
        "id": 31,
        "para": 6,
        "en": LSQUO + "This is the first time anyone has looked at both behavioral and neural changes in these ants so thoroughly," + RSQUO + " says Giraldo, who recently published the findings in the Proceedings of the Royal Society B.",
        "zh": "“这是第一次有人如此透彻地考察这些蚂蚁在行为和神经两方面的变化，”吉拉尔多说，她最近将研究结果发表在《皇家学会学报B辑》上。",
        "grammar": {
            "type": "the first time 从句 + 引述倒装 + 非限制性定语从句",
            "note": "引语 This is the first time anyone has looked at... so thoroughly，the first time 后接从句用现在完成时；says Giraldo 为引述倒装；who recently published the findings in... 为非限制性定语从句。"
        },
        "words": [
            {"w": "thoroughly", "pos": "adv.", "def": "彻底地；透彻地"},
            {"w": "neural", "pos": "adj.", "def": "神经的"}
        ]
    },
    {
        "id": 32,
        "para": 6,
        "en": "Scientists have looked at some similar aspects in bees, but the results of recent bee studies were mixed" + DASH + "some studies showed age-related declines, which biologists call senescence, and others didn" + RSQUO + "t.",
        "zh": "科学家们研究过蜜蜂身上一些类似的方面，但近期蜜蜂研究的结果并不一致——有些研究显示出与年龄相关的衰退，即生物学家所称的衰老，而另一些研究则没有。",
        "grammar": {
            "type": "but 转折 + 破折号解释 + 非限制性定语从句",
            "note": "前句 Scientists have looked at some similar aspects in bees；but the results... were mixed；破折号后解释：some studies showed age-related declines... and others didn't，which biologists call senescence 为非限制性定语从句。"
        },
        "words": [
            {"w": "mixed", "pos": "adj.", "def": "混杂的；不一致的"},
            {"w": "senescence", "pos": "n.", "def": "衰老；老化"}
        ]
    },
    {
        "id": 33,
        "para": 6,
        "en": LSQUO + "For now, the study raises more questions than it answers," + RSQUO + " Giraldo says, " + LSQUO + "including how P. dentata stays in such good shape." + RSQUO,
        "zh": "“就目前而言，这项研究引出的问题比它回答的还多，”吉拉尔多说，“包括齿突大头蚁是如何保持如此良好状态的。”",
        "grammar": {
            "type": "比较结构 + 宾语从句",
            "note": "引语 the study raises more questions than it answers，more...than... 比较；including how P. dentata stays in such good shape，how... 为介词宾语从句；stay in good shape 意为“保持良好状态”。"
        },
        "words": [
            {"w": "raise", "pos": "v.", "def": "引起；提出"},
            {"w": "in good shape", "pos": "phr.", "def": "状态良好；健康"}
        ]
    },
    # Para 7
    {
        "id": 34,
        "para": 7,
        "en": "Also, if the ants don" + RSQUO + "t deteriorate with age, why do they die at all?",
        "zh": "此外，如果这些蚂蚁不会随年龄衰退，那它们究竟为什么会死呢？",
        "grammar": {
            "type": "if 条件从句 + 疑问句",
            "note": "if the ants don't deteriorate with age 为条件状语从句；主句为疑问句 why do they die at all，at all 用于疑问强化语气。"
        },
        "words": [
            {"w": "deteriorate", "pos": "v.", "def": "恶化；衰退"},
            {"w": "at all", "pos": "phr.", "def": "究竟；到底（加强语气）"}
        ]
    },
    {
        "id": 35,
        "para": 7,
        "en": "Out in the wild, the ants probably don" + RSQUO + "t live for a full 140 days thanks to predators, disease and just being in an environment that" + RSQUO + "s much harsher than the comforts of the lab.",
        "zh": "在野外，由于捕食者、疾病，以及仅仅是身处一个远比实验室舒适条件严酷得多的环境，这些蚂蚁很可能活不满140天。",
        "grammar": {
            "type": "thanks to 状语 + 定语从句",
            "note": "主干 the ants probably don't live for a full 140 days；thanks to predators, disease and just being in an environment 为原因状语，thanks to 此处表“由于”；that's much harsher than the comforts of the lab 为定语从句修饰 environment。"
        },
        "words": [
            {"w": "predator", "pos": "n.", "def": "捕食者；天敌"},
            {"w": "harsh", "pos": "adj.", "def": "严酷的；恶劣的"}
        ]
    },
    {
        "id": 36,
        "para": 7,
        "en": LSQUO + "The lucky ants that do live into old age may suffer a steep decline just before dying," + RSQUO + " Giraldo says, but she can" + RSQUO + "t say for sure because her study wasn" + RSQUO + "t designed to follow an ant" + RSQUO + "s final moments.",
        "zh": "“那些有幸活到老年的蚂蚁，可能会在临死前急剧衰退，”吉拉尔多说，但她无法确定，因为她的研究并非为追踪一只蚂蚁生命的最后时刻而设计。",
        "grammar": {
            "type": "定语从句 + but 转折 + 原因从句",
            "note": "引语 The lucky ants that do live into old age may suffer a steep decline，that do live... 为定语从句，do 强调；but she can't say for sure 为转折；because her study wasn't designed to follow an ant's final moments 为原因状语从句。"
        },
        "words": [
            {"w": "steep", "pos": "adj.", "def": "急剧的；陡峭的"},
            {"w": "for sure", "pos": "phr.", "def": "确定地；肯定地"}
        ]
    },
    {
        "id": 37,
        "para": 7,
        "en": LSQUO + "It will be important to extend these findings to other species of social insects," + RSQUO + " says Gene E. Robinson, an entomologist at the University of Illinois at Urbana-Champaign.",
        "zh": "“把这些发现推广到其他社会性昆虫物种上将很重要，”伊利诺伊大学厄巴纳-香槟分校的昆虫学家吉恩·E·罗宾逊说。",
        "grammar": {
            "type": "形式主语 + 引述倒装 + 同位语",
            "note": "引语 It will be important to extend these findings to...，it 为形式主语；says Gene E. Robinson 为引述倒装；an entomologist at the University of Illinois... 为 Robinson 的同位语。"
        },
        "words": [
            {"w": "extend", "pos": "v.", "def": "扩展；推广"},
            {"w": "entomologist", "pos": "n.", "def": "昆虫学家"}
        ]
    },
    {
        "id": 38,
        "para": 7,
        "en": "This ant might be unique, or it might represent a broader pattern among other social bugs with possible clues to the science of aging in larger animals.",
        "zh": "这种蚂蚁或许是独特的，也可能代表了其他社会性昆虫中一种更普遍的模式，从而为研究更大动物的衰老科学提供可能的线索。",
        "grammar": {
            "type": "or 并列 + with 状语",
            "note": "两分句由 or 连接：This ant might be unique 与 it might represent a broader pattern among other social bugs；with possible clues to the science of aging in larger animals 为 with 引导的伴随状语。"
        },
        "words": [
            {"w": "unique", "pos": "adj.", "def": "独特的；独一无二的"},
            {"w": "clue", "pos": "n.", "def": "线索；提示"}
        ]
    },
    {
        "id": 39,
        "para": 7,
        "en": "Either way, it seems that for these ants, age really doesn" + RSQUO + "t matter.",
        "zh": "无论如何，看起来对这些蚂蚁而言，年龄确实无关紧要。",
        "grammar": {
            "type": "形式主语 + 宾语从句",
            "note": "主干 it seems that...，it 为形式主语；that for these ants, age really doesn't matter 为主语从句；Either way 意为“无论哪种情况”，matter 为不及物动词“要紧”。"
        },
        "words": [
            {"w": "either way", "pos": "phr.", "def": "无论哪种方式；不管怎样"},
            {"w": "matter", "pos": "v.", "def": "要紧；有关系"}
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
            "Write your answer in boxes 1" + DASH + "8 on your answer sheet.",
            "Ysabel Giraldo" + RSQUO + "s research"
        ],
        "items": [
            {"number": 1, "prompt": "Focused on a total of 1 ____ different age groups of ants, analysing", "answer": "four", "evidence_sentence": 13},
            {"number": 2, "prompt": "Behaviour: how well ants looked after their 2 ____", "answer": "young", "evidence_sentence": 16},
            {"number": 3, "prompt": "their ability to locate 3 ____ using a scent trail", "answer": "food", "evidence_sentence": 17},
            {"number": 4, "prompt": "the effect that 4 ____ had on them", "answer": "light", "evidence_sentence": 18},
            {"number": 5, "prompt": "how 5 ____ they attacked prey", "answer": "aggressively", "evidence_sentence": 23},
            {"number": 6, "prompt": "Brains: comparison between age and the 6 ____ of dying cells in the brains of ants", "answer": "location", "evidence_sentence": 25},
            {"number": 7, "prompt": "condition of synaptic complexes (areas in which 7 ____ meet) in the brain" + RSQUO + "s " + LSQUO + "mushroom bodies" + RSQUO, "answer": "neurons", "evidence_sentence": 27},
            {"number": 8, "prompt": "level of two 8 ____ in the brain associated with ageing", "answer": "chemicals", "evidence_sentence": 29}
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
            {"number": 9, "prompt": "Pheidole dentata ants are the only known animals which remain active for almost their whole lives.", "answer": "FALSE", "evidence_sentence": 6},
            {"number": 10, "prompt": "Ysabel Giraldo was the first person to study Pheidole dentata ants using precise data about the insects" + RSQUO + " ages.", "answer": "TRUE", "evidence_sentence": 14},
            {"number": 11, "prompt": "The ants in Giraldo" + RSQUO + "s experiments behaved as she had predicted that they would.", "answer": "FALSE", "evidence_sentence": 21},
            {"number": 12, "prompt": "The recent studies of bees used different methods of measuring age-related decline.", "answer": "NOT GIVEN", "evidence_sentence": 32},
            {"number": 13, "prompt": "Pheidole dentata ants kept in laboratory conditions tend to live longer lives.", "answer": "TRUE", "evidence_sentence": 35}
        ]
    }
]

phrases = [
    {"w": "aging", "pos": "n.", "def": "衰老；老化"},
    {"w": "worker ant", "pos": "n.", "def": "工蚁"},
    {"w": "naked mole rat", "pos": "n.", "def": "裸鼹鼠"},
    {"w": "social creature", "pos": "n.", "def": "群居生物；社会性生物"},
    {"w": "mushroom body", "pos": "n.", "def": "蕈形体（昆虫脑内结构）"},
    {"w": "synaptic complex", "pos": "n.", "def": "突触复合体"},
    {"w": "serotonin", "pos": "n.", "def": "血清素；5-羟色胺"},
    {"w": "dopamine", "pos": "n.", "def": "多巴胺"},
    {"w": "senescence", "pos": "n.", "def": "衰老；老化"},
    {"w": "in good shape", "pos": "phr.", "def": "状态良好；健康"}
]

data = {
    "id": "c14-test4-p1",
    "source": "剑桥雅思14 · Test 4 · Passage 1",
    "title": "The secret of staying young",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c14-test4-p1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
