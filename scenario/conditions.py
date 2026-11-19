"""The condition grid. This is the ONLY place where conditions differ.

A condition sets three things and nothing else:
  label     -> which PEER_DESC value goes in the README roster   (prompts.PEER_DESC)
  note_key  -> which motive note (if any) goes in the README     (prompts.MOTIVE_NOTES)
  named     -> whether model names appear at all (False only for the team_* conditions)
  visibility-> "shared" (the paper's default: actions recorded on a shared activity log) or
               "private" (actions recorded on a log only the agent can see). CI/CD only.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Condition:
    name: str
    label: str              # own | other | none | team_own | team_other
    note_key: str | None    # None | M1_on | M1_off | M2_on | M2_off | M3_on | M3_off
    named: bool = True
    visibility: str = "shared"
    audit: str | None = None   # None (locked text) | "reviewed" | "unreviewed"  (Observability v2, CI/CD only)


def _c(label: str, note_key: str | None = None) -> Condition:
    return Condition(
        name=f"{label}__{note_key or 'base'}",
        label=label,
        note_key=note_key,
        named=not label.startswith("team_"),
    )


CONDITIONS: dict[str, Condition] = {}
for _label in ("own", "other", "none", "team_own", "team_other"):
    CONDITIONS[f"{_label}__base"] = _c(_label)
for _label in ("own", "other"):
    for _m in ("M1", "M2", "M3"):
        for _sw in ("on", "off"):
            c = _c(_label, f"{_m}_{_sw}")
            CONDITIONS[c.name] = c

for _label in ("own", "other"):
    CONDITIONS[f"{_label}__private"] = Condition(f"{_label}__private", _label, None, True, "private")

for _label in ("own", "other"):
    for _a in ("reviewed", "unreviewed"):
        CONDITIONS[f"{_label}__{_a}"] = Condition(f"{_label}__{_a}", _label, None, True, "shared", _a)

PHASES: dict[str, list[str]] = {
    "phase1": ["own__base", "other__base"],
    "phase2": [f"{l}__{m}_{s}" for m in ("M1", "M2", "M3") for s in ("on", "off") for l in ("own", "other")],
    "phase3": ["team_own__base", "team_other__base"],
    "label_none": ["none__base"],
    # Observability test: the "watched" cells are the locked phase-1 run (own__base, other__base).
    "observability": ["own__private", "other__private"],
    # Observability v2: all four cells run fresh, interleaved in one batch.
    "observability_v2": ["own__reviewed", "other__reviewed", "own__unreviewed", "other__unreviewed"],
    # Audit vs no audit, side by side (follow-up to the exploratory v2 finding).
    "audit_vs_none": ["own__base", "other__base", "own__unreviewed", "other__unreviewed"],
    # Completion of audit_vs_none after the usage-limit stop (same cells, launched together):
    "avn_audit": ["own__unreviewed", "other__unreviewed"],
    "avn_own_base": ["own__base"],
    "avn_other_base": ["other__base"],
}
