# 04 — The Analyst–Executor Loop


**MODE: INTERIM (stub)** — scripted demonstration; figures ILLUSTRATIVE, never quoted as findings. FINAL = a complete end-to-end run (real model, recorded transcript, figures nobody typed in).
**The idea to steal:** The Error Is the Curriculum

An analyst drafts code for each question; an executor runs it in a teaching-only in-process executor (restricted builtins - not an isolation boundary) and returns the real output — or the real error — as a message. **ILLUSTRATIVE — scripted demonstration:** the analyst's five attempts are scripted for the lesson (1 ERROR on an assumed column name, 1 EMPTY from a wrong category name, 3 SUCCESS), so the attempt pattern teaches the loop; it is not a measured result. The loop's finding (an unused $78.00 charge, Feb–Mar) is computed from the synthetic export rows by the corrected code.

- Runnable build: `poc/` — run receipt: `runs/run-01.txt` + `runs/transcript-01.jsonl` · Perturbation checks: `tests/test_perturbation.py` (edit the data, watch the finding move)
- Source pack: `sources/` (01-post · 02-poc-brief · 03-implementation · 04-run-evidence · 05-charts)
- Data: `data/` · Charts: `charts/` (PNG in this folder; the chart also renders inside the executed notebook below). All data synthetic; demonstration outputs labelled ILLUSTRATIVE.
- Study artifacts: a companion NotebookLM study notebook for this POC is in preparation — its link is recorded here when the notebook is verified, and the `study/` transfer follows the harvest.
- Status: released 2026-10-26 under the lab's release gate (REL-2, released with conditions) — live on the main branch.

**▸ GAI OBSERVE LLC · POC Learning Lab**

## Jupyter / Colab book

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GAI-Engineering/poc-learning-lab/blob/main/notebooks/04-analyst-executor-loop/04-analyst-executor-loop.ipynb)

Runnable Jupyter book for this POC: `04-analyst-executor-loop.ipynb` in this folder — self-contained, executed end-to-end locally with the recorded outputs in place (the Colab badge below is live — this book is published on the main branch). Pipeline: NotebookLM notebook (knowledge + study materials) -> decks/video -> this Colab book, enriched from the NotebookLM harvest in the next stage.
