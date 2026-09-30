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

## Required metadata and original figure

Add reviewed papers to `data/papers.json`, not directly to the README. Each record needs a unique ID, title, authors, year, venue, canonical paper URL, optional code URL, section, neutral summary, and complete `figure` metadata.

The image must be an original figure from a pinned official paper PDF. Select in this order: end-to-end framework, architecture, pipeline, then method overview. For surveys and benchmarks, taxonomy, benchmark pipeline, or dataset construction may be used. Keep the complete legend, subfigure labels, and arrows. Only whitespace cropping and lossless PNG compression are allowed—do not redraw, recolor, annotate, or use third-party/AI-generated images.

Record the official PDF URL, SHA-256, one-based page number, Figure label, figure kind, crop rectangle in PDF points, and license URL when known. Then run:

```bash
python -m pip install -r requirements.txt
python scripts/extract_figure.py --paper-id PAPER_ID
python scripts/generate_readme.py
python scripts/extract_figure.py --all --verify-only
python scripts/generate_readme.py --check
python -m unittest discover -s tests -v
```

Temporary PDFs and page previews belong in `.figure-work/`; they must not be committed. Each accepted paper must have exactly one PNG at `assets/frameworks/PAPER_ID.png`. Copyright remains with the paper authors or publisher, and removal requests should be handled promptly.
