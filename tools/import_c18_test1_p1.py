# -*- coding: utf-8 -*-
"""Generate data/passages/c18-test1-p1.json (Urban farming)."""
import json
import os

RSQUO = "’"  # '
LSQUO = "‘"  # '
RDQUO = "”"  # "
LDQUO = "“"  # "
DASH = "–"   # en dash
EURO = "€"   # euro

sentences = [
    # Paragraph 1
    {
        "id": 1,
        "para": 1,
        "en": "On top of a striking new exhibition hall in southern Paris, the world" + RSQUO + "s largest urban rooftop farm has started to bear fruit.",
        "zh": "在巴黎南部一座引人注目的新展览馆顶上，世界上最大的城市屋顶农场已经开始结出果实。",
        "grammar": {
            "type": "地点状语前置 + 简单句",
            "note": "On top of a striking new exhibition hall in southern Paris 为地点状语前置；主干是 the world" + RSQUO + "s largest urban rooftop farm has started to bear fruit，has started to bear fruit 为现在完成时，bear fruit 字面“结果实”亦暗指“初见成效”。"
        },
        "words": [
            {"w": "striking", "pos": "adj.", "def": "引人注目的；醒目的"},
            {"w": "bear fruit", "pos": "phr.", "def": "结果实；（喻）取得成果"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "Strawberries that are small, intensely flavoured and resplendently red sprout abundantly from large plastic tubes.",
        "zh": "个头小、味道浓郁、红得鲜艳夺目的草莓，从大塑料管里茂盛地长出来。",
        "grammar": {
            "type": "定语从句 + 主谓",
            "note": "主干是 Strawberries... sprout abundantly from large plastic tubes；that are small, intensely flavoured and resplendently red 为定语从句修饰 Strawberries，从句内三个形容词并列作表语。"
        },
        "words": [
            {"w": "resplendently", "pos": "adv.", "def": "光彩夺目地；华丽地"},
            {"w": "sprout", "pos": "v.", "def": "发芽；长出"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "Peer inside and you see the tubes are completely hollow, the roots of dozens of strawberry plants dangling down inside them.",
        "zh": "往里一看，你会发现这些管子完全是空心的，几十株草莓的根从里面垂挂下来。",
        "grammar": {
            "type": "祈使句 + and 结果 + 独立主格",
            "note": "Peer inside and you see... 为“祈使句 + and + 陈述句”结构，表条件-结果；you see 后接省略 that 的宾语从句 the tubes are completely hollow；the roots... dangling down inside them 为独立主格结构作伴随描述。"
        },
        "words": [
            {"w": "peer", "pos": "v.", "def": "凝视；仔细看"},
            {"w": "dangle", "pos": "v.", "def": "悬垂；晃荡"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "From identical vertical tubes nearby burst row upon row of lettuces; near those are aromatic herbs, such as basil, sage and peppermint.",
        "zh": "旁边一模一样的竖管里，一排排生菜喷涌而出；靠近它们的是罗勒、鼠尾草、薄荷之类的芳香草本植物。",
        "grammar": {
            "type": "完全倒装 + 分号并列倒装",
            "note": "From identical vertical tubes nearby burst row upon row of lettuces 为地点状语提前引起的完全倒装，真正主语是 row upon row of lettuces；分号后 near those are aromatic herbs 同为倒装，such as... 举例。"
        },
        "words": [
            {"w": "aromatic", "pos": "adj.", "def": "芳香的；有香味的"},
            {"w": "row upon row", "pos": "phr.", "def": "一排又一排"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "Opposite, in narrow, horizontal trays packed not with soil but with coconut fibre, grow cherry tomatoes, shiny aubergines and brightly coloured chards.",
        "zh": "对面，在装的不是土壤而是椰壳纤维的狭窄水平托盘里，长着圣女果、油亮的茄子和色彩鲜艳的甜菜。",
        "grammar": {
            "type": "完全倒装 + not...but... 并列",
            "note": "Opposite... grow cherry tomatoes, shiny aubergines and brightly coloured chards 为地点状语提前的完全倒装，真正主语在 grow 之后；packed not with soil but with coconut fibre 为过去分词短语修饰 trays，not...but... 表“不是……而是……”。"
        },
        "words": [
            {"w": "aubergine", "pos": "n.", "def": "茄子（英式）"},
            {"w": "chard", "pos": "n.", "def": "甜菜；牛皮菜"}
        ]
    },
    # Paragraph 2
    {
        "id": 6,
        "para": 2,
        "en": "Pascal Hardy, an engineer and sustainable development consultant, began experimenting with vertical farming and aeroponic growing towers " + DASH + " as the soil-free plastic tubes are known " + DASH + " on his Paris apartment block roof five years ago.",
        "zh": "帕斯卡·哈迪是一名工程师兼可持续发展顾问，五年前他就在自家巴黎公寓楼的屋顶上，开始试验垂直农业和气培栽培塔——这种无土的塑料管就是这么叫的。",
        "grammar": {
            "type": "同位语 + 插入定语从句",
            "note": "主干是 Pascal Hardy... began experimenting with vertical farming and aeroponic growing towers；an engineer and sustainable development consultant 为主语同位语；破折号内 as the soil-free plastic tubes are known 为插入的定语从句，解释 towers 的别称。"
        },
        "words": [
            {"w": "aeroponic", "pos": "adj.", "def": "气培的；空气栽培的"},
            {"w": "consultant", "pos": "n.", "def": "顾问"}
        ]
    },
    {
        "id": 7,
        "para": 2,
        "en": "The urban rooftop space above the exhibition hall is somewhat bigger: 14,000 square metres and almost exactly the size of a couple of football pitches.",
        "zh": "展览馆上方的这片城市屋顶空间要大一些：有14,000平方米，几乎正好相当于两个足球场的大小。",
        "grammar": {
            "type": "主系表 + 冒号补充",
            "note": "主干是 The urban rooftop space... is somewhat bigger；冒号后 14,000 square metres and almost exactly the size of a couple of football pitches 为具体补充说明，与 bigger 呼应。"
        },
        "words": [
            {"w": "pitch", "pos": "n.", "def": "（英式）运动场地；球场"},
            {"w": "somewhat", "pos": "adv.", "def": "有点；稍微"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "Already, the team of young urban farmers who tend it have picked, in one day, 3,000 lettuces and 150 punnets of strawberries.",
        "zh": "打理这片农场的年轻城市农人团队，已经在一天之内采摘了3,000棵生菜和150篮草莓。",
        "grammar": {
            "type": "定语从句 + 现在完成时 + 插入语",
            "note": "主干是 the team... have picked... 3,000 lettuces and 150 punnets of strawberries；who tend it 为定语从句修饰 team；in one day 为插入的时间状语。"
        },
        "words": [
            {"w": "tend", "pos": "v.", "def": "照料；打理"},
            {"w": "punnet", "pos": "n.", "def": "（装水果的）小篮；小筐"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "When the remaining two thirds of the vast open area are in production, 20 staff will harvest up to 1,000 kg of perhaps 35 different varieties of fruit and vegetables, every day.",
        "zh": "当这片广阔露天区域剩下的三分之二都投入生产后，20名员工每天将收获多达1,000公斤、约35个不同品种的水果和蔬菜。",
        "grammar": {
            "type": "when 时间状语从句 + 主将从现",
            "note": "When... are in production 为时间状语从句；主句 20 staff will harvest up to 1,000 kg... 用一般将来时，从句用一般现在时表将来（主将从现）；up to 表“多达”。"
        },
        "words": [
            {"w": "in production", "pos": "phr.", "def": "在生产中；投产"},
            {"w": "variety", "pos": "n.", "def": "品种；种类"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": LSQUO + "We" + RSQUO + "re not ever, obviously, going to feed the whole city this way," + RSQUO + " cautions Hardy.",
        "zh": "“显然，我们永远不可能靠这种方式养活整座城市，”哈迪提醒道。",
        "grammar": {
            "type": "直接引语 + 引述倒装",
            "note": "引号内为直接引语，主干 We" + RSQUO + "re not ever going to feed the whole city this way，obviously 为插入语；cautions Hardy 为主谓倒装的引述句。"
        },
        "words": [
            {"w": "caution", "pos": "v.", "def": "告诫；提醒"},
            {"w": "obviously", "pos": "adv.", "def": "显然地"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": LSQUO + "In the urban environment you" + RSQUO + "re working with very significant practical constraints, clearly, on what you can do and where.",
        "zh": "“显然，在城市环境里，你在能做什么、在哪里做这些方面，都面临着相当大的实际限制。",
        "grammar": {
            "type": "直接引语 + 介词短语后置修饰",
            "note": "主干是 you" + RSQUO + "re working with very significant practical constraints；In the urban environment 为地点状语；clearly 为插入语；on what you can do and where 为介词短语后置修饰 constraints，what 引导宾语从句。"
        },
        "words": [
            {"w": "constraint", "pos": "n.", "def": "限制；约束"},
            {"w": "practical", "pos": "adj.", "def": "实际的；实践的"}
        ]
    },
    {
        "id": 12,
        "para": 2,
        "en": "But if enough unused space can be developed like this, there" + RSQUO + "s no reason why you shouldn" + RSQUO + "t eventually target maybe between 5% and 10% of consumption." + RSQUO,
        "zh": "但如果有足够多的闲置空间能这样开发利用，那就没有理由不把最终目标定在大约占消费量的5%到10%。”",
        "grammar": {
            "type": "if 条件状语从句 + there be + 定语从句",
            "note": "But if enough unused space can be developed like this 为条件状语从句；主句 there" + RSQUO + "s no reason why...，why you shouldn" + RSQUO + "t eventually target... 为定语从句修饰 reason；between 5% and 10% of consumption 为 target 的宾语。"
        },
        "words": [
            {"w": "target", "pos": "v.", "def": "把……定为目标；瞄准"},
            {"w": "consumption", "pos": "n.", "def": "消费；消费量"}
        ]
    },
    # Paragraph 3
    {
        "id": 13,
        "para": 3,
        "en": "Perhaps most significantly, however, this is a real-life showcase for the work of Hardy" + RSQUO + "s flourishing urban agriculture consultancy, Agripolis, which is currently fielding enquiries from around the world to design, build and equip a new breed of soil-free inner-city farm.",
        "zh": "然而，也许最重要的是，这是哈迪那家蒸蒸日上的城市农业咨询公司Agripolis的成果的一个现实展示——该公司目前正应对来自世界各地的咨询，为设计、建造并装备一种新型的无土城市中心农场。",
        "grammar": {
            "type": "主系表 + 同位语 + 非限定性定语从句",
            "note": "主干是 this is a real-life showcase for the work of Hardy" + RSQUO + "s... consultancy；Agripolis 为 consultancy 的同位语；which is currently fielding enquiries... 为非限定性定语从句修饰 Agripolis，to design, build and equip... 为不定式作目的状语。"
        },
        "words": [
            {"w": "showcase", "pos": "n.", "def": "展示（的场合）；橱窗"},
            {"w": "field", "pos": "v.", "def": "应对（问题/来电）；处理"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": LSQUO + "The method" + RSQUO + "s advantages are many," + RSQUO + " he says.",
        "zh": "“这种方法的优点很多，”他说。",
        "grammar": {
            "type": "直接引语 + 主系表",
            "note": "引号内主干 The method" + RSQUO + "s advantages are many，为主系表结构，表语 many 后置修饰 advantages 亦可理解为表语；he says 为引述句。"
        },
        "words": [
            {"w": "advantage", "pos": "n.", "def": "优点；优势"},
            {"w": "method", "pos": "n.", "def": "方法"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": LSQUO + "First, I don" + RSQUO + "t much like the fact that most of the fruit and vegetables we eat have been treated with something like 17 different pesticides, or that the intensive farming techniques that produced them are such huge generators of greenhouse gases.",
        "zh": "“首先，我很不喜欢这样一个事实：我们吃的大多数水果和蔬菜都被喷洒过大约17种不同的农药；也不喜欢生产它们的那种集约化耕作技术会产生如此大量的温室气体。",
        "grammar": {
            "type": "两个并列同位语从句 + 嵌套定语从句",
            "note": "主干是 I don" + RSQUO + "t much like the fact；两个 that 引导并列的同位语从句解释 fact：that most of the fruit... have been treated... 与 that the intensive farming techniques... are such huge generators...；we eat 和 that produced them 为嵌套定语从句。"
        },
        "words": [
            {"w": "pesticide", "pos": "n.", "def": "农药；杀虫剂"},
            {"w": "intensive", "pos": "adj.", "def": "集约的；密集的"}
        ]
    },
    {
        "id": 16,
        "para": 3,
        "en": "I don" + RSQUO + "t much like the fact, either, that they" + RSQUO + "ve travelled an average of 2,000 refrigerated kilometres to my plate, that their quality is so poor, because the varieties are selected for their capacity to withstand such substantial journeys, or that 80% of the price I pay goes to wholesalers and transport companies, not the producers." + RSQUO,
        "zh": "我同样很不喜欢这样的事实：它们平均要经过2,000公里的冷藏运输才到我的餐盘；它们的品质如此之差，是因为选育这些品种看重的是耐受长途运输的能力；还有我付的价钱里有80%落入了批发商和运输公司，而非生产者手中。”",
        "grammar": {
            "type": "三个并列同位语从句 + 原因状语",
            "note": "主干 I don" + RSQUO + "t much like the fact, either；三个 that 引导并列同位语从句：that they" + RSQUO + "ve travelled...、that their quality is so poor（其后 because... 为原因状语从句）、or that 80% of the price... goes to wholesalers...；the price I pay 为省略关系词的定语从句。"
        },
        "words": [
            {"w": "withstand", "pos": "v.", "def": "经受住；承受"},
            {"w": "wholesaler", "pos": "n.", "def": "批发商"}
        ]
    },
    # Paragraph 4
    {
        "id": 17,
        "para": 4,
        "en": "Produce grown using this soil-free method, on the other hand " + DASH + " which relies solely on a small quantity of water, enriched with organic nutrients, pumped around a closed circuit of pipes, towers and trays " + DASH + " is " + LSQUO + "produced up here, and sold locally, just down there.",
        "zh": "另一方面，用这种无土方法种出的农产品——它仅依靠少量水，这些水富含有机养分，在管道、塔架和托盘构成的闭合回路中循环流动——是“在这上面生产、就近在那下面出售的。",
        "grammar": {
            "type": "过去分词作主语定语 + 插入定语从句 + 直接引语",
            "note": "主语 Produce，grown using this soil-free method 为过去分词短语作后置定语；破折号内 which relies solely on a small quantity of water 为非限定性定语从句，enriched with organic nutrients 和 pumped around a closed circuit... 为过去分词修饰 water；主句谓语 is，其后接直接引语。"
        },
        "words": [
            {"w": "produce", "pos": "n.", "def": "农产品（此处名词，重音在前）"},
            {"w": "circuit", "pos": "n.", "def": "回路；环路"}
        ]
    },
    {
        "id": 18,
        "para": 4,
        "en": "It barely travels at all," + RSQUO + " Hardy says.",
        "zh": "它几乎完全不需要运输，”哈迪说。",
        "grammar": {
            "type": "直接引语 + 引述句",
            "note": "引号内 It barely travels at all，barely 为半否定词表“几乎不”，at all 加强否定语气；Hardy says 为引述句。"
        },
        "words": [
            {"w": "barely", "pos": "adv.", "def": "几乎不；仅仅"},
            {"w": "at all", "pos": "phr.", "def": "（用于否定）丝毫；根本"}
        ]
    },
    {
        "id": 19,
        "para": 4,
        "en": LSQUO + "You can select crop varieties for their flavour, not their resistance to the transport and storage chain, and you can pick them when they" + RSQUO + "re really at their best, and not before." + RSQUO,
        "zh": "“你可以根据风味来选择作物品种，而不是根据它们对运输和储存链条的耐受性；而且你可以在它们真正处于最佳状态时采摘，一刻也不提前。”",
        "grammar": {
            "type": "并列句 + not 对比 + 时间状语从句",
            "note": "两个 you can... 由 and 并列；第一分句 select... for their flavour, not their resistance...，not 引出对比；第二分句 pick them when they" + RSQUO + "re really at their best，when 引导时间状语从句，and not before 为省略补充。"
        },
        "words": [
            {"w": "flavour", "pos": "n.", "def": "风味；味道"},
            {"w": "resistance", "pos": "n.", "def": "抵抗力；耐受性"}
        ]
    },
    {
        "id": 20,
        "para": 4,
        "en": "No soil is exhausted, and the water that gently showers the plants" + RSQUO + " roots every 12 minutes is recycled, so the method uses 90% less water than a classic intensive farm for the same yield.",
        "zh": "没有土壤会被耗尽地力，而且每12分钟轻柔喷淋植物根部的水都会被循环利用，因此在产量相同的情况下，这种方法的用水量比传统集约化农场少90%。",
        "grammar": {
            "type": "并列句 + 定语从句 + 结果状语 + 比较结构",
            "note": "三个分句由 and、so 连接；the water that gently showers the plants" + RSQUO + " roots every 12 minutes is recycled 中 that... 为定语从句修饰 water；so 引出结果，90% less water than... 为比较结构。"
        },
        "words": [
            {"w": "exhaust", "pos": "v.", "def": "耗尽；使枯竭"},
            {"w": "yield", "pos": "n.", "def": "产量；收成"}
        ]
    },
    # Paragraph 5
    {
        "id": 21,
        "para": 5,
        "en": "Urban farming is not, of course, a new phenomenon.",
        "zh": "当然，城市农业并不是什么新现象。",
        "grammar": {
            "type": "主系表 + 插入语",
            "note": "主干是 Urban farming is not a new phenomenon；of course 为插入语，缓和语气。"
        },
        "words": [
            {"w": "phenomenon", "pos": "n.", "def": "现象"},
            {"w": "of course", "pos": "phr.", "def": "当然"}
        ]
    },
    {
        "id": 22,
        "para": 5,
        "en": "Inner-city agriculture is booming from Shanghai to Detroit and Tokyo to Bangkok.",
        "zh": "从上海到底特律、从东京到曼谷，城市中心的农业正蓬勃兴起。",
        "grammar": {
            "type": "主谓 + from...to... 并列状语",
            "note": "主干是 Inner-city agriculture is booming；from Shanghai to Detroit and Tokyo to Bangkok 为两组 from...to... 并列作范围状语，列举地点。"
        },
        "words": [
            {"w": "boom", "pos": "v.", "def": "迅速发展；繁荣"},
            {"w": "inner-city", "pos": "adj.", "def": "城市中心的；市区的"}
        ]
    },
    {
        "id": 23,
        "para": 5,
        "en": "Strawberries are being grown in disused shipping containers, mushrooms in underground carparks.",
        "zh": "草莓被种在废弃的海运集装箱里，蘑菇则种在地下停车场里。",
        "grammar": {
            "type": "现在进行时被动 + 后半省略",
            "note": "主干是 Strawberries are being grown in disused shipping containers，为现在进行时的被动语态；mushrooms in underground carparks 后省略了 are being grown，与前句并列。"
        },
        "words": [
            {"w": "disused", "pos": "adj.", "def": "废弃的；不再使用的"},
            {"w": "shipping container", "pos": "phr.", "def": "海运集装箱"}
        ]
    },
    {
        "id": 24,
        "para": 5,
        "en": "Aeroponic farming, he says, is " + LSQUO + "virtuous" + RSQUO + ".",
        "zh": "他说，气培农业是“有益无害的”。",
        "grammar": {
            "type": "主系表 + 插入引述",
            "note": "主干是 Aeroponic farming is " + LSQUO + "virtuous" + RSQUO + "；he says 为插入的引述句；virtuous 加引号，表说话人对该词的强调。"
        },
        "words": [
            {"w": "virtuous", "pos": "adj.", "def": "有益的；品德高尚的"},
            {"w": "aeroponic farming", "pos": "phr.", "def": "气培农业"}
        ]
    },
    {
        "id": 25,
        "para": 5,
        "en": "The equipment weighs little, can be installed on almost any flat surface and is cheap to buy: roughly " + EURO + "100 to " + EURO + "150 per square metre.",
        "zh": "这种设备重量很轻，几乎可以安装在任何平面上，而且购买成本低廉：每平方米大约100到150欧元。",
        "grammar": {
            "type": "并列谓语 + 冒号补充",
            "note": "主语 The equipment 带三个并列谓语：weighs little、can be installed on almost any flat surface、is cheap to buy；冒号后 roughly " + EURO + "100 to " + EURO + "150 per square metre 具体说明 cheap。"
        },
        "words": [
            {"w": "install", "pos": "v.", "def": "安装"},
            {"w": "roughly", "pos": "adv.", "def": "大约；粗略地"}
        ]
    },
    {
        "id": 26,
        "para": 5,
        "en": "It is cheap to run, too, consuming a tiny fraction of the electricity used by some techniques.",
        "zh": "它的运行成本也很低，耗电量只是某些技术用电量的极小一部分。",
        "grammar": {
            "type": "主系表 + 现在分词状语 + 过去分词定语",
            "note": "主干是 It is cheap to run, too；consuming a tiny fraction of the electricity 为现在分词短语作伴随状语；used by some techniques 为过去分词短语修饰 electricity。"
        },
        "words": [
            {"w": "fraction", "pos": "n.", "def": "小部分；分数"},
            {"w": "consume", "pos": "v.", "def": "消耗；消费"}
        ]
    },
    # Paragraph 6
    {
        "id": 27,
        "para": 6,
        "en": "Produce grown this way typically sells at prices that, while generally higher than those of classic intensive agriculture, are lower than soil-based organic growers.",
        "zh": "以这种方式种出的农产品，其售价通常虽然高于传统集约化农业的产品，却低于以土壤种植的有机种植者的产品。",
        "grammar": {
            "type": "过去分词定语 + 定语从句 + while 让步插入",
            "note": "主语 Produce，grown this way 为过去分词定语；谓语 sells at prices；that... are lower than... 为定语从句修饰 prices；while generally higher than those of classic intensive agriculture 为 while 引导的让步状语作插入语。"
        },
        "words": [
            {"w": "typically", "pos": "adv.", "def": "通常；一般而言"},
            {"w": "organic", "pos": "adj.", "def": "有机的"}
        ]
    },
    {
        "id": 28,
        "para": 6,
        "en": "There are limits to what farmers can grow this way, of course, and much of the produce is suited to the summer months.",
        "zh": "当然，农民以这种方式能种的东西是有限的，而且大部分农产品都适合在夏季种植。",
        "grammar": {
            "type": "there be + 宾语从句 + and 并列",
            "note": "第一分句 There are limits to what farmers can grow this way，what 引导宾语从句作 to 的宾语；of course 为插入语；and much of the produce is suited to the summer months 为并列分句，be suited to 表“适合”。"
        },
        "words": [
            {"w": "limit", "pos": "n.", "def": "限度；限制"},
            {"w": "be suited to", "pos": "phr.", "def": "适合于"}
        ]
    },
    {
        "id": 29,
        "para": 6,
        "en": LSQUO + "Root vegetables we cannot do, at least not yet," + RSQUO + " he says.",
        "zh": "“块根类蔬菜我们种不了，至少现在还不行，”他说。",
        "grammar": {
            "type": "宾语前置 + 直接引语",
            "note": "引号内 Root vegetables we cannot do 为宾语前置（正常语序 we cannot do root vegetables），起强调作用；at least not yet 为补充；he says 为引述句。"
        },
        "words": [
            {"w": "root vegetable", "pos": "phr.", "def": "块根类蔬菜（如胡萝卜、马铃薯）"},
            {"w": "at least", "pos": "phr.", "def": "至少"}
        ]
    },
    {
        "id": 30,
        "para": 6,
        "en": LSQUO + "Radishes are OK, but carrots, potatoes, that kind of thing " + DASH + " the roots are simply too long.",
        "zh": "“萝卜还行，但胡萝卜、马铃薯这类东西——它们的根实在太长了。",
        "grammar": {
            "type": "转折并列 + 破折号解释",
            "note": "Radishes are OK 与 but carrots, potatoes, that kind of thing 形成转折；破折号后 the roots are simply too long 解释原因，simply 加强语气。"
        },
        "words": [
            {"w": "radish", "pos": "n.", "def": "萝卜；小红萝卜"},
            {"w": "simply", "pos": "adv.", "def": "简直；完全"}
        ]
    },
    {
        "id": 31,
        "para": 6,
        "en": "Fruit trees are obviously not an option.",
        "zh": "果树显然是行不通的。",
        "grammar": {
            "type": "主系表",
            "note": "主干是 Fruit trees are... not an option，not an option 表“不是一个选项/不可行”；obviously 作状语。"
        },
        "words": [
            {"w": "option", "pos": "n.", "def": "选择；选项"},
            {"w": "obviously", "pos": "adv.", "def": "显然地"}
        ]
    },
    {
        "id": 32,
        "para": 6,
        "en": "And beans tend to take up a lot of space for not much return." + RSQUO,
        "zh": "而豆类往往会占用很大空间，回报却不多。”",
        "grammar": {
            "type": "主谓 + 介词短语状语",
            "note": "主干是 beans tend to take up a lot of space；tend to do 表“往往、倾向于”；for not much return 为介词短语作状语，表结果/代价。"
        },
        "words": [
            {"w": "take up", "pos": "phr.", "def": "占用（空间/时间）"},
            {"w": "return", "pos": "n.", "def": "回报；收益"}
        ]
    },
    {
        "id": 33,
        "para": 6,
        "en": "Nevertheless, urban farming of the kind being practised in Paris is one part of a bigger and fast-changing picture that is bringing food production closer to our lives.",
        "zh": "尽管如此，巴黎正在实践的这类城市农业，只是一幅更大、变化更快的图景中的一部分，而这幅图景正在把食物生产拉近到我们的生活中。",
        "grammar": {
            "type": "现在分词定语 + 定语从句",
            "note": "主干是 urban farming... is one part of a bigger and fast-changing picture；being practised in Paris 为现在分词短语（被动）修饰 farming；that is bringing food production closer to our lives 为定语从句修饰 picture；Nevertheless 表转折。"
        },
        "words": [
            {"w": "nevertheless", "pos": "adv.", "def": "尽管如此；然而"},
            {"w": "practise", "pos": "v.", "def": "实践；从事"}
        ]
    }
]

questions = [
    {
        "title": "Questions 1" + DASH + "3",
        "type": "sentence_completion",
        "instructions": [
            "Complete the sentences below.",
            "Choose NO MORE THAN TWO WORDS AND/OR A NUMBER from the passage for each answer.",
            "Write your answers in boxes 1" + DASH + "3 on your answer sheet.",
            "Urban farming in Paris"
        ],
        "items": [
            {"number": 1, "prompt": "Vertical tubes are used to grow strawberries, ____ and herbs.", "answer": "lettuces", "evidence_sentence": 4},
            {"number": 2, "prompt": "There will eventually be a daily harvest of as much as ____ in weight of fruit and vegetables.", "answer": "1,000 kg", "evidence_sentence": 9},
            {"number": 3, "prompt": "It may be possible that the farm" + RSQUO + "s produce will account for as much as 10% of the city" + RSQUO + "s ____ overall.", "answer": "(food) consumption", "evidence_sentence": 12}
        ]
    },
    {
        "title": "Questions 4" + DASH + "7",
        "type": "table_completion",
        "instructions": [
            "Complete the table below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 4" + DASH + "7 on your answer sheet.",
            "Intensive farming versus aeroponic urban farming"
        ],
        "items": [
            {"number": 4, "prompt": "Intensive farming " + DASH + " Growth: wide range of 4 ____ used; techniques pollute air.", "answer": "pesticides", "evidence_sentence": 15},
            {"number": 5, "prompt": "Intensive farming " + DASH + " Selection: quality not good; varieties of fruit and vegetables chosen that can survive long 5 ____ .", "answer": "journeys", "evidence_sentence": 16},
            {"number": 6, "prompt": "Intensive farming " + DASH + " Sale: 6 ____ receive very little of overall income.", "answer": "producers", "evidence_sentence": 16},
            {"number": 7, "prompt": "Aeroponic urban farming " + DASH + " Selection: produce chosen because of its 7 ____ .", "answer": "flavour", "evidence_sentence": 19}
        ]
    },
    {
        "title": "Questions 8" + DASH + "13",
        "type": "true_false_notgiven",
        "instructions": [
            "Do the following statements agree with the information given in Reading Passage 1?",
            "In boxes 8" + DASH + "13 on your answer sheet, write",
            "TRUE if the statement agrees with the information",
            "FALSE if the statement contradicts the information",
            "NOT GIVEN if there is no information on this"
        ],
        "items": [
            {"number": 8, "prompt": "Urban farming can take place above or below ground.", "answer": "TRUE", "evidence_sentence": 23},
            {"number": 9, "prompt": "Some of the equipment used in aeroponic farming can be made by hand.", "answer": "NOT GIVEN", "evidence_sentence": 25},
            {"number": 10, "prompt": "Urban farming relies more on electricity than some other types of farming.", "answer": "FALSE", "evidence_sentence": 26},
            {"number": 11, "prompt": "Fruit and vegetables grown on an aeroponic urban farm are cheaper than traditionally grown organic produce.", "answer": "TRUE", "evidence_sentence": 27},
            {"number": 12, "prompt": "Most produce can be grown on an aeroponic urban farm at any time of the year.", "answer": "FALSE", "evidence_sentence": 28},
            {"number": 13, "prompt": "Beans take longer to grow on an urban farm than other vegetables.", "answer": "NOT GIVEN", "evidence_sentence": 32}
        ]
    }
]

phrases = [
    {"w": "urban farming", "pos": "n.", "def": "城市农业"},
    {"w": "rooftop farm", "pos": "n.", "def": "屋顶农场"},
    {"w": "aeroponic growing tower", "pos": "n.", "def": "气培栽培塔"},
    {"w": "soil-free", "pos": "adj.", "def": "无土的"},
    {"w": "coconut fibre", "pos": "n.", "def": "椰壳纤维"},
    {"w": "vertical farming", "pos": "n.", "def": "垂直农业"},
    {"w": "sustainable development", "pos": "n.", "def": "可持续发展"},
    {"w": "greenhouse gases", "pos": "n.", "def": "温室气体"},
    {"w": "closed circuit", "pos": "n.", "def": "闭合回路"},
    {"w": "intensive agriculture", "pos": "n.", "def": "集约化农业"}
]

data = {
    "id": "c18-test1-p1",
    "source": "剑桥雅思18 · Test 1 · Passage 1",
    "title": "Urban farming",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "subtitle": "In Paris, urban farmers are trying a soil-free approach to agriculture that uses less space and fewer resources. Could it help cities face the threats to our food supplies?",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c18-test1-p1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
