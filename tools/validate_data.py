"""校验 data/index.json 与所有 data/passages/*.json 的结构完整性。
运行: python tools/validate_data.py
无错误则打印 OK 并以 0 退出;有问题打印每条错误并以 1 退出。
"""
import json, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []

# ---- Schema v2: deep / paraphrase 校验(字段可选,存在才校验) ----
PATTERN_IDS = {"sv", "svc", "svo", "svoo", "svoc"}
CHUNK_ROLES = {"S", "V", "O", "IO", "C", "attr", "adv", "app", "conn", "clause"}
PARA_KINDS = {"syn", "verbatim", "para", "neg"}
GRAMMAR_TAG_IDS = None  # None = 白名单文件不存在,跳过 tag 检查

def load_grammar_tags():
    global GRAMMAR_TAG_IDS
    p = os.path.join(ROOT, "data", "grammar-tags.json")
    if not os.path.exists(p):
        print("提示: data/grammar-tags.json 不存在,跳过 deep tag 白名单检查")
        return
    with open(p, encoding="utf-8") as f:
        GRAMMAR_TAG_IDS = {t["id"] for t in json.load(f)["tags"]}

def check_tag(ctx, tag):
    if not isinstance(tag, str):
        errors.append(f"{ctx}: tag 应为字符串")
    elif tag == "":
        return  # 空字符串等同于"没有 tag"(与 gen_deep_analysis.py 校验语义一致)
    elif GRAMMAR_TAG_IDS is not None and tag not in GRAMMAR_TAG_IDS:
        errors.append(f"{ctx}: tag '{tag}' 不在 grammar-tags.json 白名单")

def check_deep(path, s):
    ctx = f"{path} 句{s.get('id')}"
    d = s["deep"]
    if not isinstance(d, dict):
        errors.append(f"{ctx}: deep 应为对象")
        return
    p = d.get("pattern")
    if p is not None:
        if not isinstance(p, dict) or p.get("id") not in PATTERN_IDS:
            errors.append(f"{ctx}: deep.pattern.id 非法")
        else:
            if "tag" in p:
                check_tag(f"{ctx} pattern", p["tag"])
            sk = p.get("skeleton")
            if not isinstance(sk, list) or not sk:
                errors.append(f"{ctx}: pattern.skeleton 应为非空数组")
            else:
                for k in sk:
                    if not isinstance(k.get("role"), str) or not isinstance(k.get("text"), str):
                        errors.append(f"{ctx}: skeleton 每项需含 role/text 字符串")
    if "chunks" in d:
        if not isinstance(d["chunks"], list) or not d["chunks"]:
            errors.append(f"{ctx}: deep.chunks 应为非空数组")
        else:
            for c in d["chunks"]:
                if c.get("role") not in CHUNK_ROLES:
                    errors.append(f"{ctx}: chunk.role 非法 ({c.get('role')})")
                if not isinstance(c.get("text"), str) or not isinstance(c.get("zh"), str):
                    errors.append(f"{ctx}: chunk 需含 text/zh 字符串")
                if "tag" in c:
                    check_tag(f"{ctx} chunk", c["tag"])
    if "grammar_points" in d:
        if not isinstance(d["grammar_points"], list):
            errors.append(f"{ctx}: grammar_points 应为数组")
        else:
            for g in d["grammar_points"]:
                for k in ("tag", "name", "explain"):
                    if not isinstance(g.get(k), str):
                        errors.append(f"{ctx}: grammar_point 缺 {k}")
                if isinstance(g.get("tag"), str):
                    check_tag(f"{ctx} grammar_point", g["tag"])
    if "vocab" in d:
        if not isinstance(d["vocab"], list):
            errors.append(f"{ctx}: vocab 应为数组")
        else:
            for v in d["vocab"]:
                if not isinstance(v.get("w"), str) or not isinstance(v.get("def"), str):
                    errors.append(f"{ctx}: vocab 每词需含 w/def 字符串")
                for k in ("synonyms", "confusables"):
                    if k in v and not isinstance(v[k], list):
                        errors.append(f"{ctx}: vocab.{k} 应为数组")
                if "aids" in v and v["aids"] is not None and not isinstance(v["aids"], dict):
                    errors.append(f"{ctx}: vocab.aids 应为对象")
    if "expressions" in d:
        if not isinstance(d["expressions"], list):
            errors.append(f"{ctx}: expressions 应为数组")
        else:
            for e in d["expressions"]:
                if not isinstance(e.get("text"), str) or not isinstance(e.get("zh"), str):
                    errors.append(f"{ctx}: expression 需含 text/zh 字符串")

def check_paraphrase(path, q, sent_en):
    ctx = f"{path} 题{q.get('number')}"
    pp = q["paraphrase"]
    if not isinstance(pp, dict) or not isinstance(pp.get("pairs"), list) or not pp["pairs"]:
        errors.append(f"{ctx}: paraphrase.pairs 应为非空数组")
        return
    ev = q.get("evidence_sentence")
    en = sent_en.get(ev, "")
    for pr in pp["pairs"]:
        if not isinstance(pr.get("q"), str) or not isinstance(pr.get("p"), str):
            errors.append(f"{ctx}: 每对替换需含 q/p 字符串")
            continue
        if pr.get("kind") not in PARA_KINDS:
            errors.append(f"{ctx}: 替换 kind 非法 ({pr.get('kind')})")
        if not en:
            errors.append(f"{ctx}: evidence_sentence {ev} 找不到对应句,无法核对 p")
        elif pr["p"].lower() not in en.lower():
            errors.append(f"{ctx}: p '{pr['p']}' 未逐字出现在证据句{ev}的 en 中")

def check_passage(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    for k in ("id", "source", "title", "sentences"):
        if k not in d:
            errors.append(f"{path}: 缺字段 {k}")
    sents = d.get("sentences", [])
    if not sents:
        errors.append(f"{path}: sentences 为空")
    prev_id, prev_para = 0, 1
    for s in sents:
        for k in ("id", "para", "en", "zh", "grammar", "words"):
            if k not in s:
                errors.append(f"{path} 句{s.get('id','?')}: 缺字段 {k}")
        if s.get("id") != prev_id + 1:
            errors.append(f"{path}: 句 id 不连续,期望 {prev_id+1} 得到 {s.get('id')}")
        prev_id = s.get("id", prev_id)
        if s.get("para", prev_para) < prev_para:
            errors.append(f"{path}: para 递减 (句{s.get('id')})")
        prev_para = s.get("para", prev_para)
        g = s.get("grammar", {})
        if not isinstance(g, dict) or "type" not in g or "note" not in g:
            errors.append(f"{path} 句{s.get('id')}: grammar 需含 type 与 note")
        for w in s.get("words", []):
            for k in ("w", "pos", "def"):
                if k not in w:
                    errors.append(f"{path} 句{s.get('id')}: 生词缺字段 {k}")
        for i, detail in enumerate(s.get("details", []), 1):
            if not isinstance(detail.get("zh"), str):
                errors.append(f"{path} 段{s.get('para')} 第{i}句: 缺 zh")
            dg = detail.get("grammar", {})
            if not isinstance(dg, dict) or "type" not in dg or "note" not in dg:
                errors.append(f"{path} 段{s.get('para')} 第{i}句: grammar 需含 type 与 note")
        if s.get("deep"):
            check_deep(d.get("id", path), s)
    sent_en = {s["id"]: s.get("en", "") for s in sents if "id" in s}
    for grp in d.get("questions", []):
        for q in grp.get("items", []):
            if q.get("paraphrase"):
                check_paraphrase(d.get("id", path), q, sent_en)
    return d

def main():
    idx_path = os.path.join(ROOT, "data", "index.json")
    with open(idx_path, encoding="utf-8") as f:
        idx = json.load(f)
    listed = {p["id"] for p in idx["passages"]}
    files = {}
    for path in glob.glob(os.path.join(ROOT, "data", "passages", "*.json")):
        d = check_passage(path)
        files[d["id"]] = sum(len(s.get("details", [])) or 1 for s in d.get("sentences", []))
    for p in idx["passages"]:
        if p["id"] not in files:
            errors.append(f"index.json 列出 {p['id']} 但缺少 data/passages/{p['id']}.json")
        elif p.get("sentence_count") != files[p["id"]]:
            errors.append(f"{p['id']}: index 句数 {p.get('sentence_count')} != 文件句数 {files[p['id']]}")
    if errors:
        print("校验失败:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"OK: {len(files)} 篇文章,索引 {len(listed)} 条,全部通过。")

if __name__ == "__main__":
    main()
