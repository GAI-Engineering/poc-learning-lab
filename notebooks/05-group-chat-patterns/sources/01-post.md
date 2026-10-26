AGENTS THAT SEE - AGENTS THAT TALK - Post 5 of 15 - Patterns

Put five specialists in a room and the meeting still fails or succeeds on one unglamorous question: who speaks next, and who decides? Agent teams are identical. The agents get the attention; the routing does the governing.

THE 30-SECOND VERSION
Three routing shapes run every group chat. Round robin: a fixed sequence - cheap, predictable, debuggable. Selector: a model picks the next speaker from context - flexible, at the price of an extra model call per turn. Swarm: agents hand off to each other directly - powerful, and the hardest to trace. Same agents, three different systems. Routing is the difference.

THE IDEA TO STEAL - CHOOSE YOUR PARLIAMENT
Round robin is a queue with manners. A selector is a chair who recognises speakers. A swarm is a corridor where work passes hand to hand. Each is a theory of governance, and the behaviour you get is the governance you chose - drift, bottlenecks and all. When a team misbehaves, do not retrain the members. Change the parliament.

CHOOSING THE SHAPE
- Known sequence? Round robin - the assembly line
- Expertise needed at unpredictable points? Selector
- Work that splinters into specialities? Swarm handoffs
- The selector is itself a model call - budget for it

APPLIED POC - HEALTHCARE
Idea: Turn a referral letter into a booked, prepared appointment.
Build: A selector panel: a summariser reads the letter, a matcher picks the specialty, a scheduler proposes slots; the patient confirms.
Guardrail: Agents prepare and propose. Booking happens only on human confirmation.
The win: One conversation replaces four phone calls - with the letter's facts intact.

WHERE IT BREAKS
- A wrong routing choice compounds downstream
- Selector quality depends on crisp agent descriptions
- More agents means more context every single turn

TRY THIS WEEK
Draw the routing shape of one workflow you run - honestly, as it is today, not as designed. Name it: queue, chair, or corridor. Most "agent problems" rename themselves at this step.

Community: which of your workflows has a knowable order, and which genuinely needs a selector?

The arc: Post 4 - The Analyst-Executor Loop. Next: Post 6 - The Debate Pattern.