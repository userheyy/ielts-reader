"""Teacher-refine Cambridge IELTS 17 Test 1 Passage 3."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test1-p3.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


PHRASES = [
    w("To Catch a King", "n.", "《追捕国王》（书名）"),
    w("King Charles II", "n.", "查理二世国王"),
    w("the Battle of Worcester", "n.", "伍斯特战役"),
    w("do a deal with", "phr.", "与……达成交易/协议"),
    w("in return for", "phr.", "作为……的交换"),
    w("pre-emptive strike", "n.", "先发制人的打击"),
    w("national manhunt", "n.", "全国性追捕"),
    w("seek refuge", "phr.", "寻求避难"),
    w("commit something to paper", "phr.", "把某事写下来"),
    w("bring to life", "phr.", "生动呈现"),
    w("even-handed sympathy", "n.", "不偏不倚的同情/理解"),
    w("hit the mark", "phr.", "切中要点；达到预期"),
    w("do justice to", "phr.", "公平呈现；充分体现"),
    w("have a treat in store", "phr.", "将会有惊喜/享受等着"),
]


REFINED = {
    1: ("查尔斯·斯宾塞的最新著作《追捕国王》讲述了查理二世在1651年9月伍斯特战役惨败后六周内被追捕的故事。", "主谓宾 + 后置介词短语", "主干是 book tells us the story；of the hunt 修饰 story；in the six weeks after... 交代故事时间背景。", [w("hunt", "n.", "追捕"), w("resounding defeat", "n.", "惨败")]),
    2: ("而这真是一个精彩的故事。", "感叹句", "what a story it is 是强调式感叹，用于书评中表达叙事吸引力。", [w("what a story", "phr.", "真是精彩的故事")]),
    3: ("1649年其父被议会派处决后，年轻的查理二世牺牲了其父为之而死的一项重要原则，与苏格兰人达成协议，接受长老会为国教，以换取加冕为苏格兰国王。", "时间状语从句 + 分词结果", "After 引导时间背景；sacrificed 与 did a deal 是并列动作；thereby accepting... 表结果；in return for 表交换条件。", [w("execute", "v.", "处决"), w("principle", "n.", "原则"), w("Presbyterianism", "n.", "长老会教义")]),
    4: ("他抵达爱丁堡促使英格兰议会军先发制人地入侵苏格兰。", "名词化主语 + prompt sb to do", "His arrival 是名词化主语；prompted...to invade 表“促使……做”。", [w("prompt", "v.", "促使"), w("invade", "v.", "入侵")]),
    5: ("随后，苏格兰又入侵了英格兰。", "被动语态", "This was followed by... 表“随后发生……”，常用于叙事顺序。", [w("invasion", "n.", "入侵")]),
    6: ("双方最终于1651年在英格兰西部的伍斯特交锋。", "简单句", "faced one another 表“对阵、交锋”；at Worcester 与 in 1651 分别交代地点和时间。", [w("face one another", "phr.", "交锋；对峙")]),
    7: ("在城外草地上被议会军彻底击败后，这位21岁的国王成了全国追捕的对象，抓获他可获得巨额赏金。", "After doing + 复合宾语", "After being... 是被动动名词作时间状语；found himself the subject... 表“发现自己成为……对象”；with 短语补充悬赏信息。", [w("comprehensively", "adv.", "彻底地"), w("manhunt", "n.", "追捕"), w("capture", "n.", "抓捕")]),
    8: ("在接下来的六周里，他经历了一连串惊心动魄的险些被捕的逃脱，设法躲过议会派，随后前往法国避难。", "插入介词短语 + manage to do", "through a series of... 插入说明逃脱方式；managed to evade...before seeking... 表先后动作。", [w("evade", "v.", "躲避"), w("refuge", "n.", "避难")]),
    9: ("在接下来的九年里，身无分文且战败的查理只带着一小群忠诚支持者在欧洲各地漂泊。", "形容词并列 + 介词短语", "penniless and defeated 并列修饰 Charles；with only... 表伴随。", [w("penniless", "adj.", "身无分文的"), w("loyal", "adj.", "忠诚的")]),
    10: ("多年后，复辟为王之后，50岁的查理二世请求与作家兼日记作者塞缪尔·佩皮斯会面。", "时间状语 + 同位身份", "after his restoration as king 交代身份恢复；writer and diarist 并列说明 Pepys 身份。", [w("restoration", "n.", "复辟；恢复王位"), w("diarist", "n.", "日记作者")]),
    11: ("他请佩皮斯把自己的故事写下来，目的是确保这段极不寻常的经历永远不被遗忘。", "不定式作表语 + 宾语从句", "His intention...was to ensure...；when asking... 作时间背景；that 从句说明 ensure 的内容。", [w("intention", "n.", "意图"), w("episode", "n.", "事件；经历")]),
    12: ("在两次各三小时的谈话中，国王向他非常详细地讲述了自己作为逃亡者度过那六周的个人回忆。", "介词短语状语 + of 结构", "Over...sittings 表谈话过程；related to him... 表“向他讲述”；of the six weeks... 修饰 recollections。", [w("sitting", "n.", "一次会谈/坐谈"), w("fugitive", "n.", "逃亡者")]),
    13: ("国王和书记员坐定后，查理开始讲述：‘战斗已经完全失败、毫无挽回希望之后，我开始思考保全自己的最佳方式。’", "As 时间从句 + 直接引语", "As 引导背景动作；commenced his story 引出直接引语；so...as to... 表程度结果。", [w("commence", "v.", "开始"), w("recovery", "n.", "恢复；挽回")]),
    14: ("斯宾塞这本书的一大乐趣，尤其得益于它使用了查理二世本人以及其支持者的叙述，在于读者离事件现场如此之近。", "主系表 + 插入同位说明", "One of the joys...is just how...；a result not least of... 是插入说明原因；gets to the action 表贴近事件。", [w("narrative", "n.", "叙述"), w("not least", "phr.", "尤其；很大程度上")]),
    15: ("逐日重述逃亡者的行动提供了生动细节：用农用大剪刀剪掉国王长发，用胡桃叶染深他苍白的皮肤，以及查理躺在博斯科贝尔树林一棵大橡树枝上、议会士兵在下方搜查林地的那一天。", "冒号列举 + 多重 of 结构", "retelling...provides details 是主干；冒号后列举三个细节；as 从句说明士兵同时搜查。", [w("retelling", "n.", "重述"), w("shears", "n.", "大剪刀"), w("scour", "v.", "搜寻")]),
    16: ("斯宾塞既展现了幽默——例如查理的朋友亨利·威尔莫特荒唐地拒绝伪装，理由是这有损他的尊严——也展现了国王行踪秘密被谨慎透露给支持者时的情感张力。", "both...and... 并列", "draws out both...and... 表同时呈现两方面；such as 插入例子；when 引导时间情境。", [w("preposterous", "adj.", "荒唐的"), w("disguise", "n./v.", "伪装"), w("dignity", "n.", "尊严")]),
    17: ("查理在伍斯特战败后的冒险经历掩盖了一个令人不安的事实：尽管英格兰几乎所有人都对其父被处决感到震惊，但他们并不欢迎他的儿子率苏格兰军队到来，而是牢牢关上了大门。", "宾语从句 + whilst 让步", "hide the truth that...；whilst 引导让步；had not welcomed...but had instead... 构成转折。", [w("uncomfortable truth", "n.", "令人不安的事实"), w("appalled", "adj.", "震惊的")]),
    18: ("这部分是因为他率领的看起来像一支外国入侵军，部分是因为经历近十年内战后，人们迫切想避免战争再次开始。", "partly because...and partly because", "两个 partly because 并列解释原因；what looked like... 作介词 of 的宾语。", [w("foreign invasion force", "n.", "外国入侵军"), w("desperate", "adj.", "迫切的")]),
    19: ("这使得查理二世后来一直如此喜爱这个故事，显得更加有趣。", "make + it + 形容词 + that", "This makes it interesting that... 中 it 是形式宾语；ever after 表从那以后一直。", [w("ever after", "phr.", "从那以后一直")]),
    20: ("除了把故事讲给任何愿意听的人、惹得朝臣翻白眼之外，他还启动了一系列纪念这段经历的举措。", "As well as doing + 主谓宾", "As well as retelling... 表“不仅”；causing... 作结果；set in train 表启动。", [w("courtier", "n.", "朝臣"), w("initiative", "n.", "举措"), w("memorialise", "v.", "纪念")]),
    21: ("将要设立一个新的骑士团，即皇家橡树骑士团。", "There be + 不定式", "There was to be 表计划/安排将发生；the Knights... 是同位解释。", [w("order of chivalry", "n.", "骑士团")]),
    22: ("人们创作了一系列描绘该事件的巨幅油画，其中包括一幅两米宽的博斯科贝尔树林画布，以及六幅同样巨大的国王逃亡图。", "被动语态 + including", "were produced 是被动；depicting... 修饰 paintings；including 列举作品。", [w("depict", "v.", "描绘"), w("canvas", "n.", "画布")]),
    23: ("1660年，查理二世委托画家约翰·迈克尔·赖特，在其寝宫天花板上绘制一队飞翔的小天使把一棵橡树托向天堂的画面。", "commission sb to do", "commissioned the artist to paint... 是固定结构；carrying... 修饰 cherubs。", [w("commission", "v.", "委托创作"), w("cherub", "n.", "小天使形象"), w("bedchamber", "n.", "寝宫")]),
    24: ("很难想象还有许多其他国王会如此热情地纪念人生最低谷，或者一开始就能完成这样一次逃脱。", "It is hard to imagine + doing", "It 为形式主语；marking 与 pulling off 并列；lowest point 指人生低谷。", [w("pull off", "phr.", "成功完成"), w("enthusiastically", "adv.", "热情地")]),
    25: ("查尔斯·斯宾塞是把这个故事传给新一代读者的完美人选。", "主系表 + 不定式定语", "the perfect person 后用 to pass... 修饰，说明其适合做什么。", [w("pass on", "phr.", "传递")]),
    26: ("他节奏明快、可读性强的文字巧妙避开现代习语，并优雅地让这个伟大故事的细节鲜活起来。", "并列谓语", "steers clear of 与 brings to life 并列；pacey, readable 修饰 prose。", [w("pacey", "adj.", "节奏明快的"), w("steer clear of", "phr.", "避开"), w("idiom", "n.", "习语")]),
    27: ("他对逃亡国王和追捕他的强硬共和政权都表现出不偏不倚的同情理解，并成功实现了自己的愿望：比以往同题材书籍更深入地探索这个故事的背景。", "并列句 + 比较结构", "has sympathy 与 succeeds 并列；both...and... 表平衡态度；far more...than... 表比较。", [w("even-handed", "adj.", "公正的"), w("republican regime", "n.", "共和政权"), w("subject matter", "n.", "题材")]),
    28: ("事实上，本书前三分之一讲的就是查理二世最初如何来到伍斯特；对有些人来说，仅这一点就足以成为阅读《追捕国王》的理由。", "宾语从句 + which 非限制性定语从句", "is about how...；which 指代前面整件事并补充其吸引力。", [w("opening third", "n.", "开篇三分之一"), w("reason alone", "phr.", "单凭这一点就是理由")]),
    29: ("最终留下的诱人问题是：这一切究竟意味着什么。", "主系表 + of what 从句", "The question left 是主语；that of what... 中 that 指 question，of what 引出问题内容。", [w("tantalising", "adj.", "诱人的；撩人的")]),
    30: ("如果没有这六周经历，查理二世会不会成为一个不同的国王？", "虚拟条件倒装", "had these six weeks never happened 是 if these weeks had never happened 的倒装形式；Would...have been 表对过去的假设。", [w("had...happened", "grammar", "虚拟条件倒装")]),
    31: ("躲藏的日日夜夜一定以某种方式影响了他。", "情态动词表推测", "must have affected 表对过去的强烈推测；in some way 表影响方式不明确。", [w("affect", "v.", "影响")]),
    32: ("需要乔装、仅靠机智和魅力求生、用欺骗和诡计从险境中逃脱，这些是否帮助塑造了他？", "并列不定式 + 疑问句", "the need to assume / to survive / to use 三个不定式并列；help form him 表塑造其性格。", [w("subterfuge", "n.", "诡计"), w("tight corner", "n.", "困境")]),
    33: ("这是本书唯一没有完全切中要点的地方。", "where 定语从句", "where the book... 修饰 area；doesn’t quite hit the mark 是书评常用委婉批评。", [w("hit the mark", "phr.", "切中要点；达到预期")]),
    34: ("相反，书中把晚年查理二世描绘成一个无能、贪图享乐的君主，这既没有充分体现这个人，也没有准确呈现其性格的复杂性。", "主谓宾 + neither...or", "depiction of... 是主语；doesn’t do justice to... 表“没有公正呈现”；or 连接第二个对象。", [w("depiction", "n.", "描绘"), w("monarch", "n.", "君主"), w("complexity", "n.", "复杂性")]),
    35: ("不过，除了这一点小小的不满，《追捕国王》是一本极佳的读物；那些此前对这个著名故事知之甚少的读者，将会发现有一份享受在等着他们。", "让步转折 + 定语从句", "this one niggle aside 表“撇开这个小问题”；those who... 为先行词加定语从句；have a treat in store 表会有惊喜。", [w("niggle", "n.", "小抱怨"), w("excellent read", "n.", "佳作；好书")]),
}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    data["quality"] = "teacher_refined"
    data["phrases"] = PHRASES

    # Correct evidence offsets now that the teacher review has checked the source.
    fixes = {
        29: 7,
        30: 7,
        31: 8,
        33: 12,
        34: 13,
        35: 14,
        39: 27,
    }
    for group in data.get("questions", []):
        for item in group.get("items", []):
            if item["number"] in fixes:
                item["evidence_sentence"] = fixes[item["number"]]

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
