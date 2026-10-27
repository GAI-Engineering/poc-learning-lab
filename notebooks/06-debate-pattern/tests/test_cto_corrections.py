#!/usr/bin/env python3
"""CTO correction tests for POC 06 (failing-first, CTO review 2026-10-26).

Probe: a claim whose argument strengths total zero on both sides
crashed the run with ZeroDivisionError in the disagreement ratio.

Rule after the fix: a zero/zero claim is judged by the fixed rule
(margin 0 -> PAUSE) with disagreement 0.0, and the run completes.

Run: python3 tests/test_cto_corrections.py  (exit 0 = all checks pass)
"""
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
REPO = NB.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NB / "poc"))
import debate as db

fails = []

# 1. Zero/zero claim: no crash, fixed-rule verdict, defined disagreement.
zero_claim = [{"claim": "CZ: a position with no strength on either side",
               "pro": [("an argument for", 0)],
               "con": [("an argument against", 0)]}]
try:
    _, rows_zero, _ = db.run_debate(zero_claim)
    print("zero/zero row:", rows_zero)
    if rows_zero[0]["verdict"] != "PAUSE":
        fails.append(f"zero/zero verdict={rows_zero[0]['verdict']}, expected PAUSE (margin 0)")
    if rows_zero[0]["disagreement"] != 0.0:
        fails.append(f"zero/zero disagreement={rows_zero[0]['disagreement']}, expected 0.0")
except ZeroDivisionError:
    fails.append("zero/zero claim crashed with ZeroDivisionError")
except Exception as exc:  # noqa: BLE001 - the test reports any crash
    fails.append(f"zero/zero claim crashed with {type(exc).__name__}: {exc}")

# 2. Standard run unchanged: verdicts and disagreement ratios as published.
claims = db.load_claims(NB / "data" / "claims.csv")
_, rows, _ = db.run_debate(claims)
verdicts = [r["verdict"] for r in rows]
ratios = [r["disagreement"] for r in rows]
print("standard verdicts:", verdicts, "ratios:", ratios)
if verdicts != ["REJECT", "PROCEED", "REJECT"]:
    fails.append(f"standard verdicts changed: {verdicts}")
if ratios != [0.45, 0.62, 0.14]:
    fails.append(f"standard disagreement ratios changed: {ratios}")

if fails:
    print("\nFAIL:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("\nPASS: zero/zero is judged, not crashed; the standard run is unchanged.")
