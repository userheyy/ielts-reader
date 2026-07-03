"""Teacher-refine Cambridge IELTS 17 Test 4 Passage 3.

The draft_raw JSON for this passage had a badly scrambled text layer: the PDF
paragraphs were interleaved, sentence boundaries were broken, quotes were mojibake
(``), stray paragraph letters (A-H) and header/instruction text were mixed in,
and the true 57-sentence text had been squashed into 53 garbled entries.

Rather than patch dozens of unusable fragments, this script rebuilds the whole
`sentences` array from the PDF (page89.png / page90.png) with correct EN, zh,
grammar and words, remaps `questions[].evidence_sentence` to the new ids, sets
quality=teacher_refined, adds top-level phrases, and syncs index.json
(sentence_count 53 -> 57).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "passages" / "c17-test4-p3.json"
INDEX = ROOT / "data" / "index.json"


def w(word, pos, definition):
    return {"w": word, "pos": pos, "def": definition}


PHRASES = [
    w("blindfold chess", "n.", "盲棋（蒙眼下棋）"),
    w("take on opponents", "phr.", "迎战对手"),
    w("mental feat", "n.", "脑力壮举"),
    w("keep active at once", "phr.", "同时保持（多个局面）在脑中运转"),
    w("get one's kicks from", "phr.", "从……中获得刺激/乐趣"),
    w("go back centuries", "phr.", "可追溯到数百年前"),
    w("standard memory tests", "n.", "标准记忆测试"),
    w("brain scans", "n.", "脑部扫描"),
    w("frontoparietal control network", "n.", "额顶控制网络"),
    w("visual input", "n.", "视觉输入"),
    w("dedicate oneself to", "phr.", "全身心投入于"),
]


# Each entry: id -> (en, zh, gtype, note, [words])
# para is assigned by PARA_SIZES below (A..H -> 1..8).
S = {
    # ---- Paragraph A (para 1) ----
    1: ("Next month, a chess player named Timur Gareyev will take on nearly 50 opponents at once.",
        "下个月，一位名叫蒂穆尔·加列耶夫（Timur Gareyev）的国际象棋棋手将同时迎战近 50 名对手。",
        "主干句 + 后置定语", "主干是 a chess player will take on opponents；named Timur Gareyev 为过去分词作后置定语，at once 意为“同时”，是全文核心难点所在。",
        [w("take on", "phr.", "迎战；对付"), w("opponent", "n.", "对手")]),
    2: ("But that is not the hard part.",
        "但这还不是最难的部分。",
        "主系表 + 转折", "But 转折，为下句蒙眼这一真正难点作铺垫；that 指代上句“同时迎战近 50 人”。",
        [w("the hard part", "phr.", "难点；难办的部分")]),
    3: ("While his challengers will play the games as normal, Gareyev himself will be blindfolded.",
        "他的挑战者们会像平常一样正常对弈，而加列耶夫本人则会被蒙上双眼。",
        "while 让步/对比状语从句 + 被动语态", "While 引导对比状语从句（对手正常 vs. 他蒙眼）；主句 will be blindfolded 为将来被动；himself 强调“唯独他”——正对应第 33 题“所有人都被蒙眼”为 FALSE。",
        [w("challenger", "n.", "挑战者"), w("blindfold", "v.", "蒙住……的眼睛")]),
    4: ("Even by world record standards, it sets a high bar for human performance.",
        "即便以世界纪录的标准来衡量，这也为人类的表现设立了很高的门槛。",
        "让步状语 + 隐喻搭配", "Even by... standards 作让步状语；set a high bar 是“设定高标准/高门槛”的固定隐喻搭配；it 指这场蒙眼车轮战。",
        [w("set a high bar", "phr.", "设立很高的标准"), w("world record", "n.", "世界纪录")]),
    5: ("The 28-year-old already stands out in the rarefied world of blindfold chess.",
        "这位 28 岁的棋手在盲棋这一小众而高深的领域早已出类拔萃。",
        "主谓 + 介词短语", "主干 The 28-year-old stands out；stand out 意为“脱颖而出”；rarefied world 指“少数高手才能进入的圈子”，rarefied 是雅思常考的高级形容词。",
        [w("stand out", "phr.", "脱颖而出；出众"), w("rarefied", "adj.", "小众而高深的；曲高和寡的")]),
    6: ("He has a fondness for bright clothes and unusual hairstyles, and he gets his kicks from the adventure sport of BASE jumping.",
        "他偏爱鲜艳的服装和别致的发型，还从定点跳伞这项极限运动中寻求刺激。",
        "并列句 + 固定搭配", "两个分句由 and 并列；have a fondness for 意为“喜爱”；get one's kicks from 意为“从……中获得刺激”——这为第 34 题（是否在定点跳伞夺冠）设下 NOT GIVEN 的陷阱。",
        [w("fondness", "n.", "喜爱；偏好"), w("get one's kicks from", "phr.", "从……中获得刺激")]),
    7: ("He has already proved himself a strong chess player, too.",
        "他也早已证明自己是一名实力强劲的棋手。",
        "现在完成时 + 复合宾语", "prove oneself + 名词 是“证明自己是……”的复合宾语结构；already、too 都在强调他棋艺本身也很出众。",
        [w("prove oneself", "phr.", "证明自己（的能力）")]),
    8: ("In a 10-hour chess marathon in 2013, Gareyev played 33 games in his head simultaneously.",
        "在 2013 年一场长达 10 小时的国际象棋马拉松赛中，加列耶夫在脑中同时下了 33 盘棋。",
        "时间状语 + 主谓宾", "两个 in 短语分别交代时长与年份；in his head、simultaneously 是理解“盲棋+同时多盘”的关键，常被题目改写为 in his mind / at the same time。",
        [w("marathon", "n.", "马拉松式的长时间活动"), w("simultaneously", "adv.", "同时地")]),
    9: ("He won 29 and lost none.",
        "他赢了 29 盘，一盘未输。",
        "并列谓语", "won 与 lost 并列；none 意为“一盘都没输”，是强调战绩的否定词。",
        [w("none", "pron.", "一个也没有")]),
    10: ("The skill has become his brand: he calls himself the Blindfold King.",
         "这项本领已成了他的标志：他自称“盲棋之王”。",
         "冒号解释 + 复合宾语", "冒号后用具体做法解释前句的 brand；call oneself + 名词 为复合宾语（自称……）。",
         [w("brand", "n.", "标志；招牌形象"), w("blindfold", "adj.", "蒙眼的")]),

    # ---- Paragraph B (para 2) ----
    11: ("But Gareyev's prowess has drawn interest from beyond the chess-playing community.",
         "但加列耶夫的高超本领吸引了国际象棋圈以外人士的关注。",
         "主谓宾 + 介词短语", "主干 prowess has drawn interest；from beyond the... community 意为“来自……圈子之外”——这正是第 30 题“为何引起科学家兴趣”的定位句。",
         [w("prowess", "n.", "高超的本领；造诣"), w("beyond", "prep.", "超出……的范围")]),
    12: ("In the hope of understanding how he and others like him can perform such mental feats, researchers at the University of California in Los Angeles (UCLA) called him in for tests.",
         "为了弄清他以及像他这样的人如何能完成这类脑力壮举，加州大学洛杉矶分校（UCLA）的研究人员把他请来做测试。",
         "目的状语 + 宾语从句", "In the hope of doing 作目的状语；how 引导的宾语从句作 understanding 的宾语；主句是 researchers called him in for tests。",
         [w("mental feat", "n.", "脑力壮举"), w("call sb in", "phr.", "把某人请来（帮忙/受检）")]),
    13: ("They now have their first results.",
         "如今他们已有了初步结果。",
         "主谓宾（短句过渡）", "简短的主谓宾句，起承上启下作用；first results 指“最初/初步的结果”，与下文 tentative、initial 呼应。",
         [w("results", "n.", "（研究）结果")]),
    14: ("'The ability to play a game of chess with your eyes closed is not a far reach for most accomplished players,' said Jesse Rissman, who runs a memory lab at UCLA.",
         "“对大多数造诣深厚的棋手来说，闭着眼睛下一盘棋并非遥不可及，”在 UCLA 主持一间记忆实验室的杰西·里斯曼（Jesse Rissman）说道。",
         "直接引语 + 非限制性定语从句", "引号内主干 The ability... is not a far reach；not a far reach 意为“并不难达到”；who 引导非限定性定语从句补充说明 Rissman——此句对应第 36 题（好棋手很可能会下盲棋）为 TRUE。",
         [w("a far reach", "phr.", "遥不可及的事"), w("accomplished", "adj.", "造诣深的；技艺精湛的")]),
    15: ("'But the thing that's so remarkable about Timur and a few other individuals is the number of games they can keep active at once.",
         "“但蒂穆尔和另外少数几个人真正了不起之处，在于他们能同时在脑中运转的棋局数量。",
         "主系表 + 双重定语从句", "主干 the thing... is the number；that's so remarkable about... 修饰 the thing；(that) they can keep active 修饰 games；keep games active 意为“让多盘棋同时在脑中运转”。",
         [w("remarkable", "adj.", "非凡的；了不起的"), w("keep active", "phr.", "使保持活跃/运转")]),
    16: ("To me it is simply astonishing.'",
         "在我看来，这简直令人惊叹。”",
         "主系表 + 强调副词", "To me 作状语表个人看法；simply 加强 astonishing 的语气（“简直”）。",
         [w("astonishing", "adj.", "令人惊叹的")]),

    # ---- Paragraph C (para 3) ----
    17: ("Gareyev learned to play chess in his native Uzbekistan when he was six years old.",
         "加列耶夫六岁时在故乡乌兹别克斯坦学会了下国际象棋。",
         "主谓宾 + 时间状语从句", "主干 Gareyev learned to play chess；when 引导时间状语从句交代年龄；native 意为“出生地的、本国的”。",
         [w("native", "adj.", "故乡的；出生地的"), w("chess", "n.", "国际象棋")]),
    18: ("Tutored by his grandfather, he entered his first tournament aged eight and soon became obsessed with competitions.",
         "在祖父的指导下，他八岁便参加了首场比赛，很快就痴迷于各类赛事。",
         "过去分词状语 + 并列谓语", "Tutored by... 为过去分词作状语（表被动，“受……指导”）；entered 与 became 并列；aged eight 是“八岁时”的省略式状语；be obsessed with 意为“痴迷于”。",
         [w("tutor", "v.", "指导；辅导"), w("be obsessed with", "phr.", "痴迷于")]),
    19: ("At 16, he was crowned Asia's youngest ever chess grandmaster.",
         "16 岁时，他被加冕为亚洲有史以来最年轻的国际象棋特级大师。",
         "被动语态 + 最高级", "was crowned 为被动语态（“被封为”）；youngest ever 意为“有史以来最年轻的”，ever 强化最高级。",
         [w("crown", "v.", "为……加冕；封（某人为）"), w("grandmaster", "n.", "（国际象棋）特级大师")]),
    20: ("He moved to the US soon after, and as a student helped his university win its first national chess championship.",
         "不久后他移居美国，并在求学期间帮助所在大学赢得了首个全国国际象棋冠军。",
         "并列谓语 + help sb do", "moved 与 helped 并列；as a student 作状语（“在做学生期间”）；help + sb + do 结构（帮助某人做某事）。",
         [w("championship", "n.", "冠军头衔；锦标赛")]),
    21: ("In 2013, Gareyev was ranked the third best chess player in the US.",
         "2013 年，加列耶夫被评为全美排名第三的国际象棋棋手。",
         "被动语态 + 序数排名", "was ranked + 名词 为被动语态（“被排为……”）；the third best 表“第三好的”，序数词 + 最高级的常见排名说法。",
         [w("be ranked", "phr.", "被评为……名次；排名为")]),

    # ---- Paragraph D (para 4) ----
    22: ("To the uninitiated, blindfold chess seems to call for superhuman skill.",
         "在外行人看来，盲棋似乎需要超凡的技艺。",
         "主谓 + seem to do", "To the uninitiated 作状语（“对不懂行的人而言”）；seem to call for 意为“似乎需要”；call for 意为“需要”。",
         [w("the uninitiated", "n.", "外行；不懂行的人"), w("call for", "phr.", "需要；要求")]),
    23: ("But displays of the feat go back centuries.",
         "但这一绝技的展示可追溯到数百年前。",
         "主谓 + 转折", "But 转折；主干 displays go back centuries；go back centuries 意为“可上溯几个世纪”——本句是第 27 题“提及盲棋的早期实例”的定位句。",
         [w("display", "n.", "展示；表演"), w("go back", "phr.", "追溯到（某时）")]),
    24: ("The first recorded game in Europe was played in 13th-century Florence.",
         "欧洲有记载的第一场盲棋对局发生在 13 世纪的佛罗伦萨。",
         "被动语态 + 过去分词定语", "was played 为被动；recorded 作过去分词定语修饰 game（“有记载的”）；in 13th-century Florence 为地点状语。",
         [w("recorded", "adj.", "有记录/记载的"), w("Florence", "n.", "佛罗伦萨（意大利城市）")]),
    25: ("In 1947, the Argentinian grandmaster Miguel Najdorf played 45 simultaneous games in his mind, winning 39 in the 24-hour session.",
         "1947 年，阿根廷特级大师米格尔·纳伊多夫（Miguel Najdorf）在脑中同时下了 45 盘棋，在这场持续 24 小时的比赛中赢了 39 盘。",
         "主谓宾 + 现在分词状语", "主干 Najdorf played 45 games；winning 39... 为现在分词作结果状语；simultaneous、in his mind 呼应全文的“同时多盘盲棋”主题。",
         [w("simultaneous", "adj.", "同时发生的"), w("session", "n.", "一场（比赛/活动）")]),

    # ---- Paragraph E (para 5) ----
    26: ("Accomplished players can develop the skill of playing blind even without realising it.",
         "造诣深的棋手甚至能在不知不觉中练就盲下的本领。",
         "主谓宾 + without doing 状语", "主干 players can develop the skill；of playing blind 修饰 skill；even without realising it 作状语（“甚至没意识到”），play blind 意为“不看棋盘下棋”。",
         [w("develop a skill", "phr.", "练就/培养一项技能"), w("play blind", "phr.", "盲下（不看棋盘）")]),
    27: ("The nature of the game is to run through possible moves in the mind to see how they play out.",
         "这种棋的本质，就是在脑中把各种可能的走法过一遍，看看结果如何。",
         "主系表 + 不定式表目的", "主干 The nature is to run through moves；不定式 to see... 表目的；how they play out 为宾语从句（“走法如何发展/收场”）——此句概述盲棋的运作方式，对应第 28 题。",
         [w("run through", "phr.", "把……快速过一遍；演练"), w("play out", "phr.", "（事情）发展；收场")]),
    28: ("From this, regular players develop a memory for the patterns the pieces make, the defences and attacks.",
         "由此，普通棋手会对棋子构成的种种局面——防守与进攻——形成记忆。",
         "主谓宾 + 省略关系词的定语从句", "From this 承接上句；主干 players develop a memory；(that) the pieces make 是省略关系词的定语从句修饰 patterns；the defences and attacks 是 patterns 的同位补充。",
         [w("pattern", "n.", "（棋子构成的）局面；图式"), w("defence", "n.", "防守")]),
    29: ("'You recreate it in your mind,' said Gareyev.",
         "“你是在脑海里把它重建出来，”加列耶夫说。",
         "直接引语 + 主谓倒装", "引语后 said Gareyev 为主谓倒装（引述句常见）；recreate 意为“重建、再现”，it 指棋盘上的局面。",
         [w("recreate", "v.", "重现；重建")]),
    30: ("'A lot of players are capable of doing what I'm doing.'",
         "“很多棋手都有能力做到我所做的事。”",
         "主系表 + 宾语从句", "主干 players are capable of doing；be capable of doing 意为“有能力做”；what I'm doing 为宾语从句作 of 的宾语。",
         [w("be capable of", "phr.", "有能力（做）")]),
    31: ("The real mental challenge comes from playing multiple games at once in the head.",
         "真正的脑力挑战，来自在脑中同时下多盘棋。",
         "主谓 + 动名词宾语", "主干 The real challenge comes from playing...；come from doing 意为“源自做某事”；at once、in the head 再次点出核心难点。",
         [w("come from", "phr.", "源自；来自"), w("multiple", "adj.", "多个的")]),
    32: ("Not only must the positions of each piece on every board be memorised, they must be recalled faithfully when needed, updated with each player's moves, and then reliably stored again, so the brain can move on to the next board.",
         "每块棋盘上每个棋子的位置不仅要记住，还要在需要时准确回想起来，随每位对手的走法而更新，再可靠地重新存好，好让大脑能转到下一块棋盘。",
         "Not only 倒装 + 三重被动并列 + so 结果状语", "Not only 置于句首引起部分倒装（must the positions be memorised）；recalled / updated / stored 三个过去分词构成被动并列；when needed 为省略式状语；so 引导结果状语从句，move on to 意为“转向”。",
         [w("memorise", "v.", "记住；熟记"), w("recall", "v.", "回想；记起"), w("faithfully", "adv.", "如实地；准确地")]),
    33: ("First moves can be tough to remember because they are fairly uninteresting.",
         "开局的头几步往往很难记住，因为它们相当平淡无奇。",
         "主系表 + because 原因状语从句", "主干 First moves can be tough to remember；tough to remember 中不定式作状语（“难以记住”）；because 引导原因；fairly 意为“相当”。",
         [w("tough", "adj.", "困难的；棘手的"), w("uninteresting", "adj.", "乏味的；平淡的")]),
    34: ("But the ends of games are taxing too, as exhaustion sets in.",
         "但对局的收尾阶段同样吃力，因为疲惫开始袭来。",
         "主系表 + as 原因状语从句", "But 转折；主干 the ends are taxing；as 引导原因状语从句；set in 意为“（不好的状态）开始并持续”——本句对应第 32 题“对局最后阶段为何困难”。",
         [w("taxing", "adj.", "费力的；伤脑筋的"), w("set in", "phr.", "（坏天气/状态）开始并持续")]),
    35: ("When Gareyev is tired, his recall can get patchy.",
         "当加列耶夫疲惫时，他的记忆会变得断断续续。",
         "when 时间状语从句 + 系表", "When 引导时间状语从句；主句 his recall can get patchy；get + 形容词表状态变化；patchy 意为“不完整的、时好时坏的”。",
         [w("recall", "n.", "记忆力；回想"), w("patchy", "adj.", "不完整的；参差不齐的")]),
    36: ("He sometimes makes moves based on only a fragmented memory of the pieces' positions.",
         "有时他只凭对棋子位置的零碎记忆来走棋。",
         "主谓宾 + 过去分词短语作状语", "主干 He makes moves；based on... 为过去分词短语作状语（“基于……”）；fragmented 意为“支离破碎的”，呼应上句 patchy。",
         [w("fragmented", "adj.", "支离破碎的；零碎的"), w("make a move", "phr.", "走一步棋")]),

    # ---- Paragraph F (para 6) ----
    37: ("The scientists first had Gareyev perform some standard memory tests.",
         "科学家们首先让加列耶夫做了一些标准的记忆测试。",
         "主谓宾 + 使役动词 have", "have + sb + do 为使役结构（“让某人做”）；first 交代实验顺序；standard memory tests 对应第 37 题的填空答案 memory。",
         [w("have sb do", "phr.", "让某人做某事"), w("standard", "adj.", "标准的；常规的")]),
    38: ("These assessed his ability to hold numbers, pictures and words in mind.",
         "这些测试评估了他把数字、图像和词语记在脑中的能力。",
         "主谓宾 + 不定式定语", "These 指上句的测试；主干 These assessed his ability；to hold... in mind 为不定式作 ability 的定语；hold... in mind 意为“记住”。",
         [w("assess", "v.", "评估；评定"), w("hold in mind", "phr.", "记住；在脑中保持")]),
    39: ("One classic test measures how many numbers a person can repeat, both forwards and backwards, soon after hearing them.",
         "一项经典测试考察的是：一个人在听到一串数字后不久，能正着和倒着复述出多少个。",
         "主谓宾 + 宾语从句", "主干 One test measures how many numbers...；how 引导宾语从句；both forwards and backwards 作方式状语；soon after hearing them 为时间状语——numbers 是第 38 题的填空答案。",
         [w("measure", "v.", "考量；测定"), w("backwards", "adv.", "倒着；逆序地")]),
    40: ("Most people manage about seven.",
         "大多数人能记住大约七个。",
         "主谓宾（省略）", "manage 在此意为“勉强做到、能记住”；about seven 后省略 numbers；短句用于给出常人水平作对比。",
         [w("manage", "v.", "设法做到；勉强完成")]),
    41: ("'He was not exceptional on any of these standard tests,' said Rissman.",
         "“在这些标准测试中，他都算不上出众，”里斯曼说。",
         "直接引语 + 主谓倒装", "引语内主干 He was not exceptional；not... any 构成全否定；said Rissman 为倒装引述。",
         [w("exceptional", "adj.", "异常出色的；卓越的")]),
    42: ("'We didn't find anything other than playing chess that he seems to be supremely gifted at.'",
         "“除了下棋，我们没发现他还有什么特别擅长的天赋。”",
         "宾语从句 + 定语从句", "主干 We didn't find anything；other than 意为“除……之外”；that he seems to be supremely gifted at 是修饰 anything 的定语从句——本句对应第 29 题（其天赋仅限于国际象棋）。",
         [w("other than", "phr.", "除……之外"), w("gifted", "adj.", "有天赋的")]),
    43: ("But next came the brain scans.",
         "但接下来进行的是脑部扫描。",
         "完全倒装", "为使句子连贯，地点/时间状语 next 提前引发完全倒装（came the brain scans = the brain scans came next）；起转入下一实验的过渡作用。",
         [w("brain scan", "n.", "脑部扫描")]),
    44: ("With Gareyev lying down in the machine, Rissman looked at how well connected the various regions of the chess player's brain were.",
         "在加列耶夫躺进仪器后，里斯曼观察了这位棋手大脑各区域之间的连接紧密程度。",
         "with 独立主格 + 宾语从句", "With + 名词 + 现在分词 为独立主格作状语（“在……的情况下”）；how well connected... were 为宾语从句（含系表倒装）；look at 意为“考察”。",
         [w("independent structure", "phr.", "（语法）独立主格"), w("region", "n.", "区域；部位")]),
    45: ("Though the results are tentative and as yet unpublished, the scans found much greater than average communication between parts of Gareyev's brain that make up what is called the frontoparietal control network.",
         "尽管结果还只是初步的、尚未发表，但扫描发现，加列耶夫大脑中构成所谓“额顶控制网络”的各部分之间，其信息交流远高于常人平均水平。",
         "Though 让步从句 + 定语从句 + 名词性从句", "Though 引导让步从句；主句 the scans found... communication；that make up... 为定语从句修饰 parts；what is called... 为名词性从句作 make up 的宾语——communication 是第 39 题填空答案。",
         [w("tentative", "adj.", "初步的；不确定的"), w("communication", "n.", "（脑区间的）信息交流；连通")]),
    46: ("Of 63 people scanned alongside the chess player, only one or two scored more highly on the measure.",
         "在与这位棋手一同接受扫描的 63 人中，只有一两个人在该指标上得分更高。",
         "介词短语前置 + 比较级", "Of 63 people... 前置作范围状语；scanned alongside... 为过去分词定语修饰 people；scored more highly 用比较级凸显其罕见程度。",
         [w("alongside", "prep.", "与……一起；在……旁"), w("measure", "n.", "衡量指标；量度")]),

    # ---- Paragraph F continued (last two are the Rissman quote, still para F) ----
    47: ("'You use this network in almost any complex task.",
         "“几乎任何复杂的任务你都会用到这个网络。",
         "主谓宾 + 范围状语", "主干 You use this network；in almost any complex task 作范围状语；this network 指上文的额顶控制网络。",
         [w("complex", "adj.", "复杂的"), w("network", "n.", "（大脑的）网络")]),
    48: ("It helps you to allocate attention, keep rules in mind, and work out whether you should be responding or not,' said Rissman.",
         "它能帮你分配注意力、记住规则，并判断自己该不该做出反应，”里斯曼说。",
         "help sb do + 三重不定式并列", "help + sb + (to) do 结构；allocate、keep、work out 三个动词并列作宾补；whether... or not 为 work out 的宾语从句。",
         [w("allocate", "v.", "分配"), w("work out", "phr.", "弄清；想明白")]),

    # ---- Paragraph G (para 7) ----
    49: ("It was not the only hint of something special in Gareyev's brain.",
         "这并非加列耶夫大脑中不同寻常之处的唯一迹象。",
         "主系表 + 双重否定语气", "主干 It was not the only hint；not the only 暗示“还有其他迹象”，起承上启下作用；It 指上段的额顶网络发现。",
         [w("hint", "n.", "迹象；暗示"), w("something special", "phr.", "不同寻常之处")]),
    50: ("The scans also suggest that Gareyev's visual network is more highly connected to other brain parts than usual.",
         "扫描还显示，加列耶夫的视觉网络与大脑其他部位的连接比常人更为紧密。",
         "主谓宾 + that 宾语从句 + 比较级", "主干 The scans suggest that...；that 引导宾语从句；more... than usual 为比较级（“比通常更……”）——visual 是第 40 题填空答案。",
         [w("suggest", "v.", "表明；暗示"), w("visual", "adj.", "视觉的")]),
    51: ("Initial results suggest that the areas of his brain that process visual images - such as chess boards - may have stronger links to other brain regions, and so be more powerful than normal.",
         "初步结果表明，他大脑中处理视觉图像（例如棋盘）的区域，与其他脑区的联系可能更强，因而其功能也比常人更强大。",
         "宾语从句 + 定语从句 + 破折号插入 + and so 结果", "主干 Initial results suggest that...；that process visual images 为定语从句修饰 areas；破折号内 such as chess boards 为举例插入；may have... and so be... 由 and 并列，so 表结果。",
         [w("process", "v.", "处理；加工"), w("link", "n.", "联系；连接")]),
    52: ("While the analyses are not finalised yet, they may hold the first clues to Gareyev's extraordinary ability.",
         "尽管分析尚未定论，但它们或许握有揭示加列耶夫非凡能力的最初线索。",
         "While 让步从句 + 主谓宾", "While 引导让步状语从句（“尽管”）；主句 they may hold the first clues；clues to sth 意为“通向……的线索”；finalise 意为“最终定稿/敲定”。",
         [w("finalise", "v.", "最终确定；敲定"), w("clue", "n.", "线索")]),

    # ---- Paragraph H (para 8) ----
    53: ("For the world record attempt, Gareyev hopes to play 47 blindfold games at once in about 16 hours.",
         "为了冲击世界纪录，加列耶夫希望在约 16 小时内同时下 47 盘盲棋。",
         "目的状语 + hope to do", "For... attempt 作目的状语；主干 Gareyev hopes to play 47 games；at once、blindfold games 呼应全文主题。",
         [w("attempt", "n.", "尝试；（破纪录的）挑战"), w("blindfold", "adj.", "蒙眼的")]),
    54: ("He will need to win 80% to claim the title.",
         "他需要赢下八成的对局才能夺得这一头衔。",
         "主谓 + 不定式表目的", "主干 He will need to win 80%；to claim the title 为不定式表目的；claim the title 意为“夺得冠军头衔”。",
         [w("claim", "v.", "夺得；赢得（头衔）"), w("title", "n.", "冠军头衔")]),
    55: ("'I don't worry too much about the winning percentage, that's never been an issue for me,' he said.",
         "“我不太在意胜率，那对我从来都不是问题，”他说。",
         "直接引语 + 并列分句", "两个分句用逗号并列；worry about 意为“担心”；that's never been an issue 为现在完成时强调“一直以来都不是”。",
         [w("winning percentage", "n.", "胜率"), w("issue", "n.", "问题；麻烦事")]),
    56: ("'The most important part of blindfold chess for me is that I have found the one thing that I can fully dedicate myself to.",
         "“对我而言，盲棋最重要的意义在于：我找到了唯一一件可以全身心投入的事。",
         "主系表 + 表语从句 + 定语从句", "主干 The most important part... is that...；that I have found... 为表语从句；that I can fully dedicate myself to 为定语从句修饰 the one thing——本句概述他的人生优先事项，对应第 31 题。",
         [w("dedicate oneself to", "phr.", "全身心投入于"), w("fully", "adv.", "完全地；充分地")]),
    57: ("I miss having an obsession.'",
         "我一直渴望有一件让自己痴迷的事。”",
         "主谓宾 + 动名词宾语", "miss doing 在此意为“怀念/渴望（拥有）”；having an obsession 为动名词短语作宾语；obsession 呼应前文的 obsessed。",
         [w("miss", "v.", "怀念；因缺少而渴望"), w("obsession", "n.", "痴迷；着迷的事物")]),
}


# A..H -> para 1..8, in id order
PARA_SIZES = [
    (1, 1, 10),   # A
    (2, 11, 16),  # B
    (3, 17, 21),  # C
    (4, 22, 25),  # D
    (5, 26, 36),  # E
    (6, 37, 48),  # F
    (7, 49, 52),  # G
    (8, 53, 57),  # H
]


def para_of(sid: int) -> int:
    for para, lo, hi in PARA_SIZES:
        if lo <= sid <= hi:
            return para
    raise ValueError(f"no para for id {sid}")


LSQUO = "‘"  # '
RSQUO = "’"  # '


def curly(en: str) -> str:
    """Match Test 1's curly-quote style (PDF uses curly quotes throughout).

    All apostrophes/single quotes in the source are ASCII "'". A "'" that opens
    a dialogue turn (start of string, or after a space) becomes an opening quote
    "‘"; every other "'" (contractions, possessives, closing quote) becomes
    "’".
    """
    out = []
    for i, ch in enumerate(en):
        if ch == "'":
            prev = en[i - 1] if i > 0 else ""
            out.append(LSQUO if (prev == "" or prev == " ") else RSQUO)
        else:
            out.append(ch)
    return "".join(out)


# New evidence_sentence targets (remapped to the rebuilt 57-sentence ids)
EVIDENCE = {
    27: 23,  # D2: displays of the feat go back centuries
    28: 27,  # E2: nature of the game...
    29: 42,  # F6: we didn't find anything other than playing chess...
    30: 11,  # B1: prowess has drawn interest from beyond the chess-playing community
    31: 56,  # H4: most important part... one thing I can dedicate myself to
    32: 34,  # E9: ends of games are taxing too
    33: 3,   # A3: challengers play as normal, Gareyev blindfolded
    34: 6,   # A6: gets his kicks from BASE jumping
    35: 12,  # B2: UCLA called him in for tests
    36: 14,  # B4: ability to play with eyes closed not a far reach
    37: 37,  # F1: standard memory tests
    38: 39,  # F3: how many numbers a person can repeat
    39: 45,  # F9: communication ... frontoparietal control network
    40: 50,  # G2: visual network more highly connected
}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))

    assert set(S.keys()) == set(range(1, 58)), "S must cover ids 1..57"

    data["quality"] = "teacher_refined"
    data["phrases"] = PHRASES

    sentences = []
    for sid in range(1, 58):
        en, zh, gtype, note, words = S[sid]
        sentences.append({
            "id": sid,
            "para": para_of(sid),
            "en": curly(en),
            "zh": zh,
            "grammar": {"type": gtype, "note": note},
            "words": words,
        })
    data["sentences"] = sentences

    for q in data["questions"]:
        for it in q.get("items", []):
            num = it.get("number")
            if num in EVIDENCE:
                it["evidence_sentence"] = EVIDENCE[num]

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    for row in idx.get("passages", []):
        if row.get("id") == data["id"]:
            row["quality"] = "teacher_refined"
            row["sentence_count"] = len(sentences)
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"refined {PATH} -> {len(sentences)} sentences")


if __name__ == "__main__":
    main()
