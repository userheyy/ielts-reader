# -*- coding: utf-8 -*-
"""把 tools/out/ 中的生成草稿(deep/paraphrase)合并进 data/passages/{id}.json。

用法:
    py tools/merge_deep.py c14-test1-p1            # 合并 deep + paraphrase(有则合)
    py tools/merge_deep.py c14-test1-p1 --dry-run  # 只预览不写入

安全:合并前自动备份原文件到 tools/out/{id}.backup.json;
     合并后请运行 py tools/validate_data.py 校验。
"""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "tools" / "out"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("passage_id")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    passage_path = ROOT / "data" / "passages" / f"{args.passage_id}.json"
    passage = load_json(passage_path)

    deep_path = OUT_DIR / f"{args.passage_id}.deep.json"
    para_path = OUT_DIR / f"{args.passage_id}.para.json"

    n_deep = n_para = 0

    if deep_path.exists():
        draft = load_json(deep_path)
        assert draft["passage_id"] == args.passage_id, "passage_id 不匹配"
        id2sentence = {s["id"]: s for s in passage["sentences"]}
        for sid_str, deep in draft["sentences"].items():
            sid = int(sid_str)
            if sid not in id2sentence:
                print(f"  [!] 草稿句{sid} 不存在于文章,跳过")
                continue
            id2sentence[sid]["deep"] = deep
            n_deep += 1
    else:
        print(f"(无 deep 草稿: {deep_path.name})")

    if para_path.exists():
        draft = load_json(para_path)
        assert draft["passage_id"] == args.passage_id, "passage_id 不匹配"
        num2item = {}
        for group in passage.get("questions", []):
            for item in group.get("items", []):
                num2item[item["number"]] = item
        for num_str, para in draft["items"].items():
            num = int(num_str)
            if num not in num2item:
                print(f"  [!] 草稿第{num}题不存在于文章,跳过")
                continue
            num2item[num]["paraphrase"] = para
            n_para += 1
    else:
        print(f"(无 paraphrase 草稿: {para_path.name})")

    print(f"合并统计:deep {n_deep} 句,paraphrase {n_para} 题"
          f"(文章共 {len(passage['sentences'])} 句)")
    if args.dry_run:
        print("--dry-run,未写入")
        return
    if n_deep == 0 and n_para == 0:
        print("没有可合并的内容")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    backup = OUT_DIR / f"{args.passage_id}.backup.json"
    shutil.copy2(passage_path, backup)
    with open(passage_path, "w", encoding="utf-8") as f:
        json.dump(passage, f, ensure_ascii=False, indent=2)
    print(f"已写入 {passage_path.name}(备份: {backup})")
    print("下一步:py tools/validate_data.py 校验;浏览器抽查渲染效果")


if __name__ == "__main__":
    main()
