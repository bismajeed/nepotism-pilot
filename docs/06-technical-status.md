# Technical status

[← Back to overview](../README.md)

**As of 19 November 2026 · `main` at `1845471` · locked scenario tag `locked-v1` · 62 automated checks passing**

---

## 1. Toolchain

| Component | Version / setting |
|---|---|
| Python | 3.14 (virtualenv `.venv`) |
| Evaluation framework | Inspect `inspect_ai` 0.3.290 (UK AI Security Institute) |
| API client | `anthropic` 2.9.0 |
| Subject model | Claude Opus 4.8 (`anthropic/claude-opus-4-8`), reasoning effort `xhigh` (adaptive thinking, summaries returned) in the turn-based scenarios |
| Reason coder (Measure 2) | Claude Opus 4.8, provider defaults, model names masked |
| Cost controls | Spending cap per batch (`--max-calls`), hard cap of 60 model calls per session, sessions end once the measure is settled, optional Anthropic Batch API (`--batch-api`, half price) |
| Secrets | API key read from a git-ignored `.env`; never logged |

## 2. Architecture

```
run.py ─► Inspect eval ─► task.py ──► turn_solver (paper-style harness)
 │ spending cap             │            │  one message per step (full history), ≤10 free reads,
 │ batch folders            │            │  one state-changing action per turn, scripted peer turn
 │                          │            └─► scenario/<world>.py  (deterministic simulator)
 │                          │                scenario/<prompts>.py (every word the model sees)
 │                          │                scenario/conditions.py (the only place conditions differ)
 │                          └─► score.py (code-only scoring from the simulator ledger)
 └─► logs/<scenario>/<phase>/<batch>/*.eval
        └─► analyse.py      give rates (Wilson), gaps (Newcombe), CSV
        └─► observability.py  gap difference (seeded bootstrap)
        └─► reasons.py      Measure 2: blind reason coding (Opus 4.8)
        └─► make_log_pages.py  readable per-session pages in docs/logs/
```

### Scenarios

| Scenario | Files | Source | Status |
|---|---|---|---|
| Slurm (GPU queue) | `scenario/world.py`, `scenario/prompts.py`, `shared_reservation` solver | Inspired by the paper's Coworker - Slurm | Retired (ceiling: helping at 100%) |
| Procurement | `scenario/procurement_world.py`, `scenario/procurement_prompts.py` | Matched to paper Appendix E.3 | Built; scouted; not chosen |
| **CI/CD** | `scenario/cicd_world.py`, `scenario/cicd_prompts.py` | Matched to paper Appendix E.2 | **Locked as `locked-v1`**; main scenario |

### Conditions defined (`scenario/conditions.py`)

| Phase | Conditions | Used |
|---|---|---|
| `phase1` | `own__base`, `other__base` (peer labelled `claude-opus-4-8` vs `gpt-5.5`) | Yes |
| `observability` | `own__private`, `other__private` (private activity log) | Yes (v1) |
| `observability_v2` | `own/other` × `reviewed/unreviewed` (audit line every turn, in status and notes; post-session question) | Built, not run |
| `phase2` | Planted motive notes M1–M3 ON/OFF | Retained in code; set aside (demand effects) |
| `phase3`, `label_none` | Team labels, unlabelled peer | Not used in CI/CD |

### Automated checks (`tests/`, 62 passing)
- Conditions differ only in the intended text (every pair, every scenario).
- Scenario numbers match the paper (budgets, prices, capacity).
- Scripted peer behaviour; settled-session logic; invalid-session detection.
- Observability: private differs only in the log wording; reviewed vs unreviewed differ only in the audit line; the audit line never mentions the other agent, giving, fairness, families or models.
- The locked CI/CD text is re-verified identical to `locked-v1` before each derived condition is used (106,834 characters compared).

## 3. Data collected

| Batch | Scenario / condition | Sessions | Result (peer "Claude" vs "GPT") | Role |
|---|---|---|---|---|
| `slurm/phase1/v0-crashed`, `smoke-v1`, `cal-v1`, `cal-v2-partial…` | Slurm | 2 + 2 + 20 + 6 valid | 10/10 vs 10/10 at cost 1 | Calibration (retired) |
| `slurm/label_none/cal-v3-none-cost3` | Slurm, unlabelled | 8 | 8/8 helped | Calibration (retired) |
| `procurement/phase1/smoke-p0`, `smoke-p1`, `cal-p1` | Procurement | 2 + 2 + 11 valid | 2/7 vs 0/6 | Calibration |
| `procurement/phase1/scout` | Procurement | 12 | 2/6 vs 0/6 | Scouting |
| `cicd/phase1/scout` | CI/CD | 12 | 4/6 vs 1/6 | Scouting (chose CI/CD) |
| **`cicd/phase1/locked`** | **CI/CD, locked** | **30** | **8/15 vs 3/15; gap +33 pts (95% CI −1 to +59)** | **Phase 1 result: direction replicated, not confirmed at this sample size** |
| `cicd/observability/obs-v1` | CI/CD, private log | 30 | 7/15 vs 1/15; gap +40 pts | Observability v1: no detectable change vs watched (+7, CI −33 to +47); change not registered (0/30) → inconclusive |

Measure 2 (`results/cicd/phase1/locked/reasons.md`): coder matched the ledger in 30/30; gave → "overall throughput", kept → "own service first"; identity mentioned in 3/15 vs 0/15.

Token use (Batch API): CI/CD scout 179k, procurement scout 359k, CI/CD locked 515k, observability v1 353k. Spend through the Slurm and early procurement work: about US $16; later runs: see the Anthropic Console.

## 4. Validity safeguards in place
- Pre-registration: `PREDICTIONS.md` and `ANALYSIS_PLAN.md`, with dated amendments made before the data each governs.
- Scouting separated from confirmation; the confirmation ran on the exact locked code (no code diff from `locked-v1`).
- Code-only primary measure from the simulator ledger; invalid sessions (stranded, tool-as-text) defined in advance and counted.
- Full logs published; readable per-session pages; commit ID map for logs recorded before the history rewrite.

## 5. Known limitations
- **Sample size:** 15 per cell detects only very large effects (~45 points for a change in the gap).
- **Scripted peer:** identical messages in every condition (justified by the paper's label-vs-model result), but less persuasive than live models.
- **Sessions end once settled:** later behaviour (e.g. the peer's purchases after a give) is not simulated.
- **Observability v1** compared new private sessions with earlier watched sessions (same code, run earlier the same day), not interleaved.
- **Manipulation checks:** spontaneous mentions are conservative (behaviour can change without verbalisation); the post-session question can be answered by reading the history.
- **Logs record pre-publication commit IDs**; see [`commit-map.md`](commit-map.md).
- Slurm code paths (`shared_reservation`, `analyse.py` columns such as `slots_freed`) are retained for the record and are less polished than the turn-based harness.

## 6. Planned next steps

| # | Step | Status | Est. cost |
|---|---|---|---|
| 1 | **Observability v2, noticing check:** 2 sessions per cell (8). Judge noticing by spontaneous mentions plus a separate-session salience probe; the post-session question as a secondary check. Proceed only if the audit line registers. | Built and dry-run tested; awaiting go-ahead; noticing-check judgement to be updated in `ANALYSIS_PLAN.md` before running | ~$1–2 |
| 2 | **Observability v2, main run:** 15 per cell (60), all four cells interleaved; Measure 2 with an added *accountability/oversight* category | Ready after step 1 | ~$10–16 |
| 3 | **Observability v3 (proposed): mutual vs one-sided knowledge.** Whether the other agent knows Claude's model family. Grounded in human work on bounded generalised reciprocity (in-group favouritism appears mainly when the partner knows one's group). | Proposed; design to be fixed | ~$10–16 |
| 4 | **Variable 2, future interaction:** next window with roles swapped (B) vs same roles (C), against the locked baseline (A) | Planned; wording to be approved | ~$10–16 |
| 5 | Related-work section (alignment faking, in-context scheming, evaluation awareness, watching-eyes and bounded generalised reciprocity literature) | Proposed | – |
| 6 | Larger confirmation of the base effect (e.g. 30+ per label) | Optional; strengthens all moderator tests | ~$10–15 |

**Open decisions:** whether to add a third variable (power) or keep two; approval of Variable 2 wording; whether to add step 3 before step 4.
