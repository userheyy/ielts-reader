"""Teacher-refine Cambridge IELTS 17 Test 3 Passage 2 (Palm oil)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test3-p2.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


PHRASES = [
    w("palm oil", "n.", "棕榈油"),
    w("oil palm tree", "n.", "油棕树"),
    w("oil palm plantation", "n.", "油棕种植园"),
    w("best before date", "n.", "最佳食用日期"),
    w("seize the opportunity", "phr.", "抓住机会"),
    w("as a direct result of", "phr.", "作为……的直接结果"),
    w("global biodiversity", "n.", "全球生物多样性"),
    w("boycott movement", "n.", "抵制运动"),
    w("supply chain", "n.", "供应链"),
    w("strike a balance", "phr.", "取得平衡"),
    w("bone of contention", "n.", "争论的焦点"),
    w("sequester carbon", "phr.", "封存/吸收碳"),
    w("virgin forest", "n.", "原始森林"),
    w("get out of hand", "phr.", "失控"),
    w("carbon stocks", "n.", "碳储量"),
    w("certified sustainable palm oil", "n.", "经认证的可持续棕榈油"),
    w("green desert", "n.", "绿色荒漠（生物贫乏的单一种植区）"),
    w("keystone species", "n.", "关键物种"),
    w("bird's nest fern", "n.", "鸟巢蕨"),
]


# EN_FIX: clean the extracted English against the PDF originals.
EN_FIX = {
    1: "Palm oil is an edible oil derived from the fruit of the African oil palm tree, and is currently the most consumed vegetable oil in the world.",
    16: "But given the complexity of the argument, I think a much more nuanced story is closer to the truth.’ One response to the boycott movement has been the argument for the vital role palm oil plays in lifting many millions of people in the developing world out of poverty.",
    27: "But if it’s replacing rice, for example, it might actually sequester more carbon.’ The industry is now regulated by a group called the Roundtable on Sustainable Palm Oil (RSPO), consisting of palm growers, retailers, product manufacturers, and other interested parties.",
}


REFINED = {
    1: (
        "棕榈油是一种从非洲油棕树果实中提取的食用油，目前是世界上消费量最大的植物油。",
        "主系表 + 并列谓语",
        "主干是 Palm oil is an edible oil；derived from... 是过去分词短语作后置定语，修饰 oil；and is currently... 与前面并列，补充其“消费量最大”的地位。",
        [w("edible", "adj.", "可食用的"), w("derived from", "phr.", "从……提取")],
    ),
    2: (
        "几乎可以肯定，它就藏在我们清晨洗漱用的肥皂里、午餐吃的三明治里，以及白天当零食吃的饼干里。",
        "主系表 + 三个并列定语从句",
        "主干是 It’s almost certainly in...；in 后并列三个名词，每个名词后都跟一个省略了 that 的定语从句（we wash with / we have / we snack on），说明棕榈油无处不在。",
        [w("snack on", "phr.", "把……当零食吃")],
    ),
    3: (
        "为什么棕榈油对制造商如此有吸引力？",
        "特殊疑问句",
        "Why 引导的疑问句，作为下文展开的提问；attractive for manufacturers 是全段回答的核心，注意题目常改写成 appeal / benefit。",
        [w("manufacturer", "n.", "制造商")],
    ),
    4: (
        "主要是因为它独特的特性——比如在室温下能保持固态——使它成为长期保存的理想成分，让超市货架上许多包装食品的“最佳食用日期”能标到几个月、甚至几年之后。",
        "省略主干的原因句 + 现在分词结果状语",
        "承接上句，省略了 it is attractive；破折号间 such as remaining solid... 举例说明 properties；主干是 properties make it an ideal ingredient；allowing... 是现在分词短语表结果。",
        [w("preservation", "n.", "保存"), w("solid", "adj.", "固态的")],
    ),
    5: (
        "许多农民抓住机会，尽可能扩大油棕树的种植。",
        "主谓宾 + 不定式作定语",
        "主干是 Many farmers have seized the opportunity；to maximise the planting... 是不定式短语作定语，说明抓住的是什么机会。",
        [w("seize", "v.", "抓住"), w("maximise", "v.", "最大限度地增加")],
    ),
    6: (
        "1990 年至 2012 年间，全球用于种植油棕树的土地面积从 600 万公顷增至 1700 万公顷，如今约占全世界耕地总面积的十分之一。",
        "主谓 + 现在分词状语",
        "主干是 the global land area grew from 6 to 17 million hectares；devoted to growing... 是过去分词短语作定语修饰 land area；now accounting for... 是现在分词短语表补充说明。数字与占比常是填空题考点。",
        [w("devoted to", "phr.", "用于；专用于"), w("cropland", "n.", "耕地")],
    ),
    7: (
        "50 年前全球棕榈油年产量仅为 200 万吨，如今每年产量约为 6000 万吨，这个数字到本世纪中叶很可能会翻倍甚至翻三倍。",
        "介词短语前置 + 同位语",
        "From a mere two million tonnes... 前置作对比背景，与 there are now around 60 million tonnes 形成今昔对比；a figure looking likely to... 是同位语，补充说明这一产量数字的未来趋势。",
        [w("a mere", "phr.", "仅仅；只不过"), w("triple", "v.", "增至三倍")],
    ),
    8: (
        "然而，自然保护主义者把油棕种植园的迅速扩张列为一大隐忧，其中有多重原因。",
        "There be + why 引导定语从句",
        "主干是 there are multiple reasons；why 引导定语从句修饰 reasons；从句里 conservationists cite... as a major concern 是“把……视为一大担忧”，however 标志由“优势”转向“问题”。",
        [w("conservationist", "n.", "自然保护主义者"), w("cite", "v.", "举出；指出")],
    ),
    9: (
        "有关森林砍伐、栖息地破坏和物种数量锐减的新闻报道不计其数，而这一切都是为了大规模建立油棕单一种植而清理土地的直接结果，在马来西亚和印度尼西亚尤为严重。",
        "There be + 名词短语作同位补充",
        "主干是 There are countless news stories of...；all as a direct result of... 是名词短语，对前面现象作因果性补充；to establish... monoculture 是不定式表目的；particularly in... 缩小范围。",
        [w("monoculture", "n.", "单一种植（只种一种作物）"), w("deforestation", "n.", "森林砍伐")],
    ),
    10: (
        "濒危物种——最著名的是苏门答腊猩猩，还有犀牛、大象、老虎以及许许多多其他动物——都深受油棕种植园无可阻挡地扩张之害。",
        "主谓 + 破折号插入语",
        "主干是 Endangered species have suffered from the spread...；两个破折号之间是插入语，列举受害物种；most famously 突出最典型的苏门答腊猩猩，正是填空题答案。",
        [w("endangered species", "n.", "濒危物种"), w("fauna", "n.", "（某地区的）动物群")],
    ),
    11: (
        "“棕榈油无疑是对全球生物多样性最大的威胁之一，”布里斯托尔西英格兰大学的法农·埃尔伍德博士断言道。",
        "直接引语 + 倒装",
        "引号内是被引用的观点，one of the greatest threats to... 是表语；declares Dr Farnon Ellwood 是引语后的“主谓倒装”，of the University of... 是同位补充其身份。",
        [w("biodiversity", "n.", "生物多样性"), w("declare", "v.", "宣称；断言")],
    ),
    12: (
        "“棕榈油正在取代雨林，而雨林正是所有物种的栖息地。",
        "并列句 + 表语从句",
        "两个分句由 and 连接：前句 Palm oil is replacing rainforest；后句 rainforest is where all the species are，where 引导表语从句，等于“雨林是物种所在之地”。",
        [w("rainforest", "n.", "雨林")],
    ),
    13: (
        "那才是问题所在。”这在环保人士当中引发了一些激进的问题，比如消费者是否应当彻底抵制棕榈油。",
        "主谓宾 + such as 引出同位内容",
        "That’s a problem 收束前面的引语；This has led to some radical questions 是新句主干，This 指代前文整个论断；such as whether... 用 whether 从句举例说明是哪类问题。",
        [w("radical", "adj.", "激进的；根本的"), w("boycott", "v./n.", "抵制")],
    ),
    14: (
        "与此同时，伦敦大学亚非学院教授巴瓦尼·尚卡尔则认为：“说棕榈油是敌人、我们应当反对它，这很容易。",
        "主谓 + 直接引语（形式主语）",
        "主干是 Bhavani Shankar argues；Professor at... 是同位语说明身份；引号内 It’s easy to say that... 用 it 作形式主语，真正主语是 to say 后的 that 从句。",
        [w("argue", "v.", "主张；论证"), w("enemy", "n.", "敌人")],
    ),
    15: (
        "这样说能编出更戏剧化的故事，而且非常符合直觉。",
        "并列句",
        "两个分句由 and 连接：It makes for a more dramatic story（make for 意为“造成、有助于”）与 it’s very intuitive 并列，说明“简单化叙事”之所以吸引人的原因。",
        [w("make for", "phr.", "有助于；造就"), w("intuitive", "adj.", "符合直觉的")],
    ),
    16: (
        "但考虑到这一争论的复杂性，我认为一个远为细致的说法才更接近真相。”对抵制运动的一种回应是：人们主张棕榈油在帮助发展中国家数百万人脱贫方面起着至关重要的作用。",
        "让步状语 + 宾语从句（两句合并）",
        "本条含两句：前句 given the complexity... 是让步状语，主干 I think + (that) 宾语从句；后句主干是 One response has been the argument for the vital role...，palm oil plays 是省略 that 的定语从句修饰 role。（原文此处跨到 E 段，为保持句数合并，段标 E 已删。）",
        [w("nuanced", "adj.", "细致入微的"), w("lift ... out of poverty", "phr.", "使……脱贫")],
    ),
    17: (
        "既然发展中国家有那么多低收入者靠它维持生计，那么抵制、替代棕榈油、把它逐出全球供应链，真的可取吗？",
        "形式主语疑问句 + given 状语",
        "Is it desirable... 用 it 作形式主语，真正主语是 to have palm oil boycotted, replaced, eliminated（have + 宾语 + 过去分词，表“使……被……”）；given how many... 是让步/原因状语。",
        [w("desirable", "adj.", "可取的；值得拥有的"), w("livelihood", "n.", "生计")],
    ),
    18: (
        "如何在这些相互冲突的因素之间取得功利主义式的平衡，已成为激烈争论的焦点。",
        "疑问词不定式作主语",
        "How best to strike a balance... 是“疑问词 + 不定式”结构，整体作句子主语；主干谓语是 has become a serious bone of contention（bone of contention 意为“争论焦点”）。",
        [w("utilitarian", "adj.", "功利主义的"), w("bone of contention", "n.", "争论的焦点")],
    ),
    19: (
        "即便是森林砍伐这一论点，也没有表面看上去那么简单明了。",
        "as ... as 同级比较（否定）",
        "主干是 the deforestation argument isn’t straightforward；isn’t as straightforward as it seems 是同级比较的否定式，意为“不如它看起来那样直接”；Even 起强调作用。",
        [w("straightforward", "adj.", "简单明了的；直截了当的")],
    ),
    20: (
        "油棕种植园每公顷的产油量，至少是大豆、油菜籽、向日葵等竞争性油料作物的四倍，甚至可能高达十倍。",
        "比较级 + than 状语",
        "主干是 Oil palm plantations produce ... more oil per hectare than...；at least four and potentially up to ten times 修饰 more，构成“倍数 + 比较级 + than”结构，是本文核心数据。",
        [w("yield", "n.", "产量"), w("rapeseed", "n.", "油菜籽")],
    ),
    21: (
        "这种极高的产量——它也正是棕榈油如此有利可图的主要原因——很可能同时还是一项生态上的益处。",
        "非限制性定语从句（插入）",
        "主干是 That immensely high yield is potentially also an ecological benefit；两个破折号之间 which is predominantly what makes it so profitable 是非限制性定语从句，补充说明高产量的经济意义。",
        [w("yield", "n.", "产量"), w("profitable", "adj.", "有利可图的")],
    ),
    22: (
        "如果同一块土地产出的棕榈油能比任何竞争油料多十倍，那么要用那种竞争作物生产同样多的油，就得清理十倍的土地。",
        "if 条件状语从句 + 主句",
        "If... can be produced 是条件从句（被动语态）；主句 ten times more land would need to be cleared 也是被动，用 would 表推断结果；in order to produce... 是不定式表目的，逻辑上论证高产反而更省地。",
        [w("a patch of", "phr.", "一块（土地）"), w("clear", "v.", "清理（土地）")],
    ),
    23: (
        "至于碳排放问题，关键其实取决于油棕树取代的是什么。",
        "介词短语前置 + 宾语从句",
        "As for... 前置点明话题；主干是 the issue really depends on...；on 后接 what oil palm trees are replacing 这一 what 引导的宾语从句，暗示答案要看被替代的植被。",
        [w("carbon emissions", "n.", "碳排放"), w("depend on", "phr.", "取决于")],
    ),
    24: (
        "不同作物封存碳的程度各不相同——换句话说，就是它们从大气中捕获并储存在体内的碳量各有差异。",
        "定语从句 + 破折号同位解释",
        "主干是 Crops vary in the degree；to which they sequester carbon 是“介词 + which”引导的定语从句修饰 degree；破折号后 the amount of carbon... 是对 sequester carbon 的同位解释，they capture... and store 是修饰 carbon 的定语从句。",
        [w("sequester", "v.", "封存；隔离"), w("atmosphere", "n.", "大气")],
    ),
    25: (
        "植物封存的碳越多，它对气候变化的抑制作用就越大。",
        "the more ... the more 比较结构",
        "典型的 “the + 比较级..., the + 比较级...” 句式：前半 The more carbon a plant sequesters 是条件，后半 the more it reduces the effect... 是随之增强的结果。",
        [w("sequester", "v.", "封存；吸收"), w("climate change", "n.", "气候变化")],
    ),
    26: (
        "正如尚卡尔所解释的：“[棕榈油生产]在某些方面其实比其他替代作物封存了更多的碳。[……]当然，如果你砍的是原始森林，那就很糟糕——印度尼西亚和马来西亚正是如此，这种情况已经失控。",
        "直接引语 + if 条件句",
        "As Shankar explains 引出引语；引语主干 [Palm oil production] sequesters more carbon than other alternatives；后半 if you’re cutting down virgin forest it’s terrible 是条件句，that’s what’s happening... 与 it’s been allowed to get out of hand 补充现实情况。",
        [w("virgin forest", "n.", "原始森林"), w("get out of hand", "phr.", "失控")],
    ),
    27: (
        "但如果它取代的是比如水稻，那它实际上可能封存更多的碳。”如今这一行业由一个名为“可持续棕榈油圆桌会议”（RSPO）的组织进行监管，其成员包括棕榈种植者、零售商、产品制造商及其他利益相关方。",
        "if 条件句 + 现在分词状语（两句合并）",
        "本条含两句：前句 But if it’s replacing rice... it might sequester more carbon 是条件句收束引语；后句主干是 The industry is now regulated by a group（被动语态），called the RSPO 是过去分词定语，consisting of... 是现在分词状语列举成员。（原文此处跨到 G 段，为保持句数合并，段标 G 已删。）",
        [w("regulate", "v.", "监管；规范"), w("interested parties", "n.", "利益相关方")],
    ),
    28: (
        "在过去十来年里，各方就棕榈油生产商必须达到的标准逐渐达成了一致，只有满足这些标准，其产品才能被正式视为“可持续的”。",
        "被动语态 + 定语从句 + in order for 目的状语",
        "主干是 an agreement has gradually been reached（现在完成时被动）；regarding standards 引出话题；that producers... have to meet 是定语从句修饰 standards；in order for their product to be regarded as... 是“for + 逻辑主语 + 不定式”的目的状语。",
        [w("sustainable", "adj.", "可持续的"), w("meet a standard", "phr.", "达到标准")],
    ),
    29: (
        "RSPO 的标准包括：禁止砍伐原始森林、保持透明度、定期评估碳储量等等。",
        "主谓宾 + among other 收尾",
        "主干是 The RSPO insists upon...；upon 后并列三项要求（no virgin forest clearing / transparency / regular assessment of carbon stocks）；among other criteria 表示“这只是诸多标准中的几项”。carbon stocks 是填空题答案。",
        [w("insist upon", "phr.", "坚持要求"), w("carbon stocks", "n.", "碳储量")],
    ),
    30: (
        "只有在这些要求全部得到满足之后，这种油才被允许作为“经认证的可持续棕榈油”（CSPO）出售。",
        "Only + 状语从句引起的倒装",
        "句首 Only once these requirements are fully satisfied 是 only 引导的时间状语从句，导致主句部分倒装（is the oil allowed...）；被动语态强调“被允许出售”这一资格。",
        [w("requirement", "n.", "要求；条件"), w("certified", "adj.", "经认证的")],
    ),
    31: (
        "最新数据显示，RSPO 目前每年认证约 1200 万吨棕榈油，约相当于全球棕榈油总产量的 21%。",
        "宾语从句 + 同位补充",
        "主干是 Recent figures show that...；that 引导宾语从句，从句主干 the RSPO now certifies around 12 million tonnes；equivalent to roughly 21 percent... 是形容词短语作补充，说明这一产量的占比。",
        [w("certify", "v.", "认证"), w("equivalent to", "phr.", "相当于")],
    ),
    32: (
        "甚至有一线希望：油棕种植园或许不必像埃尔伍德所形容的那样，是贫瘠的单一种植区，即“绿色荒漠”。",
        "There be + 同位语从句 + as 状语从句",
        "主干是 There is even hope；that oil palm plantations might not need to be... 是同位语从句解释 hope 的内容；or ‘green deserts’ 是对 sterile monocultures 的换称；as Ellwood describes them 是方式状语从句。",
        [w("sterile", "adj.", "贫瘠的；不毛的"), w("green desert", "n.", "绿色荒漠")],
    ),
    33: (
        "埃尔伍德实验室的新研究，指向了一种可能带来根本改变的植物。",
        "主谓宾 + 定语从句",
        "主干是 New research hints at one plant（hint at 意为“暗示、指向”）；which might make all the difference 是定语从句修饰 plant，make all the difference 意为“起决定性作用”。",
        [w("hint at", "phr.", "暗示；指向"), w("make all the difference", "phr.", "起决定性作用")],
    ),
    34: (
        "鸟巢蕨（Asplenium nidus）以附生方式生长在树上（即它只依附树木获取支撑，而非养分），原产于许多热带地区，在那里它作为关键物种发挥着至关重要的生态作用。",
        "主谓 + 括号插入 + where 定语从句",
        "主干是 The bird’s nest fern grows on trees...；括号内 meaning it’s dependent on... 解释 epiphytic（附生）；and is native to... 是并列谓语；where 引导定语从句修饰 tropical regions，说明它在当地的作用。",
        [w("epiphytic", "adj.", "附生的"), w("keystone species", "n.", "关键物种")],
    ),
    35: (
        "埃尔伍德认为，把鸟巢蕨重新引入油棕种植园，有可能让这些地区恢复生物多样性，为形形色色的物种提供家园——从真菌、细菌，到昆虫、两栖动物、爬行动物乃至哺乳动物等各类无脊椎与脊椎动物。",
        "宾语从句 + 现在分词结果状语",
        "主干是 Ellwood believes that...；that 从句主语是动名词短语 reintroducing the bird’s nest fern，谓语 could allow these areas to recover their biodiversity；providing a home... 是现在分词表结果，from... to... 列举受益物种。",
        [w("reintroduce", "v.", "重新引入"), w("invertebrate", "n.", "无脊椎动物")],
    ),
}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    data["quality"] = "teacher_refined"
    data["phrases"] = PHRASES
    for s in data["sentences"]:
        sid = s["id"]
        if sid in EN_FIX:
            s["en"] = EN_FIX[sid]
        zh, gtype, note, words = REFINED[sid]
        s["zh"] = zh
        s["grammar"] = {"type": gtype, "note": note}
        s["words"] = words
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if INDEX.exists():
        idx = json.loads(INDEX.read_text(encoding="utf-8"))
        for row in idx.get("passages", []):
            if row.get("id") == data["id"]:
                row["quality"] = "teacher_refined"
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"refined {PATH}")


if __name__ == "__main__":
    main()
