▸ GAI OBSERVE LLC · POC LEARNING LAB
# Chaining Exercises — Component A → B → C

*DRAFT, 2026-11-19. Five exercises that join Month 1 components without
changing them. Every expected output below is checked by
`chains/check_chains.py` (25 checks, last run 2026-11-19: 25 passed). All data
is synthetic; all figures are ILLUSTRATIVE.*

Run all checks from the repository root:

```bash
python innovation-week/chains/check_chains.py
```

Expected last line: `checks=25 passed=25 failed=0`.

Each exercise has: the chain, what to build, the expected output, the checks,
and a **negative control** — a change that must move or block the result.

---

## Exercise 1 · The governed analyst
**Chain.** RODS lint (POC 03) → Analyst–Executor loop (POC 04) → unasked-for findings (POC 02), one transcript.

**Build.** A gate: lint the POC 03 contract; run only if CLEAN. Then run the POC 04
loop and the POC 02 findings pass over the same export. Copy every message into
one `TranscriptStore`.

**Expected output.**
- Gate: `OPEN`.
- Loop finding names `$78.00` (gym-unused, 2026-02 and 2026-03).
- POC 02 returns 3 findings; the first also names `$78.00`.
- Shared transcript: 16 messages, 1 of kind `error` (kept, not hidden).

**Checks.** Two components, written separately, agree on the same leak.

**Negative controls.**
- Use POC 03's `BAD_CONTRACT`. Gate: `BLOCKED`. No finding. Transcript: 2 messages.
- Change `gym-unused,39.0` to `49.0` in a copy of the export. Both findings move to `$98.00`.

**Discuss.** Why must the gate run before the loop, not after?

## Exercise 2 · Seen, then checked
**Chain.** Confidence map (POC 01) → a routing rule → a person.

**Build.** Load POC 01's claims. Send claims at or above the threshold to the report; send the rest to a human queue.

**Expected output.**
- 13 claims, 10 survived, survival rate 0.769.
- At 0.60: 10 to the report, 3 to a person.
- Every claim in the human queue failed the (scripted) check.

**Negative control.** Raise the threshold to 0.80. The human queue grows to 5.

**Discuss.** In this demo the guesses fail by construction. What would you need before trusting the threshold with a real model?

## Exercise 3 · The argued decision record
**Chain.** Debate (POC 06) → machine-readable verdicts → human gate (POC 05's rule).

**Build.** Run the debate. Route PAUSE verdicts and the closest fight to a person. Record the rest.

**Expected output.**
- Verdicts: C1 `REJECT`, C2 `PROCEED`, C3 `REJECT`. All parseable.
- Routing: C1 auto-record, **C2 to a person** (closest fight, 0.62), C3 auto-record.
- Termination: `SIGNAL`.

**Negative control.** Add a pro argument of strength 6 to C1, making it 11 v 11. The fixed rule gives `PAUSE`, and C1 goes to a person.

**Discuss.** C2 was PROCEED, yet it goes to a person. Why is that the right call?

## Exercise 4 · Audit the parliament
**Chain.** Three routing shapes (POC 05) → saved transcripts → an audit that reads only the files (POC 02's rule).

**Build.** Run all three shapes on the letter. Save each transcript as JSONL. Re-count agent turns from the files alone.

**Expected output.**
- Total calls: round robin 6, selector 7, swarm 4.
- Nothing booked in any shape.
- Audit re-count of agent turns: round robin 6, selector 3, swarm 4 — the same as the run's own table.

**Negative control.** Give the selector a chooser that always returns `Matcher`, with a cap of 5. The run is capped. It still fills `specialty` with `general` (not `orthopaedics`), because the summary was never written. Only the termination record shows the run went wrong.

**Discuss.** What should a downstream step check before it trusts a field?

## Exercise 5 · One signal ends each step
**Chain.** `kit/termination.py` as the contract between any two steps.

**Expected output.**
- `check("STEP COMPLETE")` → `SIGNAL`.

**Negative controls.**
- `check("done")` → `None`. A prose word is not a signal.
- A cap of 2 with no signal → `CAP_TURNS` on the second check.

**Discuss.** Which step in your own process ends on a word someone might say by accident?

---

## Open extensions (no expected output — design your own checks)
1. Add `kit/session_log.py` to Exercise 4 and write one row per shape.
2. Give each POC 05 specialist a RODS contract and lint all three before the run.
3. Feed POC 01's GUESS claims into POC 06 as positions to debate. What strengths would you need, and who sets them?
4. Close gap G1 in a copy of POC 02: check `EXPLORATION COMPLETE` with `kit/termination.py`.
5. Sketch combination CB-5 (perceive → extract → analyse → challenge → decide). Where does each context boundary sit?

For each extension: one perturbation test, one negative control, labels kept.
