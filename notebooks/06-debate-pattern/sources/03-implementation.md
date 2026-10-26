# Implementation — The Debate Pattern (06)

Built: `poc/debate.py` using `kit/transcript.py` (the debate log) and `kit/termination.py` (signal check).
Design: three synthetic contract positions; scripted pro/con argument sets with strengths; the Judge's rule is fixed in code before any debate runs (con − pro margin ≥ 4 → REJECT; ≥ 0 → PAUSE; otherwise PROCEED) and every verdict carries the strongest point each way plus a disagreement score (min/max strength).
Run: `python3 poc/debate.py` → `runs/run-01.txt` + `runs/debate-01.jsonl`.
