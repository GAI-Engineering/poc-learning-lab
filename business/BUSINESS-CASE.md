<img src="../assets/gai-observe-logo.png" alt="GAI Observe LLC" width="140">

# The Business Case — POC Learning Lab
▸ GAI OBSERVE LLC · POC LEARNING LAB — executive brief, 2026-10-26
*Lean edition: the pattern, the money, the industries, the path from demo to deployment.*

## Lead with the data — the market, and the failure curve
**The market (third-party forecasts, cited — not our numbers):**
- Enterprise agentic AI: **USD 2.58B in 2024 → USD 24.5B by 2030**;
  Grand View Research states the 46.2% CAGR for 2025–2030
  (Enterprise Agentic AI Market Report, 2025–2030).
- Forecasts vary by definition and scope — Omdia's software-only
  forecast is USD 1.5B in 2025 → USD 41.8B in 2030. Treat any single
  figure as a named estimate, never as a promise.
- Adoption: Gartner (Aug 2025) predicts **40% of enterprise
  applications will feature task-specific AI agents by end of 2026**,
  up from under 5% in 2025; by 2029 at least 50% of knowledge workers
  will develop skills to work with, govern or create agents.

**The failure curve (why this lab leads with controls, not demos):**
Gartner (June 2025) also predicts **over 40% of agentic AI projects
will be canceled by end of 2027**. Gartner lists escalating costs,
unclear business value and inadequate risk controls. The three
patterns below address those listed causes — a verification loop
makes value testable, a transcript-of-record is the audit trail, and
a linted contract is a pre-runtime risk control.

**Our data (separate ledger, always labelled):** everything this lab
has produced so far is ILLUSTRATIVE — scripted demonstrations over
synthetic data (see the honesty note in the patterns and
KEY-DATA-POINTS.md). Market figures are other people's, cited;
pilot figures will be ours only when a real pilot runs.

## Why this lab exists, in business terms
In our assessment, the business problem is trust: claims nobody can
trace, state nobody can audit, and behaviour nobody contracted for.
The three patterns in this lab are low-cost controls for those three
failure modes — each demonstrated by a small, runnable, public
reference implementation an executive team can inspect before it
funds anything.

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
which data. A transcript-of-record collapses the reconstruction cost in
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
**The money:** the failure mode this pattern targets is
contract-shaped: scope the agent invented, output shapes downstream
systems could not consume, runs that never cleanly ended. A lintable
contract is a low-cost control — it costs four lines and a checker,
and it surfaces agent risk *before* deployment.
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

## Sources (market section)
- Grand View Research — Enterprise Agentic AI Market Report 2025–2030:
  https://Www.grandviewresearch.com/industry-analysis/enterprise-agentic-ai-market-report
- Gartner press release, 2025-08-26 — 40% of enterprise apps to feature
  task-specific AI agents by 2026:
  https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025
- Omdia — Enterprise Agentic AI Software Market Forecast (Sep 2025):
  https://omdia.tech.informa.com/pr/2025/sep/new-omdia-analysis-shows-agentic-ai-outpacing-growth-rates-of-traditional-generative-ai
- Gartner cancellation prediction (June 2025), as widely reported.
