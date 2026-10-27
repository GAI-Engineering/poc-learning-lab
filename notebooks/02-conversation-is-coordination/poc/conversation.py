#!/usr/bin/env python3
"""POC 02 - Conversation Is a Coordination Primitive.
Two agents coordinate through a transcript only, over a synthetic
transaction export. Analyst asks; Executor runs sandboxed analysis
functions and reports back. The transcript is persisted as the state.
Deterministic stub: no live model, no live bank access (copied export only).

The transactions live in data/transactions.csv - the data file is the
input of record, and every finding below is computed from it: change
an amount or a count in the CSV and the findings move.
"""
import calendar
import csv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root for kit/
from kit.transcript import TranscriptStore

def load_tx(path):
    """Load transactions -> list of (month, category, amount) tuples."""
    tx = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tx.append((r["month"], r["category"], float(r["amount"])))
    return tx

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

def _abbr(month):  # "2026-02" -> "Feb"
    return calendar.month_abbr[int(month[5:7])]

def _name(month):  # "2026-02" -> "February"
    return calendar.month_name[int(month[5:7])]

def find_unused(tx):
    """A '<x>-unused' category charged in more than one month with no
    rows for its base category '<x>' - a paid-for thing with no use."""
    out = []
    for cat in sorted({c for _, c, _ in tx}):
        if not cat.endswith("-unused"):
            continue
        if any(c == cat[:-len("-unused")] for _, c, _ in tx):
            continue
        rows = [(m, a) for m, c, a in tx if c == cat]
        months = sorted({m for m, _ in rows})
        if len(months) < 2:
            continue
        out.append({"category": cat, "total": round(sum(a for _, a in rows), 2),
                    "months": months,
                    "amounts": sorted({a for _, a in rows})})
    return out

def find_count_change(tx):
    """A category whose monthly charge count rises above its count in
    the earliest month(s) - a duplicate-charge pattern."""
    out = []
    for cat in sorted({c for _, c, _ in tx}):
        counts = monthly_count(tx, cat)
        months = sorted(counts)
        base = counts[months[0]]
        for m in months[1:]:
            if counts[m] > base:
                out.append({"category": cat, "counts": counts, "month": m,
                            "count": counts[m], "base": base,
                            "base_months": [x for x in months if counts[x] == base]})
                break
    return out

def find_overlap(tx):
    """A subscription-class service whose first charge falls in the
    latest month, after other subscription-class services already
    existed - a possible duplicate service."""
    def subscription_class(c):
        return c.endswith("-subscription") or c.startswith("streaming-")
    first = {}
    for m, c, _ in tx:
        if subscription_class(c) and (c not in first or m < first[c]):
            first[c] = m
    if len(first) < 2:
        return []
    latest = max(first.values())
    earliest = min(first.values())
    return [{"category": c, "month": m} for c, m in sorted(first.items())
            if m == latest and m != earliest]

def compute_findings(tx):
    """Every finding, computed from the transactions. Returns
    (executor_notes, findings): the Executor's mid-conversation result
    strings keyed by question, and the Analyst's numbered findings."""
    notes, findings = {}, []
    unused = find_unused(tx)
    if unused:
        u = unused[0]
        charged = " and ".join(_abbr(m) for m in u["months"])
        notes["unused"] = (f"{u['category']} charged {charged} "
                           f"(${u['amounts'][0]:.2f} each), no paired activity category present.")
        span = f"{_abbr(u['months'][0])}-{_abbr(u['months'][-1])}"
        findings.append(f"FINDING 1: {u['category']} charges ${u['total']:.2f} across {span} "
                        "with no activity signal - owner did not ask about this.")
    changes = find_count_change(tx)
    coffee = next((c for c in changes if c["category"] == "coffee-subscription"), None)
    if coffee:
        others = "/".join(_abbr(m) for m in coffee["base_months"])
        findings.append(f"FINDING 2: {coffee['category']} billed {coffee['count']}x in "
                        f"{_name(coffee['month'])} vs {coffee['base']}x in {others} - "
                        "a duplicate charge pattern.")
    overlap = find_overlap(tx)
    if overlap:
        o = overlap[0]
        notes["overlap"] = (f"{o['category']} appears in {_name(o['month'])} alongside "
                            "existing subscriptions; class overlap flagged for owner review.")
        findings.append(f"FINDING 3: a second streaming subscription ({o['category']}) "
                        f"started in {_name(o['month'])} - possible duplicate service.")
    return notes, findings

def run(tx, out=None):
    t = TranscriptStore()
    notes, findings = compute_findings(tx)
    t.append("Analyst", "question", "What are the totals by category?")
    totals = total_by_category(tx)
    t.append("Executor", "result", f"Totals: {totals}")
    t.append("Analyst", "question", "Any category charged in every month with no variation in use?")
    t.append("Executor", "result", notes["unused"])
    t.append("Analyst", "question", "Did any subscription count change month to month?")
    counts = monthly_count(tx, "coffee-subscription")
    t.append("Executor", "result", f"coffee-subscription charges per month: {counts}")
    t.append("Analyst", "question", "Any overlapping subscriptions in the same class?")
    t.append("Executor", "result", notes["overlap"])
    for f in findings:
        t.append("Analyst", "finding", f)
    t.append("Analyst", "signal", "EXPLORATION COMPLETE")
    if out is not None:
        t.save_jsonl(out)
    return t, findings

def main():
    base = Path(__file__).resolve().parents[1]
    tx = load_tx(base / "data" / "transactions.csv")
    out = base / "runs" / "transcript-01.jsonl"
    t, findings = run(tx, out)
    print(f"messages={len(t)} findings={len(findings)} transcript={out.name}")
    for f in findings:
        print(f)

if __name__ == "__main__":
    main()
