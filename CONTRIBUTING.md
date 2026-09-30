# Contributing

Thank you for helping maintain the collection.

## Inclusion criteria

A paper should materially address at least one of these areas:

- large multimodal models used as retrievers, embedders or rerankers;
- multimodal retrieval-augmented generation;
- visual-document retrieval or RAG;
- multimodal search/browsing agents;
- a directly relevant survey, dataset or benchmark.

Ordinary image-text retrieval without a large-model or agent component is out of scope.

## Required metadata

Add reviewed papers to `data/papers.json`, not directly to the README. Each record needs a unique ID, title, year, venue, canonical paper URL, optional code URL, section, neutral summary, and 3–5 framework steps.

Run `python scripts/generate_readme.py` to regenerate the README and SVG files. Both validation commands documented in the README must pass before opening a pull request.
