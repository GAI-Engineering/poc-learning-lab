#!/usr/bin/env python3
"""POC 05 - Three Ways to Run a Group Chat.
One task (turn a synthetic referral letter into a prepared appointment
pack) run under three routing shapes: round robin (a queue), selector
(a chair) and swarm (a corridor of handoffs). Same agents, same task -
the routing is the difference, so the comparison table is the lesson.
Deterministic stub agents: no live model. Synthetic letter only.
Agents prepare and propose; booking happens only on human confirmation.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root for kit/
from kit.transcript import TranscriptStore

LETTER = {"patient": "Patient A (synthetic)", "referrer": "GP practice (synthetic)",
          "reason": "persistent knee pain, 6 weeks, physio completed without improvement",
          "requested": "orthopaedics assessment", "urgency": "routine"}

SPECIALISTS = {"Summariser": "reads the letter, extracts the facts",
               "Matcher": "picks the specialty from the summary",
               "Scheduler": "proposes appointment slots for the specialty"}


def summariser(state):
    state["summary"] = f"{LETTER['reason']}; requested: {LETTER['requested']}"
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


def run_round_robin():
    t, state = TranscriptStore(), {}
    for _ in range(2):  # fixed sequence, run twice whether needed or not - that is the queue's cost
        for name in ORDER:
            t.append(name, "turn", AGENTS[name](state))
    return t, finish(state), {"selector_calls": 0, "handoffs": 0}


def run_selector():
    t, state = TranscriptStore(), {}
    selector_calls = 0
    while True:  # the chair decides who speaks next, from state - one model call per turn in a live build
        selector_calls += 1
        nxt = ("Summariser" if "summary" not in state else
               "Matcher" if "specialty" not in state else
               "Scheduler" if "slots" not in state else None)
        if nxt is None:
            break
        t.append("Selector", "route", f"next speaker: {nxt}")
        t.append(nxt, "turn", AGENTS[nxt](state))
    return t, finish(state), {"selector_calls": selector_calls, "handoffs": 0}


def run_swarm():
    t, state = TranscriptStore(), {}
    handoffs = 0
    current = "Summariser"
    while current is not None:  # each agent hands off directly to the next - no chair, no queue
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


def main():
    base = Path(__file__).resolve().parents[1] / "runs"
    rows = []
    for mode, runner in [("round-robin", run_round_robin), ("selector", run_selector), ("swarm", run_swarm)]:
        t, outcome, meta = runner()
        t.save_jsonl(base / f"transcript-{mode}.jsonl")
        agent_turns = sum(1 for m in t.messages if m["kind"] == "turn")
        total_calls = agent_turns + meta["selector_calls"]
        rows.append({"mode": mode, "agent_turns": agent_turns,
                     "selector_calls": meta["selector_calls"], "handoffs": meta["handoffs"],
                     "total_calls": total_calls,
                     "outcome": "pack prepared" if outcome["specialty"] else "INCOMPLETE"})
        print(f"{mode}: turns={agent_turns} selector_calls={meta['selector_calls']} "
              f"handoffs={meta['handoffs']} total_calls={total_calls} outcome={rows[-1]['outcome']}")
    print("All three modes prepared the same pack (specialty orthopaedics, 2 slots, unbooked).")
    print("Difference is governance: turns spent, calls billed, and how traceable the path is.")


if __name__ == "__main__":
    main()
