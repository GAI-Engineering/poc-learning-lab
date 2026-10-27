#!/usr/bin/env python3
"""CTO correction tests for POC 05 (failing-first, CTO review 2026-10-26).

Probe: at max_turns=3 the selector produced a complete pack but the
transcript labelled the run INCOMPLETE - the loop tested the budget
before testing completion, so a run that finished exactly at the cap
was mislabelled.

Rule after the fix: INCOMPLETE is recorded only when work genuinely
remains at the cap. A run that completes exactly at the cap is complete.

Run: python3 tests/test_cto_corrections.py  (exit 0 = all checks pass)
"""
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
REPO = NB.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NB / "poc"))
import group_chat as gc

fails = []

letter = gc.load_letter(NB / "data" / "letter.json")


def has_incomplete(transcript):
    return any("INCOMPLETE" in str(m) for m in transcript.messages)


# 1. Exactly-at-cap completion: pack complete, no INCOMPLETE label.
t3, outcome3, _ = gc.run_selector(letter, max_turns=3)
print("max_turns=3 outcome:", outcome3)
if not outcome3["specialty"]:
    fails.append("max_turns=3 did not produce a complete pack (specialty missing)")
if has_incomplete(t3):
    fails.append("max_turns=3 completed the pack but the transcript labels the run INCOMPLETE")

# 2. Genuinely capped: work remains, INCOMPLETE must be recorded.
t2, _, _ = gc.run_selector(letter, max_turns=2)
if not has_incomplete(t2):
    fails.append("max_turns=2 left work undone but no INCOMPLETE was recorded")

# 3. Standard runs unchanged: counts and outcomes as published.
_, rows = gc.run_all(letter)
totals = [r["total_calls"] for r in rows]
outcomes = [r["outcome"] for r in rows]
print("standard totals:", totals, "outcomes:", outcomes)
if totals != [6, 7, 4]:
    fails.append(f"standard total_calls changed: {totals}, expected [6, 7, 4]")
if outcomes != ["pack prepared"] * 3:
    fails.append(f"standard outcomes changed: {outcomes}")

if fails:
    print("\nFAIL:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("\nPASS: completion at the cap is labelled complete; a real cap still reads INCOMPLETE.")
