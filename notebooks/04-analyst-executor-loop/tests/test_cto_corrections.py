#!/usr/bin/env python3
"""CTO correction tests for POC 04 (failing-first, CTO review 2026-10-26).

Probe: at max_turns=2 the run reported the $78 finding although the
totals/leak attempts that produce that evidence never ran - the finding
was computed by re-running the leak code out-of-band after the loop.

Rule after the fix: a finding may only be drawn from attempts that
actually executed in this run. A capped run says so.

Run: python3 tests/test_cto_corrections.py  (exit 0 = all checks pass)
"""
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
REPO = NB.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NB / "poc"))
import analyst_executor as ae

fails = []

rows = ae.load_rows(NB / "data" / "transactions.csv")

# 1. Capped run: no finding may be reported from steps that never ran.
_, attempts_cap, finding_cap, term_cap = ae.analyse(rows, max_turns=2)
print("capped finding:  ", finding_cap)
if term_cap != "CAP_TURNS":
    fails.append(f"capped run terminated_by={term_cap}, expected CAP_TURNS")
if len(attempts_cap) != 2:
    fails.append(f"capped run executed {len(attempts_cap)} attempts, expected 2")
if "$78" in finding_cap:
    fails.append("capped run reports the $78 finding although the totals/leak attempts never ran")
if "unavailable" not in finding_cap:
    fails.append("capped run finding does not state it is unavailable")

# 2. Standard run unchanged: the finding is present and exact.
_, _, finding_full, term_full = ae.analyse(rows)
print("standard finding:", finding_full)
if "$78.00" not in finding_full:
    fails.append("standard run lost the $78.00 finding")
if term_full != "SIGNAL":
    fails.append(f"standard run terminated_by={term_full}, expected SIGNAL")

if fails:
    print("\nFAIL:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("\nPASS: capped runs report no un-earned finding; the standard run is unchanged.")
