#!/usr/bin/env python3
"""Perturbation tests for POC 06 - the claims file is the source.

Run: python3 tests/test_perturbation.py  (exit 0 = all checks pass)

1. Perturbation: strengthening one C2 con argument in a copy of
   data/claims.csv (strength 2 -> 6) must flip C2's verdict from
   PROCEED to PAUSE under the judge's fixed rule. If verdicts were
   typed in anywhere, they would not move.
2. Count: adding a fourth claim must make the run judge 4 claims -
   the claims count is computed from the run records.
3. Budget: with max_turns=1 the debate must stop after one claim and
   record CAP_TURNS.
"""
import copy
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
REPO = NB.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NB / "poc"))
import debate as db

fails = []
claims = db.load_claims(NB / "data" / "claims.csv")

# 1. Perturbation
_, rows_base, _ = db.run_debate(claims)
perturbed = copy.deepcopy(claims)
for c in perturbed:
    if c["claim"].startswith("C2"):
        c["con"] = [(p, 6 if s == 2 else s) for p, s in c["con"]]
_, rows_perturbed, _ = db.run_debate(perturbed)
base = {r["claim"]: r["verdict"] for r in rows_base}
pert = {r["claim"]: r["verdict"] for r in rows_perturbed}
print("base verdicts:    ", base)
print("perturbed verdicts:", pert)
if base.get("C2") != "PROCEED":
    fails.append("base C2 verdict is not PROCEED")
if pert.get("C2") != "PAUSE":
    fails.append("perturbed C2 verdict is not PAUSE - the claims file is not the source")

# 2. Claim count is computed
four = claims + [{"claim": "C4: accept a 30-day termination clause",
                  "pro": [("exit costs are bounded and known", 3)],
                  "con": [("switching mid-term disrupts service", 3)]}]
_, rows_four, _ = db.run_debate(four)
print(f"four-claim run judged: {len(rows_four)}")
if len(rows_four) != 4:
    fails.append("adding a claim does not change the judged count")

# 3. Budget enforcement
_, rows_cap, term_cap = db.run_debate(claims, max_turns=1)
print(f"budget run: judged={len(rows_cap)} terminated_by={term_cap}")
if len(rows_cap) != 1 or term_cap != "CAP_TURNS":
    fails.append("turn budget not enforced inside the loop")

if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("PASS: strength perturbation flips a verdict; claim count computed; budget enforced")
