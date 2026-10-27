# Implementation — The Analyst–Executor Loop (04)

Built: `poc/analyst_executor.py` using `kit/transcript.py` (TranscriptStore) and `kit/termination.py` (signal + cap).
Design: Analyst code → in-process exec (restricted builtins, only the copied export visible - a teaching executor, not an isolation boundary) → output or verbatim error returned as a transcript message → Analyst revises. Five attempts: a KeyError on an assumed column name, the schema-print recovery, the corrected totals, an empty result from a wrong category name, and the corrected leak query.
Run: `python3 poc/analyst_executor.py` → `runs/run-01.txt` + `runs/transcript-01.jsonl`.
