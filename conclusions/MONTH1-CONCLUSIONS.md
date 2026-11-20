▸ GAI OBSERVE LLC · POC LEARNING LAB
# Month 1 Conclusions — POCs 01–06

*Status: v1.0 for independent review, 2026-11-19. Branch `month1-conclusions-2026-11-19`.
Mode: every Month 1 POC is **INTERIM** (scripted demonstration, deterministic
stubs, synthetic data). Every figure on this page is **ILLUSTRATIVE**. None is
a field measurement. See the mode rule in `ROADMAP.md`.*

## How to read this page
- Each POC gets four blocks: the problem, the parts it used, the runs and
  evidence, and the conclusion.
- **Proved** here means: the mechanism works as written, in a scripted run,
  and the figures move when the data moves. It never means: this works in
  production, or this saves money.
- Every claim points at a file in this repository. If a file and this page
  disagree, the file wins.

## Re-verification on 2026-11-19 (base commit b2bfadf)
All checks were re-run on a clean checkout of `main` before this page was written.

| Check | Command | Result |
|---|---|---|
| POC tests (perturbation + CTO corrections), 10 files | `python notebooks/NN-*/tests/<file>.py` | 10 of 10 exit 0 |
| Notebook code matches `kit/` and `poc/` | `python tools/notebook_code_sync.py --check` | 6 notebooks, 50 definitions, no drift |
| Sync tool self-test | `python tools/test_notebook_code_sync.py` | ALL PASS |
| Notebook cells re-run, stdout compared | `python tools/run_notebook_cells.py` | 6 of 6 OK |
| Chaining exercises (new, this branch) | `python innovation-week/chains/check_chains.py` | 25 of 25 checks pass |

---

## POC 01 · An Agent That Sees — "The Confidence Map"
**Problem.** A seeing agent writes a caption. Nobody can tell which parts it saw
and which parts it guessed. (`sources/02-poc-brief.md`)

**Parts.**
- *Scene parser* (stub): emits one claim per region, with a confidence. Input: `data/claims.csv`.
- *Confidence flagger*: confidence below 0.60 = GUESS, else GROUNDED. The flag is derived at load, never stored (`poc/sees.py`, `FLAG_THRESHOLD`).
- *Human verifier*: a recorded `verified` column. In this demo it is typed in the data.
- *Survival summariser*: survived ÷ total.

**Runs and evidence.** `runs/run-01.json` (2026-10-25): 13 claims, 10 survived,
survival rate 0.769. The 3 GUESS claims (0.42, 0.35, 0.48) are the 3 that failed.
That separation holds **by construction** (`sources/04-run-evidence.md`).
Perturbation test: flip one outcome and the rate moves to 0.692.

**Conclusion.** Proved: a claim can carry its region and its confidence, the
flag line is fixed before the run, and the headline is computed from the check
table. Not proved: that any real vision model's confidences mean anything. The
CTO review (`reviews/cto/CTO-2026-10-26-POC-LAB-001.md`) holds POC 01 at
teaching-demo status until a real perception adapter, held-out labels,
calibration and an independent replay exist.

## POC 02 · Conversation Is a Coordination Primitive — "The Transcript Is the Database"
**Problem.** Agents that coordinate through hidden state cannot be audited.

**Parts.**
- *Analyst*: asks four fixed questions.
- *Executor*: answers from sandboxed analysis functions over a copied export (`total_by_category`, `monthly_count`, `find_unused`, `find_count_change`, `find_overlap`).
- *TranscriptStore* (`kit/transcript.py`): the only channel; saved as JSONL.
- *Findings pass*: three findings nobody asked for; closes with `EXPLORATION COMPLETE`.

**Runs and evidence.** `runs/run-01.txt` and `runs/transcript-01.jsonl`
(2026-10-25): 12 messages, 3 findings — gym-unused $78.00 across Feb–Mar;
coffee-subscription billed 3× in March vs 2×; a second streaming subscription
from March. Findings are computed from `data/transactions.csv`.

**Conclusion.** Proved: two roles can work with no shared memory, and the run
can be replayed from one file. Not proved: durability, ordering, idempotency or
tamper evidence. The CTO review ranks POC 02 second for investment, after those
gates land. Note: `EXPLORATION COMPLETE` is appended but not checked by
`kit/termination.py` in this POC.

## POC 03 · RODS — "Contracts Before Capabilities"
**Problem.** Agents are briefed in prose. Scope drifts, output shapes break
downstream, runs never end cleanly.

**Parts.**
- *RODS contract*: Role, Output, Do-Nots, Signal — four lines (`poc/rods_agent.py`).
- *Parser + linter* (`kit/rods.py`): rejects duplicate fields; flags `MISSING:<field>`, `WEAK_SIGNAL` (done / complete / finished), `VAGUE_OUTPUT` (no table, schema or JSON named).
- *Clause analyst* (stub): writes the party | duty | deadline table from `data/extraction.csv`.
- *Termination* (`kit/termination.py`): ends only on the exact signal `EXTRACTION COMPLETE`, or a cap of 10.

**Runs and evidence.** `runs/run-01.txt` (2026-10-25): good contract lint CLEAN;
bad contract 3 flags; 4 obligations extracted; `TERMINATION: SIGNAL`.

**Conclusion.** Proved: a contract can be checked by a machine before any run,
and a run can end on a typed signal, not a prose word. The linter and the
termination check execute for real; the extraction is scripted. The CTO review
ranks RODS first for investment: "the governance spine".

## POC 04 · The Analyst–Executor Loop — "The Error Is the Curriculum"
**Problem.** Analytics automation fails silently, or engineers debug code when
the question was wrong.

**Parts.**
- *Analyst* (scripted): five attempts, each a question plus code.
- *Executor*: runs the code with only `rows` and a small set of builtins; returns the result or the error text (`run_executor`). **Teaching-only. Not an isolation boundary.**
- *Outcome classifier*: ERROR (code wrong), EMPTY (question wrong), SUCCESS.
- *Termination*: `ANALYSIS COMPLETE` or a cap of 20. The finding is drawn only from attempts that actually ran.

**Runs and evidence.** `runs/run-01.txt`, `runs/attempts.csv` (2026-10-26):
5 attempts — 1 ERROR (`KeyError: 'amt'`), 1 EMPTY (`gym` matched no rows),
3 SUCCESS. Finding: gym-unused $78.00 (2 × $39.00). Perturbation test moves it to $98.00.

**Conclusion.** Proved: a typed outcome per attempt routes each failure to the
right repair, and a finding can be traced to rows. The attempts are scripted, so
the attempt pattern is ILLUSTRATIVE. A live model would produce the real data here.

## POC 05 · Three Ways to Run a Group Chat — "Choose Your Parliament"
**Problem.** Teams pick a routing shape by fashion, not by cost and control.

**Parts.**
- *Specialists*: Summariser, Matcher, Scheduler — functions over a shared `state` dict.
- *Routers*: round robin (fixed order, twice), selector (a chair picks the first missing piece), swarm (direct hand-offs plus a verification hand-back).
- *Cap*: 12 turns for selector and swarm.
- *Human gate*: the pack is always `booked: False`.

**Runs and evidence.** `runs/run-01.txt`, `runs/routing-comparison.csv`
(2026-10-26): round robin 6 turns / 6 calls; selector 3 turns + 4 routing calls
/ 7; swarm 4 turns + 3 hand-offs / 4. All three prepared the same pack
(orthopaedics, 2 slots, unbooked). These are **the mechanics of this script**, not costs.

**Conclusion.** Proved: the same agents and job produce different turn and call
profiles under different routing, and each shape leaves its own transcript.
Not proved: what any shape costs with live models. One caution found while
building the chaining exercises: a router stuck on the Matcher is capped, but
still emits a plausible field (`general`). Only the termination record shows it
went wrong (`innovation-week/chains/check_chains.py`, chain 4).

## POC 06 · The Debate Pattern — "Disagreement Is a Sensor"
**Problem.** A single polished opinion hides the close calls.

**Parts.**
- *Proponent* and *Opponent*: strongest case for and against, from `data/claims.csv`. Neither concedes.
- *Judge*: a rule fixed before the debate — margin = against − for; ≥ 4 REJECT, ≥ 0 PAUSE, else PROCEED.
- *Disagreement score*: smaller total ÷ larger total.
- *Termination*: `DEBATE COMPLETE` or a cap of 30.

**Runs and evidence.** `runs/run-01.txt`, `runs/verdicts.csv` (2026-10-26):
C1 REJECT (5 v 11), C2 PROCEED (8 v 5), C3 REJECT (2 v 14). Closest fight: C2 at 0.62.

**Conclusion.** Proved: verdicts can be machine-readable, and both sides'
strongest points can be kept on the record. The closest fight is a **prompt for
human review**. It locates no genuine uncertainty. Strengths are scripted. The
verdict informs counsel; it is not legal advice.

---

## What Month 1 established, across all six
1. **Typed outputs beat prose.** Flags (01), lint codes (03), outcomes (04), verdicts (06) and signals (03, 04, 06) are all strings a second program can check.
2. **The data file is the source.** Every figure is computed from a data file. Six perturbation tests (one per POC) prove it by moving the data and watching the figure move.
3. **Endings are designed.** A turn cap appears in 03, 04, 05 and 06. A typed signal, checked by `kit/termination.py`, appears in 03, 04 and 06. POC 02 appends its signal but does not check it; POC 05 relies on the cap and the chair's stop rule.
4. **A person stays in the loop at the decision point.** Verification (01), the lawyer's queue (03), booking (05) and counsel (06).
5. **Honest labels travel with the numbers.** INTERIM and ILLUSTRATIVE are on every figure.

## What Month 1 did not establish
- No live model ran in any POC. No figure is MEASURED.
- No POC has a FINAL-mode run. FINAL means: real model, recorded transcript, figures nobody typed, a reviewer can reproduce it (`ROADMAP.md`).
- No cost, latency or accuracy claim can be made from Month 1.
- The CTO verdict stands: **PASS WITH CONDITIONS** as a learning release; **HOLD** as evidence of deployable capability.

## Next pages
- Component catalogue and dependency map: `COMPONENT-CATALOGUE.md`
- Combinations and industry map: `COMBINATIONS-AND-INDUSTRY-MAP.md`
- Sub-agent framework introduction: `../framework/SUB-AGENT-FRAMEWORK.md`
- Innovation Week guidelines: `../innovation-week/README.md`
