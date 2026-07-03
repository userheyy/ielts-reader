"""Teacher-refine Cambridge IELTS 17 Test 1 Passage 2."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test1-p2.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


PHRASES = [
    w("urban architecture", "n.", "城市建筑"),
    w("fall into disuse and disrepair", "phr.", "荒废并失修"),
    w("drive urban development", "phr.", "推动城市发展"),
    w("mono-functional sports arena", "n.", "单一功能体育场馆"),
    w("public spectacles", "n.", "公共表演/观赏活动"),
    w("be absorbed into the fabric of the city", "phr.", "融入城市肌理"),
    w("mixed-use development", "n.", "混合用途开发"),
    w("urban hub", "n.", "城市枢纽"),
    w("smart grid", "n.", "智能电网"),
    w("photovoltaic panel", "n.", "光伏板"),
    w("carbon dioxide emissions", "n.", "二氧化碳排放"),
    w("sustainable future", "n.", "可持续未来"),
]


REFINED = {
    1: ("体育场是最古老的城市建筑形式之一：早在古希腊和古罗马帝国时期，大型体育场就是西方城市生活的中心，人们可以在那里观看体育赛事；这远早于中世纪大教堂以及后来主导城市天际线的19、20世纪宏伟火车站的建造。", "冒号解释 + 多层定语从句", "冒号后解释 stadiums 的历史地位；where 引导定语从句修饰 stadiums；well before 引出时间对比；which 修饰 railway stations。", [w("vast", "adj.", "巨大的"), w("skyline", "n.", "天际线")]),
    2: ("然而，如今人们对体育场抱有越来越多的怀疑。", "被动语态", "are regarded with... 表“被以某种态度看待”；however 标志古今态度转折。", [w("scepticism", "n.", "怀疑态度")]),
    3: ("建设成本可能飙升到10亿英镑以上，而为奥运会或世界杯等大型赛事完工的体育场，明显已经陷入闲置和失修。", "并列句 + 过去分词定语", "costs can soar 与 stadiums have fallen 并列；finished for... 修饰 stadiums。", [w("soar", "v.", "飙升"), w("disrepair", "n.", "失修")]),
    4: ("但情况并非必须如此。", "情态否定", "need not 表“不必”；this 指前文体育场荒废的局面。", [w("case", "n.", "情况")]),
    5: ("历史表明，体育场能够推动城市发展，并适应每个时代的文化。", "宾语从句 + 并列谓语", "shows 后接 that 从句；drive 与 adapt to 并列。", [w("adapt to", "phr.", "适应")]),
    6: ("即使在今天，建筑师和规划者也在寻找新方法，改造那些在20世纪现代化过程中具有象征意义的单一功能体育场馆。", "定语从句", "which became... 修饰 sports arenas；adapt 在本句指“改造以适应新用途”。", [w("emblematic", "adj.", "象征性的"), w("modernisation", "n.", "现代化")]),
    7: ("法国西南部阿尔勒圆形剧场可容纳2.5万名观众，也许是体育场多功能性的最佳例子。", "插入介词短语 + 宾语从句式感叹", "with a capacity... 补充容量；just how versatile... 作 of 的宾语内容。", [w("amphitheatre", "n.", "圆形剧场"), w("versatile", "adj.", "多功能的")]),
    8: ("它由罗马人建于公元90年，5世纪之后变成一座带有四座塔楼的堡垒，随后又被改造成一个包含200多栋房屋的村庄。", "过去分词状语 + 被动语态", "Built by... 作背景；became 与 was transformed 并列展现用途变化。", [w("fortress", "n.", "堡垒"), w("transform", "v.", "改造")]),
    9: ("19世纪，随着人们对保护古迹的兴趣不断增长，它又被改回斗牛表演场，从而使该建筑恢复了最初作为公共观赏活动场所的用途。", "with 复合背景 + 分词结果", "With... 表时代背景；thereby returning... 表结果。", [w("conservation", "n.", "保护"), w("bullfight", "n.", "斗牛")]),
    10: ("另一个例子是意大利北部维罗纳宏伟的竞技场，可容纳3万名观众；它比阿尔勒圆形剧场早建60年，比罗马著名的斗兽场早建40年。", "非限制性定语从句", "with space... 补充容量；which was built... 补充建造年代比较。", [w("imposing", "adj.", "宏伟的"), w("Colosseum", "n.", "罗马斗兽场")]),
    11: ("它经受住了几个世纪的考验，如今因杰出的声学效果而被认为是世界顶级歌剧场地之一。", "现在完成时 + 被动语态", "has endured 表延续至今；is considered... thanks to... 表评价原因。", [w("endure", "v.", "经受住"), w("acoustics", "n.", "声学效果")]),
    12: ("意大利卢卡市中心的区域，即 Piazza dell’Anfiteatro，是另一个令人印象深刻的例子，显示圆形剧场如何融入城市肌理。", "同位语 + 动名词结构", "known as... 作后置说明；becoming absorbed... 作 of 的宾语。", [w("fabric", "n.", "结构；肌理"), w("absorbed", "adj.", "被吸收的")]),
    13: ("这个地点以类似阿尔勒的方式演变，从中世纪到19世纪逐渐被建筑填满，曾分别用作住宅、盐仓和监狱。", "被动语态 + 分词补充", "was filled with... 为被动；variously used as... 补充不同用途。", [w("depot", "n.", "仓库"), w("progressively", "adv.", "逐渐地")]),
    14: ("但它没有恢复为竞技场，而是成为由浪漫主义建筑师 Lorenzo Nottolini 设计的市场广场。", "rather than 对比", "rather than reverting... 与 became... 对比；designed by... 修饰 market square。", [w("revert to", "phr.", "恢复为"), w("market square", "n.", "市场广场")]),
    15: ("今天，圆形剧场遗迹仍嵌在围绕公共广场的各种商店和住宅之中。", "remain + 过去分词", "remain embedded 表持续状态；surrounding... 修饰 shops and residences。", [w("embedded", "adj.", "嵌入的"), w("residence", "n.", "住宅")]),
    16: ("现代体育场与古代用于竞技的圆形剧场有许多相似之处。", "There be 句型", "There are... between A and B 表两者之间存在相似点。", [w("similarity", "n.", "相似点")]),
    17: ("但在20世纪初，随着体育场开始使用钢材和钢筋混凝土等新材料，并利用强光进行夜间比赛，一部分灵活性丧失了。", "被动语态 + as 原因/时间从句", "was lost 为被动；as 引导发展背景；made use of 表“利用”。", [w("reinforced concrete", "n.", "钢筋混凝土"), w("flexibility", "n.", "灵活性")]),
    18: ("许多这样的体育场位于郊区，只为体育用途而设计，并被停车场包围。", "过去分词并列", "situated / designed / surrounded 三个过去分词结构描述现代体育场特征。", [w("suburban", "adj.", "郊区的"), w("parking lot", "n.", "停车场")]),
    19: ("这些因素意味着它们可能不太方便普通公众到达，需要更多能源运行，并会加剧城市热效应。", "宾语从句 + 并列谓语", "mean 后接 that 从句；may not be / require / contribute 并列。", [w("accessible", "adj.", "可到达的"), w("urban heat", "n.", "城市热效应")]),
    20: ("但今天许多最具创新精神的建筑师看到了体育场帮助改善城市的空间。", "see scope for", "see scope for... 表“看到……的可能性”；to help improve... 修饰 stadium。", [w("scope", "n.", "余地；机会"), w("innovative", "adj.", "创新的")]),
    21: ("在当前策略中，两种似乎特别成功：把体育场作为城市枢纽，以及把体育场作为发电厂。", "冒号列举", "two seem to be... 为主干；冒号后列举两种策略。", [w("strategy", "n.", "策略"), w("power plant", "n.", "发电厂")]),
    22: ("越来越多的体育场配备了公共空间和服务，这些空间和服务承担体育之外的功能，例如酒店、零售店、会议中心、餐厅酒吧、儿童游乐场和绿地。", "There be + 定语从句", "There’s a growing trend for... 表趋势；that serve... 修饰 spaces and services；such as 列举。", [w("retail outlet", "n.", "零售店"), w("conference centre", "n.", "会议中心")]),
    23: ("创建这种混合用途开发能增强紧凑性和多功能性，更高效地利用土地，并帮助再生城市空间。", "动名词主语 + 分词结果", "Creating... 作主语；making 与 helping 为并列分词，说明结果。", [w("compactness", "n.", "紧凑性"), w("regenerate", "v.", "再生；复兴")]),
    24: ("这使空间向家庭和更广泛的社会群体开放，而不是只服务运动员和支持者。", "open up + instead of", "opens...up 表开放；instead of catering only to... 表取代关系。", [w("cross-section", "n.", "代表性群体"), w("cater to", "phr.", "迎合；服务")]),
    25: ("英国已有许多这样的例子：温布利和老特拉福德的混合用途设施，已经成为世界许多其他体育场的蓝图。", "There have been + 冒号解释", "There have been 表已有例子；冒号后具体说明；blueprint 表可复制范本。", [w("facility", "n.", "设施"), w("blueprint", "n.", "蓝图；范本")]),
    26: ("体育场作为发电站的现象，源自这样一种想法：通过智能电网整合相互连接的建筑，可以克服能源问题；智能电网是一种利用数字通信技术探测并响应本地用电变化、且不会造成显著能源损失的供电网络。", "同位语从句 + 非限制性定语从句", "that energy problems... 解释 idea；which is... 解释 smart grid；to detect and react... 表用途。", [w("integrate", "v.", "整合"), w("interconnected", "adj.", "相互连接的")]),
    27: ("体育场非常适合这些用途，因为其顶棚表面积大，适合安装光伏板，而且高度足够高，可以利用微型风力涡轮机。", "because 原因状语从句", "because 解释 ideal；for fitting... 与 to make use of... 分别说明表面积和高度优势。", [w("canopy", "n.", "顶棚"), w("micro wind turbine", "n.", "微型风力涡轮机")]),
    28: ("德国弗赖堡太阳能体育场是新一代“体育场发电厂”的第一个，其中还包括阿姆斯特丹竞技场和高雄体育场。", "主系表 + 非限制性定语从句", "is the first... 为主干；which also includes... 补充同类案例。", [w("wave", "n.", "浪潮；一批新事物")]),
    29: ("后者于2009年启用，拥有8844块光伏板，每年可生产高达1.14吉瓦时的电力。", "过去分词插入 + 分词补充", "inaugurated in 2009 补充时间；producing... 说明电力产量。", [w("inaugurate", "v.", "启用"), w("annually", "adv.", "每年")]),
    30: ("这使每年二氧化碳排放减少660吨，并在体育场未使用时为周边地区提供高达80%的电力。", "并列谓语", "reduces 与 supplies 并列；when 引导时间条件。", [w("annual output", "n.", "年排放量"), w("surrounding area", "n.", "周边地区")]),
    31: ("这证明体育场可以服务其所在城市，并在减少二氧化碳排放方面产生明显积极的影响。", "表语从句 + 并列谓语", "This is proof that...；serve 与 have a positive impact 并列。", [w("decidedly", "adv.", "明显地"), w("reduction", "n.", "减少")]),
    32: ("体育场馆一直是城市生活和文化的核心。", "现在完成时", "have always been 强调从过去到现在持续成立的事实。", [w("sporting arena", "n.", "体育场馆"), w("central to", "phr.", "对……核心的")]),
    33: ("在每个时代，体育场都获得了新的价值和用途：从军事堡垒到居住村落，从公共空间到剧场，最近又成为先进工程实验的场地。", "冒号列举", "has acquired 表逐步获得；冒号后用 from...to... 列举历史用途变化。", [w("acquire", "v.", "获得"), w("experimentation", "n.", "实验")]),
    34: ("今天的体育场把多种功能结合在一起，从而帮助城市创造可持续的未来。", "分词结果状语", "brings together 为主干；thus helping... 表结果。", [w("bring together", "phr.", "汇集；结合"), w("sustainable", "adj.", "可持续的")]),
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

    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    for row in idx.get("passages", []):
        if row.get("id") == data["id"]:
            row["quality"] = "teacher_refined"
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"refined {PATH}")


if __name__ == "__main__":
    main()
