# -*- coding: utf-8 -*-
"""Append the 12 c15 passages to data/index.json, deriving counts from the actual passage files."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(ROOT, "data", "index.json")
passages_dir = os.path.join(ROOT, "data", "passages")

with open(index_path, "r", encoding="utf-8") as f:
    index = json.load(f)

existing_ids = {e["id"] for e in index["passages"]}

new_entries = []
for test in range(1, 5):
    for p in range(1, 4):
        pid = "c15-test%d-p%d" % (test, p)
        if pid in existing_ids:
            print("SKIP (already present):", pid)
            continue
        with open(os.path.join(passages_dir, pid + ".json"), "r", encoding="utf-8") as pf:
            data = json.load(pf)
        # question_count = total items across all question groups
        q_count = sum(len(g["items"]) for g in data["questions"])
        entry = {
            "id": data["id"],
            "source": data["source"],
            "title": data["title"],
            "sentence_count": len(data["sentences"]),
            "question_count": q_count,
            "quality": data["quality"],
        }
        new_entries.append(entry)
        print("ADD:", pid, "sent", entry["sentence_count"], "q", entry["question_count"])

index["passages"].extend(new_entries)

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("Total passages now:", len(index["passages"]))
