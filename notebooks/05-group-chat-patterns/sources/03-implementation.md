# Implementation — Three Ways to Run a Group Chat (05)

Built: `poc/group_chat.py` using `kit/transcript.py` (one persisted transcript per mode).
Design: shared stub agents and shared state; only the router changes. Round robin runs the fixed sequence twice (6 turns — including turns the task did not need). The selector evaluates state before each turn (4 selector calls for 3 agent turns — the chair itself is a call, and in a live build a model call). The swarm hands off directly (4 turns, 3 handoffs, including the Scheduler → Summariser verification hand-back) — fewest calls, hardest path to trace.
Run: `python3 poc/group_chat.py` → `runs/run-01.txt` + `runs/transcript-<mode>.jsonl` ×3.
