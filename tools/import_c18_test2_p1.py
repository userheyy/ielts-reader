# -*- coding: utf-8 -*-
"""Generate data/passages/c18-test2-p1.json (Stonehenge)."""
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
        "en": "For centuries, historians and archaeologists have puzzled over the many mysteries of Stonehenge, a prehistoric monument that took an estimated 1,500 years to erect.",
        "zh": "数个世纪以来，历史学家和考古学家一直对巨石阵的诸多谜团百思不得其解——这座史前遗迹据估计花了1,500年才建成。",
        "grammar": {
            "type": "现在完成时 + 同位语 + 定语从句",
            "note": "主干是 historians and archaeologists have puzzled over the many mysteries of Stonehenge，puzzle over 表“苦思”；a prehistoric monument 为 Stonehenge 的同位语，that took an estimated 1,500 years to erect 为定语从句修饰 monument。"
        },
        "words": [
            {"w": "archaeologist", "pos": "n.", "def": "考古学家"},
            {"w": "erect", "pos": "v.", "def": "建造；竖立"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "Located on Salisbury Plain in southern England, it is comprised of roughly 100 massive upright stones placed in a circular layout.",
        "zh": "它位于英格兰南部的索尔兹伯里平原，由大约100块巨大的竖立石块按环形排列而成。",
        "grammar": {
            "type": "过去分词状语 + 被动语态 + 过去分词定语",
            "note": "Located on Salisbury Plain in southern England 为过去分词短语作状语；主干 it is comprised of roughly 100 massive upright stones，be comprised of 表“由……组成”；placed in a circular layout 为过去分词修饰 stones。"
        },
        "words": [
            {"w": "be comprised of", "pos": "phr.", "def": "由……组成"},
            {"w": "upright", "pos": "adj.", "def": "竖直的；直立的"}
        ]
    },
    # Paragraph 2
    {
        "id": 3,
        "para": 2,
        "en": "Archaeologists believe England" + RSQUO + "s most iconic prehistoric ruin was built in several stages, with the earliest constructed 5,000 or more years ago.",
        "zh": "考古学家认为，英格兰这座最具标志性的史前遗迹是分几个阶段建成的，其中最早的部分建于5,000年甚至更久以前。",
        "grammar": {
            "type": "宾语从句 + with 复合结构",
            "note": "主干 Archaeologists believe（后接省略 that 的宾语从句）England" + RSQUO + "s most iconic prehistoric ruin was built in several stages；with the earliest constructed 5,000 or more years ago 为 with 复合结构作状语，constructed 为过去分词。"
        },
        "words": [
            {"w": "iconic", "pos": "adj.", "def": "标志性的；偶像的"},
            {"w": "ruin", "pos": "n.", "def": "遗迹；废墟"}
        ]
    },
    {
        "id": 4,
        "para": 2,
        "en": "First, Neolithic Britons used primitive tools, which may have been fashioned out of deer antlers, to dig a massive circular ditch and bank, or henge.",
        "zh": "首先，新石器时代的不列颠人使用原始工具——这些工具可能是用鹿角制成的——挖出一条巨大的环形沟渠和土堤，即“亨基”（环形土垣）。",
        "grammar": {
            "type": "非限定性定语从句 + 不定式目的",
            "note": "主干是 Neolithic Britons used primitive tools... to dig a massive circular ditch and bank；which may have been fashioned out of deer antlers 为非限定性定语从句修饰 tools；or henge 为 ditch and bank 的同位补充。"
        },
        "words": [
            {"w": "primitive", "pos": "adj.", "def": "原始的"},
            {"w": "antler", "pos": "n.", "def": "鹿角"}
        ]
    },
    {
        "id": 5,
        "para": 2,
        "en": "Deep pits dating back to that era and located within the circle may have once held a ring of timber posts, according to some scholars.",
        "zh": "据一些学者说，那些可追溯到那个时代、位于圆圈之内的深坑，可能曾经竖立着一圈木柱。",
        "grammar": {
            "type": "现在分词与过去分词并列定语 + 情态推测",
            "note": "主语 Deep pits，dating back to that era（现在分词）和 located within the circle（过去分词）并列作后置定语；谓语 may have once held a ring of timber posts，may have done 表对过去的推测；according to some scholars 为来源状语。"
        },
        "words": [
            {"w": "pit", "pos": "n.", "def": "坑；深坑"},
            {"w": "timber post", "pos": "phr.", "def": "木柱"}
        ]
    },
    # Paragraph 3
    {
        "id": 6,
        "para": 3,
        "en": "Several hundred years later, it is thought, Stonehenge" + RSQUO + "s builders hoisted an estimated 80 bluestones, 43 of which remain today, into standing positions and placed them in either a horseshoe or circular formation.",
        "zh": "据认为，几百年之后，巨石阵的建造者把估计约80块青石竖立起来——其中43块留存至今——并将它们摆成马蹄形或环形。",
        "grammar": {
            "type": "插入语 + 非限定性定语从句 + 并列谓语",
            "note": "it is thought 为插入语；主干 Stonehenge" + RSQUO + "s builders hoisted an estimated 80 bluestones... and placed them...，两个谓语并列；43 of which remain today 为非限定性定语从句修饰 bluestones。"
        },
        "words": [
            {"w": "hoist", "pos": "v.", "def": "举起；吊起"},
            {"w": "bluestone", "pos": "n.", "def": "青石；蓝砂岩"}
        ]
    },
    {
        "id": 7,
        "para": 3,
        "en": "These stones have been traced all the way to the Preseli Hills in Wales, some 300 kilometres from Stonehenge.",
        "zh": "这些石头的来源已被一路追溯到威尔士的普雷塞利山，那里距巨石阵约300公里。",
        "grammar": {
            "type": "现在完成被动 + 同位补充",
            "note": "主干是 These stones have been traced all the way to the Preseli Hills in Wales，为现在完成时被动语态；some 300 kilometres from Stonehenge 为补充说明距离的同位结构。"
        },
        "words": [
            {"w": "trace", "pos": "v.", "def": "追溯；追踪"},
            {"w": "all the way", "pos": "phr.", "def": "一路；一直"}
        ]
    },
    {
        "id": 8,
        "para": 3,
        "en": "How, then, did prehistoric builders without sophisticated tools or engineering haul these boulders, which weigh up to four tons, over such a great distance?",
        "zh": "那么，没有精密工具或工程技术的史前建造者，是如何把这些重达四吨的巨石搬运如此之远的呢？",
        "grammar": {
            "type": "特殊疑问句 + 非限定性定语从句",
            "note": "主句为特殊疑问句 How did prehistoric builders... haul these boulders...，then 为插入语；without sophisticated tools or engineering 为介词短语修饰 builders；which weigh up to four tons 为非限定性定语从句修饰 boulders。"
        },
        "words": [
            {"w": "haul", "pos": "v.", "def": "拖运；搬运"},
            {"w": "boulder", "pos": "n.", "def": "巨石；圆石"}
        ]
    },
    # Paragraph 4
    {
        "id": 9,
        "para": 4,
        "en": "According to one long-standing theory among archaeologists, Stonehenge" + RSQUO + "s builders fashioned sledges and rollers out of tree trunks to lug the bluestones from the Preseli Hills.",
        "zh": "根据考古学家中一种由来已久的理论，巨石阵的建造者用树干制作了雪橇和滚木，以便把青石从普雷塞利山拖运过来。",
        "grammar": {
            "type": "主谓宾 + 不定式目的",
            "note": "主干是 Stonehenge" + RSQUO + "s builders fashioned sledges and rollers out of tree trunks，fashion A out of B 表“用B做成A”；to lug the bluestones from the Preseli Hills 为不定式作目的状语；According to... 为来源状语。"
        },
        "words": [
            {"w": "sledge", "pos": "n.", "def": "雪橇"},
            {"w": "lug", "pos": "v.", "def": "用力拖；拖拉"}
        ]
    },
    {
        "id": 10,
        "para": 4,
        "en": "They then transferred the boulders onto rafts and floated them first along the Welsh coast and then up the River Avon toward Salisbury Plain; alternatively, they may have towed each stone with a fleet of vessels.",
        "zh": "然后他们把巨石转移到木筏上，先沿威尔士海岸、再溯埃文河而上漂运到索尔兹伯里平原附近；或者，他们也可能用一支船队拖曳每一块石头。",
        "grammar": {
            "type": "并列谓语 + 分号 + alternatively 转折",
            "note": "前半 They then transferred the boulders onto rafts and floated them...，两个谓语并列，first... and then... 表先后；分号后 alternatively, they may have towed each stone... 提出另一种可能，may have done 表推测。"
        },
        "words": [
            {"w": "raft", "pos": "n.", "def": "木筏；筏子"},
            {"w": "tow", "pos": "v.", "def": "拖；牵引"}
        ]
    },
    {
        "id": 11,
        "para": 4,
        "en": "More recent archaeological hypotheses have them transporting the bluestones with supersized wicker baskets on a combination of ball bearings and long grooved planks, hauled by oxen.",
        "zh": "较新的考古学假说则认为，他们是用超大的柳条筐，把青石放在由滚珠轴承和长条带槽木板组合而成的装置上运送的，而这套装置由牛来拖拉。",
        "grammar": {
            "type": "have sb doing + 过去分词定语",
            "note": "主干 More recent archaeological hypotheses have them transporting the bluestones，have sb doing 表“认为某人在做”；with supersized wicker baskets 与 on a combination of... 为方式状语；hauled by oxen 为过去分词修饰前面的装置组合。"
        },
        "words": [
            {"w": "wicker", "pos": "adj.", "def": "柳条编的"},
            {"w": "ox", "pos": "n.", "def": "牛（复数 oxen）"}
        ]
    },
    # Paragraph 5
    {
        "id": 12,
        "para": 5,
        "en": "As early as the 1970s, geologists have been adding their voices to the debate over how Stonehenge came into being.",
        "zh": "早在20世纪70年代，地质学家们就开始就巨石阵是如何形成的这场争论发表意见。",
        "grammar": {
            "type": "现在完成进行时 + 介词短语",
            "note": "主干是 geologists have been adding their voices to the debate，为现在完成进行时；over how Stonehenge came into being 为介词短语，how 引导宾语从句，come into being 表“形成、产生”。"
        },
        "words": [
            {"w": "geologist", "pos": "n.", "def": "地质学家"},
            {"w": "come into being", "pos": "phr.", "def": "形成；产生"}
        ]
    },
    {
        "id": 13,
        "para": 5,
        "en": "Challenging the classic image of industrious builders pushing, carting, rolling or hauling giant stones from faraway Wales, some scientists have suggested that it was glaciers, not humans, that carried the bluestones to Salisbury Plain.",
        "zh": "一些科学家对“勤劳的建造者从遥远的威尔士推、拉、滚、拖巨石”这一经典形象提出质疑，认为把青石运到索尔兹伯里平原的是冰川，而不是人类。",
        "grammar": {
            "type": "现在分词状语 + 宾语从句 + 强调句",
            "note": "Challenging the classic image... 为现在分词短语作状语，pushing, carting, rolling or hauling... 修饰 builders；主干 some scientists have suggested that...；从句 it was glaciers, not humans, that carried... 为强调句型（强调 glaciers）。"
        },
        "words": [
            {"w": "industrious", "pos": "adj.", "def": "勤劳的；勤奋的"},
            {"w": "glacier", "pos": "n.", "def": "冰川"}
        ]
    },
    {
        "id": 14,
        "para": 5,
        "en": "Most archaeologists have remained sceptical about this theory, however, wondering how the forces of nature could possibly have delivered the exact number of stones needed to complete the circle.",
        "zh": "然而，大多数考古学家对这一理论仍持怀疑态度，他们不解自然之力怎么可能恰好送来完成这个圆圈所需的确切数量的石头。",
        "grammar": {
            "type": "现在分词状语 + 宾语从句 + 过去分词定语",
            "note": "主干是 Most archaeologists have remained sceptical about this theory，however 为插入转折；wondering how... 为现在分词作伴随状语，how 引导宾语从句；needed to complete the circle 为过去分词短语修饰 stones。"
        },
        "words": [
            {"w": "sceptical", "pos": "adj.", "def": "怀疑的"},
            {"w": "the forces of nature", "pos": "phr.", "def": "自然之力"}
        ]
    },
    # Paragraph 6
    {
        "id": 15,
        "para": 6,
        "en": "The third phase of construction took place around 2000 BCE.",
        "zh": "第三阶段的建造大约发生在公元前2000年。",
        "grammar": {
            "type": "主谓 + 时间状语",
            "note": "主干是 The third phase of construction took place；around 2000 BCE 为时间状语，take place 表“发生”。"
        },
        "words": [
            {"w": "phase", "pos": "n.", "def": "阶段"},
            {"w": "take place", "pos": "phr.", "def": "发生；进行"}
        ]
    },
    {
        "id": 16,
        "para": 6,
        "en": "At this point, sandstone slabs " + DASH + " known as " + LSQUO + "sarsens" + RSQUO + " " + DASH + " were arranged into an outer crescent or ring; some were assembled into the iconic three-pieced structures called trilithons that stand tall in the centre of Stonehenge.",
        "zh": "在这一阶段，砂岩石板——被称为“萨尔森石”——被排列成外围的新月形或环形；其中一些被组装成标志性的三石结构，即“三石塔”，高高矗立在巨石阵的中央。",
        "grammar": {
            "type": "被动语态 + 插入定语 + 分号并列 + 定语从句",
            "note": "前半 sandstone slabs... were arranged into an outer crescent or ring，known as " + LSQUO + "sarsens" + RSQUO + " 为插入的过去分词定语；分号后 some were assembled into the iconic three-pieced structures called trilithons，called trilithons 为过去分词定语，that stand tall... 为定语从句。"
        },
        "words": [
            {"w": "slab", "pos": "n.", "def": "厚板；石板"},
            {"w": "crescent", "pos": "n.", "def": "新月形；月牙形"}
        ]
    },
    {
        "id": 17,
        "para": 6,
        "en": "Some 50 of these stones are now visible on the site, which may once have contained many more.",
        "zh": "如今遗址上可见这些石头中的大约50块，而这里过去可能曾有更多。",
        "grammar": {
            "type": "主系表 + 非限定性定语从句",
            "note": "主干是 Some 50 of these stones are now visible on the site；which may once have contained many more 为非限定性定语从句修饰 site，may have done 表对过去的推测。"
        },
        "words": [
            {"w": "visible", "pos": "adj.", "def": "可见的"},
            {"w": "contain", "pos": "v.", "def": "包含；容纳"}
        ]
    },
    {
        "id": 18,
        "para": 6,
        "en": "Radiocarbon dating has revealed that work continued at Stonehenge until roughly 1600 BCE, with the bluestones in particular being repositioned multiple times.",
        "zh": "放射性碳测年法显示，巨石阵的施工一直持续到大约公元前1600年，尤其是那些青石曾被多次重新安置。",
        "grammar": {
            "type": "宾语从句 + with 复合结构",
            "note": "主干 Radiocarbon dating has revealed that...，that 引导宾语从句 work continued at Stonehenge until roughly 1600 BCE；with the bluestones... being repositioned multiple times 为 with 复合结构，being repositioned 为现在分词被动。"
        },
        "words": [
            {"w": "radiocarbon dating", "pos": "phr.", "def": "放射性碳测年法"},
            {"w": "reposition", "pos": "v.", "def": "重新安置；重新定位"}
        ]
    },
    # Paragraph 7
    {
        "id": 19,
        "para": 7,
        "en": "But who were the builders of Stonehenge?",
        "zh": "但巨石阵的建造者究竟是谁呢？",
        "grammar": {
            "type": "特殊疑问句",
            "note": "为特殊疑问句 who were the builders of Stonehenge，But 引出话题转折，起承上启下的作用。"
        },
        "words": [
            {"w": "builder", "pos": "n.", "def": "建造者"},
            {"w": "who", "pos": "pron.", "def": "谁"}
        ]
    },
    {
        "id": 20,
        "para": 7,
        "en": "In the 17th century, archaeologist John Aubrey made the claim that Stonehenge was the work of druids, who had important religious, judicial and political roles in Celtic society.",
        "zh": "17世纪，考古学家约翰·奥布里提出，巨石阵是德鲁伊教祭司的杰作，这些祭司在凯尔特社会中担任着重要的宗教、司法和政治角色。",
        "grammar": {
            "type": "同位语从句 + 非限定性定语从句",
            "note": "主干是 archaeologist John Aubrey made the claim；that Stonehenge was the work of druids 为同位语从句解释 claim；who had important religious, judicial and political roles 为非限定性定语从句修饰 druids。"
        },
        "words": [
            {"w": "druid", "pos": "n.", "def": "德鲁伊（古凯尔特人的祭司）"},
            {"w": "judicial", "pos": "adj.", "def": "司法的"}
        ]
    },
    {
        "id": 21,
        "para": 7,
        "en": "This theory was widely popularized by the antiquarian William Stukeley, who had unearthed primitive graves at the site.",
        "zh": "这一理论经古物学家威廉·斯图克利的大力推广而广为流传，他曾在该遗址挖掘出原始的坟墓。",
        "grammar": {
            "type": "被动语态 + 非限定性定语从句",
            "note": "主干是 This theory was widely popularized by the antiquarian William Stukeley，为被动语态；who had unearthed primitive graves at the site 为非限定性定语从句修饰 Stukeley。"
        },
        "words": [
            {"w": "antiquarian", "pos": "n.", "def": "古物学家；古董研究者"},
            {"w": "unearth", "pos": "v.", "def": "挖掘出；发掘"}
        ]
    },
    {
        "id": 22,
        "para": 7,
        "en": "Even today, people who identify as modern druids continue to gather at Stonehenge for the summer solstice.",
        "zh": "即便在今天，自认为是现代德鲁伊教徒的人们仍会在夏至时聚集到巨石阵。",
        "grammar": {
            "type": "定语从句 + 目的状语",
            "note": "主干是 people... continue to gather at Stonehenge；who identify as modern druids 为定语从句修饰 people，identify as 表“认同为”；for the summer solstice 为目的/时机状语。"
        },
        "words": [
            {"w": "identify as", "pos": "phr.", "def": "认同为；自认为是"},
            {"w": "solstice", "pos": "n.", "def": "至（夏至/冬至）"}
        ]
    },
    {
        "id": 23,
        "para": 7,
        "en": "However, in the mid-20th century, radiocarbon dating demonstrated that Stonehenge stood more than 1,000 years before the Celts inhabited the region.",
        "zh": "然而，20世纪中叶，放射性碳测年法证明，巨石阵早在凯尔特人定居该地区之前1,000多年就已经存在了。",
        "grammar": {
            "type": "宾语从句 + 时间状语从句",
            "note": "主干 radiocarbon dating demonstrated that...，that 引导宾语从句 Stonehenge stood more than 1,000 years；before the Celts inhabited the region 为时间状语从句；However 表转折。"
        },
        "words": [
            {"w": "demonstrate", "pos": "v.", "def": "证明；证实"},
            {"w": "inhabit", "pos": "v.", "def": "居住于；栖居"}
        ]
    },
    # Paragraph 8
    {
        "id": 24,
        "para": 8,
        "en": "Many modern historians and archaeologists now agree that several distinct tribes of people contributed to Stonehenge, each undertaking a different phase of its construction.",
        "zh": "许多现代历史学家和考古学家如今一致认为，有几个不同的部族都参与了巨石阵的建造，各自承担了其建造的不同阶段。",
        "grammar": {
            "type": "宾语从句 + 独立主格",
            "note": "主干 Many modern historians and archaeologists now agree that...，that 引导宾语从句 several distinct tribes of people contributed to Stonehenge；each undertaking a different phase of its construction 为独立主格结构作补充说明。"
        },
        "words": [
            {"w": "distinct", "pos": "adj.", "def": "不同的；截然不同的"},
            {"w": "tribe", "pos": "n.", "def": "部落；部族"}
        ]
    },
    {
        "id": 25,
        "para": 8,
        "en": "Bones, tools and other artefacts found on the site seem to support this hypothesis.",
        "zh": "在遗址上发现的骨头、工具和其他人工制品似乎都支持这一假说。",
        "grammar": {
            "type": "过去分词定语 + 主谓",
            "note": "主语为并列的 Bones, tools and other artefacts，found on the site 为过去分词短语作后置定语；谓语 seem to support this hypothesis。"
        },
        "words": [
            {"w": "artefact", "pos": "n.", "def": "人工制品；手工艺品"},
            {"w": "hypothesis", "pos": "n.", "def": "假说；假设"}
        ]
    },
    {
        "id": 26,
        "para": 8,
        "en": "The first stage was achieved by Neolithic agrarians who were likely to have been indigenous to the British Isles.",
        "zh": "第一阶段是由新石器时代的农耕者完成的，他们很可能是不列颠群岛的原住民。",
        "grammar": {
            "type": "被动语态 + 定语从句",
            "note": "主干是 The first stage was achieved by Neolithic agrarians，为被动语态；who were likely to have been indigenous to the British Isles 为定语从句修饰 agrarians，be likely to have done 表对过去的可能推测。"
        },
        "words": [
            {"w": "agrarian", "pos": "n.", "def": "农耕者；务农的人"},
            {"w": "indigenous", "pos": "adj.", "def": "本土的；原产的"}
        ]
    },
    {
        "id": 27,
        "para": 8,
        "en": "Later, it is believed, groups with advanced tools and a more communal way of life left their mark on the site.",
        "zh": "据信，后来一些拥有先进工具、过着更具集体性生活方式的群体也在遗址上留下了自己的印记。",
        "grammar": {
            "type": "插入语 + 主谓宾",
            "note": "it is believed 为插入语；主干 groups... left their mark on the site；with advanced tools and a more communal way of life 为介词短语修饰 groups；leave one" + RSQUO + "s mark 表“留下印记”。"
        },
        "words": [
            {"w": "communal", "pos": "adj.", "def": "公共的；集体的"},
            {"w": "leave one" + RSQUO + "s mark", "pos": "phr.", "def": "留下印记；产生影响"}
        ]
    },
    {
        "id": 28,
        "para": 8,
        "en": "Some believe that they were immigrants from the European continent, while others maintain that they were probably native Britons, descended from the original builders.",
        "zh": "有些人认为他们是来自欧洲大陆的移民，而另一些人则坚持认为他们很可能是本土的不列颠人，是最初建造者的后裔。",
        "grammar": {
            "type": "宾语从句 + while 对比 + 过去分词定语",
            "note": "前半 Some believe that they were immigrants...；while others maintain that they were probably native Britons 为 while 引导的对比分句，两个 that 各引导宾语从句；descended from the original builders 为过去分词短语修饰 Britons。"
        },
        "words": [
            {"w": "immigrant", "pos": "n.", "def": "移民"},
            {"w": "descend from", "pos": "phr.", "def": "是……的后裔；源自"}
        ]
    },
    # Paragraph 9
    {
        "id": 29,
        "para": 9,
        "en": "If the facts surrounding the architects and construction of Stonehenge remain shadowy at best, the purpose of the striking monument is even more of a mystery.",
        "zh": "如果说关于巨石阵的建造者和建造过程的种种事实充其量仍然模糊不清，那么这座引人注目的遗迹的用途就更是一个谜。",
        "grammar": {
            "type": "if 条件/让步从句 + 比较结构",
            "note": "If the facts... remain shadowy at best 为 if 引导的让步状语从句，at best 表“充其量”；主句 the purpose of the striking monument is even more of a mystery，even more of a 为比较强调。"
        },
        "words": [
            {"w": "shadowy", "pos": "adj.", "def": "模糊的；朦胧的"},
            {"w": "at best", "pos": "phr.", "def": "充其量；至多"}
        ]
    },
    {
        "id": 30,
        "para": 9,
        "en": "While there is consensus among the majority of modern scholars that Stonehenge once served the function of burial ground, they have yet to determine what other purposes it had.",
        "zh": "尽管大多数现代学者一致认为巨石阵曾充当过墓地，但他们尚未确定它还有其他什么用途。",
        "grammar": {
            "type": "while 让步从句 + 同位语从句 + 宾语从句",
            "note": "While there is consensus... that Stonehenge once served the function of burial ground 为 while 让步从句，that 引导同位语从句解释 consensus；主句 they have yet to determine what other purposes it had，have yet to do 表“尚未”，what... 为宾语从句。"
        },
        "words": [
            {"w": "consensus", "pos": "n.", "def": "共识；一致意见"},
            {"w": "burial ground", "pos": "phr.", "def": "墓地；埋葬地"}
        ]
    },
    # Paragraph 10
    {
        "id": 31,
        "para": 10,
        "en": "In the 1960s, the astronomer Gerald Hawkins suggested that the cluster of megalithic stones operated as a form of calendar, with different points corresponding to astrological phenomena such as solstices, equinoxes and eclipses occurring at different times of the year.",
        "zh": "20世纪60年代，天文学家杰拉尔德·霍金斯提出，这一群巨石起着某种日历的作用，不同的点位对应着在一年不同时节出现的天象，如夏至冬至、春分秋分和日月食。",
        "grammar": {
            "type": "宾语从句 + with 复合结构 + 现在分词定语",
            "note": "主干 the astronomer Gerald Hawkins suggested that...，that 引导宾语从句 the cluster of megalithic stones operated as a form of calendar；with different points corresponding to astrological phenomena 为 with 复合结构；occurring at different times of the year 为现在分词修饰 phenomena。"
        },
        "words": [
            {"w": "megalithic", "pos": "adj.", "def": "巨石的；巨石建筑的"},
            {"w": "equinox", "pos": "n.", "def": "春分；秋分"}
        ]
    },
    {
        "id": 32,
        "para": 10,
        "en": "While his theory has received a considerable amount of attention over the decades, critics maintain that Stonehenge" + RSQUO + "s builders probably lacked the knowledge necessary to predict such events or that England" + RSQUO + "s dense cloud cover would have obscured their view of the skies.",
        "zh": "尽管他的理论几十年来受到了相当多的关注，但批评者坚称，巨石阵的建造者很可能缺乏预测此类天象所需的知识，或者认为英格兰浓密的云层本会遮挡他们观测天空的视线。",
        "grammar": {
            "type": "while 让步从句 + 两个并列宾语从句",
            "note": "While his theory has received... attention 为让步从句；主句 critics maintain that... or that...，两个 that 引导并列宾语从句：builders probably lacked the knowledge（necessary to predict such events 为不定式定语）与 England" + RSQUO + "s dense cloud cover would have obscured their view。"
        },
        "words": [
            {"w": "obscure", "pos": "v.", "def": "遮蔽；使模糊"},
            {"w": "cloud cover", "pos": "phr.", "def": "云层；云量"}
        ]
    },
    {
        "id": 33,
        "para": 10,
        "en": "More recently, signs of illness and injury in the human remains unearthed at Stonehenge led a group of British archaeologists to speculate that it was considered a place of healing, perhaps because bluestones were thought to have curative powers.",
        "zh": "最近，在巨石阵出土的人类遗骸中发现的疾病和伤痛迹象，使一群英国考古学家推测，这里曾被视为一处疗愈之地，也许是因为人们认为青石具有治病的力量。",
        "grammar": {
            "type": "过去分词定语 + lead sb to do + 宾语从句 + 原因状语",
            "note": "主语 signs of illness and injury，in the human remains unearthed at Stonehenge 为修饰成分，unearthed 为过去分词；谓语 led a group of British archaeologists to speculate that...，lead sb to do 结构；that it was considered a place of healing 为宾语从句；perhaps because bluestones were thought to have curative powers 为原因状语。"
        },
        "words": [
            {"w": "speculate", "pos": "v.", "def": "推测；猜测"},
            {"w": "curative", "pos": "adj.", "def": "治病的；有疗效的"}
        ]
    }
]

questions = [
    {
        "title": "Questions 1" + DASH + "8",
        "type": "note_completion",
        "instructions": [
            "Complete the notes below.",
            "Choose NO MORE THAN TWO WORDS from the passage for each answer.",
            "Write your answers in boxes 1" + DASH + "8 on your answer sheet.",
            "Stonehenge"
        ],
        "items": [
            {"number": 1, "prompt": "Stage 1: the ditch and henge were dug, possibly using tools made from 1 ____ .", "answer": "(deer) antlers", "evidence_sentence": 4},
            {"number": 2, "prompt": "Stage 1: 2 ____ may have been arranged in deep pits inside the circle.", "answer": "(timber) posts", "evidence_sentence": 5},
            {"number": 3, "prompt": "Stage 2 (archaeological theory): builders used 3 ____ to make sledges and rollers.", "answer": "tree trunks", "evidence_sentence": 9},
            {"number": 4, "prompt": "Stage 2 (archaeological theory): 4 ____ pulled them on giant baskets.", "answer": "oxen", "evidence_sentence": 11},
            {"number": 5, "prompt": "Stage 2 (geological theory): they were brought from Wales by 5 ____ .", "answer": "glaciers", "evidence_sentence": 13},
            {"number": 6, "prompt": "Builders: a theory arose in the 17th century that its builders were Celtic 6 ____ .", "answer": "druids", "evidence_sentence": 20},
            {"number": 7, "prompt": "Purpose: many experts agree it has been used as a 7 ____ site.", "answer": "burial", "evidence_sentence": 30},
            {"number": 8, "prompt": "Purpose: in the 1960s, it was suggested that it worked as a kind of 8 ____ .", "answer": "calendar", "evidence_sentence": 31}
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
            {"number": 9, "prompt": "During the third phase of construction, sandstone slabs were placed in both the outer areas and the middle of the Stonehenge site.", "answer": "TRUE", "evidence_sentence": 16},
            {"number": 10, "prompt": "There is scientific proof that the bluestones stood in the same spot until approximately 1600 BCE.", "answer": "FALSE", "evidence_sentence": 18},
            {"number": 11, "prompt": "John Aubrey" + RSQUO + "s claim about Stonehenge was supported by 20th-century findings.", "answer": "FALSE", "evidence_sentence": 23},
            {"number": 12, "prompt": "Objects discovered at Stonehenge seem to indicate that it was constructed by a number of different groups of people.", "answer": "TRUE", "evidence_sentence": 25},
            {"number": 13, "prompt": "Criticism of Gerald Hawkins" + RSQUO + " theory about Stonehenge has come mainly from other astronomers.", "answer": "NOT GIVEN", "evidence_sentence": 32}
        ]
    }
]

phrases = [
    {"w": "Stonehenge", "pos": "n.", "def": "巨石阵（英国史前巨石遗迹）"},
    {"w": "Salisbury Plain", "pos": "n.", "def": "索尔兹伯里平原"},
    {"w": "Preseli Hills", "pos": "n.", "def": "普雷塞利山（威尔士，青石产地）"},
    {"w": "the Neolithic (era)", "pos": "n.", "def": "新石器时代"},
    {"w": "radiocarbon dating", "pos": "n.", "def": "放射性碳测年法"},
    {"w": "sarsen", "pos": "n.", "def": "萨尔森石（一种砂岩巨石）"},
    {"w": "trilithon", "pos": "n.", "def": "三石塔（两立石加一横楣）"},
    {"w": "the Celts", "pos": "n.", "def": "凯尔特人"},
    {"w": "summer solstice", "pos": "n.", "def": "夏至"},
    {"w": "burial ground", "pos": "n.", "def": "墓地"}
]

data = {
    "id": "c18-test2-p1",
    "source": "剑桥雅思18 · Test 2 · Passage 1",
    "title": "Stonehenge",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c18-test2-p1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
