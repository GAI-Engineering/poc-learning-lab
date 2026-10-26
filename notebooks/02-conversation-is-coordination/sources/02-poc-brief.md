# POC Brief — Conversation Is a Coordination Primitive (02)

**Idea:** Explore a year-equivalent synthetic transaction export and surface what matters, through conversation rather than a fixed pipeline.
**Build steps:** (1) Two agents (Analyst, Executor) share only a TranscriptStore. (2) Executor runs sandboxed analysis functions over a copied synthetic export. (3) Transcript persisted as JSONL — the transcript is the state store. (4) Findings appended to the transcript and signalled.
**Guardrail:** Works on a copied export — never on live bank access.
**Win condition:** Three findings the owner did not know to ask for.
Data: synthetic only. Model: deterministic stub.
