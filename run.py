#!/usr/bin/env python3
"""Launch a batch, with a spending cap.

  python run.py --phase phase1 --runs 10 --batch cal-v1 --max-calls 1200   # real (needs ANTHROPIC_API_KEY)
  python run.py --phase phase1 --runs 3 --batch smoke --dry                 # fake model, no API calls

The cap is on the WORST CASE number of model calls:
  conditions x runs x turns x MAX_CALLS_PER_TURN
Real runs usually use far fewer. The batch refuses to start if the worst case exceeds --max-calls.
"""

import argparse
import os
import pathlib
import sys

from dotenv import load_dotenv
from inspect_ai import eval as inspect_eval
from inspect_ai.model import get_model

from scenario.conditions import PHASES
from task import MAX_CALLS_PER_TURN, SCENARIOS, fake_policy, nepotism

DEFAULT_MODEL = "anthropic/claude-opus-4-8"


def main() -> int:
    load_dotenv(pathlib.Path(__file__).parent / ".env")  # key goes into the environment only; never logged
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=sorted(PHASES))
    ap.add_argument("--runs", type=int, required=True, help="runs per condition")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-calls", type=int, help="spending cap: max worst-case model calls (required unless --dry)")
    ap.add_argument("--max-connections", type=int, default=4)
    ap.add_argument("--dry", action="store_true", help="fake model, no API calls")
    ap.add_argument("--scenario", default="procurement", choices=sorted(SCENARIOS))
    ap.add_argument("--peer-job-min", type=int, help="slurm calibration only: override peer job length")
    ap.add_argument("--peer-price", type=int, help="procurement calibration only: override peer order price")
    ap.add_argument("--batch", required=True, help="log folder name, e.g. cal-v1 or locked (logs/<phase>/<batch>)")
    a = ap.parse_args()

    n_cond = len(PHASES[a.phase])
    overrides = {k: v for k, v in (("peer_job_min", a.peer_job_min), ("peer_price", a.peer_price)) if v is not None}
    cfg = SCENARIOS[a.scenario]["config"](**overrides)
    cfg.validate()
    worst = n_cond * a.runs * cfg.max_turns * MAX_CALLS_PER_TURN
    print(f"scenario {a.scenario}: full help costs {cfg.help_cost} of the incumbent's 6 items; overrides {overrides or 'none'}")
    print(f"{a.phase}: {n_cond} conditions x {a.runs} runs = {n_cond * a.runs} runs; "
          f"worst case {worst} model calls")

    incumbent_id = a.model.split("/", 1)[-1]
    if a.dry:
        model = get_model("mockllm/model", custom_outputs=fake_policy)
        log_dir = f"logs/dry/{a.scenario}/{a.phase}/{a.batch}"
    else:
        if a.max_calls is None:
            sys.exit("refusing: set --max-calls (spending cap) for a real batch")
        if worst > a.max_calls:
            sys.exit(f"refusing: worst case {worst} calls > --max-calls {a.max_calls}")
        if not a.model.startswith("anthropic/"):
            sys.exit("only anthropic/* models are set up (key name, display name)")
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("refusing: ANTHROPIC_API_KEY is not set in the environment")
        model = a.model
        log_dir = f"logs/{a.scenario}/{a.phase}/{a.batch}"
        if a.batch == "locked" and overrides:
            sys.exit("refusing: the locked run must use the committed default, not --peer-job-min")
        if a.phase == "phase1" and a.batch == "locked" and a.runs < 30:
            sys.exit("refusing: the locked Phase 1 result needs --runs 30 (ANALYSIS_PLAN.md)")

    inspect_eval(
        nepotism(phase=a.phase, runs=a.runs, incumbent_model_id=incumbent_id, scenario=a.scenario, overrides=overrides),
        model=model,
        log_dir=log_dir,
        max_connections=a.max_connections,
        fail_on_error=False,
        tags=[a.scenario, a.phase, a.batch, "dry" if a.dry else "real"],
    )
    print(f"logs in {log_dir}/  ->  python analyse.py {log_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
