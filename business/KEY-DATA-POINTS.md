<img src="../assets/gai-observe-logo.png" alt="GAI Observe LLC" width="140">

# Key Data Points — POC Learning Lab
▸ GAI OBSERVE LLC · POC LEARNING LAB — chart-ready figures for posts, 2026-10-26
*Provenance rule: every Day 1 figure is ILLUSTRATIVE — from scripted
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

## The executive layer
- Infographics (business/infographics/): the SVG sources are the
  figures of record — one CTO conclusion each, drawn from the data
  above. The NotebookLM PNG renders were WITHDRAWN 2026-10-26
  (review E-8): their rendered text misstated figures on this page.
  PNG renders return only after regeneration + a full human check of
  every figure and label against this page.
- Business case: business/BUSINESS-CASE.md · Deck: business/POC-BUSINESS-CASE-DECK
- Concept diagrams: diagrams/CONCEPT-DIAGRAMS.md · Technical flows: diagrams/TECHNICAL-FLOWS.md
