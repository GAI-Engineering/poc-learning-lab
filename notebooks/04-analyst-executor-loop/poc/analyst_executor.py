#!/usr/bin/env python3
"""POC 04 - The Analyst-Executor Loop.
An Analyst drafts code for a question; an Executor runs it in a sandbox
and returns the real output - or the real error - as a message. The
Analyst reads the error and revises. The conversation is the control
flow: there is no retry table, the error is the curriculum.
Deterministic stub: no live model. Data: synthetic transactions only.
Sandbox: exec with a restricted builtin set over an in-memory export -
a teaching sandbox, not a production one (the post says so plainly).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root for kit/
from kit.transcript import TranscriptStore
from kit.termination import Termination

# Synthetic transaction export: dict rows, as a real export would arrive.
ROWS = (
    [{"month": "2026-01", "category": "groceries", "amount": 82.0}] * 4
    + [{"month": "2026-01", "category": "coffee-subscription", "amount": 14.99}] * 2
    + [{"month": "2026-02", "category": "groceries", "amount": 91.0}] * 4
    + [{"month": "2026-02", "category": "coffee-subscription", "amount": 14.99}] * 2
    + [{"month": "2026-02", "category": "gym-unused", "amount": 39.0}]
    + [{"month": "2026-03", "category": "groceries", "amount": 88.0}] * 4
    + [{"month": "2026-03", "category": "coffee-subscription", "amount": 14.99}] * 3
    + [{"month": "2026-03", "category": "gym-unused", "amount": 39.0}]
    + [{"month": "2026-03", "category": "streaming-b", "amount": 11.99}]
)

SAFE_BUILTINS = {"sum": sum, "len": len, "round": round, "sorted": sorted,
                 "min": min, "max": max, "print": print}


def run_sandbox(code):
    """Run analyst code with only `rows` and safe builtins visible.
    Returns (ok, result_or_error_message). Errors come back verbatim -
    legible errors are the whole point of the loop."""
    namespace = {"rows": [dict(r) for r in ROWS], "__builtins__": SAFE_BUILTINS}
    try:
        exec(code, namespace)
        return True, namespace.get("result")
    except Exception as exc:  # the error IS the message back to the analyst
        return False, f"{type(exc).__name__}: {exc}"


# The analyst's attempts, in order. Attempts 1 and 4 fail legibly; the
# analyst's revisions (2, 3, 5) exist only because the errors were read.
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


def main():
    t = TranscriptStore()
    term = Termination(max_turns=20, signal="ANALYSIS COMPLETE")
    attempts = []
    for i, (question, code) in enumerate(ATTEMPTS, start=1):
        t.append("Analyst", "code", f"Attempt {i} - {question}: {code.splitlines()[0]} ...")
        ok, out = run_sandbox(code)
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
        print(f"attempt {i}: {outcome} - {question}")
    totals_ok, totals = run_sandbox(ATTEMPTS[2][1])
    leak_total = round(sum(a for _, a in run_sandbox(ATTEMPTS[4][1])[1]), 2)
    finding = (f"FINDING: gym-unused totals ${leak_total:.2f} across Feb-Mar with no activity "
               "category in the export - the loop's top leak, traced to actual rows.")
    t.append("Analyst", "finding", finding)
    final = "ANALYSIS COMPLETE"
    t.append("Analyst", "signal", final)
    out_path = Path(__file__).resolve().parents[1] / "runs" / "transcript-01.jsonl"
    t.save_jsonl(out_path)
    print(f"attempts={len(attempts)} errors=1 empty=1 successes=3 transcript={out_path.name}")
    print(finding)
    print("TERMINATION:", term.check(final))


if __name__ == "__main__":
    main()
