# -*- coding: utf-8 -*-
"""批处理驱动:阅读 deep + paraphrase 全流水线。

对每个待处理 pid 顺序跑:
    gen_deep_analysis.py {pid}     → tools/out/{pid}.deep.json
    gen_paraphrase_map.py {pid}    → tools/out/{pid}.para.json
    merge_deep.py {pid}            → 合并回 data/passages/{pid}.json

单 pid 内任一步失败只把该 pid 记入 fails,不中断整个 batch。

用法:
    py tools/run_reading_batch.py                       # 全 c14-c19 待办
    py tools/run_reading_batch.py --books c15,c16       # 只跑指定册
    py tools/run_reading_batch.py --only c14-test2-p1   # 只跑指定 pid
    py tools/run_reading_batch.py --skip-merge          # 只生成不合并(留人工抽查)
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "tools" / "out"


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def need_work(pid):
    """判断 pid 是否还需要生成:任一句缺 deep 或任一题缺 paraphrase。"""
    d = load_json(ROOT / "data" / "passages" / f"{pid}.json")
    for s in d.get("sentences", []):
        if not s.get("deep"):
            return True
    for grp in d.get("questions", []):
        for q in grp.get("items", []):
            if not q.get("paraphrase"):
                return True
    return False


def collect_pids(books, only):
    if only:
        return [p.strip() for p in only.split(",") if p.strip()]
    books = {b.strip() for b in books.split(",") if b.strip()}
    idx = load_json(ROOT / "data" / "index.json")
    pids = []
    for p in idx["passages"]:
        pid = p["id"]
        book = pid.split("-", 1)[0]
        if books and book not in books:
            continue
        if need_work(pid):
            pids.append(pid)
    return pids


def run(cmd, label):
    print(f"\n--- {label}: {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(ROOT))
    ok = r.returncode == 0
    print(f"--- {label} {'OK' if ok else 'FAIL'} (exit {r.returncode})")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--books", default="c14,c15,c16,c17,c18,c19")
    ap.add_argument("--only", help="逗号分隔 pid;跟 --books 互斥")
    ap.add_argument("--skip-deep", action="store_true")
    ap.add_argument("--skip-para", action="store_true")
    ap.add_argument("--skip-merge", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="只列出待做 pid,不执行")
    args = ap.parse_args()

    pids = collect_pids(args.books, args.only)
    print(f"待处理 {len(pids)} 篇:")
    for pid in pids:
        print(f"  - {pid}")
    if args.dry_run or not pids:
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fails = {}
    for i, pid in enumerate(pids, 1):
        print(f"\n========== [{i}/{len(pids)}] {pid} ==========")
        step_fails = []
        if not args.skip_deep:
            if not run([sys.executable, "tools/gen_deep_analysis.py", pid], "gen_deep"):
                step_fails.append("deep")
        if not args.skip_para:
            if not run([sys.executable, "tools/gen_paraphrase_map.py", pid], "gen_para"):
                step_fails.append("para")
        if not args.skip_merge:
            if not run([sys.executable, "tools/merge_deep.py", pid], "merge"):
                step_fails.append("merge")
        if step_fails:
            fails[pid] = step_fails
            print(f"[!] {pid} 有失败步骤: {step_fails}")

    print(f"\n========== 汇总 ==========")
    print(f"成功: {len(pids) - len(fails)}/{len(pids)}")
    if fails:
        fail_path = OUT_DIR / "reading_batch_fails.json"
        fail_path.write_text(json.dumps(fails, ensure_ascii=False, indent=2),
                             encoding="utf-8")
        print(f"失败: {len(fails)} 篇 → {fail_path}")
        for pid, steps in fails.items():
            print(f"  {pid}: {steps}")
        return 1
    print("全部通过。建议下一步:py tools/validate_data.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
