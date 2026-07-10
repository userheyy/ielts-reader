# -*- coding: utf-8 -*-
"""为词库里已有的词补「高频搭配 collocations」。

给 data/vocab-seed.json 里还没有 collocations 字段的词,交给 LLM 产出 2~4 条地道高频搭配
(英文词块 + 中文),校验后:
  - 样品模式(默认):写到 tools/out/colloc_sample.json,不动主库,供人工验质。
  - 全量模式(--apply):把 collocations 字段合并进 data/vocab-seed.json(每 N 批周期落盘)。

用法:
    py -3 tools/gen_collocations.py --n 8               # 样品:前 8 个缺搭配的词
    py -3 tools/gen_collocations.py --apply --batch 8   # 全量:所有缺搭配的词并入主库
    py -3 tools/gen_collocations.py --provider qwen      # 用 Qwen 而非 DeepSeek

需要 tools/config.local.json 的 api_key(DeepSeek)或 dashscope_key(Qwen)。
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
OUT_DIR = os.path.join(HERE, "out")

SYSTEM_PROMPT = """你是资深雅思写作/口语老师,为中国考生整理单词的高频「搭配(collocation)」。
给你一批单词(含词性和中文释义),为每个词产出 2~4 条最高频、最地道、雅思考试用得上的搭配。

严格要求:
1. 只输出 JSON:{"items":[{"word":"...","collocations":[{"en":"...","zh":"..."}]}]},不要多余文字。
2. 每条 en 是包含该词的自然词块(动词+名词、形容词+名词、介词短语等),尽量短(2~4 词),真实高频。
3. zh 是该词块的简短中文。
4. 顺序与输入一致;每个词 2~4 条;个别功能词实在没有典型搭配,给 1 条即可,不要硬凑假搭配。
5. 优先学术/通用高频搭配,贴合雅思读写听说语境。

范例:
{"items":[
 {"word":"decision","collocations":[{"en":"make a decision","zh":"做决定"},{"en":"a difficult decision","zh":"艰难的决定"},{"en":"reach a decision","zh":"作出决定"}]},
 {"word":"research","collocations":[{"en":"conduct research","zh":"开展研究"},{"en":"research shows that","zh":"研究表明"},{"en":"carry out research","zh":"进行研究"}]}
]}"""


def load_json(path, fallback):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return fallback


def save_seed(seed):
    with open(SEED, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)


def make_client(provider):
    if provider == "qwen":
        from qwen_client import QwenClient
        return QwenClient(temperature=0.4)
    from deepseek_client import DeepSeekClient
    return DeepSeekClient(temperature=0.4)


def validate(item):
    if not item.get("word"):
        return ["缺 word"]
    cols = item.get("collocations")
    if not isinstance(cols, list) or not cols:
        return ["collocations 空"]
    for c in cols:
        if not isinstance(c, dict) or not c.get("en") or not c.get("zh"):
            return ["搭配缺 en/zh"]
    return []


def gen_batch(client, batch):
    lines = [f'{i+1}. {w["word"]} ({w.get("pos","")}) 义: {w.get("def","")}'
             for i, w in enumerate(batch)]
    user = "为下面这些词各产出 2~4 条高频搭配:\n" + "\n".join(lines)
    obj, _usage = client.chat_json(
        [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user}],
        max_tokens=3000,
    )
    items = obj.get("items") if isinstance(obj, dict) else obj
    return items if isinstance(items, list) else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8, help="样品模式生成多少词")
    ap.add_argument("--batch", type=int, default=8, help="每次 API 请求几个词")
    ap.add_argument("--provider", choices=["deepseek", "qwen"], default="deepseek")
    ap.add_argument("--apply", action="store_true", help="并入主库(否则只写样品)")
    ap.add_argument("--out", default=os.path.join(OUT_DIR, "colloc_sample.json"))
    args = ap.parse_args()

    seed = load_json(SEED, {"words": []})
    words = seed.get("words", [])
    targets = [w for w in words if not w.get("collocations")]
    if not args.apply:
        targets = targets[:args.n]
    if not targets:
        print("所有词都已有 collocations。")
        return
    print(f"待补搭配 {len(targets)} 词" + ("(全量并库)" if args.apply else f"(样品前 {args.n})"))

    client = make_client(args.provider)
    by_word = {w["word"].lower(): w for w in words}
    done, flagged = 0, []
    nbatches = (len(targets) + args.batch - 1) // args.batch
    for i in range(0, len(targets), args.batch):
        batch = targets[i:i + args.batch]
        bi = i // args.batch + 1
        try:
            items = gen_batch(client, batch)
        except SystemExit as e:
            print("  API 出错,停止:", e)
            break
        except Exception as e:  # 单批失败不致命,跳过继续
            print(f"  批 {bi} 异常,跳过: {e}")
            continue
        for it in items:
            probs = validate(it)
            if probs:
                flagged.append((it.get("word"), probs))
                continue
            tgt = by_word.get((it.get("word") or "").lower())
            if tgt is not None:
                tgt["collocations"] = it["collocations"]
                done += 1
        print(f"  批 {bi}/{nbatches}: 累计补 {done} 词")
        if args.apply and bi % 20 == 0:
            save_seed(seed)  # 周期落盘,防中断丢进度

    if args.apply:
        save_seed(seed)
        print(f"✓ 已并入主库 data/vocab-seed.json,共补 {done} 词")
    else:
        os.makedirs(OUT_DIR, exist_ok=True)
        sample = [{"word": w["word"], "pos": w.get("pos"), "def": w.get("def"),
                   "collocations": w.get("collocations")}
                  for w in targets if w.get("collocations")]
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump({"generated": len(sample), "items": sample}, f, ensure_ascii=False, indent=2)
        print(f"✓ 样品 {len(sample)} 词 → {args.out}(未动主库)")
    if flagged:
        print(f"⚠ {len(flagged)} 词有问题(未写入):", flagged[:8])
    if hasattr(client, "report"):
        print(client.report())
    prev = next((w for w in targets if w.get("collocations")), None)
    if prev:
        print("\n—— 样品预览 ——\n" + json.dumps(
            {"word": prev["word"], "collocations": prev["collocations"]},
            ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
