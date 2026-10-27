# Implementation — RODS (03)

Built: `poc/rods_agent.py` using `kit/rods.py` (parse_rods, lint_rods) and `kit/termination.py` (Termination signal check).
Linter rules: missing field; weak signal (a common prose word such as "Done"); vague output (no table/schema/JSON shape named).
Data: the extraction table is loaded from `data/extraction.csv`. Perturbation test: `tests/test_perturbation.py` (plus the CTO correction probes in `tests/test_cto_corrections.py`).
Run: `python3 poc/rods_agent.py` → `runs/run-01.txt`.
