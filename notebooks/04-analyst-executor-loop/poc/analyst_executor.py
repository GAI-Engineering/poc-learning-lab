#!/usr/bin/env python3
"""POC 04 - The Analyst-Executor Loop.
An Analyst drafts code for a question; an Executor runs it in-process
and returns the real output - or the real error - as a message. The
Analyst reads the error and revises. The conversation is the control
flow: there is no retry table, the error is the curriculum.
Deterministic stub: no live model. Data: synthetic transactions only,
read from data/transactions.csv - the data file is the single source
for the run; every figure below is computed from it.
Executor honesty note: the executor is a TEACHING-ONLY in-process
exec with a restricted builtin set over an in-memory copy of the data.
A restricted builtin set is NOT an isolation boundary - never run
untrusted code or real data through it. A production runner isolates
execution properly (separate process/container); this one does not.
"""
import csv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root for kit/
from kit.transcript import TranscriptStore
from kit.termination import Termination

SAFE_BUILTINS = {"sum": sum, "len": len, "round": round, "sorted": sorted,
                 "min": min, "max": max, "print": print}


def load_rows(path):
    """Load the transaction export (month, category, amount) from CSV."""
    with open(path, newline="", encoding="utf-8") as fh:
        return [{"month": r["month"], "category": r["category"],
                 "amount": float(r["amount"])} for r in csv.DictReader(fh)]


def run_executor(code, rows):
    """Run analyst code with only `rows` and safe builtins visible.
    Returns (ok, result_or_error_message). Errors come back as the
    exception type and message - legible errors are the point of the
    loop. Teaching-only: this is not a sandbox (see module docstring)."""
    namespace = {"rows": [dict(r) for r in rows], "__builtins__": SAFE_BUILTINS}
    try:
        exec(code, namespace)
        return True, namespace.get("result")
    except Exception as exc:  # the error IS the message back to the analyst
        return False, f"{type(exc).__name__}: {exc}"


# The analyst's attempts, in order. Attempts 1 and 4 fail legibly; the
# analyst's revisions (2, 3, 5) exist only because the errors were read.
# Attempts are selected by their question text, never by list index, so
# adding or removing an attempt cannot break the finding.
ATTEMPTS = [
    ("Total spend by category",
     "result = {}\nfor r in rows:\n    result[r['category']] = round(result.get(r['category'], 0) + r['amt'], 2)"),
    ("Print the schema first (the recovery habit)",
     "result = {'columns': sorted(rows[0].keys()), 'row_count': len(rows)}"),
    ("Total spend by category (revised: key is 'amount')",
     "result = {}\nfor r in rows:\n    result[r['category']] = round(result.get(r['category'], 0) + r['amount'], 2)"),
    ("Monthly charges for category 'gym'",
     "result = [r for r in rows if r['category'] == 'gym']"),
    ("Monthly charges for 'gym-unused' (exact name from the totals)",
     "result = [(r['month'], r['amount']) for r in rows if r['category'] == 'gym-unused']"),
]

TOTALS_QUESTION = "Total spend by category (revised: key is 'amount')"
LEAK_QUESTION = "Monthly charges for 'gym-unused' (exact name from the totals)"


def analyse(rows, max_turns=20):
    """Run the attempt loop over `rows`. The turn budget is enforced
    inside the loop: when the cap is hit the loop stops and records
    CAP_TURNS instead of completing. Returns (transcript, attempts,
    finding, terminated_by)."""
    t = TranscriptStore()
    term = Termination(max_turns=max_turns, signal="ANALYSIS COMPLETE")
    attempts = []
    terminated_by = None
    for i, (question, code) in enumerate(ATTEMPTS, start=1):
        t.append("Analyst", "code", f"Attempt {i} - {question}: {code.splitlines()[0]} ...")
        ok, out = run_executor(code, rows)
        if not ok:
            outcome = "ERROR"
            t.append("Executor", "error", out)
        elif out == [] or out == {}:
            outcome = "EMPTY"
            t.append("Executor", "result", "[] (no rows matched - the question, not the code, is wrong)")
        else:
            outcome = "SUCCESS"
            t.append("Executor", "result", str(out))
        attempts.append({"attempt": i, "stage": question, "outcome": outcome})
        if term.check(outcome) == "CAP_TURNS":
            terminated_by = "CAP_TURNS"
            t.append("Executor", "termination",
                     f"turn budget {max_turns} reached - loop stopped mid-run")
            break
    by_question = {q: c for q, c in ATTEMPTS}
    if LEAK_QUESTION in by_question and TOTALS_QUESTION in by_question:
        leak_ok, leak_rows = run_executor(by_question[LEAK_QUESTION], rows)
        leak_total = round(sum(a for _, a in leak_rows), 2) if leak_ok else 0.0
        months = ", ".join(sorted({m for m, _ in leak_rows})) if leak_ok else ""
        finding = (f"FINDING: gym-unused totals ${leak_total:.2f} across {months} with no activity "
                   "category in the export - the loop's top leak, traced to actual rows.")
    else:
        finding = "FINDING: unavailable - the totals/leak attempts were removed from this run."
    t.append("Analyst", "finding", finding)
    if terminated_by is None:
        final = "ANALYSIS COMPLETE"
        t.append("Analyst", "signal", final)
        terminated_by = term.check(final) or "SIGNAL"
    return t, attempts, finding, terminated_by


def main():
    base = Path(__file__).resolve().parents[1]
    rows = load_rows(base / "data" / "transactions.csv")
    t, attempts, finding, terminated_by = analyse(rows)
    out_path = base / "runs" / "transcript-01.jsonl"
    t.save_jsonl(out_path)
    with open(base / "runs" / "attempts.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["attempt", "stage", "outcome"])
        for a in attempts:
            w.writerow([a["attempt"], a["stage"], a["outcome"]])
    errors = sum(1 for a in attempts if a["outcome"] == "ERROR")
    empty = sum(1 for a in attempts if a["outcome"] == "EMPTY")
    successes = sum(1 for a in attempts if a["outcome"] == "SUCCESS")
    for a in attempts:
        print(f"attempt {a['attempt']}: {a['outcome']} - {a['stage']}")
    print(f"attempts={len(attempts)} errors={errors} empty={empty} successes={successes} "
          f"transcript={out_path.name}")
    print(finding)
    print("TERMINATION:", terminated_by)


if __name__ == "__main__":
    main()
