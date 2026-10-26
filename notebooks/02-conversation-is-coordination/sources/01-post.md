AGENTS THAT SEE - AGENTS THAT TALK - Post 2 of 15 - Foundations

A pipeline is a recipe: step one, step two, step three, dinner. A conversation is a kitchen brigade: the sauce splits, someone tastes, the plan changes mid-service - and the meal that arrives is one nobody wrote down in advance. Neither is better. The craft is knowing which kitchen your task needs.

THE 30-SECOND VERSION
Pipelines run steps you already know. Conversations discover steps you don't. If the path is knowable before you start, pipeline it - cheap and predictable. If the path only reveals itself as the work unfolds, conversation earns its higher cost.

THE IDEA TO STEAL - THE TRANSCRIPT IS THE DATABASE
In a pipeline, the log is a record of the work. In a conversation, the transcript IS the work: every later step reads everything earlier agents said. So design the transcript like data - structured outputs, named signals, capped messages - because whatever mess enters the transcript compounds on every single turn.

WHEN CONVERSATION WINS
- Exploratory tasks - sub-tasks appear mid-flight
- Code execution - the output decides the next move
- Humans joining at unpredictable turns, in plain language
- Agents challenging and revising each other's reasoning

APPLIED POC - PERSONAL FINANCE
Idea: Explore a year of bank transactions and surface what matters.
Build: Two agents converse over a transaction export: one asks questions, one runs sandboxed analysis code and reports back.
Guardrail: Works on a copied export - never on live bank access.
The win: Three findings the owner did not know to ask for.

WHERE IT BREAKS
- Every turn re-reads the whole history - cost compounds
- Emergent paths are harder to test than fixed ones
- A conversation can wander; a pipeline cannot

TRY THIS WEEK
Pick one pipelined task that failed on an input nobody predicted. Re-run it as a two-agent conversation on the same data. Write down the first moment the conversation found something the pipeline structurally could not.

Community: name one task you pipelined that should have been a conversation - or the reverse.

The arc: Post 1 - An Agent That Sees. Next: Post 3 - RODS, the four lines every agent needs.