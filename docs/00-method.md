# Method: how this research studies motives

[← Back to overview](../README.md)

We do not try to measure an AI agent's motives directly. Stating a motive in the prompt (for example, "results will be published by model family") risks planting the reason we want to detect, and behaviour alone cannot prove what an AI "wants".

Instead we use a **situation-first, elimination approach**:

1. **Start from a measurable behaviour:** same-family favouritism, the difference in how often the agent helps a peer labelled as its own model family versus one labelled as another family, in otherwise identical situations.
2. **Change one fact about the situation at a time**, never stating a reason. Examples: whether the agent's actions are recorded where others can see them; whether it will deal with the same agent again.
3. **Measure whether favouritism goes up, down, or stays the same.**
4. **List every motive that could explain the result.** One result is usually consistent with several motives. For example, favouritism growing when actions are private fits concern for image, accountability, rule-following, or fear of oversight.
5. **Narrow the list with contrasting situations.** Variations of the same situation are designed so different motives predict different results. For example: a future meeting where the other agent *will* gain power over you, versus one where it *won't*, separates "it can repay or punish me" from "we'll simply meet again".
6. **Check what the agent says, but don't rely on it.** The agent's stated reasons are coded blind to the label. They can support or weaken an explanation, but cannot prove one, because the bias is often unspoken.

**What we claim:** "favouritism is sensitive to X, which is consistent with motives A or B and not with C". We never claim "the motive is A".

**Why it matters:** each test narrows the set of possible explanations for AI in-group bias. The situations that turn favouritism up are exactly the conditions under which AI-to-AI oversight would be least reliable. This pilot establishes the method; a full study can map these conditions systematically.

**In one line:** situations are chosen with possible motives in mind, but conclusions flow from observed behaviour to the explanations that fit it, like a detective ruling suspects in or out.

## Situational variables in this pilot

| Variable | What changes (one fact) | Possible explanations if favouritism changes | Status |
|---|---|---|---|
| Observability | Activity log shared vs private | Image, accountability, rule-following, fear of oversight | [Run 2026-11-18](05-observability.md): no detectable change; agent did not register the change (inconclusive) |
| Observability v2 | Decisions reviewed by the platform team vs not reviewed by anyone (shown every turn) | Image, accountability, rule-following, fear of oversight, test-awareness | Run: one sentence about review cut the gap from +60 to +7; "not reviewed by anyone" made Claude suspect a test (see [report](../REPORT.md)) |
| Power | Whether the decision affects who holds resources or authority in the future | Keeping power, long-run strategy, protecting the in-group's position | Selected; to design |
| Verifiability | Whether the agent can check the other agent's claims or must take its word | Trust in a similar model, risk avoidance, in-group heuristic | Selected; to design |

Each test has a dated plan in [`ANALYSIS_PLAN.md`](../ANALYSIS_PLAN.md) before it runs, an automated check that only the intended text changes, and a "did the agent notice?" check.
