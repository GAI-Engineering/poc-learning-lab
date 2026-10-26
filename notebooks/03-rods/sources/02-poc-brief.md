# POC Brief — RODS: Four Lines Every Agent Needs (03)

**Idea:** Extract obligations from contract clauses into a fixed schema, using an agent whose whole contract is four RODS lines.
**Build steps:** (1) Write the RODS contract (Role / Output / Do-Nots / Signal: EXTRACTION COMPLETE). (2) Load and lint it with `kit/rods.py`. (3) Lint a deliberately bad contract for contrast. (4) Extract four synthetic clauses into the party | duty | deadline table; terminate on the signal.
**Guardrail:** Output feeds a lawyer's review queue. It decides nothing; no legal advice.
**Win condition:** A second person can parse every reply without reading prose; termination is signal-based, verified in the run log.
Data: synthetic only. Model: deterministic stub.
