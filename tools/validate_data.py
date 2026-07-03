"""校验 data/index.json 与所有 data/passages/*.json 的结构完整性。
运行: python tools/validate_data.py
无错误则打印 OK 并以 0 退出;有问题打印每条错误并以 1 退出。
"""
import json, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []

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
