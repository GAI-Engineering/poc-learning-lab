# 02 — Conversation Is a Coordination Primitive

**The idea to steal:** The Transcript Is the Database

Two agents coordinate through a transcript only over a synthetic transaction export: 12 messages, 3 findings the owner did not know to ask for (ILLUSTRATIVE — scripted demonstration over synthetic data). The transcript is persisted as the state store (`runs/transcript-01.jsonl`).

- Runnable build: `poc/` — run receipt: `runs/run-01.txt`
- Source pack: `sources/` (01-post · 02-poc-brief · 03-implementation · 04-run-evidence)
- Data: `data/` · Charts: the chart PNGs (`charts/`) are added by a separate binary push and are not in the repo yet — the charts render inside the executed notebook above. All data synthetic; demonstration outputs labelled ILLUSTRATIVE.
- Study artifacts: Briefing Doc, Study Guide and FAQ were generated in NotebookLM Studio 2026-10-25 over GAI Observe's own materials and live in that notebook's Studio (viewing requires a Google sign-in — NotebookLM redirects anonymous visitors); no `study/` folder exists in this repo yet — transfer is the Day 2 run's first act.
- NotebookLM notebook: https://notebook.google.com/notebook/4d372cee-af23-424f-a229-5be90c58c9e0
- NotebookLM link: https://notebook.google.com/notebook/4d372cee-af23-424f-a229-5be90c58c9e0 (sharing set to 'Anyone with a link', view-only — NOTE: NotebookLM still requires a Google sign-in to open it; anonymous visitors are redirected to sign-in, so treat this link as sign-in-gated)

**▸ GAI OBSERVE LLC · POC Learning Lab**

## Jupyter / Colab book

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GAI-Engineering/poc-learning-lab/blob/main/notebooks/02-conversation-is-coordination/02-conversation-is-coordination.ipynb)

Runnable Jupyter book for this POC: `02-conversation-is-coordination.ipynb` in this folder — self-contained, executed end-to-end with the recorded outputs in place (badge activates when the public repo is pushed). Pipeline: NotebookLM notebook (knowledge + study materials) -> decks/video -> this Colab book, enriched from the NotebookLM harvest in the next stage.
