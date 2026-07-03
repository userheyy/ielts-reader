# -*- coding: utf-8 -*-
"""Generate data/passages/c18-test1-p2.json (Forest management in Pennsylvania, USA)."""
import json
import os

RSQUO = "’"
LSQUO = "‘"
DASH = "–"

sentences = [
    # Paragraph A (para 1)
    {
        "id": 1,
        "para": 1,
        "en": "A tree" + RSQUO + "s " + LSQUO + "value" + RSQUO + " depends on several factors including its species, size, form, condition, quality, function, and accessibility, and depends on the management goals for a given forest.",
        "zh": "一棵树的“价值”取决于若干因素，包括它的树种、大小、形态、状况、品质、用途和可及性，同时也取决于某片特定森林的经营目标。",
        "grammar": {
            "type": "并列谓语 + 现在分词举例",
            "note": "主语 A tree" + RSQUO + "s " + LSQUO + "value" + RSQUO + " 带两个并列谓语 depends on several factors... and depends on the management goals...；including its species, size... 为现在分词短语举例说明 factors。"
        },
        "words": [
            {"w": "accessibility", "pos": "n.", "def": "可及性；可达到性"},
            {"w": "factor", "pos": "n.", "def": "因素"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "The same tree can be valued very differently by each person who looks at it.",
        "zh": "同一棵树，在每个看它的人眼中，其价值评判可能大相径庭。",
        "grammar": {
            "type": "被动语态 + 定语从句",
            "note": "主干是 The same tree can be valued very differently，为被动语态；by each person 为动作发出者；who looks at it 为定语从句修饰 person。"
        },
        "words": [
            {"w": "value", "pos": "v.", "def": "评估……的价值；重视"},
            {"w": "differently", "pos": "adv.", "def": "不同地"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "A large, straight black cherry tree has high value as timber to be cut into logs or made into furniture, but for a landowner more interested in wildlife habitat, the real value of that stem (or trunk) may be the food it provides to animals.",
        "zh": "一棵高大挺直的黑樱桃树，作为可锯成原木或制成家具的木材，价值很高；但对一个更关注野生动物栖息地的土地所有者来说，那根树干真正的价值也许在于它为动物提供的食物。",
        "grammar": {
            "type": "转折并列 + 不定式定语 + 省略关系词定语从句",
            "note": "but 连接转折；前半 A large... tree has high value as timber，to be cut into logs or made into furniture 为不定式作定语修饰 timber；后半 the real value... may be the food，it provides to animals 为省略关系词的定语从句修饰 food。"
        },
        "words": [
            {"w": "timber", "pos": "n.", "def": "木材"},
            {"w": "habitat", "pos": "n.", "def": "栖息地"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "Likewise, if the tree suffers from black knot disease, its value for timber decreases, but to a woodworker interested in making bowls, it brings an opportunity for a unique and beautiful piece of art.",
        "zh": "同样地，如果这棵树患了黑瘤病，它作为木材的价值就会下降，但对一个热衷于做木碗的木工来说，它却带来了制作一件独特而精美的艺术品的机会。",
        "grammar": {
            "type": "if 条件状语从句 + 转折并列",
            "note": "if the tree suffers from black knot disease 为条件状语从句；主句前半 its value for timber decreases，but 引出转折；to a woodworker interested in making bowls 中 interested in making bowls 为形容词短语修饰 woodworker；Likewise 表类比。"
        },
        "words": [
            {"w": "woodworker", "pos": "n.", "def": "木工；木器工匠"},
            {"w": "likewise", "pos": "adv.", "def": "同样地"}
        ]
    },
    # Paragraph B (para 2)
    {
        "id": 5,
        "para": 2,
        "en": "In the past, Pennsylvania landowners were solely interested in the value of their trees as high-quality timber.",
        "zh": "过去，宾夕法尼亚的土地所有者只关心自己的树作为优质木材的价值。",
        "grammar": {
            "type": "主系表 + 时间状语",
            "note": "主干是 Pennsylvania landowners were solely interested in the value of their trees；In the past 为时间状语；as high-quality timber 为介词短语说明 value 的角度。"
        },
        "words": [
            {"w": "solely", "pos": "adv.", "def": "仅仅；唯一地"},
            {"w": "high-quality", "pos": "adj.", "def": "高质量的；优质的"}
        ]
    },
    {
        "id": 6,
        "para": 2,
        "en": "The norm was to remove the stems of highest quality and leave behind poorly formed trees that were not as well suited to the site where they grew.",
        "zh": "当时的惯例是把品质最高的树干移走，而把那些形态不良、并不太适应其生长地的树留下。",
        "grammar": {
            "type": "主系表 + 不定式并列 + 定语从句",
            "note": "主干是 The norm was to remove... and leave behind...，两个不定式作表语并列；that were not as well suited to the site 为定语从句修饰 trees；where they grew 为定语从句修饰 site。"
        },
        "words": [
            {"w": "norm", "pos": "n.", "def": "惯例；常态"},
            {"w": "stem", "pos": "n.", "def": "（树）干；茎"}
        ]
    },
    {
        "id": 7,
        "para": 2,
        "en": "This practice, called " + LSQUO + "high-grading" + RSQUO + ", has left a legacy of " + LSQUO + "low-use wood" + RSQUO + " in the forests.",
        "zh": "这种被称为“择优采伐”的做法，在森林里留下了“低用途木材”的遗留问题。",
        "grammar": {
            "type": "过去分词作插入定语 + 现在完成时",
            "note": "主干是 This practice... has left a legacy of " + LSQUO + "low-use wood" + RSQUO + "；called " + LSQUO + "high-grading" + RSQUO + " 为过去分词短语作插入定语修饰 practice。"
        },
        "words": [
            {"w": "legacy", "pos": "n.", "def": "遗留物；遗产"},
            {"w": "high-grading", "pos": "n.", "def": "择优采伐（只砍最好的树）"}
        ]
    },
    {
        "id": 8,
        "para": 2,
        "en": "Some people even call these " + LSQUO + "junk trees" + RSQUO + ", and they are abundant in Pennsylvania.",
        "zh": "有些人甚至把这些树叫作“垃圾树”，而它们在宾夕法尼亚非常多。",
        "grammar": {
            "type": "并列句 + call sth sth",
            "note": "两个分句由 and 并列；前句 Some people even call these " + LSQUO + "junk trees" + RSQUO + " 为 call + 宾语 + 宾语补足语结构；后句 they are abundant in Pennsylvania。"
        },
        "words": [
            {"w": "junk", "pos": "n.", "def": "废物；无用之物"},
            {"w": "abundant", "pos": "adj.", "def": "大量的；丰富的"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "These trees have lower economic value for traditional timber markets, compete for growth with higher-value trees, shade out desirable regeneration and decrease the health of a stand leaving it more vulnerable to poor weather and disease.",
        "zh": "这些树对传统木材市场而言经济价值较低，会与价值更高的树争夺生长空间，遮蔽掉理想的新生林木，并削弱一片林分的健康，使其更容易受到恶劣天气和病害的侵袭。",
        "grammar": {
            "type": "多重并列谓语 + 现在分词结果状语",
            "note": "主语 These trees 带四个并列谓语：have lower economic value、compete for growth、shade out desirable regeneration、decrease the health of a stand；leaving it more vulnerable to... 为现在分词短语作结果状语。"
        },
        "words": [
            {"w": "regeneration", "pos": "n.", "def": "（林木）再生；更新"},
            {"w": "vulnerable", "pos": "adj.", "def": "易受伤害的；脆弱的"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "Management that specifically targets low-use wood can help landowners manage these forest health issues, and wood energy markets help promote this.",
        "zh": "专门针对低用途木材的经营管理，能帮助土地所有者处理这些森林健康问题，而木材能源市场则有助于推动这一点。",
        "grammar": {
            "type": "定语从句 + 并列句",
            "note": "前句主干 Management... can help landowners manage these forest health issues，that specifically targets low-use wood 为定语从句修饰 Management；and wood energy markets help promote this 为并列分句。"
        },
        "words": [
            {"w": "target", "pos": "v.", "def": "针对；以……为目标"},
            {"w": "promote", "pos": "v.", "def": "促进；推动"}
        ]
    },
    # Paragraph C (para 3)
    {
        "id": 11,
        "para": 3,
        "en": "Wood energy markets can accept less expensive wood material of lower quality than would be suitable for traditional timber markets.",
        "zh": "木材能源市场可以接受比传统木材市场所需更便宜、质量更低的木料。",
        "grammar": {
            "type": "比较结构 + 省略主语定语从句",
            "note": "主干是 Wood energy markets can accept less expensive wood material of lower quality；than would be suitable for traditional timber markets 为比较状语从句，than 后省略了主语（承前指代该木料）。"
        },
        "words": [
            {"w": "accept", "pos": "v.", "def": "接受；接纳"},
            {"w": "suitable", "pos": "adj.", "def": "合适的；适宜的"}
        ]
    },
    {
        "id": 12,
        "para": 3,
        "en": "Most wood used for energy in Pennsylvania is used to produce heat or electricity through combustion.",
        "zh": "宾夕法尼亚用于能源的木材，大部分是通过燃烧来产生热能或电力。",
        "grammar": {
            "type": "过去分词定语 + 被动语态",
            "note": "主语 Most wood，used for energy in Pennsylvania 为过去分词短语作定语；主干 is used to produce heat or electricity，为被动语态；through combustion 为方式状语。"
        },
        "words": [
            {"w": "combustion", "pos": "n.", "def": "燃烧"},
            {"w": "electricity", "pos": "n.", "def": "电；电力"}
        ]
    },
    {
        "id": 13,
        "para": 3,
        "en": "Many schools and hospitals use wood boiler systems to heat and power their facilities, many homes are primarily heated with wood, and some coal plants incorporate wood into their coal streams to produce electricity.",
        "zh": "许多学校和医院用木材锅炉系统来为其设施供暖供电，许多家庭主要靠木材取暖，还有一些燃煤电厂把木材掺入煤流中来发电。",
        "grammar": {
            "type": "三个并列分句 + 不定式目的状语",
            "note": "三个分句由逗号和 and 并列：Many schools and hospitals use wood boiler systems（to heat and power... 为目的状语）、many homes are primarily heated with wood、some coal plants incorporate wood into their coal streams（to produce electricity 为目的状语）。"
        },
        "words": [
            {"w": "boiler", "pos": "n.", "def": "锅炉"},
            {"w": "incorporate", "pos": "v.", "def": "掺入；使并入"}
        ]
    },
    {
        "id": 14,
        "para": 3,
        "en": "Wood can also be gasified for electrical generation and can even be made into liquid fuels like ethanol and gasoline for lorries and cars.",
        "zh": "木材还可以被气化用于发电，甚至可以被制成乙醇、汽油之类的液体燃料，供货车和汽车使用。",
        "grammar": {
            "type": "并列被动谓语",
            "note": "主语 Wood 带两个并列的情态被动谓语：can also be gasified for electrical generation 和 can even be made into liquid fuels；like ethanol and gasoline 举例，for lorries and cars 为用途状语。"
        },
        "words": [
            {"w": "gasify", "pos": "v.", "def": "使气化"},
            {"w": "ethanol", "pos": "n.", "def": "乙醇；酒精"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "All these products are made primarily from low-use wood.",
        "zh": "所有这些产品主要都是用低用途木材制成的。",
        "grammar": {
            "type": "被动语态",
            "note": "主干是 All these products are made primarily from low-use wood，为被动语态；primarily 作状语表“主要地”。"
        },
        "words": [
            {"w": "primarily", "pos": "adv.", "def": "主要地"},
            {"w": "product", "pos": "n.", "def": "产品"}
        ]
    },
    {
        "id": 16,
        "para": 3,
        "en": "Several tree- and plant-cutting approaches, which could greatly improve the long-term quality of a forest, focus strongly or solely on the use of wood for those markets.",
        "zh": "若干种树木和植物的采伐方法——它们本可以大大提升森林的长期质量——却把重点强烈甚至完全放在为那些市场供应木材上。",
        "grammar": {
            "type": "非限定性定语从句作插入语",
            "note": "主干是 Several tree- and plant-cutting approaches... focus strongly or solely on the use of wood；which could greatly improve the long-term quality of a forest 为非限定性定语从句作插入语修饰 approaches。"
        },
        "words": [
            {"w": "approach", "pos": "n.", "def": "方法；途径"},
            {"w": "long-term", "pos": "adj.", "def": "长期的"}
        ]
    },
    # Paragraph D (para 4)
    {
        "id": 17,
        "para": 4,
        "en": "One such approach is called a Timber Stand Improvement (TSI) Cut.",
        "zh": "其中一种这样的方法叫作“林分改良（TSI）采伐”。",
        "grammar": {
            "type": "被动语态",
            "note": "主干是 One such approach is called a Timber Stand Improvement (TSI) Cut，为被动语态，call sth sth 的被动形式。"
        },
        "words": [
            {"w": "timber stand", "pos": "phr.", "def": "林分（成片生长、特征相近的林木）"},
            {"w": "improvement", "pos": "n.", "def": "改良；改善"}
        ]
    },
    {
        "id": 18,
        "para": 4,
        "en": "In a TSI Cut, really poor-quality tree and plant material is cut down to allow more space, light, and other resources to the highest-valued stems that remain.",
        "zh": "在林分改良采伐中，质量很差的树木和植物会被砍掉，以便给留下来的最有价值的树干腾出更多空间、阳光和其他资源。",
        "grammar": {
            "type": "被动语态 + 不定式目的状语 + 定语从句",
            "note": "主干是 really poor-quality tree and plant material is cut down，为被动语态；to allow more space, light, and other resources to the highest-valued stems 为不定式作目的状语；that remain 为定语从句修饰 stems。"
        },
        "words": [
            {"w": "poor-quality", "pos": "adj.", "def": "劣质的；质量差的"},
            {"w": "remain", "pos": "v.", "def": "留下；剩余"}
        ]
    },
    {
        "id": 19,
        "para": 4,
        "en": "Removing invasive plants might be another primary goal of a TSI Cut.",
        "zh": "清除入侵植物可能是林分改良采伐的另一个主要目标。",
        "grammar": {
            "type": "动名词作主语",
            "note": "主干是 Removing invasive plants might be another primary goal；Removing invasive plants 为动名词短语作主语；might 表推测。"
        },
        "words": [
            {"w": "invasive", "pos": "adj.", "def": "入侵的；侵袭性的"},
            {"w": "primary", "pos": "adj.", "def": "主要的；首要的"}
        ]
    },
    {
        "id": 20,
        "para": 4,
        "en": "The stems that are left behind might then grow in size and develop more foliage and larger crowns or tops that produce more coverage for wildlife; they have a better chance to regenerate in a less crowded environment.",
        "zh": "被留下来的树干随后可能会长粗，并长出更多枝叶、更大的树冠或树顶，从而为野生动物提供更多遮蔽；在不那么拥挤的环境里，它们也有更好的更新机会。",
        "grammar": {
            "type": "定语从句 + 并列谓语 + 分号并列",
            "note": "前半主干 The stems... might then grow in size and develop more foliage and larger crowns or tops，that are left behind 修饰 stems，that produce more coverage for wildlife 修饰 crowns or tops；分号后 they have a better chance to regenerate 为并列句。"
        },
        "words": [
            {"w": "foliage", "pos": "n.", "def": "枝叶；叶子（总称）"},
            {"w": "crown", "pos": "n.", "def": "树冠"}
        ]
    },
    {
        "id": 21,
        "para": 4,
        "en": "TSI Cuts can be tailored to one farmer" + RSQUO + "s specific management goals for his or her land.",
        "zh": "林分改良采伐可以根据某个农场主对自己土地的具体经营目标来量身定制。",
        "grammar": {
            "type": "被动语态 + 介词短语",
            "note": "主干是 TSI Cuts can be tailored to one farmer" + RSQUO + "s specific management goals，为被动语态，be tailored to 表“为……量身定制”；for his or her land 为介词短语修饰 goals。"
        },
        "words": [
            {"w": "tailor", "pos": "v.", "def": "使适合；量身定制"},
            {"w": "specific", "pos": "adj.", "def": "具体的；特定的"}
        ]
    },
    # Paragraph E (para 5)
    {
        "id": 22,
        "para": 5,
        "en": "Another approach that might yield a high amount of low-use wood is a Salvage Cut.",
        "zh": "另一种可能产出大量低用途木材的方法是“抢救性采伐”。",
        "grammar": {
            "type": "定语从句 + 主系表",
            "note": "主干是 Another approach... is a Salvage Cut；that might yield a high amount of low-use wood 为定语从句修饰 approach。"
        },
        "words": [
            {"w": "yield", "pos": "v.", "def": "产出；出产"},
            {"w": "salvage", "pos": "n.", "def": "抢救；打捞（利用）"}
        ]
    },
    {
        "id": 23,
        "para": 5,
        "en": "With the many pests and pathogens visiting forests including hemlock wooly adelgid, Asian longhorned beetle, emerald ash borer, and gypsy moth, to name just a few, it is important to remember that those working in the forests can help ease these issues through cutting procedures.",
        "zh": "鉴于有众多害虫和病原体侵袭森林——仅举几例，就有铁杉球蚜、亚洲天牛、白蜡窄吉丁和舞毒蛾——重要的是要记住，在森林里作业的人可以通过采伐手段帮助缓解这些问题。",
        "grammar": {
            "type": "with 复合结构 + it 形式主语 + 宾语从句",
            "note": "With the many pests and pathogens visiting forests... 为 with 复合结构作状语，including... 举例，to name just a few 为插入语；主句 it is important to remember that...，it 为形式主语，that 引导宾语从句，those working in the forests 为从句主语。"
        },
        "words": [
            {"w": "pathogen", "pos": "n.", "def": "病原体"},
            {"w": "ease", "pos": "v.", "def": "缓解；减轻"}
        ]
    },
    {
        "id": 24,
        "para": 5,
        "en": "These types of cut reduce the number of sick trees and seek to manage the future spread of a pest problem.",
        "zh": "这类采伐能减少病树的数量，并力图控制虫害问题未来的蔓延。",
        "grammar": {
            "type": "并列谓语",
            "note": "主语 These types of cut 带两个并列谓语 reduce the number of sick trees 和 seek to manage the future spread of a pest problem；seek to do 表“力求做”。"
        },
        "words": [
            {"w": "spread", "pos": "n.", "def": "蔓延；扩散"},
            {"w": "pest", "pos": "n.", "def": "害虫"}
        ]
    },
    {
        "id": 25,
        "para": 5,
        "en": "They leave vigorous trees that have stayed healthy enough to survive the outbreak.",
        "zh": "它们会留下那些一直足够健康、能够挺过这场（病虫害）暴发的强壮树木。",
        "grammar": {
            "type": "定语从句 + 结果状语",
            "note": "主干是 They leave vigorous trees；that have stayed healthy enough to survive the outbreak 为定语从句修饰 trees，enough to do 表“足以做”。"
        },
        "words": [
            {"w": "vigorous", "pos": "adj.", "def": "茁壮的；有活力的"},
            {"w": "outbreak", "pos": "n.", "def": "（疾病/虫害）暴发"}
        ]
    },
    # Paragraph F (para 6)
    {
        "id": 26,
        "para": 6,
        "en": "A Shelterwood Cut, which only takes place in a mature forest that has already been thinned several times, involves removing all the mature trees when other seedlings have become established.",
        "zh": "“庇护林采伐”只在已经间伐过数次的成熟森林中进行，其做法是在其他树苗已经扎根成活之后，把所有成熟的树木都移走。",
        "grammar": {
            "type": "非限定性定语从句 + 动名词宾语 + 时间状语从句",
            "note": "主干是 A Shelterwood Cut... involves removing all the mature trees；which only takes place in a mature forest 为非限定性定语从句，其中 that has already been thinned several times 再修饰 forest；when other seedlings have become established 为时间状语从句。"
        },
        "words": [
            {"w": "thin", "pos": "v.", "def": "间伐；使稀疏"},
            {"w": "seedling", "pos": "n.", "def": "树苗；幼苗"}
        ]
    },
    {
        "id": 27,
        "para": 6,
        "en": "This then allows the forester to decide which tree species are regenerated.",
        "zh": "这样一来，护林员便可以决定让哪些树种得到更新繁育。",
        "grammar": {
            "type": "allow sb to do + 宾语从句",
            "note": "主干是 This... allows the forester to decide...，allow sb to do 结构；which tree species are regenerated 为 decide 的宾语从句。"
        },
        "words": [
            {"w": "forester", "pos": "n.", "def": "护林员；林务员"},
            {"w": "regenerate", "pos": "v.", "def": "使再生；更新"}
        ]
    },
    {
        "id": 28,
        "para": 6,
        "en": "It leaves a young forest where all trees are at a similar point in their growth.",
        "zh": "它会造就一片年轻的森林，其中所有的树都处在生长的相近阶段。",
        "grammar": {
            "type": "定语从句",
            "note": "主干是 It leaves a young forest；where all trees are at a similar point in their growth 为定语从句修饰 forest，where 引导表地点。"
        },
        "words": [
            {"w": "similar", "pos": "adj.", "def": "相似的；类似的"},
            {"w": "growth", "pos": "n.", "def": "生长；成长"}
        ]
    },
    {
        "id": 29,
        "para": 6,
        "en": "It can also be used to develop a two-tier forest so that there are two harvests and the money that comes in is spread out over a decade or more.",
        "zh": "它也可以用来营造一片双层林，从而带来两次采伐收益，使收入分摊到十年甚至更长的时间里。",
        "grammar": {
            "type": "被动语态 + 目的/结果状语从句 + 定语从句",
            "note": "主干是 It can also be used to develop a two-tier forest，为被动语态；so that there are two harvests and the money... is spread out 为 so that 引导的结果状语从句；that comes in 为定语从句修饰 money。"
        },
        "words": [
            {"w": "two-tier", "pos": "adj.", "def": "双层的；两级的"},
            {"w": "spread out", "pos": "phr.", "def": "分散；分摊"}
        ]
    },
    # Paragraph G (para 7)
    {
        "id": 30,
        "para": 7,
        "en": "Thinnings and dense and dead wood removal for fire prevention also center on the production of low-use wood.",
        "zh": "为预防火灾而进行的间伐以及密林和枯木的清除，同样也围绕着低用途木材的产出。",
        "grammar": {
            "type": "并列主语 + 主谓",
            "note": "主语为并列的 Thinnings and dense and dead wood removal，for fire prevention 为目的修饰；谓语 center on the production of low-use wood，center on 表“以……为中心”。"
        },
        "words": [
            {"w": "removal", "pos": "n.", "def": "清除；移除"},
            {"w": "prevention", "pos": "n.", "def": "预防"}
        ]
    },
    {
        "id": 31,
        "para": 7,
        "en": "However, it is important to remember that some retention of what many would classify as low-use wood is very important.",
        "zh": "然而，重要的是要记住，保留一部分许多人会归为低用途木材的东西，其实非常重要。",
        "grammar": {
            "type": "it 形式主语 + 宾语从句 + 嵌套宾语从句",
            "note": "主干 it is important to remember that...，it 为形式主语；that 引导宾语从句，从句主干 some retention of... is very important；what many would classify as low-use wood 为 of 的宾语从句。"
        },
        "words": [
            {"w": "retention", "pos": "n.", "def": "保留；保持"},
            {"w": "classify", "pos": "v.", "def": "把……归类"}
        ]
    },
    {
        "id": 32,
        "para": 7,
        "en": "The tops of trees that have been cut down should be left on the site so that their nutrients cycle back into the soil.",
        "zh": "被砍倒的树木的树顶部分应留在原地，这样其中的养分才能循环回土壤中。",
        "grammar": {
            "type": "定语从句 + 目的状语从句",
            "note": "主干是 The tops of trees... should be left on the site；that have been cut down 为定语从句修饰 trees；so that their nutrients cycle back into the soil 为目的状语从句。"
        },
        "words": [
            {"w": "nutrient", "pos": "n.", "def": "养分；营养物"},
            {"w": "cycle", "pos": "v.", "def": "循环"}
        ]
    },
    {
        "id": 33,
        "para": 7,
        "en": "In addition, trees with many cavities are extremely important habitats for insect predators like woodpeckers, bats and small mammals.",
        "zh": "此外，有很多树洞的树木，是啄木鸟、蝙蝠和小型哺乳动物等食虫动物极其重要的栖息地。",
        "grammar": {
            "type": "主系表 + 举例",
            "note": "主干是 trees with many cavities are extremely important habitats；with many cavities 为介词短语修饰 trees；for insect predators 说明 habitats 的服务对象，like woodpeckers, bats and small mammals 举例；In addition 表递进。"
        },
        "words": [
            {"w": "cavity", "pos": "n.", "def": "洞；空腔"},
            {"w": "predator", "pos": "n.", "def": "捕食者；掠食动物"}
        ]
    },
    {
        "id": 34,
        "para": 7,
        "en": "They help control problem insects and increase the health and resilience of the forest.",
        "zh": "它们有助于控制有害昆虫，并提高森林的健康程度和恢复力。",
        "grammar": {
            "type": "并列谓语",
            "note": "主语 They 带两个并列谓语 help control problem insects 和 increase the health and resilience of the forest；help do 中省略 to。"
        },
        "words": [
            {"w": "resilience", "pos": "n.", "def": "恢复力；韧性"},
            {"w": "control", "pos": "v.", "def": "控制"}
        ]
    },
    {
        "id": 35,
        "para": 7,
        "en": "It is also important to remember that not all small trees are low-use.",
        "zh": "同样重要的是要记住，并非所有的小树都是低用途的。",
        "grammar": {
            "type": "it 形式主语 + 宾语从句 + 部分否定",
            "note": "主干 It is also important to remember that...，it 为形式主语；that 引导宾语从句 not all small trees are low-use，not all 为部分否定，表“并非所有……都”。"
        },
        "words": [
            {"w": "remember", "pos": "v.", "def": "记住"},
            {"w": "not all", "pos": "phr.", "def": "并非所有（部分否定）"}
        ]
    },
    {
        "id": 36,
        "para": 7,
        "en": "For example, many species like hawthorn provide food for wildlife.",
        "zh": "例如，山楂之类的许多树种能为野生动物提供食物。",
        "grammar": {
            "type": "主谓宾 + 举例",
            "note": "主干是 many species... provide food for wildlife；like hawthorn 举例修饰 species；For example 表举例。"
        },
        "words": [
            {"w": "hawthorn", "pos": "n.", "def": "山楂（树）"},
            {"w": "species", "pos": "n.", "def": "物种；种类"}
        ]
    },
    {
        "id": 37,
        "para": 7,
        "en": "Finally, rare species of trees in a forest should also stay behind as they add to its structural diversity.",
        "zh": "最后，森林中稀有的树种也应当被保留下来，因为它们能增加森林的结构多样性。",
        "grammar": {
            "type": "主谓 + 原因状语从句",
            "note": "主干是 rare species of trees... should also stay behind；as they add to its structural diversity 为原因状语从句，as 表“因为”；Finally 表总结。"
        },
        "words": [
            {"w": "rare", "pos": "adj.", "def": "稀有的；罕见的"},
            {"w": "diversity", "pos": "n.", "def": "多样性"}
        ]
    }
]

questions = [
    {
        "title": "Questions 14" + DASH + "18",
        "type": "matching_information",
        "instructions": [
            "Reading Passage 2 has seven paragraphs, A" + DASH + "G.",
            "Which paragraph contains the following information?",
            "Write the correct letter, A" + DASH + "G, in boxes 14" + DASH + "18 on your answer sheet.",
            "NB You may use any letter more than once."
        ],
        "items": [
            {"number": 14, "prompt": "bad outcomes for a forest when people focus only on its financial reward", "answer": "B", "evidence_sentence": 9},
            {"number": 15, "prompt": "reference to the aspects of any tree that contribute to its worth", "answer": "A", "evidence_sentence": 1},
            {"number": 16, "prompt": "mention of the potential use of wood to help run vehicles", "answer": "C", "evidence_sentence": 14},
            {"number": 17, "prompt": "examples of insects that attack trees", "answer": "E", "evidence_sentence": 23},
            {"number": 18, "prompt": "an alternative name for trees that produce low-use wood", "answer": "B", "evidence_sentence": 8}
        ]
    },
    {
        "title": "Questions 19" + DASH + "21",
        "type": "matching_features",
        "instructions": [
            "Look at the following purposes (Questions 19" + DASH + "21) and the list of timber cuts below.",
            "Match each purpose with the correct timber cut, A, B or C.",
            "Write the correct letter, A, B or C, in boxes 19" + DASH + "21 on your answer sheet.",
            "NB You may use any letter more than once.",
            "List of Timber Cuts",
            "A a TSI Cut",
            "B a Salvage Cut",
            "C a Shelterwood Cut"
        ],
        "items": [
            {"number": 19, "prompt": "to remove trees that are diseased", "answer": "B", "evidence_sentence": 24},
            {"number": 20, "prompt": "to generate income across a number of years", "answer": "C", "evidence_sentence": 29},
            {"number": 21, "prompt": "to create a forest whose trees are close in age", "answer": "C", "evidence_sentence": 28}
        ]
    },
    {
        "title": "Questions 22" + DASH + "26",
        "type": "sentence_completion",
        "instructions": [
            "Complete the sentences below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 22" + DASH + "26 on your answer sheet."
        ],
        "items": [
            {"number": 22, "prompt": "Some dead wood is removed to avoid the possibility of ____ .", "answer": "fire", "evidence_sentence": 30},
            {"number": 23, "prompt": "The ____ from the tops of cut trees can help improve soil quality.", "answer": "nutrients", "evidence_sentence": 32},
            {"number": 24, "prompt": "Some damaged trees should be left, as their ____ provide habitats for a range of creatures.", "answer": "cavities", "evidence_sentence": 33},
            {"number": 25, "prompt": "Some trees that are small, such as ____ , are a source of food for animals and insects.", "answer": "hawthorn", "evidence_sentence": 36},
            {"number": 26, "prompt": "Any trees that are ____ should be left to grow, as they add to the variety of species in the forest.", "answer": "rare", "evidence_sentence": 37}
        ]
    }
]

phrases = [
    {"w": "forest management", "pos": "n.", "def": "森林经营；森林管理"},
    {"w": "low-use wood", "pos": "n.", "def": "低用途木材"},
    {"w": "high-grading", "pos": "n.", "def": "择优采伐"},
    {"w": "TSI Cut (Timber Stand Improvement Cut)", "pos": "n.", "def": "林分改良采伐"},
    {"w": "Salvage Cut", "pos": "n.", "def": "抢救性采伐"},
    {"w": "Shelterwood Cut", "pos": "n.", "def": "庇护林采伐"},
    {"w": "black cherry tree", "pos": "n.", "def": "黑樱桃树"},
    {"w": "black knot disease", "pos": "n.", "def": "黑瘤病（樱桃等果树的一种真菌病）"},
    {"w": "wood energy market", "pos": "n.", "def": "木材能源市场"},
    {"w": "structural diversity", "pos": "n.", "def": "结构多样性"}
]

data = {
    "id": "c18-test1-p2",
    "source": "剑桥雅思18 · Test 1 · Passage 2",
    "title": "Forest management in Pennsylvania, USA",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "subtitle": "How managing low-quality wood (also known as low-use wood) for bioenergy can encourage sustainable forest management",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c18-test1-p2.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
