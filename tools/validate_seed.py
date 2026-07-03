#!/usr/bin/env python
# 校验 data/vocab-seed.json:字段完整、类型正确、无重复 word、morphemes.type 合法。
# 用法: python tools/validate_seed.py
import json, sys, os, io
# Windows 终端默认 GBK,强制 stdout 用 UTF-8,避免 emoji/中文报 UnicodeEncodeError
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(HERE, "..", "data", "vocab-seed.json")

VALID_TYPES = {"prefix", "root", "suffix", "connector"}
errors = []
warns = []

def err(msg): errors.append(msg)
def warn(msg): warns.append(msg)

with open(SEED, encoding="utf-8") as f:
    data = json.load(f)

if "meta" not in data or "words" not in data:
    err("顶层缺 meta 或 words")
    print("FAIL"); sys.exit(1)

meta = data["meta"]
words = data["words"]
seen = set()

for i, w in enumerate(words):
    tag = f"[{i}] {w.get('word','<no word>')}"
    for k in ("word", "def"):
        if not w.get(k):
            err(f"{tag}: 缺必填字段 {k}")
    wl = (w.get("word") or "").lower()
    if wl in seen:
        err(f"{tag}: 重复单词")
    seen.add(wl)

    aids = w.get("aids")
    if aids is None:
        warn(f"{tag}: 无 aids(允许,但内置词应尽量带)")
        continue
    # morphemes
    for m in aids.get("morphemes", []) or []:
        if not m.get("text"):
            err(f"{tag}: morpheme 缺 text")
        if m.get("type") not in VALID_TYPES:
            err(f"{tag}: morpheme.type 非法: {m.get('type')}")
    # family
    fam = aids.get("family")
    if fam:
        if not isinstance(fam.get("words", []), list):
            err(f"{tag}: family.words 必须是数组")
        for fw in fam.get("words", []) or []:
            if not fw.get("word"):
                err(f"{tag}: family 词缺 word")
    # forms
    for fm in aids.get("forms", []) or []:
        if not fm.get("word"):
            err(f"{tag}: form 缺 word")
    # 至少要有一种记忆法内容,否则内置词的 aids 是空壳
    has_any = (
        (aids.get("morphemes")) or (aids.get("derivation") or "").strip()
        or (fam and fam.get("words")) or (aids.get("mnemonic") or "").strip()
        or (aids.get("forms"))
    )
    if not has_any:
        warn(f"{tag}: aids 存在但无任何内容")

print(f"词数: {len(words)}  (meta.total_target={meta.get('total_target')}, generated_batches={meta.get('generated_batches')})")
if warns:
    print(f"\n⚠️  {len(warns)} 条提示:")
    for m in warns[:20]: print("  -", m)
if errors:
    print(f"\n❌ {len(errors)} 条错误:")
    for m in errors: print("  -", m)
    print("\nFAIL"); sys.exit(1)
print("\n✅ 全部校验通过")
