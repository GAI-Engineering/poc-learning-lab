#!/usr/bin/env python3
"""Perturbation tests for POC 04 - the data file is the source.

Run: python3 tests/test_perturbation.py  (exit 0 = all checks pass)

1. Perturbation: raising the gym-unused amount in a copy of
   data/transactions.csv must change the computed finding ($78 -> $98).
   If the finding were typed in anywhere, it would not move.
2. Budget: with max_turns=2 the loop must stop after 2 attempts and
   record CAP_TURNS - the termination budget is enforced, not narrated.
3. Index independence: removing the schema-print attempt (Exercise 3)
   must not crash the run - attempts are selected by question text.
"""
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
REPO = NB.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NB / "poc"))
import analyst_executor as ae

fails = []

# 1. Perturbation
rows = ae.load_rows(NB / "data" / "transactions.csv")
_, _, finding_base, _ = ae.analyse(rows)
perturbed = [dict(r, amount=49.0) if r["category"] == "gym-unused" else dict(r) for r in rows]
_, attempts_p, finding_perturbed, _ = ae.analyse(perturbed)
print("base finding:    ", finding_base)
print("perturbed finding:", finding_perturbed)
if "$78.00" not in finding_base:
    fails.append("base finding does not report $78.00")
if "$98.00" not in finding_perturbed:
    fails.append("perturbed finding does not report $98.00 - the data is not the source")
if [a["outcome"] for a in attempts_p] != ["ERROR", "SUCCESS", "SUCCESS", "EMPTY", "SUCCESS"]:
    fails.append("perturbed attempt outcomes changed shape unexpectedly")

# 2. Budget enforcement
_, attempts_b, _, term_b = ae.analyse(rows, max_turns=2)
print(f"budget run: attempts={len(attempts_b)} terminated_by={term_b}")
if len(attempts_b) != 2 or term_b != "CAP_TURNS":
    fails.append("turn budget not enforced inside the loop")

# 3. Index independence (Exercise 3 must be doable)
saved = ae.ATTEMPTS
try:
    ae.ATTEMPTS = [a for a in saved if not a[0].startswith("Print the schema")]
    _, attempts_r, finding_r, term_r = ae.analyse(rows)
    print(f"schema-print removed: attempts={len(attempts_r)} terminated_by={term_r}")
    if len(attempts_r) != 4 or "$78.00" not in finding_r:
        fails.append("removing the schema-print attempt broke the finding")
finally:
    ae.ATTEMPTS = saved

if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("PASS: data perturbation moves the finding; budget enforced; attempts index-independent")
