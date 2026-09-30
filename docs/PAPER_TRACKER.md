# Paper tracker and review workflow

## What runs automatically

Every Monday, `Discover Multimodal Retrieval Papers` searches arXiv, OpenAlex and Crossref with the queries in `config/paper-tracker.json`. Reviewers use DBLP and official conference pages to verify publication metadata. A DBLP fetcher is available in the script but is disabled by default because the public endpoint may present an anti-bot challenge to GitHub-hosted runners.

The tracker normalizes titles, arXiv IDs and DOIs, merges sources, scores relevance, removes known papers, and updates `data/candidates.json` on a dedicated pull-request branch. It never writes an unreviewed result into `data/papers.json` or `README.md`.

## Optional repository settings

- Secret `OPENALEX_API_KEY`: raises OpenAlex limits when an API key is available.
- Variable `PAPER_TRACKER_EMAIL`: identifies polite API traffic to OpenAlex and Crossref.
- `Settings → Actions → General → Workflow permissions`: select **Read and write permissions** and allow GitHub Actions to create pull requests.

## Review and accept a candidate

Read the full paper. Reject false positives, duplicate preprint/conference versions, papers without a material retrieval component, and papers without a large-model or agent connection. Select exactly one author-created Figure from the official PDF and pin that PDF version.

Priority: end-to-end framework → architecture → pipeline → method overview. For surveys and benchmarks, use taxonomy → benchmark pipeline → dataset construction when the earlier choices do not exist. Do not select result plots, tables, third-party illustrations, blogs, or recreated diagrams.

Record the SHA-256 (`shasum -a 256 paper.pdf`), one-based PDF page, and a crop rectangle in PDF points. The crop must preserve the full legend, subfigure labels, and arrows. Then accept the candidate:

```bash
python scripts/accept_candidate.py "unique title text" \
  --section "Agentic Multimodal Search" \
  --summary "Neutral one-sentence contribution summary." \
  --author "First Author" \
  --author "Second Author" \
  --year 2026 \
  --venue "Conference 2026" \
  --source-pdf-url "https://arxiv.org/pdf/0000.00000v1" \
  --source-pdf-sha256 "64-lowercase-hex-characters" \
  --figure-label "Figure 2" \
  --figure-kind "framework" \
  --figure-page 3 \
  --figure-crop "32,78,560,410" \
  --code-url "https://github.com/example/project"
```

The acceptance tool moves the candidate, verifies the pinned PDF hash, renders the PNG, and regenerates README. Finish with:

```bash
python scripts/extract_figure.py --all --verify-only
python scripts/generate_readme.py --check
python -m unittest discover -s tests -v
```

A candidate cannot appear in the formal README until all figure metadata is present and the PNG passes review. The automatic discovery PR must remain candidate-only.

## Figure rights

Each README image is accompanied by its Figure label, official PDF link, author credit, and rights notice. Add a license link only when an explicit reusable license is known. The repository does not copy full captions. Only whitespace cropping and lossless compression are permitted; no redraw, recoloring, or added content.

## Removing a rejected candidate

Delete it from `data/candidates.json` and add its normalized title to `ignored_titles` in `config/paper-tracker.json`. This prevents it from reappearing during the next scan.
