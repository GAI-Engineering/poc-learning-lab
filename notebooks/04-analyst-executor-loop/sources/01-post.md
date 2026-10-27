AGENTS THAT SEE - AGENTS THAT TALK - Post 4 of 15 - Patterns

Here is the most productive relationship in applied AI: one agent that thinks in questions and writes code, and one that runs the code in a small in-process executor and reports back exactly what happened - including, especially, the errors. Most teams treat the error message as a failure. In this loop, the error message is the teacher.

THE 30-SECOND VERSION
The analyst drafts code for the question. The executor runs it in-process. Real output - or a real error - comes back, and the analyst adapts. There is no retry logic and no error table: the conversation itself is the control flow. That is why the loop discovers answers a fixed pipeline cannot reach.

THE IDEA TO STEAL - THE ERROR IS THE CURRICULUM
Every error the loop survives makes the next attempt smarter, because the analyst reads the failure and revises. Your job as the builder is not to make errors rare - it is to make errors legible: the real exception type and message, verbatim, and printed schemas. A loop fed vague errors learns nothing and bills you for the lesson anyway.

HABITS THAT MAKE IT WORK
- Print the schema first - never assume column names
- Cap every output; giant results drown the context
- Terminate on the Signal OR a message budget - always both
- A restricted builtin list is not a security boundary. Production means isolated execution - its own process or container. The in-process executor in the POC is for learning only

APPLIED POC - PERSONAL FINANCE
Idea: Find the leaks in a household budget from a transaction export.
Build: An analyst-executor pair categorises spending, charts the top leaks, and proposes three specific cuts - iterating on the synthetic numbers.
Guardrail: Education, not financial advice. Synthetic data only - real personal data belongs only in an isolated production runner, never in a teaching executor.
The win: Findings trace to actual rows, not generic money tips.

WHERE IT BREAKS
- In-process execution of untrusted code is a security incident waiting - restricted builtins are not isolation
- If the executor hangs, an uncapped loop retries forever - the budget is the guardrail
- Assumed schemas break silently on real-world files

TRY THIS WEEK
Hand the loop a synthetic dataset shaped like yours - invented rows, same columns. Before the first question, make it print the schema and row count. Watch how many wrong assumptions die in that single step.

Community: what is the first dataset you would hand a loop like this?

The arc: Post 3 - RODS. Next: Post 5 - Three Ways to Run a Group Chat.