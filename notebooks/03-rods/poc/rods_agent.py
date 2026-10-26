#!/usr/bin/env python3
"""POC 03 - RODS: Four Lines Every Agent Needs.
A RODS-written clause analyst: role / fixed table output / do-nots /
signal EXTRACTION COMPLETE. Uses kit.rods loader+linter and
kit.termination signal check. Synthetic clauses only; no legal advice.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from kit.rods import parse_rods, lint_rods
from kit.termination import Termination

CONTRACT = """    Role: Clause analyst. Extract obligations from contract clauses into a fixed schema. You do not interpret intent.
Output: A markdown table with columns party | duty | deadline, one row per obligation.
Do-Nots: No legal advice. No obligations not stated in the clause. Do not address any party not named.
Signal: EXTRACTION COMPLETE
"""
BAD_CONTRACT = """    Role: Helpful assistant.
Output: A summary.
Signal: Done
"""
CLAUSES = [
    {"clause": "C1", "party": "Supplier", "duty": "deliver monthly uptime report", "deadline": "5th business day"},
    {"clause": "C2", "party": "Client", "duty": "pay undisputed invoices", "deadline": "30 days from invoice"},
    {"clause": "C3", "party": "Supplier", "duty": "notify of security incidents", "deadline": "24 hours from discovery"},
    {"clause": "C4", "party": "Both", "duty": "review service levels jointly", "deadline": "quarterly"},
]

def main():
    contract = parse_rods(CONTRACT)
    print("CONTRACT fields:", sorted(contract.keys()))
    print("LINT good contract:", lint_rods(contract) or "CLEAN")
    print("LINT bad contract:", lint_rods(parse_rods(BAD_CONTRACT)))
    term = Termination(max_turns=10, signal=contract["Signal"])
    print("| party | duty | deadline |")
    print("|---|---|---|")
    for c in CLAUSES:
        print(f"| {c['party']} | {c['duty']} | {c['deadline']} |")
    final = "EXTRACTION COMPLETE"
    print(final)
    print("TERMINATION:", term.check(final))

if __name__ == "__main__":
    main()
