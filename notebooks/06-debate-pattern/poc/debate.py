#!/usr/bin/env python3
"""POC 06 - The Debate Pattern.
A Proponent builds the strongest case for a contract position, an
Opponent builds the strongest case against, and a Judge rules in a
fixed, machine-readable format: PROCEED, PAUSE or REJECT, with the
strongest point each way. Advocates never concede - the tension is
the instrument. The map of the fight is an illustrative
argument-balance prompt for human review: it is NOT a risk register,
and a scripted strength ratio locates no genuine uncertainty - a
real position requires independent evidence and counsel review.
Deterministic stub advocates: argument strengths are scripted for the
worked example, so verdicts are ILLUSTRATIVE. The verdict informs
counsel; it never accepts, signs, or advises a client.
The claims are read from data/claims.csv - the data file is the
single source for the run; every figure below is computed from it.
"""
import csv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root for kit/
from kit.transcript import TranscriptStore
from kit.termination import Termination


def load_claims(path):
    """Load claims from CSV (claim_id, claim, side, point, strength),
    grouped in file order: each claim with its pro and con arguments."""
    claims, by_id = [], {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            c = by_id.get(r["claim_id"])
            if c is None:
                c = {"claim": f"{r['claim_id']}: {r['claim']}", "pro": [], "con": []}
                by_id[r["claim_id"]] = c
                claims.append(c)
            c[r["side"]].append((r["point"], int(r["strength"])))
    return claims


def judge(pro_total, con_total):
    """Fixed rule, stated before the debate runs: margin decides."""
    margin = con_total - pro_total
    if margin >= 4:
        return "REJECT"
    if margin >= 0:
        return "PAUSE"
    return "PROCEED"


def run_debate(claims, max_turns=30):
    """Run the debate. The turn budget is enforced inside the loop:
    when the cap is hit, remaining claims go unjudged and the run
    records CAP_TURNS. Returns (transcript, rows, terminated_by)."""
    t = TranscriptStore()
    term = Termination(max_turns=max_turns, signal="DEBATE COMPLETE")
    rows = []
    terminated_by = None
    for c in claims:
        pro_total = sum(s for _, s in c["pro"])
        con_total = sum(s for _, s in c["con"])
        verdict = judge(pro_total, con_total)
        top = max(pro_total, con_total)
        disagreement = round(min(pro_total, con_total) / top, 2) if top else 0.0
        strongest_pro = max(c["pro"], key=lambda a: a[1])[0] if c["pro"] else "(no argument recorded)"
        strongest_con = max(c["con"], key=lambda a: a[1])[0] if c["con"] else "(no argument recorded)"
        t.append("Proponent", "case", f"{c['claim']} - FOR: {strongest_pro} (total {pro_total})")
        t.append("Opponent", "case", f"{c['claim']} - AGAINST: {strongest_con} (total {con_total})")
        t.append("Judge", "verdict",
                 f"{verdict} | strongest for: {strongest_pro} | strongest against: {strongest_con}")
        rows.append({"claim": c["claim"].split(":")[0], "pro_strength": pro_total,
                     "con_strength": con_total, "verdict": verdict,
                     "disagreement": disagreement})
        if term.check(verdict) == "CAP_TURNS":
            terminated_by = "CAP_TURNS"
            t.append("Judge", "termination",
                     f"turn budget {max_turns} reached - remaining claims unjudged")
            break
    if terminated_by is None:
        final = "DEBATE COMPLETE"
        t.append("Judge", "signal", final)
        terminated_by = term.check(final) or "SIGNAL"
    return t, rows, terminated_by


def main():
    base = Path(__file__).resolve().parents[1]
    claims = load_claims(base / "data" / "claims.csv")
    t, rows, terminated_by = run_debate(claims)
    out = base / "runs" / "debate-01.jsonl"
    t.save_jsonl(out)
    with open(base / "runs" / "verdicts.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["claim", "pro_strength", "con_strength", "verdict", "disagreement"])
        for r in rows:
            w.writerow([r["claim"], r["pro_strength"], r["con_strength"], r["verdict"],
                        r["disagreement"]])
    for c, r in zip(claims, rows):
        print(f"{c['claim']} -> pro {r['pro_strength']} vs con {r['con_strength']} -> "
              f"{r['verdict']} (disagreement {r['disagreement']})")
    print(f"claims={len(rows)} verdicts: " +
          ", ".join(f"{r['claim']}={r['verdict']}" for r in rows))
    if rows:
        closest = max(rows, key=lambda r: r["disagreement"])
        print(f"Closest fight: {closest['claim']} (disagreement {closest['disagreement']}) - the "
              "most balanced argument in this scripted example. Use it as a prompt for human "
              "review: it locates no genuine uncertainty, and a real position needs independent "
              "evidence and counsel review.")
    print("TERMINATION:", terminated_by)


if __name__ == "__main__":
    main()
