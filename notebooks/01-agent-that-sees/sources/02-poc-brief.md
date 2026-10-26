# POC Brief — An Agent That Sees (01)

**Idea:** Audit public spaces for accessibility barriers from photos, with every finding pinned to a region.
**Build steps:** (1) Define synthetic scenes as regions with ground-truth objects. (2) Stub parser emits region-grounded claims + confidence per region. (3) Flag claims under 0.60 as GUESS. (4) Human verification recorded against ground truth; survival rate computed.
**Guardrail:** Findings are drafts until a human confirms them on the image.
**Win condition:** Every reported barrier points at the region that proves it; survival rate is measured, not asserted.
Data: synthetic only. Model: deterministic stub, no live model.
