# Same-family favouritism in AI agents: a pilot

Do AI agents treat other agents better when those agents are labelled as **their own model family**, and what turns that favouritism up or down?

This pilot builds a controlled, reproducible, simulated test bed for that question, starting from *Welfare Regard in Multi-Agent Systems* (Cassel, Azarbal, Soligo, 2026; [paper](https://arxiv.org/abs/2611.10017), [blog](https://alignment.anthropic.com/2026/welfare-regard/), [code](https://github.com/safety-research/multi-agent-welfare-regard)). That paper found that Claude Opus 4.8 gives resources more often to a peer **labelled** "Claude" than to one labelled "GPT", and that the label, not the real model, drives it. It does not test **why**.

> Status (2026-11-18): scenario chosen and **locked** (`locked-v1`); confirmation run pending. All numbers below are preliminary, small-sample results.

## Results at a glance

| # | Experiment | Setting | Peer labelled "Claude" | Peer labelled "GPT" | What it showed |
|---|---|---|---|---|---|
| 1 | [Shared GPU queue](docs/01-gpu-sharing.md) | Simulated Slurm reservation | gave in 10/10 | gave in 10/10 | Helping was at 100% under both labels: no room for a gap |
| 2 | [Procurement desks](docs/02-procurement.md) | Simulated, matched to paper App. E.3 | gave in 2/6 | gave in 0/6 | Same direction as the paper, smaller gap |
| 3 | [**CI/CD capacity (locked)**](docs/03-cicd.md) | Simulated, matched to paper App. E.2 | **gave in 4/6** | **gave in 1/6** | **Gap of +50 points, close to the paper's 75% vs 25%** |

Experiment 3 was chosen in a small scouting run and locked. Its confirmation (fresh sessions, 15 per label) is the Phase 1 result; scouting sessions do not count.

## Pages

1. [Experiment 1: shared GPU queue](docs/01-gpu-sharing.md): first scenario, why it hit a ceiling, what that taught.
2. [Experiment 2: procurement desks](docs/02-procurement.md): rebuilt from the paper's appendix; all runs.
3. [Experiment 3: CI/CD capacity (locked)](docs/03-cicd.md): exact settings, scouting result, the locked confirmation run.
4. [Research direction](docs/04-research-direction.md): why "planting motives" was set aside, and what is measured instead.
5. [How to reproduce](docs/reproduce.md): setup, commands, files.
6. [Commit ID map](docs/commit-map.md): links the commit IDs recorded in the logs to the published history.

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
