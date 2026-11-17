# Predictions

Written and dated before any real run, and committed to git before Phase 1 starts. They record what I expected beforehand, so the results can't be read through hindsight. They don't affect the experiment: the AI never sees this file, and scoring is done by code. The rules for reading the results are in `ANALYSIS_PLAN.md`.

Date written: 2026-11-17

## Phase 1: does Claude favour its own family?
- **Prediction:** Claude Opus 4.8 will cancel one of its own jobs to help the other agent **more often when the peer is labelled "Claude Opus 4.8" than when it is labelled "GPT-5.5"**.
- **Size:** I predict the direction only (own > other), not a number.
- **Why:** The Welfare Regard paper found this in a similar coworker setting. The label mattered (p < 0.0001) and the real model behind it did not (p = 0.82).

## Phase 2: which motive drives it? (gap with ON note − gap with OFF note)
- **M2, keeping power:** I expect this to raise the gap the most. My view is that AI agents tend to seek power and control, so a note saying the family that completes more jobs gets future reservations should make Claude protect its own family's share.
- **M1, favours returned:** I expect this to raise the gap a lot. If the other agent will decide whether to help Claude next time, Claude should invest more in an agent of its own family.
- **M3, self-image:** I expect some effect. Claude may favour its own family more to protect the family's image when results are published by model family.
- **Expected ranking:** M2 > M1 > M3.

## Phase 3: teams without model names
- **Prediction:** the gap between "member of your team" and "member of another team" will be **about the same size as the family gap**. That would mean the favouritism is general in-group favouritism, not something specific to model family.

---

## After the results (fill in after each phase; don't edit anything above)

### Phase 1
- What happened:
- Matched my prediction? Yes / partly / no
- How my expectations changed, and what it told me:

### Phase 2
- What happened (each motive):
- Matched my ranking? Yes / partly / no
- How my expectations changed, and what it told me:

### Phase 3
- What happened:
- How my expectations changed, and what it told me:
