# -*- coding: utf-8 -*-
"""Generate data/passages/c15-test1-p1.json (Nutmeg - a valuable spice)."""
import json
import os

RSQUO = "’"  # '
LSQUO = "‘"  # '
DASH = "–"   # –

sentences = [
    # Para 1
    {
        "id": 1,
        "para": 1,
        "en": "The nutmeg tree, Myristica fragrans, is a large evergreen tree native to Southeast Asia.",
        "zh": "肉豆蔻树（学名 Myristica fragrans）是一种原产于东南亚的大型常绿乔木。",
        "grammar": {
            "type": "同位语 + 主系表",
            "note": "Myristica fragrans 为 The nutmeg tree 的同位语（斜体学名）；native to Southeast Asia 为形容词短语作后置定语修饰 tree。"
        },
        "words": [
            {"w": "nutmeg", "pos": "n.", "def": "肉豆蔻（香料）"},
            {"w": "evergreen", "pos": "adj.", "def": "常绿的"},
            {"w": "native to", "pos": "phr.", "def": "原产于；……的原生地"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "Until the late 18th century, it only grew in one place in the world: a small group of islands in the Banda Sea, part of the Moluccas " + DASH + " or Spice Islands " + DASH + " in northeastern Indonesia.",
        "zh": "直到18世纪晚期，它在全世界只生长于一个地方：位于印度尼西亚东北部班达海中的一小群岛屿，即摩鹿加群岛（又称香料群岛）的一部分。",
        "grammar": {
            "type": "冒号说明 + 同位语",
            "note": "冒号后 a small group of islands... 具体说明 one place；part of the Moluccas 为同位语；两个破折号间 or Spice Islands 为对 the Moluccas 的补充。"
        },
        "words": [
            {"w": "grow", "pos": "v.", "def": "生长"},
            {"w": "Spice Islands", "pos": "phr.", "def": "香料群岛（摩鹿加群岛的旧称）"},
            {"w": "northeastern", "pos": "adj.", "def": "东北部的"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "The tree is thickly branched with dense foliage of tough, dark green oval leaves, and produces small, yellow, bell-shaped flowers and pale yellow pear-shaped fruits.",
        "zh": "这种树枝干繁茂，长着坚韧的深绿色椭圆形叶片构成的浓密枝叶，并会开出黄色的小钟形花，结出淡黄色的梨形果实。",
        "grammar": {
            "type": "并列谓语 + with 短语",
            "note": "主语 The tree 带两个并列谓语 is thickly branched 与 produces...；with dense foliage of... 为介词短语作伴随状语；oval、bell-shaped、pear-shaped 均为形容词修饰各中心词。"
        },
        "words": [
            {"w": "branched", "pos": "adj.", "def": "有分枝的"},
            {"w": "foliage", "pos": "n.", "def": "叶子（总称）；枝叶"},
            {"w": "oval", "pos": "adj.", "def": "椭圆形的"},
            {"w": "bell-shaped", "pos": "adj.", "def": "钟形的"},
            {"w": "pear-shaped", "pos": "adj.", "def": "梨形的"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "The fruit is encased in a fleshy husk.",
        "zh": "果实被包裹在一层肉质的外壳中。",
        "grammar": {
            "type": "被动语态",
            "note": "is encased in 为被动结构，encase 意为 “把……装入、包住”；fleshy husk 意为 “肉质的外壳”。"
        },
        "words": [
            {"w": "encase", "pos": "v.", "def": "把……装入；包住"},
            {"w": "fleshy", "pos": "adj.", "def": "肉质的；多肉的"},
            {"w": "husk", "pos": "n.", "def": "外壳；果皮"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "When the fruit is ripe, this husk splits into two halves along a ridge running the length of the fruit.",
        "zh": "当果实成熟时，这层外壳会沿着一条贯穿果实全长的脊线裂成两半。",
        "grammar": {
            "type": "时间状语从句 + 现在分词定语",
            "note": "When 引导时间状语从句；running the length of the fruit 为现在分词短语作定语修饰 ridge；split into 意为 “裂开成”。"
        },
        "words": [
            {"w": "ripe", "pos": "adj.", "def": "成熟的"},
            {"w": "split into", "pos": "phr.", "def": "裂开成；分成"},
            {"w": "ridge", "pos": "n.", "def": "脊；隆起线"}
        ]
    },
    {
        "id": 6,
        "para": 1,
        "en": "Inside is a purple-brown shiny seed, 2" + DASH + "3 cm long by about 2 cm across, surrounded by a lacy red or crimson covering called an " + LSQUO + "aril" + RSQUO + ".",
        "zh": "里面是一颗紫褐色、有光泽的种子，长约2至3厘米、横径约2厘米，外面裹着一层网状的红色或深红色包膜，称为“假种皮”（aril）。",
        "grammar": {
            "type": "完全倒装 + 过去分词定语",
            "note": "Inside is a... seed 为地点状语前置引起的完全倒装（正常语序 A seed is inside）；surrounded by... 与 called an 'aril' 均为过去分词短语作定语；by 此处表尺寸的 “乘、及”。"
        },
        "words": [
            {"w": "shiny", "pos": "adj.", "def": "有光泽的；闪亮的"},
            {"w": "across", "pos": "adv.", "def": "（直径/横向）宽"},
            {"w": "lacy", "pos": "adj.", "def": "花边似的；网状的"},
            {"w": "crimson", "pos": "adj.", "def": "深红色的"},
            {"w": "aril", "pos": "n.", "def": "假种皮"}
        ]
    },
    {
        "id": 7,
        "para": 1,
        "en": "These are the sources of the two spices nutmeg and mace, the former being produced from the dried seed and the latter from the aril.",
        "zh": "这些便是肉豆蔻（nutmeg）和肉豆蔻衣（mace）这两种香料的来源，前者由干燥的种子制成，后者则取自假种皮。",
        "grammar": {
            "type": "独立主格结构",
            "note": "the former being produced... 为独立主格结构补充说明；the former / the latter 分别指 nutmeg / mace；后半句 and the latter (being produced) from the aril 承前省略。"
        },
        "words": [
            {"w": "source", "pos": "n.", "def": "来源；出处"},
            {"w": "spice", "pos": "n.", "def": "香料；调味品"},
            {"w": "mace", "pos": "n.", "def": "肉豆蔻衣（由假种皮制成的香料）"},
            {"w": "the former ... the latter", "pos": "phr.", "def": "前者……后者……"}
        ]
    },
    # Para 2
    {
        "id": 8,
        "para": 2,
        "en": "Nutmeg was a highly prized and costly ingredient in European cuisine in the Middle Ages, and was used as a flavouring, medicinal, and preservative agent.",
        "zh": "在中世纪，肉豆蔻是欧洲烹饪中一种备受珍视且价格昂贵的原料，被用作调味剂、药物和防腐剂。",
        "grammar": {
            "type": "并列谓语（被动）",
            "note": "主语 Nutmeg 带两个并列谓语 was a... ingredient 与 was used as...；flavouring, medicinal, and preservative 并列修饰 agent。"
        },
        "words": [
            {"w": "prized", "pos": "adj.", "def": "受珍视的；珍贵的"},
            {"w": "costly", "pos": "adj.", "def": "昂贵的"},
            {"w": "cuisine", "pos": "n.", "def": "烹饪；菜肴"},
            {"w": "flavouring", "pos": "n.", "def": "调味品；香料"},
            {"w": "preservative", "pos": "adj.", "def": "防腐的"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "Throughout this period, the Arabs were the exclusive importers of the spice to Europe.",
        "zh": "在整个这一时期，阿拉伯人是将这种香料输入欧洲的唯一进口商。",
        "grammar": {
            "type": "主系表",
            "note": "Throughout this period 为时间状语；the exclusive importers of the spice to Europe 为表语；exclusive 意为 “独家的、唯一的”。"
        },
        "words": [
            {"w": "exclusive", "pos": "adj.", "def": "独家的；专有的"},
            {"w": "importer", "pos": "n.", "def": "进口商"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "They sold nutmeg for high prices to merchants based in Venice, but they never revealed the exact location of the source of this extremely valuable commodity.",
        "zh": "他们以高价把肉豆蔻卖给驻威尼斯的商人，却从不透露这种极其贵重的商品的确切产地。",
        "grammar": {
            "type": "转折并列 + 过去分词定语",
            "note": "but 连接转折两分句；based in Venice 为过去分词短语作定语修饰 merchants；reveal 意为 “透露、揭示”。"
        },
        "words": [
            {"w": "merchant", "pos": "n.", "def": "商人"},
            {"w": "reveal", "pos": "v.", "def": "透露；揭示"},
            {"w": "commodity", "pos": "n.", "def": "商品；货物"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": "The Arab-Venetian dominance of the trade finally ended in 1512, when the Portuguese reached the Banda Islands and began exploiting its precious resources.",
        "zh": "阿拉伯-威尼斯人对这一贸易的垄断最终于1512年结束，那一年葡萄牙人抵达班达群岛并开始开发其宝贵的资源。",
        "grammar": {
            "type": "非限定性定语从句",
            "note": "when the Portuguese reached... 为 when 引导的非限定性定语从句修饰 1512；从句内 reached 与 began 为并列谓语。"
        },
        "words": [
            {"w": "dominance", "pos": "n.", "def": "支配；主导地位"},
            {"w": "exploit", "pos": "v.", "def": "开发；利用；剥削"},
            {"w": "precious", "pos": "adj.", "def": "宝贵的；珍贵的"}
        ]
    },
    # Para 3
    {
        "id": 12,
        "para": 3,
        "en": "Always in danger of competition from neighbouring Spain, the Portuguese began subcontracting their spice distribution to Dutch traders.",
        "zh": "由于始终面临来自邻国西班牙的竞争威胁，葡萄牙人开始把香料的分销转包给荷兰商人。",
        "grammar": {
            "type": "形容词短语状语",
            "note": "Always in danger of competition from neighbouring Spain 为形容词短语作原因状语；subcontract A to B 意为 “把 A 转包给 B”。"
        },
        "words": [
            {"w": "competition", "pos": "n.", "def": "竞争"},
            {"w": "neighbouring", "pos": "adj.", "def": "邻近的"},
            {"w": "subcontract", "pos": "v.", "def": "转包；分包"},
            {"w": "distribution", "pos": "n.", "def": "分销；分配"}
        ]
    },
    {
        "id": 13,
        "para": 3,
        "en": "Profits began to flow into the Netherlands, and the Dutch commercial fleet swiftly grew into one of the largest in the world.",
        "zh": "利润开始流入荷兰，荷兰的商船队迅速发展成世界上最庞大的船队之一。",
        "grammar": {
            "type": "并列句",
            "note": "and 连接两个分句；grow into 意为 “发展成、成长为”；one of the largest 为 “最……之一”。"
        },
        "words": [
            {"w": "profit", "pos": "n.", "def": "利润"},
            {"w": "commercial", "pos": "adj.", "def": "商业的"},
            {"w": "fleet", "pos": "n.", "def": "船队；舰队"},
            {"w": "swiftly", "pos": "adv.", "def": "迅速地"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": "The Dutch quietly gained control of most of the shipping and trading of spices in Northern Europe.",
        "zh": "荷兰人悄然掌控了北欧大部分香料的运输和贸易。",
        "grammar": {
            "type": "简单句",
            "note": "gain control of 意为 “取得对……的控制”；of spices 修饰 shipping and trading。"
        },
        "words": [
            {"w": "gain control of", "pos": "phr.", "def": "取得对……的控制"},
            {"w": "shipping", "pos": "n.", "def": "航运；运输"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "Then, in 1580, Portugal fell under Spanish rule, and by the end of the 16th century the Dutch found themselves locked out of the market.",
        "zh": "随后，1580年葡萄牙落入西班牙的统治之下，到16世纪末，荷兰人发现自己被挡在了市场之外。",
        "grammar": {
            "type": "并列句 + 复合宾语",
            "note": "and 连接两分句；found themselves locked out 为 “find + 宾语 + 过去分词” 复合宾语结构；fall under... rule 意为 “落入……的统治”。"
        },
        "words": [
            {"w": "fall under", "pos": "phr.", "def": "落入（……的控制/统治）"},
            {"w": "rule", "pos": "n.", "def": "统治"},
            {"w": "lock out", "pos": "phr.", "def": "把……关在外面；排斥在外"}
        ]
    },
    {
        "id": 16,
        "para": 3,
        "en": "As prices for pepper, nutmeg, and other spices soared across Europe, they decided to fight back.",
        "zh": "随着胡椒、肉豆蔻及其他香料的价格在整个欧洲飞涨，他们决定反击。",
        "grammar": {
            "type": "时间/原因状语从句",
            "note": "As 引导状语从句（表 “随着/由于”）；soar 意为 “猛涨”；fight back 意为 “反击、还击”。"
        },
        "words": [
            {"w": "pepper", "pos": "n.", "def": "胡椒"},
            {"w": "soar", "pos": "v.", "def": "猛增；飞涨"},
            {"w": "fight back", "pos": "phr.", "def": "反击；还击"}
        ]
    },
    # Para 4
    {
        "id": 17,
        "para": 4,
        "en": "In 1602, Dutch merchants founded the VOC, a trading corporation better known as the Dutch East India Company.",
        "zh": "1602年，荷兰商人创立了 VOC，即更为人所熟知的荷兰东印度公司。",
        "grammar": {
            "type": "同位语",
            "note": "a trading corporation better known as... 为 VOC 的同位语；better known as 意为 “更常被称为”。"
        },
        "words": [
            {"w": "found", "pos": "v.", "def": "创立；建立"},
            {"w": "corporation", "pos": "n.", "def": "公司；企业"},
            {"w": "better known as", "pos": "phr.", "def": "更常被称为"}
        ]
    },
    {
        "id": 18,
        "para": 4,
        "en": "By 1617, the VOC was the richest commercial operation in the world.",
        "zh": "到1617年，VOC 已成为世界上最富有的商业机构。",
        "grammar": {
            "type": "主系表",
            "note": "By 1617 为时间状语；the richest commercial operation 为表语，operation 此处指 “商业机构/企业”。"
        },
        "words": [
            {"w": "commercial operation", "pos": "phr.", "def": "商业机构；商业运作"},
            {"w": "richest", "pos": "adj.", "def": "最富有的"}
        ]
    },
    {
        "id": 19,
        "para": 4,
        "en": "The company had 50,000 employees worldwide, with a private army of 30,000 men and a fleet of 200 ships.",
        "zh": "该公司在全球拥有5万名员工，还配备一支3万人的私人军队和一支200艘船的船队。",
        "grammar": {
            "type": "with 复合结构",
            "note": "with a private army of 30,000 men and a fleet of 200 ships 为 with 引导的复合结构作伴随状语。"
        },
        "words": [
            {"w": "employee", "pos": "n.", "def": "员工；雇员"},
            {"w": "worldwide", "pos": "adv.", "def": "在全世界"},
            {"w": "private army", "pos": "phr.", "def": "私人军队"}
        ]
    },
    {
        "id": 20,
        "para": 4,
        "en": "At the same time, thousands of people across Europe were dying of the plague, a highly contagious and deadly disease.",
        "zh": "与此同时，整个欧洲有成千上万的人死于瘟疫——一种传染性极强的致命疾病。",
        "grammar": {
            "type": "过去进行时 + 同位语",
            "note": "were dying of 为过去进行时；a highly contagious and deadly disease 为 the plague 的同位语；die of 意为 “死于（疾病等）”。"
        },
        "words": [
            {"w": "plague", "pos": "n.", "def": "瘟疫；鼠疫"},
            {"w": "contagious", "pos": "adj.", "def": "传染性的"},
            {"w": "deadly", "pos": "adj.", "def": "致命的"}
        ]
    },
    {
        "id": 21,
        "para": 4,
        "en": "Doctors were desperate for a way to stop the spread of this disease, and they decided nutmeg held the cure.",
        "zh": "医生们迫切想找到阻止这种疾病传播的办法，于是他们认定肉豆蔻能治愈它。",
        "grammar": {
            "type": "并列句 + 宾语从句",
            "note": "and 连接两分句；decided (that) nutmeg held the cure 为省略 that 的宾语从句；be desperate for 意为 “极度渴望”；hold the cure 意为 “掌握治愈之法”。"
        },
        "words": [
            {"w": "desperate for", "pos": "phr.", "def": "极度渴望；急需"},
            {"w": "spread", "pos": "n.", "def": "传播；蔓延"},
            {"w": "cure", "pos": "n.", "def": "治愈；疗法"}
        ]
    },
    {
        "id": 22,
        "para": 4,
        "en": "Everybody wanted nutmeg, and many were willing to spare no expense to have it.",
        "zh": "人人都想要肉豆蔻，许多人愿意不惜一切代价去得到它。",
        "grammar": {
            "type": "并列句",
            "note": "and 连接两分句；be willing to do 意为 “愿意做”；spare no expense 意为 “不惜代价”。"
        },
        "words": [
            {"w": "be willing to", "pos": "phr.", "def": "愿意（做）"},
            {"w": "spare no expense", "pos": "phr.", "def": "不惜代价；不吝花费"}
        ]
    },
    {
        "id": 23,
        "para": 4,
        "en": "Nutmeg bought for a few pennies in Indonesia could be sold for 68,000 times its original cost on the streets of London.",
        "zh": "在印度尼西亚只花几便士买到的肉豆蔻，在伦敦街头能以其原价的6.8万倍卖出。",
        "grammar": {
            "type": "过去分词定语 + 被动",
            "note": "bought for a few pennies in Indonesia 为过去分词短语作定语修饰 Nutmeg；could be sold 为被动；68,000 times its original cost 表 “原价的6.8万倍”。"
        },
        "words": [
            {"w": "penny", "pos": "n.", "def": "便士（英国货币单位）"},
            {"w": "original", "pos": "adj.", "def": "原来的；最初的"},
            {"w": "cost", "pos": "n.", "def": "成本；价钱"}
        ]
    },
    {
        "id": 24,
        "para": 4,
        "en": "The only problem was the short supply. And that" + RSQUO + "s where the Dutch found their opportunity.",
        "zh": "唯一的问题是供应短缺。而这正是荷兰人发现商机之处。",
        "grammar": {
            "type": "主系表 + 表语从句",
            "note": "第一句主系表结构；第二句 that's where... 为 where 引导的表语从句，表 “那正是……的地方”。"
        },
        "words": [
            {"w": "short supply", "pos": "phr.", "def": "供应不足；短缺"},
            {"w": "opportunity", "pos": "n.", "def": "机会；商机"}
        ]
    },
    # Para 5
    {
        "id": 25,
        "para": 5,
        "en": "The Banda Islands were ruled by local sultans who insisted on maintaining a neutral trading policy towards foreign powers.",
        "zh": "班达群岛由当地的苏丹统治，他们坚持对外国列强奉行中立的贸易政策。",
        "grammar": {
            "type": "被动 + 定语从句",
            "note": "were ruled by 为被动；who insisted on... 为定语从句修饰 sultans；insist on doing 意为 “坚持做”。"
        },
        "words": [
            {"w": "sultan", "pos": "n.", "def": "苏丹（某些穆斯林国家的君主）"},
            {"w": "insist on", "pos": "phr.", "def": "坚持"},
            {"w": "neutral", "pos": "adj.", "def": "中立的"},
            {"w": "foreign powers", "pos": "phr.", "def": "外国列强"}
        ]
    },
    {
        "id": 26,
        "para": 5,
        "en": "This allowed them to avoid the presence of Portuguese or Spanish troops on their soil, but it also left them unprotected from other invaders.",
        "zh": "这使他们得以避免葡萄牙或西班牙军队进驻其领土，但也使他们在面对其他入侵者时毫无防护。",
        "grammar": {
            "type": "转折并列 + 复合宾语",
            "note": "but 连接转折；allow sb to do 意为 “使某人能够做”；left them unprotected 为 “leave + 宾语 + 形容词” 复合宾语。"
        },
        "words": [
            {"w": "presence", "pos": "n.", "def": "存在；驻扎"},
            {"w": "troops", "pos": "n.", "def": "军队；部队"},
            {"w": "soil", "pos": "n.", "def": "国土；领土"},
            {"w": "invader", "pos": "n.", "def": "入侵者"}
        ]
    },
    {
        "id": 27,
        "para": 5,
        "en": "In 1621, the Dutch arrived and took over.",
        "zh": "1621年，荷兰人到来并接管了这里。",
        "grammar": {
            "type": "并列谓语",
            "note": "arrived 与 took over 为并列谓语；take over 意为 “接管、占领”。"
        },
        "words": [
            {"w": "take over", "pos": "phr.", "def": "接管；接手；占领"}
        ]
    },
    {
        "id": 28,
        "para": 5,
        "en": "Once securely in control of the Bandas, the Dutch went to work protecting their new investment.",
        "zh": "一旦稳固地控制了班达群岛，荷兰人便着手保护他们的这项新投资。",
        "grammar": {
            "type": "省略状语从句 + 现在分词状语",
            "note": "Once (they were) securely in control of... 为省略主谓的时间状语从句；protecting their new investment 为现在分词短语作方式状语；go to work doing 意为 “开始着手做”。"
        },
        "words": [
            {"w": "securely", "pos": "adv.", "def": "牢固地；安全地"},
            {"w": "in control of", "pos": "phr.", "def": "控制着；掌管"},
            {"w": "investment", "pos": "n.", "def": "投资"}
        ]
    },
    {
        "id": 29,
        "para": 5,
        "en": "They concentrated all nutmeg production into a few easily guarded areas, uprooting and destroying any trees outside the plantation zones.",
        "zh": "他们把所有肉豆蔻生产集中到少数几个易于守卫的区域，并连根拔除、销毁种植区以外的任何树木。",
        "grammar": {
            "type": "现在分词状语",
            "note": "uprooting and destroying... 为现在分词短语作伴随状语；concentrate A into B 意为 “把 A 集中到 B”；easily guarded 为副词+过去分词作定语。"
        },
        "words": [
            {"w": "concentrate", "pos": "v.", "def": "集中"},
            {"w": "guarded", "pos": "adj.", "def": "被守卫的；受保护的"},
            {"w": "uproot", "pos": "v.", "def": "连根拔起；根除"},
            {"w": "plantation", "pos": "n.", "def": "种植园"}
        ]
    },
    {
        "id": 30,
        "para": 5,
        "en": "Anyone caught growing a nutmeg seedling or carrying seeds without the proper authority was severely punished.",
        "zh": "任何人若被发现在未经适当许可的情况下种植肉豆蔻幼苗或携带种子，都会受到严厉惩罚。",
        "grammar": {
            "type": "过去分词定语 + 被动",
            "note": "caught growing... or carrying... 为过去分词短语作定语修饰 Anyone（catch sb doing 的被动含义）；主句谓语 was severely punished 为被动。"
        },
        "words": [
            {"w": "seedling", "pos": "n.", "def": "幼苗；秧苗"},
            {"w": "authority", "pos": "n.", "def": "许可；授权；权限"},
            {"w": "severely", "pos": "adv.", "def": "严厉地；严重地"},
            {"w": "punish", "pos": "v.", "def": "惩罚"}
        ]
    },
    {
        "id": 31,
        "para": 5,
        "en": "In addition, all exported nutmeg was covered with lime to make sure there was no chance a fertile seed which could be grown elsewhere would leave the islands.",
        "zh": "此外，所有出口的肉豆蔻都被涂上石灰，以确保不会有能在别处种植的有活力的种子流出这些岛屿。",
        "grammar": {
            "type": "目的状语 + 多重从句",
            "note": "to make sure... 为目的状语；其后 (that) there was no chance (that) a fertile seed... would leave... 含省略连词的宾语从句与同位语从句；which could be grown elsewhere 为定语从句修饰 seed。"
        },
        "words": [
            {"w": "exported", "pos": "adj.", "def": "出口的"},
            {"w": "lime", "pos": "n.", "def": "石灰"},
            {"w": "fertile", "pos": "adj.", "def": "能结果实的；有繁殖力的"},
            {"w": "elsewhere", "pos": "adv.", "def": "在别处"}
        ]
    },
    {
        "id": 32,
        "para": 5,
        "en": "There was only one obstacle to Dutch domination.",
        "zh": "荷兰人的统治只有一个障碍。",
        "grammar": {
            "type": "there be 句型",
            "note": "obstacle to sth 意为 “……的障碍”；to Dutch domination 为介词短语作定语。"
        },
        "words": [
            {"w": "obstacle", "pos": "n.", "def": "障碍；阻碍"},
            {"w": "domination", "pos": "n.", "def": "统治；支配"}
        ]
    },
    {
        "id": 33,
        "para": 5,
        "en": "One of the Banda Islands, a sliver of land called Run, only 3 km long by less than 1 km wide, was under the control of the British.",
        "zh": "班达群岛中的一座岛——一条名为伦（Run）的狭长陆地，仅约3公里长、不到1公里宽——当时处于英国的控制之下。",
        "grammar": {
            "type": "同位语插入",
            "note": "a sliver of land called Run... 为主语 One of the Banda Islands 的同位语（含 called Run 过去分词定语与尺寸插入语）；主句谓语 was under the control of。"
        },
        "words": [
            {"w": "sliver", "pos": "n.", "def": "细长的一片；小条"},
            {"w": "under the control of", "pos": "phr.", "def": "在……的控制之下"}
        ]
    },
    {
        "id": 34,
        "para": 5,
        "en": "After decades of fighting for control of this tiny island, the Dutch and British arrived at a compromise settlement, the Treaty of Breda, in 1667.",
        "zh": "在为争夺这座小岛的控制权而征战数十年后，荷兰人与英国人于1667年达成了一项妥协协议，即《布雷达条约》。",
        "grammar": {
            "type": "同位语",
            "note": "the Treaty of Breda 为 a compromise settlement 的同位语；arrive at a settlement 意为 “达成协议”；fighting for 为动名词作介词 of 的宾语。"
        },
        "words": [
            {"w": "decade", "pos": "n.", "def": "十年"},
            {"w": "compromise", "pos": "n.", "def": "妥协；折中"},
            {"w": "settlement", "pos": "n.", "def": "协议；解决；和解"},
            {"w": "treaty", "pos": "n.", "def": "条约"}
        ]
    },
    {
        "id": 35,
        "para": 5,
        "en": "Intent on securing their hold over every nutmeg-producing island, the Dutch offered a trade: if the British would give them the island of Run, they would in turn give Britain a distant and much less valuable island in North America.",
        "zh": "荷兰人一心要确保对每一座产肉豆蔻的岛屿的掌控，于是提出一笔交易：如果英国把伦岛给他们，他们就作为回报把北美一座遥远且价值低得多的岛屿给英国。",
        "grammar": {
            "type": "形容词短语状语 + 冒号 + 条件句",
            "note": "Intent on securing... 为形容词短语作状语；冒号后 if... they would in turn... 为条件句；in turn 意为 “作为回报、反过来”。"
        },
        "words": [
            {"w": "intent on", "pos": "phr.", "def": "决心做；专注于"},
            {"w": "secure", "pos": "v.", "def": "确保；使安全"},
            {"w": "hold", "pos": "n.", "def": "掌控；控制"},
            {"w": "in turn", "pos": "phr.", "def": "作为回报；反过来"}
        ]
    },
    {
        "id": 36,
        "para": 5,
        "en": "The British agreed. That other island was Manhattan, which is how New Amsterdam became New York.",
        "zh": "英国同意了。那另一座岛就是曼哈顿——新阿姆斯特丹正是这样变成了纽约。",
        "grammar": {
            "type": "非限定性定语从句",
            "note": "which is how... 为非限定性定语从句，which 指代前一整句内容；how New Amsterdam became New York 为表语从句。"
        },
        "words": [
            {"w": "agree", "pos": "v.", "def": "同意"},
            {"w": "Manhattan", "pos": "n.", "def": "曼哈顿（纽约的一个区）"}
        ]
    },
    {
        "id": 37,
        "para": 5,
        "en": "The Dutch now had a monopoly over the nutmeg trade which would last for another century.",
        "zh": "荷兰人如今对肉豆蔻贸易拥有了垄断，而这种垄断还将再持续一个世纪。",
        "grammar": {
            "type": "定语从句",
            "note": "which would last for another century 为定语从句修饰 monopoly；have a monopoly over 意为 “对……拥有垄断”。"
        },
        "words": [
            {"w": "monopoly", "pos": "n.", "def": "垄断；专营"},
            {"w": "last", "pos": "v.", "def": "持续"},
            {"w": "century", "pos": "n.", "def": "世纪"}
        ]
    },
    # Para 6
    {
        "id": 38,
        "para": 6,
        "en": "Then, in 1770, a Frenchman named Pierre Poivre successfully smuggled nutmeg plants to safety in Mauritius, an island off the coast of Africa.",
        "zh": "后来，1770年，一位名叫皮埃尔·普瓦夫尔的法国人成功地把肉豆蔻植株偷运到安全的毛里求斯——一座位于非洲海岸外的岛屿。",
        "grammar": {
            "type": "过去分词定语 + 同位语",
            "note": "named Pierre Poivre 为过去分词短语作定语修饰 a Frenchman；an island off the coast of Africa 为 Mauritius 的同位语；smuggle... to safety 意为 “把……偷运至安全处”。"
        },
        "words": [
            {"w": "smuggle", "pos": "v.", "def": "走私；偷运"},
            {"w": "to safety", "pos": "phr.", "def": "到安全的地方"},
            {"w": "off the coast of", "pos": "phr.", "def": "在……海岸外"}
        ]
    },
    {
        "id": 39,
        "para": 6,
        "en": "Some of these were later exported to the Caribbean where they thrived, especially on the island of Grenada.",
        "zh": "其中一些后来被出口到加勒比海地区，并在那里茁壮生长，尤其是在格林纳达岛上。",
        "grammar": {
            "type": "被动 + 定语从句",
            "note": "were later exported 为被动；where they thrived 为定语从句修饰 the Caribbean；thrive 意为 “繁茂、兴旺”。"
        },
        "words": [
            {"w": "Caribbean", "pos": "n.", "def": "加勒比海地区"},
            {"w": "thrive", "pos": "v.", "def": "茁壮成长；繁荣"}
        ]
    },
    {
        "id": 40,
        "para": 6,
        "en": "Next, in 1778, a volcanic eruption in the Banda region caused a tsunami that wiped out half the nutmeg groves.",
        "zh": "接着，1778年，班达地区的一次火山喷发引发了海啸，摧毁了半数的肉豆蔻林。",
        "grammar": {
            "type": "定语从句",
            "note": "that wiped out half the nutmeg groves 为定语从句修饰 a tsunami；wipe out 意为 “彻底摧毁、消灭”。"
        },
        "words": [
            {"w": "volcanic eruption", "pos": "phr.", "def": "火山喷发"},
            {"w": "tsunami", "pos": "n.", "def": "海啸"},
            {"w": "wipe out", "pos": "phr.", "def": "彻底摧毁；消灭"},
            {"w": "grove", "pos": "n.", "def": "小树林；果园"}
        ]
    },
    {
        "id": 41,
        "para": 6,
        "en": "Finally, in 1809, the British returned to Indonesia and seized the Banda Islands by force.",
        "zh": "最后，1809年，英国人重返印度尼西亚，以武力夺取了班达群岛。",
        "grammar": {
            "type": "并列谓语",
            "note": "returned 与 seized 为并列谓语；by force 意为 “以武力”；seize 意为 “夺取、抓住”。"
        },
        "words": [
            {"w": "return", "pos": "v.", "def": "返回"},
            {"w": "seize", "pos": "v.", "def": "夺取；抓住"},
            {"w": "by force", "pos": "phr.", "def": "以武力；强行"}
        ]
    },
    {
        "id": 42,
        "para": 6,
        "en": "They returned the islands to the Dutch in 1817, but not before transplanting hundreds of nutmeg seedlings to plantations in several locations across southern Asia.",
        "zh": "他们于1817年把这些岛屿归还给荷兰，但在此之前已先把数百株肉豆蔻幼苗移植到南亚多个地方的种植园中。",
        "grammar": {
            "type": "转折 + not before 结构",
            "note": "but not before transplanting... 意为 “但在……之前并非没有做（即先做了）”，强调移植发生在归还之前；transplanting 为动名词。"
        },
        "words": [
            {"w": "transplant", "pos": "v.", "def": "移植；迁移"},
            {"w": "location", "pos": "n.", "def": "地点；位置"},
            {"w": "southern", "pos": "adj.", "def": "南部的"}
        ]
    },
    {
        "id": 43,
        "para": 6,
        "en": "The Dutch nutmeg monopoly was over.",
        "zh": "荷兰人对肉豆蔻的垄断就此终结。",
        "grammar": {
            "type": "主系表",
            "note": "be over 意为 “结束、终止”。"
        },
        "words": [
            {"w": "over", "pos": "adj.", "def": "结束的；完结的"}
        ]
    },
    # Para 7
    {
        "id": 44,
        "para": 7,
        "en": "Today, nutmeg is grown in Indonesia, the Caribbean, India, Malaysia, Papua New Guinea and Sri Lanka, and world nutmeg production is estimated to average between 10,000 and 12,000 tonnes per year.",
        "zh": "如今，肉豆蔻种植于印度尼西亚、加勒比海地区、印度、马来西亚、巴布亚新几内亚和斯里兰卡，全球肉豆蔻年产量估计平均在1万到1.2万吨之间。",
        "grammar": {
            "type": "并列句 + 被动",
            "note": "and 连接两分句；is grown 与 is estimated 均为被动；be estimated to do 意为 “据估计……”；average 此处作动词 “平均为”。"
        },
        "words": [
            {"w": "estimate", "pos": "v.", "def": "估计；估算"},
            {"w": "average", "pos": "v.", "def": "平均为；平均达到"},
            {"w": "tonne", "pos": "n.", "def": "公吨（1000公斤）"}
        ]
    }
]

phrases = [
    {"w": "native to", "pos": "phr.", "def": "原产于；……的原生地"},
    {"w": "the former ... the latter", "pos": "phr.", "def": "前者……后者……"},
    {"w": "gain control of", "pos": "phr.", "def": "取得对……的控制"},
    {"w": "fall under", "pos": "phr.", "def": "落入（……的控制/统治）"},
    {"w": "lock out", "pos": "phr.", "def": "把……关在外面；排斥在外"},
    {"w": "fight back", "pos": "phr.", "def": "反击；还击"},
    {"w": "spare no expense", "pos": "phr.", "def": "不惜代价；不吝花费"},
    {"w": "take over", "pos": "phr.", "def": "接管；接手；占领"},
    {"w": "in turn", "pos": "phr.", "def": "作为回报；反过来"},
    {"w": "wipe out", "pos": "phr.", "def": "彻底摧毁；消灭"}
]

questions = [
    {
        "title": "Questions 1" + DASH + "4",
        "type": "note_completion",
        "instructions": [
            "Complete the notes below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 1" + DASH + "4 on your answer sheet.",
            "The nutmeg tree and fruit"
        ],
        "items": [
            {"number": 1, "prompt": "the leaves of the tree are __________ in shape", "answer": "oval", "evidence_sentence": 3},
            {"number": 2, "prompt": "the __________ surrounds the fruit and breaks open when the fruit is ripe", "answer": "husk", "evidence_sentence": 5},
            {"number": 3, "prompt": "the __________ is used to produce the spice nutmeg", "answer": "seed", "evidence_sentence": 7},
            {"number": 4, "prompt": "the covering known as the aril is used to produce __________", "answer": "mace", "evidence_sentence": 7}
        ]
    },
    {
        "title": "Questions 5" + DASH + "7",
        "type": "true_false_notgiven",
        "instructions": [
            "Do the following statements agree with the information given in Reading Passage 1?",
            "In boxes 5" + DASH + "7 on your answer sheet, write",
            "TRUE if the statement agrees with the information",
            "FALSE if the statement contradicts the information",
            "NOT GIVEN if there is no information on this"
        ],
        "items": [
            {"number": 5, "prompt": "In the Middle Ages, most Europeans knew where nutmeg was grown.", "answer": "FALSE", "evidence_sentence": 10},
            {"number": 6, "prompt": "The VOC was the world" + RSQUO + "s first major trading company.", "answer": "NOT GIVEN", "evidence_sentence": 17},
            {"number": 7, "prompt": "Following the Treaty of Breda, the Dutch had control of all the islands where nutmeg grew.", "answer": "TRUE", "evidence_sentence": 37}
        ]
    },
    {
        "title": "Questions 8" + DASH + "13",
        "type": "table_completion",
        "instructions": [
            "Complete the table below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 8" + DASH + "13 on your answer sheet."
        ],
        "items": [
            {"number": 8, "prompt": "Middle Ages: Nutmeg was brought to Europe by the __________", "answer": "Arabs", "evidence_sentence": 9},
            {"number": 9, "prompt": "17th century: Demand for nutmeg grew, as it was believed to be effective against the disease known as the __________", "answer": "plague", "evidence_sentence": 20},
            {"number": 10, "prompt": "The Dutch put __________ on nutmeg to avoid it being cultivated outside the islands", "answer": "lime", "evidence_sentence": 31},
            {"number": 11, "prompt": "The Dutch finally obtained the island of __________ from the British", "answer": "Run", "evidence_sentence": 35},
            {"number": 12, "prompt": "Late 18th century: 1770 " + DASH + " nutmeg plants were secretly taken to __________", "answer": "Mauritius", "evidence_sentence": 38},
            {"number": 13, "prompt": "1778 " + DASH + " half the Banda Islands" + RSQUO + " nutmeg plantations were destroyed by a __________", "answer": "tsunami", "evidence_sentence": 40}
        ]
    }
]

data = {
    "id": "c15-test1-p1",
    "source": "剑桥雅思15 Test 1 Passage 1",
    "title": "Nutmeg " + DASH + " a valuable spice",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c15-test1-p1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
