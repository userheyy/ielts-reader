# -*- coding: utf-8 -*-
"""Generate data/passages/c15-test1-p2.json (Driverless cars)."""
import json
import os

RSQUO = "’"  # '
LSQUO = "‘"  # '
DASH = "–"   # –
PCT = "%"

sentences = [
    # Para A (1)
    {
        "id": 1,
        "para": 1,
        "en": "The automotive sector is well used to adapting to automation in manufacturing.",
        "zh": "汽车行业早已习惯于适应制造过程中的自动化。",
        "grammar": {
            "type": "主系表",
            "note": "be used to (doing) sth 意为 “习惯于（做）某事”，注意与 used to do（过去常常）区分；此处 to 为介词，后接动名词 adapting。"
        },
        "words": [
            {"w": "automotive", "pos": "adj.", "def": "汽车的"},
            {"w": "sector", "pos": "n.", "def": "行业；部门"},
            {"w": "be used to", "pos": "phr.", "def": "习惯于"},
            {"w": "automation", "pos": "n.", "def": "自动化"}
        ]
    },
    {
        "id": 2,
        "para": 1,
        "en": "The implementation of robotic car manufacture from the 1970s onwards led to significant cost savings and improvements in the reliability and flexibility of vehicle mass production.",
        "zh": "自20世纪70年代起，机器人汽车制造的实施带来了大幅的成本节约，并提升了车辆大规模生产的可靠性与灵活性。",
        "grammar": {
            "type": "简单句（长主语+宾语）",
            "note": "主语 The implementation of...，谓语 led to，宾语为并列的 cost savings and improvements...；from the 1970s onwards 意为 “自20世纪70年代起”。"
        },
        "words": [
            {"w": "implementation", "pos": "n.", "def": "实施；执行"},
            {"w": "led to", "pos": "phr.", "def": "导致；带来"},
            {"w": "reliability", "pos": "n.", "def": "可靠性"},
            {"w": "flexibility", "pos": "n.", "def": "灵活性"},
            {"w": "mass production", "pos": "phr.", "def": "大规模生产"}
        ]
    },
    {
        "id": 3,
        "para": 1,
        "en": "A new challenge to vehicle production is now on the horizon and, again, it comes from automation.",
        "zh": "车辆生产的一项新挑战如今已然临近，而它同样来自自动化。",
        "grammar": {
            "type": "并列句",
            "note": "and 连接两分句；on the horizon 意为 “即将出现、在望”；it 指代 A new challenge。"
        },
        "words": [
            {"w": "challenge", "pos": "n.", "def": "挑战"},
            {"w": "on the horizon", "pos": "phr.", "def": "即将出现；在望"}
        ]
    },
    {
        "id": 4,
        "para": 1,
        "en": "However, this time it is not to do with the manufacturing process, but with the vehicles themselves.",
        "zh": "然而，这一次它与制造过程无关，而是与车辆本身有关。",
        "grammar": {
            "type": "not ... but ... 结构",
            "note": "not to do with... but with... 为 “不是与……而是与……有关” 结构；to do with 意为 “与……有关”。"
        },
        "words": [
            {"w": "have to do with", "pos": "phr.", "def": "与……有关"},
            {"w": "process", "pos": "n.", "def": "过程；工序"}
        ]
    },
    {
        "id": 5,
        "para": 1,
        "en": "Research projects on vehicle automation are not new.",
        "zh": "有关车辆自动化的研究项目并不新鲜。",
        "grammar": {
            "type": "主系表",
            "note": "on vehicle automation 为介词短语作定语修饰 Research projects。"
        },
        "words": [
            {"w": "research project", "pos": "phr.", "def": "研究项目"}
        ]
    },
    {
        "id": 6,
        "para": 1,
        "en": "Vehicles with limited self-driving capabilities have been around for more than 50 years, resulting in significant contributions towards driver assistance systems.",
        "zh": "具备有限自动驾驶能力的车辆已存在了50多年，为驾驶辅助系统做出了重大贡献。",
        "grammar": {
            "type": "现在分词状语",
            "note": "resulting in... 为现在分词短语作结果状语；with limited self-driving capabilities 为介词短语作定语修饰 Vehicles；have been around 意为 “已存在”。"
        },
        "words": [
            {"w": "capability", "pos": "n.", "def": "能力；性能"},
            {"w": "be around", "pos": "phr.", "def": "存在；出现"},
            {"w": "contribution", "pos": "n.", "def": "贡献"},
            {"w": "driver assistance", "pos": "phr.", "def": "驾驶辅助"}
        ]
    },
    {
        "id": 7,
        "para": 1,
        "en": "But since Google announced in 2010 that it had been trialling self-driving cars on the streets of California, progress in this field has quickly gathered pace.",
        "zh": "但自从谷歌于2010年宣布已在加利福尼亚州的街道上试验自动驾驶汽车以来，该领域的进展便迅速加快了步伐。",
        "grammar": {
            "type": "since 时间状语从句 + 宾语从句",
            "note": "since 引导时间状语从句，从句内 that it had been trialling... 为宾语从句（过去完成进行时）；主句用现在完成时 has quickly gathered pace 与 since 呼应；gather pace 意为 “加快、加速”。"
        },
        "words": [
            {"w": "announce", "pos": "v.", "def": "宣布"},
            {"w": "trial", "pos": "v.", "def": "试验；试用"},
            {"w": "gather pace", "pos": "phr.", "def": "加快步伐；加速"}
        ]
    },
    # Para B (2)
    {
        "id": 8,
        "para": 2,
        "en": "There are many reasons why technology is advancing so fast.",
        "zh": "技术之所以进步如此之快，有很多原因。",
        "grammar": {
            "type": "定语从句",
            "note": "why technology is advancing so fast 为定语从句修饰 reasons（关系副词 why = for which）。"
        },
        "words": [
            {"w": "advance", "pos": "v.", "def": "进步；发展"}
        ]
    },
    {
        "id": 9,
        "para": 2,
        "en": "One frequently cited motive is safety; indeed, research at the UK" + RSQUO + "s Transport Research Laboratory has demonstrated that more than 90 percent of road collisions involve human error as a contributory factor, and it is the primary cause in the vast majority.",
        "zh": "一个经常被提及的动因是安全；事实上，英国交通研究实验室的研究已表明，90%以上的道路碰撞都有人为失误作为促成因素，且在绝大多数情况下人为失误是主因。",
        "grammar": {
            "type": "分号并列 + 宾语从句",
            "note": "分号连接两分句；has demonstrated that... 后接宾语从句（含 and 连接的两个并列成分）；frequently cited 为副词+过去分词作定语修饰 motive；as a contributory factor 意为 “作为一个促成因素”。"
        },
        "words": [
            {"w": "cited", "pos": "adj.", "def": "被引用的；被提及的"},
            {"w": "motive", "pos": "n.", "def": "动机；原因"},
            {"w": "collision", "pos": "n.", "def": "碰撞；相撞"},
            {"w": "contributory", "pos": "adj.", "def": "促成的；起作用的"},
            {"w": "vast majority", "pos": "phr.", "def": "绝大多数"}
        ]
    },
    {
        "id": 10,
        "para": 2,
        "en": "Automation may help to reduce the incidence of this.",
        "zh": "自动化或许有助于减少此类情况的发生。",
        "grammar": {
            "type": "简单句",
            "note": "help to do 意为 “有助于做”；this 指代前句的 human error（人为失误）；incidence 意为 “发生率”。"
        },
        "words": [
            {"w": "reduce", "pos": "v.", "def": "减少；降低"},
            {"w": "incidence", "pos": "n.", "def": "发生率；发生"}
        ]
    },
    {
        "id": 11,
        "para": 2,
        "en": "Another aim is to free the time people spend driving for other purposes.",
        "zh": "另一个目标是把人们花在开车上的时间解放出来，用于其他用途。",
        "grammar": {
            "type": "主系表 + 省略定语从句",
            "note": "to free the time... 为不定式作表语；(that) people spend driving 为省略关系词的定语从句修饰 time；free... for 意为 “腾出……用于”。"
        },
        "words": [
            {"w": "aim", "pos": "n.", "def": "目标；目的"},
            {"w": "free", "pos": "v.", "def": "解放；腾出"},
            {"w": "purpose", "pos": "n.", "def": "目的；用途"}
        ]
    },
    {
        "id": 12,
        "para": 2,
        "en": "If the vehicle can do some or all of the driving, it may be possible to be productive, to socialise or simply to relax while automation systems have responsibility for safe control of the vehicle.",
        "zh": "如果车辆能承担部分或全部驾驶任务，那么在自动化系统负责安全操控车辆的同时，人们或许就能从事有意义的工作、社交，或者单纯地放松。",
        "grammar": {
            "type": "条件句 + 并列不定式 + while 从句",
            "note": "If 引导条件句；主句 it may be possible to be productive, to socialise or... to relax 含并列不定式；while automation systems have responsibility... 为时间/伴随状语从句。"
        },
        "words": [
            {"w": "productive", "pos": "adj.", "def": "多产的；富有成效的"},
            {"w": "socialise", "pos": "v.", "def": "社交；交际"},
            {"w": "responsibility", "pos": "n.", "def": "责任"}
        ]
    },
    {
        "id": 13,
        "para": 2,
        "en": "If the vehicle can do the driving, those who are challenged by existing mobility models " + DASH + " such as older or disabled travellers " + DASH + " may be able to enjoy significantly greater travel autonomy.",
        "zh": "如果车辆能自行驾驶，那么受现有出行方式所限的人群——例如年长或残障的出行者——或许就能享有大得多的出行自主权。",
        "grammar": {
            "type": "条件句 + 定语从句 + 破折号插入",
            "note": "If 引导条件句；who are challenged by existing mobility models 为定语从句修饰 those；两破折号间 such as... 为举例插入语；be challenged by 意为 “受……困扰/限制”。"
        },
        "words": [
            {"w": "challenged", "pos": "adj.", "def": "有障碍的；受限制的"},
            {"w": "mobility", "pos": "n.", "def": "移动性；出行"},
            {"w": "disabled", "pos": "adj.", "def": "残障的"},
            {"w": "autonomy", "pos": "n.", "def": "自主；自治"}
        ]
    },
    # Para C (3)
    {
        "id": 14,
        "para": 3,
        "en": "Beyond these direct benefits, we can consider the wider implications for transport and society, and how manufacturing processes might need to respond as a result.",
        "zh": "除了这些直接的好处，我们还可以思考对交通和社会更广泛的影响，以及制造业可能因此需要如何应对。",
        "grammar": {
            "type": "并列宾语",
            "note": "consider 后接两个并列宾语 the wider implications... 与 how manufacturing processes might need to respond...；Beyond these direct benefits 为介词短语作状语；as a result 意为 “因此”。"
        },
        "words": [
            {"w": "implication", "pos": "n.", "def": "影响；后果；含意"},
            {"w": "respond", "pos": "v.", "def": "回应；作出反应"},
            {"w": "as a result", "pos": "phr.", "def": "结果；因此"}
        ]
    },
    {
        "id": 15,
        "para": 3,
        "en": "At present, the average car spends more than 90 percent of its life parked.",
        "zh": "目前，普通汽车其寿命的90%以上都处于停放状态。",
        "grammar": {
            "type": "简单句 + 过去分词作补语",
            "note": "spend time (doing/in a state) 结构，parked 为过去分词作宾补，表车处于 “被停放” 的状态；At present 意为 “目前”。"
        },
        "words": [
            {"w": "at present", "pos": "phr.", "def": "目前；现在"},
            {"w": "average", "pos": "adj.", "def": "平均的；普通的"},
            {"w": "parked", "pos": "adj.", "def": "停放着的"}
        ]
    },
    {
        "id": 16,
        "para": 3,
        "en": "Automation means that initiatives for car-sharing become much more viable, particularly in urban areas with significant travel demand.",
        "zh": "自动化意味着拼车方案变得可行得多，尤其是在出行需求大的城市地区。",
        "grammar": {
            "type": "宾语从句",
            "note": "means that... 后接宾语从句；particularly in urban areas... 为补充状语；with significant travel demand 为介词短语作定语修饰 urban areas；viable 意为 “可行的”。"
        },
        "words": [
            {"w": "initiative", "pos": "n.", "def": "倡议；新方案"},
            {"w": "car-sharing", "pos": "n.", "def": "拼车；汽车共享"},
            {"w": "viable", "pos": "adj.", "def": "可行的"},
            {"w": "urban", "pos": "adj.", "def": "城市的"}
        ]
    },
    {
        "id": 17,
        "para": 3,
        "en": "If a significant proportion of the population choose to use shared automated vehicles, mobility demand can be met by far fewer vehicles.",
        "zh": "如果相当大比例的人口选择使用共享的自动驾驶车辆，那么用少得多的车辆就能满足出行需求。",
        "grammar": {
            "type": "条件句 + 被动",
            "note": "If 引导条件句；主句 mobility demand can be met by... 为被动；far fewer 中 far 修饰比较级 fewer，意为 “少得多的”。"
        },
        "words": [
            {"w": "proportion", "pos": "n.", "def": "比例；部分"},
            {"w": "population", "pos": "n.", "def": "人口"},
            {"w": "meet demand", "pos": "phr.", "def": "满足需求"}
        ]
    },
    # Para D (4)
    {
        "id": 18,
        "para": 4,
        "en": "The Massachusetts Institute of Technology investigated automated mobility in Singapore, finding that fewer than 30 percent of the vehicles currently used would be required if fully automated car sharing could be implemented.",
        "zh": "麻省理工学院对新加坡的自动化出行进行了研究，发现如果能够实施全自动的汽车共享，那么所需的车辆将不到目前使用量的30%。",
        "grammar": {
            "type": "现在分词状语 + 宾语从句 + 虚拟条件",
            "note": "finding that... 为现在分词短语作结果状语；that 从句内含虚拟条件 if fully automated car sharing could be implemented，主句 fewer than 30 percent... would be required 用 would 表推测。"
        },
        "words": [
            {"w": "investigate", "pos": "v.", "def": "调查；研究"},
            {"w": "require", "pos": "v.", "def": "需要；要求"},
            {"w": "implement", "pos": "v.", "def": "实施；执行"}
        ]
    },
    {
        "id": 19,
        "para": 4,
        "en": "If this is the case, it might mean that we need to manufacture far fewer vehicles to meet demand.",
        "zh": "如果情况果真如此，那可能意味着我们只需制造少得多的车辆便能满足需求。",
        "grammar": {
            "type": "条件句 + 宾语从句",
            "note": "If this is the case 意为 “如果情况如此”；主句 it might mean that... 后接宾语从句；to meet demand 为目的状语。"
        },
        "words": [
            {"w": "be the case", "pos": "phr.", "def": "情况属实；确是如此"},
            {"w": "manufacture", "pos": "v.", "def": "制造；生产"}
        ]
    },
    {
        "id": 20,
        "para": 4,
        "en": "However, the number of trips being taken would probably increase, partly because empty vehicles would have to be moved from one customer to the next.",
        "zh": "然而，出行次数很可能会增加，部分原因是空车必须从一位顾客处调往下一位顾客处。",
        "grammar": {
            "type": "原因状语从句 + 被动",
            "note": "being taken 为现在分词被动式作定语修饰 trips；partly because... 引导原因状语从句；would have to be moved 为含情态的被动。"
        },
        "words": [
            {"w": "trip", "pos": "n.", "def": "出行；行程"},
            {"w": "empty", "pos": "adj.", "def": "空的"},
            {"w": "customer", "pos": "n.", "def": "顾客"}
        ]
    },
    {
        "id": 21,
        "para": 4,
        "en": "Modelling work by the University of Michigan Transportation Research Institute suggests automated vehicles might reduce vehicle ownership by 43 percent, but that vehicles" + RSQUO + " average annual mileage would double as a result.",
        "zh": "密歇根大学交通研究所的建模研究表明，自动驾驶车辆可能使车辆保有量减少43%，但作为结果，车辆的年均行驶里程会翻一番。",
        "grammar": {
            "type": "并列宾语从句",
            "note": "suggests 后接两个并列宾语从句（第二个由 but that 引出）：(that) automated vehicles might reduce... 与 that vehicles' average annual mileage would double...；reduce... by 43 percent 意为 “减少43%”。"
        },
        "words": [
            {"w": "modelling", "pos": "n.", "def": "建模；模型构建"},
            {"w": "ownership", "pos": "n.", "def": "所有权；保有量"},
            {"w": "annual", "pos": "adj.", "def": "每年的；年度的"},
            {"w": "mileage", "pos": "n.", "def": "里程；行驶里程"},
            {"w": "double", "pos": "v.", "def": "翻倍；增加一倍"}
        ]
    },
    {
        "id": 22,
        "para": 4,
        "en": "As a consequence, each vehicle would be used more intensively, and might need replacing sooner.",
        "zh": "因此，每辆车的使用会更为频繁密集，可能也需要更早更换。",
        "grammar": {
            "type": "并列谓语",
            "note": "would be used 与 might need replacing 为并列谓语；need replacing 为 “need + 动名词” 表被动（=need to be replaced）；As a consequence 意为 “因此”。"
        },
        "words": [
            {"w": "as a consequence", "pos": "phr.", "def": "因此；结果"},
            {"w": "intensively", "pos": "adv.", "def": "密集地；集中地"},
            {"w": "replace", "pos": "v.", "def": "更换；替换"}
        ]
    },
    {
        "id": 23,
        "para": 4,
        "en": "This faster rate of turnover may mean that vehicle production will not necessarily decrease.",
        "zh": "这种更快的更新速度可能意味着车辆产量未必会下降。",
        "grammar": {
            "type": "宾语从句",
            "note": "may mean that... 后接宾语从句；not necessarily 意为 “未必、不一定”；rate of turnover 意为 “更新/周转速度”。"
        },
        "words": [
            {"w": "turnover", "pos": "n.", "def": "（更新、周转的）速率；更替"},
            {"w": "not necessarily", "pos": "phr.", "def": "未必；不一定"},
            {"w": "decrease", "pos": "v.", "def": "减少；下降"}
        ]
    },
    # Para E (5)
    {
        "id": 24,
        "para": 5,
        "en": "Automation may prompt other changes in vehicle manufacture.",
        "zh": "自动化可能会促使车辆制造发生其他变化。",
        "grammar": {
            "type": "简单句",
            "note": "prompt 此处作及物动词 “促使、引起”；in vehicle manufacture 为介词短语作定语。"
        },
        "words": [
            {"w": "prompt", "pos": "v.", "def": "促使；引起"},
            {"w": "manufacture", "pos": "n.", "def": "制造；生产"}
        ]
    },
    {
        "id": 25,
        "para": 5,
        "en": "If we move to a model where consumers are tending not to own a single vehicle but to purchase access to a range of vehicles through a mobility provider, drivers will have the freedom to select one that best suits their needs for a particular journey, rather than making a compromise across all their requirements.",
        "zh": "如果我们转向这样一种模式——消费者倾向于不再拥有单独一辆车，而是通过出行服务提供商购买使用多种车辆的权限——那么驾驶者就能自由地选择最适合某一次出行需求的车辆，而不必在自己的所有需求之间做出折中。",
        "grammar": {
            "type": "条件句 + 定语从句 + not ... but ...",
            "note": "If 引导条件句，其中 where consumers are tending... 为定语从句修饰 model，从句内 not to own... but to purchase... 为并列不定式；主句含定语从句 that best suits...；rather than making a compromise 为对比状语。"
        },
        "words": [
            {"w": "consumer", "pos": "n.", "def": "消费者"},
            {"w": "purchase", "pos": "v.", "def": "购买"},
            {"w": "provider", "pos": "n.", "def": "提供者；供应商"},
            {"w": "compromise", "pos": "n.", "def": "折中；妥协"},
            {"w": "requirement", "pos": "n.", "def": "需求；要求"}
        ]
    },
    {
        "id": 26,
        "para": 5,
        "en": "Since, for most of the time, most of the seats in most cars are unoccupied, this may boost production of a smaller, more efficient range of vehicles that suit the needs of individuals.",
        "zh": "由于在大多数时间里，大多数汽车的大多数座位都空着，这可能会推动生产一系列更小、更高效、适合个人需求的车辆。",
        "grammar": {
            "type": "原因状语从句 + 定语从句",
            "note": "Since 引导原因状语从句；for most of the time 为插入状语；主句 this may boost production of...；that suit the needs of individuals 为定语从句修饰 vehicles。"
        },
        "words": [
            {"w": "unoccupied", "pos": "adj.", "def": "空着的；无人使用的"},
            {"w": "boost", "pos": "v.", "def": "促进；推动"},
            {"w": "efficient", "pos": "adj.", "def": "高效的"},
            {"w": "individual", "pos": "n.", "def": "个人；个体"}
        ]
    },
    {
        "id": 27,
        "para": 5,
        "en": "Specialised vehicles may then be available for exceptional journeys, such as going on a family camping trip or helping a son or daughter move to university.",
        "zh": "届时，专门的车辆可用于特殊的出行，例如全家去露营，或帮子女搬去上大学。",
        "grammar": {
            "type": "简单句 + 举例",
            "note": "such as going on... or helping... 以并列动名词短语举例说明 exceptional journeys；be available for 意为 “可供……使用”。"
        },
        "words": [
            {"w": "specialised", "pos": "adj.", "def": "专门的；专业化的"},
            {"w": "exceptional", "pos": "adj.", "def": "特殊的；例外的"},
            {"w": "camping trip", "pos": "phr.", "def": "露营出游"}
        ]
    },
    # Para F (6)
    {
        "id": 28,
        "para": 6,
        "en": "There are a number of hurdles to overcome in delivering automated vehicles to our roads.",
        "zh": "要把自动驾驶车辆推上道路，还有一些障碍需要克服。",
        "grammar": {
            "type": "there be + 不定式定语",
            "note": "to overcome 为不定式作定语修饰 hurdles；in delivering... 为介词短语作状语；deliver... to our roads 意为 “将……投放到道路上”。"
        },
        "words": [
            {"w": "hurdle", "pos": "n.", "def": "障碍；难关"},
            {"w": "overcome", "pos": "v.", "def": "克服；战胜"},
            {"w": "deliver", "pos": "v.", "def": "交付；投放；实现"}
        ]
    },
    {
        "id": 29,
        "para": 6,
        "en": "These include the technical difficulties in ensuring that the vehicle works reliably in the infinite range of traffic, weather and road situations it might encounter; the regulatory challenges in understanding how liability and enforcement might change when drivers are no longer essential for vehicle operation; and the societal changes that may be required for communities to trust and accept automated vehicles as being a valuable part of the mobility landscape.",
        "zh": "这些障碍包括：确保车辆在其可能遇到的无穷多种交通、天气和道路情况下都能可靠运行的技术难题；在驾驶者不再是车辆运行必需时，厘清责任认定与法规执行会如何变化的监管难题；以及要让社会大众信任并接受自动驾驶车辆、视其为出行格局中有价值的一部分所需的社会性变革。",
        "grammar": {
            "type": "分号并列三大宾语 + 多重从句",
            "note": "include 后接三组由分号并列的宾语：the technical difficulties... / the regulatory challenges... / the societal changes...；各含定语从句或 in doing 结构；(that) it might encounter 为省略关系词的定语从句修饰 situations。"
        },
        "words": [
            {"w": "infinite", "pos": "adj.", "def": "无限的；无穷的"},
            {"w": "regulatory", "pos": "adj.", "def": "监管的；管理的"},
            {"w": "liability", "pos": "n.", "def": "责任；法律责任"},
            {"w": "enforcement", "pos": "n.", "def": "（法规的）执行；实施"},
            {"w": "societal", "pos": "adj.", "def": "社会的"}
        ]
    },
    # Para G (7)
    {
        "id": 30,
        "para": 7,
        "en": "It" + RSQUO + "s clear that there are many challenges that need to be addressed but, through robust and targeted research, these can most probably be conquered within the next 10 years.",
        "zh": "显然，有许多挑战需要解决，但通过强有力且有针对性的研究，这些挑战很可能会在未来10年内被攻克。",
        "grammar": {
            "type": "形式主语 + 转折 + 被动",
            "note": "It's clear that... 为形式主语结构；that need to be addressed 为定语从句修饰 challenges；but 后 these can... be conquered 为被动，through... research 为方式状语。"
        },
        "words": [
            {"w": "address", "pos": "v.", "def": "处理；解决"},
            {"w": "robust", "pos": "adj.", "def": "强健的；强有力的"},
            {"w": "targeted", "pos": "adj.", "def": "有针对性的"},
            {"w": "conquer", "pos": "v.", "def": "克服；攻克；征服"}
        ]
    },
    {
        "id": 31,
        "para": 7,
        "en": "Mobility will change in such potentially significant ways and in association with so many other technological developments, such as telepresence and virtual reality, that it is hard to make concrete predictions about the future.",
        "zh": "出行将以可能极其重大的方式发生变化，并与远程呈现、虚拟现实等诸多其他技术发展相互交织，以至于很难对未来做出确切的预测。",
        "grammar": {
            "type": "such ... that ... 结果状语",
            "note": "such... ways and... developments... that it is hard to... 为 such...that... 结果状语结构；in association with 意为 “与……相关联”；such as... 举例。"
        },
        "words": [
            {"w": "in association with", "pos": "phr.", "def": "与……相关联；连同"},
            {"w": "telepresence", "pos": "n.", "def": "远程呈现（技术）"},
            {"w": "virtual reality", "pos": "phr.", "def": "虚拟现实"},
            {"w": "concrete", "pos": "adj.", "def": "具体的；确切的"}
        ]
    },
    {
        "id": 32,
        "para": 7,
        "en": "However, one thing is certain: change is coming, and the need to be flexible in response to this will be vital for those involved in manufacturing the vehicles that will deliver future mobility.",
        "zh": "然而，有一点是确定的：变革即将到来，而对于那些参与制造未来出行车辆的人来说，能够灵活应对这一变化将至关重要。",
        "grammar": {
            "type": "冒号说明 + 并列句 + 定语从句",
            "note": "冒号后为对 one thing 的说明；change is coming 与 the need... will be vital 为并列分句；those involved in... 中 involved 为过去分词定语；that will deliver future mobility 为定语从句修饰 vehicles。"
        },
        "words": [
            {"w": "certain", "pos": "adj.", "def": "确定的；肯定的"},
            {"w": "flexible", "pos": "adj.", "def": "灵活的；有弹性的"},
            {"w": "in response to", "pos": "phr.", "def": "回应；对……作出反应"},
            {"w": "vital", "pos": "adj.", "def": "至关重要的"}
        ]
    }
]

phrases = [
    {"w": "be used to", "pos": "phr.", "def": "习惯于"},
    {"w": "on the horizon", "pos": "phr.", "def": "即将出现；在望"},
    {"w": "have to do with", "pos": "phr.", "def": "与……有关"},
    {"w": "gather pace", "pos": "phr.", "def": "加快步伐；加速"},
    {"w": "as a result", "pos": "phr.", "def": "结果；因此"},
    {"w": "meet demand", "pos": "phr.", "def": "满足需求"},
    {"w": "be the case", "pos": "phr.", "def": "情况属实；确是如此"},
    {"w": "as a consequence", "pos": "phr.", "def": "因此；结果"},
    {"w": "in association with", "pos": "phr.", "def": "与……相关联；连同"},
    {"w": "in response to", "pos": "phr.", "def": "回应；对……作出反应"}
]

questions = [
    {
        "title": "Questions 14" + DASH + "18",
        "type": "matching_information",
        "instructions": [
            "Reading Passage 2 has seven sections, A" + DASH + "G.",
            "Which section contains the following information?",
            "Write the correct letter, A" + DASH + "G, in boxes 14" + DASH + "18 on your answer sheet."
        ],
        "items": [
            {"number": 14, "prompt": "reference to the amount of time when a car is not in use", "answer": "C", "evidence_sentence": 15},
            {"number": 15, "prompt": "mention of several advantages of driverless vehicles for individual road-users", "answer": "B", "evidence_sentence": 12},
            {"number": 16, "prompt": "reference to the opportunity of choosing the most appropriate vehicle for each trip", "answer": "E", "evidence_sentence": 25},
            {"number": 17, "prompt": "an estimate of how long it will take to overcome a number of problems", "answer": "G", "evidence_sentence": 30},
            {"number": 18, "prompt": "a suggestion that the use of driverless cars may have no effect on the number of vehicles manufactured", "answer": "D", "evidence_sentence": 23}
        ]
    },
    {
        "title": "Questions 19" + DASH + "22",
        "type": "summary_completion",
        "instructions": [
            "Complete the summary below.",
            "Choose NO MORE THAN TWO WORDS from the passage for each answer.",
            "Write your answers in boxes 19" + DASH + "22 on your answer sheet.",
            "The impact of driverless cars"
        ],
        "items": [
            {"number": 19, "prompt": "Figures from the Transport Research Laboratory indicate that most motor accidents are partly due to __________, so the introduction of driverless vehicles will result in greater safety.", "answer": "human error", "evidence_sentence": 9},
            {"number": 20, "prompt": "For example, schemes for __________ will be more workable, especially in towns and cities, resulting in fewer cars on the road.", "answer": "car(-)sharing", "evidence_sentence": 16},
            {"number": 21, "prompt": "According to the University of Michigan Transportation Research Institute, there could be a 43 percent drop in __________ of cars.", "answer": "ownership", "evidence_sentence": 21},
            {"number": 22, "prompt": "However, this would mean that the yearly __________ of each car would, on average, be twice as high as it currently is.", "answer": "mileage", "evidence_sentence": 21}
        ]
    },
    {
        "title": "Questions 23 and 24",
        "type": "multiple_choice_two",
        "instructions": [
            "Choose TWO letters, A" + DASH + "E.",
            "Write the correct letters in boxes 23 and 24 on your answer sheet.",
            "Which TWO benefits of automated vehicles does the writer mention?"
        ],
        "items": [
            {"number": 23, "prompt": "A  Car travellers could enjoy considerable cost savings.\nB  It would be easier to find parking spaces in urban areas.\nC  Travellers could spend journeys doing something other than driving.\nD  People who find driving physically difficult could travel independently.\nE  A reduction in the number of cars would mean a reduction in pollution.", "answer": "C, D", "evidence_sentence": 12},
            {"number": 24, "prompt": "(See Question 23 " + DASH + " choose the second of the TWO correct letters.)", "answer": "C, D", "evidence_sentence": 13}
        ]
    },
    {
        "title": "Questions 25 and 26",
        "type": "multiple_choice_two",
        "instructions": [
            "Choose TWO letters, A" + DASH + "E.",
            "Write the correct letters in boxes 25 and 26 on your answer sheet.",
            "Which TWO challenges to automated vehicle development does the writer mention?"
        ],
        "items": [
            {"number": 25, "prompt": "A  making sure the general public has confidence in automated vehicles\nB  managing the pace of transition from conventional to automated vehicles\nC  deciding how to compensate professional drivers who become redundant\nD  setting up the infrastructure to make roads suitable for automated vehicles\nE  getting automated vehicles to adapt to various different driving conditions", "answer": "A, E", "evidence_sentence": 29},
            {"number": 26, "prompt": "(See Question 25 " + DASH + " choose the second of the TWO correct letters.)", "answer": "A, E", "evidence_sentence": 29}
        ]
    }
]

data = {
    "id": "c15-test1-p2",
    "source": "剑桥雅思15 Test 1 Passage 2",
    "title": "Driverless cars",
    "quality": "teacher_refined",
    "analysis_unit": "sentence",
    "phrases": phrases,
    "sentences": sentences,
    "questions": questions
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "passages", "c15-test1-p2.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Wrote", out_path)
print("sentences:", len(sentences), "question groups:", len(questions), "phrases:", len(phrases))
