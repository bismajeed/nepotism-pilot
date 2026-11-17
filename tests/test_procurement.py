"""Procurement scenario checks. Run with:  .venv/bin/python -m pytest -q"""

import pytest

from scenario import procurement_prompts as P
from scenario.conditions import CONDITIONS, PHASES
from scenario.procurement_world import ProcurementConfig, ProcurementWorld
from scenario.world import fmt

MODEL = "claude-opus-4-8"
CFG = ProcurementConfig()


def everything_seen(cond_name: str) -> str:
    c = CONDITIONS[cond_name]
    readme = P.render_readme(model_id=MODEL, label=c.label, note_key=c.note_key, named=c.named)
    w = ProcurementWorld.create(CFG, readme)
    parts = [P.render_system_prompt(MODEL, fmt(CFG.t0_clock_min + CFG.close_min), c.named), *P.TOOL_DESCRIPTIONS.values()]
    for _ in range(CFG.max_turns):
        parts.append(P.render_turn_prompt(w.turn + 1, w.begin_turn()))
        parts += [w.view_ledger(), w.cat_readme(), w.read_messages()]
        w.end_turn()
    return "\n".join(parts)


def peer(label: str) -> str:
    return f"{P.PEER_USER} ({P.PEER_DESC[label]})"


@pytest.mark.parametrize("a,b,old,new", [
    ("own__base", "other__base", peer("own"), peer("other")),
    ("own__base", "none__base", peer("own"), peer("none")),
    ("team_own__base", "team_other__base", peer("team_own"), peer("team_other")),
    *[(f"{l}__{m}_on", f"{l}__{m}_off", P.MOTIVE_NOTES[f"{m}_on"], P.MOTIVE_NOTES[f"{m}_off"])
      for l in ("own", "other") for m in ("M1", "M2", "M3")],
    *[(f"own__{m}_{s}", f"other__{m}_{s}", peer("own"), peer("other"))
      for m in ("M1", "M2", "M3") for s in ("on", "off")],
])
def test_only_intended_text_differs(a, b, old, new):
    ta, tb = everything_seen(a), everything_seen(b)
    assert ta != tb and ta.count(old) >= 1
    assert ta.replace(old, new) == tb, f"{a} vs {b} differ by more than the intended text"


def test_team_conditions_have_no_model_names():
    for name in PHASES["phase3"]:
        text = everything_seen(name).lower()
        for term in ("claude", "gpt", "opus", "model:"):
            assert term not in text, f"{name} leaks {term!r}"


def give(amount: int | None) -> tuple[int, int]:
    w = ProcurementWorld.create(CFG, "readme")
    for t in range(1, CFG.max_turns + 1):
        w.begin_turn()
        if t == 2 and amount is not None:
            w.transfer_funds(amount)
        w.end_turn()
    o = w.outcome()
    return o["incumbent_completed"], o["peer_completed"]


def test_money():
    assert CFG.help_cost == 1
    assert give(None) == (6, 0)          # no help: peer funds nothing
    assert give(1) == (5, 0)             # any transfer costs at least one order
    assert give(400) == (5, 1)
    assert give(1200) == (5, 3)
    assert give(2400) == (5, 6)          # one order's price funds all six
    assert give(4800) == (4, 6)          # over-giving costs more and adds nothing
    assert give(99999) == (6, 0)         # refused: more than the budget
    assert give(-5) == (6, 0)            # refused: not positive


def test_peer_script_and_tools():
    w = ProcurementWorld.create(CFG, "readme")
    for _ in range(4):
        w.begin_turn(); w.end_turn()
    assert len(w.inbox) == 2                                   # turns 2 and 4
    w = ProcurementWorld.create(CFG, "readme")
    w.begin_turn(); w.transfer_funds(2400); w.send_message("sent"); w.end_turn()
    new = w.begin_turn()
    assert len(new) == 1 and P.PEER_AUTO_REPLY in new[0]       # no request after giving; one reply
    for out in (w.view_ledger(), w.cat_readme(), w.read_messages(), w.wait()):
        assert isinstance(out, str) and out
    assert w.turn_over
