▸ GAI OBSERVE LLC · POC LEARNING LAB
# Innovation Week — Guidelines for Reusing the Month 1 Components

*DRAFT, 2026-11-19. These pages are guidance, not new POCs. They set no dates
and announce nothing; the Lab's schedule decides when and how they are used.
Everything here builds on POCs 01–06, which are scripted demonstrations over
synthetic data (mode INTERIM, figures ILLUSTRATIVE).*

## What is in this folder
| File | Use it for |
|---|---|
| `README.md` (this page) | The guidelines: how to pick, combine and check components |
| `FOOD-FOR-THOUGHT.md` | Prompts to think with, alone or in a group |
| `CHAINING-EXERCISES.md` | Five exercises: component A → B → C, with expected outputs and checks |
| `chains/check_chains.py` | Runs every exercise's checks. `python innovation-week/chains/check_chains.py` |
| `STORIES-DRAFT-FOR-SAM2.md` | Story drafts, awaiting voice and tone |

Background reading: `conclusions/` (what Month 1 showed) and
`framework/SUB-AGENT-FRAMEWORK.md` (the pattern behind it).

## The guidelines

### G1 · Start from a problem you own
Name one decision in your organisation that rests on a claim nobody can trace,
a hand-off nobody recorded, or an agent nobody contracted. That is your starting
point. Pick the Month 1 pattern that answers it (see the industry map in
`conclusions/COMBINATIONS-AND-INDUSTRY-MAP.md`).

### G2 · Reuse before you build
Every Month 1 component runs on the Python standard library. Import it; do not
copy and change it. The kit (`kit/`) is the spine: transcript, termination, RODS.
If you change a component, write down why.

### G3 · Contract first
Write a RODS contract for every agent you add. Run the linter. Nothing runs on a
contract with flags.

### G4 · One record
Every agent writes to one transcript, in the shape `turn, speaker, kind, content`.
If a hand-off is not in the transcript, it did not happen.

### G5 · Typed hand-offs only
Branch only on typed strings: GROUNDED / GUESS, ERROR / EMPTY / SUCCESS,
PROCEED / PAUSE / REJECT. Never branch on prose.

### G6 · A signal and a cap on every step
Use `kit/termination.py`. A run that hits the cap records it.

### G7 · Put a person at the decision
Name the point where a person decides. Route doubt there: guesses, pauses,
the closest fight, any booking or signature.

### G8 · Prove the figure moves
For every figure you show, write one perturbation test. Change the input; the
figure must change. Add one negative control: a change that must block or
fail the run.

### G9 · Keep the labels
Synthetic data and scripted agents give ILLUSTRATIVE figures. A combination of
ILLUSTRATIVE parts is ILLUSTRATIVE. Only a real, recorded, reproducible run is
MEASURED.

### G10 · Never use real people's data
Use synthetic data, or a copied and anonymised export you are allowed to use.
No live systems, no credentials, no customer records.

## Reuse, re-apply, innovate — three levels
| Level | What you do | Example |
|---|---|---|
| **Reuse** | Run a Month 1 component on your own synthetic data | Point POC 04's loop at your own export shape |
| **Re-apply** | Move a pattern to a new sector | POC 06's debate for a vendor review instead of a contract |
| **Innovate** | Combine components into a flow Month 1 did not build | CB-1: RODS gate → loop → findings, one transcript |

## Done looks like
- A one-page problem statement (G1).
- RODS contracts, lint CLEAN (G3).
- A transcript file from one run (G4).
- One perturbation test and one negative control, both passing (G8).
- Every figure labelled (G9).
- A note on where a person decides (G7), and what would make it MEASURED.
