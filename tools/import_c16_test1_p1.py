# -*- coding: utf-8 -*-
"""Generate data/passages/c16-test1-p1.json (Why we need to protect polar bears)."""
import json
import os

RSQUO = "’"  # '
LSQUO = "‘"  # '
DASH = "–"   # -
DEG = "°"    # degree

sentences = [
    # Para 1
    {
        "id": 1,
        "para": 1,
        "en": "Polar bears are being increasingly threatened by the effects of climate change, but their disappearance could have far-reaching consequences.",
        "zh": "北极熊正日益受到气候变化影响的威胁，但它们的消失可能会带来深远的后果。",
        "grammar": {
            "type": "现在进行时被动 + but 转折",
            "note": "are being increasingly threatened by 为现在进行时的被动语态，表示 “正日益被……威胁”；but 连接转折分句；far-reaching 意为 “影响深远的”；could have consequences 表推测。"
        },
        "words": [
            {"w": "threaten", "pos": "v.", "def": "威胁"},
            {"w": "climate change", "pos": "phr.", "def": "气候变化"},
            {"w": "disappearance", "pos": "n.", "def": "消失；灭绝"},
            {"w": "far-reaching", "pos": "adj.", "def": "影响深远的"},
            {"w": "consequence", "pos": "n.", "def": "后果"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "They are uniquely adapted to the extreme conditions of the Arctic Circle, where temperatures can reach " + DASH + "40" + DEG + "C.",
        "zh": "它们对北极圈极端环境有着独特的适应能力，那里的气温可低至零下40摄氏度。",
        "grammar": {
            "type": "where 定语从句",
            "note": "where temperatures can reach -40°C 为定语从句修饰 the Arctic Circle，where 引导表地点；be adapted to 意为 “适应”；uniquely 修饰 adapted 表 “独特地”。"
        },
        "words": [
            {"w": "be adapted to", "pos": "phr.", "def": "适应"},
            {"w": "extreme", "pos": "adj.", "def": "极端的"},
            {"w": "the Arctic Circle", "pos": "phr.", "def": "北极圈"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "One reason for this is that they have up to 11 centimetres of fat underneath their skin.",
        "zh": "其中一个原因是它们皮肤下有多达11厘米厚的脂肪。",
        "grammar": {
            "type": "表语从句",
            "note": "that they have up to 11 centimetres of fat... 为表语从句，说明 One reason 的内容；up to 意为 “多达”；underneath 意为 “在……下面”。"
        },
        "words": [
            {"w": "up to", "pos": "phr.", "def": "多达；高达"},
            {"w": "fat", "pos": "n.", "def": "脂肪"},
            {"w": "underneath", "pos": "prep.", "def": "在……下面"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "Humans with comparative levels of adipose tissue would be considered obese and would be likely to suffer from diabetes and heart disease.",
        "zh": "拥有相当水平脂肪组织的人类会被认为是肥胖的，并且很可能患上糖尿病和心脏病。",
        "grammar": {
            "type": "虚拟语气(would) + 后置定语",
            "note": "with comparative levels of adipose tissue 为介词短语作后置定语修饰 Humans；两个 would be 表虚拟推测；be considered obese 意为 “被认为肥胖”；be likely to 意为 “很可能”。"
        },
        "words": [
            {"w": "comparative", "pos": "adj.", "def": "相当的；比较的"},
            {"w": "adipose tissue", "pos": "phr.", "def": "脂肪组织"},
            {"w": "obese", "pos": "adj.", "def": "肥胖的"},
            {"w": "diabetes", "pos": "n.", "def": "糖尿病"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "Yet the polar bear experiences no such consequences.",
        "zh": "然而北极熊却不会经历此类后果。",
        "grammar": {
            "type": "Yet 转折 + no such",
            "note": "Yet 表转折，意为 “然而”；no such consequences 意为 “没有此类后果”，such 指代前句所述的肥胖、糖尿病等。"
        },
        "words": [
            {"w": "yet", "pos": "adv.", "def": "然而；但是"},
            {"w": "experience", "pos": "v.", "def": "经历"},
            {"w": "no such", "pos": "phr.", "def": "没有这样的"}
        ]
    },
    # Para 2
    {
        "id": 6,
        "para": 2,
        "en": "A 2014 study by Shi Ping Liu and colleagues sheds light on this mystery.",
        "zh": "刘世平（音译）及其同事在2014年的一项研究揭示了这个谜团。",
        "grammar": {
            "type": "简单句",
            "note": "主语 A 2014 study，by Shi Ping Liu and colleagues 为后置定语说明研究者；shed light on 意为 “揭示、阐明”；this mystery 指代上段北极熊为何不受脂肪危害之谜。"
        },
        "words": [
            {"w": "shed light on", "pos": "phr.", "def": "揭示；阐明"},
            {"w": "mystery", "pos": "n.", "def": "谜；奥秘"},
            {"w": "colleague", "pos": "n.", "def": "同事"}
        ]
    },
    {
        "id": 7,
        "para": 2,
        "en": "They compared the genetic structure of polar bears with that of their closest relatives from a warmer climate, the brown bears.",
        "zh": "他们将北极熊的基因结构与其来自较温暖气候的近亲——棕熊的基因结构进行了比较。",
        "grammar": {
            "type": "compare A with B + 同位语",
            "note": "compare A with B 意为 “把 A 与 B 比较”；that 指代 the genetic structure 以避免重复；the brown bears 为 their closest relatives 的同位语。"
        },
        "words": [
            {"w": "genetic structure", "pos": "phr.", "def": "基因结构"},
            {"w": "compare ... with", "pos": "phr.", "def": "把……与……比较"},
            {"w": "relative", "pos": "n.", "def": "亲属；近亲"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "This allowed them to determine the genes that have allowed polar bears to survive in one of the toughest environments on Earth.",
        "zh": "这使他们得以确定那些使北极熊能够在地球上最严酷环境之一中生存下来的基因。",
        "grammar": {
            "type": "allow sb to do + 定语从句",
            "note": "allow sb to do 意为 “使某人能够做”；the genes that have allowed polar bears to survive... 含定语从句，that 指代 genes 作主语；one of the toughest environments 为 “最严酷环境之一”。"
        },
        "words": [
            {"w": "determine", "pos": "v.", "def": "确定；查明"},
            {"w": "gene", "pos": "n.", "def": "基因"},
            {"w": "survive", "pos": "v.", "def": "生存；存活"},
            {"w": "tough", "pos": "adj.", "def": "严酷的；艰难的"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "Liu and his colleagues found the polar bears had a gene known as APoB, which reduces levels of low-density lipoproteins (LDLs) " + DASH + " a form of " + LSQUO + "bad" + RSQUO + " cholesterol.",
        "zh": "刘和同事们发现北极熊拥有一种名为APoB的基因，它能降低低密度脂蛋白（LDL）——一种“坏”胆固醇——的水平。",
        "grammar": {
            "type": "省略that宾语从句 + which 非限制性定语从句",
            "note": "found (that) the polar bears had a gene 为省略 that 的宾语从句；known as APoB 为过去分词定语；which reduces levels of LDLs 为非限制性定语从句；破折号后 a form of 'bad' cholesterol 为 LDLs 的补充说明。"
        },
        "words": [
            {"w": "known as", "pos": "phr.", "def": "被称为"},
            {"w": "reduce", "pos": "v.", "def": "降低；减少"},
            {"w": "low-density lipoprotein", "pos": "phr.", "def": "低密度脂蛋白"},
            {"w": "cholesterol", "pos": "n.", "def": "胆固醇"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "In humans, mutations of this gene are associated with increased risk of heart disease.",
        "zh": "在人类身上，这种基因的突变与心脏病风险增加有关。",
        "grammar": {
            "type": "be associated with",
            "note": "be associated with 意为 “与……相关联”；mutations of this gene 为主语；increased 为过去分词作定语修饰 risk。"
        },
        "words": [
            {"w": "mutation", "pos": "n.", "def": "突变；变异"},
            {"w": "be associated with", "pos": "phr.", "def": "与……相关"},
            {"w": "risk", "pos": "n.", "def": "风险"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": "Polar bears may therefore be an important study model to understand heart disease in humans.",
        "zh": "因此，北极熊可能是理解人类心脏病的重要研究模型。",
        "grammar": {
            "type": "therefore 推断 + 不定式定语",
            "note": "therefore 表因果推断；to understand heart disease in humans 为不定式作定语修饰 study model；may be 表推测。"
        },
        "words": [
            {"w": "therefore", "pos": "adv.", "def": "因此"},
            {"w": "study model", "pos": "phr.", "def": "研究模型"}
        ]
    },
    # Para 3
    {
        "id": 12,
        "para": 3,
        "en": "The genome of the polar bear may also provide the solution for another condition, one that particularly affects our older generation: osteoporosis.",
        "zh": "北极熊的基因组或许还能为另一种病症提供解决方案——一种尤其影响老年人的疾病：骨质疏松症。",
        "grammar": {
            "type": "one that 定语从句 + 冒号解释",
            "note": "one 指代 another condition，that particularly affects our older generation 为定语从句修饰 one；冒号后 osteoporosis 点明该病名；provide the solution for 意为 “为……提供解决办法”。"
        },
        "words": [
            {"w": "genome", "pos": "n.", "def": "基因组"},
            {"w": "condition", "pos": "n.", "def": "疾病；病症"},
            {"w": "generation", "pos": "n.", "def": "一代人"},
            {"w": "osteoporosis", "pos": "n.", "def": "骨质疏松症"}
        ]
    },
    {
        "id": 13,
        "para": 3,
        "en": "This is a disease where bones show reduced density, usually caused by insufficient exercise, reduced calcium intake or food starvation.",
        "zh": "这是一种骨密度降低的疾病，通常由运动不足、钙摄入减少或食物匮乏引起。",
        "grammar": {
            "type": "where 定语从句 + 过去分词状语",
            "note": "where bones show reduced density 为定语从句修饰 disease；usually caused by... 为过去分词短语作状语，说明病因；三项并列 insufficient exercise / reduced calcium intake / food starvation。"
        },
        "words": [
            {"w": "density", "pos": "n.", "def": "密度"},
            {"w": "insufficient", "pos": "adj.", "def": "不足的"},
            {"w": "calcium intake", "pos": "phr.", "def": "钙摄入"},
            {"w": "starvation", "pos": "n.", "def": "饥饿；匮乏"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": "Bone tissue is constantly being remodelled, meaning that bone is added or removed, depending on nutrient availability and the stress that the bone is under.",
        "zh": "骨组织在不断被重塑，也就是说，骨质会依据养分供应情况和骨骼所承受的压力而增加或减少。",
        "grammar": {
            "type": "现在进行时被动 + 分词状语 + depending on",
            "note": "is constantly being remodelled 为现在进行时被动；meaning that... 为现在分词作结果状语；depending on 意为 “取决于”；the stress that the bone is under 含定语从句，介词 under 后置。"
        },
        "words": [
            {"w": "bone tissue", "pos": "phr.", "def": "骨组织"},
            {"w": "remodel", "pos": "v.", "def": "重塑；改造"},
            {"w": "nutrient", "pos": "n.", "def": "养分；营养物"},
            {"w": "availability", "pos": "n.", "def": "可获得性；供应"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "Female polar bears, however, undergo extreme conditions during every pregnancy.",
        "zh": "然而，雌性北极熊在每次怀孕期间都要经受极端的处境。",
        "grammar": {
            "type": "however 插入语",
            "note": "however 作插入语表转折；undergo 意为 “经历、经受”；during every pregnancy 为时间状语。"
        },
        "words": [
            {"w": "undergo", "pos": "v.", "def": "经历；经受"},
            {"w": "pregnancy", "pos": "n.", "def": "怀孕；孕期"}
        ]
    },
    {
        "id": 16,
        "para": 3,
        "en": "Once autumn comes around, these females will dig maternity dens in the snow and will remain there throughout the winter, both before and after the birth of their cubs.",
        "zh": "一旦秋天来临，这些雌熊便会在雪中挖掘产崽洞穴，并在整个冬天都待在那里，无论是在幼崽出生之前还是之后。",
        "grammar": {
            "type": "Once 时间状语从句 + 并列谓语",
            "note": "Once autumn comes around 为 once 引导的时间状语从句；主句两个 will 并列谓语 dig... and will remain...；both before and after 为并列介词短语作时间状语。"
        },
        "words": [
            {"w": "come around", "pos": "phr.", "def": "到来；来临"},
            {"w": "maternity den", "pos": "phr.", "def": "产崽洞穴"},
            {"w": "throughout", "pos": "prep.", "def": "贯穿；整个"},
            {"w": "cub", "pos": "n.", "def": "幼崽"}
        ]
    },
    {
        "id": 17,
        "para": 3,
        "en": "This process results in about six months of fasting, where the female bears have to keep themselves and their cubs alive, depleting their own calcium and calorie reserves.",
        "zh": "这一过程导致大约六个月的禁食期，在此期间雌熊必须让自己和幼崽存活下来，从而耗尽自身的钙和热量储备。",
        "grammar": {
            "type": "result in + where 定语从句 + 分词状语",
            "note": "result in 意为 “导致”；where the female bears have to... 为定语从句修饰 six months of fasting；depleting their own... reserves 为现在分词作结果状语；keep sb alive 意为 “使某人活着”。"
        },
        "words": [
            {"w": "result in", "pos": "phr.", "def": "导致；造成"},
            {"w": "fasting", "pos": "n.", "def": "禁食"},
            {"w": "deplete", "pos": "v.", "def": "耗尽；使枯竭"},
            {"w": "calorie", "pos": "n.", "def": "卡路里；热量"},
            {"w": "reserve", "pos": "n.", "def": "储备"}
        ]
    },
    {
        "id": 18,
        "para": 3,
        "en": "Despite this, their bones remain strong and dense.",
        "zh": "尽管如此，它们的骨骼依然强壮而致密。",
        "grammar": {
            "type": "Despite 介词短语",
            "note": "Despite this 为介词短语表让步，意为 “尽管如此”；remain 为系动词，后接形容词 strong and dense 作表语。"
        },
        "words": [
            {"w": "despite", "pos": "prep.", "def": "尽管"},
            {"w": "remain", "pos": "v.", "def": "保持；仍然是"},
            {"w": "dense", "pos": "adj.", "def": "致密的；密集的"}
        ]
    },
    # Para 4
    {
        "id": 19,
        "para": 4,
        "en": "Physiologists Alanda Lennox and Allen Goodship found an explanation for this paradox in 2008.",
        "zh": "生理学家阿兰达·伦诺克斯和艾伦·古德希普在2008年找到了这一悖论的解释。",
        "grammar": {
            "type": "简单句 + 同位语",
            "note": "Physiologists 为职业头衔，与人名 Alanda Lennox and Allen Goodship 构成同位关系；find an explanation for 意为 “找到……的解释”；this paradox 指代上段 “禁食却骨骼强壮” 的矛盾现象。"
        },
        "words": [
            {"w": "physiologist", "pos": "n.", "def": "生理学家"},
            {"w": "explanation", "pos": "n.", "def": "解释"},
            {"w": "paradox", "pos": "n.", "def": "悖论；自相矛盾的现象"}
        ]
    },
    {
        "id": 20,
        "para": 4,
        "en": "They discovered that pregnant bears were able to increase the density of their bones before they started to build their dens.",
        "zh": "他们发现，怀孕的熊在开始筑巢之前就能够增加骨骼的密度。",
        "grammar": {
            "type": "that 宾语从句 + before 时间从句",
            "note": "discovered that... 为宾语从句；were able to increase 意为 “能够增加”；before they started to build their dens 为 before 引导的时间状语从句。"
        },
        "words": [
            {"w": "discover", "pos": "v.", "def": "发现"},
            {"w": "pregnant", "pos": "adj.", "def": "怀孕的"},
            {"w": "den", "pos": "n.", "def": "洞穴；巢穴"}
        ]
    },
    {
        "id": 21,
        "para": 4,
        "en": "In addition, six months later, when they finally emerged from the den with their cubs, there was no evidence of significant loss of bone density.",
        "zh": "此外，六个月后，当它们最终带着幼崽从洞穴中出来时，并没有出现骨密度显著流失的迹象。",
        "grammar": {
            "type": "when 时间从句 + there be",
            "note": "In addition 表递进；when they finally emerged from the den... 为时间状语从句；主句 there was no evidence of...；emerge from 意为 “从……出来”；loss of bone density 意为 “骨密度流失”。"
        },
        "words": [
            {"w": "in addition", "pos": "phr.", "def": "此外"},
            {"w": "emerge from", "pos": "phr.", "def": "从……出来；显现"},
            {"w": "evidence", "pos": "n.", "def": "证据；迹象"},
            {"w": "significant", "pos": "adj.", "def": "显著的；重大的"}
        ]
    },
    {
        "id": 22,
        "para": 4,
        "en": "Hibernating brown bears do not have this capacity and must therefore resort to major bone reformation in the following spring.",
        "zh": "冬眠的棕熊不具备这种能力，因此必须在来年春天进行大规模的骨骼重建。",
        "grammar": {
            "type": "并列谓语 + therefore",
            "note": "Hibernating 为现在分词作定语修饰 brown bears；两个谓语 do not have... and must resort to... 并列；therefore 表因果；resort to 意为 “诉诸、采取（某手段）”。"
        },
        "words": [
            {"w": "hibernate", "pos": "v.", "def": "冬眠"},
            {"w": "capacity", "pos": "n.", "def": "能力"},
            {"w": "resort to", "pos": "phr.", "def": "诉诸；不得不采用"},
            {"w": "reformation", "pos": "n.", "def": "重建；重新形成"}
        ]
    },
    {
        "id": 23,
        "para": 4,
        "en": "If the mechanism of bone remodelling in polar bears can be understood, many bedridden humans, and even astronauts, could potentially benefit.",
        "zh": "如果能够弄清北极熊骨骼重塑的机制，许多卧床不起的人乃至宇航员都有可能从中受益。",
        "grammar": {
            "type": "if 条件从句 + 被动 + could 推测",
            "note": "If... can be understood 为 if 引导的条件状语从句，含被动语态；主句 many bedridden humans, and even astronauts, could potentially benefit 用 could 表可能性；mechanism of 意为 “……的机制”。"
        },
        "words": [
            {"w": "mechanism", "pos": "n.", "def": "机制；机理"},
            {"w": "bedridden", "pos": "adj.", "def": "卧床不起的"},
            {"w": "astronaut", "pos": "n.", "def": "宇航员"},
            {"w": "potentially", "pos": "adv.", "def": "潜在地；有可能地"}
        ]
    },
    # Para 5
    {
        "id": 24,
        "para": 5,
        "en": "The medical benefits of the polar bear for humanity certainly have their importance in our conservation efforts, but these should not be the only factors taken into consideration.",
        "zh": "北极熊对人类的医学益处在我们的保护工作中当然有其重要性，但这些不应是唯一被纳入考量的因素。",
        "grammar": {
            "type": "but 转折 + 过去分词定语",
            "note": "主句 The medical benefits... have their importance；but 转折；taken into consideration 为过去分词短语作定语修饰 factors；take sth into consideration 意为 “考虑到某事”。"
        },
        "words": [
            {"w": "medical benefit", "pos": "phr.", "def": "医学益处"},
            {"w": "humanity", "pos": "n.", "def": "人类"},
            {"w": "conservation", "pos": "n.", "def": "保护；保育"},
            {"w": "take into consideration", "pos": "phr.", "def": "考虑；顾及"}
        ]
    },
    {
        "id": 25,
        "para": 5,
        "en": "We tend to want to protect animals we think are intelligent and possess emotions, such as elephants and primates.",
        "zh": "我们往往想保护那些我们认为聪明且拥有情感的动物，比如大象和灵长类动物。",
        "grammar": {
            "type": "tend to + 省略that定语从句",
            "note": "tend to do 意为 “倾向于做”；animals (that) we think are intelligent... 为省略关系词的定语从句，we think 为插入语；such as 引出例子；possess 意为 “拥有”。"
        },
        "words": [
            {"w": "tend to", "pos": "phr.", "def": "倾向于"},
            {"w": "possess", "pos": "v.", "def": "拥有"},
            {"w": "emotion", "pos": "n.", "def": "情感；情绪"},
            {"w": "primate", "pos": "n.", "def": "灵长类动物"}
        ]
    },
    {
        "id": 26,
        "para": 5,
        "en": "Bears, on the other hand, seem to be perceived as stupid and in many cases violent.",
        "zh": "另一方面，熊似乎被认为是愚蠢的，而且在很多情况下是凶暴的。",
        "grammar": {
            "type": "on the other hand + 被动",
            "note": "on the other hand 意为 “另一方面”；seem to be perceived as 为 “似乎被视为”，含被动；stupid 与 violent 并列作 perceived 的宾语补足语；in many cases 为状语。"
        },
        "words": [
            {"w": "on the other hand", "pos": "phr.", "def": "另一方面"},
            {"w": "perceive", "pos": "v.", "def": "认为；感知"},
            {"w": "violent", "pos": "adj.", "def": "凶暴的；暴力的"}
        ]
    },
    {
        "id": 27,
        "para": 5,
        "en": "And yet anecdotal evidence from the field challenges those assumptions, suggesting for example that polar bears have good problem-solving abilities.",
        "zh": "然而来自野外的传闻性证据却对那些假设提出了挑战，例如表明北极熊具有很强的解决问题的能力。",
        "grammar": {
            "type": "And yet 转折 + 现在分词状语",
            "note": "And yet 表强烈转折；challenges those assumptions 为谓语；suggesting... 为现在分词作伴随/结果状语，其后接 that 宾语从句；anecdotal evidence 意为 “传闻性证据”。"
        },
        "words": [
            {"w": "anecdotal", "pos": "adj.", "def": "传闻的；轶事的"},
            {"w": "challenge", "pos": "v.", "def": "质疑；对……提出挑战"},
            {"w": "assumption", "pos": "n.", "def": "假设"},
            {"w": "problem-solving", "pos": "adj.", "def": "解决问题的"}
        ]
    },
    {
        "id": 28,
        "para": 5,
        "en": "A male bear called GoGo in Tennoji Zoo, Osaka, has even been observed making use of a tool to manipulate his environment.",
        "zh": "在大阪天王寺动物园，一头名叫GoGo的雄性熊甚至被观察到利用工具来操控其周围环境。",
        "grammar": {
            "type": "现在完成时被动 + 分词宾补",
            "note": "has been observed 为现在完成时被动；making use of a tool... 为现在分词作宾语补足语（observe sb doing 的被动形式）；called GoGo 为过去分词定语；make use of 意为 “利用”。"
        },
        "words": [
            {"w": "observe", "pos": "v.", "def": "观察到"},
            {"w": "make use of", "pos": "phr.", "def": "利用"},
            {"w": "tool", "pos": "n.", "def": "工具"},
            {"w": "manipulate", "pos": "v.", "def": "操控；操纵"}
        ]
    },
    {
        "id": 29,
        "para": 5,
        "en": "The bear used a tree branch on multiple occasions to dislodge a piece of meat hung out of his reach.",
        "zh": "这头熊多次用树枝把挂在其够不到的地方的一块肉弄下来。",
        "grammar": {
            "type": "不定式目的 + 过去分词定语",
            "note": "to dislodge a piece of meat 为不定式表目的；hung out of his reach 为过去分词短语作定语修饰 meat；on multiple occasions 意为 “多次”；out of one's reach 意为 “够不到的地方”。"
        },
        "words": [
            {"w": "tree branch", "pos": "phr.", "def": "树枝"},
            {"w": "on multiple occasions", "pos": "phr.", "def": "多次"},
            {"w": "dislodge", "pos": "v.", "def": "使移动；弄下来"},
            {"w": "out of one" + RSQUO + "s reach", "pos": "phr.", "def": "够不到；力所不及"}
        ]
    },
    {
        "id": 30,
        "para": 5,
        "en": "Problem-solving ability has also been witnessed in wild polar bears, although not as obviously as with GoGo.",
        "zh": "在野生北极熊身上也观察到了解决问题的能力，尽管不如GoGo那样明显。",
        "grammar": {
            "type": "现在完成时被动 + although 让步省略",
            "note": "has been witnessed 为现在完成时被动；although not as obviously as with GoGo 为让步状语，省略了 it is（although it is not as obviously... as with GoGo）；as...as 为同级比较。"
        },
        "words": [
            {"w": "witness", "pos": "v.", "def": "见证；观察到"},
            {"w": "wild", "pos": "adj.", "def": "野生的"},
            {"w": "obviously", "pos": "adv.", "def": "明显地"}
        ]
    },
    {
        "id": 31,
        "para": 5,
        "en": "A calculated move by a male bear involved running and jumping onto barrels in an attempt to get to a photographer standing on a platform four metres high.",
        "zh": "一头雄熊经过盘算的举动包括奔跑并跳上桶，试图够到站在四米高平台上的一名摄影师。",
        "grammar": {
            "type": "动名词作宾语 + in an attempt to",
            "note": "running and jumping onto barrels 为动名词短语作 involved 的宾语；in an attempt to get to... 意为 “试图够到”；standing on a platform... 为现在分词定语修饰 photographer；calculated 意为 “精心算计的”。"
        },
        "words": [
            {"w": "calculated", "pos": "adj.", "def": "精心算计的；蓄意的"},
            {"w": "barrel", "pos": "n.", "def": "桶"},
            {"w": "in an attempt to", "pos": "phr.", "def": "试图；企图"},
            {"w": "platform", "pos": "n.", "def": "平台"}
        ]
    },
    {
        "id": 32,
        "para": 6,
        "en": "In other studies, such as one by Alison Ames in 2008, polar bears showed deliberate and focussed manipulation.",
        "zh": "在其他研究中，例如艾莉森·埃姆斯2008年的一项研究，北极熊表现出有意且专注的操控行为。",
        "grammar": {
            "type": "such as 举例 + 简单句",
            "note": "such as one by Alison Ames in 2008 为插入的举例，one 指代 study；主句 polar bears showed... manipulation；deliberate and focussed 并列修饰 manipulation。"
        },
        "words": [
            {"w": "deliberate", "pos": "adj.", "def": "有意的；蓄意的"},
            {"w": "focussed", "pos": "adj.", "def": "专注的"},
            {"w": "manipulation", "pos": "n.", "def": "操控；操纵"}
        ]
    },
    {
        "id": 33,
        "para": 6,
        "en": "For example, Ames observed bears putting objects in piles and then knocking them over in what appeared to be a game.",
        "zh": "例如，埃姆斯观察到熊把物体堆成堆，然后又把它们推倒，看上去像是在做游戏。",
        "grammar": {
            "type": "observe sb doing + what 从句",
            "note": "observed bears putting... and then knocking... 为 observe sb doing 结构，两动名词并列；in what appeared to be a game 中 what 引导介词宾语从句；knock over 意为 “推倒、打翻”。"
        },
        "words": [
            {"w": "pile", "pos": "n.", "def": "堆"},
            {"w": "knock over", "pos": "phr.", "def": "推倒；打翻"},
            {"w": "appear to be", "pos": "phr.", "def": "看起来是"}
        ]
    },
    {
        "id": 34,
        "para": 6,
        "en": "The study demonstrates that bears are capable of agile and thought-out behaviours.",
        "zh": "该研究表明，熊能够做出灵活且经过深思熟虑的行为。",
        "grammar": {
            "type": "that 宾语从句",
            "note": "demonstrates that... 为宾语从句；be capable of 意为 “能够”，后接名词/动名词；agile and thought-out 并列修饰 behaviours。"
        },
        "words": [
            {"w": "demonstrate", "pos": "v.", "def": "证明；表明"},
            {"w": "be capable of", "pos": "phr.", "def": "能够"},
            {"w": "agile", "pos": "adj.", "def": "灵活的；敏捷的"},
            {"w": "thought-out", "pos": "adj.", "def": "深思熟虑的"}
        ]
    },
    {
        "id": 35,
        "para": 6,
        "en": "These examples suggest bears have greater creativity and problem-solving abilities than previously thought.",
        "zh": "这些例子表明，熊拥有比以往认为的更强的创造力和解决问题的能力。",
        "grammar": {
            "type": "省略that宾语从句 + 比较 + 省略",
            "note": "suggest (that) bears have... 为省略 that 的宾语从句；greater... than previously thought 为比较结构，than 后省略 they were（than was previously thought）；creativity 意为 “创造力”。"
        },
        "words": [
            {"w": "suggest", "pos": "v.", "def": "表明；暗示"},
            {"w": "creativity", "pos": "n.", "def": "创造力"},
            {"w": "previously", "pos": "adv.", "def": "以前；先前"}
        ]
    },
    # Para 7
    {
        "id": 36,
        "para": 7,
        "en": "As for emotions, while the evidence is once again anecdotal, many bears have been seen to hit out at ice and snow " + DASH + " seemingly out of frustration " + DASH + " when they have just missed out on a kill.",
        "zh": "至于情感，尽管证据同样是传闻性的，但许多熊被看到会击打冰雪——似乎是出于沮丧——就在它们刚刚错失一次捕猎之后。",
        "grammar": {
            "type": "As for + while 让步 + 破折号插入 + when 从句",
            "note": "As for emotions 意为 “至于情感”；while the evidence is... anecdotal 为 while 让步从句；主句 many bears have been seen to hit out...；破折号间 seemingly out of frustration 为插入说明；when they have just missed out on a kill 为时间从句；miss out on 意为 “错过”。"
        },
        "words": [
            {"w": "as for", "pos": "phr.", "def": "至于；关于"},
            {"w": "hit out at", "pos": "phr.", "def": "猛击；抨击"},
            {"w": "out of frustration", "pos": "phr.", "def": "出于沮丧"},
            {"w": "miss out on", "pos": "phr.", "def": "错过"}
        ]
    },
    {
        "id": 37,
        "para": 7,
        "en": "Moreover, polar bears can form unusual relationships with other species, including playing with the dogs used to pull sleds in the Arctic.",
        "zh": "此外，北极熊能够与其他物种建立不寻常的关系，包括与北极地区用来拉雪橇的狗一起玩耍。",
        "grammar": {
            "type": "including 分词 + 过去分词定语",
            "note": "Moreover 表递进；including playing with the dogs 为 including 后接动名词；used to pull sleds in the Arctic 为过去分词短语作定语修饰 dogs；form relationships with 意为 “与……建立关系”。"
        },
        "words": [
            {"w": "moreover", "pos": "adv.", "def": "此外；而且"},
            {"w": "unusual", "pos": "adj.", "def": "不寻常的"},
            {"w": "species", "pos": "n.", "def": "物种"},
            {"w": "sled", "pos": "n.", "def": "雪橇"}
        ]
    },
    {
        "id": 38,
        "para": 7,
        "en": "Remarkably, one hand-raised polar bear called Agee has formed a close relationship with her owner Mark Dumas to the point where they even swim together.",
        "zh": "值得注意的是，一头名叫Agee、由人工抚养长大的北极熊与它的主人马克·杜马斯建立了亲密的关系，甚至到了会一起游泳的地步。",
        "grammar": {
            "type": "to the point where 结果状语",
            "note": "Remarkably 为评注性状语；called Agee 为过去分词定语；to the point where they even swim together 为 “到了……的地步” 结构，where 引导定语从句修饰 point；hand-raised 意为 “人工抚养的”。"
        },
        "words": [
            {"w": "remarkably", "pos": "adv.", "def": "显著地；值得注意地"},
            {"w": "hand-raised", "pos": "adj.", "def": "人工抚养的"},
            {"w": "to the point where", "pos": "phr.", "def": "到了……的地步"}
        ]
    },
    {
        "id": 39,
        "para": 7,
        "en": "This is even more astonishing since polar bears are known to actively hunt humans in the wild.",
        "zh": "这就更加令人惊讶了，因为众所周知北极熊在野外会主动猎杀人类。",
        "grammar": {
            "type": "since 原因从句",
            "note": "even more astonishing 为比较级作表语；since polar bears are known to... 为 since 引导的原因状语从句；be known to do 意为 “众所周知会做”；actively 意为 “主动地”。"
        },
        "words": [
            {"w": "astonishing", "pos": "adj.", "def": "令人惊讶的"},
            {"w": "be known to", "pos": "phr.", "def": "众所周知；已知"},
            {"w": "actively", "pos": "adv.", "def": "主动地；积极地"},
            {"w": "in the wild", "pos": "phr.", "def": "在野外"}
        ]
    },
    # Para 8
    {
        "id": 40,
        "para": 8,
        "en": "If climate change were to lead to their extinction, this would mean not only the loss of potential breakthroughs in human medicine, but more importantly, the disappearance of an intelligent, majestic animal.",
        "zh": "如果气候变化导致它们灭绝，这将不仅意味着人类医学潜在突破的丧失，更重要的是，还意味着一种聪明而威严的动物的消失。",
        "grammar": {
            "type": "were to 虚拟条件 + not only... but...",
            "note": "If climate change were to lead to... 为 were to 引导的虚拟条件从句，表对将来的假设；主句 this would mean...；not only... but (also) more importantly... 为并列结构，连接两个宾语；lead to 意为 “导致”。"
        },
        "words": [
            {"w": "extinction", "pos": "n.", "def": "灭绝"},
            {"w": "potential", "pos": "adj.", "def": "潜在的"},
            {"w": "breakthrough", "pos": "n.", "def": "突破"},
            {"w": "majestic", "pos": "adj.", "def": "威严的；壮丽的"}
        ]
    }
]

phrases = [
    {"w": "shed light on", "pos": "phr.", "def": "揭示；阐明"},
    {"w": "be adapted to", "pos": "phr.", "def": "适应"},
    {"w": "be associated with", "pos": "phr.", "def": "与……相关"},
    {"w": "result in", "pos": "phr.", "def": "导致；造成"},
    {"w": "resort to", "pos": "phr.", "def": "诉诸；不得不采用"},
    {"w": "make use of", "pos": "phr.", "def": "利用"},
    {"w": "take into consideration", "pos": "phr.", "def": "考虑；顾及"},
    {"w": "miss out on", "pos": "phr.", "def": "错过"},
    {"w": "to the point where", "pos": "phr.", "def": "到了……的地步"},
    {"w": "in the wild", "pos": "phr.", "def": "在野外"}
]

questions = [
    {
        "title": "Questions 1" + DASH + "7",
        "type": "true_false_notgiven",
        "instructions": [
            "Do the following statements agree with the information given in Reading Passage 1?",
            "In boxes 1" + DASH + "7 on your answer sheet, write",
            "TRUE if the statement agrees with the information",
            "FALSE if the statement contradicts the information",
            "NOT GIVEN if there is no information on this"
        ],
        "items": [
            {"number": 1, "prompt": "Polar bears suffer from various health problems due to the build-up of fat under their skin.", "answer": "FALSE", "evidence_sentence": 5},
            {"number": 2, "prompt": "The study done by Liu and his colleagues compared different groups of polar bears.", "answer": "FALSE", "evidence_sentence": 7},
            {"number": 3, "prompt": "Liu and colleagues were the first researchers to compare polar bears and brown bears genetically.", "answer": "NOT GIVEN", "evidence_sentence": 7},
            {"number": 4, "prompt": "Polar bears are able to control their levels of " + LSQUO + "bad" + RSQUO + " cholesterol by genetic means.", "answer": "TRUE", "evidence_sentence": 9},
            {"number": 5, "prompt": "Female polar bears are able to survive for about six months without food.", "answer": "TRUE", "evidence_sentence": 17},
            {"number": 6, "prompt": "It was found that the bones of female polar bears were very weak when they came out of their dens in spring.", "answer": "FALSE", "evidence_sentence": 21},
            {"number": 7, "prompt": "The polar bear" + RSQUO + "s mechanism for increasing bone density could also be used by people one day.", "answer": "TRUE", "evidence_sentence": 23}
        ]
    },
    {
        "title": "Questions 8" + DASH + "13",
        "type": "table_completion",
        "instructions": [
            "Complete the table below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 8" + DASH + "13 on your answer sheet.",
            "Reasons why polar bears should be protected"
        ],
        "items": [
            {"number": 8, "prompt": "People think of bears as unintelligent and 8 ______.", "answer": "violent", "evidence_sentence": 26},
            {"number": 9, "prompt": "In Tennoji Zoo, a bear has been seen using a branch as a 9 ______.", "answer": "tool", "evidence_sentence": 28},
            {"number": 10, "prompt": "This allowed him to knock down some 10 ______.", "answer": "meat", "evidence_sentence": 29},
            {"number": 11, "prompt": "A wild polar bear worked out a method of reaching a platform where a 11 ______ was located.", "answer": "photographer", "evidence_sentence": 31},
            {"number": 12, "prompt": "Polar bears have displayed behaviour such as conscious manipulation of objects and activity similar to a 12 ______.", "answer": "game", "evidence_sentence": 33},
            {"number": 13, "prompt": "They may make movements suggesting 13 ______ if disappointed when hunting.", "answer": "frustration", "evidence_sentence": 36}
        ]
    }
]

data = {
    "id": "c16-test1-p1",
    "source": "剑桥雅思16 Test 1 Passage 1",
    "title": "Why we need to protect polar bears",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c16-test1-p1.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
