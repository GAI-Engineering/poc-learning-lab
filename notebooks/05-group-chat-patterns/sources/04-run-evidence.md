# Run Evidence — Three Ways to Run a Group Chat (05)

Label: **ILLUSTRATIVE** — scripted demonstration: from `runs/run-01.txt` (executed 2026-10-26, deterministic stubs, synthetic referral letter); the agents' behaviours are scripted, so the counts are the mechanics of this script for each routing shape — against live agents this is where measured turn/cost data would land.

- Round robin: 6 agent turns, 0 selector calls, 0 handoffs, 6 total calls — pack prepared.
- Selector: 3 agent turns, 4 selector calls, 0 handoffs, 7 total calls — pack prepared. Fewest turns, most calls: in this script the chair spends a routing decision on every turn, including the final stop-check.
- Swarm: 4 agent turns, 0 selector calls, 3 handoffs, 4 total calls — pack prepared, including a verification hand-back.
- All three modes produced the same pack (specialty: orthopaedics; slots Tue 09:30 / Wed 14:10; booked: false — human confirmation required).
- Input: `data/letter.json` — the letter the run reads. Results: `runs/routing-comparison.csv`, written by the run itself (ILLUSTRATIVE). Chart: drawn in the notebook from the run's own results table (ILLUSTRATIVE).
