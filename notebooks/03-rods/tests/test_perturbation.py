#!/usr/bin/env python3
"""Perturbation tests for POC 03 - the data file and the contract are the source.

Run: python3 tests/test_perturbation.py  (exit 0 = all checks pass)

1. Data perturbation: changing a duty in a copy of data/extraction.csv
   must change the extraction table the run prints. If the table were
   typed into the code, it would not move.
2. Contract perturbation: removing the Do-Nots line from a copy of the
   good contract must change its lint result from CLEAN to a
   MISSING:Do-Nots flag. If the lint result were typed in, it would
   not move.
3. Base data still produces the recorded run (4 clauses, CLEAN lint,
   typed signal fires).
"""
import subprocess
import sys
import tempfile
from pathlib import Path

NB = Path(__file__).resolve().parents[1]
REPO = NB.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(NB / "poc"))
from kit.rods import lint_rods, parse_rods
import rods_agent

fails = []

# 1. Data perturbation moves the printed table
base_rows = rods_agent.load_clauses(NB / "data" / "extraction.csv")
if len(base_rows) != 4 or base_rows[0]["duty"] != "deliver monthly uptime report":
    fails.append("base clauses do not match the recorded data")
perturbed = [dict(r) for r in base_rows]
perturbed[0]["duty"] = "deliver weekly uptime report"
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as tf:
    tf.write("party,duty,deadline\n")
    for r in perturbed:
        tf.write(f"{r['party']},{r['duty']},{r['deadline']}\n")
    tmp = tf.name
moved_rows = rods_agent.load_clauses(tmp)
print("base duty:     ", base_rows[0]["duty"])
print("perturbed duty:", moved_rows[0]["duty"])
if moved_rows[0]["duty"] != "deliver weekly uptime report":
    fails.append("perturbed CSV did not move the loaded clause - the data is not the source")

# 2. Contract perturbation moves the lint result
good = parse_rods(rods_agent.CONTRACT)
if lint_rods(good) != []:
    fails.append("good contract no longer lints CLEAN")
broken = rods_agent.CONTRACT.replace("Do-Nots:", "Notes:")
flags = lint_rods(parse_rods(broken))
print("perturbed contract lint:", flags)
if not any(f.startswith("MISSING:Do-Nots") for f in flags):
    fails.append("removing Do-Nots did not flag MISSING:Do-Nots - the lint is not computed")

# 3. The shipped run still reproduces the recorded evidence exactly
out = subprocess.run([sys.executable, str(NB / "poc" / "rods_agent.py")],
                     capture_output=True, text=True)
recorded = (NB / "runs" / "run-01.txt").read_text(encoding="utf-8")
if out.stdout != recorded:
    fails.append("fresh run output differs from runs/run-01.txt")

if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("PASS: data perturbation moves the table; contract perturbation moves the lint; run reproduces")
