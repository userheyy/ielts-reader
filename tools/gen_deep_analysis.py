# -*- coding: utf-8 -*-
"""批量生成句子深度解析(deep 字段) — DeepSeek 管线。

用法:
    py tools/gen_deep_analysis.py c14-test1-p1              # 全部缺 deep 的句子
    py tools/gen_deep_analysis.py c14-test1-p1 --only 3,5   # 只跑指定句
    py tools/gen_deep_analysis.py c14-test1-p1 --resume     # 跳过 out 里已有的句
    py tools/gen_deep_analysis.py c14-test1-p1 --force      # 已有 deep 的句也重生成

流程:每句一请求(带前句上下文)→ 本地结构校验(失败带错误重试一次)→
     逐句落盘 tools/out/{id}.deep.json → 人工抽查 → merge_deep.py 合并。
few-shot 样例取自 data/passages/c14-test1-p1.json 句1(需先完成手工样例)。
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deepseek_client import DeepSeekClient  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "tools" / "out"

PATTERN_IDS = {"sv", "svc", "svo", "svoo", "svoc"}
ROLES = {"S", "V", "O", "IO", "C", "attr", "adv", "app", "conn", "clause"}
MORPH_TYPES = {"prefix", "root", "suffix", "connector"}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_tags():
    tags = load_json(ROOT / "data" / "grammar-tags.json")["tags"]
    return {t["id"]: t for t in tags}


def build_system_prompt(tags, fewshot_sentence):
    tag_lines = "\n".join(
        f"- {t['id']}:{t['name']} — {t['brief']}" for t in tags.values())
    fewshot = json.dumps(fewshot_sentence["deep"], ensure_ascii=False, indent=1)
    return f"""你是一名给雅思 4.5-5.5 分、语法基础薄弱的中国学生讲课的英语老师。你的任务:对给定的雅思阅读句子输出结构化深度解析 JSON(deep 对象)。

# 分析框架(《语法俱乐部》体系,必须按此顺序思考)
1) 先判定五大基本句型之一:S+V / S+V+C / S+V+O / S+V+O+O / S+V+O+C(pattern.id 对应 sv/svc/svo/svoo/svoc,以最外层主句为准);
2) 再识别名词词组、修饰语(形容词/副词/介词短语)、时态;
3) 再识别中级句型:合句、名词从句、副词从句、关系从句;
4) 最后识别从句减化:分词、不定词、动名词、同位语都按"从句减化"理解。

# 可用语法标签(白名单,禁止发明新标签;tag 字段只能从下面选)
{tag_lines}

# 输出 JSON 结构(只输出这一个 JSON 对象,不要包裹在其它字段里)
{{
 "pattern": {{"id":"五大句型之一","label":"如 S + Vt + O(主语+及物动词+宾语)","tag":"ch1.*",
   "skeleton":[{{"role":"S|V|O|IO|C","text":"英文","zh":"中文"}}...],
   "plain":"一句大白话:去掉修饰后这句只剩什么"}},
 "chunks": [{{"text":"原句成分块(按顺序线性覆盖整句)","role":"S|V|O|IO|C|attr|adv|app|conn|clause","zh":"中文","note":"讲解(可空串)","tag":"可选,白名单内"}}...],
 "grammar_points": [{{"tag":"白名单内","name":"语法点名","explain":"3-6 句大白话讲透,像面对面上课"}}...],
 "vocab": [{{"w":"原文词形","lemma":"原形","pos":"n./v./adj./adv./phr.","def":"中文释义",
   "aids":{{"morphemes":[{{"text":"词素","type":"prefix|root|suffix|connector","gloss":"含义"}}],
     "derivation":"拆解推导一句话(无则空串)",
     "family":{{"root":"词根","gloss":"含义","words":[{{"word":"同根词","def":"释义"}}]}} 或 null,
     "mnemonic":"联想记忆一句话(无则空串)","forms":[{{"word":"派生词形","pos":"...","def":"..."}}]}},
   "synonyms":[{{"w":"同义词","note":"雅思何种场景会用它替换"}}],
   "confusables":[{{"w":"形近/易混词","note":"区别"}}]}}...],
 "expressions": [{{"text":"值得积累的表达/搭配","zh":"中文","usage":"怎么迁移使用(写作/口语)"}}...]
}}

# 写作要求
- 全中文讲解,大白话,像老师面对面上课;术语第一次出现要用括号解释(例:宾语(动作的对象));
- explain/note 必须是你自己的原创讲解,禁止引用任何书籍原文;
- chunks 必须按原句顺序、尽量完整覆盖整句(≥90% 的文字要落在某个块里);
- vocab 只挑 2-4 个"雅思考点词"(太简单的 the/is 不要);morphemes 拆解要词源准确,拆不了的单词素词就一个 root;
- synonyms 优先给雅思阅读/听力真实会考的同义替换,note 说明场景;每个考点词至少 1 个 synonym;
- grammar_points 1-3 个,选本句最值得学的;tag 必须在白名单内;
- expressions 0-2 个,没有就给空数组。

# 完整示例(对句 "{fewshot_sentence['en']}" 的标准输出)
{fewshot}"""


def build_user_prompt(sentence, prev_sentence):
    ctx = ""
    if prev_sentence is not None:
        ctx = f"【上一句(仅供理解指代,不要分析它)】{prev_sentence['en']}\n"
    words = json.dumps(sentence.get("words", []), ensure_ascii=False)
    return f"""{ctx}【本句】{sentence['en']}
【已有中文翻译】{sentence['zh']}
【已有语法简注】{sentence.get('grammar', {}).get('type', '')} — {sentence.get('grammar', {}).get('note', '')}
【已有生词】{words}

请对【本句】输出 deep JSON。"""


def validate_deep(deep, sentence, tag_ids):
    """本地结构校验,返回错误列表(空=通过)。"""
    errs = []
    if not isinstance(deep, dict):
        return ["deep 不是对象"]

    p = deep.get("pattern")
    if not isinstance(p, dict):
        errs.append("缺 pattern")
    else:
        if p.get("id") not in PATTERN_IDS:
            errs.append(f"pattern.id 非法: {p.get('id')!r}(应为 {sorted(PATTERN_IDS)})")
        if p.get("tag") and p["tag"] not in tag_ids:
            errs.append(f"pattern.tag 不在白名单: {p['tag']}")
        sk = p.get("skeleton")
        if not isinstance(sk, list) or not sk:
            errs.append("pattern.skeleton 缺失或为空")
        else:
            for it in sk:
                if it.get("role") not in ROLES:
                    errs.append(f"skeleton role 非法: {it.get('role')!r}")
        if not p.get("plain"):
            errs.append("pattern.plain 缺失")

    chunks = deep.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        errs.append("chunks 缺失或为空")
    else:
        covered = sum(len(c.get("text", "")) for c in chunks)
        ratio = covered / max(1, len(sentence["en"]))
        if ratio < 0.6:
            errs.append(f"chunks 覆盖率过低 {ratio:.0%}(应≥90%,至少 60%)")
        for c in chunks:
            if c.get("role") not in ROLES:
                errs.append(f"chunk role 非法: {c.get('role')!r}({c.get('text','')[:20]})")
            if c.get("tag") and c["tag"] not in tag_ids:
                errs.append(f"chunk tag 不在白名单: {c['tag']}")

    gps = deep.get("grammar_points")
    if not isinstance(gps, list) or not gps:
        errs.append("grammar_points 缺失或为空")
    else:
        for g in gps:
            if g.get("tag") not in tag_ids:
                errs.append(f"grammar_point tag 不在白名单: {g.get('tag')!r}")
            if not g.get("explain") or len(g.get("explain", "")) < 20:
                errs.append(f"grammar_point explain 太短: {g.get('name')}")

    vocab = deep.get("vocab")
    if not isinstance(vocab, list):
        errs.append("vocab 缺失")
    else:
        for v in vocab:
            if not v.get("w") or not v.get("def"):
                errs.append(f"vocab 缺 w/def: {v}")
            aids = v.get("aids") or {}
            for m in (aids.get("morphemes") or []):
                if m.get("type") not in MORPH_TYPES:
                    errs.append(f"morpheme type 非法: {m.get('type')!r}({v.get('w')})")

    if not isinstance(deep.get("expressions", []), list):
        errs.append("expressions 应为数组")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("passage_id")
    ap.add_argument("--only", help="只处理这些句 id,逗号分隔")
    ap.add_argument("--resume", action="store_true", help="跳过 out 中已有的句")
    ap.add_argument("--force", action="store_true", help="已有 deep 的句也重生成")
    args = ap.parse_args()

    passage_path = ROOT / "data" / "passages" / f"{args.passage_id}.json"
    passage = load_json(passage_path)
    tags = load_tags()

    # few-shot:c14-test1-p1 句 1 的手工样例
    fewshot_src = load_json(ROOT / "data" / "passages" / "c14-test1-p1.json")
    fewshot_sentence = next(
        (s for s in fewshot_src["sentences"] if s.get("deep")), None)
    if fewshot_sentence is None:
        raise SystemExit("few-shot 样例缺失:请先完成 c14-test1-p1 句1-3 的手工 deep 样例")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{args.passage_id}.deep.json"
    out = {"passage_id": args.passage_id, "sentences": {}}
    if out_path.exists():
        out = load_json(out_path)

    only = set(int(x) for x in args.only.split(",")) if args.only else None
    todo = []
    for s in passage["sentences"]:
        if only and s["id"] not in only:
            continue
        if s.get("deep") and not args.force:
            continue
        if args.resume and str(s["id"]) in out["sentences"]:
            continue
        todo.append(s)

    if not todo:
        print("没有需要处理的句子(可用 --force / --only 调整)")
        return

    system_prompt = build_system_prompt(tags, fewshot_sentence)
    client = DeepSeekClient()
    print(f"{args.passage_id}: 待生成 {len(todo)} 句 → {out_path}")

    id2sentence = {s["id"]: s for s in passage["sentences"]}
    fails = []
    for i, s in enumerate(todo, 1):
        prev = id2sentence.get(s["id"] - 1)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": build_user_prompt(s, prev)},
        ]
        print(f"[{i}/{len(todo)}] 句{s['id']}: {s['en'][:60]}…")
        deep, _ = client.chat_json(messages, max_tokens=4096)
        errs = validate_deep(deep, s, set(tags))
        if errs:
            print(f"  校验失败({len(errs)}),带错误重试一次: {errs[:3]}")
            retry = messages + [
                {"role": "assistant", "content": json.dumps(deep, ensure_ascii=False)},
                {"role": "user", "content": "你的输出未通过校验:\n- " + "\n- ".join(errs)
                 + "\n请修正后重新输出完整 deep JSON。"},
            ]
            deep, _ = client.chat_json(retry, max_tokens=4096)
            errs = validate_deep(deep, s, set(tags))
        if errs:
            print(f"  仍未通过,记入 errors: {errs}")
            fails.append((s["id"], errs))
        else:
            out["sentences"][str(s["id"])] = deep
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=1)

    if fails:
        err_path = OUT_DIR / f"{args.passage_id}.errors.txt"
        with open(err_path, "w", encoding="utf-8") as f:
            for sid, errs in fails:
                f.write(f"句{sid}:\n" + "\n".join("  - " + e for e in errs) + "\n")
        print(f"[!] {len(fails)} 句未通过校验 → {err_path}")
    print(f"完成:成功 {len(out['sentences'])} 句,失败 {len(fails)} 句")
    print(client.report())


if __name__ == "__main__":
    main()
