▸ GAI OBSERVE LLC · POC LEARNING LAB
# Month 1 Lessons — Curriculum (the fourth week)

*v1.0 for independent review, 2026-11-19. One week of lessons drawn from
POCs 01–06: what they showed, how their parts fit together, and where they
apply. Not new POCs. No dates or live events are set here; the Lab's schedule
does that. Mode INTERIM; every figure ILLUSTRATIVE.*

## Who it is for
| Track | For | Pace |
|---|---|---|
| **CTO** | Technology leaders who approve, fund or review agent work | About 4 hours across the week |
| **Beginners** | Learners meeting agents for the first time; no programming needed for modules 1, 2, 4 and 5 | About 4 hours across the week |

## What you will be able to do by the end
1. State what each of POCs 01–06 proved, and what it did not prove.
2. Name the parts of a sub-agent system: orchestrator, sub-agents, record, signal, cap, human gate.
3. Read a dependency map and say which Month 1 components can feed which.
4. Run a chain of three components and check its output, including a negative control.
5. Match a Month 1 pattern to a problem in your own sector, with its preconditions and risks.
6. Write a one-page plan to reuse a component, with a contract, a perturbation test and honest labels.

## The five modules
Each module lists its materials, what to do, and how you know you are done.
Films and the walkthrough deck are listed by name; use them once the Lab releases them.

### Module 1 · What Month 1 showed (about 45 min)
- **Read:** `conclusions/MONTH1-CONCLUSIONS.md`.
- **Watch:** Month 1 Lessons Film A — "Six Bricks, One Spine" (CTO track) or "Six Bricks, One Box" (Beginners track).
- **Do:** for each POC, write one line: proved / not proved.
- **Done when:** your six lines match the conclusions page, and you can say why no Month 1 figure is MEASURED.

### Module 2 · The sub-agent pattern (about 45 min)
- **Read:** `framework/SUB-AGENT-FRAMEWORK.md`, sections 1–5.
- **Do:** pick one POC. Name its orchestrator, its sub-agents, its record and its ending.
- **CTO extra:** sections 6–7. For one failure mode, name the control and the file that holds it.
- **Done when:** you can draw the framework diagram from memory, with the six parts in place.

### Module 3 · Stitching the parts (about 60 min)
- **Read:** `conclusions/COMPONENT-CATALOGUE.md` (catalogue and dependency map).
- **Walk through:** the Month 1 lessons deck "Six Builds, One Spine", the walkthrough slides (chain 1 step by step, the five chains, and "break it on purpose").
- **Run:** `python innovation-week/chains/check_chains.py`. Expect `checks=25 passed=25 failed=0`.
- **Do:** Exercises 1 and 3 in `CHAINING-EXERCISES.md`, including both negative controls.
- **Beginners:** follow the deck's walkthrough slides, which show what you should see at each step. Running the check yourself needs Python 3 and a copy of this repository; no code changes are needed.
- **Done when:** you can explain why the bad contract produces 2 messages and no finding.

### Module 4 · Where it applies (about 45 min)
- **Read:** `conclusions/COMBINATIONS-AND-INDUSTRY-MAP.md`.
- **Watch:** Month 1 Lessons Film B — "Build It in Your Industry" (CTO track) or "Where the Bricks Fit at Work" (Beginners track).
- **Read:** two stories from `STORIES-DRAFT-FOR-SAM2.md` (once released in final voice).
- **Do:** choose one sector row. Write its preconditions and its biggest risk in your own words.
- **Done when:** your row names a person at the decision point.

### Module 5 · Plan your own reuse (about 45 min)
- **Read:** `innovation-week/README.md` (guidelines G1–G10) and `FOOD-FOR-THOUGHT.md`.
- **Do:** write a one-page plan: the problem (G1), the components you reuse (G2), the RODS contracts (G3), where a person decides (G7), one perturbation test and one negative control (G8), and your labels (G9).
- **CTO extra:** say what a measured pilot would need: checkers, a baseline, a recorded run.
- **Done when:** your plan passes the "Done looks like" list in `innovation-week/README.md`.

## Map of materials
| Module | Repo pages | Film | Walkthrough | Check |
|---|---|---|---|---|
| 1 | conclusions/MONTH1-CONCLUSIONS.md | Film A | Lessons deck, conclusions slides | Six proved / not-proved lines |
| 2 | framework/SUB-AGENT-FRAMEWORK.md | Film A (beats 4–7) | Lessons deck, box-of-bricks slides | Diagram from memory |
| 3 | conclusions/COMPONENT-CATALOGUE.md, CHAINING-EXERCISES.md | — | Lessons deck, walkthrough slides | 25 of 25; two negative controls |
| 4 | conclusions/COMBINATIONS-AND-INDUSTRY-MAP.md, stories | Film B | Lessons deck, flows and value slides | One sector row, with a person at the decision |
| 5 | innovation-week/README.md, FOOD-FOR-THOUGHT.md | Film B (close) | — | One-page plan |

## Assessment, in plain terms
There is no test to pass and nothing to buy. The checks above are for you. If
you share your plan with the Lab community, keep the labels on: a plan built on
ILLUSTRATIVE figures is ILLUSTRATIVE.
