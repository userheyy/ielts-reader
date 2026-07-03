# -*- coding: utf-8 -*-
"""Generate data/passages/c15-test4-p2.json (Silbo Gomero - the whistle 'language' of the Canary Islands)."""
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
        "en": "La Gomera is one of the Canary Islands situated in the Atlantic Ocean off the northwest coast of Africa.",
        "zh": "拉戈梅拉是加那利群岛之一，位于非洲西北海岸外的大西洋中。",
        "grammar": {
            "type": "过去分词定语",
            "note": "situated in the Atlantic Ocean off the northwest coast of Africa 为过去分词短语作定语修饰 the Canary Islands；off the coast of 意为 “在……海岸外”。"
        },
        "words": [
            {"w": "the Canary Islands", "pos": "phr.", "def": "加那利群岛"},
            {"w": "situated", "pos": "adj.", "def": "位于……的"},
            {"w": "off the coast of", "pos": "phr.", "def": "在……海岸外"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "This small volcanic island is mountainous, with steep rocky slopes and deep, wooded ravines, rising to 1,487 metres at its highest peak.",
        "zh": "这座火山小岛多山，有陡峭的岩石斜坡和幽深、林木茂密的峡谷，最高峰海拔达1487米。",
        "grammar": {
            "type": "with 复合结构 + 现在分词状语",
            "note": "with steep rocky slopes and deep, wooded ravines 为 with 复合结构；rising to 1,487 metres at its highest peak 为现在分词短语作伴随状语；wooded 意为 “林木茂密的”。"
        },
        "words": [
            {"w": "volcanic", "pos": "adj.", "def": "火山的"},
            {"w": "mountainous", "pos": "adj.", "def": "多山的"},
            {"w": "slope", "pos": "n.", "def": "斜坡"},
            {"w": "ravine", "pos": "n.", "def": "峡谷；沟壑"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "It is also home to the best known of the world" + RSQUO + "s whistle " + LSQUO + "languages" + RSQUO + ", a means of transmitting information over long distances which is perfectly adapted to the extreme terrain of the island.",
        "zh": "它也是世界上最著名的哨语的发源地——这是一种远距离传递信息的方式，完美适应了岛上极端的地形。",
        "grammar": {
            "type": "同位语 + 定语从句",
            "note": "a means of transmitting information over long distances 为前面 whistle 'languages' 的同位语；which is perfectly adapted to... 为定语从句修饰 a means；be home to 意为 “是……的所在地”；be adapted to 意为 “适应”。"
        },
        "words": [
            {"w": "be home to", "pos": "phr.", "def": "是……的所在地/发源地"},
            {"w": "whistle", "pos": "n.", "def": "口哨；哨声"},
            {"w": "a means of", "pos": "phr.", "def": "一种……的方式"},
            {"w": "terrain", "pos": "n.", "def": "地形；地势"}
        ]
    },
    # Para 2
    {
        "id": 4,
        "para": 2,
        "en": "This " + LSQUO + "language" + RSQUO + ", known as " + LSQUO + "Silbo" + RSQUO + " or " + LSQUO + "Silbo Gomero" + RSQUO + " " + DASH + " from the Spanish word for " + LSQUO + "whistle" + RSQUO + " " + DASH + " is now shedding light on the language-processing abilities of the human brain, according to scientists.",
        "zh": "据科学家称，这种被称为“Silbo”或“Silbo Gomero”的“语言”——名称源自西班牙语中表示“口哨”的词——如今正在揭示人脑的语言处理能力。",
        "grammar": {
            "type": "过去分词定语 + 破折号插入",
            "note": "known as 'Silbo' or 'Silbo Gomero' 为过去分词短语作定语；两破折号间为对名称来源的插入说明；shed light on 意为 “揭示、阐明”；according to 意为 “据……所说”。"
        },
        "words": [
            {"w": "known as", "pos": "phr.", "def": "被称为"},
            {"w": "shed light on", "pos": "phr.", "def": "揭示；阐明"},
            {"w": "language-processing", "pos": "adj.", "def": "语言处理的"},
            {"w": "ability", "pos": "n.", "def": "能力"}
        ]
    },
    {
        "id": 5,
        "para": 2,
        "en": "Researchers say that Silbo activates parts of the brain normally associated with spoken language, suggesting that the brain is remarkably flexible in its ability to interpret sounds as language.",
        "zh": "研究人员称，Silbo 会激活大脑中通常与口语相关的部分，这表明大脑在把声音解读为语言的能力上具有非凡的灵活性。",
        "grammar": {
            "type": "宾语从句 + 现在分词状语",
            "note": "say that Silbo activates... 为宾语从句；normally associated with spoken language 为过去分词短语作定语修饰 parts；suggesting that... 为现在分词短语作结果状语；interpret A as B 意为 “把 A 解读为 B”。"
        },
        "words": [
            {"w": "activate", "pos": "v.", "def": "激活；使活跃"},
            {"w": "be associated with", "pos": "phr.", "def": "与……相关联"},
            {"w": "flexible", "pos": "adj.", "def": "灵活的"},
            {"w": "interpret", "pos": "v.", "def": "解读；理解"}
        ]
    },
    # Para 3
    {
        "id": 6,
        "para": 3,
        "en": LSQUO + "Science has developed the idea of brain areas that are dedicated to language, and we are starting to understand the scope of signals that can be recognised as language," + RSQUO + " says David Corina, co-author of a recent study and associate professor of psychology at the University of Washington in Seattle.",
        "zh": "“科学已经提出了专司语言的脑区这一概念，而我们正开始理解哪些信号能够被识别为语言的范围，”戴维·科里纳说，他是近期一项研究的合著者、西雅图华盛顿大学心理学副教授。",
        "grammar": {
            "type": "定语从句 + 同位语",
            "note": "that are dedicated to language 为定语从句修饰 brain areas；that can be recognised as language 为定语从句修饰 signals；co-author... and associate professor... 为 David Corina 的同位语；be dedicated to 意为 “专用于”。"
        },
        "words": [
            {"w": "be dedicated to", "pos": "phr.", "def": "专用于；致力于"},
            {"w": "scope", "pos": "n.", "def": "范围"},
            {"w": "signal", "pos": "n.", "def": "信号"},
            {"w": "recognise as", "pos": "phr.", "def": "把……识别/认作"}
        ]
    },
    # Para 4
    {
        "id": 7,
        "para": 4,
        "en": "Silbo is a substitute for Spanish, with individual words recoded into whistles which have high- and low-frequency tones.",
        "zh": "Silbo 是西班牙语的一种替代形式，其中单个词被重新编码为具有高频和低频音调的哨声。",
        "grammar": {
            "type": "with 复合结构 + 定语从句",
            "note": "with individual words recoded into whistles 为 with 复合结构（含过去分词 recoded）；which have high- and low-frequency tones 为定语从句修饰 whistles；a substitute for 意为 “……的替代品”。"
        },
        "words": [
            {"w": "substitute for", "pos": "phr.", "def": "……的替代品"},
            {"w": "individual", "pos": "adj.", "def": "单个的；个别的"},
            {"w": "recode", "pos": "v.", "def": "重新编码"},
            {"w": "frequency", "pos": "n.", "def": "频率"}
        ]
    },
    {
        "id": 8,
        "para": 4,
        "en": "A whistler " + DASH + " or silbador " + DASH + " puts a finger in his or her mouth to increase the whistle" + RSQUO + "s pitch, while the other hand can be cupped to adjust the direction of the sound.",
        "zh": "吹哨者——即 silbador——把一根手指放进嘴里以提高哨声的音调，同时另一只手可以拢成杯状来调节声音的方向。",
        "grammar": {
            "type": "破折号同位 + while 伴随",
            "note": "两破折号间 or silbador 为 A whistler 的同位语；to increase the whistle's pitch 为目的状语；while the other hand can be cupped to... 为 while 引导的伴随状语从句；cup 此处作动词 “使成杯状”。"
        },
        "words": [
            {"w": "whistler", "pos": "n.", "def": "吹哨者"},
            {"w": "finger", "pos": "n.", "def": "手指"},
            {"w": "pitch", "pos": "n.", "def": "音高；音调"},
            {"w": "cup", "pos": "v.", "def": "使成杯状；拢起"}
        ]
    },
    {
        "id": 9,
        "para": 4,
        "en": LSQUO + "There is much more ambiguity in the whistled signal than in the spoken signal," + RSQUO + " explains lead researcher Manuel Carreiras, psychology professor at the University of La Laguna on the Canary island of Tenerife.",
        "zh": "“哨声信号比口语信号含有多得多的歧义，”首席研究员曼努埃尔·卡雷拉斯解释道，他是加那利群岛特内里费岛拉拉古纳大学的心理学教授。",
        "grammar": {
            "type": "比较结构 + 同位语",
            "note": "much more ambiguity... than in the spoken signal 为比较结构；psychology professor at... 为 Manuel Carreiras 的同位语；ambiguity 意为 “歧义、模糊”。"
        },
        "words": [
            {"w": "ambiguity", "pos": "n.", "def": "歧义；模糊"},
            {"w": "whistled", "pos": "adj.", "def": "用口哨吹出的"},
            {"w": "lead researcher", "pos": "phr.", "def": "首席研究员"},
            {"w": "professor", "pos": "n.", "def": "教授"}
        ]
    },
    {
        "id": 10,
        "para": 4,
        "en": "Because whistled " + LSQUO + "words" + RSQUO + " can be hard to distinguish, silbadores rely on repetition, as well as awareness of context, to make themselves understood.",
        "zh": "由于哨声“词语”可能很难分辨，silbador 们依靠重复以及对语境的把握来让别人听懂自己的意思。",
        "grammar": {
            "type": "原因状语从句 + as well as",
            "note": "Because whistled 'words' can be hard to distinguish 为原因状语从句；rely on repetition, as well as awareness of context 为 “A as well as B” 并列宾语；to make themselves understood 为目的状语，make oneself understood 意为 “让别人明白自己”。"
        },
        "words": [
            {"w": "distinguish", "pos": "v.", "def": "区分；分辨"},
            {"w": "rely on", "pos": "phr.", "def": "依靠；依赖"},
            {"w": "repetition", "pos": "n.", "def": "重复"},
            {"w": "context", "pos": "n.", "def": "语境；上下文"}
        ]
    },
    # Para 5
    {
        "id": 11,
        "para": 5,
        "en": "The silbadores of Gomera are traditionally shepherds and other isolated mountain folk, and their novel means of staying in touch allows them to communicate over distances of up to 10 kilometres.",
        "zh": "戈梅拉的 silbador 们传统上是牧羊人和其他与世隔绝的山地居民，他们这种新奇的联络方式使他们能够在远达10公里的距离上进行交流。",
        "grammar": {
            "type": "并列句",
            "note": "and 连接两分句；their novel means of staying in touch 为主语（of doing 作定语）；allow sb to do 意为 “使某人能够做”；up to 意为 “多达、高达”。"
        },
        "words": [
            {"w": "shepherd", "pos": "n.", "def": "牧羊人"},
            {"w": "isolated", "pos": "adj.", "def": "与世隔绝的；孤立的"},
            {"w": "stay in touch", "pos": "phr.", "def": "保持联系"},
            {"w": "up to", "pos": "phr.", "def": "多达；高达"}
        ]
    },
    {
        "id": 12,
        "para": 5,
        "en": "Carreiras explains that silbadores are able to pass a surprising amount of information via their whistles.",
        "zh": "卡雷拉斯解释说，silbador 们能够通过哨声传递数量惊人的信息。",
        "grammar": {
            "type": "宾语从句",
            "note": "explains that... 后接宾语从句；be able to do 意为 “能够做”；via 意为 “通过、借助”；a surprising amount of 意为 “数量惊人的”。"
        },
        "words": [
            {"w": "pass", "pos": "v.", "def": "传递；传送"},
            {"w": "via", "pos": "prep.", "def": "通过；经由"},
            {"w": "amount", "pos": "n.", "def": "数量"}
        ]
    },
    {
        "id": 13,
        "para": 5,
        "en": LSQUO + "In daily life they use whistles to communicate short commands, but any Spanish sentence could be whistled." + RSQUO,
        "zh": "“在日常生活中，他们用哨声传达简短的指令，但任何西班牙语句子都可以用哨声吹出来。”",
        "grammar": {
            "type": "转折并列句",
            "note": "but 连接转折两分句；use whistles to communicate short commands 中不定式作目的状语；any Spanish sentence could be whistled 为被动；command 意为 “指令、命令”。"
        },
        "words": [
            {"w": "daily life", "pos": "phr.", "def": "日常生活"},
            {"w": "communicate", "pos": "v.", "def": "传达；交流"},
            {"w": "command", "pos": "n.", "def": "指令；命令"},
            {"w": "sentence", "pos": "n.", "def": "句子"}
        ]
    },
    {
        "id": 14,
        "para": 5,
        "en": "Silbo has proved particularly useful when fires have occurred on the island and rapid communication across large areas has been vital.",
        "zh": "当岛上发生火灾、需要在大范围内快速沟通时，Silbo 已被证明尤为有用。",
        "grammar": {
            "type": "时间状语从句",
            "note": "when fires have occurred... and rapid communication... has been vital 为时间状语从句（并列谓语）；prove + 形容词 表 “被证明是”；particularly 意为 “尤其”。"
        },
        "words": [
            {"w": "prove", "pos": "v.", "def": "证明是；结果是"},
            {"w": "occur", "pos": "v.", "def": "发生"},
            {"w": "rapid", "pos": "adj.", "def": "快速的"},
            {"w": "vital", "pos": "adj.", "def": "至关重要的"}
        ]
    },
    # Para 6
    {
        "id": 15,
        "para": 6,
        "en": "The study team used neuroimaging equipment to contrast the brain activity of silbadores while listening to whistled and spoken Spanish.",
        "zh": "研究团队使用神经成像设备，对比了 silbador 们在听哨语西班牙语和口语西班牙语时的大脑活动。",
        "grammar": {
            "type": "不定式目的 + 省略状语从句",
            "note": "to contrast the brain activity... 为目的状语；while listening to... 为省略主谓的时间状语从句（=while they were listening to...）；neuroimaging 意为 “神经成像”。"
        },
        "words": [
            {"w": "neuroimaging", "pos": "n.", "def": "神经成像"},
            {"w": "equipment", "pos": "n.", "def": "设备"},
            {"w": "contrast", "pos": "v.", "def": "对比"},
            {"w": "activity", "pos": "n.", "def": "活动"}
        ]
    },
    {
        "id": 16,
        "para": 6,
        "en": "Results showed the left temporal lobe of the brain, which is usually associated with spoken language, was engaged during the processing of Silbo.",
        "zh": "结果表明，通常与口语相关的大脑左颞叶在处理 Silbo 时被调动了起来。",
        "grammar": {
            "type": "宾语从句 + 非限定性定语从句",
            "note": "showed (that) the left temporal lobe... was engaged... 为省略连词的宾语从句；which is usually associated with spoken language 为非限定性定语从句；be engaged 意为 “被调动、参与其中”。"
        },
        "words": [
            {"w": "temporal lobe", "pos": "phr.", "def": "颞叶"},
            {"w": "be engaged", "pos": "phr.", "def": "被调动；参与"},
            {"w": "processing", "pos": "n.", "def": "处理；加工"}
        ]
    },
    {
        "id": 17,
        "para": 6,
        "en": "The researchers found that other key regions in the brain" + RSQUO + "s frontal lobe also responded to the whistles, including those activated in response to sign language among deaf people.",
        "zh": "研究人员发现，大脑额叶中其他一些关键区域也对哨声作出了反应，其中包括聋人在使用手语时被激活的那些区域。",
        "grammar": {
            "type": "宾语从句 + 过去分词定语",
            "note": "found that other key regions... also responded... 为宾语从句；including those activated in response to... 为现在分词短语作补充，activated 为过去分词修饰 those；respond to 意为 “对……作出反应”。"
        },
        "words": [
            {"w": "region", "pos": "n.", "def": "区域"},
            {"w": "frontal lobe", "pos": "phr.", "def": "额叶"},
            {"w": "respond to", "pos": "phr.", "def": "对……作出反应"},
            {"w": "sign language", "pos": "phr.", "def": "手语"}
        ]
    },
    {
        "id": 18,
        "para": 6,
        "en": "When the experiments were repeated with non-whistlers, however, activation was observed in all areas of the brain.",
        "zh": "然而，当这些实验在不会吹哨的人身上重复进行时，大脑所有区域都观察到了激活现象。",
        "grammar": {
            "type": "时间状语从句 + 被动",
            "note": "When the experiments were repeated with non-whistlers 为时间状语从句（被动）；主句 activation was observed... 为被动；however 为插入的转折词。"
        },
        "words": [
            {"w": "experiment", "pos": "n.", "def": "实验"},
            {"w": "repeat", "pos": "v.", "def": "重复"},
            {"w": "activation", "pos": "n.", "def": "激活"},
            {"w": "observe", "pos": "v.", "def": "观察到"}
        ]
    },
    # Para 7
    {
        "id": 19,
        "para": 7,
        "en": LSQUO + "Our results provide more evidence about the flexibility of human capacity for language in a variety of forms," + RSQUO + " Corina says.",
        "zh": "“我们的结果为人类以多种形式运用语言的能力之灵活性提供了更多证据，”科里纳说。",
        "grammar": {
            "type": "简单句",
            "note": "provide evidence about 意为 “提供关于……的证据”；the flexibility of human capacity for language 为多层名词短语；in a variety of forms 意为 “以多种形式”。"
        },
        "words": [
            {"w": "evidence", "pos": "n.", "def": "证据"},
            {"w": "flexibility", "pos": "n.", "def": "灵活性"},
            {"w": "capacity", "pos": "n.", "def": "能力；容量"}
        ]
    },
    {
        "id": 20,
        "para": 7,
        "en": LSQUO + "These data suggest that left-hemisphere language regions are uniquely adapted for communicative purposes, independent of the modality of signal.",
        "zh": "“这些数据表明，左半球的语言区域独特地适应于交流目的，而与信号的形式无关。",
        "grammar": {
            "type": "宾语从句 + 形容词短语状语",
            "note": "suggest that left-hemisphere language regions are uniquely adapted... 为宾语从句；independent of the modality of signal 为形容词短语作状语；be adapted for 意为 “适应于”；modality 意为 “形式、模态”。"
        },
        "words": [
            {"w": "data", "pos": "n.", "def": "数据"},
            {"w": "hemisphere", "pos": "n.", "def": "（大脑）半球"},
            {"w": "communicative", "pos": "adj.", "def": "交流的；沟通的"},
            {"w": "modality", "pos": "n.", "def": "形式；模态"}
        ]
    },
    {
        "id": 21,
        "para": 7,
        "en": "The non-Silbo speakers were not recognising Silbo as a language. They had nothing to grab onto, so multiple areas of their brains were activated." + RSQUO,
        "zh": "不会 Silbo 的人并没有把 Silbo 当作一种语言来识别。他们没有任何可以抓住的东西，所以他们大脑的多个区域都被激活了。”",
        "grammar": {
            "type": "结果状语",
            "note": "recognise A as B 意为 “把 A 认作 B”；nothing to grab onto 中不定式作定语；so multiple areas... were activated 为结果分句；grab onto 意为 “抓住、依附”。"
        },
        "words": [
            {"w": "recognise as", "pos": "phr.", "def": "把……认作"},
            {"w": "grab onto", "pos": "phr.", "def": "抓住；依附"},
            {"w": "multiple", "pos": "adj.", "def": "多个的；多重的"}
        ]
    },
    # Para 8
    {
        "id": 22,
        "para": 8,
        "en": "Carreiras says the origins of Silbo Gomero remain obscure, but that indigenous Canary Islanders, who were of North African origin, already had a whistled language when Spain conquered the volcanic islands in the 15th century.",
        "zh": "卡雷拉斯说，Silbo Gomero 的起源仍不清楚，但当西班牙在15世纪征服这些火山群岛时，原为北非血统的加那利群岛原住民就已经拥有一种哨语了。",
        "grammar": {
            "type": "并列宾语从句 + 非限定性定语从句",
            "note": "says (that) the origins... remain obscure, but that indigenous Canary Islanders... already had... 为并列宾语从句；who were of North African origin 为非限定性定语从句；when Spain conquered... 为时间状语从句；remain 意为 “仍然是”。"
        },
        "words": [
            {"w": "origin", "pos": "n.", "def": "起源；出身"},
            {"w": "obscure", "pos": "adj.", "def": "不清楚的；模糊的"},
            {"w": "indigenous", "pos": "adj.", "def": "本土的；原住民的"},
            {"w": "conquer", "pos": "v.", "def": "征服"}
        ]
    },
    {
        "id": 23,
        "para": 8,
        "en": "Whistled languages survive today in Papua New Guinea, Mexico, Vietnam, Guyana, China, Nepal, Senegal, and a few mountainous pockets in southern Europe.",
        "zh": "如今，哨语仍存续于巴布亚新几内亚、墨西哥、越南、圭亚那、中国、尼泊尔、塞内加尔以及南欧少数几个多山的地区。",
        "grammar": {
            "type": "简单句",
            "note": "survive 此处作 “存续、留存” 讲；a few mountainous pockets 意为 “少数几个多山的小块地区”，pocket 引申为 “小块区域”。"
        },
        "words": [
            {"w": "survive", "pos": "v.", "def": "存续；幸存"},
            {"w": "mountainous", "pos": "adj.", "def": "多山的"},
            {"w": "pocket", "pos": "n.", "def": "小块地区；孤立小区域"}
        ]
    },
    {
        "id": 24,
        "para": 8,
        "en": "There are thought to be as many as 70 whistled languages still in use, though only 12 have been described and studied scientifically.",
        "zh": "据认为，仍在使用的哨语多达70种，尽管其中只有12种得到了科学的描述和研究。",
        "grammar": {
            "type": "被动 + 让步状语从句",
            "note": "There are thought to be... 为 “被认为存在……” 的被动结构；as many as 70 意为 “多达70”；though only 12 have been... 为让步状语从句；in use 意为 “在使用中”。"
        },
        "words": [
            {"w": "as many as", "pos": "phr.", "def": "多达"},
            {"w": "in use", "pos": "phr.", "def": "在使用中"},
            {"w": "describe", "pos": "v.", "def": "描述"},
            {"w": "scientifically", "pos": "adv.", "def": "科学地"}
        ]
    },
    {
        "id": 25,
        "para": 8,
        "en": "This form of communication is an adaptation found among cultures where people are often isolated from each other, according to Julien Meyer, a researcher at the Institute of Human Sciences in Lyon, France.",
        "zh": "据法国里昂人文科学研究所的研究员朱利安·迈耶所说，这种交流形式是一种在人们常常彼此隔绝的文化中出现的适应性产物。",
        "grammar": {
            "type": "过去分词定语 + 定语从句 + 同位语",
            "note": "found among cultures... 为过去分词短语作定语修饰 an adaptation；where people are often isolated from each other 为定语从句修饰 cultures；a researcher at... 为 Julien Meyer 的同位语；be isolated from 意为 “与……隔绝”。"
        },
        "words": [
            {"w": "adaptation", "pos": "n.", "def": "适应；适应性产物"},
            {"w": "culture", "pos": "n.", "def": "文化"},
            {"w": "be isolated from", "pos": "phr.", "def": "与……隔绝"},
            {"w": "institute", "pos": "n.", "def": "研究所；学院"}
        ]
    },
    {
        "id": 26,
        "para": 8,
        "en": LSQUO + "They are mostly used in mountains or dense forests," + RSQUO + " he says. " + LSQUO + "Whistled languages are quite clearly defined and represent an original adaptation of the spoken language for the needs of isolated human groups." + RSQUO,
        "zh": "“它们大多用于山区或茂密的森林中，”他说。“哨语有着相当清晰的界定，代表了口语为适应与世隔绝的人群的需求而进行的一种独创性演变。”",
        "grammar": {
            "type": "并列谓语 + 被动",
            "note": "are quite clearly defined and represent... 为并列谓语，前者为被动；an original adaptation of... for... 意为 “……为……而作的独创性演变”；dense 意为 “茂密的”。"
        },
        "words": [
            {"w": "dense", "pos": "adj.", "def": "茂密的；密集的"},
            {"w": "define", "pos": "v.", "def": "界定；定义"},
            {"w": "represent", "pos": "v.", "def": "代表；体现"},
            {"w": "original", "pos": "adj.", "def": "独创的；最初的"}
        ]
    },
    # Para 9
    {
        "id": 27,
        "para": 9,
        "en": "But with modern communication technology now widely available, researchers say whistled languages like Silbo are threatened with extinction.",
        "zh": "但随着现代通信技术如今的广泛普及，研究人员表示，像 Silbo 这样的哨语正面临灭绝的威胁。",
        "grammar": {
            "type": "with 独立主格 + 宾语从句",
            "note": "with modern communication technology now widely available 为 with 独立主格结构作状语；say (that) whistled languages... are threatened... 为省略连词的宾语从句；be threatened with 意为 “受到……的威胁”。"
        },
        "words": [
            {"w": "technology", "pos": "n.", "def": "技术"},
            {"w": "available", "pos": "adj.", "def": "可获得的；普及的"},
            {"w": "be threatened with", "pos": "phr.", "def": "受到……的威胁"},
            {"w": "extinction", "pos": "n.", "def": "灭绝"}
        ]
    },
    {
        "id": 28,
        "para": 9,
        "en": "With dwindling numbers of Gomera islanders still fluent in the language, Canaries" + RSQUO + " authorities are taking steps to try to ensure its survival.",
        "zh": "由于仍能流利使用这种语言的戈梅拉岛民人数日益减少，加那利群岛当局正采取措施，努力确保它的存续。",
        "grammar": {
            "type": "with 独立主格 + 不定式目的",
            "note": "With dwindling numbers of Gomera islanders still fluent... 为 with 独立主格结构；take steps to do 意为 “采取措施做”；to try to ensure its survival 为目的状语；dwindling 意为 “日益减少的”。"
        },
        "words": [
            {"w": "dwindling", "pos": "adj.", "def": "日益减少的"},
            {"w": "fluent", "pos": "adj.", "def": "流利的"},
            {"w": "authority", "pos": "n.", "def": "当局；官方"},
            {"w": "take steps", "pos": "phr.", "def": "采取措施"}
        ]
    },
    {
        "id": 29,
        "para": 9,
        "en": "Since 1999, Silbo Gomero has been taught in all of the island" + RSQUO + "s elementary schools.",
        "zh": "自1999年以来，Silbo Gomero 已在该岛所有的小学中教授。",
        "grammar": {
            "type": "现在完成时被动",
            "note": "has been taught 为现在完成时被动，与 Since 1999 呼应；elementary school 意为 “小学”。"
        },
        "words": [
            {"w": "teach", "pos": "v.", "def": "教授"},
            {"w": "elementary school", "pos": "phr.", "def": "小学"}
        ]
    },
    {
        "id": 30,
        "para": 9,
        "en": "In addition, locals are seeking assistance from the United Nations Educational, Scientific and Cultural Organization (UNESCO).",
        "zh": "此外，当地人正在向联合国教育、科学及文化组织（联合国教科文组织）寻求援助。",
        "grammar": {
            "type": "简单句",
            "note": "seek assistance from 意为 “向……寻求援助”；In addition 意为 “此外”；括号内为 UNESCO 的全称说明。"
        },
        "words": [
            {"w": "in addition", "pos": "phr.", "def": "此外"},
            {"w": "seek", "pos": "v.", "def": "寻求"},
            {"w": "assistance", "pos": "n.", "def": "援助；帮助"},
            {"w": "organization", "pos": "n.", "def": "组织；机构"}
        ]
    },
    {
        "id": 31,
        "para": 9,
        "en": LSQUO + "The local authorities are trying to get an award from the organisation to declare [Silbo Gomero] as something that should be preserved for humanity," + RSQUO + " Carreiras adds.",
        "zh": "“当地当局正试图从该组织获得一项认定，把（Silbo Gomero）宣布为一种应当为全人类保护的事物，”卡雷拉斯补充道。",
        "grammar": {
            "type": "不定式目的 + 定语从句",
            "note": "to get an award... to declare... 为连续的不定式作目的状语；that should be preserved for humanity 为定语从句修饰 something；declare A as B 意为 “把 A 宣布为 B”。"
        },
        "words": [
            {"w": "award", "pos": "n.", "def": "奖项；认定"},
            {"w": "declare", "pos": "v.", "def": "宣布；宣告"},
            {"w": "preserve", "pos": "v.", "def": "保护；保存"},
            {"w": "humanity", "pos": "n.", "def": "人类；全人类"}
        ]
    }
]

phrases = [
    {"w": "off the coast of", "pos": "phr.", "def": "在……海岸外"},
    {"w": "be home to", "pos": "phr.", "def": "是……的所在地/发源地"},
    {"w": "shed light on", "pos": "phr.", "def": "揭示；阐明"},
    {"w": "be associated with", "pos": "phr.", "def": "与……相关联"},
    {"w": "be dedicated to", "pos": "phr.", "def": "专用于；致力于"},
    {"w": "rely on", "pos": "phr.", "def": "依靠；依赖"},
    {"w": "stay in touch", "pos": "phr.", "def": "保持联系"},
    {"w": "respond to", "pos": "phr.", "def": "对……作出反应"},
    {"w": "as many as", "pos": "phr.", "def": "多达"},
    {"w": "take steps", "pos": "phr.", "def": "采取措施"}
]

questions = [
    {
        "title": "Questions 14" + DASH + "19",
        "type": "true_false_notgiven",
        "instructions": [
            "Do the following statements agree with the information given in Reading Passage 2?",
            "In boxes 14" + DASH + "19 on your answer sheet, write",
            "TRUE if the statement agrees with the information",
            "FALSE if the statement contradicts the information",
            "NOT GIVEN if there is no information on this"
        ],
        "items": [
            {"number": 14, "prompt": "La Gomera is the most mountainous of all the Canary Islands.", "answer": "NOT GIVEN", "evidence_sentence": 2},
            {"number": 15, "prompt": "Silbo is only appropriate for short and simple messages.", "answer": "FALSE", "evidence_sentence": 13},
            {"number": 16, "prompt": "In the brain-activity study, silbadores and non-whistlers produced different results.", "answer": "TRUE", "evidence_sentence": 18},
            {"number": 17, "prompt": "The Spanish introduced Silbo to the islands in the 15th century.", "answer": "FALSE", "evidence_sentence": 22},
            {"number": 18, "prompt": "There is precise data available regarding all of the whistle languages in existence today.", "answer": "FALSE", "evidence_sentence": 24},
            {"number": 19, "prompt": "The children of Gomera now learn Silbo.", "answer": "TRUE", "evidence_sentence": 29}
        ]
    },
    {
        "title": "Questions 20" + DASH + "26",
        "type": "note_completion",
        "instructions": [
            "Complete the notes below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 20" + DASH + "26 on your answer sheet.",
            "Silbo Gomero"
        ],
        "items": [
            {"number": 20, "prompt": "How Silbo is produced: high- and low-frequency tones represent different sounds in Spanish __________", "answer": "words", "evidence_sentence": 7},
            {"number": 21, "prompt": "pitch of whistle is controlled using silbador" + RSQUO + "s __________", "answer": "finger", "evidence_sentence": 8},
            {"number": 22, "prompt": "__________ is changed with a cupped hand", "answer": "direction", "evidence_sentence": 8},
            {"number": 23, "prompt": "How Silbo is used: in everyday use for the transmission of brief __________", "answer": "commands", "evidence_sentence": 13},
            {"number": 24, "prompt": "can relay essential information quickly, e.g. to inform people about __________", "answer": "fires", "evidence_sentence": 14},
            {"number": 25, "prompt": "The future of Silbo: future under threat because of new __________", "answer": "technology", "evidence_sentence": 27},
            {"number": 26, "prompt": "Canaries" + RSQUO + " authorities hoping to receive a UNESCO __________ to help preserve it", "answer": "award", "evidence_sentence": 31}
        ]
    }
]

data = {
    "id": "c15-test4-p2",
    "source": "剑桥雅思15 Test 4 Passage 2",
    "title": "Silbo Gomero " + DASH + " the whistle " + LSQUO + "language" + RSQUO + " of the Canary Islands",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c15-test4-p2.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
