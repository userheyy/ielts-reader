"""Teacher-refine Cambridge IELTS 17 Test 1 Passage 1.

The draft generator creates usable question-bank JSON. This refinement layer is
hand-curated: Chinese translation, grammar focus, sentence notes, and fixed
phrases are written from an IELTS teaching perspective rather than blindly
imported from OCR.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test1-p1.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


PHRASES = [
    w("at an astonishing rate", "phr.", "以惊人的速度"),
    w("overground railway network", "n.", "地上铁路网络"),
    w("the City", "n.", "伦敦金融城；伦敦老城商业中心"),
    w("horse-drawn traffic", "n.", "马车交通"),
    w("Charles Pearson", "n.", "查尔斯·皮尔逊"),
    w("Metropolitan Railway Company", "n.", "大都会铁路公司"),
    w("cut and cover", "n.", "明挖回填法"),
    w("ventilation shaft", "n.", "通风井"),
    w("deep-level electric railway", "n.", "深层电气铁路"),
    w("the Tuppenny Tube", "n.", "两便士地铁；中央伦敦铁路绰号"),
]


REFINED = {
    1: (
        "19世纪上半叶，伦敦人口以惊人的速度增长，中心城区也变得越来越拥堵。",
        "并列句 + 比较级递进",
        "主干是 population grew 与 area became congested；at an astonishing rate 作方式状语；increasingly 强调拥堵程度逐步加深。",
        [w("astonishing", "adj.", "惊人的"), w("congested", "adj.", "拥堵的")],
    ),
    2: (
        "此外，地上铁路网络的扩张导致越来越多的乘客抵达首都。",
        "名词化主语 + result in",
        "the expansion 是名词化主语；resulted in 表“导致”；arriving in the capital 为现在分词短语，修饰 passengers。",
        [w("expansion", "n.", "扩张"), w("result in", "phr.", "导致")],
    ),
    3: (
        "然而，1846年，一个皇家委员会决定不应允许铁路进入伦敦城——这个首都的历史与商业中心。",
        "宾语从句 + 同位语",
        "decided 后接 that 宾语从句；should not be allowed 是被动；逗号后的名词短语解释 the City。",
        [w("Royal Commission", "n.", "皇家委员会"), w("historic", "adj.", "历史悠久的")],
    ),
    4: (
        "结果是，地上铁路车站在伦敦城周围形成了一个环。",
        "表语从句",
        "The result was that... 用来引出前文决定造成的结果；formed a ring around 表空间布局。",
        [w("form", "v.", "形成"), w("ring", "n.", "环；圈")],
    ),
    5: (
        "环内区域由建筑质量很差且拥挤不堪的贫民窟组成，街道上满是马车交通。",
        "并列句 + consisted of",
        "consisted of 表“由……组成”；poorly built 与 overcrowded 并列修饰 slums；and 连接另一分句。",
        [w("slum", "n.", "贫民窟"), w("overcrowded", "adj.", "过度拥挤的")],
    ),
    6: (
        "穿过伦敦城成了一场噩梦。",
        "动名词主语",
        "Crossing the City 是动名词短语作主语；became a nightmare 概括交通困难。",
        [w("nightmare", "n.", "噩梦；极糟的经历")],
    ),
    7: (
        "乘马车或公共马车走 8 公里可能要花一个半小时。",
        "It takes time to do",
        "It could take...to travel... 是花费时间句型；by horse-drawn carriage or bus 表交通方式。",
        [w("carriage", "n.", "马车"), w("horse-drawn", "adj.", "马拉的")],
    ),
    8: (
        "人们提出了许多方案来解决这些问题，但很少有方案成功。",
        "被动语态 + 转折",
        "schemes were proposed 是被动；to resolve... 表目的；but few succeeded 形成转折。",
        [w("scheme", "n.", "方案；计划"), w("resolve", "v.", "解决")],
    ),
    9: (
        "在为解决伦敦交通问题而大声疾呼的人中，查尔斯·皮尔逊是最积极的一位；他是伦敦城的一名律师。",
        "倒装结构 + 非限制性定语从句",
        "Amongst...was Charles Pearson 为地点/范围状语提前引起的倒装；who worked... 补充人物身份。",
        [w("advocate", "n.", "倡导者"), w("solicitor", "n.", "事务律师")],
    ),
    10: (
        "他看到，修建一条把地上铁路车站连接起来、同时清理伦敦贫民窟的地下铁路，既有社会利益，也有经济利益。",
        "see advantages in doing + 定语从句",
        "in building... 作介词宾语；that would link...and clear... 修饰 railway，说明铁路功能。",
        [w("link", "v.", "连接"), w("clear", "v.", "清除；清理")],
    ),
    11: (
        "他的想法是把住在内城贫民窟的贫困工人迁到新建郊区，并为他们提供廉价铁路交通去上班。",
        "不定式作表语 + 定语从句",
        "was to relocate...and to provide... 是并列不定式表方案内容；who lived... 修饰 workers。",
        [w("relocate", "v.", "迁移；重新安置"), w("suburb", "n.", "郊区")],
    ),
    12: (
        "皮尔逊的想法得到了一些商人的支持，并且在1851年他向议会提交了一份计划。",
        "并列谓语",
        "gained support 与 submitted a plan 并列；amongst some businessmen 对应题目中的 A number of businessmen。",
        [w("gain support", "phr.", "获得支持"), w("Parliament", "n.", "议会")],
    ),
    13: (
        "该计划被否决了，但它恰好与另一个团体提出的地下连接线方案同时出现，而这个方案获得了议会通过。",
        "被动语态 + which 定语从句",
        "It was rejected 是被动；coincided with 表“与……同时发生”；which Parliament passed 修饰 proposal。",
        [w("reject", "v.", "拒绝；否决"), w("coincide with", "phr.", "与……同时发生")],
    ),
    14: (
        "这两个团体合并，并于1854年8月成立了大都会铁路公司。",
        "并列谓语",
        "merged 与 established 并列，交代组织形成。",
        [w("merge", "v.", "合并"), w("establish", "v.", "建立")],
    ),
    15: (
        "公司的计划是修建一条地下铁路线，从帕丁顿的大西部铁路车站通往伦敦城边缘的法灵顿街，全程将近5公里。",
        "不定式作表语 + 插入解释",
        "was to construct... 表计划内容；from...to... 说明路线；破折号后补充距离。",
        [w("construct", "v.", "修建"), w("edge", "n.", "边缘")],
    ),
    16: (
        "该组织很难为这样一个激进而昂贵的方案筹集资金，尤其是因为报刊刊登了批评文章。",
        "have difficulty in doing + 原因状语",
        "had difficulty in raising... 是固定结构；not least because... 强调重要原因，对应 funding 与 press 两题。",
        [w("funding", "n.", "资金"), w("radical", "adj.", "激进的；彻底的")],
    ),
    17: (
        "反对者声称，隧道会在上方交通重量下坍塌，建筑会被震动，乘客会被火车发动机排放的废气毒害。",
        "宾语从句 + 并列被动",
        "argued 后接三个并列 that 内容；collapse / be shaken / be poisoned 构成反对理由。",
        [w("objector", "n.", "反对者"), w("emission", "n.", "排放物")],
    ),
    18: (
        "然而，皮尔逊和他的伙伴们坚持了下来。",
        "转折句",
        "However 承接反对声音后转折；persisted 强调持续推进。",
        [w("persist", "v.", "坚持")],
    ),
    19: (
        "大西部铁路公司意识到新线路最终会让他们把火车开进伦敦城中心，于是向该方案投资了近25万英镑。",
        "分词插入语 + 宾语从句",
        "aware that... 是形容词短语作插入状语；invested...in... 表投资。",
        [w("enable", "v.", "使能够"), w("invest", "v.", "投资")],
    ),
    20: (
        "最终，在五年时间里筹集到了100万英镑。",
        "被动语态",
        "was raised 是被动，强调资金被筹集完成；over a five-year period 表时间跨度。",
        [w("raise", "v.", "筹集")],
    ),
    21: (
        "所选路线位于现有主干道下方，以尽量减少拆除建筑物的费用。",
        "目的状语",
        "ran beneath... 表路线位置；to minimise... 是目的状语。",
        [w("beneath", "prep.", "在……下方"), w("demolish", "v.", "拆除")],
    ),
    22: (
        "地下线路原定21个月完工，但施工实际用了三年。",
        "过去分词状语 + 对比",
        "Originally scheduled... 为过去分词短语，表示原计划；took three years 与 21 months 对比。",
        [w("schedule", "v.", "安排；预定"), w("construction", "n.", "施工")],
    ),
    23: (
        "它建在刚低于街面的地方，采用一种被称为“明挖回填法”的技术。",
        "被动语态 + 过去分词定语",
        "was built 是被动；known as ‘cut and cover’ 修饰 technique。",
        [w("street level", "n.", "街面高度"), w("technique", "n.", "技术")],
    ),
    24: (
        "人们挖出一条约十米宽、六米深的沟渠，并用木梁临时支撑两侧。",
        "被动语态并列",
        "was dug 与 were held up 并列被动；about...wide/deep 描述尺寸。",
        [w("trench", "n.", "沟渠"), w("timber beam", "n.", "木梁")],
    ),
    25: (
        "随后建起砖墙，最后再加上砖拱，形成隧道。",
        "被动语态 + 目的状语",
        "were constructed 与 was added 并列；to create a tunnel 表结果/目的。",
        [w("brick arch", "n.", "砖拱"), w("construct", "v.", "建造")],
    ),
    26: (
        "隧道顶部铺上一层两米厚的土，随后上方道路被重建。",
        "被动语态",
        "was laid 与 rebuilt 省略并列助动词，说明明挖回填的最后步骤；soil 对应第6题。",
        [w("layer", "n.", "一层"), w("rebuild", "v.", "重建")],
    ),
    27: (
        "1863年1月10日开通的大都会线，是世界上第一条地下铁路。",
        "非限制性定语从句",
        "which opened... 补充开通时间；the world’s first underground railway 是关键信息，判断第7题 FALSE。",
        [w("Metropolitan line", "n.", "大都会线")],
    ),
    28: (
        "开通第一天，帕丁顿和法灵顿之间运送了近4万名乘客，全程约18分钟。",
        "独立主格结构",
        "passengers were carried 是被动；the journey taking... 为独立主格补充行程耗时。",
        [w("carry", "v.", "运送"), w("journey", "n.", "行程")],
    ),
    29: (
        "到大都会线运营第一年结束时，已经完成了950万次出行。",
        "过去完成时被动",
        "had been made 表示到过去某个时间点已经完成的出行次数。",
        [w("operation", "n.", "运营"), w("journey", "n.", "出行次数")],
    ),
    30: (
        "甚至在大都会线刚开始运营时，第一批延长线就已获批；这些延长线在接下来五年建成，东到伦敦的穆尔盖特，西到哈默史密斯。",
        "时间从句 + 分号并列",
        "Even as 引导时间背景；were being authorised 为过去进行时被动；reaching... 补充延伸方向。",
        [w("extension", "n.", "延长线"), w("authorise", "v.", "批准")],
    ),
    31: (
        "最初的计划是用蒸汽机车牵引列车，并在锅炉中使用耐火砖来产生蒸汽，但这些发动机从未投入使用。",
        "不定式作表语 + 转折",
        "was to pull... 表计划；using... 作方式；but 转折说明未采用。",
        [w("steam locomotive", "n.", "蒸汽机车"), w("boiler", "n.", "锅炉")],
    ),
    32: (
        "相反，该线路使用特别设计的机车，这些机车装有水箱，可使蒸汽冷凝。",
        "定语从句 + 被动语态",
        "that were fitted with... 修饰 locomotives；in which steam could be condensed 继续说明 water tanks 功能。",
        [w("fit with", "phr.", "装配有"), w("condense", "v.", "冷凝")],
    ),
    33: (
        "然而，尽管隧道增加了通风井，烟雾和废气仍然是个问题。",
        "让步状语从句",
        "even though 引导让步；remained a problem 对应第9题 TRUE。",
        [w("fume", "n.", "烟气；废气"), w("ventilation shaft", "n.", "通风井")],
    ),
    34: (
        "尽管地下铁路不断延伸，到19世纪80年代，伦敦街道的拥堵却变得更加严重。",
        "让步 + 时间状语",
        "Despite 后接名词短语；by the 1880s 表到某时为止；had become worse 表变化结果。",
        [w("despite", "prep.", "尽管"), w("congestion", "n.", "拥堵")],
    ),
    35: (
        "问题部分在于，现有地下线路围绕伦敦中心形成了一个环并延伸到郊区，却没有穿过首都中心。",
        "表语从句 + but 转折",
        "The problem was partly that... 解释问题原因；formed / extended / did not cross 形成对比。",
        [w("circuit", "n.", "环线"), w("extend", "v.", "延伸")],
    ),
    36: (
        "在首都的这一部分，“明挖回填”施工法并不可行。",
        "主系表",
        "was not an option 表“不是可选方案、不可行”，对应第10题需要 different approach。",
        [w("option", "n.", "选择；可行办法")],
    ),
    37: (
        "唯一的替代方案是在地下深处开凿隧道。",
        "主系表 + 不定式",
        "The only alternative was to... 表唯一解决路径；deep underground 强调深层隧道。",
        [w("alternative", "n.", "替代方案"), w("tunnel", "v.", "开凿隧道")],
    ),
    38: (
        "尽管建造这些隧道的技术已经存在，蒸汽机车却不能在如此狭小的空间内使用。",
        "Although 让步从句",
        "Although 引出已有条件；could not be used 是被动，说明限制。",
        [w("confined", "adj.", "狭窄受限的"), w("space", "n.", "空间")],
    ),
    39: (
        "直到可靠电动机以及把发电机动力传输到移动列车的方法发展出来，世界第一条深层电气铁路——城市与南伦敦铁路——才成为可能。",
        "It wasn’t until...that 强调句",
        "强调结构突出技术突破是前提；a means of transferring power 与 reliable electric motor 并列。",
        [w("reliable", "adj.", "可靠的"), w("generator", "n.", "发电机"), w("transfer", "v.", "传输")],
    ),
    40: (
        "该线路于1890年开通，从伦敦城通往泰晤士河南岸的斯托克韦尔。",
        "并列谓语",
        "opened 与 ran 并列；south of the River Thames 补充 Stockwell 的位置。",
        [w("south of", "phr.", "在……以南")],
    ),
    41: (
        "列车由三节车厢组成，并由电力发动机驱动。",
        "被动语态",
        "were made up of 表“由……组成”；driven by 表动力来源。",
        [w("be made up of", "phr.", "由……组成"), w("carriage", "n.", "车厢")],
    ),
    42: (
        "车厢很窄，窗户很小且位于靠近车顶的位置，因为当时认为乘客不会想看隧道墙壁。",
        "because 原因状语从句",
        "had tiny windows just below the roof 说明窗户位置，不是 eye level；because 解释设计原因。",
        [w("narrow", "adj.", "狭窄的"), w("roof", "n.", "顶部；车顶")],
    ),
    43: (
        "这条线路并非没有问题，问题主要由不可靠的供电造成。",
        "双重否定 + 过去分词短语",
        "was not without its problems 表“确实有问题”；mainly caused by... 说明问题来源。",
        [w("power supply", "n.", "供电"), w("unreliable", "adj.", "不可靠的")],
    ),
    44: (
        "虽然城市与南伦敦铁路是一项伟大的技术成就，但它没有盈利。",
        "Although 让步从句",
        "Although 引出让步；did not make a profit 对应第12题 FALSE。",
        [w("technical achievement", "n.", "技术成就"), w("make a profit", "phr.", "盈利")],
    ),
    45: (
        "随后，1900年，被称为“两便士地铁”的中央伦敦铁路开始运营，使用新的电力机车。",
        "过去分词插入 + 分词状语",
        "known as... 补充 Central London Railway 的绰号；using... 表运营方式。",
        [w("begin operation", "phr.", "开始运营"), w("locomotive", "n.", "机车")],
    ),
    46: (
        "它非常受欢迎，不久之后，新的铁路和延长线被加入不断扩大的地铁网络。",
        "并列句 + 被动语态",
        "was very popular 与 were added 并列；growing tube network 表逐步扩展的系统。",
        [w("extension", "n.", "延长线"), w("tube network", "n.", "地铁网络")],
    ),
    47: (
        "到1907年，今天伦敦地铁系统的核心已经形成。",
        "完成状态",
        "was in place 表“已经就位、形成”；heart 指系统核心。",
        [w("be in place", "phr.", "就位；形成"), w("Underground system", "n.", "伦敦地铁系统")],
    ),
}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    data["quality"] = "teacher_refined"
    data["phrases"] = PHRASES
    for s in data["sentences"]:
        zh, gtype, note, words = REFINED[s["id"]]
        s["zh"] = zh
        s["grammar"] = {"type": gtype, "note": note}
        s["words"] = words
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"refined {PATH}")


if __name__ == "__main__":
    main()
