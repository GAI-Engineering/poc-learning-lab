#!/usr/bin/env python3
"""POC 02 - Conversation Is a Coordination Primitive.
Two agents coordinate through a transcript only, over a synthetic
transaction export. Analyst asks; Executor runs sandboxed analysis
functions and reports back. The transcript is persisted as the state.
Deterministic stub: no live model, no live bank access (copied export only).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root for kit/
from kit.transcript import TranscriptStore

# Synthetic transactions: (month, category, amount)
TX = ([("2026-01", "groceries", 82.0)] * 4 + [("2026-01", "coffee-subscription", 14.99)] * 2
      + [("2026-02", "groceries", 91.0)] * 4 + [("2026-02", "coffee-subscription", 14.99)] * 2
      + [("2026-02", "gym-unused", 39.0)]
      + [("2026-03", "groceries", 88.0)] * 4 + [("2026-03", "coffee-subscription", 14.99)] * 3
      + [("2026-03", "gym-unused", 39.0)] + [("2026-03", "streaming-b", 11.99)])

def total_by_category(tx):
    out = {}
    for _, c, a in tx:
        out[c] = round(out.get(c, 0) + a, 2)
    return out

def monthly_count(tx, category):
    out = {}
    for m, c, _ in tx:
        if c == category:
            out[m] = out.get(m, 0) + 1
    return out

def main():
    t = TranscriptStore()
    findings = []
    t.append("Analyst", "question", "What are the totals by category?")
    totals = total_by_category(TX)
    t.append("Executor", "result", f"Totals: {totals}")
    t.append("Analyst", "question", "Any category charged in every month with no variation in use?")
    t.append("Executor", "result", "gym-unused charged Feb and Mar ($39.00 each), no paired activity category present.")
    findings.append("FINDING 1: gym-unused charges $78.00 across Feb-Mar with no activity signal - owner did not ask about this.")
    t.append("Analyst", "question", "Did any subscription count change month to month?")
    counts = monthly_count(TX, "coffee-subscription")
    t.append("Executor", "result", f"coffee-subscription charges per month: {counts}")
    findings.append("FINDING 2: coffee-subscription billed 3x in March vs 2x in Jan/Feb - a duplicate charge pattern.")
    t.append("Analyst", "question", "Any overlapping subscriptions in the same class?")
    t.append("Executor", "result", "streaming-b appears in March alongside existing subscriptions; class overlap flagged for owner review.")
    findings.append("FINDING 3: a second streaming subscription (streaming-b) started in March - possible duplicate service.")
    for f in findings:
        t.append("Analyst", "finding", f)
    t.append("Analyst", "signal", "EXPLORATION COMPLETE")
    out = Path(__file__).resolve().parents[1] / "runs" / "transcript-01.jsonl"
    t.save_jsonl(out)
    print(f"messages={len(t)} findings={len(findings)} transcript={out.name}")
    for f in findings:
        print(f)

if __name__ == "__main__":
    main()
