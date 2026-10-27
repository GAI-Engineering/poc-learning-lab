# 06 — The Debate Pattern


**MODE: INTERIM (stub)** — scripted demonstration; figures ILLUSTRATIVE, never quoted as findings. FINAL = a complete end-to-end run (real model, recorded transcript, figures nobody typed in).
**The idea to steal:** Disagreement Is a Sensor

Two advocates who never concede argue three synthetic contract positions; a judge applies a rule fixed before the debate and rules in a machine-readable format. **ILLUSTRATIVE — scripted demonstration:** argument strengths are scripted for the worked example, so the verdicts (C1 REJECT, C2 PROCEED, C3 REJECT) illustrate the pattern — the closest fight, C2 at disagreement 0.62, is the lesson: the most balanced scripted argument is where a human reviewer should look first — a prompt for review, not a located uncertainty.

- Runnable build: `poc/` — run receipt: `runs/run-01.txt` + `runs/debate-01.jsonl` · Perturbation checks: `tests/test_perturbation.py` (change a strength, watch a verdict flip)
- Source pack: `sources/` (01-post · 02-poc-brief · 03-implementation · 04-run-evidence · 05-charts)
- Data: `data/` · Charts: `charts/` (PNG in this folder; the chart also renders inside the executed notebook below). All data synthetic; demonstration outputs labelled ILLUSTRATIVE.
- Study artifacts: a companion NotebookLM study notebook for this POC is in preparation — its link is recorded here when the notebook is verified, and the `study/` transfer follows the harvest.
- Status: released 2026-10-26 under the lab's release gate, with conditions — live on the main branch. Release record: RELEASES.md at the repo root.

**▸ GAI OBSERVE LLC · POC Learning Lab**

## Jupyter / Colab book

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GAI-Engineering/poc-learning-lab/blob/main/notebooks/06-debate-pattern/06-debate-pattern.ipynb)

Runnable Jupyter book for this POC: `06-debate-pattern.ipynb` in this folder — self-contained, executed end-to-end locally with the recorded outputs in place (its Colab badge is live — this book is published on the main branch). Pipeline: NotebookLM notebook (knowledge + study materials) -> decks/video -> this Colab book, enriched from the NotebookLM harvest in the next stage.
