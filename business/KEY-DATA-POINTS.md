<img src="../assets/gai-observe-logo.png" alt="GAI Observe LLC" width="140">

# Key Data Points — POC Learning Lab
▸ GAI OBSERVE LLC · POC LEARNING LAB — chart-ready figures for posts, 2026-10-26
*Provenance rule: every figure in this file is ILLUSTRATIVE — from scripted
demonstrations over synthetic data, executed and recorded in this repo.
Quote them only with that label attached. Measured figures replace
these only from real pilot runs, never by editing this file's labels.*

## POC 01 · An Agent That Sees
- 13 region claims · 10 survived verification · survival rate 0.769
- Flag rule: confidence < 0.60 = GUESS (flagged, not hidden)
- The 3 failed claims are exactly the 3 flagged (0.42 / 0.35 / 0.48) — in
  the demo this holds by construction; the lesson is the loop, not the rate
- Flip one verification outcome and the headline moves to 0.692 — try it
  live in the notebook (§ "Change one outcome")

## POC 02 · Conversation Is a Coordination Primitive
- 12 transcript messages · 4 tasks · 2 agents · 0 side channels
- 3 unasked-for findings: $78.00 unused gym charge (Feb–Mar) · coffee
  subscription billed 3x in March vs 2x · second streaming sub started March
- State = the transcript file; replay and audit read it alone

## POC 03 · RODS
- Contract = 4 lines (Role · Output · Do-Nots · Signal)
- Good contract: lint CLEAN · Bad contract: 3 flags (MISSING Do-Nots,
  WEAK_SIGNAL, VAGUE_OUTPUT)
- Extraction: 4 obligations · termination on the typed signal
  EXTRACTION COMPLETE (check returned SIGNAL, never a prose word)

## POC 04 · The Analyst–Executor Loop
- 5 attempts · 1 ERROR · 1 EMPTY · 3 SUCCESS — outcomes computed from
  the run record (runs/attempts.csv), never typed into the summary
- The error was a wrong key ('amt'); the recovery habit — print the
  schema first — is attempt 2, and the revised query succeeds
- EMPTY means the question was wrong (category 'gym' matches no rows);
  the exact name from the totals ('gym-unused') succeeds
- Finding: gym-unused totals $78.00 (2 x $39.00, 2026-02 and 2026-03),
  traced to rows in data/transactions.csv (22 rows)
- Change a figure in the CSV and the finding moves — the perturbation
  test moves the gym amounts and watches $78.00 become $98.00
  (tests/test_perturbation.py)

## POC 05 · Three Ways to Run a Group Chat
- Same job, three shapes, counted from runs/routing-comparison.csv:
  round robin 6 agent turns / 6 total calls · selector 3 agent turns +
  4 routing calls / 7 total · swarm 4 agent turns + 3 hand-offs / 4 total
- All three modes prepared the same pack (specialty orthopaedics,
  2 slots — Tue 09:30, Wed 14:10 — unbooked, awaiting human confirmation)
- These counts are the mechanics of this script — round robin runs its
  sequence twice by construction; the swarm takes a verification
  hand-back by construction. They are not live routing costs.
- A router that can never finish is capped and ends INCOMPLETE
  (tests/test_perturbation.py, failed-router case)

## POC 06 · The Debate Pattern
- 3 positions debated (runs/verdicts.csv): C1 auto-renewal at +8% —
  REJECT (strength 5 for / 11 against) · C2 24-hour incident-notice
  duty — PROCEED (8 / 5) · C3 uncapped liability — REJECT (2 / 14)
- Closest fight: C2, balance 0.62 — the most balanced argument in the
  script and the reviewer's first stop
- The balance map is an illustrative argument-balance prompt for human
  review: it locates no genuine uncertainty, is not a risk register,
  and a real position requires independent evidence and counsel review
- Adding a fourth position produces four verdicts — the counts are
  computed, not typed (tests/test_perturbation.py)

## The executive layer
- Infographics (business/infographics/): the SVG sources are the
  figures of record — one CTO conclusion each, drawn from the data
  above. PNG copies beside them are rendered FROM the SVGs
  (SE-18, 2026-10-26). The earlier NotebookLM PNG renders were
  WITHDRAWN 2026-10-26 (review E-8): their rendered text misstated
  figures on this page. See business/infographics/README.md.
- Business case: business/BUSINESS-CASE.md (Patterns 1–6, one per POC,
  each with its concept diagram embedded) · Deck: business/POC-BUSINESS-CASE-DECK
- Concept diagrams: diagrams/CONCEPT-DIAGRAMS.md · Technical flows:
  diagrams/TECHNICAL-FLOWS.md — both cover all six POCs; every notebook
  also carries its own technical flow in its "How it is built" section.
- Day 2 infographics (04–06) were added 2026-10-26 in the Day 1
  template, figures from the run data on this page, PNGs rendered from
  the SVGs and read at full size before use.
