# Releases

Release record for this repository. A batch is released only on the evaluator of record's signed verdict; conditions are recorded with the release and stay attached to it until closed. Everything in this lab is a scripted demonstration on synthetic data — results are ILLUSTRATIVE, never measured, until a mode promotion says otherwise (see the mode rule in the README).

## REL-1 — Day 1 (POCs 01–03) — 2026-10-26

**RELEASED WITH CONDITIONS** by the evaluator of record, 2026-10-26.

Conditions: (a) `.gitattributes` line-ending pin — closed in commit 90935685; (b) the announcement post's results wording — a correction was recorded as posted as an author comment under the post on 2026-10-26 (the platform allows no edit or pin); the item is not closed: it remains open pending the owner's approval (see REL-2, condition 4); (c) the two LinkedIn seeding posts to be read live and any results wording corrected — open at the time of this record.

## REL-2 — Day 2 (POCs 04–06) — 2026-10-26

**RELEASED WITH CONDITIONS** by the evaluator of record, 2026-10-26, on the re-verified review-branch head 280c8f6 (remediation snapshot d6e275b; re-test 13/13). Merged to main the same evening by the lab maintainer (PR #1, merge commit a603abf1bc3748afdec14952b132c0b3441aa7c0).

Conditions: (1) status and badge lines reworded to read true at the merge — done in the merge (branch tip d606ac9) and verified by the evaluator of record on 2026-10-26: the merged tree is byte-identical to the branch tip, and the Day 2 notebooks may be quoted; (2) D2-G — the POC 06 win condition rewording lands on main by Wed Oct 28, 12:00 ET; (3) INTERIM and illustrative wording throughout — never "measured"; (4) REL-1's Olympus correction still needs the owner's approval.

*This log was first committed to the tree on 2026-10-26, after the REL-2 merge; both entries record verdicts signed earlier that day. Wording corrected the same evening on the evaluator's review (RL-1..RL-4).*

## Maintenance sync — 2026-10-26 (night)

Published on the founder's direction; the evaluator of record's checks on this material proceed against this tree.

- **CTO correction batch** (commit 6ac46231): four edge-case defects found by independent CTO probes, each reproduced failing-first and fixed with a regression test — POC 04's finding is now derived only from attempts that actually ran; POC 05 no longer labels a completed run INCOMPLETE; POC 06's disagreement ratio no longer divides by zero; the shared kit's termination check requires the exact typed signal and the RODS parser rejects a duplicate field instead of overwriting it. Standard outputs are unchanged (all six notebooks re-executed after the fixes: text outputs identical to the released versions). The POC 06 brief in this commit carries the D2-G win-condition rewording — **REL-2 condition (2) is satisfied by this commit**, recorded here for the evaluator's verification.
- **Executive layer completed for Day 2** (commit 4df7b2f3, plus the binary sync in commits 5d58705 through 00b5709 (14 commits; head 00b5709)): every notebook 01–06 opens with the market-data lead; the business case covers Patterns 4–6; key-data rows added for POCs 04–06; each notebook's own technical flow is embedded in its §2; the Day 2 SVG infographics are the figures of record, with PNGs rendered from them; chart style unified across all six notebooks and the charts re-rendered from the notebooks' own code; the business deck rebuilt across all six POCs with the infographics embedded (PPTX + PDF).
