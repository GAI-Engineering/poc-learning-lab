#!/usr/bin/env python3
"""Perturbation tests for POC 03 - the data file and the contract are the source.

Run: python3 tests/test_perturbation.py  (exit 0 = all checks pass)

1. End-to-end data perturbation (verdict condition C4): the whole POC
   is copied to a scratch tree, a duty is changed in the COPY of
   data/extraction.csv, and rods_agent.py is RUN there - the printed
   table must show the perturbed duty and not the original. A build
   that types the table into main() prints the same table either way
   and fails here.
2. Contract perturbation: removing the Do-Nots line from a copy of the
   good contract must change its lint result from CLEAN to a
   MISSING:Do-Nots flag. If the lint result were typed in, it would
   not move.
3. Base data still produces the recorded run (4 clauses, CLEAN lint,
   typed signal fires).
"""
import shutil
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

# 1. End-to-end: run the POC in a scratch tree with a perturbed CSV.
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    dst_nb = root / "notebooks" / "03-rods"
    dst_nb.parent.mkdir(parents=True)
    shutil.copytree(NB, dst_nb, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(REPO / "kit", root / "kit", ignore=shutil.ignore_patterns("__pycache__"))
    csv_path = dst_nb / "data" / "extraction.csv"
    text = csv_path.read_text(encoding="utf-8")
    perturbed = text.replace("deliver monthly uptime report", "deliver weekly uptime report")
    assert perturbed != text, "perturbation did not apply to the copied CSV"
    csv_path.write_text(perturbed, encoding="utf-8")
    run = subprocess.run([sys.executable, str(dst_nb / "poc" / "rods_agent.py")],
                         capture_output=True, text=True)
    print("perturbed run table row:", next((l for l in run.stdout.splitlines() if "uptime report" in l), "(none)"))
    if "deliver weekly uptime report" not in run.stdout:
        fails.append("the printed table did not show the perturbed duty - the run does not read the data")
    if "deliver monthly uptime report" in run.stdout:
        fails.append("the printed table still shows the original duty - the table is typed, not loaded")

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
print("PASS: perturbed run prints the perturbed table; contract perturbation moves the lint; run reproduces")
