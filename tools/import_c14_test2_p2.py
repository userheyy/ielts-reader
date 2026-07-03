# -*- coding: utf-8 -*-
"""Generate data/passages/c14-test2-p2.json (Back to the future of skyscraper design)."""
import json
import os

RSQUO = "’"
LSQUO = "‘"
DASH = "–"
PCT = "%"

sentences = [
    # Section A (1)
    {
        "id": 1,
        "para": 1,
        "en": "The Recovery of Natural Environments in Architecture by Professor Alan Short is the culmination of 30 years of research and award-winning green building design by Short and colleagues in Architecture, Engineering, Applied Maths and Earth Sciences at the University of Cambridge.",
        "zh": "艾伦·肖特教授所著的《建筑中自然环境的复兴》一书，是肖特及其在剑桥大学建筑学、工程学、应用数学和地球科学领域的同事们30年研究与屡获殊荣的绿色建筑设计的集大成之作。",
        "grammar": {
            "type": "主系表 + 后置定语",
            "note": "主干 The Recovery of Natural Environments in Architecture... is the culmination of 30 years of research and... green building design；by Professor Alan Short 与 by Short and colleagues in... 为后置定语，说明作者/设计者。"
        },
        "words": [
            {"w": "culmination", "pos": "n.", "def": "顶点；最高潮；集大成"},
            {"w": "award-winning", "pos": "adj.", "def": "获奖的"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": LSQUO + "The crisis in building design is already here," + RSQUO + " said Short. " + LSQUO + "Policy makers think you can solve energy and building problems with gadgets. You can" + RSQUO + "t." + RSQUO,
        "zh": "“建筑设计的危机已经到来，”肖特说。“政策制定者认为你可以用一些小装置来解决能源和建筑问题。你不能。”",
        "grammar": {
            "type": "直接引语 + 宾语从句",
            "note": "首句 The crisis in building design is already here 为主系表；Policy makers think (that) you can solve... with gadgets 含省略 that 的宾语从句；末句 You can't 为省略句（=You can't solve them with gadgets）。"
        },
        "words": [
            {"w": "crisis", "pos": "n.", "def": "危机"},
            {"w": "gadget", "pos": "n.", "def": "小装置；小器械"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": LSQUO + "As global temperatures continue to rise, we are going to continue to squander more and more energy on keeping our buildings mechanically cool until we have run out of capacity." + RSQUO,
        "zh": "“随着全球气温持续上升，我们将继续在用机械手段给建筑降温上浪费越来越多的能源，直到耗尽我们的（供能）能力为止。”",
        "grammar": {
            "type": "As 时间状语从句 + until 从句",
            "note": "As global temperatures continue to rise 为 as 引导的时间状语从句；主句 we are going to continue to squander more and more energy on...；until we have run out of capacity 为 until 引导的时间状语从句，run out of 意为“用尽”。"
        },
        "words": [
            {"w": "squander", "pos": "v.", "def": "浪费；挥霍"},
            {"w": "run out of", "pos": "phr.", "def": "用尽；耗尽"}
        ]
    },
    # Section B (2)
    {
        "id": 4,
        "para": 2,
        "en": "Short is calling for a sweeping reinvention of how skyscrapers and major public buildings are designed " + DASH + " to end the reliance on sealed buildings which exist solely via the " + LSQUO + "life support" + RSQUO + " system of vast air conditioning units.",
        "zh": "肖特呼吁彻底重新构想摩天大楼和大型公共建筑的设计方式——以终结对密闭建筑的依赖，这类建筑仅靠庞大空调机组这一“生命维持”系统才得以存在。",
        "grammar": {
            "type": "call for + 宾语从句 + 不定式目的 + 定语从句",
            "note": "主干 Short is calling for a sweeping reinvention of how...，how skyscrapers and major public buildings are designed 为介词宾语从句；破折号后 to end the reliance on sealed buildings 为不定式目的状语；which exist solely via... 为定语从句修饰 buildings。"
        },
        "words": [
            {"w": "sweeping", "pos": "adj.", "def": "彻底的；影响广泛的"},
            {"w": "reinvention", "pos": "n.", "def": "彻底革新；重新构想"}
        ]
    },
    {
        "id": 5,
        "para": 2,
        "en": "Instead, he shows it is entirely possible to accommodate natural ventilation and cooling in large buildings by looking into the past, before the widespread introduction of air conditioning systems, which were " + LSQUO + "relentlessly and aggressively marketed" + RSQUO + " by their inventors.",
        "zh": "相反，他表明，通过回顾过去——回到空调系统被广泛引入之前——完全有可能在大型建筑中实现自然通风与降温；而当年空调系统曾被其发明者“不遗余力、咄咄逼人地推向市场”。",
        "grammar": {
            "type": "宾语从句 + by 方式状语 + 非限制性定语从句",
            "note": "主干 he shows (that) it is entirely possible to accommodate...，it 为形式主语；by looking into the past 为方式状语；before the widespread introduction of air conditioning systems 为时间状语；which were 'relentlessly and aggressively marketed' by their inventors 为非限制性定语从句。"
        },
        "words": [
            {"w": "accommodate", "pos": "v.", "def": "容纳；使适应"},
            {"w": "ventilation", "pos": "n.", "def": "通风；空气流通"}
        ]
    },
    # Section C (3)
    {
        "id": 6,
        "para": 3,
        "en": "Short points out that to make most contemporary buildings habitable, they have to be sealed and air conditioned.",
        "zh": "肖特指出，为了让大多数当代建筑适宜居住，它们不得不被密封并安装空调。",
        "grammar": {
            "type": "宾语从句 + 不定式目的",
            "note": "主干 Short points out that...；从句 they have to be sealed and air conditioned；to make most contemporary buildings habitable 为不定式作目的状语，make sth habitable 为复合宾语。"
        },
        "words": [
            {"w": "contemporary", "pos": "adj.", "def": "当代的；现代的"},
            {"w": "habitable", "pos": "adj.", "def": "适宜居住的"}
        ]
    },
    {
        "id": 7,
        "para": 3,
        "en": "The energy use and carbon emissions this generates is spectacular and largely unnecessary.",
        "zh": "由此产生的能源消耗和碳排放极其惊人，而且在很大程度上并无必要。",
        "grammar": {
            "type": "省略关系词定语从句",
            "note": "主语 The energy use and carbon emissions，(that) this generates 为省略关系词的定语从句修饰前面的名词；谓语 is spectacular and largely unnecessary。"
        },
        "words": [
            {"w": "emission", "pos": "n.", "def": "排放；排放物"},
            {"w": "spectacular", "pos": "adj.", "def": "惊人的；壮观的"}
        ]
    },
    {
        "id": 8,
        "para": 3,
        "en": "Buildings in the West account for 40" + DASH + "50" + PCT + " of electricity usage, generating substantial carbon emissions, and the rest of the world is catching up at a frightening rate.",
        "zh": "西方国家的建筑消耗了40%到50%的电力，产生了大量碳排放，而世界其他地区正以惊人的速度迎头赶上。",
        "grammar": {
            "type": "account for + 现在分词状语 + and 并列",
            "note": "前一分句 Buildings in the West account for 40–50% of electricity usage，account for 意为“占（比例）”；generating substantial carbon emissions 为现在分词状语；and 连接 the rest of the world is catching up at a frightening rate。"
        },
        "words": [
            {"w": "account for", "pos": "phr.", "def": "占（比例）；解释"},
            {"w": "catch up", "pos": "phr.", "def": "追赶；赶上"}
        ]
    },
    {
        "id": 9,
        "para": 3,
        "en": "Short regards glass, steel and air-conditioned skyscrapers as symbols of status, rather than practical ways of meeting our requirements.",
        "zh": "肖特把玻璃、钢材和带空调的摩天大楼视为地位的象征，而非满足我们需求的实用方式。",
        "grammar": {
            "type": "regard as + rather than 对比",
            "note": "主干 Short regards... skyscrapers as symbols of status，regard A as B 结构；rather than practical ways of meeting our requirements 用 rather than 构成对比。"
        },
        "words": [
            {"w": "regard as", "pos": "phr.", "def": "把……视为"},
            {"w": "status", "pos": "n.", "def": "地位；身份"}
        ]
    },
    # Section D (4)
    {
        "id": 10,
        "para": 4,
        "en": "Short" + RSQUO + "s book highlights a developing and sophisticated art and science of ventilating buildings through the 19th and earlier-20th centuries, including the design of ingeniously ventilated hospitals.",
        "zh": "肖特的书着重介绍了19世纪至20世纪早期一门不断发展、日益精妙的建筑通风艺术与科学，其中包括通风设计巧妙的医院。",
        "grammar": {
            "type": "主谓宾 + including 举例",
            "note": "主干 Short's book highlights a developing and sophisticated art and science of ventilating buildings；through the 19th and earlier-20th centuries 为时间状语；including the design of ingeniously ventilated hospitals 为举例补充。"
        },
        "words": [
            {"w": "highlight", "pos": "v.", "def": "突出；强调"},
            {"w": "ingeniously", "pos": "adv.", "def": "巧妙地；别出心裁地"}
        ]
    },
    {
        "id": 11,
        "para": 4,
        "en": "Of particular interest were those built to the designs of John Shaw Billings, including the first Johns Hopkins Hospital in the US city of Baltimore (1873" + DASH + "1889).",
        "zh": "尤其令人感兴趣的，是那些按照约翰·肖·比林斯的设计建造的医院，其中包括美国巴尔的摩市的第一座约翰斯·霍普金斯医院（1873—1889年）。",
        "grammar": {
            "type": "表语前置倒装 + 过去分词定语",
            "note": "Of particular interest were those... 为表语提前引起的完全倒装，正常语序为 Those... were of particular interest；built to the designs of John Shaw Billings 为过去分词定语修饰 those；including... 为举例。"
        },
        "words": [
            {"w": "of particular interest", "pos": "phr.", "def": "尤其令人感兴趣的"},
            {"w": "design", "pos": "n.", "def": "设计；图样"}
        ]
    },
    {
        "id": 12,
        "para": 4,
        "en": LSQUO + "We spent three years digitally modelling Billings" + RSQUO + " final designs," + RSQUO + " says Short. " + LSQUO + "We put pathogens in the airstreams, modelled for someone with tuberculosis (TB) coughing in the wards and we found the ventilation systems in the room would have kept other patients safe from harm." + RSQUO,
        "zh": "“我们花了三年时间对比林斯的最终设计进行数字建模，”肖特说。“我们在气流中放入病原体，模拟一名结核病（TB）患者在病房里咳嗽的情形，结果发现房间里的通风系统本可以使其他病人免受伤害。”",
        "grammar": {
            "type": "过去分词状语 + 宾语从句 + 虚拟语气",
            "note": "首句 We spent three years digitally modelling...，spend time doing 结构；后句含并列谓语 put... modelled... and found...，modelled for someone... coughing 为过去分词状语；we found (that) the ventilation systems... would have kept other patients safe，would have kept 为对过去的虚拟推测。"
        },
        "words": [
            {"w": "pathogen", "pos": "n.", "def": "病原体（可致病的微生物）"},
            {"w": "tuberculosis", "pos": "n.", "def": "结核病；肺结核"}
        ]
    },
    # Section E (5)
    {
        "id": 13,
        "para": 5,
        "en": LSQUO + "We discovered that 19th-century hospital wards could generate up to 24 air changes an hour " + DASH + " that" + RSQUO + "s similar to the performance of a modern-day, computer-controlled operating theatre. We believe you could build wards based on these principles now." + RSQUO,
        "zh": "“我们发现，19世纪的医院病房每小时可实现多达24次的空气交换——这与现代由计算机控制的手术室的性能相当。我们相信，如今你完全可以依据这些原理来建造病房。”",
        "grammar": {
            "type": "宾语从句 + 破折号补充 + 过去分词定语",
            "note": "首句 We discovered that 19th-century hospital wards could generate up to 24 air changes an hour，that 引导宾语从句；破折号后 that's similar to... 为补充说明；末句 you could build wards based on these principles now，based on these principles 为过去分词定语修饰 wards。"
        },
        "words": [
            {"w": "generate", "pos": "v.", "def": "产生；生成"},
            {"w": "operating theatre", "pos": "n.", "def": "手术室"}
        ]
    },
    {
        "id": 14,
        "para": 5,
        "en": "Single rooms are not appropriate for all patients. Communal wards appropriate for certain patients " + DASH + " older people with dementia, for example " + DASH + " would work just as well in today" + RSQUO + "s hospitals, at a fraction of the energy cost." + RSQUO,
        "zh": "“单人病房并不适合所有病人。适合某些病人——比如患有痴呆症的老年人——的公共病房，在今天的医院里同样能发挥很好的作用，而能耗只是其一小部分。”",
        "grammar": {
            "type": "形容词短语后置定语 + 破折号插入",
            "note": "首句 Single rooms are not appropriate for all patients；后句主语 Communal wards，appropriate for certain patients 为形容词短语后置定语，两破折号间 older people with dementia, for example 为举例插入；谓语 would work just as well；at a fraction of the energy cost 为状语，a fraction of 意为“一小部分”。"
        },
        "words": [
            {"w": "communal", "pos": "adj.", "def": "公共的；共用的"},
            {"w": "dementia", "pos": "n.", "def": "痴呆症"}
        ]
    },
    {
        "id": 15,
        "para": 5,
        "en": "Professor Short contends the mindset and skill-sets behind these designs have been completely lost, lamenting the disappearance of expertly designed theatres, opera houses, and other buildings where up to half the volume of the building was given over to ensuring everyone got fresh air.",
        "zh": "肖特教授认为，这些设计背后的思维方式和技能已经完全失传，他惋惜那些精心设计的剧院、歌剧院及其他建筑的消失——在这些建筑中，多达一半的建筑体积被用于确保每个人都能呼吸到新鲜空气。",
        "grammar": {
            "type": "宾语从句 + 现在分词状语 + where 定语从句",
            "note": "主干 Professor Short contends (that) the mindset and skill-sets... have been completely lost；lamenting the disappearance of... 为现在分词状语；where up to half the volume... was given over to ensuring... 为定语从句修饰前述 buildings，be given over to 意为“被用于”。"
        },
        "words": [
            {"w": "contend", "pos": "v.", "def": "主张；声称"},
            {"w": "lament", "pos": "v.", "def": "哀叹；惋惜"}
        ]
    },
    # Section F (6)
    {
        "id": 16,
        "para": 6,
        "en": "Much of the ingenuity present in 19th-century hospital and building design was driven by a panicked public clamouring for buildings that could protect against what was thought to be the lethal threat of miasmas " + DASH + " toxic air that spread disease.",
        "zh": "19世纪医院及建筑设计中的诸多巧思，源于惊恐的公众对能抵御瘴气（当时被认为是致命威胁）的建筑的强烈呼求——瘴气即传播疾病的有毒空气。",
        "grammar": {
            "type": "被动语态 + 定语从句 + 宾语从句 + 破折号同位",
            "note": "主干 Much of the ingenuity... was driven by a panicked public（被动）；clamouring for buildings 为现在分词定语修饰 public；that could protect against... 为定语从句，what was thought to be the lethal threat of miasmas 为宾语从句；破折号后 toxic air that spread disease 为 miasmas 的同位解释。"
        },
        "words": [
            {"w": "ingenuity", "pos": "n.", "def": "独创性；巧妙构思"},
            {"w": "miasma", "pos": "n.", "def": "瘴气；毒气"}
        ]
    },
    {
        "id": 17,
        "para": 6,
        "en": "Miasmas were feared as the principal agents of disease and epidemics for centuries, and were used to explain the spread of infection from the Middle Ages right through to the cholera outbreaks in London and Paris during the 1850s.",
        "zh": "数百年来，瘴气一直被视为疾病和瘟疫的主要致因而令人恐惧，并被用来解释从中世纪一直到19世纪50年代伦敦和巴黎霍乱暴发期间感染的传播。",
        "grammar": {
            "type": "被动语态并列谓语 + 不定式",
            "note": "主语 Miasmas 带两并列被动谓语 were feared as... 与 were used to explain...；from the Middle Ages right through to the cholera outbreaks... 为时间范围状语，right through to 意为“一直到”。"
        },
        "words": [
            {"w": "epidemic", "pos": "n.", "def": "流行病；瘟疫"},
            {"w": "cholera", "pos": "n.", "def": "霍乱"}
        ]
    },
    {
        "id": 18,
        "para": 6,
        "en": "Foul air, rather than germs, was believed to be the main driver of " + LSQUO + "hospital fever" + RSQUO + ", leading to disease and frequent death. The prosperous steered clear of hospitals.",
        "zh": "人们曾认为，是污浊的空气而非病菌，才是“医院热”的主要诱因，从而导致疾病和频繁的死亡。富裕阶层因此对医院敬而远之。",
        "grammar": {
            "type": "被动语态 + rather than 插入 + 现在分词状语",
            "note": "首句 Foul air... was believed to be the main driver of 'hospital fever'，rather than germs 为插入对比；leading to disease and frequent death 为现在分词状语；后句 The prosperous steered clear of hospitals，The prosperous 为“the+形容词”表一类人，steer clear of 意为“避开”。"
        },
        "words": [
            {"w": "foul", "pos": "adj.", "def": "污浊的；恶臭的"},
            {"w": "steer clear of", "pos": "phr.", "def": "避开；绕开"}
        ]
    },
    {
        "id": 19,
        "para": 6,
        "en": "While miasma theory has been long since disproved, Short has for the last 30 years advocated a return to some of the building design principles produced in its wake.",
        "zh": "尽管瘴气理论早已被推翻，肖特在过去30年里却一直主张回归当年在其影响下产生的某些建筑设计原则。",
        "grammar": {
            "type": "While 让步从句 + 现在完成时 + 过去分词定语",
            "note": "While miasma theory has been long since disproved 为让步状语从句；主句 Short has... advocated a return to some of the building design principles；produced in its wake 为过去分词定语修饰 principles，in its wake 意为“在其之后、随之而来”。"
        },
        "words": [
            {"w": "disprove", "pos": "v.", "def": "证明……错误；驳倒"},
            {"w": "in its wake", "pos": "phr.", "def": "随之而来；紧随其后"}
        ]
    },
    # Section G (7)
    {
        "id": 20,
        "para": 7,
        "en": "Today, huge amounts of a building" + RSQUO + "s space and construction cost are given over to air conditioning.",
        "zh": "如今，一座建筑的大量空间和建造成本都被用于空调系统。",
        "grammar": {
            "type": "被动语态",
            "note": "主干 huge amounts of a building's space and construction cost are given over to air conditioning（被动），be given over to 意为“被用于、被划归”。"
        },
        "words": [
            {"w": "construction cost", "pos": "n.", "def": "建造成本"},
            {"w": "be given over to", "pos": "phr.", "def": "被用于；被划作"}
        ]
    },
    {
        "id": 21,
        "para": 7,
        "en": LSQUO + "But I have designed and built a series of buildings over the past three decades which have tried to reinvent some of these ideas and then measure what happens." + RSQUO,
        "zh": "“但在过去三十年里，我设计并建造了一系列建筑，试图重新构想其中一些理念，然后测量会发生什么。”",
        "grammar": {
            "type": "现在完成时 + 定语从句 + 宾语从句",
            "note": "主干 I have designed and built a series of buildings；which have tried to reinvent some of these ideas and then measure what happens 为定语从句修饰 buildings，其中 what happens 为 measure 的宾语从句。"
        },
        "words": [
            {"w": "reinvent", "pos": "v.", "def": "重新构想；彻底革新"},
            {"w": "measure", "pos": "v.", "def": "测量；衡量"}
        ]
    },
    {
        "id": 22,
        "para": 7,
        "en": LSQUO + "To go forward into our new low-energy, low-carbon future, we would be well advised to look back at design before our high-energy, high-carbon present appeared. What is surprising is what a rich legacy we have abandoned." + RSQUO,
        "zh": "“要迈入我们全新的低能耗、低碳的未来，我们最好回顾一下在这个高能耗、高碳的当下出现之前的设计。令人惊讶的是，我们竟然抛弃了如此丰厚的遗产。”",
        "grammar": {
            "type": "不定式状语 + 主语从句 + 感叹句宾语从句",
            "note": "首句 To go forward into... 为不定式目的状语，主句 we would be well advised to look back at design，before... present appeared 为时间从句；末句 What is surprising is what a rich legacy we have abandoned，前一 what 引导主语从句，后一 what a rich legacy... 为感叹语气的表语从句。"
        },
        "words": [
            {"w": "be well advised to", "pos": "phr.", "def": "最好……；明智的做法是"},
            {"w": "legacy", "pos": "n.", "def": "遗产；遗留物"}
        ]
    },
    # Section H (8)
    {
        "id": 23,
        "para": 8,
        "en": "Successful examples of Short" + RSQUO + "s approach include the Queen" + RSQUO + "s Building at De Montfort University in Leicester.",
        "zh": "肖特这一方法的成功范例，包括莱斯特德蒙福特大学的女王大楼。",
        "grammar": {
            "type": "主谓宾",
            "note": "主干 Successful examples of Short's approach include the Queen's Building；at De Montfort University in Leicester 为地点定语。"
        },
        "words": [
            {"w": "approach", "pos": "n.", "def": "方法；途径"},
            {"w": "example", "pos": "n.", "def": "范例；例子"}
        ]
    },
    {
        "id": 24,
        "para": 8,
        "en": "Containing as many as 2,000 staff and students, the entire building is naturally ventilated, passively cooled and naturally lit, including the two largest auditoria, each seating more than 150 people.",
        "zh": "这座能容纳多达2000名教职员工和学生的整栋建筑，采用自然通风、被动降温和自然采光，就连两个最大的礼堂（每个可容纳150多人）也是如此。",
        "grammar": {
            "type": "现在分词状语 + 被动并列 + 独立主格",
            "note": "Containing as many as 2,000 staff and students 为现在分词状语；主干 the entire building is naturally ventilated, passively cooled and naturally lit，三个被动并列；including the two largest auditoria 为补充，each seating more than 150 people 为独立主格结构。"
        },
        "words": [
            {"w": "passively", "pos": "adv.", "def": "被动地（此处指不借助机械）"},
            {"w": "auditoria", "pos": "n.", "def": "礼堂；观众席（auditorium 的复数）"}
        ]
    },
    {
        "id": 25,
        "para": 8,
        "en": "The award-winning building uses a fraction of the electricity of comparable buildings in the UK.",
        "zh": "这座获奖建筑的耗电量仅为英国同类建筑的一小部分。",
        "grammar": {
            "type": "主谓宾",
            "note": "主干 The award-winning building uses a fraction of the electricity；of comparable buildings in the UK 为后置定语，a fraction of 意为“……的一小部分”。"
        },
        "words": [
            {"w": "a fraction of", "pos": "phr.", "def": "……的一小部分"},
            {"w": "comparable", "pos": "adj.", "def": "可比的；类似的"}
        ]
    },
    {
        "id": 26,
        "para": 8,
        "en": "Short contends that glass skyscrapers in London and around the world will become a liability over the next 20 or 30 years if climate modelling predictions and energy price rises come to pass as expected.",
        "zh": "肖特认为，如果气候模型的预测和能源价格上涨如预期般成真，那么伦敦及世界各地的玻璃摩天大楼在未来二三十年里将成为一种累赘。",
        "grammar": {
            "type": "宾语从句 + if 条件从句",
            "note": "主干 Short contends that...；从句 glass skyscrapers... will become a liability over the next 20 or 30 years；if climate modelling predictions and energy price rises come to pass as expected 为条件状语从句，come to pass 意为“发生、成真”。"
        },
        "words": [
            {"w": "liability", "pos": "n.", "def": "累赘；负担；债务"},
            {"w": "come to pass", "pos": "phr.", "def": "发生；成为现实"}
        ]
    },
    # Section I (9)
    {
        "id": 27,
        "para": 9,
        "en": "He is convinced that sufficiently cooled skyscrapers using the natural environment can be produced in almost any climate.",
        "zh": "他坚信，利用自然环境实现充分降温的摩天大楼，几乎可以在任何气候条件下建造出来。",
        "grammar": {
            "type": "宾语从句 + 现在分词定语",
            "note": "主干 He is convinced that...；从句 sufficiently cooled skyscrapers... can be produced in almost any climate（被动）；using the natural environment 为现在分词定语修饰 skyscrapers。"
        },
        "words": [
            {"w": "be convinced that", "pos": "phr.", "def": "坚信；确信"},
            {"w": "sufficiently", "pos": "adv.", "def": "充分地；足够地"}
        ]
    },
    {
        "id": 28,
        "para": 9,
        "en": "He and his team have worked on hybrid buildings in the harsh climates of Beijing and Chicago " + DASH + " built with natural ventilation assisted by back-up air conditioning " + DASH + " which, surprisingly perhaps, can be switched off more than half the time on milder days and during the spring and autumn.",
        "zh": "他和他的团队曾在北京和芝加哥这样气候严酷的地方设计混合式建筑——这些建筑以自然通风为主、辅以备用空调——而或许令人意外的是，在较为温和的日子以及春秋两季，这些空调有一半以上的时间都可以关闭。",
        "grammar": {
            "type": "现在完成时 + 破折号插入(过去分词) + 定语从句",
            "note": "主干 He and his team have worked on hybrid buildings；两破折号间 built with natural ventilation assisted by back-up air conditioning 为过去分词短语插入定语；which... can be switched off more than half the time 为定语从句修饰 air conditioning/buildings。"
        },
        "words": [
            {"w": "hybrid", "pos": "adj.", "def": "混合的；混合式的"},
            {"w": "back-up", "pos": "adj.", "def": "备用的；后备的"}
        ]
    },
    {
        "id": 29,
        "para": 9,
        "en": "Short looks at how we might reimagine the cities, offices and homes of the future. Maybe it" + RSQUO + "s time we changed our outlook.",
        "zh": "肖特探讨了我们该如何重新构想未来的城市、办公室和住宅。或许，是时候改变我们的观念了。",
        "grammar": {
            "type": "宾语从句 + it" + RSQUO + "s time + 虚拟语气",
            "note": "首句 Short looks at how we might reimagine...，how 引导宾语从句；末句 it's time we changed our outlook，it's time (that) 后接从句用过去式表虚拟，意为“该……了”。"
        },
        "words": [
            {"w": "reimagine", "pos": "v.", "def": "重新构想；重新设想"},
            {"w": "outlook", "pos": "n.", "def": "观念；看法；前景"}
        ]
    }
]

questions = [
    {
        "title": "Questions 14" + DASH + "18",
        "type": "matching_information",
        "instructions": [
            "Reading Passage 2 has nine sections, A" + DASH + "I.",
            "Which section contains the following information?",
            "Write the correct letter, A" + DASH + "I, in boxes 14" + DASH + "18 on your answer sheet."
        ],
        "items": [
            {"number": 14, "prompt": "why some people avoided hospitals in the 19th century", "answer": "F", "evidence_sentence": 18},
            {"number": 15, "prompt": "a suggestion that the popularity of tall buildings is linked to prestige", "answer": "C", "evidence_sentence": 9},
            {"number": 16, "prompt": "a comparison between the circulation of air in a 19th-century building and modern standards", "answer": "E", "evidence_sentence": 13},
            {"number": 17, "prompt": "how Short tested the circulation of air in a 19th-century building", "answer": "D", "evidence_sentence": 12},
            {"number": 18, "prompt": "an implication that advertising led to the large increase in the use of air conditioning", "answer": "B", "evidence_sentence": 5}
        ]
    },
    {
        "title": "Questions 19" + DASH + "26",
        "type": "summary_completion",
        "instructions": [
            "Complete the summary below.",
            "Choose ONE WORD ONLY from the passage for each answer.",
            "Write your answers in boxes 19" + DASH + "26 on your answer sheet.",
            "Ventilation in 19th-century hospital wards"
        ],
        "items": [
            {"number": 19, "prompt": "Professor Alan Short examined the work of John Shaw Billings, who influenced the architectural 19 ____ of hospitals to ensure they had good ventilation.", "answer": "design", "evidence_sentence": 11},
            {"number": 20, "prompt": "He calculated that 20 ____ in the air coming from patients suffering from 21 ____ would not have harmed other patients.", "answer": "pathogens", "evidence_sentence": 12},
            {"number": 21, "prompt": "He calculated that pathogens in the air coming from patients suffering from 21 ____ would not have harmed other patients.", "answer": "tuberculosis", "evidence_sentence": 12},
            {"number": 22, "prompt": "He also found that the air in 22 ____ in hospitals could change as often as in a modern operating theatre.", "answer": "wards", "evidence_sentence": 13},
            {"number": 23, "prompt": "He suggests that energy use could be reduced by locating more patients in 23 ____ areas.", "answer": "communal", "evidence_sentence": 14},
            {"number": 24, "prompt": "A major reason for improving ventilation in 19th-century hospitals was the demand from the 24 ____ for protection against bad air, known as 25 ____ .", "answer": "public", "evidence_sentence": 16},
            {"number": 25, "prompt": "A major reason for improving ventilation in 19th-century hospitals was the demand from the public for protection against bad air, known as 25 ____ .", "answer": "miasmas", "evidence_sentence": 16},
            {"number": 26, "prompt": "These were blamed for the spread of disease for hundreds of years, including epidemics of 26 ____ in London and Paris in the middle of the 19th century.", "answer": "cholera", "evidence_sentence": 17}
        ]
    }
]

phrases = [
    {"w": "skyscraper", "pos": "n.", "def": "摩天大楼"},
    {"w": "air conditioning", "pos": "n.", "def": "空调；空气调节"},
    {"w": "natural ventilation", "pos": "n.", "def": "自然通风"},
    {"w": "carbon emissions", "pos": "n.", "def": "碳排放"},
    {"w": "green building design", "pos": "n.", "def": "绿色建筑设计"},
    {"w": "operating theatre", "pos": "n.", "def": "手术室"},
    {"w": "miasma theory", "pos": "n.", "def": "瘴气理论"},
    {"w": "hospital ward", "pos": "n.", "def": "医院病房"},
    {"w": "low-carbon", "pos": "adj.", "def": "低碳的"},
    {"w": "hospital fever", "pos": "n.", "def": "医院热（旧称院内感染性发热）"}
]

data = {
    "id": "c14-test2-p2",
    "source": "剑桥雅思14 · Test 2 · Passage 2",
    "title": "Back to the future of skyscraper design",
    "subtitle": "Answers to the problem of excessive electricity use by skyscrapers and large public buildings can be found in ingenious but forgotten architectural designs of the 19th and early-20th centuries",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c14-test2-p2.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
