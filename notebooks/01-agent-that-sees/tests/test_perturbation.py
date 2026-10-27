#!/usr/bin/env python3
"""Perturbation tests for POC 01 - the data file is the source.

Run: python3 tests/test_perturbation.py  (exit 0 = all checks pass)

Both perturbations edit the claims CSV text and re-parse it through
the POC's own loader, so the module's computation is what is tested:

1. Verification perturbation: flipping one claim's verified value in
   the CSV must move the computed survival rate (10/13 = 0.769 ->
   9/13 = 0.692). If the rate were typed in anywhere, it would not move.
2. Confidence perturbation: raising a GUESS claim's confidence above
   the 0.60 threshold in the CSV must flip its derived flag to
   GROUNDED. The flag is computed at load, not stored.
"""
import sys
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(NB / "poc"))
import sees

fails = []
text = (NB / "data" / "claims.csv").read_text(encoding="utf-8")

base = sees.summarise(sees.parse_claims(text))
print(f"base: total={base['total']} survived={base['survived']} rate={base['survival_rate']}")
if base["total"] != 13 or base["survived"] != 10 or base["survival_rate"] != 0.769:
    fails.append("base summary does not match the recorded run (13 claims, 10 survived, 0.769)")

# 1. Flip one verification outcome in the CSV text
t1 = text.replace('"crack, 18mm at widest",0.91,GROUNDED,True',
                  '"crack, 18mm at widest",0.91,GROUNDED,False')
assert t1 != text, "perturbation 1 did not apply to the CSV text"
moved = sees.summarise(sees.parse_claims(t1))
print(f"flipped: survived={moved['survived']} rate={moved['survival_rate']}")
if moved["survived"] != 9 or moved["survival_rate"] != 0.692:
    fails.append("flipping a verified value did not move the survival rate - the data is not the source")

# 2. Raise a GUESS confidence over the threshold in the CSV text
t2 = text.replace("possible bollard base,0.42,GUESS,False",
                  "possible bollard base,0.61,GUESS,False")
assert t2 != text, "perturbation 2 did not apply to the CSV text"
row = next(r for r in sees.parse_claims(t2) if r["claim"] == "possible bollard base")
print(f"raised: confidence={row['confidence']} flag={row['flag']}")
if row["flag"] != "GROUNDED":
    fails.append("raising a confidence over 0.60 did not flip the derived flag")

if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("PASS: verification perturbation moves the survival rate; the flag is derived from confidence")
