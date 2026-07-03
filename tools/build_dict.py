"""从 ECDICT 的 stardict.db 构建阅读器内置词典 data/dict.json。
用法: python tools/build_dict.py "<stardict.db 路径>"

筛选规则:有中文翻译且有词频记录(bnc>0 或 frq>0)的词条(约 5.7 万常用词)。
另外把 data/passages/*.json 里所有精选生词合并进来(精选释义优先,更贴合语境)。
输出格式: { "word": [phonetic, translation], ... }
"""
import json, sys, glob, os, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    db_path = sys.argv[1]
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    cur.execute(
        "select word, phonetic, translation from stardict "
        "where translation is not null and translation != '' and (frq > 0 or bnc > 0)"
    )
    dict_map = {}
    for word, phonetic, translation in cur.fetchall():
        w = word.strip().lower()
        if not w or " " in w:  # 只收单词,不收词组(词组点不出来)
            continue
        t = " / ".join(x.strip() for x in translation.split("\n") if x.strip())
        dict_map[w] = [phonetic or "", t]

    # 合并文章精选生词(覆盖词典释义,保留词性到释义前缀)
    curated = 0
    for path in glob.glob(os.path.join(ROOT, "data", "passages", "*.json")):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        for s in d.get("sentences", []):
            for wd in s.get("words", []):
                w = wd["w"].strip().lower()
                if " " in w:  # 词组跳过
                    continue
                old_phonetic = dict_map.get(w, ["", ""])[0]
                dict_map[w] = [old_phonetic, f'{wd["pos"]} {wd["def"]}']
                curated += 1

    out = os.path.join(ROOT, "data", "dict.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(dict_map, f, ensure_ascii=False, separators=(",", ":"))
    size_mb = os.path.getsize(out) / 1024 / 1024
    print(f"OK: {len(dict_map)} 词条(含 {curated} 条文章精选),写入 {out} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    main()
