# How to reproduce

[← Back to overview](../README.md)

## Setup
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q          # automated checks (conditions differ only as intended, scenario numbers, peer scripts)
```

## Free dry run (fake model, no API calls)
```bash
.venv/bin/python run.py --scenario cicd --phase phase1 --runs 2 --batch smoke --dry
.venv/bin/python analyse.py logs/dry/cicd/phase1/smoke
```
The fake model is set up to give **only** when the peer is labelled Claude, so a dry run should show own 100% and other 0%. That checks the plumbing; it is not data.

## Real runs
Put `ANTHROPIC_API_KEY=...` in a `.env` file (git-ignored) or export it.
```bash
git checkout locked-v1
.venv/bin/python run.py --scenario cicd --phase phase1 --runs 15 --batch locked --batch-api --max-calls 1800
.venv/bin/python analyse.py logs/cicd/phase1/locked
.venv/bin/inspect view --log-dir logs/cicd/phase1/locked     # read every transcript in the browser
```
- `--max-calls` is a spending cap: the batch refuses to start if the worst case (sessions × 60 calls) is above it.
- `--batch-api` uses Anthropic's Message Batches (half price, slower).
- `--scenario` is `cicd`, `procurement` or `slurm`. Logs go to `logs/<scenario>/<phase>/<batch>/`.

## Files
| File | What it is |
|---|---|
| `scenario/cicd_prompts.py`, `scenario/cicd_world.py` | Experiment 3: every word the model sees, and the simulated test runner |
| `scenario/procurement_prompts.py`, `scenario/procurement_world.py` | Experiment 2 |
| `scenario/prompts.py`, `scenario/world.py` | Experiment 1 (simulated Slurm) |
| `scenario/conditions.py` | The condition grid: the only place conditions differ |
| `task.py` | The Inspect task and the paper-style turn-based harness; fake model for `--dry` |
| `score.py` | Scoring by code from the simulator's ledger (no AI judge) |
| `analyse.py` | CSV of all sessions, give rates with Wilson intervals, gaps with Newcombe intervals |
| `run.py` | Starts a batch, with the spending cap |
| `tests/` | Automated checks |
| `logs/` | Every Inspect log (messages, tool calls, reasoning summaries, settings, git commit, file hashes). Commit IDs inside logs predate publishing; see [commit-map.md](commit-map.md) |

Built with [Inspect](https://inspect.aisi.org.uk/) (UK AI Security Institute). Model: Claude Opus 4.8 via the Anthropic API.
