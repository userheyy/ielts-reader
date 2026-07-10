# -*- coding: utf-8 -*-
"""词库扩充生成器(样品版)。

把 seed_wordlist.json 里"还没生成记忆法"的高频词,交给 LLM 按 vocab-seed.json 的
既定 schema + 质量标准生成 aids(词根词缀 + 联想 + 例句),校验后写到 tools/out/seed_sample.json。

这是"样品"脚本:默认只生成一小批(N 词)供人工验质,不动主词库 data/vocab-seed.json。
验质满意后,可把 --out 指到主库并加大 N 分批跑(见 README 注释)。

用法:
    py -3 tools/gen_seed_sample.py --n 8            # 生成 8 个词的样品
    py -3 tools/gen_seed_sample.py --n 40 --batch 5 # 40 词,每次 API 请求 5 词
    py -3 tools/gen_seed_sample.py --provider qwen   # 用 Qwen(dashscope)而非 DeepSeek

需要 tools/config.local.json 里的 api_key(DeepSeek)或 dashscope_key(Qwen)。
"""
import argparse
import io
import json
import os
import sys

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(HERE, "..", "data", "vocab-seed.json")
WORDLIST = os.path.join(HERE, "seed_wordlist.json")
OUT_DIR = os.path.join(HERE, "out")

# ---- 生成的 JSON schema(与 vocab-seed.json 逐字段对齐)+ 一个 few-shot 范例 ----
SYSTEM_PROMPT = """你是资深雅思词汇讲师,为中国考生做"词根词缀 + 联想助记"的单词卡。
给你一批英文单词(含音标和粗略中文释义参考),为每个词产出一个 JSON 对象,字段与示例完全一致。

严格要求:
1. 只输出一个 JSON 对象 {"words": [ ... ]},words 是数组,顺序与输入一致,不要多余文字。
2. def:2~4 个最核心的中文释义,逗号分隔,别抄词典长条目。
3. pos:词性缩写(n./v./adj./adv./prep. 等),多词性用斜杠,如 "v./n."。
4. cefr:该词的欧标级别,雅思核心词多为 A2/B1/B2,少数 C1。
5. sentence_en:一句简单地道的例句(含该词),sentence_zh 是对应中文翻译。
6. aids.morphemes:词素数组,每个 {text, type, gloss};type 取 prefix/root/suffix/connector。
   词根要真实(拉丁/希腊来源);若确无明确词根,就把整词作为一个 root 并如实注明来源
   (如"古英语/古法语 xxx"),不要编造假词根。
7. aids.derivation:一句"词素相加 → 推导 → 词义"的白话链条。
8. aids.family:同根词族 {root, gloss, words:[{word, def}]},给 2~4 个同族词。
9. aids.mnemonic:一段生动、准确、便于记忆的中文联想(可含常见搭配、派生词提示)。
10. aids.forms:该词的常见派生/变形 [{word, pos, def}],给 1~3 个;没有就给 []。

范例(输出格式以此为准):
{"words":[{
  "word":"restrict","phonetic":"rɪˈstrɪkt","pos":"v.","def":"限制，限定，约束","cefr":"B2","freq_rank":3539,
  "sentence_en":"The new law restricts the sale of alcohol.","sentence_zh":"这项新法律限制了酒类的销售。",
  "aids":{"morphemes":[{"text":"re","type":"prefix","gloss":"回，向后"},{"text":"strict","type":"root","gloss":"拉紧，捆"}],
    "derivation":"re(向后)+strict(拉紧) → 往回拉紧、勒住 → 限制",
    "family":{"root":"strict/string","gloss":"拉紧、捆","words":[{"word":"restriction","def":"限制"},{"word":"strict","def":"严格的"},{"word":"strain","def":"拉紧；压力"}]},
    "mnemonic":"strict=拉紧(和 strict 严格一家);把范围往回勒紧,就是 restrict 限制;restriction 限制;be restricted to 仅限于。",
    "forms":[{"word":"restriction","pos":"n.","def":"限制"},{"word":"restricted","pos":"adj.","def":"受限制的"}]}}]}"""

REQUIRED = ["word", "pos", "def", "cefr", "sentence_en", "sentence_zh", "aids"]
AID_REQUIRED = ["morphemes", "derivation", "family", "mnemonic", "forms"]


def load_json(path, fallback):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return fallback


def clean_translation(t):
    # ECDICT translation 用 \n 分行、含词性标注,取前 40 字做提示即可
    return (t or "").replace("\\n", "；").replace("\n", "；")[:60]


def pick_targets(n):
    seed = load_json(SEED, {"words": []})
    have = {w["word"].lower() for w in seed.get("words", [])}
    wl = load_json(WORDLIST, [])
    wl = sorted(wl, key=lambda x: x.get("freq_rank", 1e9))
    out = []
    for w in wl:
        word = (w.get("word") or "").strip()
        if not word or word.lower() in have:
            continue
        out.append(w)
        if len(out) >= n:
            break
    return out


def make_client(provider):
    if provider == "qwen":
        from qwen_client import QwenClient  # noqa
        return QwenClient(temperature=0.4)
    from deepseek_client import DeepSeekClient
    return DeepSeekClient(temperature=0.4)


def validate(word_obj):
    problems = []
    for k in REQUIRED:
        if not word_obj.get(k):
            problems.append(f"缺 {k}")
    aids = word_obj.get("aids") or {}
    for k in AID_REQUIRED:
        if k not in aids:
            problems.append(f"缺 aids.{k}")
    if not isinstance(aids.get("morphemes"), list) or not aids.get("morphemes"):
        problems.append("morphemes 空")
    fam = aids.get("family") or {}
    if not fam.get("words"):
        problems.append("family.words 空")
    return problems


def gen_batch(client, batch):
    hint_lines = [
        f'{i+1}. {w["word"]}  /{w.get("phonetic","")}/  参考义: {clean_translation(w.get("translation"))}'
        for i, w in enumerate(batch)
    ]
    user = "为下面这些词生成卡片(freq_rank 用我给的值):\n" + "\n".join(hint_lines)
    obj, usage = client.chat_json(
        [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user}],
        max_tokens=4096,
    )
    words = obj.get("words") if isinstance(obj, dict) else obj
    if not isinstance(words, list):
        return []
    # 回填权威字段(音标、freq_rank 用词表原值,避免 LLM 记错)
    by_word = {w["word"].lower(): w for w in batch}
    for wd in words:
        src = by_word.get((wd.get("word") or "").lower())
        if src:
            wd["phonetic"] = src.get("phonetic", wd.get("phonetic", ""))
            wd["freq_rank"] = src.get("freq_rank", wd.get("freq_rank"))
    return words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8, help="生成多少个词(样品默认 8)")
    ap.add_argument("--batch", type=int, default=4, help="每次 API 请求几个词")
    ap.add_argument("--provider", choices=["deepseek", "qwen"], default="deepseek")
    ap.add_argument("--out", default=os.path.join(OUT_DIR, "seed_sample.json"))
    args = ap.parse_args()

    targets = pick_targets(args.n)
    if not targets:
        print("没有待生成的词(词库可能已覆盖 seed_wordlist 全部)。")
        return
    print(f"待生成 {len(targets)} 词(freq 最高的未收录词): "
          + ", ".join(t["word"] for t in targets))

    client = make_client(args.provider)
    produced, flagged = [], []
    for i in range(0, len(targets), args.batch):
        batch = targets[i:i + args.batch]
        print(f"  → 生成第 {i//args.batch + 1} 批 ({len(batch)} 词)…")
        try:
            words = gen_batch(client, batch)
        except SystemExit as e:
            print("  API 出错,停止:", e)
            break
        for wd in words:
            probs = validate(wd)
            (flagged if probs else produced).append((wd, probs))

    os.makedirs(OUT_DIR, exist_ok=True)
    ok_words = [w for w, _ in produced]
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"generated": len(ok_words), "words": ok_words}, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 通过校验 {len(ok_words)} 词,写入 {args.out}")
    if flagged:
        print(f"⚠ {len(flagged)} 词有问题(未写入):")
        for wd, probs in flagged:
            print(f"   - {wd.get('word')}: {', '.join(probs)}")
    if hasattr(client, "report"):
        print(client.report())

    # 预览第一个词,便于肉眼验质
    if ok_words:
        print("\n—— 样品预览(第一个词)——")
        print(json.dumps(ok_words[0], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
