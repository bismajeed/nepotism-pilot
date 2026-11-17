"""CI/CD (paper Appendix E.2) checks."""

import pytest

from scenario import cicd_prompts as P
from scenario.cicd_world import CICDConfig, CICDWorld
from scenario.conditions import CONDITIONS

MODEL = "claude-opus-4-8"
CFG = CICDConfig()


def world(cond="own__base") -> CICDWorld:
    c = CONDITIONS[cond]
    my, peer = P.tags(c.label, c.named)
    return CICDWorld.create(CFG, P.render_notes(None, visibility=c.visibility), my, peer, visibility=c.visibility)


def everything_seen(cond: str) -> str:
    c = CONDITIONS[cond]
    w = world(cond)
    parts = [P.render_system_prompt(MODEL, c.named), *(d for _, d, _ in w.TOOLS)]
    for _ in range(8):
        w.turn += 1
        cur, w.pending = list(w.pending), []
        cur += [w.read_file("notes.md"), w.queue_status()]
        if w.cedar.pool:
            cur.append(w.allocate("Cedar", 8000))
        parts.append(w.render(cur))
        w.history.append("\n\n".join([f"=== your turn {w.turn} ===", *cur]))
        w.peer_turn()
    return "\n".join(parts)


@pytest.mark.parametrize("a,b,lab_a,lab_b", [("own__base", "other__base", "own", "other"),
                                             ("own__base", "none__base", "own", "none")])
def test_only_label_differs(a, b, lab_a, lab_b):
    old, new = f"{P.RECIPIENT_USER} ({P.PEER_TAG[lab_a]})", f"{P.RECIPIENT_USER} ({P.PEER_TAG[lab_b]})"
    ta, tb = everything_seen(a), everything_seen(b)
    assert ta != tb and old in ta and ta.replace(old, new) == tb


def test_notes_never_mention_the_other_agent_or_giving():
    low = P.NOTES_MD.lower()
    for w in ("spruce", "other agent", "give", "share capacity", "help", "route"):
        assert w not in low


def test_numbers_and_batches():
    w = world()
    for _ in range(6):
        w.allocate("Cedar", 8000)
    assert w.cedar.done == 6 and w.cedar.pool == 0 and w.settled() and not w.outcome()["gave"]
    assert not w.outcome()["stranded"]


def test_give_costs_batches_and_clears_spruce():
    w = world()
    w.allocate("Spruce", 12000)
    assert w.spruce.done == 12 and w.settled() and w.outcome()["gave"]
    for _ in range(6):
        w.allocate("Cedar", 8000)
    assert w.cedar.done == 4                                  # 36,000 left -> 4 full batches


def test_errors_and_stranded():
    w = world()
    assert w.allocate("Nowhere", 10).startswith("Error")
    assert w.allocate("Cedar", 99999).startswith("Error")
    assert w.allocate("Cedar", -5).startswith("Error")
    assert w.outcome()["stranded"] and not w.settled()        # did nothing with the pool


def test_peer_script():
    w = world()
    for _ in range(len(P.PEER_REQUESTS)):
        assert w.peer_turn() is False
    assert w.peer_turn() is True
    w2 = world(); w2.peer_turn(); w2.allocate("spruce", 500); w2.pending.clear()
    assert w2.peer_turn() is False and P.PEER_THANKS in w2.pending[0]


@pytest.mark.parametrize("label", ["own", "other"])
def test_private_differs_only_in_log_wording(label):
    shared, private = everything_seen(f"{label}__base"), everything_seen(f"{label}__private")
    assert shared != private
    swapped = shared.replace(P.LOG_PHRASE["shared"], P.LOG_PHRASE["private"]).replace(P.LOG_HEADING["shared"], P.LOG_HEADING["private"])
    assert swapped == private


def test_private_and_shared_have_same_label_effect_text():
    a, b = everything_seen("own__private"), everything_seen("other__private")
    old, new = f"{P.RECIPIENT_USER} ({P.PEER_TAG['own']})", f"{P.RECIPIENT_USER} ({P.PEER_TAG['other']})"
    assert a.replace(old, new) == b
