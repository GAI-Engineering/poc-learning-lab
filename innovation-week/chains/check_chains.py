#!/usr/bin/env python3
"""check_chains.py - verify the expected outputs of the Innovation Week
chaining exercises (innovation-week/CHAINING-EXERCISES.md).

This is NOT a new POC. It imports the six Month 1 POC modules and the
shared kit as they are, joins them with a few lines of glue, and checks
every expected output the exercises print. Each chain also runs a
NEGATIVE CONTROL: a change that must move or block the result. If the
glue faked a figure, the control would fail.

  python innovation-week/chains/check_chains.py      exit 0 = all checks pass

Standard library only. Synthetic data only (the POCs' own data files).
Every figure is ILLUSTRATIVE: these are scripted demonstrations.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NB = ROOT / "notebooks"
sys.path.insert(0, str(ROOT))
from kit.rods import parse_rods, lint_rods          # noqa: E402
from kit.termination import Termination              # noqa: E402
from kit.transcript import TranscriptStore           # noqa: E402

RESULTS = []


def load(name, rel):
    """Import a POC module by file path under a unique name."""
    spec = importlib.util.spec_from_file_location(name, NB / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sees = load("poc01_sees", "01-agent-that-sees/poc/sees.py")
conv = load("poc02_conversation", "02-conversation-is-coordination/poc/conversation.py")
rods_agent = load("poc03_rods", "03-rods/poc/rods_agent.py")
loop = load("poc04_loop", "04-analyst-executor-loop/poc/analyst_executor.py")
chat = load("poc05_chat", "05-group-chat-patterns/poc/group_chat.py")
debate = load("poc06_debate", "06-debate-pattern/poc/debate.py")


def check(chain, label, got, want):
    ok = got == want
    RESULTS.append(ok)
    print(f"  {'PASS' if ok else 'FAIL'}  {chain} {label}: got {got!r}" + ("" if ok else f", want {want!r}"))


# ---------------------------------------------------------------- Chain 1
# POC 03 gate -> POC 04 loop -> POC 02 findings, one shared transcript.
def contract_gate(contract_text):
    """Glue: the RODS lint is a gate. Any issue blocks the run."""
    issues = lint_rods(parse_rods(contract_text))
    return ("OPEN" if not issues else "BLOCKED"), issues


def chain1(rows_path, contract_text):
    gate, issues = contract_gate(contract_text)
    shared = TranscriptStore()
    shared.append("Gate", "lint", "CLEAN" if not issues else "; ".join(issues))
    if gate == "BLOCKED":
        shared.append("Gate", "signal", "RUN BLOCKED")
        return gate, None, None, shared
    rows = loop.load_rows(rows_path)
    t4, attempts, finding, terminated_by = loop.analyse(rows)
    for m in t4.messages:
        shared.append(m["speaker"], m["kind"], m["content"])
    tx = conv.load_tx(rows_path)
    _, findings = conv.compute_findings(tx)
    for f in findings:
        shared.append("Analyst-02", "finding", f)
    return gate, finding, findings, shared


def run_chain1():
    print("Chain 1 - contract gate -> analyst-executor loop -> unasked-for findings")
    data = NB / "04-analyst-executor-loop/data/transactions.csv"
    gate, finding, findings, shared = chain1(data, rods_agent.CONTRACT)
    check("C1", "gate", gate, "OPEN")
    check("C1", "loop finding names $78.00", "$78.00" in finding, True)
    check("C1", "POC 02 findings count", len(findings), 3)
    check("C1", "both components agree on the leak", "$78.00" in findings[0], True)
    kinds = {}
    for m in shared.messages:
        kinds[m["kind"]] = kinds.get(m["kind"], 0) + 1
    check("C1", "shared transcript messages", len(shared), 16)
    check("C1", "shared transcript errors kept", kinds.get("error"), 1)
    # Negative control A: the bad contract must block the whole chain.
    gate_bad, f_bad, _, shared_bad = chain1(data, rods_agent.BAD_CONTRACT)
    check("C1", "NEG bad contract blocks", (gate_bad, f_bad, len(shared_bad)), ("BLOCKED", None, 2))
    # Negative control B: change the gym amount; both findings must move together.
    tmp = Path(__file__).with_name("_tmp_tx.csv")
    text = data.read_text(encoding="utf-8").replace("gym-unused,39.0", "gym-unused,49.0")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    try:
        _, f2, fs2, _ = chain1(tmp, rods_agent.CONTRACT)
    finally:
        tmp.unlink()
    check("C1", "NEG perturbed leak moves in POC 04", "$98.00" in f2, True)
    check("C1", "NEG perturbed leak moves in POC 02", "$98.00" in fs2[0], True)


# ---------------------------------------------------------------- Chain 2
# POC 01 confidence map -> POC 05-style router: GUESS -> human queue.
def route_claims(rows, threshold):
    """Glue: re-derive the flag at a stated threshold, then route."""
    report, human = [], []
    for r in rows:
        (human if r["confidence"] < threshold else report).append(r)
    return report, human


def run_chain2():
    print("Chain 2 - confidence map -> routing: guesses go to a person")
    rows = sees.load_claims(NB / "01-agent-that-sees/data/claims.csv")
    s = sees.summarise(rows)
    check("C2", "claims / survived / rate", (s["total"], s["survived"], s["survival_rate"]), (13, 10, 0.769))
    report, human = route_claims(rows, sees.FLAG_THRESHOLD)
    check("C2", "report / human queue at 0.60", (len(report), len(human)), (10, 3))
    check("C2", "every human-queue claim failed the scripted check", all(not r["verified"] for r in human), True)
    # Negative control: a stricter threshold must grow the human queue.
    _, human80 = route_claims(rows, 0.80)
    check("C2", "NEG human queue at 0.80", len(human80), 5)


# ---------------------------------------------------------------- Chain 3
# POC 06 debate -> machine-readable verdict -> human gate (POC 05 rule).
def gate_verdicts(rows):
    """Glue: only PROCEED passes on; PAUSE and the closest fight go to a person."""
    closest = max(rows, key=lambda r: r["disagreement"])["claim"] if rows else None
    out = []
    for r in rows:
        to_human = r["verdict"] == "PAUSE" or r["claim"] == closest
        out.append((r["claim"], r["verdict"], "HUMAN" if to_human else "AUTO-RECORD"))
    return out


def run_chain3():
    print("Chain 3 - debate verdicts -> human gate")
    claims = debate.load_claims(NB / "06-debate-pattern/data/claims.csv")
    _, rows, term = debate.run_debate(claims)
    check("C3", "verdicts", [r["verdict"] for r in rows], ["REJECT", "PROCEED", "REJECT"])
    check("C3", "all verdicts parseable", all(r["verdict"] in ("PROCEED", "PAUSE", "REJECT") for r in rows), True)
    check("C3", "routing", gate_verdicts(rows),
          [("C1", "REJECT", "AUTO-RECORD"), ("C2", "PROCEED", "HUMAN"), ("C3", "REJECT", "AUTO-RECORD")])
    check("C3", "termination", term, "SIGNAL")
    # Negative control: make C1 a tie; the fixed rule must say PAUSE and route it to a person.
    tied = copy.deepcopy(claims)
    tied[0]["pro"].append(("added for the control", 6))
    _, rows_t, _ = debate.run_debate(tied)
    check("C3", "NEG tie -> PAUSE -> HUMAN", gate_verdicts(rows_t)[0], ("C1", "PAUSE", "HUMAN"))


# ---------------------------------------------------------------- Chain 4
# POC 05 shapes over one letter -> the transcript is the audit (POC 02).
def run_chain4():
    print("Chain 4 - three routing shapes -> audit from the transcripts alone")
    letter = chat.load_letter(NB / "05-group-chat-patterns/data/letter.json")
    transcripts, rows = chat.run_all(letter)
    check("C4", "total_calls per shape", [r["total_calls"] for r in rows], [6, 7, 4])
    booked = [runner(letter)[1]["booked"] for runner in
              (chat.run_round_robin, chat.run_selector, chat.run_swarm)]
    check("C4", "nothing booked (human gate)", booked, [False, False, False])
    # Audit: write each transcript to JSONL, then re-count agent turns from
    # the file alone - not from the run's own comparison table.
    recount = {}
    tmp = Path(__file__).with_name("_tmp_transcript.jsonl")
    try:
        for mode, t in transcripts.items():
            t.save_jsonl(tmp)
            lines = [json.loads(x) for x in tmp.read_text(encoding="utf-8").splitlines() if x]
            recount[mode] = sum(1 for m in lines if m["kind"] == "turn")
    finally:
        if tmp.exists():
            tmp.unlink()
    check("C4", "audit recount of agent turns", recount, {"round-robin": 6, "selector": 3, "swarm": 4})
    # Negative control: a router stuck on the Matcher must hit the cap, not
    # loop. It still emits a plausible-looking specialty ('general', not
    # 'orthopaedics') because the summary was never written - only the
    # termination record shows the run went wrong.
    t_bad, out_bad, _ = chat.run_selector(letter, chooser=lambda s: "Matcher", max_turns=5)
    capped = any(m["kind"] == "termination" for m in t_bad.messages)
    check("C4", "NEG stuck router capped, field looks plausible", (capped, out_bad["specialty"]),
          (True, "general"))


# ---------------------------------------------------------------- Chain 5
# kit Termination as the shared contract between steps.
def run_chain5():
    print("Chain 5 - one typed signal ends each step")
    term = Termination(max_turns=3, signal="STEP COMPLETE")
    check("C5", "exact signal", term.check("STEP COMPLETE"), "SIGNAL")
    check("C5", "NEG prose word is not a signal", Termination(5, "STEP COMPLETE").check("done"), None)
    capped = Termination(max_turns=2, signal="STEP COMPLETE")
    capped.check("working")
    check("C5", "NEG cap ends a run that never signals", capped.check("still working"), "CAP_TURNS")


def main():
    for fn in (run_chain1, run_chain2, run_chain3, run_chain4, run_chain5):
        fn()
    passed = sum(RESULTS)
    print(f"checks={len(RESULTS)} passed={passed} failed={len(RESULTS) - passed}")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
