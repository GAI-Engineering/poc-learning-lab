# Implementation — Conversation Is a Coordination Primitive (02)

Built: `poc/conversation.py` using `kit/transcript.py` (TranscriptStore).
Design: Analyst questions → Executor results → follow-up questions that only exist because of earlier results (exploratory path a pipeline cannot pre-write). Transcript saved to `runs/transcript-01.jsonl`.
Run: `python3 poc/conversation.py` → `runs/run-01.txt` + transcript.
