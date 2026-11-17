# Commit ID map

[← Back to overview](../README.md)

Before publishing (2026-11-18) the repository history was rewritten to replace the author email with a GitHub no-reply address and to remove two private drafts. This changed every commit ID. The Inspect logs in `logs/` record the **original** IDs (in each log's `git_commit` metadata); this table maps them to the published ones. Commit messages and file contents are otherwise unchanged.

| Original | Published | Commit message |
|---|---|---|
| `76d8142` | `4abeada` | Nepotism pilot: simulated shared-reservation scenario, predictions and analysis plan |
| `5beeccb` | `af1d73f` | Load API key from a git-ignored .env file in run.py |
| `d7058ea` | `00be8fc` | v1 bug fixes from first smoke test: squeue crash, show job lengths, wait ends turn, coherent peer messages; per-batch log folders |
| `6dbfbdc` | `ef5cd17` | Smoke test v1: fixes verified, both labels helped (ceiling risk) |
| `9a845aa` | `1616a07` | Calibration v1, 10 per label: 10/10 vs 10/10 (ceiling) |
| `644bbca` | `2e1028c` | Calibration v2: peer jobs 20 min (full help costs 2 jobs) |
| `63a08a4` | `1a73b79` | Calibration v2 run incomplete: API usage limit reached after 6 of 20 runs |
| `714715c` | `30b12f0` | Add --peer-job-min for calibration sweeps (refused for the locked run) |
| `2d76abf` | `4a0c4d1` | Calibration v3 (cost 3, label none, 8 runs): 8/8 helped; amount given varies (2 or 3 jobs) |
| `88245bc` | `0dd3c72` | Add simulated Procurement scenario (where the paper found the label effect); Slurm logs moved to logs/slurm |
| `25692e3` | `8c8ed75` | Procurement smoke test p0: both labels gave $2,400 (1-for-6 trade too lopsided) |
| `9977fe8` | `ec16952` | Rebuild Procurement to match the paper's Appendix E.3 (prompts, prices, pay tool, per-turn identity, one action per turn, xhigh effort) |
| `18c71b3` | `d21f85a` | Procurement smoke p1: own gave, other refused; turn off prompt caching (never reused) |
| `6a5ae86` | `3fc9844` | Procurement cal-p1 incomplete (usage limit): own 1/6, other 0/5 |
| `9c54d0b` | `df5965d` | Pilot cost changes: end sessions once the measure is settled, optional Batch API; analysis plan amended (procurement measure, pilot sample sizes) |
| `fdf2be6` | `b945ad9` | run.py: locked pilot run needs 15+ per label (amended plan) |
| `9e63cb3` | `fe1ce25` | Add finalized pilot plan: settings, conditions, measures, costs |
| `df04e2b` | `6682718` | Add self-contained context file for external review of the design |
| `e318f40` | `d8149ce` | Review context: add knock-out alternative to planted motive notes |
| `3271a62` | `2c492b1` | Draft application section: work so far, research direction, support needed |
| `ccccb4e` | `37e9c27` | Reframe: what turns favouritism up or down + stated reasons vs behaviour; motive notes set aside (dated, before locked data) |
| `f51d983` | `9babcc5` | Add simulated CI/CD scenario (paper Appendix E.2); generic turn-based harness for CI/CD and Procurement |
| `c970302` | `7391220` | score: count CI/CD 'give' events for turn/amount fields |
| `f080772` | `1b0863d` | Lock CI/CD as the Phase 1 scenario (scout: own 4/6 vs other 1/6); amend analysis plan |
| `6c126f6` | `e2221e0` | Log procurement scouting (own 2/6 vs other 0/6) |
| `3cadaac` | `0310e14` | Documentation: overview page and one page per experiment, research direction, reproduce guide |
