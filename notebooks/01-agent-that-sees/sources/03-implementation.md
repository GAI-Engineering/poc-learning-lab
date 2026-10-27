# Implementation — An Agent That Sees (01)

Built: `poc/sees.py` — a layered scene parser over three synthetic scenes (pavement, entrance, crossing), 13 region claims.
Design: PERCEIVE (regions) → RELATE (region labels carry spatial relations) → INTERPRET (accessibility-relevant objects named) → VERIFY (recorded human check per claim).
Data: `data/claims.csv` is the input of record — scenes, claims, confidences and the recorded human verification live in the data file; the code derives each flag from its confidence and computes the survival rate. Perturbation test: `tests/test_perturbation.py`.
Run: `python3 poc/sees.py` → `runs/run-01.json`.
Shared kit: none required for this minimal build; transcript/termination primitives are introduced in POCs 02–03 and reused later.
