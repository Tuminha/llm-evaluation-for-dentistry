# arXiv Draft Notes

This directory contains the first arXiv-oriented manuscript draft.

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
- Comments: `8 pages, 2 figures; draft benchmark report`

## Before Submission

1. Confirm final author affiliation, funding, competing-interest wording, acknowledgments, and author contributions.
2. Push or archive the reviewed repository state, then insert the exact commit hash or DOI.
3. Rebuild `main.pdf` and inspect every page.
4. Upload `arxiv_upload.zip` to arXiv and verify the processed PDF before final submission.
