# Implementation — Conversation Is a Coordination Primitive (02)

Built: `poc/conversation.py` using `kit/transcript.py` (TranscriptStore).
Design: Analyst questions → Executor results → follow-up questions that only exist because of earlier results (exploratory path a pipeline cannot pre-write). Transcript saved to `runs/transcript-01.jsonl`.
Data: `data/transactions.csv` is the input of record — every finding is computed from it (unused-charge totals, monthly count changes, subscription-class overlap). Perturbation test: `tests/test_perturbation.py`.
Run: `python3 poc/conversation.py` → `runs/run-01.txt` + transcript.
