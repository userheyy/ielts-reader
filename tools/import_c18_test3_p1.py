# -*- coding: utf-8 -*-
"""Generate data/passages/c18-test3-p1.json (Materials to take us beyond concrete)."""
import json
import os

RSQUO = "’"
LSQUO = "‘"
DASH = "–"

sentences = [
    # Section A (para 1)
    {
        "id": 1,
        "para": 1,
        "en": "Concrete is the second most used substance in the global economy, after water " + DASH + " and one of the world" + RSQUO + "s biggest single sources of greenhouse gas emissions.",
        "zh": "混凝土是全球经济中使用量仅次于水的第二大物质——同时也是世界上温室气体排放的最大单一来源之一。",
        "grammar": {
            "type": "主系表 + 破折号补充",
            "note": "主干是 Concrete is the second most used substance in the global economy；after water 为插入的比较状语；破折号后 and one of the world" + RSQUO + "s biggest single sources of greenhouse gas emissions 为并列表语补充。"
        },
        "words": [
            {"w": "concrete", "pos": "n.", "def": "混凝土"},
            {"w": "substance", "pos": "n.", "def": "物质"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "The chemical process by which cement, the key ingredient of concrete, is created results in large quantities of carbon dioxide.",
        "zh": "生成水泥（混凝土的关键成分）的化学过程会产生大量的二氧化碳。",
        "grammar": {
            "type": "介词提前定语从句 + 同位语",
            "note": "主干是 The chemical process... results in large quantities of carbon dioxide；by which cement... is created 为“介词+关系代词”引导的定语从句修饰 process；the key ingredient of concrete 为 cement 的同位语。"
        },
        "words": [
            {"w": "cement", "pos": "n.", "def": "水泥"},
            {"w": "carbon dioxide", "pos": "phr.", "def": "二氧化碳"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "The UN estimates that there will be 9.8 billion people living on the planet by mid-century.",
        "zh": "联合国估计，到本世纪中叶，地球上将有98亿人口。",
        "grammar": {
            "type": "宾语从句 + there be",
            "note": "主干 The UN estimates that...，that 引导宾语从句 there will be 9.8 billion people living on the planet，living on the planet 为现在分词修饰 people；by mid-century 为时间状语。"
        },
        "words": [
            {"w": "estimate", "pos": "v.", "def": "估计；估算"},
            {"w": "billion", "pos": "num.", "def": "十亿"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "They will need somewhere to live.",
        "zh": "他们将需要地方居住。",
        "grammar": {
            "type": "主谓宾 + 不定式定语",
            "note": "主干是 They will need somewhere；to live 为不定式作定语修饰 somewhere。"
        },
        "words": [
            {"w": "somewhere", "pos": "adv./n.", "def": "某处；某个地方"},
            {"w": "need", "pos": "v.", "def": "需要"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "If concrete is the only answer to the construction of new cities, then carbon emissions will soar, aggravating global warming.",
        "zh": "如果混凝土是建造新城市的唯一答案，那么碳排放量将会激增，从而加剧全球变暖。",
        "grammar": {
            "type": "if 条件状语从句 + 现在分词结果状语",
            "note": "If concrete is the only answer to the construction of new cities 为条件状语从句；主句 carbon emissions will soar；aggravating global warming 为现在分词短语作结果状语。"
        },
        "words": [
            {"w": "soar", "pos": "v.", "def": "激增；猛涨"},
            {"w": "aggravate", "pos": "v.", "def": "加剧；使恶化"}
        ]
    },
    {
        "id": 6,
        "para": 1,
        "en": "And so scientists have started innovating with other materials, in a scramble for alternatives to a universal commodity that has underpinned our modern life for many years.",
        "zh": "因此，科学家们已经开始尝试用其他材料进行创新，争相寻找一种多年来一直支撑着我们现代生活的通用材料的替代品。",
        "grammar": {
            "type": "现在完成时 + 介词短语 + 定语从句",
            "note": "主干是 scientists have started innovating with other materials；in a scramble for alternatives to a universal commodity 为状语；that has underpinned our modern life for many years 为定语从句修饰 commodity。"
        },
        "words": [
            {"w": "scramble", "pos": "n.", "def": "争夺；抢先行动"},
            {"w": "underpin", "pos": "v.", "def": "支撑；巩固"}
        ]
    },
    # Section B (para 2)
    {
        "id": 7,
        "para": 2,
        "en": "The problem with replacing concrete is that it is so very good at what it does.",
        "zh": "替代混凝土的难题在于，它太擅长自己所承担的功用了。",
        "grammar": {
            "type": "表语从句 + 宾语从句",
            "note": "主干 The problem with replacing concrete is that...，that 引导表语从句 it is so very good at what it does，what it does 为宾语从句。"
        },
        "words": [
            {"w": "replace", "pos": "v.", "def": "替代；取代"},
            {"w": "be good at", "pos": "phr.", "def": "擅长"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "Chris Cheeseman, an engineering professor at Imperial College London, says the key thing to consider is the extent to which concrete is used around the world, and is likely to continue to be used.",
        "zh": "伦敦帝国理工学院的工程学教授克里斯·奇斯曼说，需要考虑的关键在于混凝土在全球被使用、并且可能继续被使用的程度。",
        "grammar": {
            "type": "同位语 + 宾语从句 + 介词提前定语从句",
            "note": "主干 Chris Cheeseman... says（后接省略 that 的宾语从句）the key thing to consider is the extent；an engineering professor at Imperial College London 为同位语；to which concrete is used around the world, and is likely to continue to be used 为定语从句修饰 extent。"
        },
        "words": [
            {"w": "extent", "pos": "n.", "def": "程度；范围"},
            {"w": "professor", "pos": "n.", "def": "教授"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": LSQUO + "Concrete is not a high-carbon product. Cement is high carbon, but concrete is not.",
        "zh": "“混凝土并不是一种高碳产品。水泥是高碳的，但混凝土不是。",
        "grammar": {
            "type": "主系表 + 转折并列",
            "note": "两句均为主系表结构；Concrete is not a high-carbon product 为独立判断；Cement is high carbon, but concrete is not 由 but 连接转折，后半 concrete is not 后省略 high carbon。"
        },
        "words": [
            {"w": "high-carbon", "pos": "adj.", "def": "高碳的"},
            {"w": "product", "pos": "n.", "def": "产品"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "But it is the scale on which it is used that makes it high carbon.",
        "zh": "但正是它被使用的规模之大，才使它变成了高碳的。",
        "grammar": {
            "type": "强调句 + 介词提前定语从句",
            "note": "it is the scale... that makes it high carbon 为强调句型，强调 the scale；on which it is used 为“介词+关系代词”定语从句修饰 scale。"
        },
        "words": [
            {"w": "scale", "pos": "n.", "def": "规模；程度"},
            {"w": "use", "pos": "v.", "def": "使用"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": "The sheer scale of manufacture is so huge, that is the issue." + RSQUO,
        "zh": "生产的规模实在太庞大了，这才是问题所在。”",
        "grammar": {
            "type": "主系表 + 总结句",
            "note": "The sheer scale of manufacture is so huge 为主系表，sheer 强调“纯粹的、十足的”；that is the issue 为总结性判断句。"
        },
        "words": [
            {"w": "sheer", "pos": "adj.", "def": "十足的；纯粹的"},
            {"w": "manufacture", "pos": "n.", "def": "制造；生产"}
        ]
    },
    # Section C (para 3)
    {
        "id": 12,
        "para": 3,
        "en": "Not only are the ingredients of concrete relatively cheap and found in abundance in most places around the globe, the stuff itself has marvellous properties: Portland cement, the vital component of concrete, is mouldable and pourable, but quickly sets hard.",
        "zh": "混凝土的原料不仅相对廉价、在全球大多数地方储量丰富，这种材料本身还具有绝佳的特性：作为混凝土关键成分的波特兰水泥可塑可浇，却又能迅速凝固变硬。",
        "grammar": {
            "type": "not only 倒装 + 冒号 + 同位语",
            "note": "Not only are the ingredients... cheap and found in abundance 为 not only 引起的部分倒装；主句 the stuff itself has marvellous properties；冒号后 Portland cement... is mouldable and pourable, but quickly sets hard，the vital component of concrete 为 Portland cement 的同位语。"
        },
        "words": [
            {"w": "in abundance", "pos": "phr.", "def": "大量地；丰富地"},
            {"w": "mouldable", "pos": "adj.", "def": "可塑的；可成型的"}
        ]
    },
    {
        "id": 13,
        "para": 3,
        "en": "Cheeseman also notes another advantage: concrete and steel have similar thermal expansion properties, so steel can be used to reinforce concrete, making it far stronger and more flexible as a building material than it could be on its own.",
        "zh": "奇斯曼还指出了另一个优点：混凝土和钢材的热膨胀特性相近，因此钢材可以用来加固混凝土，使它作为建筑材料比单独使用时坚固得多、灵活得多。",
        "grammar": {
            "type": "冒号解释 + 结果状语 + 现在分词状语 + 比较结构",
            "note": "主干 Cheeseman also notes another advantage；冒号后 concrete and steel have similar thermal expansion properties, so steel can be used to reinforce concrete，so 引出结果；making it far stronger and more flexible... than it could be on its own 为现在分词作结果状语，含比较结构。"
        },
        "words": [
            {"w": "thermal expansion", "pos": "phr.", "def": "热膨胀"},
            {"w": "reinforce", "pos": "v.", "def": "加固；增强"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": "According to Cheeseman, all these factors together make concrete hard to beat.",
        "zh": "奇斯曼认为，所有这些因素加在一起，使混凝土难以被超越。",
        "grammar": {
            "type": "make sth adj. 复合宾语",
            "note": "主干是 all these factors together make concrete hard to beat，make + 宾语 + 形容词 构成复合宾语，hard to beat 表“难以击败/超越”；According to Cheeseman 为来源状语。"
        },
        "words": [
            {"w": "factor", "pos": "n.", "def": "因素"},
            {"w": "beat", "pos": "v.", "def": "超越；击败"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": LSQUO + "Concrete is amazing stuff. Making anything with similar properties is going to be very difficult." + RSQUO,
        "zh": "“混凝土是种了不起的材料。要制造出具有类似特性的任何东西都将非常困难。”",
        "grammar": {
            "type": "主系表 + 动名词主语",
            "note": "第一句 Concrete is amazing stuff 为主系表；第二句 Making anything with similar properties is going to be very difficult，Making anything with similar properties 为动名词短语作主语。"
        },
        "words": [
            {"w": "amazing", "pos": "adj.", "def": "了不起的；惊人的"},
            {"w": "property", "pos": "n.", "def": "特性；性质"}
        ]
    },
    # Section D (para 4)
    {
        "id": 16,
        "para": 4,
        "en": "A possible alternative to concrete is wood.",
        "zh": "混凝土的一种可能替代品是木材。",
        "grammar": {
            "type": "主系表",
            "note": "主干是 A possible alternative to concrete is wood，to concrete 为介词短语修饰 alternative。"
        },
        "words": [
            {"w": "alternative", "pos": "n.", "def": "替代品；选择"},
            {"w": "wood", "pos": "n.", "def": "木材"}
        ]
    },
    {
        "id": 17,
        "para": 4,
        "en": "Making buildings from wood may seem like a rather medieval idea, but climate change is driving architects to turn to treated timber as a possible resource.",
        "zh": "用木材建造建筑物听起来也许是个相当中世纪的想法，但气候变化正促使建筑师把经处理的木材当作一种可能的资源。",
        "grammar": {
            "type": "动名词主语 + 转折 + drive sb to do",
            "note": "前句 Making buildings from wood may seem like a rather medieval idea，动名词短语作主语；but climate change is driving architects to turn to treated timber，drive sb to do 表“促使某人做”，turn to 表“求助于、转向”。"
        },
        "words": [
            {"w": "medieval", "pos": "adj.", "def": "中世纪的"},
            {"w": "architect", "pos": "n.", "def": "建筑师"}
        ]
    },
    {
        "id": 18,
        "para": 4,
        "en": "Recent years have seen the emergence of tall buildings constructed almost entirely from timber.",
        "zh": "近年来出现了几乎完全用木材建造的高层建筑。",
        "grammar": {
            "type": "拟人主语 + 过去分词定语",
            "note": "主干是 Recent years have seen the emergence of tall buildings，以时间作主语的拟人化表达；constructed almost entirely from timber 为过去分词短语修饰 buildings。"
        },
        "words": [
            {"w": "emergence", "pos": "n.", "def": "出现；兴起"},
            {"w": "timber", "pos": "n.", "def": "木材"}
        ]
    },
    {
        "id": 19,
        "para": 4,
        "en": "Vancouver, Vienna and Brumunddal in Norway are all home to constructed tall, wooden buildings.",
        "zh": "温哥华、维也纳以及挪威的布鲁蒙达尔都建有高大的木质建筑。",
        "grammar": {
            "type": "主系表",
            "note": "主干是 Vancouver, Vienna and Brumunddal in Norway are all home to... buildings，be home to 表“是……的所在地”；constructed tall, wooden 为修饰 buildings 的定语。"
        },
        "words": [
            {"w": "be home to", "pos": "phr.", "def": "是……的所在地"},
            {"w": "wooden", "pos": "adj.", "def": "木制的"}
        ]
    },
    # Section E (para 5)
    {
        "id": 20,
        "para": 5,
        "en": "Using wood to construct buildings, however, is not straightforward.",
        "zh": "然而，用木材建造建筑物并不简单。",
        "grammar": {
            "type": "动名词主语 + 插入语",
            "note": "主干是 Using wood to construct buildings is not straightforward，动名词短语作主语；however 为插入的转折语。"
        },
        "words": [
            {"w": "construct", "pos": "v.", "def": "建造；构造"},
            {"w": "straightforward", "pos": "adj.", "def": "简单的；直接的"}
        ]
    },
    {
        "id": 21,
        "para": 5,
        "en": "Wood expands as it absorbs moisture from the air and is susceptible to pests, not to mention fire.",
        "zh": "木材会因吸收空气中的水分而膨胀，还容易受虫害侵袭，更不用说火灾了。",
        "grammar": {
            "type": "as 时间状语从句 + 并列谓语",
            "note": "主干 Wood expands... and is susceptible to pests，两个谓语并列；as it absorbs moisture from the air 为 as 引导的时间/原因状语从句；not to mention fire 为插入语，表“更不用说”。"
        },
        "words": [
            {"w": "moisture", "pos": "n.", "def": "水分；湿气"},
            {"w": "susceptible", "pos": "adj.", "def": "易受影响的；易受感染的"}
        ]
    },
    {
        "id": 22,
        "para": 5,
        "en": "But treating wood and combining it with other materials can improve its properties.",
        "zh": "但对木材进行处理并将其与其他材料结合，可以改善它的性能。",
        "grammar": {
            "type": "动名词主语并列",
            "note": "主干是 treating wood and combining it with other materials can improve its properties，两个动名词短语并列作主语。"
        },
        "words": [
            {"w": "treat", "pos": "v.", "def": "处理；加工"},
            {"w": "combine", "pos": "v.", "def": "结合；组合"}
        ]
    },
    {
        "id": 23,
        "para": 5,
        "en": "Cross-laminated timber is engineered wood.",
        "zh": "交叉层压木材是一种工程木材。",
        "grammar": {
            "type": "主系表",
            "note": "主干是 Cross-laminated timber is engineered wood，engineered wood 为表语，engineered 为过去分词作定语，表“经过工程加工的”。"
        },
        "words": [
            {"w": "cross-laminated timber", "pos": "phr.", "def": "交叉层压木材（CLT）"},
            {"w": "engineered wood", "pos": "phr.", "def": "工程木材；复合木材"}
        ]
    },
    {
        "id": 24,
        "para": 5,
        "en": "An adhesive is used to stick layers of solid-sawn timber together, crosswise, to form building blocks.",
        "zh": "人们用一种黏合剂把整锯木材的各层交叉叠合黏在一起，形成建筑用的块材。",
        "grammar": {
            "type": "被动语态 + 不定式目的",
            "note": "主干是 An adhesive is used to stick layers of solid-sawn timber together，为被动语态；crosswise 为方式状语；to form building blocks 为不定式作目的状语。"
        },
        "words": [
            {"w": "adhesive", "pos": "n.", "def": "黏合剂；胶粘剂"},
            {"w": "crosswise", "pos": "adv.", "def": "交叉地；横向地"}
        ]
    },
    {
        "id": 25,
        "para": 5,
        "en": "This material is light but has the strength of concrete and steel.",
        "zh": "这种材料重量轻，却拥有混凝土和钢材般的强度。",
        "grammar": {
            "type": "主系表 + 转折并列谓语",
            "note": "主语 This material 带两个由 but 连接的谓语：is light 和 has the strength of concrete and steel。"
        },
        "words": [
            {"w": "light", "pos": "adj.", "def": "轻的"},
            {"w": "strength", "pos": "n.", "def": "强度；力量"}
        ]
    },
    {
        "id": 26,
        "para": 5,
        "en": "Construction experts say that wooden buildings can be constructed at a greater speed than ones of concrete and steel and the process, it seems, is quieter.",
        "zh": "建筑专家表示，木质建筑的建造速度比混凝土和钢结构建筑更快，而且这一过程似乎也更安静。",
        "grammar": {
            "type": "宾语从句 + 比较结构 + 插入语",
            "note": "主干 Construction experts say that...，that 引导宾语从句，含两个并列分句：wooden buildings can be constructed at a greater speed than ones of concrete and steel（比较结构）和 the process is quieter，it seems 为插入语。"
        },
        "words": [
            {"w": "speed", "pos": "n.", "def": "速度"},
            {"w": "process", "pos": "n.", "def": "过程"}
        ]
    },
    # Section F (para 6)
    {
        "id": 27,
        "para": 6,
        "en": "Stora Enso is Europe" + RSQUO + "s biggest supplier of cross-laminated timber, and its vice-president Markus Mannström reports that the company is seeing increasing demand globally for building in wood, with climate change concerns the key driver.",
        "zh": "斯道拉恩索是欧洲最大的交叉层压木材供应商，其副总裁马库斯·曼斯特伦称，该公司正看到全球范围内对木结构建筑需求的增长，而气候变化方面的担忧是主要推动力。",
        "grammar": {
            "type": "并列句 + 宾语从句 + with 复合结构",
            "note": "前句 Stora Enso is Europe" + RSQUO + "s biggest supplier；后句 its vice-president Markus Mannström reports that the company is seeing increasing demand...，that 引导宾语从句；with climate change concerns the key driver 为 with 复合结构。"
        },
        "words": [
            {"w": "supplier", "pos": "n.", "def": "供应商"},
            {"w": "demand", "pos": "n.", "def": "需求"}
        ]
    },
    {
        "id": 28,
        "para": 6,
        "en": "Finland, with its large forests, where Stora Enso is based, has been leading the way, but the company is seeing a rise in demand for its timber products across the world, including in Asia.",
        "zh": "拥有大片森林、也是斯道拉恩索总部所在地的芬兰一直走在前列，但该公司正看到全世界（包括亚洲）对其木材产品需求的上升。",
        "grammar": {
            "type": "with 插入 + 定语从句 + 转折并列",
            "note": "前句主干 Finland... has been leading the way，with its large forests 为插入状语，where Stora Enso is based 为定语从句修饰 forests；but the company is seeing a rise in demand... 为转折分句，including in Asia 为补充。"
        },
        "words": [
            {"w": "forest", "pos": "n.", "def": "森林"},
            {"w": "lead the way", "pos": "phr.", "def": "带头；引领"}
        ]
    },
    {
        "id": 29,
        "para": 6,
        "en": "Of course, using timber in a building also locks away the carbon that it absorbed as it grew.",
        "zh": "当然，在建筑中使用木材也把它在生长过程中所吸收的碳封存了起来。",
        "grammar": {
            "type": "动名词主语 + 定语从句 + as 时间状语从句",
            "note": "主干 using timber in a building also locks away the carbon，动名词短语作主语，lock away 表“封存”；that it absorbed 为定语从句修饰 carbon，as it grew 为时间状语从句。"
        },
        "words": [
            {"w": "lock away", "pos": "phr.", "def": "封存；锁住"},
            {"w": "absorb", "pos": "v.", "def": "吸收"}
        ]
    },
    {
        "id": 30,
        "para": 6,
        "en": "But even treated wood has its limitations and only when a wider range of construction projects has been proven in practice will it be possible to see wood as a real alternative to concrete in constructing tall buildings.",
        "zh": "但即便是经处理的木材也有其局限，只有当更广泛的建筑项目在实践中得到验证，才有可能把木材视为在建造高层建筑方面对混凝土的真正替代。",
        "grammar": {
            "type": "转折并列 + only when 引起倒装",
            "note": "前半 But even treated wood has its limitations；后半 only when a wider range of construction projects has been proven in practice will it be possible to see wood as...，only when 置于句首引起主句部分倒装（will it be possible），see A as B 表“把A看作B”。"
        },
        "words": [
            {"w": "limitation", "pos": "n.", "def": "局限；限制"},
            {"w": "prove", "pos": "v.", "def": "证明；证实"}
        ]
    },
    # Section G (para 7)
    {
        "id": 31,
        "para": 7,
        "en": "Fly ash and slag from iron ore are possible alternatives to cement in a concrete mix.",
        "zh": "粉煤灰和铁矿渣是混凝土配料中水泥的可能替代品。",
        "grammar": {
            "type": "主系表",
            "note": "主干是 Fly ash and slag from iron ore are possible alternatives to cement；from iron ore 修饰 slag，in a concrete mix 为地点/范围状语。"
        },
        "words": [
            {"w": "fly ash", "pos": "phr.", "def": "粉煤灰；飞灰"},
            {"w": "slag", "pos": "n.", "def": "矿渣；炉渣"}
        ]
    },
    {
        "id": 32,
        "para": 7,
        "en": "Fly ash, a byproduct of coal-burning power plants, can be incorporated into concrete mixes to make up as much as 15 to 30% of the cement, without harming the strength or durability of the resulting mix.",
        "zh": "粉煤灰是燃煤发电厂的副产品，可以掺入混凝土配料中，占到水泥的15%至30%，而不会损害所得混合料的强度或耐久性。",
        "grammar": {
            "type": "同位语 + 被动语态 + 不定式 + without 状语",
            "note": "主干 Fly ash... can be incorporated into concrete mixes，a byproduct of coal-burning power plants 为同位语；to make up as much as 15 to 30% of the cement 为不定式表结果；without harming the strength or durability 为伴随状语。"
        },
        "words": [
            {"w": "byproduct", "pos": "n.", "def": "副产品"},
            {"w": "durability", "pos": "n.", "def": "耐久性；耐用性"}
        ]
    },
    {
        "id": 33,
        "para": 7,
        "en": "Iron-ore slag, a byproduct of the iron-ore smelting process, can be used in a similar way.",
        "zh": "铁矿渣是炼铁过程的副产品，也可以以类似的方式使用。",
        "grammar": {
            "type": "同位语 + 被动语态",
            "note": "主干 Iron-ore slag... can be used in a similar way，为被动语态；a byproduct of the iron-ore smelting process 为同位语。"
        },
        "words": [
            {"w": "smelting", "pos": "n.", "def": "冶炼；熔炼"},
            {"w": "in a similar way", "pos": "phr.", "def": "以类似方式"}
        ]
    },
    {
        "id": 34,
        "para": 7,
        "en": "Their incorporation into concrete mixes has the potential to reduce greenhouse gas emissions.",
        "zh": "把它们掺入混凝土配料，有可能减少温室气体的排放。",
        "grammar": {
            "type": "主谓宾 + 不定式定语",
            "note": "主干是 Their incorporation into concrete mixes has the potential；to reduce greenhouse gas emissions 为不定式作定语修饰 potential。"
        },
        "words": [
            {"w": "incorporation", "pos": "n.", "def": "掺入；合并"},
            {"w": "emission", "pos": "n.", "def": "排放"}
        ]
    },
    {
        "id": 35,
        "para": 7,
        "en": "But Anna Surgenor, of the UK" + RSQUO + "s Green Building Council, notes that although these waste products can save carbon in the concrete mix, their use is not always straightforward.",
        "zh": "但英国绿色建筑委员会的安娜·瑟金诺指出，尽管这些废料能在混凝土配料中减少碳排放，它们的使用却并不总是那么简单。",
        "grammar": {
            "type": "宾语从句 + 内嵌 although 让步从句",
            "note": "主干 But Anna Surgenor... notes that...，of the UK" + RSQUO + "s Green Building Council 为插入的同位成分；that 引导宾语从句，其中 although these waste products can save carbon... 为让步状语从句，主句 their use is not always straightforward。"
        },
        "words": [
            {"w": "waste product", "pos": "phr.", "def": "废料；废弃产品"},
            {"w": "save", "pos": "v.", "def": "节省；减少"}
        ]
    },
    {
        "id": 36,
        "para": 7,
        "en": LSQUO + "It" + RSQUO + "s possible to replace the cement content in concrete with waste products to lower the overall carbon impact.",
        "zh": "“用废料替代混凝土中的水泥成分，从而降低整体的碳影响，是可行的。",
        "grammar": {
            "type": "it 形式主语 + 不定式主语 + 不定式目的",
            "note": "主干 It" + RSQUO + "s possible to replace the cement content in concrete with waste products，it 为形式主语，to replace... 为真正主语，replace A with B 表“用B替代A”；to lower the overall carbon impact 为不定式作目的状语。"
        },
        "words": [
            {"w": "content", "pos": "n.", "def": "含量；成分"},
            {"w": "impact", "pos": "n.", "def": "影响；冲击"}
        ]
    },
    {
        "id": 37,
        "para": 7,
        "en": "But there are several calculations that need to be considered across the entire life cycle of the building " + DASH + " these include factoring in where these materials are being shipped from.",
        "zh": "但有若干项计算需要在建筑物的整个生命周期中加以考虑——其中包括把这些材料从何处运来这一因素计算在内。",
        "grammar": {
            "type": "there be + 定语从句 + 破折号补充 + 宾语从句",
            "note": "主干 there are several calculations，that need to be considered across the entire life cycle 为定语从句修饰 calculations；破折号后 these include factoring in where these materials are being shipped from，where... 为宾语从句，factor in 表“把……计入考虑”。"
        },
        "words": [
            {"w": "calculation", "pos": "n.", "def": "计算；估算"},
            {"w": "life cycle", "pos": "phr.", "def": "生命周期"}
        ]
    },
    {
        "id": 38,
        "para": 7,
        "en": "If they are transported over long distances, using fossil fuels, the use of alternative materials might not make sense from an overall carbon reduction perspective." + RSQUO,
        "zh": "如果它们要用化石燃料长途运输，那么从整体减碳的角度来看，使用替代材料也许就没有意义了。”",
        "grammar": {
            "type": "if 条件从句 + 现在分词状语",
            "note": "If they are transported over long distances 为条件状语从句，using fossil fuels 为现在分词作伴随状语；主句 the use of alternative materials might not make sense，from an overall carbon reduction perspective 为角度状语。"
        },
        "words": [
            {"w": "transport", "pos": "v.", "def": "运输"},
            {"w": "fossil fuel", "pos": "phr.", "def": "化石燃料"}
        ]
    },
    # Section H (para 8)
    {
        "id": 39,
        "para": 8,
        "en": "While these technologies are all promising ideas, they are either unproven or based on materials that are not abundant.",
        "zh": "尽管这些技术都是有前景的设想，但它们要么尚未得到验证，要么依赖于并不丰富的材料。",
        "grammar": {
            "type": "while 让步从句 + either...or... + 定语从句",
            "note": "While these technologies are all promising ideas 为让步从句；主句 they are either unproven or based on materials，either...or... 表“要么……要么……”；that are not abundant 为定语从句修饰 materials。"
        },
        "words": [
            {"w": "promising", "pos": "adj.", "def": "有前景的；有希望的"},
            {"w": "unproven", "pos": "adj.", "def": "未经证实的"}
        ]
    },
    {
        "id": 40,
        "para": 8,
        "en": "In their overview of innovation in the concrete industry, Felix Preston and Johanna Lehne of the UK" + RSQUO + "s Royal Institute of International Affairs reached the conclusion that, " + LSQUO + "Some novel cements have been discussed for more than a decade within the research community, without breaking through.",
        "zh": "英国皇家国际事务研究所的费利克斯·普雷斯顿和约翰娜·莱内在对混凝土行业创新的综述中得出结论：“一些新型水泥在研究界已被讨论了十多年，却始终未能取得突破。",
        "grammar": {
            "type": "同位语从句 + without 状语",
            "note": "主干 Felix Preston and Johanna Lehne... reached the conclusion that...，In their overview of innovation 为状语；that 引导同位语从句 Some novel cements have been discussed for more than a decade；without breaking through 为伴随状语。"
        },
        "words": [
            {"w": "novel", "pos": "adj.", "def": "新型的；新颖的"},
            {"w": "break through", "pos": "phr.", "def": "取得突破"}
        ]
    },
    {
        "id": 41,
        "para": 8,
        "en": "At present, these alternatives are rarely as cost-effective as conventional cement, and they face raw-material shortages and resistance from customers." + RSQUO,
        "zh": "目前，这些替代品很少能像传统水泥那样具有成本效益，而且它们还面临原材料短缺和客户的抵触。”",
        "grammar": {
            "type": "as...as 同级比较 + 并列句",
            "note": "前句 these alternatives are rarely as cost-effective as conventional cement，as...as... 为同级比较，rarely 表否定；and they face raw-material shortages and resistance from customers 为并列分句。"
        },
        "words": [
            {"w": "cost-effective", "pos": "adj.", "def": "有成本效益的；划算的"},
            {"w": "resistance", "pos": "n.", "def": "抵触；阻力"}
        ]
    }
]

questions = [
    {
        "title": "Questions 1" + DASH + "4",
        "type": "matching_information",
        "instructions": [
            "Reading Passage 1 has eight sections, A" + DASH + "H.",
            "Which section contains the following information?",
            "Write the correct letter, A" + DASH + "H, in boxes 1" + DASH + "4 on your answer sheet."
        ],
        "items": [
            {"number": 1, "prompt": "an explanation of the industrial processes that create potential raw materials for concrete", "answer": "G", "evidence_sentence": 32},
            {"number": 2, "prompt": "a reference to the various locations where high-rise wooden buildings can be found", "answer": "D", "evidence_sentence": 19},
            {"number": 3, "prompt": "an indication of how widely available the raw materials of concrete are", "answer": "C", "evidence_sentence": 12},
            {"number": 4, "prompt": "the belief that more high-rise wooden buildings are needed before wood can be regarded as a viable construction material", "answer": "F", "evidence_sentence": 30}
        ]
    },
    {
        "title": "Questions 5" + DASH + "8",
        "type": "summary_completion",
        "instructions": [
            "Complete the summary below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 5" + DASH + "8 on your answer sheet.",
            "Making buildings with wood"
        ],
        "items": [
            {"number": 5, "prompt": "Wood is a traditional building material, but current environmental concerns are encouraging 5 ____ to use wood in modern construction projects.", "answer": "architects", "evidence_sentence": 17},
            {"number": 6, "prompt": "Using wood, however, has its challenges. For example, as 6 ____ in the atmosphere enters wood, it increases in size.", "answer": "moisture", "evidence_sentence": 21},
            {"number": 7, "prompt": "In one process, 7 ____ of solid wood are glued together to create building blocks.", "answer": "layers", "evidence_sentence": 24},
            {"number": 8, "prompt": "Experts say that wooden buildings are an improvement on those made of concrete and steel in terms of the 8 ____ with which they can be constructed and how much noise is generated by the process.", "answer": "speed", "evidence_sentence": 26}
        ]
    },
    {
        "title": "Questions 9" + DASH + "13",
        "type": "matching_features",
        "instructions": [
            "Look at the following statements (Questions 9" + DASH + "13) and the list of people below.",
            "Match each statement with the correct person, A, B, C or D.",
            "Write the correct letter, A, B, C or D, in boxes 9" + DASH + "13 on your answer sheet.",
            "NB You may use any letter more than once.",
            "List of People",
            "A Chris Cheeseman",
            "B Markus Mannström",
            "C Anna Surgenor",
            "D Felix Preston and Johanna Lehne"
        ],
        "items": [
            {"number": 9, "prompt": "The environmental advantage of cement alternatives may not be as great as initially assumed.", "answer": "C", "evidence_sentence": 38},
            {"number": 10, "prompt": "It would be hard to create a construction alternative to concrete that offers so many comparable benefits.", "answer": "A", "evidence_sentence": 15},
            {"number": 11, "prompt": "Worries about the environment have led to increased interest in wood as a construction material.", "answer": "B", "evidence_sentence": 27},
            {"number": 12, "prompt": "Expense has been a factor in the negative response to the development of new cements.", "answer": "D", "evidence_sentence": 41},
            {"number": 13, "prompt": "The environmental damage caused by concrete is due to it being produced in large quantities.", "answer": "A", "evidence_sentence": 10}
        ]
    }
]

phrases = [
    {"w": "concrete", "pos": "n.", "def": "混凝土"},
    {"w": "cement", "pos": "n.", "def": "水泥"},
    {"w": "greenhouse gas emissions", "pos": "n.", "def": "温室气体排放"},
    {"w": "Portland cement", "pos": "n.", "def": "波特兰水泥（普通硅酸盐水泥）"},
    {"w": "cross-laminated timber", "pos": "n.", "def": "交叉层压木材（CLT）"},
    {"w": "engineered wood", "pos": "n.", "def": "工程木材；复合木材"},
    {"w": "thermal expansion", "pos": "n.", "def": "热膨胀"},
    {"w": "fly ash", "pos": "n.", "def": "粉煤灰；飞灰"},
    {"w": "iron-ore slag", "pos": "n.", "def": "铁矿渣"},
    {"w": "life cycle", "pos": "n.", "def": "生命周期"}
]

data = {
    "id": "c18-test3-p1",
    "source": "剑桥雅思18 · Test 3 · Passage 1",
    "title": "Materials to take us beyond concrete",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "subtitle": "Concrete is everywhere, but it" + RSQUO + "s bad for the planet, generating large amounts of carbon dioxide " + DASH + " alternatives are being developed",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c18-test3-p1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
