# The Business Case — POC Learning Lab
▸ GAI OBSERVE LLC · POC LEARNING LAB — executive brief, 2026-10-26
*Lean edition: the pattern, the money, the industries, the path from demo to deployment.*

## Why this lab exists, in business terms
Most agent projects do not fail on model quality. They fail on trust:
claims nobody can trace, state nobody can audit, and behaviour nobody
contracted for. The three patterns in this lab are the cheapest known
controls for those three failure modes — each demonstrated by a small,
runnable, public reference implementation an executive team can inspect
before it funds anything.

**Honesty note (read first):** the Day 1 notebooks are *scripted
demonstrations over synthetic data*, labelled ILLUSTRATIVE in this
repository. Nothing here is a measured field result. What a measured
pilot looks like is specified at the end — that is the standard we sell
against, and the standard we hold ourselves to.

## Pattern 1 — Grounded perception with a verification loop (POC 01)
**The pattern:** every machine claim names its evidence region, carries
a confidence, and is checked against ground truth; the headline metric
is the *survival rate* — how many claims withstand verification.
**The money:** unverified automation is rework with a latency period.
A verification loop converts silent errors into a priced quantity: the
survival rate tells you, before scale, what fraction of output a human
must still touch.
**Where it applies:**
- Insurance & field services: photo-based claims triage, damage assessment.
- Construction & facilities: site-inspection QA, punch-list verification.
- Retail: shelf and signage audits from store photography.
- Public sector: accessibility audits of public spaces (the demo's case).

## Pattern 2 — The transcript is the system of record (POC 02)
**The pattern:** agents coordinate only through a shared, persisted
transcript; the transcript *is* the state — replayable, auditable,
with no side channels.
**The money:** coordination failures in operations are usually
*provenance* failures — nobody can reconstruct who decided what, from
which data. A transcript-of-record removes the reconstruction cost from
every audit, dispute and incident review, and makes agent work
supervisable by ordinary management tools.
**Where it applies:**
- Contact centres: agent-assist wrap-up, QA sampling, complaint handling.
- Finance operations: reconciliations and exception hunts with a full trail.
- Healthcare administration: multi-step case coordination under audit.
- Shared services / BPO: any workflow where the client may ask "show me".

## Pattern 3 — Contract before capability (POC 03, RODS)
**The pattern:** no agent runs without a four-line contract — Role,
Output, Do-Nots, Signal — checked mechanically (linted) before runtime,
and terminated on a typed signal, never a prose word.
**The money:** incidents with agents are disproportionately contract
incidents: scope the agent invented, output shapes downstream systems
could not consume, runs that never cleanly ended. A lintable contract is
the cheapest control in this entire field — it costs four lines and a
checker, and it prices agent risk *before* deployment.
**Where it applies:**
- Telecom & utilities: regulated customer operations, SLA extraction.
- Banking & insurance: document extraction with explicit do-nots.
- Legal operations: clause and obligation extraction (the demo's case).
- Any enterprise: as the intake gate for every internal agent.

## From demonstration to deployment — the four steps
1. **Pattern fit (days):** pick the pattern, name the business owner and
   the cost line it moves. No pattern, no project.
2. **Measured pilot (weeks):** one site, one workflow, human checkers;
   the demo's illustrative metrics become measured ones (survival rate,
   findings precision, lint catch rate) against a recorded baseline.
3. **Contract & controls (weeks):** RODS contracts for every agent,
   transcript-of-record switched on, verification loop staffed.
4. **Scale decision:** expand only on the measured pilot numbers —
   the same evidence discipline this repository is published under.

## What it costs to start
The reference implementations are free (MIT / CC BY 4.0) and run
offline. The real cost of step 2 is people-time: one business owner,
one engineer, and checker hours for the verification loop. That is the
lean start: evidence first, platform spend after the numbers exist.
