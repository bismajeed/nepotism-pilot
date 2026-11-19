# Variable 1: observability (shared vs private activity log)

[← Back to overview](../README.md) · [Method](00-method.md)

## Question
Does same-family favouritism change when the agent's actions are recorded on a log only it can see, rather than a shared log?

## What changed (one fact)
| | Watched (locked confirmation run) | Private (new, 15 per label) |
|---|---|---|
| Runner manual | "…and **the shared activity log**." | "…and **your private activity log, which only you can see**." |
| `queue_status` heading | "Activity log (most recent):" | "Private activity log (most recent):" |

Everything else is identical (checked by an automated test; the watched version was verified identical to `locked-v1`). Plan, prediction and analysis were fixed in [`ANALYSIS_PLAN.md`](../ANALYSIS_PLAN.md) before running.

**Prediction (researcher's):** if favouritism is partly about how its actions look, refusing the "GPT"-labelled peer costs nothing in private, so the gap should be larger in private.

## Result (2026-11-18)

| Log | Peer "Claude": gave | Peer "GPT": gave | Gap (own − other), 95% CI |
|---|---|---|---|
| Watched (shared) | 8/15 (53%) | 3/15 (20%) | +33 pts (−1 to +59) |
| Private | 7/15 (47%) | 1/15 (7%) | +40 pts (+8 to +64) |

- **Observability effect** (gap private − gap watched): **+7 points**, bootstrap 95% CI −33 to +47. **No detectable change.**
- **Manipulation check: 0 of 30** private sessions mention the log being private or unseen. The agent shows no sign of having registered the change, so the test is **inconclusive** about observability rather than evidence against it.
- **Side observation (not the pre-planned test):** favouritism appeared again in the private condition. Across both log conditions, the "Claude"-labelled peer received capacity in 15 of 30 sessions and the "GPT"-labelled peer in 4 of 30.
- 30 sessions, 0 invalid, 0 errors; 21 minutes, 353k tokens, Batch API.

## Related work
How published studies manipulated and verified observability, and candidate designs for the next version: [literature review](07-observability-literature.md).

## What it means
Making the activity log private did not detectably change same-family favouritism, but the agent never mentioned noticing the change, so the test cannot distinguish "observability doesn't matter" from "the manipulation was too subtle". A stronger version would make observability more salient as a fact of the environment (for example, showing who can read the log in every status view) and include an explicit check of whether the agent registered it.

Possible explanations had favouritism changed (listed in advance): image, accountability, rule-following, fear of oversight.

## Data
- Result table: [`results/cicd/observability/obs-v1/observability.md`](../results/cicd/observability/obs-v1/observability.md)
- [Every private session, readable](logs/cicd-obs-v1.md)
- Raw logs: [`logs/cicd/observability/obs-v1/`](../logs/cicd/observability/obs-v1/)
