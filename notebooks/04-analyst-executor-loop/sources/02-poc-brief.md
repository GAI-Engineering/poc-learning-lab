# POC Brief — The Analyst–Executor Loop (04)

**Idea:** Find the leaks in a household budget from a transaction export, with an analyst that writes code and an executor that runs it — iterating on real output and real errors.
**Build steps:** (1) Two roles share only a transcript (`kit/transcript.py`). (2) The Analyst drafts code per question; the Executor runs it in a teaching-only in-process executor and returns output or the verbatim error as a message. (3) Failed attempts stay in the transcript — the Analyst's revisions exist because the errors were legible. (4) Terminate on the signal ANALYSIS COMPLETE or the turn cap.
**Guardrail:** Education, not financial advice. Synthetic data only; the executor here is teaching-only (in-process exec, restricted builtins over an in-memory copy) — a restricted builtin set is not an isolation boundary; production means an isolated runner.
**Win condition:** Findings trace to actual rows of the export, not generic money tips; every error in the run is printed, read, and answered by a revision.
Data: synthetic only. Model: deterministic stub, no live model.
