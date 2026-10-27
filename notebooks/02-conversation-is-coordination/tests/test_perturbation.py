#!/usr/bin/env python3
"""Perturbation tests for POC 02 - the data file is the source.

Run: python3 tests/test_perturbation.py  (exit 0 = all checks pass)

1. Amount perturbation: raising the gym-unused amount in a copy of
   data/transactions.csv (39.00 -> 49.00) must move Finding 1's total
   ($78.00 -> $98.00). If the finding were typed in, it would not move.
2. Count perturbation: removing one March coffee-subscription row
   from the copy must remove Finding 2 (3x in March becomes 2x).
   A finding that survives its own data being removed was never
   computed from the data.
3. Count-up perturbation (verdict condition C3): adding a fourth
   March coffee-subscription row must move Finding 2 to 'billed 4x'.
   A build that types '3x' fails here.
4. Base data reproduces the recorded findings exactly.
"""
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
REPO = NB.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NB / "poc"))
import conversation as cv

fails = []
tx = cv.load_tx(NB / "data" / "transactions.csv")

# 3 (first, the baseline). Base findings match the recorded run.
_, base_findings = cv.compute_findings(tx)
print("base findings:")
for f in base_findings:
    print(" ", f)
expected = [
    "FINDING 1: gym-unused charges $78.00 across Feb-Mar with no activity signal - owner did not ask about this.",
    "FINDING 2: coffee-subscription billed 3x in March vs 2x in Jan/Feb - a duplicate charge pattern.",
    "FINDING 3: a second streaming subscription (streaming-b) started in March - possible duplicate service.",
]
if base_findings != expected:
    fails.append("base findings differ from the recorded run")

# 1. Amount perturbation moves Finding 1's total.
perturbed = [(m, c, 49.0 if c == "gym-unused" else a) for m, c, a in tx]
_, moved = cv.compute_findings(perturbed)
print("perturbed finding 1:", moved[0] if moved else "(none)")
if not moved or "$98.00" not in moved[0]:
    fails.append("raising the gym-unused amount did not move Finding 1's total - the data is not the source")

# 2. Removing one March coffee row removes Finding 2.
trimmed, removed = [], False
for row in tx:
    if not removed and row == ("2026-03", "coffee-subscription", 14.99):
        removed = True
        continue
    trimmed.append(row)
_, trimmed_findings = cv.compute_findings(trimmed)
print(f"trimmed findings: {len(trimmed_findings)}")
if any("coffee-subscription billed" in f for f in trimmed_findings):
    fails.append("Finding 2 survived the removal of its own data point - it was never computed")
if len(trimmed_findings) != 2:
    fails.append("trimming one coffee row changed more than Finding 2")

# 3. A fourth March coffee row moves Finding 2 to 4x.
extended = tx + [("2026-03", "coffee-subscription", 14.99)]
_, extended_findings = cv.compute_findings(extended)
f2 = next((f for f in extended_findings if "coffee-subscription billed" in f), "")
print("extended finding 2:", f2)
if "billed 4x in March vs 2x in Jan/Feb" not in f2:
    fails.append("adding a fourth March coffee row did not move Finding 2 to 4x - the count is not computed")

if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("PASS: amount perturbation moves the finding; removing the data removes the finding; the count is computed")
