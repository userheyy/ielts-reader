# -*- coding: utf-8 -*-
"""Generate data/passages/c15-test4-p1.json (The return of the huarango)."""
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
        "en": "The south coast of Peru is a narrow, 2,000-kilometre-long strip of desert squeezed between the Andes and the Pacific Ocean.",
        "zh": "秘鲁南部海岸是一条狭长的、长达2000公里的沙漠地带，夹在安第斯山脉与太平洋之间。",
        "grammar": {
            "type": "过去分词定语",
            "note": "squeezed between the Andes and the Pacific Ocean 为过去分词短语作定语修饰 a narrow... strip of desert；2,000-kilometre-long 为复合形容词。"
        },
        "words": [
            {"w": "coast", "pos": "n.", "def": "海岸"},
            {"w": "strip", "pos": "n.", "def": "狭长地带"},
            {"w": "squeeze", "pos": "v.", "def": "挤；压"},
            {"w": "the Andes", "pos": "phr.", "def": "安第斯山脉"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "It is also one of the most fragile ecosystems on Earth.",
        "zh": "它也是地球上最脆弱的生态系统之一。",
        "grammar": {
            "type": "主系表",
            "note": "one of the most fragile ecosystems 为 “最……之一” 结构；on Earth 为介词短语作定语。"
        },
        "words": [
            {"w": "fragile", "pos": "adj.", "def": "脆弱的"},
            {"w": "ecosystem", "pos": "n.", "def": "生态系统"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "It hardly ever rains there, and the only year-round source of water is located tens of metres below the surface.",
        "zh": "那里几乎从不下雨，唯一常年可用的水源位于地表以下数十米处。",
        "grammar": {
            "type": "并列句 + 被动",
            "note": "and 连接两分句；is located 为被动，表 “位于”；hardly ever 意为 “几乎从不”；year-round 意为 “全年的、常年的”。"
        },
        "words": [
            {"w": "hardly ever", "pos": "phr.", "def": "几乎从不"},
            {"w": "year-round", "pos": "adj.", "def": "全年的；常年的"},
            {"w": "be located", "pos": "phr.", "def": "位于"},
            {"w": "surface", "pos": "n.", "def": "表面；地表"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "This is why the huarango tree is so suited to life there: it has the longest roots of any tree in the world.",
        "zh": "这就是为什么牧豆树（huarango）如此适应那里的生活：它拥有世界上所有树木中最长的根。",
        "grammar": {
            "type": "表语从句 + 冒号说明",
            "note": "This is why... 为 why 引导的表语从句；冒号后 it has the longest roots... 说明原因；be suited to 意为 “适合、适应”；of any tree 意为 “在所有树中”。"
        },
        "words": [
            {"w": "huarango", "pos": "n.", "def": "牧豆树（南美耐旱树种）"},
            {"w": "be suited to", "pos": "phr.", "def": "适合；适应"},
            {"w": "root", "pos": "n.", "def": "根"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "They stretch down 50" + DASH + "80 metres and, as well as sucking up water for the tree, they bring it into the higher subsoil, creating a water source for other plant life.",
        "zh": "它们向下延伸50至80米，除了为树木吸取水分之外，还把水带到较浅的底土中，为其他植物创造出一处水源。",
        "grammar": {
            "type": "并列谓语 + as well as + 现在分词状语",
            "note": "stretch down... and... bring it into... 为并列谓语；as well as sucking up water... 为插入的伴随成分；creating a water source... 为现在分词短语作结果状语。"
        },
        "words": [
            {"w": "stretch down", "pos": "phr.", "def": "向下延伸"},
            {"w": "suck up", "pos": "phr.", "def": "吸上来；吸取"},
            {"w": "subsoil", "pos": "n.", "def": "底土；下层土"},
            {"w": "as well as", "pos": "phr.", "def": "除……之外；以及"}
        ]
    },
    # Para 2
    {
        "id": 6,
        "para": 2,
        "en": "Dr David Beresford-Jones, archaeobotanist at Cambridge University, has been studying the role of the huarango tree in landscape change in the Lower Ica Valley in southern Peru.",
        "zh": "剑桥大学的考古植物学家戴维·贝雷斯福德-琼斯博士一直在研究牧豆树在秘鲁南部下伊卡河谷地貌变化中所起的作用。",
        "grammar": {
            "type": "同位语 + 现在完成进行时",
            "note": "archaeobotanist at Cambridge University 为主语的同位语；has been studying 为现在完成进行时，表持续动作；the role of... in... 意为 “……在……中的作用”。"
        },
        "words": [
            {"w": "archaeobotanist", "pos": "n.", "def": "考古植物学家"},
            {"w": "role", "pos": "n.", "def": "作用；角色"},
            {"w": "landscape", "pos": "n.", "def": "地貌；景观"},
            {"w": "valley", "pos": "n.", "def": "山谷；河谷"}
        ]
    },
    {
        "id": 7,
        "para": 2,
        "en": "He believes the huarango was key to the ancient people" + RSQUO + "s diet and, because it could reach deep water sources, it allowed local people to withstand years of drought when their other crops failed.",
        "zh": "他认为牧豆树是古代人饮食中的关键，而且由于它能触及深层水源，它使当地人在其他作物歉收时也能挺过多年的干旱。",
        "grammar": {
            "type": "宾语从句 + 原因状语从句 + 时间状语从句",
            "note": "believes (that) the huarango was key... and... it allowed... 为并列宾语从句；because it could reach... 为原因状语从句；when their other crops failed 为时间状语从句；allow sb to do 意为 “使某人能够做”。"
        },
        "words": [
            {"w": "key to", "pos": "phr.", "def": "……的关键"},
            {"w": "diet", "pos": "n.", "def": "饮食"},
            {"w": "withstand", "pos": "v.", "def": "抵御；经受住"},
            {"w": "drought", "pos": "n.", "def": "干旱"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "But over the centuries huarango trees were gradually replaced with crops.",
        "zh": "但几个世纪以来，牧豆树逐渐被农作物所取代。",
        "grammar": {
            "type": "被动语态",
            "note": "were gradually replaced with 为被动结构；replace A with B 的被动形式；over the centuries 意为 “几个世纪以来”。"
        },
        "words": [
            {"w": "gradually", "pos": "adv.", "def": "逐渐地"},
            {"w": "replace with", "pos": "phr.", "def": "用……取代"},
            {"w": "crop", "pos": "n.", "def": "作物；庄稼"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "Cutting down native woodland leads to erosion, as there is nothing to keep the soil in place.",
        "zh": "砍伐本地林地会导致水土流失，因为没有任何东西能把土壤固定住。",
        "grammar": {
            "type": "动名词主语 + 原因状语从句",
            "note": "Cutting down native woodland 为动名词短语作主语；as there is nothing to keep... 为原因状语从句；lead to 意为 “导致”；keep... in place 意为 “使……固定”。"
        },
        "words": [
            {"w": "cut down", "pos": "phr.", "def": "砍伐；砍倒"},
            {"w": "woodland", "pos": "n.", "def": "林地"},
            {"w": "erosion", "pos": "n.", "def": "侵蚀；水土流失"},
            {"w": "in place", "pos": "phr.", "def": "在原处；固定"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "So when the huarangos go, the land turns into a desert. Nothing grows at all in the Lower Ica Valley now.",
        "zh": "因此，牧豆树一旦消失，土地就变成了沙漠。如今，下伊卡河谷中根本什么都不长。",
        "grammar": {
            "type": "时间状语从句",
            "note": "when the huarangos go 为时间状语从句；turn into 意为 “变成”；at all 强化否定 “根本（不）”。"
        },
        "words": [
            {"w": "turn into", "pos": "phr.", "def": "变成"},
            {"w": "desert", "pos": "n.", "def": "沙漠"},
            {"w": "at all", "pos": "phr.", "def": "（用于否定）根本；丝毫"}
        ]
    },
    # Para 3
    {
        "id": 11,
        "para": 3,
        "en": "For centuries the huarango tree was vital to the people of the neighbouring Middle Ica Valley too.",
        "zh": "几个世纪以来，牧豆树对邻近的中伊卡河谷的人们同样至关重要。",
        "grammar": {
            "type": "主系表",
            "note": "be vital to 意为 “对……至关重要”；neighbouring 意为 “邻近的”；For centuries 为时间状语。"
        },
        "words": [
            {"w": "vital", "pos": "adj.", "def": "至关重要的"},
            {"w": "neighbouring", "pos": "adj.", "def": "邻近的"},
            {"w": "century", "pos": "n.", "def": "世纪"}
        ]
    },
    {
        "id": 12,
        "para": 3,
        "en": "They grew vegetables under it and ate products made from its seed pods.",
        "zh": "他们在树下种植蔬菜，并食用用其种荚制成的产品。",
        "grammar": {
            "type": "并列谓语 + 过去分词定语",
            "note": "grew... and ate... 为并列谓语；made from its seed pods 为过去分词短语作定语修饰 products；seed pod 意为 “种荚”。"
        },
        "words": [
            {"w": "vegetable", "pos": "n.", "def": "蔬菜"},
            {"w": "product", "pos": "n.", "def": "产品"},
            {"w": "seed pod", "pos": "phr.", "def": "种荚；豆荚"}
        ]
    },
    {
        "id": 13,
        "para": 3,
        "en": "Its leaves and bark were used for herbal remedies, while its branches were used for charcoal for cooking and heating, and its trunk was used to build houses.",
        "zh": "它的叶子和树皮被用作草药，树枝被烧成木炭用于做饭和取暖，树干则被用来建造房屋。",
        "grammar": {
            "type": "并列被动 + while 对比",
            "note": "三个并列被动分句（were used for/to...）；while 引导对比；herbal remedies 意为 “草药”；charcoal 意为 “木炭”。"
        },
        "words": [
            {"w": "bark", "pos": "n.", "def": "树皮"},
            {"w": "herbal remedy", "pos": "phr.", "def": "草药；草药疗法"},
            {"w": "charcoal", "pos": "n.", "def": "木炭"},
            {"w": "trunk", "pos": "n.", "def": "树干"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": "But now it is disappearing rapidly.",
        "zh": "但如今它正在迅速消失。",
        "grammar": {
            "type": "现在进行时",
            "note": "is disappearing 为现在进行时，表正在发生；rapidly 意为 “迅速地”。"
        },
        "words": [
            {"w": "disappear", "pos": "v.", "def": "消失"},
            {"w": "rapidly", "pos": "adv.", "def": "迅速地"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "The majority of the huarango forests in the valley have already been cleared for fuel and agriculture " + DASH + " initially, these were smallholdings, but now they" + RSQUO + "re huge farms producing crops for the international market.",
        "zh": "河谷中大部分牧豆树林已经为了燃料和农业而被清除——起初这些是小块农田，但如今已是为国际市场生产作物的大型农场。",
        "grammar": {
            "type": "被动 + 破折号转折",
            "note": "have already been cleared 为现在完成时被动；破折号后 initially, these were... but now they're... 为转折说明；producing crops... 为现在分词短语作定语修饰 huge farms。"
        },
        "words": [
            {"w": "the majority of", "pos": "phr.", "def": "大多数的"},
            {"w": "clear", "pos": "v.", "def": "清除；砍伐"},
            {"w": "initially", "pos": "adv.", "def": "起初；最初"},
            {"w": "smallholding", "pos": "n.", "def": "小块农地；小农场"}
        ]
    },
    # Para 4
    {
        "id": 16,
        "para": 4,
        "en": LSQUO + "Of the forests that were here 1,000 years ago, 99 per cent have already gone," + RSQUO + " says botanist Oliver Whaley from Kew Gardens in London, who, together with ethnobotanist Dr William Milliken, is running a pioneering project to protect and restore the rapidly disappearing habitat.",
        "zh": "“1000年前生长在这里的森林，如今已有99%消失了，”来自伦敦邱园的植物学家奥利弗·惠利说，他正与民族植物学家威廉·米利肯博士一起开展一个旨在保护和恢复这一迅速消失的栖息地的开创性项目。",
        "grammar": {
            "type": "定语从句 + 非限定性定语从句",
            "note": "that were here 1,000 years ago 为定语从句修饰 the forests；who... is running a pioneering project 为非限定性定语从句修饰 Oliver Whaley；to protect and restore... 为不定式作定语；ethnobotanist 意为 “民族植物学家”。"
        },
        "words": [
            {"w": "botanist", "pos": "n.", "def": "植物学家"},
            {"w": "ethnobotanist", "pos": "n.", "def": "民族植物学家"},
            {"w": "pioneering", "pos": "adj.", "def": "开创性的；先驱的"},
            {"w": "restore", "pos": "v.", "def": "恢复；修复"},
            {"w": "habitat", "pos": "n.", "def": "栖息地"}
        ]
    },
    {
        "id": 17,
        "para": 4,
        "en": "In order to succeed, Whaley needs to get the local people on board, and that has meant overcoming local prejudices.",
        "zh": "为了取得成功，惠利需要争取当地人的支持，而这意味着要克服当地人的偏见。",
        "grammar": {
            "type": "不定式状语 + 并列句",
            "note": "In order to succeed 为目的状语；and that has meant overcoming... 为并列分句，overcoming 为动名词作宾语；get sb on board 意为 “争取某人支持、使某人参与”。"
        },
        "words": [
            {"w": "in order to", "pos": "phr.", "def": "为了"},
            {"w": "get on board", "pos": "phr.", "def": "争取支持；使加入"},
            {"w": "overcome", "pos": "v.", "def": "克服"},
            {"w": "prejudice", "pos": "n.", "def": "偏见"}
        ]
    },
    {
        "id": 18,
        "para": 4,
        "en": LSQUO + "Increasingly aspirational communities think that if you plant food trees in your home or street, it shows you are poor, and still need to grow your own food," + RSQUO + " he says.",
        "zh": "“越来越有抱负、追求上进的社区认为，如果你在自家院子或街道上种食用树木，就表明你很穷、还得自己种粮食，”他说。",
        "grammar": {
            "type": "宾语从句 + 条件从句",
            "note": "think that... 后接宾语从句；从句内 if you plant... 为条件状语从句，主句 it shows (that) you are poor... 含省略连词的宾语从句；aspirational 意为 “有抱负的、追求上进的”。"
        },
        "words": [
            {"w": "increasingly", "pos": "adv.", "def": "越来越；日益"},
            {"w": "aspirational", "pos": "adj.", "def": "有抱负的；追求上进的"},
            {"w": "community", "pos": "n.", "def": "社区；群体"},
            {"w": "plant", "pos": "v.", "def": "种植"}
        ]
    },
    {
        "id": 19,
        "para": 4,
        "en": "In order to stop the Middle Ica Valley going the same way as the Lower Ica Valley, Whaley is encouraging locals to love the huarangos again.",
        "zh": "为了阻止中伊卡河谷重蹈下伊卡河谷的覆辙，惠利正在鼓励当地人重新爱上牧豆树。",
        "grammar": {
            "type": "不定式状语",
            "note": "In order to stop... going... 为目的状语，stop sb/sth doing 意为 “阻止……做”；go the same way as 意为 “走上与……相同的路、重蹈覆辙”；encourage sb to do 意为 “鼓励某人做”。"
        },
        "words": [
            {"w": "go the same way as", "pos": "phr.", "def": "重蹈……的覆辙"},
            {"w": "encourage", "pos": "v.", "def": "鼓励"},
            {"w": "local", "pos": "n.", "def": "当地人"}
        ]
    },
    {
        "id": 20,
        "para": 4,
        "en": LSQUO + "It" + RSQUO + "s a process of cultural resuscitation," + RSQUO + " he says.",
        "zh": "“这是一个文化复苏的过程，”他说。",
        "grammar": {
            "type": "主系表",
            "note": "a process of cultural resuscitation 为表语；resuscitation 意为 “复苏、复兴”。"
        },
        "words": [
            {"w": "process", "pos": "n.", "def": "过程"},
            {"w": "cultural", "pos": "adj.", "def": "文化的"},
            {"w": "resuscitation", "pos": "n.", "def": "复苏；复兴"}
        ]
    },
    {
        "id": 21,
        "para": 4,
        "en": "He has already set up a huarango festival to reinstate a sense of pride in their eco-heritage, and has helped local schoolchildren plant thousands of trees.",
        "zh": "他已经创办了一个牧豆树节，以重新唤起人们对其生态遗产的自豪感，并帮助当地学童种下了成千上万棵树。",
        "grammar": {
            "type": "并列谓语 + 不定式目的状语",
            "note": "has already set up... and has helped... 为并列谓语；to reinstate a sense of pride... 为目的状语；help sb do 结构；eco-heritage 意为 “生态遗产”。"
        },
        "words": [
            {"w": "set up", "pos": "phr.", "def": "创办；建立"},
            {"w": "reinstate", "pos": "v.", "def": "使恢复；重新确立"},
            {"w": "a sense of pride", "pos": "phr.", "def": "自豪感"},
            {"w": "eco-heritage", "pos": "n.", "def": "生态遗产"}
        ]
    },
    # Para 5
    {
        "id": 22,
        "para": 5,
        "en": LSQUO + "In order to get people interested in habitat restoration, you need to plant a tree that is useful to them," + RSQUO + " says Whaley.",
        "zh": "“为了让人们对栖息地恢复产生兴趣，你需要种植一种对他们有用的树，”惠利说。",
        "grammar": {
            "type": "不定式状语 + 定语从句",
            "note": "In order to get people interested in... 为目的状语，get sb interested in 意为 “使某人对……感兴趣”；that is useful to them 为定语从句修饰 a tree。"
        },
        "words": [
            {"w": "restoration", "pos": "n.", "def": "恢复；修复"},
            {"w": "useful", "pos": "adj.", "def": "有用的"},
            {"w": "get interested in", "pos": "phr.", "def": "对……产生兴趣"}
        ]
    },
    {
        "id": 23,
        "para": 5,
        "en": "So, he has been working with local families to attempt to create a sustainable income from the huarangos by turning their products into foodstuffs.",
        "zh": "因此，他一直与当地家庭合作，试图通过把牧豆树的产品转化为食品，从而创造出一份可持续的收入。",
        "grammar": {
            "type": "不定式目的 + 方式状语",
            "note": "to attempt to create... 为目的状语；by turning their products into foodstuffs 为方式状语；turn A into B 意为 “把 A 变成 B”；work with 意为 “与……合作”。"
        },
        "words": [
            {"w": "attempt to", "pos": "phr.", "def": "试图；尝试"},
            {"w": "sustainable", "pos": "adj.", "def": "可持续的"},
            {"w": "income", "pos": "n.", "def": "收入"},
            {"w": "foodstuff", "pos": "n.", "def": "食品；食物"}
        ]
    },
    {
        "id": 24,
        "para": 5,
        "en": LSQUO + "Boil up the beans and you get this thick brown syrup like molasses.",
        "zh": "“把豆子煮开，你就会得到一种像糖蜜一样浓稠的棕色糖浆。",
        "grammar": {
            "type": "祈使句 + and 结果",
            "note": "“祈使句 + and + 陈述句” 结构，表 “如果……就……”；like molasses 为介词短语作定语；boil up 意为 “煮开”。"
        },
        "words": [
            {"w": "boil up", "pos": "phr.", "def": "煮开；煮沸"},
            {"w": "bean", "pos": "n.", "def": "豆子"},
            {"w": "syrup", "pos": "n.", "def": "糖浆"},
            {"w": "molasses", "pos": "n.", "def": "糖蜜；糖浆"}
        ]
    },
    {
        "id": 25,
        "para": 5,
        "en": "You can also use it in drinks, soups or stews." + RSQUO + " The pods can be ground into flour to make cakes, and the seeds roasted into a sweet, chocolatey " + LSQUO + "coffee" + RSQUO + ".",
        "zh": "你也可以把它用在饮料、汤或炖菜里。”豆荚可以磨成面粉做蛋糕，种子则可烘烤成一种甜甜的、带巧克力味的“咖啡”。",
        "grammar": {
            "type": "被动 + 并列省略",
            "note": "can be ground into flour 为被动；the seeds (can be) roasted into... 承前省略；grind into 意为 “磨成”，roast into 意为 “烘烤成”。"
        },
        "words": [
            {"w": "stew", "pos": "n.", "def": "炖菜；炖肉"},
            {"w": "grind into", "pos": "phr.", "def": "磨成"},
            {"w": "flour", "pos": "n.", "def": "面粉"},
            {"w": "roast", "pos": "v.", "def": "烘烤；焙"}
        ]
    },
    {
        "id": 26,
        "para": 5,
        "en": LSQUO + "It" + RSQUO + "s packed full of vitamins and minerals," + RSQUO + " Whaley says.",
        "zh": "“它富含维生素和矿物质，”惠利说。",
        "grammar": {
            "type": "主系表",
            "note": "be packed full of 意为 “充满、富含”；vitamins and minerals 为并列宾语。"
        },
        "words": [
            {"w": "be packed full of", "pos": "phr.", "def": "充满；富含"},
            {"w": "vitamin", "pos": "n.", "def": "维生素"},
            {"w": "mineral", "pos": "n.", "def": "矿物质"}
        ]
    },
    # Para 6
    {
        "id": 27,
        "para": 6,
        "en": "And some farmers are already planting huarangos.",
        "zh": "而且，一些农民已经在种植牧豆树了。",
        "grammar": {
            "type": "现在进行时",
            "note": "are already planting 为现在进行时，表正在进行的动作；already 意为 “已经”。"
        },
        "words": [
            {"w": "farmer", "pos": "n.", "def": "农民"},
            {"w": "already", "pos": "adv.", "def": "已经"}
        ]
    },
    {
        "id": 28,
        "para": 6,
        "en": "Alberto Benevides, owner of Ica Valley" + RSQUO + "s only certified organic farm, which Whaley helped set up, has been planting the tree for 13 years.",
        "zh": "阿尔贝托·贝内维德斯是伊卡河谷唯一一家经认证的有机农场的主人——该农场是在惠利帮助下建立的——他已经种这种树13年了。",
        "grammar": {
            "type": "同位语 + 非限定性定语从句",
            "note": "owner of Ica Valley's only certified organic farm 为主语的同位语；which Whaley helped set up 为非限定性定语从句修饰 farm；has been planting... for 13 years 为现在完成进行时。"
        },
        "words": [
            {"w": "owner", "pos": "n.", "def": "拥有者；主人"},
            {"w": "certified", "pos": "adj.", "def": "经认证的"},
            {"w": "organic", "pos": "adj.", "def": "有机的"},
            {"w": "set up", "pos": "phr.", "def": "建立；创办"}
        ]
    },
    {
        "id": 29,
        "para": 6,
        "en": "He produces syrup and flour, and sells these products at an organic farmers" + RSQUO + " market in Lima.",
        "zh": "他生产糖浆和面粉，并在利马的一个有机农贸市场上销售这些产品。",
        "grammar": {
            "type": "并列谓语",
            "note": "produces... and sells... 为并列谓语；at an organic farmers' market 为地点状语；Lima 为秘鲁首都。"
        },
        "words": [
            {"w": "produce", "pos": "v.", "def": "生产"},
            {"w": "sell", "pos": "v.", "def": "销售"},
            {"w": "market", "pos": "n.", "def": "市场"}
        ]
    },
    {
        "id": 30,
        "para": 6,
        "en": "His farm is relatively small and doesn" + RSQUO + "t yet provide him with enough to live on, but he hopes this will change.",
        "zh": "他的农场规模相对较小，还不能为他提供足够的生计，但他希望这种情况会有所改变。",
        "grammar": {
            "type": "并列谓语 + 转折",
            "note": "is relatively small and doesn't yet provide... 为并列谓语；but he hopes (that) this will change 为转折分句（含省略连词的宾语从句）；enough to live on 意为 “足以维持生计”。"
        },
        "words": [
            {"w": "relatively", "pos": "adv.", "def": "相对地"},
            {"w": "provide with", "pos": "phr.", "def": "提供；供给"},
            {"w": "live on", "pos": "phr.", "def": "靠……生活；以……为生"}
        ]
    },
    {
        "id": 31,
        "para": 6,
        "en": LSQUO + "The organic market is growing rapidly in Peru," + RSQUO + " Benevides says. " + LSQUO + "I am investing in the future." + RSQUO,
        "zh": "“秘鲁的有机市场正在迅速增长，”贝内维德斯说。“我是在为未来投资。”",
        "grammar": {
            "type": "现在进行时",
            "note": "is growing rapidly 与 am investing 均为现在进行时；invest in 意为 “投资于”。"
        },
        "words": [
            {"w": "grow", "pos": "v.", "def": "增长；生长"},
            {"w": "invest in", "pos": "phr.", "def": "投资于"},
            {"w": "future", "pos": "n.", "def": "未来"}
        ]
    },
    # Para 7
    {
        "id": 32,
        "para": 7,
        "en": "But even if Whaley can convince the local people to fall in love with the huarango again, there is still the threat of the larger farms.",
        "zh": "但即使惠利能说服当地人重新爱上牧豆树，大型农场的威胁依然存在。",
        "grammar": {
            "type": "让步状语从句",
            "note": "even if 引导让步状语从句；convince sb to do 意为 “说服某人做”；fall in love with 意为 “爱上”；the threat of 意为 “……的威胁”。"
        },
        "words": [
            {"w": "even if", "pos": "phr.", "def": "即使"},
            {"w": "convince", "pos": "v.", "def": "说服；使信服"},
            {"w": "fall in love with", "pos": "phr.", "def": "爱上"},
            {"w": "threat", "pos": "n.", "def": "威胁"}
        ]
    },
    {
        "id": 33,
        "para": 7,
        "en": "Some of these cut across the forests and break up the corridors that allow the essential movement of mammals, birds and pollen up and down the narrow forest strip.",
        "zh": "其中一些农场横穿森林，切断了那些供哺乳动物、鸟类和花粉沿着这条狭长林带上下往来所必需的通道。",
        "grammar": {
            "type": "并列谓语 + 定语从句",
            "note": "cut across... and break up... 为并列谓语；that allow the essential movement of... 为定语从句修饰 the corridors；cut across 意为 “横穿”，break up 意为 “打断、破坏”。"
        },
        "words": [
            {"w": "cut across", "pos": "phr.", "def": "横穿；穿过"},
            {"w": "break up", "pos": "phr.", "def": "打断；分割"},
            {"w": "corridor", "pos": "n.", "def": "走廊；通道"},
            {"w": "mammal", "pos": "n.", "def": "哺乳动物"},
            {"w": "pollen", "pos": "n.", "def": "花粉"}
        ]
    },
    {
        "id": 34,
        "para": 7,
        "en": "In the hope of counteracting this, he" + RSQUO + "s persuading farmers to let him plant forest corridors on their land.",
        "zh": "为了抵消这种影响，他正在劝说农民允许他在他们的土地上种植林带通道。",
        "grammar": {
            "type": "介词短语状语 + 使役动词",
            "note": "In the hope of counteracting this 为介词短语作目的状语；persuade sb to do 意为 “劝说某人做”；let him plant... 为 “let + 宾语 + 动词原形” 使役结构。"
        },
        "words": [
            {"w": "in the hope of", "pos": "phr.", "def": "希望；为了"},
            {"w": "counteract", "pos": "v.", "def": "抵消；抵抗"},
            {"w": "persuade", "pos": "v.", "def": "劝说；说服"}
        ]
    },
    {
        "id": 35,
        "para": 7,
        "en": "He believes the extra woodland will also benefit the farms by reducing their water usage through a lowering of evaporation and providing a refuge for bio-control insects.",
        "zh": "他认为，这些额外的林地还会通过降低蒸发从而减少农场的用水量、并为生物防治昆虫提供庇护所，从而使农场受益。",
        "grammar": {
            "type": "宾语从句 + 方式状语",
            "note": "believes (that) the extra woodland will... benefit... 为省略连词的宾语从句；by reducing... and providing... 为方式状语（并列动名词）；bio-control 意为 “生物防治的”。"
        },
        "words": [
            {"w": "benefit", "pos": "v.", "def": "使受益"},
            {"w": "usage", "pos": "n.", "def": "使用量；用法"},
            {"w": "evaporation", "pos": "n.", "def": "蒸发"},
            {"w": "refuge", "pos": "n.", "def": "庇护所；避难所"}
        ]
    },
    # Para 8
    {
        "id": 36,
        "para": 8,
        "en": LSQUO + "If we can record biodiversity and see how it all works, then we" + RSQUO + "re in a good position to move on from there.",
        "zh": "“如果我们能记录生物多样性、了解它整个是如何运作的，那么我们就处于一个有利的位置，可以从这里继续推进。",
        "grammar": {
            "type": "条件句 + 宾语从句",
            "note": "If we can record... and see how it all works 为条件状语从句（含 how 宾语从句）；in a good position to do 意为 “处于做……的有利位置”；move on 意为 “继续前进”。"
        },
        "words": [
            {"w": "record", "pos": "v.", "def": "记录"},
            {"w": "biodiversity", "pos": "n.", "def": "生物多样性"},
            {"w": "in a good position to", "pos": "phr.", "def": "处于做……的有利位置"},
            {"w": "move on", "pos": "phr.", "def": "继续前进"}
        ]
    },
    {
        "id": 37,
        "para": 8,
        "en": "Desert habitats can reduce down to very little," + RSQUO + " Whaley explains. " + LSQUO + "It" + RSQUO + "s not like a rainforest that needs to have this huge expanse.",
        "zh": "沙漠栖息地可以缩减到极小的范围，”惠利解释道。“它不像雨林那样需要有一片巨大的广袤空间。",
        "grammar": {
            "type": "定语从句",
            "note": "that needs to have this huge expanse 为定语从句修饰 a rainforest；reduce down to 意为 “缩减到”；expanse 意为 “广阔的区域”。"
        },
        "words": [
            {"w": "reduce down to", "pos": "phr.", "def": "缩减到"},
            {"w": "rainforest", "pos": "n.", "def": "雨林"},
            {"w": "expanse", "pos": "n.", "def": "广阔的区域；一大片"}
        ]
    },
    {
        "id": 38,
        "para": 8,
        "en": "Life has always been confined to corridors and islands here. If you just have a few trees left, the population can grow up quickly because it" + RSQUO + "s used to exploiting water when it arrives." + RSQUO,
        "zh": "在这里，生命一直被局限在通道和孤岛之中。如果你只剩下几棵树，种群也能迅速壮大，因为它已习惯于在水到来时加以利用。”",
        "grammar": {
            "type": "条件句 + 原因状语从句",
            "note": "be confined to 意为 “被限制于”；If you just have a few trees left 为条件从句；because it's used to exploiting... 为原因状语从句，be used to doing 意为 “习惯于做”；when it arrives 为时间状语从句。"
        },
        "words": [
            {"w": "be confined to", "pos": "phr.", "def": "被限制于；局限于"},
            {"w": "grow up", "pos": "phr.", "def": "成长；壮大"},
            {"w": "be used to", "pos": "phr.", "def": "习惯于"},
            {"w": "exploit", "pos": "v.", "def": "利用；开发"}
        ]
    },
    {
        "id": 39,
        "para": 8,
        "en": "He sees his project as a model that has the potential to be rolled out across other arid areas around the world.",
        "zh": "他把自己的项目视为一个有潜力推广到世界其他干旱地区的范本。",
        "grammar": {
            "type": "see A as B + 定语从句",
            "note": "see A as B 意为 “把 A 视为 B”；that has the potential to be rolled out... 为定语从句修饰 a model；roll out 意为 “推出、推广”；arid 意为 “干旱的”。"
        },
        "words": [
            {"w": "see ... as", "pos": "phr.", "def": "把……视为"},
            {"w": "potential", "pos": "n.", "def": "潜力"},
            {"w": "roll out", "pos": "phr.", "def": "推出；推广"},
            {"w": "arid", "pos": "adj.", "def": "干旱的"}
        ]
    },
    {
        "id": 40,
        "para": 8,
        "en": LSQUO + "If we can do it here, in the most fragile system on Earth, then that" + RSQUO + "s a real message of hope for lots of places, including Africa, where there is drought and they just can" + RSQUO + "t afford to wait for rain." + RSQUO,
        "zh": "“如果我们能在这里——在地球上最脆弱的系统里——做成这件事，那么这对许多地方来说都是一个真正充满希望的讯息，包括非洲那些遭受干旱、根本等不起雨水的地方。”",
        "grammar": {
            "type": "条件句 + 定语从句",
            "note": "If we can do it here... 为条件状语从句；where there is drought and they just can't afford to... 为定语从句修饰 Africa/places；a message of hope 意为 “希望的讯息”；afford to do 意为 “负担得起做”。"
        },
        "words": [
            {"w": "message of hope", "pos": "phr.", "def": "希望的讯息"},
            {"w": "including", "pos": "prep.", "def": "包括"},
            {"w": "afford to", "pos": "phr.", "def": "负担得起；有能力做"}
        ]
    }
]

phrases = [
    {"w": "be suited to", "pos": "phr.", "def": "适合；适应"},
    {"w": "as well as", "pos": "phr.", "def": "除……之外；以及"},
    {"w": "replace with", "pos": "phr.", "def": "用……取代"},
    {"w": "lead to", "pos": "phr.", "def": "导致"},
    {"w": "get on board", "pos": "phr.", "def": "争取支持；使加入"},
    {"w": "go the same way as", "pos": "phr.", "def": "重蹈……的覆辙"},
    {"w": "fall in love with", "pos": "phr.", "def": "爱上"},
    {"w": "in the hope of", "pos": "phr.", "def": "希望；为了"},
    {"w": "roll out", "pos": "phr.", "def": "推出；推广"},
    {"w": "afford to", "pos": "phr.", "def": "负担得起；有能力做"}
]

questions = [
    {
        "title": "Questions 1" + DASH + "5",
        "type": "note_completion",
        "instructions": [
            "Complete the notes below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 1" + DASH + "5 on your answer sheet.",
            "The importance of the huarango tree"
        ],
        "items": [
            {"number": 1, "prompt": "its roots can extend as far as 80 metres into the soil; can access __________ deep below the surface", "answer": "water", "evidence_sentence": 3},
            {"number": 2, "prompt": "was a crucial part of local inhabitants" + RSQUO + " __________ a long time ago", "answer": "diet", "evidence_sentence": 7},
            {"number": 3, "prompt": "helped people to survive periods of __________", "answer": "drought", "evidence_sentence": 7},
            {"number": 4, "prompt": "prevents __________ of the soil", "answer": "erosion", "evidence_sentence": 9},
            {"number": 5, "prompt": "prevents land from becoming a __________", "answer": "desert", "evidence_sentence": 10}
        ]
    },
    {
        "title": "Questions 6" + DASH + "8",
        "type": "table_completion",
        "instructions": [
            "Complete the table below.",
            "Choose NO MORE THAN TWO WORDS from the passage for each answer.",
            "Write your answers in boxes 6" + DASH + "8 on your answer sheet.",
            "Traditional uses of the huarango tree"
        ],
        "items": [
            {"number": 6, "prompt": "Part of tree: __________  |  Traditional use: fuel", "answer": "(its/huarango/the) branches", "evidence_sentence": 13},
            {"number": 7, "prompt": "Part of tree: __________ and __________  |  Traditional use: medicine", "answer": "leaves (and) bark", "evidence_sentence": 13},
            {"number": 8, "prompt": "Part of tree: __________  |  Traditional use: construction", "answer": "(its/huarango/the) trunk", "evidence_sentence": 13}
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
            {"number": 9, "prompt": "Local families have told Whaley about some traditional uses of huarango products.", "answer": "NOT GIVEN", "evidence_sentence": 23},
            {"number": 10, "prompt": "Farmer Alberto Benevides is now making a good profit from growing huarangos.", "answer": "FALSE", "evidence_sentence": 30},
            {"number": 11, "prompt": "Whaley needs the co-operation of farmers to help preserve the area" + RSQUO + "s wildlife.", "answer": "TRUE", "evidence_sentence": 34},
            {"number": 12, "prompt": "For Whaley" + RSQUO + "s project to succeed, it needs to be extended over a very large area.", "answer": "FALSE", "evidence_sentence": 37},
            {"number": 13, "prompt": "Whaley has plans to go to Africa to set up a similar project.", "answer": "NOT GIVEN", "evidence_sentence": 40}
        ]
    }
]

data = {
    "id": "c15-test4-p1",
    "source": "剑桥雅思15 Test 4 Passage 1",
    "title": "The return of the huarango",
    "subtitle": "The arid valleys of southern Peru are welcoming the return of a native plant",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c15-test4-p1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
