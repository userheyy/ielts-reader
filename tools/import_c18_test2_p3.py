# -*- coding: utf-8 -*-
"""Generate data/passages/c18-test2-p3.json (An ideal city)."""
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
        "en": "The word " + LSQUO + "genius" + RSQUO + " is universally associated with the name of Leonardo da Vinci.",
        "zh": "“天才”一词在全世界都与列奥纳多·达·芬奇的名字联系在一起。",
        "grammar": {
            "type": "被动语态",
            "note": "主干是 The word " + LSQUO + "genius" + RSQUO + " is universally associated with the name of Leonardo da Vinci，为被动语态，be associated with 表“与……相关联”，universally 作状语。"
        },
        "words": [
            {"w": "genius", "pos": "n.", "def": "天才"},
            {"w": "be associated with", "pos": "phr.", "def": "与……相关联"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "A true Renaissance man, he embodied scientific spirit, artistic talent and humanist sensibilities.",
        "zh": "作为一个真正的文艺复兴式全才，他集科学精神、艺术天赋与人文情怀于一身。",
        "grammar": {
            "type": "名词短语作状语 + 主谓宾",
            "note": "A true Renaissance man 为名词短语作状语（表身份）；主干 he embodied scientific spirit, artistic talent and humanist sensibilities，三个宾语并列。"
        },
        "words": [
            {"w": "embody", "pos": "v.", "def": "体现；集中表现"},
            {"w": "humanist", "pos": "adj.", "def": "人文主义的"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "Five hundred years have passed since Leonardo died in his home at Château du Clos Lucé, outside Tours, France.",
        "zh": "自列奥纳多在法国图尔近郊的克洛·吕塞城堡的家中去世以来，已经过去了五百年。",
        "grammar": {
            "type": "现在完成时 + since 时间状语从句",
            "note": "主干是 Five hundred years have passed；since Leonardo died in his home... 为 since 引导的时间状语从句；outside Tours, France 为地点补充。"
        },
        "words": [
            {"w": "pass", "pos": "v.", "def": "（时间）流逝；经过"},
            {"w": "château", "pos": "n.", "def": "城堡；庄园（法语）"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "Yet far from fading into insignificance, his thinking has carried down the centuries and still surprises today.",
        "zh": "然而，他的思想非但没有淡入无足轻重的境地，反而穿越数个世纪流传下来，至今仍令人惊叹。",
        "grammar": {
            "type": "far from 状语 + 并列谓语",
            "note": "Yet far from fading into insignificance 为状语，far from doing 表“远非、非但不”；主干 his thinking has carried down the centuries and still surprises today，两个谓语并列。"
        },
        "words": [
            {"w": "fade", "pos": "v.", "def": "褪去；逐渐消失"},
            {"w": "insignificance", "pos": "n.", "def": "无足轻重；微不足道"}
        ]
    },
    # Paragraph 2
    {
        "id": 5,
        "para": 2,
        "en": "The Renaissance marked the transition from the 15th century to modernity and took place after the spread of the plague in the 14th century, which caused a global crisis resulting in some 200 million deaths across Europe and Asia.",
        "zh": "文艺复兴标志着从15世纪向现代的过渡，它发生在14世纪瘟疫蔓延之后——那场瘟疫引发了一场全球性危机，导致欧亚两洲约两亿人死亡。",
        "grammar": {
            "type": "并列谓语 + 非限定性定语从句 + 现在分词",
            "note": "主语 The Renaissance 带两个并列谓语 marked the transition... 和 took place after the spread of the plague；which caused a global crisis 为非限定性定语从句修饰 plague，resulting in some 200 million deaths 为现在分词作结果状语。"
        },
        "words": [
            {"w": "transition", "pos": "n.", "def": "过渡；转变"},
            {"w": "plague", "pos": "n.", "def": "瘟疫；鼠疫"}
        ]
    },
    {
        "id": 6,
        "para": 2,
        "en": "Today, the world is on the cusp of a climate crisis, which is predicted to cause widespread displacement, extinctions and death, if left unaddressed.",
        "zh": "如今，世界正处于一场气候危机的临界点，据预测，若不加以应对，这场危机将造成大规模的流离失所、物种灭绝和死亡。",
        "grammar": {
            "type": "非限定性定语从句 + if 省略条件状语",
            "note": "主干 the world is on the cusp of a climate crisis，on the cusp of 表“处于……的临界点”；which is predicted to cause... 为非限定性定语从句；if left unaddressed 为省略主语和 be 的条件状语从句（=if it is left unaddressed）。"
        },
        "words": [
            {"w": "displacement", "pos": "n.", "def": "流离失所；迁移"},
            {"w": "unaddressed", "pos": "adj.", "def": "未得到处理的"}
        ]
    },
    {
        "id": 7,
        "para": 2,
        "en": "Then, as now, radical solutions were called for to revolutionise the way people lived and safeguard humanity against catastrophe.",
        "zh": "当时和现在一样，人们呼吁采取激进的解决方案，以彻底变革人们的生活方式，并保护人类免遭灾难。",
        "grammar": {
            "type": "被动语态 + 不定式目的",
            "note": "主干是 radical solutions were called for，call for 的被动形式，表“被呼吁、被需要”；to revolutionise the way people lived and safeguard humanity against catastrophe 为不定式作目的状语，两个动词并列；Then, as now 为状语。"
        },
        "words": [
            {"w": "radical", "pos": "adj.", "def": "激进的；根本的"},
            {"w": "safeguard", "pos": "v.", "def": "保护；捍卫"}
        ]
    },
    # Paragraph 3
    {
        "id": 8,
        "para": 3,
        "en": "Around 1486 " + DASH + " after a pestilence that killed half the population in Milan, Italy " + DASH + " Leonardo turned his thoughts to urban planning problems.",
        "zh": "大约在1486年——在一场夺去意大利米兰一半人口的瘟疫之后——列奥纳多把思考转向了城市规划问题。",
        "grammar": {
            "type": "破折号插入 + 定语从句",
            "note": "主干是 Leonardo turned his thoughts to urban planning problems；破折号内 after a pestilence that killed half the population 为插入的时间状语，that killed half the population 为定语从句修饰 pestilence。"
        },
        "words": [
            {"w": "pestilence", "pos": "n.", "def": "瘟疫；传染病"},
            {"w": "urban planning", "pos": "phr.", "def": "城市规划"}
        ]
    },
    {
        "id": 9,
        "para": 3,
        "en": "Following a typical Renaissance trend, he began to work on an " + LSQUO + "ideal city" + RSQUO + " project, which " + DASH + " due to its excessive costs " + DASH + " would remain unfulfilled.",
        "zh": "顺应一种典型的文艺复兴潮流，他着手进行一个“理想之城”的项目，而这个项目——由于成本过于高昂——最终未能实现。",
        "grammar": {
            "type": "现在分词状语 + 非限定性定语从句 + 破折号插入",
            "note": "Following a typical Renaissance trend 为现在分词短语作状语；主干 he began to work on an " + LSQUO + "ideal city" + RSQUO + " project；which... would remain unfulfilled 为非限定性定语从句，破折号内 due to its excessive costs 为插入的原因状语。"
        },
        "words": [
            {"w": "excessive", "pos": "adj.", "def": "过度的；过高的"},
            {"w": "unfulfilled", "pos": "adj.", "def": "未实现的；未完成的"}
        ]
    },
    {
        "id": 10,
        "para": 3,
        "en": "Yet given that unsustainable urban models are a key cause of global climate change today, it" + RSQUO + "s only natural to wonder how Leonardo might have changed the shape of modern cities.",
        "zh": "然而，鉴于不可持续的城市模式是当今全球气候变化的一个关键原因，人们自然会好奇：列奥纳多本可能会如何改变现代城市的面貌。",
        "grammar": {
            "type": "given that 原因状语从句 + it 形式主语 + 宾语从句",
            "note": "Yet given that unsustainable urban models are a key cause... 为 given that 原因状语从句；主句 it" + RSQUO + "s only natural to wonder how...，it 为形式主语，how Leonardo might have changed the shape of modern cities 为宾语从句，might have done 表对过去的推测。"
        },
        "words": [
            {"w": "unsustainable", "pos": "adj.", "def": "不可持续的"},
            {"w": "wonder", "pos": "v.", "def": "想知道；好奇"}
        ]
    },
    # Paragraph 4
    {
        "id": 11,
        "para": 4,
        "en": "Although the Renaissance is renowned as an era of incredible progress in art and architecture, it is rarely noted that the 15th century also marked the birth of urbanism as a true academic discipline.",
        "zh": "尽管文艺复兴以艺术和建筑领域取得惊人进步的时代而著称，但人们很少注意到，15世纪也标志着城市规划学作为一门真正的学术学科的诞生。",
        "grammar": {
            "type": "although 让步从句 + it 形式主语 + 主语从句",
            "note": "Although the Renaissance is renowned as an era of... 为让步状语从句；主句 it is rarely noted that...，it 为形式主语，that the 15th century also marked the birth of urbanism... 为主语从句。"
        },
        "words": [
            {"w": "renowned", "pos": "adj.", "def": "著名的；有声望的"},
            {"w": "urbanism", "pos": "n.", "def": "城市规划学；城市生活方式"}
        ]
    },
    {
        "id": 12,
        "para": 4,
        "en": "The rigour and method behind the conscious conception of a city had been largely missing in Western thought until the moment when prominent Renaissance men pushed forward large-scale urban projects in Italy, such as the reconfiguration of the town of Pienza and the expansion of the city of Ferrara.",
        "zh": "在西方思想中，有意识地构想一座城市所需的严谨与方法在很大程度上一直是缺失的，直到文艺复兴时期一些杰出人物在意大利推动大规模的城市工程，如皮恩扎镇的重新规划和费拉拉城的扩建。",
        "grammar": {
            "type": "过去完成时 + until 时间状语从句 + 举例",
            "note": "主干 The rigour and method... had been largely missing in Western thought，为过去完成时；until the moment when prominent Renaissance men pushed forward large-scale urban projects 为 until 时间状语，when 引导定语从句修饰 moment；such as... 举例。"
        },
        "words": [
            {"w": "rigour", "pos": "n.", "def": "严谨；缜密"},
            {"w": "reconfiguration", "pos": "n.", "def": "重新配置；重新规划"}
        ]
    },
    {
        "id": 13,
        "para": 4,
        "en": "These works surely inspired Leonardo" + RSQUO + "s decision to rethink the design of medieval cities, with their winding and overcrowded streets and with houses piled against one another.",
        "zh": "这些工程无疑激发了列奥纳多重新思考中世纪城市设计的决心——那些城市街道蜿蜒曲折、拥挤不堪，房屋一栋紧挨一栋地堆叠在一起。",
        "grammar": {
            "type": "主谓宾 + 不定式定语 + with 复合结构",
            "note": "主干 These works surely inspired Leonardo" + RSQUO + "s decision；to rethink the design of medieval cities 为不定式作定语修饰 decision；with their winding and overcrowded streets and with houses piled against one another 为两个 with 复合结构，描述中世纪城市。"
        },
        "words": [
            {"w": "winding", "pos": "adj.", "def": "蜿蜒的；曲折的"},
            {"w": "pile", "pos": "v.", "def": "堆叠；堆积"}
        ]
    },
    # Paragraph 5
    {
        "id": 14,
        "para": 5,
        "en": "It is not easy to identify a coordinated vision of Leonardo" + RSQUO + "s ideal city because of his disordered way of working with notes and sketches.",
        "zh": "由于列奥纳多用笔记和草图工作的方式杂乱无章，要从中辨识出他理想之城的一套协调统一的构想并非易事。",
        "grammar": {
            "type": "it 形式主语 + because of 原因状语",
            "note": "主干 It is not easy to identify a coordinated vision...，it 为形式主语，to identify... 为真正主语；because of his disordered way of working with notes and sketches 为原因状语。"
        },
        "words": [
            {"w": "coordinated", "pos": "adj.", "def": "协调的；统一的"},
            {"w": "disordered", "pos": "adj.", "def": "杂乱的；无序的"}
        ]
    },
    {
        "id": 15,
        "para": 5,
        "en": "But from the largest collection of Leonardo" + RSQUO + "s papers ever assembled, a series of innovative thoughts can be reconstructed regarding the foundation of a new city along the Ticino River, which runs from Switzerland into Italy and is 248 kilometres long.",
        "zh": "但从有史以来汇集的规模最大的列奥纳多手稿中，可以重建出一系列关于沿提契诺河建造一座新城的创新构想——提契诺河自瑞士流入意大利，全长248公里。",
        "grammar": {
            "type": "被动语态 + 过去分词定语 + 非限定性定语从句",
            "note": "主干 a series of innovative thoughts can be reconstructed，为被动语态；from the largest collection of Leonardo" + RSQUO + "s papers ever assembled 为状语，ever assembled 为过去分词修饰 papers；which runs from Switzerland into Italy and is 248 kilometres long 为非限定性定语从句修饰 Ticino River。"
        },
        "words": [
            {"w": "innovative", "pos": "adj.", "def": "创新的"},
            {"w": "reconstruct", "pos": "v.", "def": "重建；重构"}
        ]
    },
    {
        "id": 16,
        "para": 5,
        "en": "He designed the city for the easy transport of goods and clean urban spaces, and he wanted a comfortable and spacious city, with well-ordered streets and architecture.",
        "zh": "他设计这座城市是为了便于货物运输和保持城市空间的洁净，他想要一座舒适而宽敞、街道和建筑井然有序的城市。",
        "grammar": {
            "type": "并列句 + with 复合结构",
            "note": "两个分句由 and 连接；前句 He designed the city for the easy transport of goods and clean urban spaces，for... 为目的状语；后句 he wanted a comfortable and spacious city，with well-ordered streets and architecture 为 with 复合结构。"
        },
        "words": [
            {"w": "spacious", "pos": "adj.", "def": "宽敞的"},
            {"w": "well-ordered", "pos": "adj.", "def": "井然有序的"}
        ]
    },
    {
        "id": 17,
        "para": 5,
        "en": "He recommended " + LSQUO + "high, strong walls" + RSQUO + ", with " + LSQUO + "towers and battlements of all necessary and pleasant beauty" + RSQUO + ".",
        "zh": "他建议修筑“高大坚固的城墙”，配以“兼具一切必要功能与赏心悦目之美的塔楼和城垛”。",
        "grammar": {
            "type": "主谓宾 + with 复合结构",
            "note": "主干是 He recommended " + LSQUO + "high, strong walls" + RSQUO + "；with " + LSQUO + "towers and battlements of all necessary and pleasant beauty" + RSQUO + " 为 with 复合结构作补充，of all necessary and pleasant beauty 修饰 towers and battlements。"
        },
        "words": [
            {"w": "battlement", "pos": "n.", "def": "城垛；雉堞"},
            {"w": "recommend", "pos": "v.", "def": "建议；推荐"}
        ]
    },
    # Paragraph 6
    {
        "id": 18,
        "para": 6,
        "en": "His plans for a modern and " + LSQUO + "rational" + RSQUO + " city were consistent with Renaissance ideals.",
        "zh": "他关于一座现代而“理性”的城市的规划，与文艺复兴的理想相一致。",
        "grammar": {
            "type": "主系表",
            "note": "主干是 His plans... were consistent with Renaissance ideals，be consistent with 表“与……一致”；for a modern and " + LSQUO + "rational" + RSQUO + " city 为介词短语修饰 plans。"
        },
        "words": [
            {"w": "rational", "pos": "adj.", "def": "理性的；合理的"},
            {"w": "be consistent with", "pos": "phr.", "def": "与……一致"}
        ]
    },
    {
        "id": 19,
        "para": 6,
        "en": "But, in keeping with his personality, Leonardo included several innovations in his urban design.",
        "zh": "但是，与他的个性相符，列奥纳多在城市设计中加入了几项创新。",
        "grammar": {
            "type": "主谓宾 + 插入状语",
            "note": "主干是 Leonardo included several innovations in his urban design；in keeping with his personality 为插入状语，in keeping with 表“与……相符”。"
        },
        "words": [
            {"w": "in keeping with", "pos": "phr.", "def": "与……一致；符合"},
            {"w": "innovation", "pos": "n.", "def": "创新；革新"}
        ]
    },
    {
        "id": 20,
        "para": 6,
        "en": "Leonardo wanted the city to be built on several levels, linked with vertical outdoor staircases.",
        "zh": "列奥纳多希望这座城市建在若干层面上，各层之间用垂直的室外楼梯相连。",
        "grammar": {
            "type": "want sth to be done + 过去分词状语",
            "note": "主干 Leonardo wanted the city to be built on several levels，want sth to be done 结构；linked with vertical outdoor staircases 为过去分词短语作状语，说明各层的连接方式。"
        },
        "words": [
            {"w": "level", "pos": "n.", "def": "层；层面"},
            {"w": "staircase", "pos": "n.", "def": "楼梯"}
        ]
    },
    {
        "id": 21,
        "para": 6,
        "en": "This design can be seen in some of today" + RSQUO + "s high-rise buildings but was unconventional at the time.",
        "zh": "这种设计在如今的一些高层建筑中可以见到，但在当时却是非同寻常的。",
        "grammar": {
            "type": "被动语态 + 转折并列",
            "note": "主语 This design 带两个由 but 连接的谓语：can be seen in some of today" + RSQUO + "s high-rise buildings（被动）和 was unconventional at the time。"
        },
        "words": [
            {"w": "high-rise", "pos": "adj.", "def": "高层的"},
            {"w": "unconventional", "pos": "adj.", "def": "非传统的；不落俗套的"}
        ]
    },
    {
        "id": 22,
        "para": 6,
        "en": "Indeed, this idea of taking full advantage of the interior spaces wasn" + RSQUO + "t implemented until the 1920s and 1930s, with the birth of the Modernist movement.",
        "zh": "事实上，这种充分利用内部空间的理念直到20世纪二三十年代、随着现代主义运动的兴起，才得以实现。",
        "grammar": {
            "type": "not...until... + with 复合结构",
            "note": "主干 this idea... wasn" + RSQUO + "t implemented until the 1920s and 1930s，not...until... 表“直到……才”；of taking full advantage of the interior spaces 为介词短语修饰 idea；with the birth of the Modernist movement 为 with 复合结构。"
        },
        "words": [
            {"w": "implement", "pos": "v.", "def": "实施；执行"},
            {"w": "take advantage of", "pos": "phr.", "def": "利用"}
        ]
    },
    # Paragraph 7
    {
        "id": 23,
        "para": 7,
        "en": "While in the upper layers of the city, people could walk undisturbed between elegant palaces and streets, the lower layer was the place for services, trade, transport and industry.",
        "zh": "在城市的上层，人们可以在雅致的宫殿和街道之间不受打扰地行走，而下层则是提供服务、进行贸易、运输和工业活动的地方。",
        "grammar": {
            "type": "while 对比状语从句",
            "note": "While in the upper layers of the city, people could walk undisturbed... 为 while 引导的对比状语从句，undisturbed 作状语；主句 the lower layer was the place for services, trade, transport and industry。"
        },
        "words": [
            {"w": "undisturbed", "pos": "adj.", "def": "不受打扰的"},
            {"w": "elegant", "pos": "adj.", "def": "雅致的；优美的"}
        ]
    },
    {
        "id": 24,
        "para": 7,
        "en": "But the true originality of Leonardo" + RSQUO + "s vision was its fusion of architecture and engineering.",
        "zh": "但列奥纳多这一构想真正的独创之处，在于它将建筑与工程融为一体。",
        "grammar": {
            "type": "主系表",
            "note": "主干是 the true originality of Leonardo" + RSQUO + "s vision was its fusion of architecture and engineering；fusion of A and B 表“A与B的融合”。"
        },
        "words": [
            {"w": "originality", "pos": "n.", "def": "独创性；新颖"},
            {"w": "fusion", "pos": "n.", "def": "融合；结合"}
        ]
    },
    {
        "id": 25,
        "para": 7,
        "en": "Leonardo designed extensive hydraulic plants to create artificial canals throughout the city.",
        "zh": "列奥纳多设计了大规模的水利设施，以在全城开凿人工运河。",
        "grammar": {
            "type": "主谓宾 + 不定式目的",
            "note": "主干是 Leonardo designed extensive hydraulic plants；to create artificial canals throughout the city 为不定式作目的状语。"
        },
        "words": [
            {"w": "hydraulic", "pos": "adj.", "def": "水力的；液压的"},
            {"w": "canal", "pos": "n.", "def": "运河；水道"}
        ]
    },
    {
        "id": 26,
        "para": 7,
        "en": "The canals, regulated by clocks and basins, were supposed to make it easier for boats to navigate inland.",
        "zh": "这些运河由水闸时钟和水池调节，本应使船只更容易向内陆航行。",
        "grammar": {
            "type": "过去分词插入定语 + it 形式宾语",
            "note": "主干 The canals... were supposed to make it easier for boats to navigate inland；regulated by clocks and basins 为过去分词短语作插入定语；make it easier for boats to navigate 中 it 为形式宾语，for boats to navigate 为真正宾语。"
        },
        "words": [
            {"w": "regulate", "pos": "v.", "def": "调节；控制"},
            {"w": "navigate", "pos": "v.", "def": "航行；导航"}
        ]
    },
    {
        "id": 27,
        "para": 7,
        "en": "Leonardo also thought that the width of the streets ought to match the average height of the adjacent houses: a rule still followed in many contemporary cities across Italy, to allow access to sun and reduce the risk of damage from earthquakes.",
        "zh": "列奥纳多还认为，街道的宽度应当与两旁房屋的平均高度相匹配：这一规则如今仍为意大利许多城市所遵循，其目的是让阳光能够照进来，并降低地震造成损害的风险。",
        "grammar": {
            "type": "宾语从句 + 冒号同位语 + 过去分词定语 + 不定式目的",
            "note": "主干 Leonardo also thought that...，that 引导宾语从句 the width of the streets ought to match the average height...；冒号后 a rule still followed in many contemporary cities 为同位语，followed 为过去分词修饰 rule；to allow access to sun and reduce the risk... 为不定式作目的状语。"
        },
        "words": [
            {"w": "adjacent", "pos": "adj.", "def": "邻近的；毗邻的"},
            {"w": "contemporary", "pos": "adj.", "def": "当代的；现代的"}
        ]
    },
    # Paragraph 8
    {
        "id": 28,
        "para": 8,
        "en": "Although some of these features existed in Roman cities, before Leonardo" + RSQUO + "s drawings there had never been a multi-level, compact modern city which was thoroughly technically conceived.",
        "zh": "尽管其中一些特征在古罗马城市中就已存在，但在列奥纳多的图纸问世之前，从未有过一座在技术上被彻底构想过的多层紧凑型现代城市。",
        "grammar": {
            "type": "although 让步从句 + 过去完成时 + 定语从句",
            "note": "Although some of these features existed in Roman cities 为让步从句；主句 before Leonardo" + RSQUO + "s drawings there had never been a multi-level, compact modern city，为过去完成时；which was thoroughly technically conceived 为定语从句修饰 city。"
        },
        "words": [
            {"w": "compact", "pos": "adj.", "def": "紧凑的；密实的"},
            {"w": "conceive", "pos": "v.", "def": "构想；设想"}
        ]
    },
    {
        "id": 29,
        "para": 8,
        "en": "Indeed, it wasn" + RSQUO + "t until the 19th century that some of his ideas were applied.",
        "zh": "事实上，直到19世纪，他的一些理念才得以应用。",
        "grammar": {
            "type": "not...until... 强调句",
            "note": "it wasn" + RSQUO + "t until the 19th century that some of his ideas were applied 为 not...until... 的强调句型，强调时间状语 until the 19th century。"
        },
        "words": [
            {"w": "apply", "pos": "v.", "def": "应用；运用"},
            {"w": "indeed", "pos": "adv.", "def": "确实；事实上"}
        ]
    },
    {
        "id": 30,
        "para": 8,
        "en": "For example, the subdivision of the city by function " + DASH + " with services and infrastructures located in the lower levels and wide and well-ventilated boulevards and walkways above for residents " + DASH + " is an idea that can be found in Georges-Eugène Haussmann" + RSQUO + "s renovation of Paris under Emperor Napoleon III between 1853 and 1870.",
        "zh": "例如，按功能对城市进行分区——把各种服务设施和基础设施设在下层，而把宽阔、通风良好的林荫大道和人行道设在上层供居民使用——这一理念可以在1853年至1870年间乔治-欧仁·奥斯曼于拿破仑三世治下对巴黎的改造中找到。",
        "grammar": {
            "type": "破折号插入 + 定语从句",
            "note": "主干 the subdivision of the city by function... is an idea；破折号内 with services and infrastructures located... and... boulevards and walkways above 为 with 复合结构作插入语；that can be found in Georges-Eugène Haussmann" + RSQUO + "s renovation of Paris 为定语从句修饰 idea。"
        },
        "words": [
            {"w": "subdivision", "pos": "n.", "def": "细分；分区"},
            {"w": "well-ventilated", "pos": "adj.", "def": "通风良好的"}
        ]
    },
    # Paragraph 9
    {
        "id": 31,
        "para": 9,
        "en": "Today, Leonardo" + RSQUO + "s ideas are not simply valid, they actually suggest a way forward for urban planning.",
        "zh": "如今，列奥纳多的理念不仅仅是有效的，它们实际上还为城市规划指明了一条前进的道路。",
        "grammar": {
            "type": "not simply... 递进并列",
            "note": "两个分句由逗号连接、语义递进；前句 Leonardo" + RSQUO + "s ideas are not simply valid，not simply 表“不仅仅”；后句 they actually suggest a way forward for urban planning。"
        },
        "words": [
            {"w": "valid", "pos": "adj.", "def": "有效的；站得住脚的"},
            {"w": "a way forward", "pos": "phr.", "def": "前进的道路；出路"}
        ]
    },
    {
        "id": 32,
        "para": 9,
        "en": "Many scholars think that the compact city, built upwards instead of outwards, integrated with nature (especially water systems), with efficient transport infrastructure, could help modern cities become more efficient and sustainable.",
        "zh": "许多学者认为，向上而非向外扩展、与自然（尤其是水系）相融合、并配备高效交通基础设施的紧凑型城市，能够帮助现代城市变得更加高效和可持续。",
        "grammar": {
            "type": "宾语从句 + 多重过去分词定语",
            "note": "主干 Many scholars think that...，that 引导宾语从句，从句主干 the compact city... could help modern cities become more efficient and sustainable；built upwards instead of outwards、integrated with nature 为过去分词短语作定语，with efficient transport infrastructure 为 with 结构，共同修饰 city。"
        },
        "words": [
            {"w": "integrate", "pos": "v.", "def": "使融合；整合"},
            {"w": "infrastructure", "pos": "n.", "def": "基础设施"}
        ]
    },
    {
        "id": 33,
        "para": 9,
        "en": "This is yet another reason why Leonardo was aligned so closely with modern urban planning and centuries ahead of his time.",
        "zh": "这正是列奥纳多与现代城市规划如此紧密契合、并领先于他所处时代数个世纪的又一个原因。",
        "grammar": {
            "type": "主系表 + 定语从句",
            "note": "主干是 This is yet another reason；why Leonardo was aligned so closely with modern urban planning and centuries ahead of his time 为定语从句修饰 reason，why 引导；ahead of his time 表“超越其时代”。"
        },
        "words": [
            {"w": "align", "pos": "v.", "def": "使一致；使契合"},
            {"w": "ahead of one" + RSQUO + "s time", "pos": "phr.", "def": "超越时代；领先于时代"}
        ]
    }
]

questions = [
    {
        "title": "Questions 27" + DASH + "33",
        "type": "true_false_notgiven",
        "instructions": [
            "Do the following statements agree with the information given in Reading Passage 3?",
            "In boxes 27" + DASH + "33 on your answer sheet, write",
            "TRUE if the statement agrees with the information",
            "FALSE if the statement contradicts the information",
            "NOT GIVEN if there is no information on this"
        ],
        "items": [
            {"number": 27, "prompt": "People first referred to Leonardo da Vinci as a genius 500 years ago.", "answer": "NOT GIVEN", "evidence_sentence": 1},
            {"number": 28, "prompt": "The current climate crisis is predicted to cause more deaths than the plague.", "answer": "NOT GIVEN", "evidence_sentence": 6},
            {"number": 29, "prompt": "Some of the challenges we face today can be compared to those of earlier times.", "answer": "TRUE", "evidence_sentence": 7},
            {"number": 30, "prompt": "Leonardo da Vinci" + RSQUO + "s " + LSQUO + "ideal city" + RSQUO + " was constructed in the 15th century.", "answer": "FALSE", "evidence_sentence": 9},
            {"number": 31, "prompt": "Poor town planning is a major contributor to climate change.", "answer": "TRUE", "evidence_sentence": 10},
            {"number": 32, "prompt": "In Renaissance times, local people fought against the changes to Pienza and Ferrara.", "answer": "NOT GIVEN", "evidence_sentence": 12},
            {"number": 33, "prompt": "Leonardo da Vinci kept a neat, organised record of his designs.", "answer": "FALSE", "evidence_sentence": 14}
        ]
    },
    {
        "title": "Questions 34" + DASH + "40",
        "type": "summary_completion",
        "instructions": [
            "Complete the summary below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 34" + DASH + "40 on your answer sheet.",
            "Leonardo da Vinci" + RSQUO + "s ideal city"
        ],
        "items": [
            {"number": 34, "prompt": "A collection of Leonardo da Vinci" + RSQUO + "s paperwork reveals his design of a new city beside the Ticino River. This was to provide better 34 ____ for trade and a less polluted environment.", "answer": "transport", "evidence_sentence": 16},
            {"number": 35, "prompt": "They included features that can be seen in some tower blocks today, such as 35 ____ on the exterior of a building.", "answer": "staircases", "evidence_sentence": 20},
            {"number": 36, "prompt": "His expertise in 36 ____ was evident in his plans for artificial canals within his ideal city.", "answer": "engineering", "evidence_sentence": 24},
            {"number": 37, "prompt": "The design of many cities in Italy today follows this 37 ____ .", "answer": "rule", "evidence_sentence": 27},
            {"number": 38, "prompt": "While some cities from 38 ____ times have aspects that can also be found in Leonardo" + RSQUO + "s designs, his ideas weren" + RSQUO + "t put into practice until long after his death.", "answer": "Roman", "evidence_sentence": 28},
            {"number": 39, "prompt": "39 ____ is one example of a city that was redesigned in the 19th century in the way that Leonardo had envisaged.", "answer": "Paris", "evidence_sentence": 30},
            {"number": 40, "prompt": "His ideas are also relevant to today" + RSQUO + "s world, where building 40 ____ no longer seems to be the best approach.", "answer": "outwards", "evidence_sentence": 32}
        ]
    }
]

phrases = [
    {"w": "Leonardo da Vinci", "pos": "n.", "def": "列奥纳多·达·芬奇"},
    {"w": "the Renaissance", "pos": "n.", "def": "文艺复兴"},
    {"w": "ideal city", "pos": "n.", "def": "理想之城"},
    {"w": "urban planning", "pos": "n.", "def": "城市规划"},
    {"w": "urbanism", "pos": "n.", "def": "城市规划学；城市主义"},
    {"w": "Ticino River", "pos": "n.", "def": "提契诺河"},
    {"w": "the Modernist movement", "pos": "n.", "def": "现代主义运动"},
    {"w": "hydraulic plant", "pos": "n.", "def": "水利设施；水力装置"},
    {"w": "compact city", "pos": "n.", "def": "紧凑型城市"},
    {"w": "ahead of one" + RSQUO + "s time", "pos": "phr.", "def": "超越时代；领先于时代"}
]

data = {
    "id": "c18-test2-p3",
    "source": "剑桥雅思18 · Test 2 · Passage 3",
    "title": "An ideal city",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "subtitle": "Leonardo da Vinci" + RSQUO + "s ideal city was centuries ahead of its time",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c18-test2-p3.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
