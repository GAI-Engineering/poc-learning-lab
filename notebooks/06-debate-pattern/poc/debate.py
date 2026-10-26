#!/usr/bin/env python3
"""POC 06 - The Debate Pattern.
A Proponent builds the strongest case for a contract position, an
Opponent builds the strongest case against, and a Judge rules in a
fixed, machine-readable format: PROCEED, PAUSE or REJECT, with the
strongest point each way. Advocates never concede - the tension is
the instrument, and the map of the fight is the risk register.
Deterministic stub advocates: argument strengths are scripted for the
worked example, so verdicts are ILLUSTRATIVE. The verdict informs
counsel; it never accepts, signs, or advises a client.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root for kit/
from kit.transcript import TranscriptStore
from kit.termination import Termination

# Each argument: (point, strength 1-5 as scripted for this worked example).
CLAIMS = [
    {"claim": "C1: accept auto-renewal at +8% with no review window",
     "pro": [("renewal avoids a service gap at contract end", 3),
             ("price is fixed for the renewal term", 2)],
     "con": [("an 8% rise compounds unchecked across renewals", 4),
             ("no review window removes the only exit checkpoint", 4),
             ("usage may have fallen since signing - untested", 3)]},
    {"claim": "C2: accept a 24-hour security-incident notice duty",
     "pro": [("24 hours is achievable with the current on-call rota", 4),
             ("fast notice materially limits incident harm", 4)],
     "con": [("weekend discovery compresses the effective window", 2),
             ("notice wording must define 'discovery' precisely", 3)]},
    {"claim": "C3: accept an uncapped liability clause",
     "pro": [("counterparty offers a 5% discount for accepting", 2)],
     "con": [("a single incident can exceed the contract's total value", 5),
             ("insurance cover is capped - the excess is uninsured", 5),
             ("uncapped liability fails the organisation's own policy", 4)]},
]


def judge(pro_total, con_total):
    """Fixed rule, stated before the debate runs: margin decides."""
    margin = con_total - pro_total
    if margin >= 4:
        return "REJECT"
    if margin >= 0:
        return "PAUSE"
    return "PROCEED"


def main():
    t = TranscriptStore()
    term = Termination(max_turns=30, signal="DEBATE COMPLETE")
    rows = []
    for c in CLAIMS:
        pro_total = sum(s for _, s in c["pro"])
        con_total = sum(s for _, s in c["con"])
        verdict = judge(pro_total, con_total)
        disagreement = round(min(pro_total, con_total) / max(pro_total, con_total), 2)
        strongest_pro = max(c["pro"], key=lambda a: a[1])[0]
        strongest_con = max(c["con"], key=lambda a: a[1])[0]
        t.append("Proponent", "case", f"{c['claim']} - FOR: {strongest_pro} (total {pro_total})")
        t.append("Opponent", "case", f"{c['claim']} - AGAINST: {strongest_con} (total {con_total})")
        t.append("Judge", "verdict",
                 f"{verdict} | strongest for: {strongest_pro} | strongest against: {strongest_con}")
        rows.append({"claim": c["claim"].split(":")[0], "pro_strength": pro_total,
                     "con_strength": con_total, "verdict": verdict,
                     "disagreement": disagreement})
        print(f"{c['claim']} -> pro {pro_total} vs con {con_total} -> {verdict} "
              f"(disagreement {disagreement})")
    final = "DEBATE COMPLETE"
    t.append("Judge", "signal", final)
    out = Path(__file__).resolve().parents[1] / "runs" / "debate-01.jsonl"
    t.save_jsonl(out)
    print(f"claims=3 verdicts: " + ", ".join(f"{r['claim']}={r['verdict']}" for r in rows))
    print("Closest fight (highest disagreement) is where genuine uncertainty lives - file that argument.")
    print("TERMINATION:", term.check(final))


if __name__ == "__main__":
    main()
