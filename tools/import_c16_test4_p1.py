# -*- coding: utf-8 -*-
"""Generate data/passages/c16-test4-p1.json (Roman tunnels)."""
import json
import os

RSQUO = "’"  # '
LSQUO = "‘"  # '
DASH = "–"   # -
CCEDIL = "Ç"  # C with cedilla (Çevlik)

sentences = [
    # Para 1
    {
        "id": 1,
        "para": 1,
        "en": "The Persians, who lived in present-day Iran, were one of the first civilizations to build tunnels that provided a reliable supply of water to human settlements in dry areas.",
        "zh": "波斯人生活在今天的伊朗，是最早修建隧道、为干旱地区人类聚居地提供可靠水源的文明之一。",
        "grammar": {
            "type": "who 非限制性定语 + 不定式定语 + that 定语从句",
            "note": "who lived in present-day Iran 为非限制性定语从句；one of the first civilizations to build tunnels 中 to build 为不定式定语；that provided a reliable supply of water 为 that 定语从句修饰 tunnels；settlement 意为 “聚居地”。"
        },
        "words": [
            {"w": "Persian", "pos": "n.", "def": "波斯人"},
            {"w": "present-day", "pos": "adj.", "def": "当今的；现代的"},
            {"w": "civilization", "pos": "n.", "def": "文明"},
            {"w": "settlement", "pos": "n.", "def": "聚居地；定居点"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "In the early first millennium BCE, they introduced the qanat method of tunnel construction, which consisted of placing posts over a hill in a straight line, to ensure that the tunnel kept to its route, and then digging vertical shafts down into the ground at regular intervals.",
        "zh": "在公元前第一个千年的早期，他们引入了“坎儿井”的隧道建造法，其做法是先在山丘上沿直线放置标杆，以确保隧道不偏离路线，然后再每隔一定距离向地下挖掘垂直竖井。",
        "grammar": {
            "type": "which 非限制性定语 + consist of doing",
            "note": "which consisted of placing... and then digging... 为非限制性定语从句，consist of doing 意为 “由做……构成”，含两个并列动名词；to ensure that the tunnel kept to its route 为不定式表目的；at regular intervals 意为 “每隔一定距离”；post 意为 “标杆”。"
        },
        "words": [
            {"w": "millennium", "pos": "n.", "def": "千年"},
            {"w": "post", "pos": "n.", "def": "柱；标杆"},
            {"w": "keep to", "pos": "phr.", "def": "坚持；不偏离"},
            {"w": "vertical shaft", "pos": "phr.", "def": "垂直竖井"},
            {"w": "at regular intervals", "pos": "phr.", "def": "每隔一定距离/时间"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "Underground, workers removed the earth from between the ends of the shafts, creating a tunnel.",
        "zh": "在地下，工人们把各竖井端头之间的泥土清除掉，从而形成一条隧道。",
        "grammar": {
            "type": "现在分词状语",
            "note": "Underground 为地点状语；主句 workers removed the earth from between the ends of the shafts；creating a tunnel 为现在分词作结果状语；remove 意为 “清除”，earth 此处意为 “泥土”。"
        },
        "words": [
            {"w": "underground", "pos": "adv.", "def": "在地下"},
            {"w": "remove", "pos": "v.", "def": "清除；移除"},
            {"w": "earth", "pos": "n.", "def": "泥土；土壤"},
            {"w": "shaft", "pos": "n.", "def": "竖井"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "The excavated soil was taken up to the surface using the shafts, which also provided ventilation during the work.",
        "zh": "挖出的泥土通过竖井被运到地面，这些竖井在施工期间还起到了通风的作用。",
        "grammar": {
            "type": "被动 + 现在分词状语 + which 非限制性定语",
            "note": "The excavated soil was taken up to the surface 为被动；using the shafts 为现在分词作方式状语；which also provided ventilation 为非限制性定语从句修饰 shafts；excavated 意为 “挖出的”，ventilation 意为 “通风”。"
        },
        "words": [
            {"w": "excavated", "pos": "adj.", "def": "挖出的；发掘的"},
            {"w": "surface", "pos": "n.", "def": "地面；表面"},
            {"w": "ventilation", "pos": "n.", "def": "通风"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "Once the tunnel was completed, it allowed water to flow from the top of a hillside down towards a canal, which supplied water for human use.",
        "zh": "隧道一旦建成，就能让水从山坡顶部往下流向一条水渠，而这条水渠则供应人们生活用水。",
        "grammar": {
            "type": "Once 时间从句 + allow sb to do + which 定语从句",
            "note": "Once the tunnel was completed 为时间状语从句；allow water to flow 为 allow sth to do；from the top... down towards a canal 为方向状语；which supplied water for human use 为非限制性定语从句修饰 canal；canal 意为 “水渠、运河”。"
        },
        "words": [
            {"w": "complete", "pos": "v.", "def": "完成"},
            {"w": "flow", "pos": "v.", "def": "流动"},
            {"w": "hillside", "pos": "n.", "def": "山坡"},
            {"w": "canal", "pos": "n.", "def": "水渠；运河"}
        ]
    },
    {
        "id": 6,
        "para": 1,
        "en": "Remarkably, some qanats built by the Persians 2,700 years ago are still in use today.",
        "zh": "值得注意的是，波斯人在2700年前修建的一些坎儿井至今仍在使用。",
        "grammar": {
            "type": "过去分词定语",
            "note": "Remarkably 为评注状语；built by the Persians 2,700 years ago 为过去分词短语作定语修饰 qanats；are still in use today 为主句谓语；in use 意为 “在使用中”。"
        },
        "words": [
            {"w": "remarkably", "pos": "adv.", "def": "值得注意地"},
            {"w": "qanat", "pos": "n.", "def": "坎儿井（地下引水渠）"},
            {"w": "in use", "pos": "phr.", "def": "在使用中"}
        ]
    },
    # Para 2
    {
        "id": 7,
        "para": 2,
        "en": "They later passed on their knowledge to the Romans, who also used the qanat method to construct water-supply tunnels for agriculture.",
        "zh": "后来他们把自己的知识传给了罗马人，罗马人同样使用坎儿井法为农业修建供水隧道。",
        "grammar": {
            "type": "who 非限制性定语 + 不定式目的",
            "note": "pass on A to B 意为 “把 A 传给 B”；who also used the qanat method to construct... 为非限制性定语从句；to construct water-supply tunnels for agriculture 为不定式表目的；water-supply 意为 “供水的”。"
        },
        "words": [
            {"w": "pass on", "pos": "phr.", "def": "传递；传授"},
            {"w": "construct", "pos": "v.", "def": "建造"},
            {"w": "water-supply", "pos": "adj.", "def": "供水的"},
            {"w": "agriculture", "pos": "n.", "def": "农业"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "Roman qanat tunnels were constructed with vertical shafts dug at intervals of between 30 and 60 meters.",
        "zh": "罗马的坎儿井隧道在修建时，每隔30到60米就挖一个垂直竖井。",
        "grammar": {
            "type": "被动 + 过去分词定语",
            "note": "were constructed with vertical shafts 为被动；dug at intervals of between 30 and 60 meters 为过去分词短语作定语修饰 shafts；at intervals of 意为 “以……的间隔”；between... and... 表范围。"
        },
        "words": [
            {"w": "interval", "pos": "n.", "def": "间隔"},
            {"w": "dig", "pos": "v.", "def": "挖掘"},
            {"w": "meter", "pos": "n.", "def": "米"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "The shafts were equipped with handholds and footholds to help those climbing in and out of them and were covered with a wooden or stone lid.",
        "zh": "竖井里装有供攀爬用的手抓点和脚踏点，以帮助上下攀爬的人，井口则盖有木质或石质的盖子。",
        "grammar": {
            "type": "并列被动谓语 + 不定式目的",
            "note": "were equipped with... and were covered with... 为并列被动谓语；to help those climbing in and out of them 为不定式表目的，climbing... 为现在分词定语修饰 those；handhold 意为 “手抓点”，foothold 意为 “立足点”，lid 意为 “盖子”。"
        },
        "words": [
            {"w": "be equipped with", "pos": "phr.", "def": "配备有"},
            {"w": "handhold", "pos": "n.", "def": "手抓点；抓手"},
            {"w": "foothold", "pos": "n.", "def": "立足点；踏脚处"},
            {"w": "lid", "pos": "n.", "def": "盖子"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "To ensure that the shafts were vertical, Romans hung a plumb line from a rod placed across the top of each shaft and made sure that the weight at the end of it hung in the center of the shaft.",
        "zh": "为确保竖井垂直，罗马人会在每个竖井顶部横放一根杆子，从杆上垂下一条铅垂线，并确保线端的重物悬垂在竖井的中心。",
        "grammar": {
            "type": "不定式目的 + 过去分词定语 + that 宾语从句",
            "note": "To ensure that the shafts were vertical 为不定式表目的，含 that 从句；hung a plumb line from a rod... and made sure that... 为并列谓语；placed across the top of each shaft 为过去分词定语修饰 rod；plumb line 意为 “铅垂线”，rod 意为 “杆”。"
        },
        "words": [
            {"w": "plumb line", "pos": "phr.", "def": "铅垂线"},
            {"w": "rod", "pos": "n.", "def": "杆；棒"},
            {"w": "weight", "pos": "n.", "def": "重物；重量"},
            {"w": "vertical", "pos": "adj.", "def": "垂直的"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": "Plumb lines were also used to measure the depth of the shaft and to determine the slope of the tunnel.",
        "zh": "铅垂线还被用来测量竖井的深度以及确定隧道的坡度。",
        "grammar": {
            "type": "被动 + 并列不定式",
            "note": "were also used to measure... and to determine... 为被动加两个并列不定式；the depth of the shaft 意为 “竖井的深度”；the slope of the tunnel 意为 “隧道的坡度”；slope 意为 “坡度、斜度”。"
        },
        "words": [
            {"w": "measure", "pos": "v.", "def": "测量"},
            {"w": "depth", "pos": "n.", "def": "深度"},
            {"w": "determine", "pos": "v.", "def": "确定"},
            {"w": "slope", "pos": "n.", "def": "坡度；斜度"}
        ]
    },
    {
        "id": 12,
        "para": 2,
        "en": "The 5.6-kilometer-long Claudius tunnel, built in 41 CE to drain the Fucine Lake in central Italy, had shafts that were up to 122 meters deep, took 11 years to build and involved approximately 30,000 workers.",
        "zh": "长5.6公里的克劳狄乌斯隧道建于公元41年，用于排干意大利中部的富奇诺湖，其竖井深达122米，历时11年建成，动用了约3万名工人。",
        "grammar": {
            "type": "过去分词定语 + that 定语从句 + 并列谓语",
            "note": "built in 41 CE to drain the Fucine Lake 为过去分词短语作定语修饰 tunnel；had shafts that were up to 122 meters deep 含 that 定语从句；三个并列谓语 had... took... and involved...；drain 意为 “排干”，up to 意为 “多达”。"
        },
        "words": [
            {"w": "drain", "pos": "v.", "def": "排干；排水"},
            {"w": "up to", "pos": "phr.", "def": "多达；高达"},
            {"w": "involve", "pos": "v.", "def": "涉及；动用"},
            {"w": "approximately", "pos": "adv.", "def": "大约"}
        ]
    },
    # Para 3
    {
        "id": 13,
        "para": 3,
        "en": "By the 6th century BCE, a second method of tunnel construction appeared called the counter-excavation method, in which the tunnel was constructed from both ends.",
        "zh": "到公元前6世纪，出现了第二种隧道建造法，称为“对向开挖法”，即从隧道两端同时施工。",
        "grammar": {
            "type": "过去分词定语 + in which 定语从句",
            "note": "a second method of tunnel construction appeared 为主句；called the counter-excavation method 为过去分词定语修饰 method（后置）；in which the tunnel was constructed from both ends 为 in which 定语从句；counter-excavation 意为 “对向开挖”。"
        },
        "words": [
            {"w": "appear", "pos": "v.", "def": "出现"},
            {"w": "counter-excavation", "pos": "n.", "def": "对向开挖"},
            {"w": "construct", "pos": "v.", "def": "建造"},
            {"w": "both ends", "pos": "phr.", "def": "两端"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": "It was used to cut through high mountains when the qanat method was not a practical alternative.",
        "zh": "当坎儿井法并非可行的替代方案时，这种方法就被用来穿凿高山。",
        "grammar": {
            "type": "被动 + when 时间从句",
            "note": "It was used to cut through high mountains 为被动加不定式；when the qanat method was not a practical alternative 为时间/条件状语从句；cut through 意为 “穿过、凿穿”；alternative 意为 “替代方案”。"
        },
        "words": [
            {"w": "cut through", "pos": "phr.", "def": "穿过；凿穿"},
            {"w": "practical", "pos": "adj.", "def": "可行的；实际的"},
            {"w": "alternative", "pos": "n.", "def": "替代方案"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "This method required greater planning and advanced knowledge of surveying, mathematics and geometry as both ends of a tunnel had to meet correctly at the center of the mountain.",
        "zh": "这种方法需要更周密的规划以及测量、数学和几何方面的高深知识，因为隧道的两端必须在山体中心准确会合。",
        "grammar": {
            "type": "as 原因从句",
            "note": "required greater planning and advanced knowledge of... 为主句；as both ends of a tunnel had to meet correctly 为 as 引导的原因状语从句；surveying 意为 “测量”，geometry 意为 “几何学”；meet 意为 “会合”。"
        },
        "words": [
            {"w": "require", "pos": "v.", "def": "需要"},
            {"w": "surveying", "pos": "n.", "def": "测量学；勘测"},
            {"w": "geometry", "pos": "n.", "def": "几何学"},
            {"w": "meet", "pos": "v.", "def": "会合；相接"}
        ]
    },
    {
        "id": 16,
        "para": 3,
        "en": "Adjustments to the direction of the tunnel also had to be made whenever builders encountered geological problems or when it deviated from its set path.",
        "zh": "每当建造者遇到地质问题、或隧道偏离既定路线时，还必须对隧道的方向进行调整。",
        "grammar": {
            "type": "被动 + whenever/when 时间从句",
            "note": "Adjustments... had to be made 为被动；whenever builders encountered geological problems or when it deviated from its set path 为两个并列时间状语从句；deviate from 意为 “偏离”；geological 意为 “地质的”，set path 意为 “既定路线”。"
        },
        "words": [
            {"w": "adjustment", "pos": "n.", "def": "调整"},
            {"w": "encounter", "pos": "v.", "def": "遇到；遭遇"},
            {"w": "geological", "pos": "adj.", "def": "地质的"},
            {"w": "deviate from", "pos": "phr.", "def": "偏离"}
        ]
    },
    {
        "id": 17,
        "para": 3,
        "en": "They constantly checked the tunnel" + RSQUO + "s advancing direction, for example, by looking back at the light that penetrated through the tunnel mouth, and made corrections whenever necessary.",
        "zh": "他们不断检查隧道的推进方向，例如通过回望从洞口透进来的光线，并在必要时进行修正。",
        "grammar": {
            "type": "by 方式 + that 定语从句 + 省略",
            "note": "constantly checked... and made corrections 为并列谓语；by looking back at the light 为方式状语；that penetrated through the tunnel mouth 为 that 定语从句修饰 light；whenever necessary 为省略的时间从句（= whenever it was necessary）；penetrate 意为 “穿透”。"
        },
        "words": [
            {"w": "constantly", "pos": "adv.", "def": "不断地"},
            {"w": "advancing", "pos": "adj.", "def": "推进的；前进的"},
            {"w": "penetrate", "pos": "v.", "def": "穿透"},
            {"w": "correction", "pos": "n.", "def": "修正；纠正"}
        ]
    },
    {
        "id": 18,
        "para": 3,
        "en": "Large deviations could happen, and they could result in one end of the tunnel not being usable.",
        "zh": "大的偏差有可能发生，而这可能导致隧道的一端无法使用。",
        "grammar": {
            "type": "and 并列 + result in doing",
            "note": "Large deviations could happen 为一分句；they could result in one end of the tunnel not being usable 为并列分句；result in doing 意为 “导致”，其中 one end... not being usable 为动名词复合结构；deviation 意为 “偏差”。"
        },
        "words": [
            {"w": "deviation", "pos": "n.", "def": "偏差；偏离"},
            {"w": "result in", "pos": "phr.", "def": "导致"},
            {"w": "usable", "pos": "adj.", "def": "可用的"}
        ]
    },
    {
        "id": 19,
        "para": 3,
        "en": "An inscription written on the side of a 428-meter tunnel, built by the Romans as part of the Saldae aqueduct system in modern-day Algeria, describes how the two teams of builders missed each other in the mountain and how the later construction of a lateral link between both corridors corrected the initial error.",
        "zh": "在一条428米长隧道的侧壁上刻有一段铭文，这条隧道是罗马人在今天的阿尔及利亚作为萨尔达伊输水系统的一部分而修建的；铭文描述了两支施工队如何在山体中彼此错过，以及后来如何在两条坑道之间修建横向连接通道来纠正最初的错误。",
        "grammar": {
            "type": "过去分词定语 + 两个 how 宾语从句",
            "note": "written on the side of a 428-meter tunnel 与 built by the Romans as part of... 为过去分词定语；describes how... and how... 为两个并列 how 宾语从句；lateral link 意为 “横向连接”，aqueduct 意为 “输水道”，inscription 意为 “铭文”。"
        },
        "words": [
            {"w": "inscription", "pos": "n.", "def": "铭文；碑文"},
            {"w": "aqueduct", "pos": "n.", "def": "输水道；渡槽"},
            {"w": "lateral", "pos": "adj.", "def": "横向的；侧面的"},
            {"w": "corridor", "pos": "n.", "def": "走廊；坑道"}
        ]
    },
    # Para 4
    {
        "id": 20,
        "para": 4,
        "en": "The Romans dug tunnels for their roads using the counter-excavation method, whenever they encountered obstacles such as hills or mountains that were too high for roads to pass over.",
        "zh": "每当遇到诸如太高而道路无法翻越的山丘或山脉之类的障碍时，罗马人就用对向开挖法为道路挖掘隧道。",
        "grammar": {
            "type": "现在分词状语 + whenever 从句 + that 定语从句",
            "note": "dug tunnels for their roads 为主句；using the counter-excavation method 为现在分词作方式状语；whenever they encountered obstacles 为时间状语从句；that were too high for roads to pass over 含 that 定语从句及 too...for...to... 结构；obstacle 意为 “障碍”。"
        },
        "words": [
            {"w": "obstacle", "pos": "n.", "def": "障碍"},
            {"w": "pass over", "pos": "phr.", "def": "越过；跨过"},
            {"w": "encounter", "pos": "v.", "def": "遇到"}
        ]
    },
    {
        "id": 21,
        "para": 4,
        "en": "An example is the 37-meter-long, 6-meter-high, Furlo Pass Tunnel built in Italy in 69" + DASH + "79 CE.",
        "zh": "一个例子是意大利于公元69至79年间修建的、长37米、高6米的富尔洛山口隧道。",
        "grammar": {
            "type": "过去分词定语",
            "note": "An example is the... Furlo Pass Tunnel 为主系表；built in Italy in 69-79 CE 为过去分词短语作定语修饰 Tunnel；37-meter-long, 6-meter-high 为复合形容词作定语；pass 意为 “山口”。"
        },
        "words": [
            {"w": "example", "pos": "n.", "def": "例子"},
            {"w": "pass", "pos": "n.", "def": "山口；隘口"},
            {"w": "tunnel", "pos": "n.", "def": "隧道"}
        ]
    },
    {
        "id": 22,
        "para": 4,
        "en": "Remarkably, a modern road still uses this tunnel today. Tunnels were also built for mineral extraction.",
        "zh": "值得注意的是，如今仍有一条现代道路使用这条隧道。隧道也曾被用于开采矿物。",
        "grammar": {
            "type": "简单句 + 被动",
            "note": "a modern road still uses this tunnel today 为一般现在时；Tunnels were also built for mineral extraction 为被动，for 表目的；mineral extraction 意为 “矿物开采”。"
        },
        "words": [
            {"w": "modern", "pos": "adj.", "def": "现代的"},
            {"w": "mineral extraction", "pos": "phr.", "def": "矿物开采"},
            {"w": "build", "pos": "v.", "def": "建造"}
        ]
    },
    {
        "id": 23,
        "para": 4,
        "en": "Miners would locate a mineral vein and then pursue it with shafts and tunnels underground.",
        "zh": "矿工会先找到一条矿脉，然后在地下用竖井和隧道去追踪开采它。",
        "grammar": {
            "type": "并列谓语",
            "note": "would locate a mineral vein and then pursue it 为并列谓语；with shafts and tunnels underground 为方式/地点状语；mineral vein 意为 “矿脉”，pursue 意为 “追踪、追寻”。"
        },
        "words": [
            {"w": "miner", "pos": "n.", "def": "矿工"},
            {"w": "locate", "pos": "v.", "def": "找到；定位"},
            {"w": "mineral vein", "pos": "phr.", "def": "矿脉"},
            {"w": "pursue", "pos": "v.", "def": "追踪；追寻"}
        ]
    },
    {
        "id": 24,
        "para": 4,
        "en": "Traces of such tunnels used to mine gold can still be found at the Dolaucothi mines in Wales.",
        "zh": "在威尔士的多劳科希矿场，至今仍能找到这类用于开采黄金的隧道遗迹。",
        "grammar": {
            "type": "过去分词定语 + 情态被动",
            "note": "Traces of such tunnels 为主语；used to mine gold 为过去分词短语作定语修饰 tunnels（此处 used to do 表 “被用来做”，非 “过去常常”）；can still be found 为情态被动；trace 意为 “痕迹、遗迹”。"
        },
        "words": [
            {"w": "trace", "pos": "n.", "def": "痕迹；遗迹"},
            {"w": "mine", "pos": "v.", "def": "开采"},
            {"w": "gold", "pos": "n.", "def": "黄金"}
        ]
    },
    {
        "id": 25,
        "para": 4,
        "en": "When the sole purpose of a tunnel was mineral extraction, construction required less planning, as the tunnel route was determined by the mineral vein.",
        "zh": "当一条隧道的唯一目的就是开采矿物时，其建造所需的规划就较少，因为隧道的走向是由矿脉决定的。",
        "grammar": {
            "type": "When 时间从句 + as 原因从句",
            "note": "When the sole purpose... was mineral extraction 为时间/条件从句；主句 construction required less planning；as the tunnel route was determined by the mineral vein 为原因从句，含被动；sole 意为 “唯一的”，route 意为 “路线、走向”。"
        },
        "words": [
            {"w": "sole", "pos": "adj.", "def": "唯一的"},
            {"w": "purpose", "pos": "n.", "def": "目的"},
            {"w": "route", "pos": "n.", "def": "路线；走向"},
            {"w": "determine", "pos": "v.", "def": "决定"}
        ]
    },
    # Para 5
    {
        "id": 26,
        "para": 5,
        "en": "Roman tunnel projects were carefully planned and carried out.",
        "zh": "罗马的隧道工程都经过精心的规划和实施。",
        "grammar": {
            "type": "并列被动谓语",
            "note": "were carefully planned and carried out 为并列被动谓语；carry out 意为 “实施、执行”；project 意为 “工程、项目”。"
        },
        "words": [
            {"w": "project", "pos": "n.", "def": "工程；项目"},
            {"w": "carefully", "pos": "adv.", "def": "仔细地"},
            {"w": "carry out", "pos": "phr.", "def": "实施；执行"}
        ]
    },
    {
        "id": 27,
        "para": 5,
        "en": "The length of time it took to construct a tunnel depended on the method being used and the type of rock being excavated.",
        "zh": "修建一条隧道所需的时间长短，取决于所采用的方法以及所开挖岩石的类型。",
        "grammar": {
            "type": "省略关系词定语从句 + 现在分词定语",
            "note": "The length of time (that) it took to construct a tunnel 为省略关系词的定语从句作主语；depended on... 为谓语；the method being used 与 the type of rock being excavated 各含现在分词的被动式定语；depend on 意为 “取决于”。"
        },
        "words": [
            {"w": "length of time", "pos": "phr.", "def": "时间长度"},
            {"w": "depend on", "pos": "phr.", "def": "取决于"},
            {"w": "excavate", "pos": "v.", "def": "开挖；发掘"}
        ]
    },
    {
        "id": 28,
        "para": 5,
        "en": "The qanat construction method was usually faster than the counter-excavation method as it was more straightforward.",
        "zh": "坎儿井建造法通常比对向开挖法更快，因为它更为简单直接。",
        "grammar": {
            "type": "比较 + as 原因从句",
            "note": "was usually faster than the counter-excavation method 为比较结构；as it was more straightforward 为原因从句；straightforward 意为 “简单直接的”。"
        },
        "words": [
            {"w": "usually", "pos": "adv.", "def": "通常"},
            {"w": "straightforward", "pos": "adj.", "def": "简单直接的"}
        ]
    },
    {
        "id": 29,
        "para": 5,
        "en": "This was because the mountain could be excavated not only from the tunnel mouths but also from shafts.",
        "zh": "这是因为山体不仅可以从洞口开挖，还可以从竖井开挖。",
        "grammar": {
            "type": "because + not only ... but also",
            "note": "This was because... 说明原因；could be excavated 为情态被动；not only from the tunnel mouths but also from shafts 为 not only...but also... 连接两个介词短语；tunnel mouth 意为 “洞口”。"
        },
        "words": [
            {"w": "excavate", "pos": "v.", "def": "开挖"},
            {"w": "tunnel mouth", "pos": "phr.", "def": "洞口；隧道口"},
            {"w": "not only ... but also", "pos": "phr.", "def": "不仅……而且"}
        ]
    },
    {
        "id": 30,
        "para": 5,
        "en": "The type of rock could also influence construction times.",
        "zh": "岩石的类型也会影响建造时间。",
        "grammar": {
            "type": "简单句",
            "note": "The type of rock 为主语；could also influence construction times 为谓语；influence 意为 “影响”；construction times 意为 “建造时间”。"
        },
        "words": [
            {"w": "influence", "pos": "v.", "def": "影响"},
            {"w": "rock", "pos": "n.", "def": "岩石"}
        ]
    },
    {
        "id": 31,
        "para": 5,
        "en": "When the rock was hard, the Romans employed a technique called fire quenching which consisted of heating the rock with fire, and then suddenly cooling it with cold water so that it would crack.",
        "zh": "当岩石坚硬时，罗马人会采用一种名为“火淬法”的技术，即先用火加热岩石，然后突然用冷水冷却，使其开裂。",
        "grammar": {
            "type": "When 从句 + 过去分词定语 + which 定语从句 + so that",
            "note": "When the rock was hard 为时间状语从句；called fire quenching 为过去分词定语；which consisted of heating... and then... cooling... 为定语从句，含并列动名词；so that it would crack 为目的状语从句；fire quenching 意为 “火淬法”，crack 意为 “开裂”。"
        },
        "words": [
            {"w": "employ", "pos": "v.", "def": "采用；使用"},
            {"w": "fire quenching", "pos": "phr.", "def": "火淬法"},
            {"w": "cool", "pos": "v.", "def": "冷却"},
            {"w": "crack", "pos": "v.", "def": "开裂；破裂"}
        ]
    },
    {
        "id": 32,
        "para": 5,
        "en": "Progress through hard rock could be very slow, and it was not uncommon for tunnels to take years, if not decades, to be built.",
        "zh": "在坚硬岩石中的进度可能非常缓慢，隧道耗时数年、乃至数十年才建成也并不罕见。",
        "grammar": {
            "type": "it 形式主语 + if not 插入",
            "note": "Progress through hard rock could be very slow 为一分句；it was not uncommon for tunnels to take years... to be built 为 it 形式主语句，for tunnels 为逻辑主语；if not decades 为插入语，表递进 “即使不是数十年”；uncommon 意为 “不寻常的”。"
        },
        "words": [
            {"w": "progress", "pos": "n.", "def": "进展"},
            {"w": "uncommon", "pos": "adj.", "def": "不寻常的；罕见的"},
            {"w": "decade", "pos": "n.", "def": "十年"},
            {"w": "if not", "pos": "phr.", "def": "即使不是；甚至"}
        ]
    },
    {
        "id": 33,
        "para": 5,
        "en": "Construction marks left on a Roman tunnel in Bologna show that the rate of advance through solid rock was 30 centimeters per day.",
        "zh": "博洛尼亚一条罗马隧道上留下的施工标记表明，在坚硬岩石中的推进速度为每天30厘米。",
        "grammar": {
            "type": "过去分词定语 + that 宾语从句",
            "note": "Construction marks left on a Roman tunnel in Bologna 为主语，left on... 为过去分词定语；show that... 为宾语从句；the rate of advance through solid rock 意为 “穿过坚硬岩石的推进速度”；per day 意为 “每天”。"
        },
        "words": [
            {"w": "construction mark", "pos": "phr.", "def": "施工标记"},
            {"w": "rate of advance", "pos": "phr.", "def": "推进速度"},
            {"w": "solid", "pos": "adj.", "def": "坚硬的；实心的"},
            {"w": "per day", "pos": "phr.", "def": "每天"}
        ]
    },
    {
        "id": 34,
        "para": 5,
        "en": "In contrast, the rate of advance of the Claudius tunnel can be calculated at 1.4 meters per day.",
        "zh": "相比之下，克劳狄乌斯隧道的推进速度可计算为每天1.4米。",
        "grammar": {
            "type": "In contrast + 情态被动",
            "note": "In contrast 意为 “相比之下”；the rate of advance of the Claudius tunnel can be calculated at 1.4 meters per day 为情态被动；calculate at 意为 “计算为”；与上句形成对比。"
        },
        "words": [
            {"w": "in contrast", "pos": "phr.", "def": "相比之下"},
            {"w": "calculate", "pos": "v.", "def": "计算"},
            {"w": "rate", "pos": "n.", "def": "速度；比率"}
        ]
    },
    {
        "id": 35,
        "para": 5,
        "en": "Most tunnels had inscriptions showing the names of patrons who ordered construction and sometimes the name of the architect.",
        "zh": "大多数隧道都刻有铭文，标明下令修建的资助者的名字，有时还有建筑师的名字。",
        "grammar": {
            "type": "现在分词定语 + who 定语从句",
            "note": "had inscriptions showing... 中 showing 为现在分词定语修饰 inscriptions；who ordered construction 为定语从句修饰 patrons；and sometimes the name of the architect 与 the names of patrons 并列作 showing 的宾语；patron 意为 “资助者”，architect 意为 “建筑师”。"
        },
        "words": [
            {"w": "inscription", "pos": "n.", "def": "铭文"},
            {"w": "patron", "pos": "n.", "def": "资助者；赞助人"},
            {"w": "order", "pos": "v.", "def": "下令；命令"},
            {"w": "architect", "pos": "n.", "def": "建筑师"}
        ]
    },
    {
        "id": 36,
        "para": 5,
        "en": "For example, the 1.4-kilometer " + CCEDIL + "evlik tunnel in Turkey, built to divert the floodwater threatening the harbor of the ancient city of Seleuceia Pieria, had inscriptions on the entrance, still visible today, that also indicate that the tunnel was started in 69 CE and was completed in 81 CE.",
        "zh": "例如，土耳其那条1.4公里长的切夫利克隧道，是为引开威胁古城塞琉西亚·皮埃里亚港口的洪水而修建的，其入口处刻有至今仍清晰可见的铭文，铭文还表明这条隧道于公元69年动工、公元81年竣工。",
        "grammar": {
            "type": "过去分词定语 + that 定语从句 + that 宾语从句",
            "note": "built to divert the floodwater... 为过去分词定语修饰 tunnel，其中 threatening the harbor... 为现在分词定语修饰 floodwater；that also indicate that... 为定语从句修饰 inscriptions，其后接 that 宾语从句（含并列被动）；still visible today 为插入的形容词短语；divert 意为 “引开、转移”。"
        },
        "words": [
            {"w": "divert", "pos": "v.", "def": "引开；转移"},
            {"w": "floodwater", "pos": "n.", "def": "洪水"},
            {"w": "harbor", "pos": "n.", "def": "港口"},
            {"w": "entrance", "pos": "n.", "def": "入口"}
        ]
    }
]

phrases = [
    {"w": "at regular intervals", "pos": "phr.", "def": "每隔一定距离/时间"},
    {"w": "pass on", "pos": "phr.", "def": "传递；传授"},
    {"w": "be equipped with", "pos": "phr.", "def": "配备有"},
    {"w": "cut through", "pos": "phr.", "def": "穿过；凿穿"},
    {"w": "deviate from", "pos": "phr.", "def": "偏离"},
    {"w": "result in", "pos": "phr.", "def": "导致"},
    {"w": "pass over", "pos": "phr.", "def": "越过；跨过"},
    {"w": "carry out", "pos": "phr.", "def": "实施；执行"},
    {"w": "depend on", "pos": "phr.", "def": "取决于"},
    {"w": "in contrast", "pos": "phr.", "def": "相比之下"}
]

questions = [
    {
        "title": "Questions 1" + DASH + "6",
        "type": "diagram_label",
        "instructions": [
            "Label the diagrams below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 1" + DASH + "6 on your answer sheet.",
            "The Persian Qanat Method / Cross-section of a Roman Qanat Shaft"
        ],
        "items": [
            {"number": 1, "prompt": "The Persian Qanat Method: 1 ______ to direct the tunnelling.", "answer": "posts", "evidence_sentence": 2},
            {"number": 2, "prompt": "water runs into a 2 ______ used by local people.", "answer": "canal", "evidence_sentence": 5},
            {"number": 3, "prompt": "vertical shafts to remove earth and for 3 ______.", "answer": "ventilation", "evidence_sentence": 4},
            {"number": 4, "prompt": "Cross-section of a Roman Qanat Shaft: 4 ______ made of wood or stone.", "answer": "lid", "evidence_sentence": 9},
            {"number": 5, "prompt": "5 ______ attached to the plumb line.", "answer": "weight", "evidence_sentence": 10},
            {"number": 6, "prompt": "handholds and footholds used for 6 ______.", "answer": "climbing", "evidence_sentence": 9}
        ]
    },
    {
        "title": "Questions 7" + DASH + "10",
        "type": "true_false_notgiven",
        "instructions": [
            "Do the following statements agree with the information given in Reading Passage 1?",
            "In boxes 7" + DASH + "10 on your answer sheet, write",
            "TRUE if the statement agrees with the information",
            "FALSE if the statement contradicts the information",
            "NOT GIVEN if there is no information on this"
        ],
        "items": [
            {"number": 7, "prompt": "The counter-excavation method completely replaced the qanat method in the 6th century BCE.", "answer": "FALSE", "evidence_sentence": 14},
            {"number": 8, "prompt": "Only experienced builders were employed to construct a tunnel using the counter-excavation method.", "answer": "NOT GIVEN", "evidence_sentence": 15},
            {"number": 9, "prompt": "The information about a problem that occurred during the construction of the Saldae aqueduct system was found in an ancient book.", "answer": "FALSE", "evidence_sentence": 19},
            {"number": 10, "prompt": "The mistake made by the builders of the Saldae aqueduct system was that the two parts of the tunnel failed to meet.", "answer": "TRUE", "evidence_sentence": 19}
        ]
    },
    {
        "title": "Questions 11" + DASH + "13",
        "type": "short_answer",
        "instructions": [
            "Answer the questions below.",
            "Choose NO MORE THAN TWO WORDS from the passage for each answer.",
            "Write your answers in boxes 11" + DASH + "13 on your answer sheet."
        ],
        "items": [
            {"number": 11, "prompt": "What type of mineral were the Dolaucothi mines in Wales built to extract?", "answer": "gold", "evidence_sentence": 24},
            {"number": 12, "prompt": "In addition to the patron, whose name might be carved onto a tunnel?", "answer": "(the) architect", "evidence_sentence": 35},
            {"number": 13, "prompt": "What part of Seleuceia Pieria was the " + CCEDIL + "evlik tunnel built to protect?", "answer": "(the) harbour", "evidence_sentence": 36}
        ]
    }
]

data = {
    "id": "c16-test4-p1",
    "source": "剑桥雅思16 Test 4 Passage 1",
    "title": "Roman tunnels",
    "subtitle": "The Romans, who once controlled areas of Europe, North Africa and Asia Minor, adopted the construction techniques of other civilizations to build tunnels in their territories",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c16-test4-p1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
