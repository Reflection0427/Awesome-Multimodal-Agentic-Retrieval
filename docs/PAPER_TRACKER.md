# Paper tracker and review workflow

## What runs automatically

Every Monday, `Discover Multimodal Retrieval Papers` searches arXiv, OpenAlex and Crossref with the queries in `config/paper-tracker.json`. Reviewers use DBLP and official conference pages to verify publication metadata. A DBLP fetcher is available in the script but is disabled by default because the public endpoint may present an anti-bot challenge to GitHub-hosted runners.

The tracker:

1. normalizes titles, arXiv IDs and DOIs;
2. merges results returned by multiple sources;
3. scores topical relevance;
4. removes papers already present in `data/papers.json`;
5. updates `data/candidates.json` on a dedicated pull-request branch.

The workflow never writes an unreviewed result into `data/papers.json` or `README.md`.

## Optional repository settings

- Secret `OPENALEX_API_KEY`: raises OpenAlex limits when an API key is available.
- Variable `PAPER_TRACKER_EMAIL`: identifies polite API traffic to OpenAlex and Crossref.
- `Settings → Actions → General → Workflow permissions`: select **Read and write permissions** and allow GitHub Actions to create pull requests.

## Review a candidate

Read the paper rather than relying only on its abstract. Reject false positives, duplicate preprint/conference versions, papers without a material retrieval component, and papers without a large-model or agent connection.

To accept one candidate:

```bash
python scripts/accept_candidate.py "unique title text" \
  --section "Agentic Multimodal Search" \
  --summary "Neutral one-sentence contribution summary." \
  --framework "Input and task" \
  --framework "Agent planning" \
  --framework "Iterative multimodal retrieval" \
  --framework "Grounded response" \
  --code-url "https://github.com/example/project"
```

Then run:

```bash
python scripts/generate_readme.py --check
python -m unittest discover -s tests -v
```

## Framework-figure policy

Every accepted paper must have 3–5 concise `framework` steps. The generator turns these reviewed steps into a consistent SVG reading aid shown directly after the paper entry.

The SVG must not imply that it is the paper authors' original illustration. Do not copy an author figure into this repository without confirming its license and recording attribution. When exact architecture details are uncertain, leave the paper in the candidate queue until a reviewer has checked the full text.

## Removing a rejected candidate

Delete it from `data/candidates.json` and add its normalized title to `ignored_titles` in `config/paper-tracker.json`. This prevents it from reappearing during the next scan.
