#!/usr/bin/env python3
"""POC 01 - An Agent That Sees: layered scene parser (deterministic stub).
Synthetic scenes only. The scenes, the parser's claims and confidences,
and the recorded human verification live in data/claims.csv - the data
file is the input of record. This module loads it, derives each claim's
flag from its confidence (below 0.60 = GUESS, the confidence map) and
computes the survival rate from the verification column. Edit the CSV
and every figure in the run moves.
"""
import csv
import json
from pathlib import Path

FLAG_THRESHOLD = 0.60

def parse_claims(text):
    """Parse claims CSV text -> rows with the flag derived from confidence."""
    rows = []
    for r in csv.DictReader(text.splitlines()):
        confidence = float(r["confidence"])
        rows.append({"scene": r["scene"], "region": r["region"],
                     "claim": r["claim"], "confidence": confidence,
                     "flag": "GUESS" if confidence < FLAG_THRESHOLD else "GROUNDED",
                     "verified": r["verified"].strip().lower() == "true"})
    return rows

def load_claims(path):
    return parse_claims(Path(path).read_text(encoding="utf-8"))

def summarise(rows):
    survived = sum(1 for r in rows if r["verified"])
    return {"claims": rows, "total": len(rows), "survived": survived,
            "survival_rate": round(survived / len(rows), 3)}

def main():
    base = Path(__file__).resolve().parents[1]
    print(json.dumps(summarise(load_claims(base / "data" / "claims.csv")), indent=2))

if __name__ == "__main__":
    main()
