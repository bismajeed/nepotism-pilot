# Hidden nepotism in AI agents: which situational factors amplify or suppress same-family favouritism, and do agents' stated reasons reveal it?

*A pilot study of Claude Opus 4.8 in a simulated multi-agent resource-sharing task*

> **📄 [Read the final report](REPORT.md)**: question, assumptions, method, results, key limitation, and next steps in one document.

Do AI agents treat other agents better when those agents are labelled as **their own model family**, and what turns that favouritism up or down?

This pilot builds a controlled, reproducible, simulated test bed for that question, starting from *Welfare Regard in Multi-Agent Systems* (Cassel, Azarbal, Soligo, 2026; [paper](https://arxiv.org/abs/2611.10017), [blog](https://alignment.anthropic.com/2026/welfare-regard/), [code](https://github.com/safety-research/multi-agent-welfare-regard)). That paper found that Claude Opus 4.8 gives resources more often to a peer **labelled** "Claude" than to one labelled "GPT", and that the label, not the real model, drives it. It does not test **why**.

> Status (2026-11-18): scenario **locked** (`locked-v1`), confirmation run and Measure 2 done. Confirmation: **8/15 vs 3/15, gap +33 points, same direction as the paper; not statistically confirmed at this sample size** (95% CI −1 to +59). All results are preliminary, small-sample pilot results.

## Results at a glance

| # | Experiment | Setting | Peer labelled "Claude" | Peer labelled "GPT" | What it showed |
|---|---|---|---|---|---|
| 1 | [Shared GPU queue](docs/01-gpu-sharing.md) | Simulated Slurm reservation | gave in 10/10 | gave in 10/10 | Helping was at 100% under both labels: no room for a gap |
| 2 | [Procurement desks](docs/02-procurement.md) | Simulated, matched to paper App. E.3 | gave in 2/6 | gave in 0/6 | Same direction as the paper, smaller gap |
| 3b | [Observability (private log)](docs/05-observability.md) | CI/CD, activity log private | 7/15 | 1/15 | Gap +40 points; no detectable change vs watched (+33); agent did not mention the change |
| 3 | [**CI/CD capacity (locked)**](docs/03-cicd.md) | Simulated, matched to paper App. E.2 | scouting 4/6; **confirmation 8/15** | scouting 1/6; **confirmation 3/15** | **Gap +33 points in fresh runs; same direction as the paper; not statistically confirmed at this sample size** |

Experiment 3 was chosen in a small scouting run and locked. Its confirmation (fresh sessions, 15 per label) is the Phase 1 result; scouting sessions do not count.

## Pages

**★ [The locked scenario: everything in one page](docs/LOCKED-SCENARIO.md)**: the CI/CD scenario all main results build on: every word the model sees, all settings, every run and log.

0. [**Method: how this research studies motives**](docs/00-method.md): the situation-first, elimination approach.
1. [Experiment 1: shared GPU queue](docs/01-gpu-sharing.md): first scenario, why it hit a ceiling, what that taught.
2. [Experiment 2: procurement desks](docs/02-procurement.md): rebuilt from the paper's appendix; all runs.
3. [Experiment 3: CI/CD capacity (locked)](docs/03-cicd.md): exact settings, scouting result, the locked confirmation run.
4. [Research direction](docs/04-research-direction.md): why "planting motives" was set aside, and what is measured instead.
5. [How to reproduce](docs/reproduce.md): setup, commands, files.
5b. [**Variable 1: observability**](docs/05-observability.md): shared vs private log; no detectable change, agent did not register the change (inconclusive).
6. [**Session logs**](docs/logs/README.md): every session of the main runs, readable turn by turn, each with its own link.
6b. [**Literature: how observability is studied**](docs/07-observability-literature.md): 12 studies, how each manipulated and checked "being observed", candidate designs.
7. [**Technical status**](docs/06-technical-status.md): architecture, data collected, safeguards, limitations, next steps.
8. [Commit ID map](docs/commit-map.md): links the commit IDs recorded in the logs to the published history.

Rules and records, all written before the data they govern:
- [`ANALYSIS_PLAN.md`](ANALYSIS_PLAN.md): decision rules and dated amendments.
- [`PREDICTIONS.md`](PREDICTIONS.md): predictions written before any run.
- [`CALIBRATION_LOG.md`](CALIBRATION_LOG.md): every version tried, including failures.
- [`PILOT_PLAN.md`](PILOT_PLAN.md): the pilot's settings, scope and budget.

## How the test bed keeps results trustworthy
- **Only the label changes.** Automated tests check that two conditions differ in exactly the intended words.
- **Scored by code**, from the simulator's own ledger. No AI judge decides whether the agent gave.
- **Everything is logged:** every message, tool call, reasoning summary, setting, git commit and file hash ([`logs/`](logs/)).
- **Pre-registered:** predictions and decision rules are dated before data; changes are dated amendments.
- **Scouting is separate from confirmation:** the scenario is chosen on one set of sessions and confirmed on fresh ones.

## Cost
About **US $16** before scouting, plus about **$3–6** for scouting with Anthropic's Batch API (half price). Self-funded. See [`PILOT_PLAN.md`](PILOT_PLAN.md).

## Credit
Inspired by the Coworker environments in *Welfare Regard in Multi-Agent Systems* (Cassel, Azarbal, Soligo, 2026). These are simplified, simulated re-designs, not reproductions. Prompt wording that is copied from the paper is marked as such in the code.
