# Infographics — provenance (read before reusing)
▸ GAI OBSERVE LLC · POC LEARNING LAB

- The **SVG files are the figures of record**: every number on these
  cards is drawn from `business/KEY-DATA-POINTS.md` (which traces to
  the notebooks' run data). All figures are from scripted
  demonstrations over synthetic data — each card is labelled
  SCRIPTED DEMONSTRATION (ILLUSTRATIVE), and that label is part of
  the card.
- The **PNG files beside them are rendered from these SVGs**
  (LibreOffice render, 2026-10-26, review SE-18) — never from an
  image-generation model. Lesson L-11: text rendered by an image
  model is unreliable; the earlier NotebookLM PNG renders were
  withdrawn under review E-8 because their text misstated these
  figures.
- If a figure changes, change KEY-DATA-POINTS, then the SVG, then
  re-render the PNG — and read the new render at full size against
  KEY-DATA-POINTS before it is used anywhere.
