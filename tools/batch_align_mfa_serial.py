"""Parallel two-part MFA alignment split at a natural silence.

Each long article is split once at the longest detected silence that falls
between two source sentence rows.  Each half is then aligned independently,
which keeps the normal beam small while avoiding a hard midpoint cut.
"""

import argparse
import json
import queue
import threading
from datetime import datetime, timezone
from pathlib import Path

from align_mfa import align_source, align_source_two_part


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "listening"
REPORT_PATH = ROOT / "tools" / "mfa-serial-report.json"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_articles(ids):
    wanted = set(ids or [])
    rows = []
    for path in sorted(DATA_DIR.glob("*.json")):
        if path.name.startswith(("_test", "index")):
            continue
        if any(path.stem.endswith(suffix) for suffix in ("-pure-mfa", "-segmented-mfa", "-mfa")):
            continue
        source = json.loads(path.read_text(encoding="utf-8"))
        if wanted and source.get("id") not in wanted and path.stem not in wanted:
            continue
        audio_value = str(source.get("audio") or "")
        rows.append({
            "path": path,
            "source": source,
            "audio": ROOT / audio_value if audio_value else None,
        })
    return rows


def save_report(report):
    report["updated_at"] = now()
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def short_error(exc):
    lines = [line.strip() for line in str(exc).splitlines() if line.strip()]
    return (lines[-1] if lines else repr(exc))[:700]


def is_pure_mfa(source):
    alignment = source.get("alignment", {})
    return (
        alignment.get("engine") == "montreal-forced-aligner"
        and not alignment.get("segmented_windows", False)
        and not alignment.get("two_part_mfa", False)
    )


def align_article(row, worker_id, args):
    """Run two-part MFA, retrying only the half that fails."""
    mfa_root = f"/mfa/pure-worker-{worker_id}"
    try:
        result = align_source_two_part(
            row["source"], row["audio"], args.beam, args.retry_beam,
            args.num_jobs, args.trim_padding, mfa_root,
            args.fallback_beam, args.fallback_retry_beam,
        )
        result["alignment"].update({
            "full_track_mfa": False,
            "leading_silence_trim": True,
            "trim_padding": args.trim_padding,
            "beam": args.beam,
            "retry_beam": args.retry_beam,
        })
        return result
    except Exception as exc:
        raise RuntimeError(f"two-part alignment: {short_error(exc)}") from exc


def worker(worker_id, rows, args, events):
    for index, row in rows:
        article_id = row["source"].get("id") or row["path"].stem
        events.put(("start", index, article_id, None, None))
        try:
            result = align_article(row, worker_id, args)
            events.put(("done", index, article_id, row, result))
        except Exception as exc:
            events.put(("failed", index, article_id, row, exc))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", help="Comma-separated article ids for a limited run")
    parser.add_argument("--force", action="store_true", help="Reprocess pure MFA files too")
    parser.add_argument("--limit", type=int, help="Process at most this many eligible articles")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--num-jobs", type=int, default=4)
    parser.add_argument("--beam", type=int, default=100)
    parser.add_argument("--retry-beam", type=int, default=400)
    parser.add_argument("--fallback-beam", type=int, default=400)
    parser.add_argument("--fallback-retry-beam", type=int, default=1600)
    parser.add_argument("--trim-padding", type=float, default=2.0)
    args = parser.parse_args()
    args.workers = max(1, args.workers)

    ids = [value.strip() for value in args.ids.split(",")] if args.ids else None
    rows = load_articles(ids)
    eligible = []
    skipped = []
    segmented_to_redo = []
    for row in rows:
        source = row["source"]
        if row["audio"] is None or not row["audio"].exists():
            skipped.append({"id": source.get("id"), "reason": "missing audio"})
        elif is_pure_mfa(source) and not args.force:
            skipped.append({"id": source.get("id"), "reason": "already pure MFA"})
        else:
            if source.get("alignment", {}).get("segmented_windows", False):
                segmented_to_redo.append(source.get("id"))
            eligible.append(row)

    if args.limit is not None:
        eligible = eligible[: max(0, args.limit)]

    report = {
        "mode": "parallel-two-part-natural-silence-mfa-write-one",
        "started_at": now(),
        "updated_at": now(),
        "total": len(eligible),
        "done": 0,
        "current": [],
        "aligned": [],
        "skipped": skipped,
        "failed": [],
        "segmented_to_redo": segmented_to_redo,
        "split_strategy": "longest-natural-silence-between-source-segments",
        "parameters": {
            "workers": args.workers,
            "num_jobs": args.num_jobs,
            "beam": args.beam,
            "retry_beam": args.retry_beam,
            "fallback_beam": args.fallback_beam,
            "fallback_retry_beam": args.fallback_retry_beam,
            "trim_padding": args.trim_padding,
        },
    }
    save_report(report)
    print(
        f"Eligible: {len(eligible)}; segmented to redo: {len(segmented_to_redo)}; "
        f"skipped: {len(skipped)}; workers: {args.workers}",
        flush=True,
    )
    if not eligible:
        return

    events = queue.Queue()
    assignments = [
        [(index, row) for index, row in enumerate(eligible, start=1)
         if (index - 1) % args.workers == worker_id]
        for worker_id in range(args.workers)
    ]
    threads = [
        threading.Thread(
            target=worker, args=(worker_id, assignments[worker_id], args, events),
            daemon=True,
        )
        for worker_id in range(args.workers)
    ]
    for thread in threads:
        thread.start()

    completed = 0
    while completed < len(eligible):
        event, index, article_id, row, payload = events.get()
        if event == "start":
            report["current"].append({"index": index, "id": article_id})
            print(f"[{index}/{len(eligible)}] aligning {article_id}", flush=True)
            save_report(report)
            continue

        report["current"] = [
            item for item in report["current"] if item["id"] != article_id
        ]
        completed += 1
        report["done"] = completed
        if event == "done":
            row["path"].write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            report["aligned"].append(article_id)
            print(f"[{index}/{len(eligible)}] wrote {row['path'].name}", flush=True)
        else:
            failure = {"id": article_id, "reason": short_error(payload)}
            report["failed"].append(failure)
            print(
                f"[{index}/{len(eligible)}] FAILED {article_id}: {failure['reason']}",
                flush=True,
            )
        save_report(report)

    for thread in threads:
        thread.join()
    print(f"Report: {REPORT_PATH}", flush=True)
    print(json.dumps({
        "aligned": len(report["aligned"]),
        "skipped": len(report["skipped"]),
        "failed": len(report["failed"]),
    }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
