▸ GAI OBSERVE LLC · POC LEARNING LAB
# Combination Use and Industry Map — POCs 01–06

*DRAFT, 2026-11-19. Component IDs (K1–K4, A–F) are defined in
`COMPONENT-CATALOGUE.md`. Each combination below is a **design pattern for
discussion**, not a built system and not a new POC. Where a combination is
exercised in code, it is by `innovation-week/chains/check_chains.py` (glue
only, synthetic data, ILLUSTRATIVE).*

## 1. Combinations

### CB-1 · The governed analyst — RODS gate → Analyst–Executor loop → unasked-for findings
**Parts.** K3 → D1–D3 → B2, all writing to one K1 transcript.
**Flow.** The contract is linted. Only a CLEAN contract opens the run. The loop
types every attempt. The POC 02 findings pass runs over the same export.
**Exercised.** Chain 1: both components report the same $78.00 leak; a bad
contract blocks the run (2 messages, no finding); moving the gym amount moves
both findings to $98.00.
**Preconditions.** A written contract per agent. A copied export, never live
access. In production, an isolated executor (D2 is teaching-only).
**Risks.** The POC 02 finders rely on category naming (`-unused`,
`-subscription`, `streaming-`). Real exports will not follow that convention.

### CB-2 · Seen, then checked — Confidence map → routing → a person
**Parts.** A1–A4 → a routing rule in the spirit of E3 → human review, recorded in K1.
**Flow.** GROUNDED claims go to the report. GUESS claims go to a person.
**Exercised.** Chain 2: at 0.60, 10 to the report and 3 to a person; at 0.80, 5 to a person.
**Preconditions.** Calibrated confidences and held-out labels (the CTO review's HOLD conditions for POC 01).
**Risks.** In the demo the guesses fail by construction. A real model may be confidently wrong; the threshold then routes errors past the person.

### CB-3 · The argued decision record — RODS advocates → debate → human gate
**Parts.** K3 contracts for Proponent, Opponent and Judge → F1–F3 → the E5 human-gate rule → K1.
**Flow.** Verdicts are parsed by machine. PAUSE and the closest fight go to a person; the rest are recorded.
**Exercised.** Chain 3: C2 (PROCEED, closest fight) goes to a person; forcing a tie on C1 gives PAUSE and routes it to a person.
**Preconditions.** The judge's rule is written before the debate. Each side argues from a stated evidence list.
**Risks.** Strengths are scripted in Month 1. With live models, advocates may drift toward agreement; RODS Do-Nots must forbid conceding.

### CB-4 · The routed case team — specialists under a chair, each with a contract
**Parts.** E1 specialists, each with a K3 contract → E3 selector with K2 cap → E5 pack → K4 SessionLog row per case.
**Exercised.** Chain 4: turn counts re-counted from the saved JSONL match the run's own table (6 / 3 / 4); a stuck router is capped.
**Preconditions.** A stop rule for the chair. A cap. A human gate on any act with consequences.
**Risks.** Gap G3: a capped run can still emit a plausible field. Check the termination record, not just the output. Gap G2: shared state means one specialist can overwrite another.

### CB-5 · End to end — perceive → extract → analyse → challenge → decide
**Parts.** A (perceive) → C (extract under contract) → D (analyse with typed outcomes) → F (challenge) → E5 human gate, one K1 transcript, K2 on every step.
**Status.** A thought exercise only. It is not exercised in code.
**Risks.** Errors compound across steps. The transcript grows; each step needs a clear context boundary (see `framework/SUB-AGENT-FRAMEWORK.md`). No Month 1 component has run against a live model.

## 2. Rules for combining (from what the code does today)
1. **Hand off through K1.** One message shape: `turn, speaker, kind, content`.
2. **Branch only on typed strings.** Never on prose.
3. **Every step has a signal and a cap.** K2 does both.
4. **Gate before you run.** K3 lint is cheap; run it first.
5. **Route doubt to a person.** GUESS, PAUSE, closest fight, any booking.
6. **Keep the labels.** A combination of ILLUSTRATIVE parts is ILLUSTRATIVE.

## 3. Industry application map
*Sectors and use cases come from this repository's business case
(`business/BUSINESS-CASE.md`) and the Month 1 film scripts' sector beats.
"Value" is qualitative. No figure on this page is a result. For market context
use only the cited sources in the business case.*

| Sector | Use case | Combination | Value (qualitative) | Constraints |
|---|---|---|---|---|
| Insurance | Photo-based claims triage | CB-2 + CB-3 | Each damage claim points at its region; balanced cases go to a person | Calibration; claims-handling rules; a person decides payment |
| Healthcare administration | Referral preparation | CB-4 | A prepared pack, never auto-booked; every hand-off on record | Patient-data privacy law; clinical decisions stay with clinicians |
| Finance operations | Recurring spend and exception hunts | CB-1 | Findings trace to rows; errors are typed and kept | Copied exports only; isolated executor; not financial advice |
| Banking | Document extraction with explicit Do-Nots | CB-1 (contract gate) | Scope fixed before the run | Regulated-advice rules; audit retention |
| Legal and contract operations | Clause extraction and position review | C + CB-3 | Fixed-table output; the closest fight is read first | Not legal advice; counsel decides |
| Procurement | Challenge terms before signature | CB-3 | The strongest case against is filed before signing | Human sign-off |
| Public sector | Accessibility audits of public spaces | CB-2 | Each barrier report shows the spot in the photo | Public-record and privacy rules for images |
| Construction and facilities | Site inspection, punch lists | CB-2 | Occluded regions listed, not skipped | Safety calls stay with an inspector |
| Manufacturing | Visual inspection | CB-2 | Unsure calls stop for a person | Line-stop authority; calibration per line |
| Retail | Shelf and signage audits | CB-2 | Counts a person can recheck | Store photography consent |
| Contact centres | Multi-specialist case handling | CB-4 + K1 | Warm transfers with the full transcript | Recording consent; quality sampling |
| Telecom and utilities | SLA extraction, regulated operations | C + CB-1 | Output shapes downstream systems can read | Regulator reporting formats |
| Engineering and architecture boards | Decision records | CB-3 | The losing design's best argument is kept | The board still decides |
| Shared services / BPO | Any "show me" workflow | K1 everywhere | Replay from one file | Client data boundaries |

## 4. What would turn a row into evidence
The business case states the path: pattern fit, a measured pilot with human
checkers, contracts and controls, then a scale decision on measured numbers
(`business/BUSINESS-CASE.md`, "From demonstration to deployment"). Nothing on
this page skips that path.
