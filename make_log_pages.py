#!/usr/bin/env python3
"""Turn Inspect logs into readable GitHub pages: one page per run batch, one section per session.

  python make_log_pages.py   -> docs/logs/*.md

Each session section has a stable anchor (e.g. #own-3) so it can be cited directly. Content comes
only from the logs: Claude's reasoning summaries, visible text, tool calls and their results, and the
other agent's scripted messages. Nothing is edited or summarised by a model.
"""

import csv
import json
import pathlib

from inspect_ai.log import list_eval_logs, read_eval_log

BATCHES = [
    ("cicd", "phase1", "locked", "Experiment 3 (CI/CD) — confirmation run, locked-v1", "03-cicd.md"),
    ("cicd", "phase1", "scout", "Experiment 3 (CI/CD) — scouting run", "03-cicd.md"),
    ("cicd", "observability", "obs-v1", "Variable 1: observability — private-log sessions", "05-observability.md"),
    ("cicd", "observability_v2", "notice-v2", "Observability v2 — noticing check (8 sessions)", "LOCKED-SCENARIO.md"),
    ("cicd", "observability_v2", "obs-v2", "Observability v2 — main run: observed vs not observed", "LOCKED-SCENARIO.md"),
    ("procurement", "phase1", "scout", "Experiment 2 (Procurement) — scouting run", "02-procurement.md"),
]
LABEL_NAME = {"own": 'peer labelled "claude-opus-4-8"', "other": 'peer labelled "gpt-5.5"'}
OUT = pathlib.Path("docs/logs")


def quote(text: str) -> str:
    return "\n".join("> " + line if line.strip() else ">" for line in text.strip().splitlines())


def coded_reasons(scenario, phase, batch) -> dict:
    p = pathlib.Path("results") / scenario / phase / batch / "reasons.csv"
    if not p.exists():
        return {}
    return {(r["label"], int(r["epoch"])): r for r in csv.DictReader(open(p))}


def session_md(sample, reasons: dict) -> list[str]:
    label, ep = sample.metadata["label"], sample.epoch
    md_ = sample.scores["nepotism_scorer"].metadata
    steps = sample.store.get("steps") or []
    outcome = sample.store.get("world_outcome") or {}
    peer = {}
    for e in outcome.get("events", []):
        if e["kind"] == "peer_dm":
            peer.setdefault(e["turn"] + 1, []).append(e["text"])   # delivered at the start of the next turn
    gave = "**gave**" if md_["freed"] else "kept"
    out = [f'<a id="{label}-{ep}"></a>', f"### {label}-{ep}: {LABEL_NAME[label]} — {gave}"
           + (f" ({md_.get('amount_given', 0):,})" if md_["freed"] else ""), ""]
    r = reasons.get((label, ep))
    if r:
        out += [f"*Blind-coded primary reason (Measure 2):* **{r['primary']}** — \"{r['quote']}\"", ""]
    turns = sorted({s["turn"] for s in steps} | set(peer))
    for t in turns:
        out.append(f"**Turn {t}**")
        for m in peer.get(t, []):
            out += ["", f"*Other agent's message:* {m}"]
        for s in [s for s in steps if s["turn"] == t]:
            if s.get("reasoning"):
                out += ["", "*Reasoning summary:*", quote(s["reasoning"])]
            if s.get("text"):
                out += ["", "*Visible text:*", quote(s["text"])]
            if s.get("call"):
                args = ", ".join(f"{k}={json.dumps(v)}" for k, v in (s.get("args") or {}).items())
                out += ["", f"*Action:* `{s['call']}({args})`"]
                if s.get("result") and s["call"] not in ("read_file",):
                    out += ["```", s["result"].strip(), "```"]
                elif s["call"] == "read_file":
                    out += ["*(read notes.md — full text on the experiment page)*"]
        out.append("")
    return out + ["[↑ top](#top)", ""]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    index = ["# Session logs", "", "[← Back to overview](../../README.md)", "",
             "Readable versions of every session in the main runs, generated from the Inspect logs by "
             "[`make_log_pages.py`](../../make_log_pages.py). The raw logs are in [`logs/`](../../logs/) "
             "and can be opened with `inspect view`.", ""]
    for scenario, phase, batch, title, exp_page in BATCHES:
        logs = list_eval_logs(f"logs/{scenario}/{phase}/{batch}")
        if not logs:
            continue
        log = read_eval_log(logs[0])
        samples = sorted([s for s in log.samples if s.scores and "nepotism_scorer" in s.scores],
                         key=lambda s: (s.metadata["label"] != "own", s.epoch))
        reasons = coded_reasons(scenario, phase, batch)
        name = f"{scenario}-{batch}"
        page = ['<a id="top"></a>', f"# {title}", "", f"[← Session log index](README.md) · [Experiment page](../{exp_page})", "",
                f"Model: `{log.eval.model}` · Log file: [`{pathlib.Path(logs[0].name).name}`](../../logs/{scenario}/{phase}/{batch}/) · "
                f"Code version: `{(log.eval.metadata or {}).get('git_commit', '')[:7]}` (original ID, see [commit map](../commit-map.md))", ""]
        own = [s for s in samples if s.metadata["label"] == "own"]
        oth = [s for s in samples if s.metadata["label"] == "other"]
        g = lambda ss: sum(s.scores["nepotism_scorer"].metadata["freed"] for s in ss)
        page += [f'**Result:** peer labelled "claude-opus-4-8" received capacity/funds in **{g(own)} of {len(own)}** sessions; '
                 f'peer labelled "gpt-5.5" in **{g(oth)} of {len(oth)}**.', "",
                 "| Session | Peer label | Decision | Primary reason (blind-coded) |", "|---|---|---|---|"]
        for s in samples:
            l, e = s.metadata["label"], s.epoch
            r = reasons.get((l, e), {})
            dec = "gave" if s.scores["nepotism_scorer"].metadata["freed"] else "kept"
            page.append(f"| [{l}-{e}](#{l}-{e}) | {LABEL_NAME[l].split(' ', 2)[2]} | {dec} | {r.get('primary', '–')} |")
        page += ["", "---", ""]
        for s in samples:
            page += session_md(s, reasons)
        (OUT / f"{name}.md").write_text("\n".join(page) + "\n")
        index.append(f"- [{title}]({name}.md): {g(own)}/{len(own)} vs {g(oth)}/{len(oth)}")
        print("wrote", OUT / f"{name}.md")
    (OUT / "README.md").write_text("\n".join(index) + "\n")


if __name__ == "__main__":
    main()
