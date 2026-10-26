# 01 — An Agent That Sees

**The idea to steal:** The Confidence Map

A layered scene parser over three synthetic scenes emits 13 region-grounded claims with confidences. **ILLUSTRATIVE — scripted demonstration:** the confidences and the human-verification outcomes are fixed in the script (poc/sees.py), so the 3 claims it flagged as guesses are the 3 that fail the check BY CONSTRUCTION — the pattern is what is taught here, not a measured result. Script survival: 10/13 (0.769).

- Runnable build: `poc/` — run receipt: `runs/run-01.json`
- Source pack: `sources/` (01-post · 02-poc-brief · 03-implementation · 04-run-evidence)
- Data: `data/` · Charts: the chart PNGs (`charts/`) are added by a separate binary push and are not in the repo yet — the charts render inside the executed notebook above. All data synthetic; demonstration outputs labelled ILLUSTRATIVE.
- Study artifacts: Briefing Doc, Study Guide and FAQ were generated in NotebookLM Studio 2026-10-25 over GAI Observe's own materials and live in that notebook's Studio (viewing requires a Google sign-in — NotebookLM redirects anonymous visitors); no `study/` folder exists in this repo yet — transfer is the Day 2 run's first act.
- NotebookLM notebook: https://notebook.google.com/notebook/06429ab0-f2ae-478a-95a2-f2ee08ea2660
- NotebookLM link: https://notebook.google.com/notebook/06429ab0-f2ae-478a-95a2-f2ee08ea2660 (sharing set to 'Anyone with a link', view-only — NOTE: NotebookLM still requires a Google sign-in to open it; anonymous visitors are redirected to sign-in, so treat this link as sign-in-gated)

**▸ GAI OBSERVE LLC · POC Learning Lab**

## Jupyter / Colab book

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GAI-Engineering/poc-learning-lab/blob/main/notebooks/01-agent-that-sees/01-agent-that-sees.ipynb)

Runnable Jupyter book for this POC: `01-agent-that-sees.ipynb` in this folder — self-contained, executed end-to-end with the recorded outputs in place (badge activates when the public repo is pushed). Pipeline: NotebookLM notebook (knowledge + study materials) -> decks/video -> this Colab book, enriched from the NotebookLM harvest in the next stage.
