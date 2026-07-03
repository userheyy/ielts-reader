# -*- coding: utf-8 -*-
"""Generate data/passages/c15-test3-p3.json (Why fairy tales are really scary tales)."""
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
        "en": "People of every culture tell each other fairy tales but the same story often takes a variety of forms in different parts of the world.",
        "zh": "每种文化的人都会互相讲述童话故事，但同一个故事在世界不同地区往往会有多种形式。",
        "grammar": {
            "type": "转折并列句",
            "note": "but 连接转折两分句；take a variety of forms 意为 “呈现多种形式”；of every culture 为介词短语作定语。"
        },
        "words": [
            {"w": "fairy tale", "pos": "phr.", "def": "童话故事"},
            {"w": "a variety of", "pos": "phr.", "def": "各种各样的"},
            {"w": "form", "pos": "n.", "def": "形式；样式"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "In the story of Little Red Riding Hood that European children are familiar with, a young girl on the way to see her grandmother meets a wolf and tells him where she is going.",
        "zh": "在欧洲儿童熟悉的《小红帽》故事里，一个小女孩在去看外婆的路上遇到一只狼，并告诉它自己要去哪里。",
        "grammar": {
            "type": "定语从句 + 并列谓语",
            "note": "that European children are familiar with 为定语从句修饰 the story；on the way to see her grandmother 为介词短语作定语修饰 a young girl；meets... and tells... 为并列谓语；where she is going 为宾语从句。"
        },
        "words": [
            {"w": "be familiar with", "pos": "phr.", "def": "熟悉"},
            {"w": "on the way to", "pos": "phr.", "def": "在去……的路上"},
            {"w": "wolf", "pos": "n.", "def": "狼"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "The wolf runs on ahead and disposes of the grandmother, then gets into bed dressed in the grandmother" + RSQUO + "s clothes to wait for Little Red Riding Hood.",
        "zh": "狼抢先跑到前面除掉了外婆，然后穿上外婆的衣服躺进床里，等待小红帽的到来。",
        "grammar": {
            "type": "并列谓语 + 过去分词状语",
            "note": "runs on ahead and disposes of..., then gets into bed... 为并列谓语；dressed in the grandmother's clothes 为过去分词短语作状语；to wait for... 为目的状语；dispose of 意为 “除掉、处理”。"
        },
        "words": [
            {"w": "run on ahead", "pos": "phr.", "def": "抢先跑到前面"},
            {"w": "dispose of", "pos": "phr.", "def": "除掉；处理掉"},
            {"w": "dressed in", "pos": "phr.", "def": "穿着"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "You may think you know the story " + DASH + " but which version?",
        "zh": "你也许以为自己知道这个故事——但是哪个版本呢？",
        "grammar": {
            "type": "宾语从句 + 破折号反问",
            "note": "think (that) you know the story 为省略连词的宾语从句；破折号后 but which version? 为省略句式的反问，强调版本之多。"
        },
        "words": [
            {"w": "version", "pos": "n.", "def": "版本"},
            {"w": "may", "pos": "modal", "def": "也许；可能"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "In some versions, the wolf swallows up the grandmother, while in others it locks her in a cupboard.",
        "zh": "在有些版本里，狼把外婆整个吞了下去；而在另一些版本里，它把外婆锁进了柜子。",
        "grammar": {
            "type": "while 对比状语从句",
            "note": "while 引导对比状语从句；in some versions / in others 形成对照；swallow up 意为 “吞下”；lock... in 意为 “把……锁进”。"
        },
        "words": [
            {"w": "swallow up", "pos": "phr.", "def": "吞没；吞下"},
            {"w": "lock in", "pos": "phr.", "def": "把……锁在里面"},
            {"w": "cupboard", "pos": "n.", "def": "橱柜；碗柜"}
        ]
    },
    {
        "id": 6,
        "para": 1,
        "en": "In some stories Red Riding Hood gets the better of the wolf on her own, while in others a hunter or a woodcutter hears her cries and comes to her rescue.",
        "zh": "在有些故事里，小红帽独自战胜了狼；而在另一些故事里，一个猎人或樵夫听到她的呼喊，前来营救她。",
        "grammar": {
            "type": "while 对比状语从句",
            "note": "while 引导对比状语从句；get the better of 意为 “战胜、占上风”；on her own 意为 “独自”；come to one's rescue 意为 “前来营救”。"
        },
        "words": [
            {"w": "get the better of", "pos": "phr.", "def": "战胜；占上风"},
            {"w": "on one" + RSQUO + "s own", "pos": "phr.", "def": "独自；靠自己"},
            {"w": "woodcutter", "pos": "n.", "def": "樵夫；伐木工"},
            {"w": "come to one" + RSQUO + "s rescue", "pos": "phr.", "def": "前来营救"}
        ]
    },
    # Para 2
    {
        "id": 7,
        "para": 2,
        "en": "The universal appeal of these tales is frequently attributed to the idea that they contain cautionary messages: in the case of Little Red Riding Hood, to listen to your mother, and avoid talking to strangers.",
        "zh": "这些故事之所以具有普遍的吸引力，常被归因于它们蕴含警示性寓意这一观点：就《小红帽》而言，即要听妈妈的话、不要和陌生人说话。",
        "grammar": {
            "type": "被动 + 同位语从句 + 冒号说明",
            "note": "is attributed to 为被动；the idea that they contain... 中 that 引导同位语从句；冒号后为对 cautionary messages 的具体说明；be attributed to 意为 “归因于”。"
        },
        "words": [
            {"w": "universal", "pos": "adj.", "def": "普遍的"},
            {"w": "appeal", "pos": "n.", "def": "吸引力"},
            {"w": "be attributed to", "pos": "phr.", "def": "被归因于"},
            {"w": "cautionary", "pos": "adj.", "def": "警示的；劝诫的"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": LSQUO + "It might be what we find interesting about this story is that it" + RSQUO + "s got this survival-relevant information in it," + RSQUO + " says anthropologist Jamie Tehrani at Durham University in the UK.",
        "zh": "“我们觉得这个故事有趣的地方，或许正在于它包含了与生存相关的信息，”英国杜伦大学的人类学家杰米·特赫拉尼说。",
        "grammar": {
            "type": "主语从句 + 表语从句",
            "note": "what we find interesting about this story 为主语从句；is that it's got... 为表语从句；survival-relevant 意为 “与生存相关的”。"
        },
        "words": [
            {"w": "anthropologist", "pos": "n.", "def": "人类学家"},
            {"w": "survival-relevant", "pos": "adj.", "def": "与生存相关的"},
            {"w": "information", "pos": "n.", "def": "信息"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "But his research suggests otherwise.",
        "zh": "但他的研究却表明并非如此。",
        "grammar": {
            "type": "简单句",
            "note": "suggest otherwise 意为 “表明并非如此、暗示相反的情况”；otherwise 此处作 “不然、以其他方式” 讲。"
        },
        "words": [
            {"w": "research", "pos": "n.", "def": "研究"},
            {"w": "suggest otherwise", "pos": "phr.", "def": "表明并非如此"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": LSQUO + "We have this huge gap in our knowledge about the history and prehistory of storytelling, despite the fact that we know this genre is an incredibly ancient one," + RSQUO + " he says.",
        "zh": "“尽管我们知道这一体裁极其古老，但对于讲故事的历史和史前史，我们的认识仍存在巨大空白，”他说。",
        "grammar": {
            "type": "同位语从句 + 让步",
            "note": "despite the fact that... 为让步状语，含 that 同位语从句；(that) we know this genre is... 又含省略连词的宾语从句；a huge gap in 意为 “……方面的巨大空白”。"
        },
        "words": [
            {"w": "gap", "pos": "n.", "def": "空白；差距"},
            {"w": "prehistory", "pos": "n.", "def": "史前史"},
            {"w": "genre", "pos": "n.", "def": "体裁；类型"},
            {"w": "incredibly", "pos": "adv.", "def": "极其；难以置信地"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": "That hasn" + RSQUO + "t stopped anthropologists, folklorists and other academics devising theories to explain the importance of fairy tales in human society.",
        "zh": "但这并未阻止人类学家、民俗学者和其他学者们提出各种理论，来解释童话故事在人类社会中的重要性。",
        "grammar": {
            "type": "stop sb doing + 不定式状语",
            "note": "stop sb (from) doing 意为 “阻止某人做”，此处省略 from；devising theories... 为现在分词；to explain... 为目的状语。"
        },
        "words": [
            {"w": "folklorist", "pos": "n.", "def": "民俗学者"},
            {"w": "academic", "pos": "n.", "def": "学者；学术人员"},
            {"w": "devise", "pos": "v.", "def": "设计；想出"},
            {"w": "theory", "pos": "n.", "def": "理论"}
        ]
    },
    {
        "id": 12,
        "para": 2,
        "en": "Now Tehrani has found a way to test these ideas, borrowing a technique from evolutionary biologists.",
        "zh": "如今，特赫拉尼找到了一种检验这些观点的方法——借用了进化生物学家的一项技术。",
        "grammar": {
            "type": "现在分词状语",
            "note": "borrowing a technique from... 为现在分词短语作伴随状语；a way to test these ideas 中不定式作定语；evolutionary biologist 意为 “进化生物学家”。"
        },
        "words": [
            {"w": "test", "pos": "v.", "def": "检验；测试"},
            {"w": "borrow", "pos": "v.", "def": "借用"},
            {"w": "technique", "pos": "n.", "def": "技术；方法"},
            {"w": "evolutionary", "pos": "adj.", "def": "进化的"}
        ]
    },
    # Para 3
    {
        "id": 13,
        "para": 3,
        "en": "To work out the evolutionary history, development and relationships among groups of organisms, biologists compare the characteristics of living species in a process called " + LSQUO + "phylogenetic analysis" + RSQUO + ".",
        "zh": "为了弄清各类生物群体之间的进化历史、发展和相互关系，生物学家会在一个称为“系统发育分析”的过程中比较现存物种的特征。",
        "grammar": {
            "type": "不定式状语 + 过去分词定语",
            "note": "To work out... 为不定式作目的状语；called 'phylogenetic analysis' 为过去分词短语作定语修饰 a process；work out 意为 “弄清、算出”。"
        },
        "words": [
            {"w": "work out", "pos": "phr.", "def": "弄清；算出"},
            {"w": "organism", "pos": "n.", "def": "生物；有机体"},
            {"w": "characteristic", "pos": "n.", "def": "特征；特性"},
            {"w": "phylogenetic analysis", "pos": "phr.", "def": "系统发育分析"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": "Tehrani has used the same approach to compare related versions of fairy tales to discover how they have evolved and which elements have survived longest.",
        "zh": "特赫拉尼用同样的方法来比较童话故事相关的各个版本，以发现它们是如何演变的、哪些要素留存得最久。",
        "grammar": {
            "type": "不定式目的状语 + 并列宾语从句",
            "note": "to compare... to discover... 为连续的不定式作目的状语；how they have evolved 与 which elements have survived longest 为并列宾语从句；approach 意为 “方法”。"
        },
        "words": [
            {"w": "approach", "pos": "n.", "def": "方法；途径"},
            {"w": "related", "pos": "adj.", "def": "相关的"},
            {"w": "evolve", "pos": "v.", "def": "演变；进化"},
            {"w": "element", "pos": "n.", "def": "要素；成分"}
        ]
    },
    # Para 4
    {
        "id": 15,
        "para": 4,
        "en": "Tehrani" + RSQUO + "s analysis focused on Little Red Riding Hood in its many forms, which include another Western fairy tale known as The Wolf and the Kids.",
        "zh": "特赫拉尼的分析聚焦于《小红帽》的众多形式，其中还包括另一则名为《狼和小羊》的西方童话。",
        "grammar": {
            "type": "非限定性定语从句 + 过去分词定语",
            "note": "which include another Western fairy tale... 为非限定性定语从句修饰 its many forms；known as The Wolf and the Kids 为过去分词短语作定语；focus on 意为 “聚焦于”。"
        },
        "words": [
            {"w": "analysis", "pos": "n.", "def": "分析"},
            {"w": "focus on", "pos": "phr.", "def": "聚焦于；集中于"},
            {"w": "include", "pos": "v.", "def": "包括"}
        ]
    },
    {
        "id": 16,
        "para": 4,
        "en": "Checking for variants of these two tales and similar stories from Africa, East Asia and other regions, he ended up with 58 stories recorded from oral traditions.",
        "zh": "在查找这两则故事的变体以及来自非洲、东亚和其他地区的类似故事后，他最终得到了58个从口头传统中记录下来的故事。",
        "grammar": {
            "type": "现在分词状语",
            "note": "Checking for variants... 为现在分词短语作时间状语；recorded from oral traditions 为过去分词短语作定语修饰 58 stories；end up with 意为 “最终得到”。"
        },
        "words": [
            {"w": "variant", "pos": "n.", "def": "变体；变种"},
            {"w": "end up with", "pos": "phr.", "def": "最终得到；以……告终"},
            {"w": "oral tradition", "pos": "phr.", "def": "口头传统"},
            {"w": "region", "pos": "n.", "def": "地区"}
        ]
    },
    {
        "id": 17,
        "para": 4,
        "en": "Once his phylogenetic analysis had established that they were indeed related, he used the same methods to explore how they have developed and altered over time.",
        "zh": "一旦他的系统发育分析确认了它们之间确实存在关联，他便运用同样的方法去探究它们随时间是如何发展和演变的。",
        "grammar": {
            "type": "时间状语从句 + 宾语从句",
            "note": "Once... had established that... 为时间状语从句（含 that 宾语从句）；how they have developed and altered over time 为 explore 的宾语从句；establish 意为 “确认、证实”。"
        },
        "words": [
            {"w": "establish", "pos": "v.", "def": "确认；确立"},
            {"w": "explore", "pos": "v.", "def": "探究；探索"},
            {"w": "alter", "pos": "v.", "def": "改变；变化"},
            {"w": "over time", "pos": "phr.", "def": "随着时间；逐渐"}
        ]
    },
    # Para 5
    {
        "id": 18,
        "para": 5,
        "en": "First he tested some assumptions about which aspects of the story alter least as it evolves, indicating their importance.",
        "zh": "首先，他检验了一些关于故事哪些方面在演变过程中变化最小的假设——这些方面的稳定表明了它们的重要性。",
        "grammar": {
            "type": "宾语从句 + 现在分词状语",
            "note": "assumptions about which aspects... alter least 中 which... 为介词 about 的宾语从句；as it evolves 为时间状语从句；indicating their importance 为现在分词短语作结果状语。"
        },
        "words": [
            {"w": "assumption", "pos": "n.", "def": "假设；设想"},
            {"w": "aspect", "pos": "n.", "def": "方面"},
            {"w": "indicate", "pos": "v.", "def": "表明；显示"},
            {"w": "importance", "pos": "n.", "def": "重要性"}
        ]
    },
    {
        "id": 19,
        "para": 5,
        "en": "Folklorists believe that what happens in a story is more central to the story than the characters in it " + DASH + " that visiting a relative, only to be met by a scary animal in disguise, is more fundamental than whether the visitor is a little girl or three siblings, or the animal is a tiger instead of a wolf.",
        "zh": "民俗学者认为，故事中发生的事情比故事里的人物更为核心——即去探望亲戚、结果却遇到一只伪装起来的可怕动物，这一情节比访客是小女孩还是三个兄弟姐妹、动物是老虎还是狼更为根本。",
        "grammar": {
            "type": "宾语从句 + 破折号同位说明",
            "note": "believe that... 后接宾语从句，其主语为 what happens in a story；破折号后 that visiting a relative... is more fundamental than... 为对前句的同位补充说明；only to be met by... 为不定式表意外结果；in disguise 意为 “伪装的”。"
        },
        "words": [
            {"w": "central", "pos": "adj.", "def": "核心的；中心的"},
            {"w": "in disguise", "pos": "phr.", "def": "伪装的；乔装的"},
            {"w": "fundamental", "pos": "adj.", "def": "根本的；基础的"},
            {"w": "sibling", "pos": "n.", "def": "兄弟姐妹"}
        ]
    },
    # Para 6
    {
        "id": 20,
        "para": 6,
        "en": "However, Tehrani found no significant difference in the rate of evolution of incidents compared with that of characters.",
        "zh": "然而，特赫拉尼发现，情节的演变速度与人物的演变速度相比并无显著差异。",
        "grammar": {
            "type": "过去分词状语",
            "note": "compared with that of characters 为过去分词短语作状语（that 指代 the rate of evolution）；no significant difference in 意为 “在……方面无显著差异”；incident 意为 “情节、事件”。"
        },
        "words": [
            {"w": "significant", "pos": "adj.", "def": "显著的；重要的"},
            {"w": "rate", "pos": "n.", "def": "速度；比率"},
            {"w": "incident", "pos": "n.", "def": "情节；事件"},
            {"w": "compared with", "pos": "phr.", "def": "与……相比"}
        ]
    },
    {
        "id": 21,
        "para": 6,
        "en": LSQUO + "Certain episodes are very stable because they are crucial to the story, but there are lots of other details that can evolve quite freely," + RSQUO + " he says.",
        "zh": "“某些情节非常稳定，因为它们对故事至关重要；但也有大量其他细节可以相当自由地演变，”他说。",
        "grammar": {
            "type": "原因状语从句 + 转折 + 定语从句",
            "note": "because they are crucial to the story 为原因状语从句；but 后 there are lots of other details that... 含 that 定语从句；be crucial to 意为 “对……至关重要”。"
        },
        "words": [
            {"w": "episode", "pos": "n.", "def": "情节；片段"},
            {"w": "stable", "pos": "adj.", "def": "稳定的"},
            {"w": "crucial", "pos": "adj.", "def": "至关重要的"},
            {"w": "detail", "pos": "n.", "def": "细节"}
        ]
    },
    {
        "id": 22,
        "para": 6,
        "en": "Neither did his analysis support the theory that the central section of a story is the most conserved part.",
        "zh": "他的分析也不支持“故事的中间部分是保留得最完整的部分”这一理论。",
        "grammar": {
            "type": "否定倒装 + 同位语从句",
            "note": "Neither did his analysis support... 为否定词前置引起的部分倒装；the theory that... 中 that 引导同位语从句；the most conserved part 意为 “保留最完整的部分”。"
        },
        "words": [
            {"w": "support", "pos": "v.", "def": "支持"},
            {"w": "section", "pos": "n.", "def": "部分；段落"},
            {"w": "conserved", "pos": "adj.", "def": "保留的；保存下来的"}
        ]
    },
    {
        "id": 23,
        "para": 6,
        "en": "He found no significant difference in the flexibility of events there compared with the beginning or the end.",
        "zh": "他发现，与开头或结尾相比，中间部分事件的可变性并无显著差异。",
        "grammar": {
            "type": "过去分词状语",
            "note": "compared with the beginning or the end 为过去分词短语作状语；the flexibility of events there 中 there 指 “中间部分”；no significant difference in 意为 “在……方面无显著差异”。"
        },
        "words": [
            {"w": "flexibility", "pos": "n.", "def": "灵活性；可变性"},
            {"w": "event", "pos": "n.", "def": "事件；情节"},
            {"w": "beginning", "pos": "n.", "def": "开头；开端"}
        ]
    },
    # Para 7
    {
        "id": 24,
        "para": 7,
        "en": "But the really big surprise came when he looked at the cautionary elements of the story.",
        "zh": "但真正大的意外出现在他考察故事中的警示性成分时。",
        "grammar": {
            "type": "时间状语从句",
            "note": "when he looked at... 为时间状语从句；the really big surprise 为主语；cautionary elements 意为 “警示性成分”。"
        },
        "words": [
            {"w": "surprise", "pos": "n.", "def": "意外；惊讶"},
            {"w": "look at", "pos": "phr.", "def": "考察；查看"},
            {"w": "cautionary", "pos": "adj.", "def": "警示的；劝诫的"}
        ]
    },
    {
        "id": 25,
        "para": 7,
        "en": LSQUO + "Studies on hunter-gatherer folk tales suggest that these narratives include really important information about the environment and the possible dangers that may be faced there " + DASH + " stuff that" + RSQUO + "s relevant to survival," + RSQUO + " he says.",
        "zh": "“关于狩猎采集族群民间故事的研究表明，这些叙事包含了关于环境以及在那里可能面临的危险的重要信息——即与生存相关的内容，”他说。",
        "grammar": {
            "type": "宾语从句 + 定语从句 + 破折号补充",
            "note": "suggest that these narratives include... 为宾语从句；that may be faced there 为定语从句修饰 the possible dangers；破折号后 stuff that's relevant to survival 为补充说明，含定语从句；hunter-gatherer 意为 “狩猎采集的”。"
        },
        "words": [
            {"w": "hunter-gatherer", "pos": "adj.", "def": "狩猎采集的"},
            {"w": "narrative", "pos": "n.", "def": "叙事；故事"},
            {"w": "relevant to", "pos": "phr.", "def": "与……相关"},
            {"w": "survival", "pos": "n.", "def": "生存"}
        ]
    },
    {
        "id": 26,
        "para": 7,
        "en": "Yet in his analysis such elements were just as flexible as seemingly trivial details.",
        "zh": "然而在他的分析中，这类成分与看似无关紧要的细节一样容易发生变化。",
        "grammar": {
            "type": "as ... as 比较",
            "note": "just as flexible as... 为 “as...as” 同级比较；seemingly trivial 意为 “看似琐碎的”；Yet 表转折。"
        },
        "words": [
            {"w": "flexible", "pos": "adj.", "def": "易变的；灵活的"},
            {"w": "seemingly", "pos": "adv.", "def": "看似；表面上"},
            {"w": "trivial", "pos": "adj.", "def": "琐碎的；不重要的"}
        ]
    },
    {
        "id": 27,
        "para": 7,
        "en": "What, then, is important enough to be reproduced from generation to generation?",
        "zh": "那么，究竟什么才重要到足以世代相传呢？",
        "grammar": {
            "type": "主语从句（疑问）",
            "note": "What... is important enough to be reproduced...? 为主语疑问句；then 为插入语；from generation to generation 意为 “世代相传”。"
        },
        "words": [
            {"w": "reproduce", "pos": "v.", "def": "复制；再现；传承"},
            {"w": "from generation to generation", "pos": "phr.", "def": "世代相传"}
        ]
    },
    # Para 8
    {
        "id": 28,
        "para": 8,
        "en": "The answer, it would appear, is fear " + DASH + " blood-thirsty and gruesome aspects of the story, such as the eating of the grandmother by the wolf, turned out to be the best preserved of all.",
        "zh": "看来答案是恐惧——故事中血腥、可怕的部分，比如狼吃掉外婆的情节，结果被证明是保留得最完整的。",
        "grammar": {
            "type": "插入语 + 破折号说明",
            "note": "it would appear 为插入语；破折号后 blood-thirsty and gruesome aspects... turned out to be... 为对 fear 的具体说明；such as... 举例；turn out to be 意为 “结果是”。"
        },
        "words": [
            {"w": "blood-thirsty", "pos": "adj.", "def": "嗜血的；残忍的"},
            {"w": "gruesome", "pos": "adj.", "def": "可怕的；令人毛骨悚然的"},
            {"w": "turn out to be", "pos": "phr.", "def": "结果是；原来是"},
            {"w": "preserved", "pos": "adj.", "def": "保留的；保存的"}
        ]
    },
    {
        "id": 29,
        "para": 8,
        "en": "Why are these details retained by generations of storytellers, when other features are not?",
        "zh": "为什么这些细节能被一代代讲故事的人保留下来，而其他特征却没有呢？",
        "grammar": {
            "type": "被动疑问 + 时间/对比状语从句",
            "note": "are these details retained 为被动疑问；when other features are not 为对比状语从句（承前省略 retained）；be retained by 意为 “被……保留”。"
        },
        "words": [
            {"w": "retain", "pos": "v.", "def": "保留；保持"},
            {"w": "storyteller", "pos": "n.", "def": "讲故事的人"},
            {"w": "feature", "pos": "n.", "def": "特征；特色"}
        ]
    },
    {
        "id": 30,
        "para": 8,
        "en": "Tehrani has an idea: " + LSQUO + "In an oral context, a story won" + RSQUO + "t survive because of one great teller.",
        "zh": "特赫拉尼有一个看法：“在口头传播的语境中，一个故事不会仅因为一位出色的讲述者而流传下来。",
        "grammar": {
            "type": "冒号引出观点",
            "note": "冒号后为对 an idea 的具体阐述；In an oral context 意为 “在口头传播的语境中”；because of 意为 “因为、由于”。"
        },
        "words": [
            {"w": "oral", "pos": "adj.", "def": "口头的"},
            {"w": "context", "pos": "n.", "def": "语境；背景"},
            {"w": "survive", "pos": "v.", "def": "留存；幸存"}
        ]
    },
    {
        "id": 31,
        "para": 8,
        "en": "It also needs to be interesting when it" + RSQUO + "s told by someone who" + RSQUO + "s not necessarily a great storyteller." + RSQUO,
        "zh": "它还需要在由一个未必擅长讲故事的人讲述时也依然有趣。”",
        "grammar": {
            "type": "时间状语从句 + 定语从句",
            "note": "when it's told by someone... 为时间状语从句（被动）；who's not necessarily a great storyteller 为定语从句修饰 someone；not necessarily 意为 “未必”。"
        },
        "words": [
            {"w": "interesting", "pos": "adj.", "def": "有趣的"},
            {"w": "not necessarily", "pos": "phr.", "def": "未必；不一定"}
        ]
    },
    {
        "id": 32,
        "para": 8,
        "en": "Maybe being swallowed whole by a wolf, then cut out of its stomach alive is so gripping that it helps the story remain popular, no matter how badly it" + RSQUO + "s told.",
        "zh": "也许被狼整个吞下、然后又活生生地从它肚子里被剖出来，这一情节如此扣人心弦，以至于无论讲得多糟，都能帮助故事保持流行。",
        "grammar": {
            "type": "so ... that ... + 让步状语从句",
            "note": "being swallowed... then cut out... 为动名词主语；so gripping that... 为 so...that... 结果结构；no matter how badly it's told 为让步状语从句；gripping 意为 “扣人心弦的”。"
        },
        "words": [
            {"w": "swallow", "pos": "v.", "def": "吞下；吞咽"},
            {"w": "gripping", "pos": "adj.", "def": "扣人心弦的；引人入胜的"},
            {"w": "remain", "pos": "v.", "def": "保持；仍然是"},
            {"w": "no matter how", "pos": "phr.", "def": "无论如何"}
        ]
    },
    # Para 9
    {
        "id": 33,
        "para": 9,
        "en": "Jack Zipes at the University of Minnesota, Minneapolis, is unconvinced by Tehrani" + RSQUO + "s views on fairy tales.",
        "zh": "明尼阿波利斯明尼苏达大学的杰克·齐普斯并不认同特赫拉尼关于童话故事的观点。",
        "grammar": {
            "type": "主系表",
            "note": "be unconvinced by 意为 “不被……说服、不认同”；views on 意为 “关于……的观点”。"
        },
        "words": [
            {"w": "unconvinced", "pos": "adj.", "def": "不信服的；不认同的"},
            {"w": "view", "pos": "n.", "def": "观点；看法"}
        ]
    },
    {
        "id": 34,
        "para": 9,
        "en": LSQUO + "Even if they" + RSQUO + "re gruesome, they won" + RSQUO + "t stick unless they matter," + RSQUO + " he says.",
        "zh": "“即便它们很可怕，若无关紧要，也不会流传下来，”他说。",
        "grammar": {
            "type": "让步 + unless 条件",
            "note": "Even if they're gruesome 为让步状语从句；unless they matter 为条件状语从句；stick 此处意为 “留存、被记住”；matter 意为 “要紧、重要”。"
        },
        "words": [
            {"w": "stick", "pos": "v.", "def": "留存；被记住"},
            {"w": "unless", "pos": "conj.", "def": "除非"},
            {"w": "matter", "pos": "v.", "def": "要紧；重要"}
        ]
    },
    {
        "id": 35,
        "para": 9,
        "en": "He believes the perennial theme of women as victims in stories like Little Red Riding Hood explains why they continue to feel relevant.",
        "zh": "他认为，在《小红帽》这类故事中，女性作为受害者这一长盛不衰的主题，解释了为什么这些故事至今仍让人觉得贴近现实。",
        "grammar": {
            "type": "宾语从句 + why 从句",
            "note": "believes (that) the perennial theme... explains... 为省略连词的宾语从句；why they continue to feel relevant 为 explains 的宾语从句；perennial 意为 “长期的、常年的”。"
        },
        "words": [
            {"w": "perennial", "pos": "adj.", "def": "长期的；常年的"},
            {"w": "theme", "pos": "n.", "def": "主题"},
            {"w": "victim", "pos": "n.", "def": "受害者"},
            {"w": "relevant", "pos": "adj.", "def": "相关的；贴近现实的"}
        ]
    },
    {
        "id": 36,
        "para": 9,
        "en": "But Tehrani points out that although this is often the case in Western versions, it is not always true elsewhere.",
        "zh": "但特赫拉尼指出，尽管在西方版本中往往如此，但在其他地方却未必总是这样。",
        "grammar": {
            "type": "宾语从句 + 让步状语从句",
            "note": "points out that... 后接宾语从句；although this is often the case... 为其内让步状语从句；be the case 意为 “情况如此”；elsewhere 意为 “在别处”。"
        },
        "words": [
            {"w": "point out", "pos": "phr.", "def": "指出"},
            {"w": "be the case", "pos": "phr.", "def": "情况如此；确实这样"},
            {"w": "elsewhere", "pos": "adv.", "def": "在别处"}
        ]
    },
    {
        "id": 37,
        "para": 9,
        "en": "In Chinese and Japanese versions, often known as The Tiger Grandmother, the villain is a woman, and in both Iran and Nigeria, the victim is a boy.",
        "zh": "在常被称为《老虎外婆》的中国和日本版本里，反派是一个女人；而在伊朗和尼日利亚，受害者则是一个男孩。",
        "grammar": {
            "type": "并列句 + 过去分词定语",
            "note": "often known as The Tiger Grandmother 为过去分词短语作插入定语；and 连接两个分句；villain 意为 “反派、恶人”。"
        },
        "words": [
            {"w": "villain", "pos": "n.", "def": "反派；恶棍"},
            {"w": "victim", "pos": "n.", "def": "受害者"}
        ]
    },
    # Para 10
    {
        "id": 38,
        "para": 10,
        "en": "Mathias Clasen at Aarhus University in Denmark isn" + RSQUO + "t surprised by Tehrani" + RSQUO + "s findings.",
        "zh": "丹麦奥胡斯大学的马蒂亚斯·克拉森对特赫拉尼的研究结果并不感到意外。",
        "grammar": {
            "type": "主系表",
            "note": "be surprised by 意为 “对……感到意外”；findings 意为 “研究结果”。"
        },
        "words": [
            {"w": "be surprised by", "pos": "phr.", "def": "对……感到意外"},
            {"w": "finding", "pos": "n.", "def": "研究结果；发现"}
        ]
    },
    {
        "id": 39,
        "para": 10,
        "en": LSQUO + "Habits and morals change, but the things that scare us, and the fact that we seek out entertainment that" + RSQUO + "s designed to scare us " + DASH + " those are constant," + RSQUO + " he says.",
        "zh": "“习惯和道德会改变，但那些吓唬我们的东西，以及我们会主动去寻找旨在吓唬我们的娱乐这一事实——这些都是恒定不变的，”他说。",
        "grammar": {
            "type": "转折并列 + 定语从句 + 同位语从句",
            "note": "but 后主语为并列的 the things that scare us 和 the fact that...；that scare us 为定语从句，the fact that we seek out... 含同位语从句；破折号后 those are constant 复指前面主语；seek out 意为 “寻找、搜寻”。"
        },
        "words": [
            {"w": "moral", "pos": "n.", "def": "道德；道德观"},
            {"w": "scare", "pos": "v.", "def": "使害怕；吓唬"},
            {"w": "seek out", "pos": "phr.", "def": "寻找；搜寻"},
            {"w": "constant", "pos": "adj.", "def": "恒定的；不变的"}
        ]
    },
    {
        "id": 40,
        "para": 10,
        "en": "Clasen believes that scary stories teach us what it feels like to be afraid without having to experience real danger, and so build up resistance to negative emotions.",
        "zh": "克拉森认为，恐怖故事让我们在无需经历真正危险的情况下体会到害怕的感觉，从而增强对负面情绪的抵抗力。",
        "grammar": {
            "type": "宾语从句 + 宾语从句 + 结果状语",
            "note": "believes that scary stories teach us... 为宾语从句；what it feels like to be afraid 为 teach 的宾语从句（it 为形式主语）；without having to experience... 为方式状语；and so build up... 为结果状语；build up resistance to 意为 “增强对……的抵抗力”。"
        },
        "words": [
            {"w": "experience", "pos": "v.", "def": "经历；体验"},
            {"w": "build up", "pos": "phr.", "def": "增强；建立"},
            {"w": "resistance", "pos": "n.", "def": "抵抗力；抵抗"},
            {"w": "negative", "pos": "adj.", "def": "负面的；消极的"}
        ]
    }
]

phrases = [
    {"w": "dispose of", "pos": "phr.", "def": "除掉；处理掉"},
    {"w": "get the better of", "pos": "phr.", "def": "战胜；占上风"},
    {"w": "be attributed to", "pos": "phr.", "def": "被归因于"},
    {"w": "work out", "pos": "phr.", "def": "弄清；算出"},
    {"w": "end up with", "pos": "phr.", "def": "最终得到；以……告终"},
    {"w": "over time", "pos": "phr.", "def": "随着时间；逐渐"},
    {"w": "turn out to be", "pos": "phr.", "def": "结果是；原来是"},
    {"w": "from generation to generation", "pos": "phr.", "def": "世代相传"},
    {"w": "seek out", "pos": "phr.", "def": "寻找；搜寻"},
    {"w": "build up", "pos": "phr.", "def": "增强；建立"}
]

questions = [
    {
        "title": "Questions 27" + DASH + "31",
        "type": "sentence_endings",
        "instructions": [
            "Complete each sentence with the correct ending, A" + DASH + "F, below.",
            "Write the correct letter, A" + DASH + "F, in boxes 27" + DASH + "31 on your answer sheet.",
            "A may be provided through methods used in biological research. | B are the reason for their survival. | C show considerable global variation. | D contain animals which transform to become humans. | E were originally spoken rather than written. | F have been developed without factual basis."
        ],
        "items": [
            {"number": 27, "prompt": "In fairy tales, details of the plot", "answer": "C", "evidence_sentence": 1},
            {"number": 28, "prompt": "Tehrani rejects the idea that the useful lessons for life in fairy tales", "answer": "B", "evidence_sentence": 26},
            {"number": 29, "prompt": "Various theories about the social significance of fairy tales", "answer": "F", "evidence_sentence": 11},
            {"number": 30, "prompt": "Insights into the development of fairy tales", "answer": "A", "evidence_sentence": 14},
            {"number": 31, "prompt": "All the fairy tales analysed by Tehrani", "answer": "E", "evidence_sentence": 16}
        ]
    },
    {
        "title": "Questions 32" + DASH + "36",
        "type": "summary_completion_wordlist",
        "instructions": [
            "Complete the summary using the list of words, A" + DASH + "I, below.",
            "Write the correct letter, A" + DASH + "I, in boxes 32" + DASH + "36 on your answer sheet.",
            "Phylogenetic analysis of Little Red Riding Hood",
            "A ending  B events  C warning  D links  E records  F variations  G horror  H people  I plot"
        ],
        "items": [
            {"number": 32, "prompt": "Tehrani used techniques from evolutionary biology to find out if __________ existed among 58 stories from around the world.", "answer": "D", "evidence_sentence": 17},
            {"number": 33, "prompt": "He also wanted to know which aspects of the stories had fewest __________, as he believed these aspects would be the most important ones.", "answer": "F", "evidence_sentence": 18},
            {"number": 34, "prompt": "Contrary to other beliefs, he found that some __________ that were included in a story tended to change over time ...", "answer": "B", "evidence_sentence": 21},
            {"number": 35, "prompt": "He was also surprised that parts of a story which seemed to provide some sort of __________ were unimportant.", "answer": "C", "evidence_sentence": 26},
            {"number": 36, "prompt": "The aspect that he found most important in a story" + RSQUO + "s survival was __________.", "answer": "G", "evidence_sentence": 28}
        ]
    },
    {
        "title": "Questions 37" + DASH + "40",
        "type": "multiple_choice",
        "instructions": [
            "Choose the correct letter, A, B, C or D.",
            "Write the correct letter in boxes 37" + DASH + "40 on your answer sheet."
        ],
        "items": [
            {"number": 37, "prompt": "What method did Jamie Tehrani use to test his ideas about fairy tales?\nA  He compared oral and written forms of the same stories.\nB  He looked at many different forms of the same basic story.\nC  He looked at unrelated stories from many different countries.\nD  He contrasted the development of fairy tales with that of living creatures.", "answer": "B", "evidence_sentence": 15},
            {"number": 38, "prompt": "When discussing Tehrani" + RSQUO + "s views, Jack Zipes suggests that\nA  Tehrani ignores key changes in the role of women.\nB  stories which are too horrific are not always taken seriously.\nC  Tehrani overemphasises the importance of violence in stories.\nD  features of stories only survive if they have a deeper significance.", "answer": "D", "evidence_sentence": 34},
            {"number": 39, "prompt": "Why does Tehrani refer to Chinese and Japanese fairy tales?\nA  to indicate that Jack Zipes" + RSQUO + " theory is incorrect\nB  to suggest that crime is a global problem\nC  to imply that all fairy tales have a similar meaning\nD  to add more evidence for Jack Zipes" + RSQUO + " ideas", "answer": "A", "evidence_sentence": 37},
            {"number": 40, "prompt": "What does Mathias Clasen believe about fairy tales?\nA  They are a safe way of learning to deal with fear.\nB  They are a type of entertainment that some people avoid.\nC  They reflect the changing values of our society.\nD  They reduce our ability to deal with real-world problems.", "answer": "A", "evidence_sentence": 40}
        ]
    }
]

data = {
    "id": "c15-test3-p3",
    "source": "剑桥雅思15 Test 3 Passage 3",
    "title": "Why fairy tales are really scary tales",
    "subtitle": "Some people think that fairy tales are just stories to amuse children, but their universal and enduring appeal may be due to more serious reasons",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c15-test3-p3.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
