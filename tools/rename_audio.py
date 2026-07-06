# -*- coding: utf-8 -*-
"""基于 audio↔tape 内容匹配的音频文件重命名。

诊断结果:96 个 mp3 里,74 个文件名跟音频内容不匹配(拷贝时错位)。
本脚本用双向 Jaccard 词集匹配确定每个 audio 的真正身份,
然后用两阶段 rename(中转 .tmp)避免文件互相覆盖。

用法:
    py -3 tools/rename_audio.py --plan       # 只输出计划,不改文件
    py -3 tools/rename_audio.py --apply      # 备份并执行 rename
    py -3 tools/rename_audio.py --revert     # 从备份恢复(如果出错)
"""
import argparse
import glob
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "media" / "audio"
BACKUP_DIR = ROOT / "media" / "audio_backup"
CACHE_DIR = ROOT / "tools" / "out"
DATA_DIR = ROOT / "data" / "listening"

_NORM = re.compile(r"[^a-z0-9\s]+")
_STOP = set(
    "the a an and or but so of to in on at for is are was were be been being i you "
    "he she it we they this that these those have has had do does did will would "
    "can could my your his her our their about with from as by not just very there "
    "here what who where when how am also all any some".split()
)


def cwords(text):
    text = _NORM.sub(" ", (text or "").lower())
    return set(w for w in text.split() if len(w) >= 4 and w not in _STOP)


def collect():
    tapes, audios = {}, {}
    for fp in sorted(glob.glob(str(DATA_DIR / "c*-test*-l*.json"))):
        pid = Path(fp).stem
        d = json.load(open(fp, encoding="utf-8"))
        tapes[pid] = cwords(" ".join(s.get("en", "") for s in d.get("segments", [])))
    for fp in sorted(glob.glob(str(CACHE_DIR / "c*-l*.paraformer.json"))):
        pid = Path(fp).stem.replace(".paraformer", "")
        p = json.load(open(fp, encoding="utf-8"))
        text = " ".join(s.get("text", "")
                        for s in p.get("transcripts", [{}])[0].get("sentences", []))
        audios[pid] = cwords(text)
    return tapes, audios


def match(tapes, audios):
    scores = {}
    for a in audios:
        for t in tapes:
            inter = len(audios[a] & tapes[t])
            union = len(audios[a] | tapes[t])
            scores[(a, t)] = inter / max(1, union)
    a2t = {a: max(tapes, key=lambda t: scores[(a, t)]) for a in audios}
    t2a = {t: max(audios, key=lambda a: scores[(a, t)]) for t in tapes}
    confirmed = {}   # audio_pid -> target_tape_pid
    conflicts = []
    for a, t in a2t.items():
        r = scores[(a, t)]
        if t2a[t] == a and r >= 0.15:
            confirmed[a] = (t, r)
        else:
            conflicts.append((a, t, r, t2a[t]))
    return confirmed, conflicts


def build_plan(confirmed):
    """Generate rename plan. audio_pid c14-test1-l3 → target tape c14-test3-l1
    means the mp3 called c14-test1-part3.mp3 should be renamed to c14-test3-part1.mp3."""
    plan = []
    for a_pid, (t_pid, r) in confirmed.items():
        if a_pid == t_pid:
            continue  # 命名已正确
        src = a_pid.replace("-l", "-part") + ".mp3"
        dst = t_pid.replace("-l", "-part") + ".mp3"
        plan.append({"src": src, "dst": dst, "sim": round(r, 3)})
    return plan


def check_conflicts(plan):
    """检查 plan 是否有 dst 冲突(两个 src 指向同一个 dst)"""
    dsts = {}
    for item in plan:
        dsts.setdefault(item["dst"], []).append(item["src"])
    conflicts = [(d, srcs) for d, srcs in dsts.items() if len(srcs) > 1]
    return conflicts


def do_rename(plan, apply=False):
    """两阶段 rename:先 →.tmp,再 .tmp→ 目标。"""
    if apply and not BACKUP_DIR.exists():
        print(f"备份 media/audio → media/audio_backup ...")
        shutil.copytree(AUDIO_DIR, BACKUP_DIR)
        print(f"备份完成")

    # Stage 1: src → src.pending.tmp
    stage1 = []
    for i, item in enumerate(plan):
        src = AUDIO_DIR / item["src"]
        if not src.exists():
            print(f"  [warn] 源不存在: {src.name}")
            continue
        tmp = AUDIO_DIR / f"_pending_{i}.tmp"
        stage1.append((tmp, item["dst"]))
        if apply:
            src.rename(tmp)
    print(f"Stage 1: {len(stage1)} 文件 → .tmp")

    # Stage 2: tmp → dst(如果 dst 存在会 rename 到 tmp 环节)
    for tmp, dst in stage1:
        target = AUDIO_DIR / dst
        if apply:
            if target.exists():
                # 目标同名文件仍然存在(在 stage1 没被处理),移到 conflict 目录
                conflict_dir = AUDIO_DIR / "_conflicts"
                conflict_dir.mkdir(exist_ok=True)
                target.rename(conflict_dir / target.name)
                print(f"  [conflict] 移动 {target.name} → _conflicts/")
            tmp.rename(target)
    print(f"Stage 2: 完成 rename")


def rename_paraformer_cache(plan, apply=False):
    """同步重命名 paraformer 缓存文件,让下一次 align 用正确的 mapping。"""
    mapping = {}
    for item in plan:
        src_pid = item["src"].replace("-part", "-l").replace(".mp3", "")
        dst_pid = item["dst"].replace("-part", "-l").replace(".mp3", "")
        mapping[src_pid] = dst_pid

    stage1 = []
    for i, (src_pid, dst_pid) in enumerate(mapping.items()):
        src_fp = CACHE_DIR / f"{src_pid}.paraformer.json"
        if not src_fp.exists():
            continue
        tmp = CACHE_DIR / f"_pending_{i}.paraformer.json"
        stage1.append((tmp, dst_pid))
        if apply:
            src_fp.rename(tmp)

    for tmp, dst_pid in stage1:
        target = CACHE_DIR / f"{dst_pid}.paraformer.json"
        if apply:
            if target.exists():
                target.unlink()  # 旧的可以覆盖(反正下次会重算)
            tmp.rename(target)
    print(f"Paraformer cache: {len(stage1)} rename")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true", help="dry run,只输出方案")
    ap.add_argument("--apply", action="store_true", help="实际执行 rename")
    ap.add_argument("--revert", action="store_true", help="从备份恢复")
    ap.add_argument("--out", default="tools/out/rename_plan.json")
    args = ap.parse_args()

    if args.revert:
        if not BACKUP_DIR.exists():
            print("没有备份可恢复")
            return
        print(f"从 {BACKUP_DIR} 恢复到 {AUDIO_DIR}")
        if AUDIO_DIR.exists():
            shutil.rmtree(AUDIO_DIR)
        shutil.copytree(BACKUP_DIR, AUDIO_DIR)
        print("恢复完成")
        return

    tapes, audios = collect()
    confirmed, conflicts = match(tapes, audios)
    plan = build_plan(confirmed)
    plan_conflicts = check_conflicts(plan)

    print(f"tape: {len(tapes)}, audio: {len(audios)}")
    print(f"双向确认: {len(confirmed)}")
    print(f"需 rename: {len(plan)}")
    print(f"匹配冲突(未加入 plan): {len(conflicts)}")
    print(f"plan 内 dst 冲突: {len(plan_conflicts)}")

    plan_fp = ROOT / args.out
    plan_fp.parent.mkdir(exist_ok=True)
    with open(plan_fp, "w", encoding="utf-8") as f:
        json.dump({
            "plan": plan,
            "unconfirmed": [{"audio": a, "guess": t, "sim": round(r, 3)}
                            for a, t, r, _ in conflicts],
            "plan_dst_conflicts": [{"dst": d, "srcs": s} for d, s in plan_conflicts],
        }, f, ensure_ascii=False, indent=2)
    print(f"方案写入 {plan_fp}")

    if plan_conflicts:
        print("\n⚠ 有 dst 冲突,不能自动 apply:")
        for d, srcs in plan_conflicts[:10]:
            print(f"  {d} ← {srcs}")

    if args.apply:
        if plan_conflicts:
            print("有冲突,不执行 apply。请手工处理 plan_dst_conflicts")
            return
        do_rename(plan, apply=True)
        rename_paraformer_cache(plan, apply=True)
        print("完成")


if __name__ == "__main__":
    main()
