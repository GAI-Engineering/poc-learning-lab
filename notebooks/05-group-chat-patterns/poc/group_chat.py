#!/usr/bin/env python3
"""POC 05 - Three Ways to Run a Group Chat.
One task (turn a synthetic referral letter into a prepared appointment
pack) run under three routing shapes: round robin (a queue), selector
(a chair) and swarm (a corridor of handoffs). Same agents, same task -
the routing is the difference, so the comparison table is the lesson.
Deterministic stub agents: no live model. The letter is read from
data/letter.json - the data file is the single source for the run.
Agents prepare and propose; booking happens only on human confirmation.
The counts this run prints are the mechanics of THIS script (round
robin runs its sequence twice by construction; the swarm takes a
verification hand-back by construction). They show what each shape
does in the demo - they are not evidence of what a live system would
cost, earn, or how hard a real trace would be.
"""
import csv
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root for kit/
from kit.transcript import TranscriptStore

MAX_TURNS = 12  # enforced cap for the selector and swarm loops


def load_letter(path):
    """Load the synthetic referral letter from its data file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summariser(state):
    letter = state["letter"]
    state["summary"] = f"{letter['reason']}; requested: {letter['requested']}"
    return "summary written"


def matcher(state):
    state["specialty"] = "orthopaedics" if "knee" in state.get("summary", "") else "general"
    return f"specialty = {state['specialty']}"


def scheduler(state):
    state["slots"] = ["Tue 09:30", "Wed 14:10"] if state.get("specialty") else []
    return f"slots proposed: {state['slots']} (unbooked - awaiting human confirmation)"


AGENTS = {"Summariser": summariser, "Matcher": matcher, "Scheduler": scheduler}
ORDER = ["Summariser", "Matcher", "Scheduler"]


def finish(state):
    return {"specialty": state.get("specialty"), "slots": state.get("slots", []),
            "booked": False, "note": "prepared pack only - booking requires human confirmation"}


def run_round_robin(letter):
    t, state = TranscriptStore(), {"letter": letter}
    for _ in range(2):  # fixed sequence, run twice whether needed or not - that is the queue's cost
        for name in ORDER:
            t.append(name, "turn", AGENTS[name](state))
    return t, finish(state), {"selector_calls": 0, "handoffs": 0}


def choose_next(state):
    """The chair's rule: the first missing piece decides who speaks."""
    return ("Summariser" if "summary" not in state else
            "Matcher" if "specialty" not in state else
            "Scheduler" if "slots" not in state else None)


def run_selector(letter, chooser=choose_next, max_turns=MAX_TURNS):
    """The chair decides who speaks next, from state. The turn cap is
    enforced inside the loop: a router that never finishes (a failed
    router) hits the cap and the run ends INCOMPLETE instead of
    looping forever."""
    t, state = TranscriptStore(), {"letter": letter}
    selector_calls = 0
    turns = 0
    while turns < max_turns:
        selector_calls += 1
        nxt = chooser(state)
        if nxt is None:
            break
        turns += 1
        t.append("Selector", "route", f"next speaker: {nxt}")
        t.append(nxt, "turn", AGENTS[nxt](state))
    else:
        t.append("Selector", "termination",
                 f"turn cap {max_turns} reached - router never finished; run INCOMPLETE")
    return t, finish(state), {"selector_calls": selector_calls, "handoffs": 0}


def run_swarm(letter, max_turns=MAX_TURNS):
    t, state = TranscriptStore(), {"letter": letter}
    handoffs = 0
    current = "Summariser"
    steps = 0
    while current is not None and steps < max_turns:  # each agent hands off directly - no chair, no queue
        steps += 1
        t.append(current, "turn", AGENTS[current](state))
        nxt = {"Summariser": "Matcher", "Matcher": "Scheduler", "Scheduler": "Summariser"}.get(current)
        if current == "Summariser" and "verified" in state:
            nxt = None
        if current == "Scheduler":
            state["verified"] = True  # scheduler hands back to summariser for a verification pass
        if nxt:
            handoffs += 1
            t.append(current, "handoff", f"hands off to {nxt}")
        current = nxt
    return t, finish(state), {"selector_calls": 0, "handoffs": handoffs}


def run_all(letter):
    """Run all three shapes over the same letter; every figure in the
    returned rows is counted from the run records, never typed in."""
    transcripts, rows = {}, []
    for mode, runner in [("round-robin", run_round_robin), ("selector", run_selector),
                         ("swarm", run_swarm)]:
        t, outcome, meta = runner(letter)
        transcripts[mode] = t
        agent_turns = sum(1 for m in t.messages if m["kind"] == "turn")
        total_calls = agent_turns + meta["selector_calls"]
        rows.append({"mode": mode, "agent_turns": agent_turns,
                     "selector_calls": meta["selector_calls"], "handoffs": meta["handoffs"],
                     "total_calls": total_calls,
                     "outcome": "pack prepared" if outcome["specialty"] else "INCOMPLETE",
                     "specialty": outcome["specialty"], "slots": outcome["slots"]})
    return transcripts, rows


def main():
    base = Path(__file__).resolve().parents[1]
    letter = load_letter(base / "data" / "letter.json")
    transcripts, rows = run_all(letter)
    for mode, t in transcripts.items():
        t.save_jsonl(base / "runs" / f"transcript-{mode}.jsonl")
    with open(base / "runs" / "routing-comparison.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["mode", "agent_turns", "selector_calls", "handoffs", "total_calls", "outcome"])
        for r in rows:
            w.writerow([r["mode"], r["agent_turns"], r["selector_calls"], r["handoffs"],
                        r["total_calls"], r["outcome"]])
    for r in rows:
        print(f"{r['mode']}: turns={r['agent_turns']} selector_calls={r['selector_calls']} "
              f"handoffs={r['handoffs']} total_calls={r['total_calls']} outcome={r['outcome']}")
    prepared = [r for r in rows if r["outcome"] == "pack prepared"]
    if len(prepared) == len(rows) and len({r["specialty"] for r in rows}) == 1:
        r0 = rows[0]
        print(f"All three modes prepared the same pack (specialty {r0['specialty']}, "
              f"{len(r0['slots'])} slots, unbooked).")
    else:
        print("Modes did NOT all prepare the pack: " +
              ", ".join(f"{r['mode']}={r['outcome']}" for r in rows) + ".")
    print("These counts are the mechanics of this script - round robin runs its sequence twice "
          "by construction and the swarm takes a verification hand-back by construction. They "
          "show what each shape does in the demo, not what a live routing mode costs or how "
          "hard a real path is to trace.")


if __name__ == "__main__":
    main()
