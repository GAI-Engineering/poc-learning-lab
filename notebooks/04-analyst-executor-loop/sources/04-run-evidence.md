# Run Evidence — The Analyst–Executor Loop (04)

Label: **ILLUSTRATIVE** — scripted demonstration: from `runs/run-01.txt` (executed 2026-10-26, deterministic stub, synthetic transactions); the analyst's attempts are scripted for the lesson, so the attempt outcomes illustrate the pattern — against a live model this is where measured attempt data would land.

- Attempts: 5 — 3 SUCCESS, 1 ERROR (KeyError: 'amt' — an assumed column name, returned verbatim and answered by printing the schema), 1 EMPTY (category 'gym' matched no rows; the exact name 'gym-unused' came from the totals table).
- Finding: gym-unused totals $78.00 across Feb–Mar with no activity category in the export — computed from the export rows by the corrected code.
- Termination: ANALYSIS COMPLETE → TERMINATION: SIGNAL.
- Data: `data/attempts.csv`, `data/leaks.csv` (ILLUSTRATIVE). Chart: drawn live in the notebook from the attempts table (ILLUSTRATIVE).
