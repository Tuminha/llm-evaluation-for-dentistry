# arXiv Submission Notes

This directory contains the arXiv-oriented manuscript source.

## Files

- `main.tex` — LaTeX source with inline bibliography.
- `main.pdf` — locally compiled preview using Tectonic.
- `figures/accuracy_by_model_arxiv.pdf` — paper-safe model accuracy figure without third-party logos.
- `figures/accuracy_by_domain_arxiv.pdf` — paper-safe domain heatmap.
- `arxiv_upload.zip` — minimal source package for arXiv test upload.

## Suggested arXiv Metadata

- Group: `cs`
- Primary category: `cs.CL`
- Secondary category: `cs.AI`
- Optional secondary category: `cs.CY` only if the final framing emphasizes clinical deployment risk.
- Comments: `9 pages, 2 figures; benchmark report`

## Before Submission

1. Confirm final author affiliation, funding, competing-interest wording, acknowledgments, and author contributions.
2. Confirm the repository commit hash in `main.tex` still points to the intended public reproducibility snapshot.
3. Rebuild `main.pdf` and inspect every page.
4. Upload `arxiv_upload.zip` to arXiv and verify the processed PDF before final submission.
