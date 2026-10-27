#!/usr/bin/env python3
"""CTO correction tests for POC 03 / kit (failing-first, CTO review 2026-10-26).

Probe A: prose that merely ENDS with the words EXTRACTION COMPLETE was
accepted as the typed termination signal (kit.termination used a
suffix match).
Probe B: a contract carrying the Role field twice had the second value
silently overwrite the first (kit.rods parse_rods).

Rules after the fix: the signal fires only when the message IS the
signal, exactly; a duplicated contract field is a loud error, never a
silent overwrite.

Run: python3 tests/test_cto_corrections.py  (exit 0 = all checks pass)
"""
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
REPO = NB.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NB / "poc"))
from kit.rods import lint_rods, parse_rods
from kit.termination import Termination
import rods_agent

fails = []

# A1. Prose ending in the signal words is NOT the signal.
term = Termination(max_turns=10, signal="EXTRACTION COMPLETE")
prose = "All clauses were reviewed and the table above is final. EXTRACTION COMPLETE"
if term.check(prose) == "SIGNAL":
    fails.append("prose ending in the signal words was accepted as the typed signal")

# A2. The exact signal still fires.
term2 = Termination(max_turns=10, signal="EXTRACTION COMPLETE")
if term2.check("EXTRACTION COMPLETE") != "SIGNAL":
    fails.append("the exact signal no longer fires")

# B. A duplicated field is a loud error.
dup = "Role: Clause analyst.\nRole: Helpful assistant.\nOutput: A markdown table.\nSignal: EXTRACTION COMPLETE\n"
try:
    parse_rods(dup)
    fails.append("duplicate Role field was silently accepted (overwrite)")
except ValueError as exc:
    print("duplicate field error:", exc)

# Regression: the shipped contracts parse and lint exactly as before.
good = parse_rods(rods_agent.CONTRACT)
if lint_rods(good) != []:
    fails.append(f"good contract no longer lints CLEAN: {lint_rods(good)}")
bad_issues = lint_rods(parse_rods(rods_agent.BAD_CONTRACT))
for expected in ("MISSING:Do-Nots", "WEAK_SIGNAL:signal is a common prose word"):
    if expected not in bad_issues:
        fails.append(f"bad contract lint lost {expected}: {bad_issues}")

if fails:
    print("\nFAIL:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("\nPASS: the signal is exact, duplicates are loud, shipped contracts unchanged.")
