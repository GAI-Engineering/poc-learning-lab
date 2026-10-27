# POC Brief — Three Ways to Run a Group Chat (05)

**Idea:** Turn a referral letter into a booked, prepared appointment — and show that the routing shape, not the agents, decides how the team behaves.
**Build steps:** (1) Three stub specialists (Summariser, Matcher, Scheduler) with crisp one-line descriptions. (2) Run the same referral task under round robin (fixed sequence), selector (a chair picks the next speaker from state) and swarm (direct handoffs, with a verification hand-back). (3) Record turns, selector calls, handoffs and total calls per mode in one comparison table. (4) Same prepared pack from all three modes — the difference is governance, not output.
**Guardrail:** Agents prepare and propose. Booking happens only on human confirmation — every run ends with the pack unbooked.
**Win condition:** One prepared pack from one letter, facts intact — and the builder can name which parliament they chose and what its mechanics spent in turns and calls (scripted counts from this demo, not prices).
Data: synthetic only. Model: deterministic stub, no live model.
