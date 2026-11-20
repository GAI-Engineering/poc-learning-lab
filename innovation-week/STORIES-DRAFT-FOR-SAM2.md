▸ GAI OBSERVE LLC · POC LEARNING LAB
# Stories — DRAFT-FOR-SAM-2

*Status: DRAFT-FOR-SAM-2, 2026-11-19. Facts drafted by Sam 5; voice and tone
to be rewritten by Sam 2; facts re-checked by Sam 5 after the rewrite.
Every story is fictional. People and organisations are invented. No story
reports a real result. Where a story cites a Month 1 run, the figure is
ILLUSTRATIVE (scripted demonstration, synthetic data, mode INTERIM).*

---

## S1 · POC 01 · "The photo nobody zoomed into"
Priya runs inspections for a small housing association. Every month a contractor
sends forty photos and one line: "All entrances accessible." One winter a tenant
using a wheelchair cannot get in. The photo shows a ramp. It also shows, in the
corner, a step nobody mentioned. Priya now asks for a confidence map: each claim
pinned to a region, each with a score, anything under the line marked as a guess.
In the Lab's scripted run, 3 of 13 claims were guesses and all 3 failed the
check — by construction, so the lesson is the habit, not the rate.
**Thread to pull:** a caption hides doubt; a map shows it.

## S2 · POC 02 · "Who said what, and when?"
Two weeks after a refund went out twice, Tom's team tries to rebuild what
happened. Three tools, two inboxes, one chat. Nobody can say who decided. Tom
makes one rule for the next pilot: the agents talk only in one transcript, and
the transcript is saved. The first replay takes ten minutes instead of two
days. *(The ten minutes is part of the story, not a measurement.)*
**Thread to pull:** if it is not in the transcript, it did not happen.

## S3 · POC 03 · "Four lines on a sticky note"
Amara inherits an agent that "helps with contracts". Its brief is two pages of
prose. It once drafted advice to a client. She rewrites the brief as four lines:
Role, Output, Do-Nots, Signal. The linter flags her first try: her signal was
"done". She changes it to `EXTRACTION COMPLETE`. Now the Do-Not is written
down, the linter checks it is there, and the output is a table a reviewer can
scan in a minute. The contract does not enforce itself; the review queue still does.
**Thread to pull:** a promise you can check beats a brief you have to trust.

## S4 · POC 04 · "The empty answer"
Luis asks an analyst agent how much the team spends on the gym. Answer: nothing.
He nearly closes the ticket. Then he sees the outcome says EMPTY, not SUCCESS.
The question was wrong: the category is called `gym-unused`. Asked again, the
agent finds a charge nobody uses, traced to two rows. In the Lab's scripted run
that leak was $78.00 (ILLUSTRATIVE).
**Thread to pull:** an empty answer is a different kind of wrong.

## S5 · POC 05 · "Three ways to run the morning huddle"
A clinic's admin team trials three ways to prepare referrals. In the first, everyone
speaks in turn, twice. In the second, a coordinator picks who speaks next. In the
third, each person hands to the next and the last hands back for a check. All
three produce the same pack. Nobody books anything until a person confirms. The
team argues less about the agents and more about who chairs.
**Thread to pull:** choosing who speaks next is a governance choice.

## S6 · POC 06 · "The argument we filed"
A procurement lead, Ines, gets a one-page recommendation: accept all three terms.
She asks for a debate instead: one advocate for, one against, a judge with a rule
written first. Two terms are rejected. The third proceeds, but it was the closest
fight, so she reads it first. The strongest losing point — define "discovery" —
goes into the file. Not legal advice; counsel still decides.
**Thread to pull:** the closest fight is where a person looks first.

---

## X1 · Cross-POC (03 + 04 + 02) · "The gate before the loop"
A finance team wants an analyst agent on its expense exports. The engineer says:
first, the contract. The linter blocks the first draft — no Do-Nots. The second
passes. The loop runs, errors and all, into one transcript. Two separate finders
report the same unused charge. The audit later reads one file.
**Thread to pull:** contract, loop, record — in that order.

## X2 · Cross-POC (01 + 05 + 06) · "Doubt goes to a person"
An insurer's triage pilot sends confident photo claims straight to the file and
guesses to an adjuster. Disputed claims go to a debate; the closest fight goes to
a senior adjuster. Nobody pays out on an agent's word.
**Thread to pull:** every pattern in Month 1 ends with a person at the decision.

## X3 · Cross-POC (all six) · "The field that looked fine"
A team chains five agents. One day the router gets stuck. The run is capped, but
the output still has every field filled — one of them quietly wrong. The only
clue is a line in the transcript: cap reached. The team adds one rule: read the
termination record before the output.
**Thread to pull:** a full form is not a finished job. (Shown in chaining exercise 4.)
