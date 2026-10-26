# Implementation — RODS (03)

Built: `poc/rods_agent.py` using `kit/rods.py` (parse_rods, lint_rods) and `kit/termination.py` (Termination signal check).
Linter rules: missing field; weak signal (a common prose word such as "Done"); vague output (no table/schema/JSON shape named).
Run: `python3 poc/rods_agent.py` → `runs/run-01.txt`.
