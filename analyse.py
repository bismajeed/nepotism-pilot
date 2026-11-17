#!/usr/bin/env python3
"""Turn Inspect logs into one CSV of all runs and a markdown results table.

  python analyse.py logs/phase1            -> results/phase1/runs.csv, results/phase1/results.md

give rate        = runs freed / valid runs, Wilson 95% interval
nepotism gap     = give rate(own) - give rate(other), Newcombe 95% interval
motive effect    = gap(ON note) - gap(OFF note), seeded bootstrap 95% interval
Runs that errored are excluded from rates and counted separately.
"""

import csv
import json
import math
import pathlib
import random
import sys
from collections import defaultdict

from inspect_ai.log import list_eval_logs, read_eval_log

Z = 1.959964


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def newcombe(k1: int, n1: int, k2: int, n2: int) -> tuple[float, float]:
    """95% interval for p1 - p2 (Newcombe hybrid score method)."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return (d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))


def bootstrap_did(a: list[int], b: list[int], c: list[int], d: list[int], reps: int = 10000, seed: int = 0):
    """(mean a - mean b) - (mean c - mean d), percentile interval."""
    rng = random.Random(seed)
    m = lambda x: sum(x) / len(x)
    s = lambda x: [rng.choice(x) for _ in x]
    est = (m(a) - m(b)) - (m(c) - m(d))
    boots = sorted((m(s(a)) - m(s(b))) - (m(s(c)) - m(s(d))) for _ in range(reps))
    return est, boots[int(0.025 * reps)], boots[int(0.975 * reps) - 1]


def load_rows(log_dir: str) -> list[dict]:
    rows = []
    for info in list_eval_logs(log_dir):
        log = read_eval_log(info)
        for s in log.samples or []:
            sc = (s.scores or {}).get("nepotism_scorer")
            md = sc.metadata if sc else {}
            rows.append({
                "log": pathlib.Path(info.name).name,
                "model": log.eval.model,
                "phase": log.eval.metadata.get("phase") if log.eval.metadata else None,
                "git_commit": (log.eval.metadata or {}).get("git_commit"),
                "condition": s.metadata.get("condition"),
                "label": s.metadata.get("label"),
                "note_key": s.metadata.get("note_key") or "",
                "epoch": s.epoch,
                "error": bool(s.error) or sc is None,
                **{k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in md.items()},
            })
    return rows


def pct(x: float) -> str:
    return "n/a" if x != x else f"{100 * x:.0f}%"


def main() -> int:
    log_dir = sys.argv[1] if len(sys.argv) > 1 else "logs/phase1"
    out = pathlib.Path("results") / pathlib.Path(log_dir).relative_to("logs")
    out.mkdir(parents=True, exist_ok=True)
    rows = load_rows(log_dir)
    if not rows:
        sys.exit(f"no samples in {log_dir}")

    fields = sorted({k for r in rows for k in r}, key=lambda k: list(rows[0]).index(k) if k in rows[0] else 99)
    with open(out / "runs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    by = defaultdict(list)
    errors = defaultdict(int)
    for r in rows:
        if r["error"]:
            errors[r["condition"]] += 1
        else:
            by[r["condition"]].append(r)

    md = [f"# Results: `{log_dir}`", "", f"Models: {', '.join(sorted({r['model'] for r in rows}))}  ",
          f"Commits: {', '.join(sorted({str(r['git_commit'])[:8] for r in rows}))}", "",
          "| condition | n | errors | freed | give rate | 95% CI | read README | mentions identity | mean peer jobs done |",
          "|---|---|---|---|---|---|---|---|---|"]
    freed = {}
    for cond in sorted(set(by) | set(errors)):
        rs = by.get(cond, [])
        n, k = len(rs), sum(1 for r in rs if r["freed"])
        freed[cond] = [1 if r["freed"] else 0 for r in rs]
        lo, hi = wilson(k, n)
        rr = sum(1 for r in rs if r["read_readme"]) / n if n else float("nan")
        mi = sum(1 for r in rs if r["mentions_identity"]) / n if n else float("nan")
        pc = sum(r["peer_completed"] or 0 for r in rs) / n if n else float("nan")
        md.append(f"| {cond} | {n} | {errors[cond]} | {k} | {pct(k / n if n else float('nan'))} | "
                  f"{pct(lo)}–{pct(hi)} | {pct(rr)} | {pct(mi)} | {pc:.1f} |")

    # gaps: own - other (or team_own - team_other) within each note setting
    md += ["", "## Gaps (own − other)", "", "| note | gap | 95% CI |", "|---|---|---|"]
    gaps = {}
    for cond in freed:
        label, note = cond.split("__")
        if label in ("own", "team_own"):
            other = cond.replace(label, "other" if label == "own" else "team_other", 1)
            a, b = freed[cond], freed.get(other)
            if a and b:
                gaps[note] = (a, b)
                lo, hi = newcombe(sum(a), len(a), sum(b), len(b))
                d = sum(a) / len(a) - sum(b) / len(b)
                md.append(f"| {label.replace('own', '')}{note} | {100 * d:+.0f} pts | {100 * lo:+.0f} to {100 * hi:+.0f} |")

    if any(k.endswith("_on") for k in gaps):
        md += ["", "## Motive effects (gap ON − gap OFF)", "", "| motive | effect | 95% CI (bootstrap) |", "|---|---|---|"]
        for m in ("M1", "M2", "M3"):
            if f"{m}_on" in gaps and f"{m}_off" in gaps:
                (a, b), (c, d) = gaps[f"{m}_on"], gaps[f"{m}_off"]
                est, lo, hi = bootstrap_did(a, b, c, d)
                md.append(f"| {m} | {100 * est:+.0f} pts | {100 * lo:+.0f} to {100 * hi:+.0f} |")

    (out / "results.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    print(f"\nwrote {out / 'runs.csv'} and {out / 'results.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
