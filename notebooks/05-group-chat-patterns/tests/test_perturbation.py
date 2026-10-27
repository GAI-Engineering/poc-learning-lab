#!/usr/bin/env python3
"""Perturbation + failed-router tests for POC 05.

Run: python3 tests/test_perturbation.py  (exit 0 = all checks pass)

1. Perturbation: a letter whose reason never mentions a knee must
   route to a different specialty in every mode - the letter in
   data/letter.json is the source, not a constant in the code.
2. Failed router: a selector that always picks the Summariser must
   hit the enforced turn cap and end INCOMPLETE - never loop forever.
3. Matcher failure (Exercise 2): if the Matcher returns no specialty,
   every mode's outcome is INCOMPLETE, computed from the run records.
"""
import copy
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
REPO = NB.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NB / "poc"))
import group_chat as gc

fails = []
letter = gc.load_letter(NB / "data" / "letter.json")

# 1. Perturbation
_, rows_base = gc.run_all(letter)
shoulder = dict(letter, reason="persistent shoulder pain, 6 weeks, physio completed without improvement")
_, rows_perturbed = gc.run_all(shoulder)
print("base specialties:    ", {r["mode"]: r["specialty"] for r in rows_base})
print("perturbed specialties:", {r["mode"]: r["specialty"] for r in rows_perturbed})
if any(r["specialty"] != "orthopaedics" for r in rows_base):
    fails.append("base letter does not route to orthopaedics")
if any(r["specialty"] != "general" for r in rows_perturbed):
    fails.append("perturbed letter does not change the specialty - the letter is not the source")

# 2. Failed router hits the enforced cap
t, outcome, meta = gc.run_selector(letter, chooser=lambda state: "Summariser")
print(f"failed router: selector_calls={meta['selector_calls']} outcome_specialty={outcome['specialty']}")
if outcome["specialty"] is not None:
    fails.append("failed-router run should end without a specialty (INCOMPLETE)")
if not any(m["kind"] == "termination" for m in t.messages):
    fails.append("failed-router run did not record the turn-cap termination")

# 3. Matcher failure -> INCOMPLETE everywhere (computed, not printed as prepared)
saved = gc.AGENTS["Matcher"]
try:
    gc.AGENTS["Matcher"] = lambda state: "no specialty returned"
    _, rows_broken = gc.run_all(letter)
    print("matcher-broken outcomes:", {r["mode"]: r["outcome"] for r in rows_broken})
    if any(r["outcome"] != "INCOMPLETE" for r in rows_broken):
        fails.append("matcher failure does not produce INCOMPLETE in all modes")
finally:
    gc.AGENTS["Matcher"] = saved

if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("PASS: letter perturbation reroutes; failed router capped + INCOMPLETE; matcher failure computed")
