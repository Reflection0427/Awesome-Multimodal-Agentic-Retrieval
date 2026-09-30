#!/usr/bin/env python3
"""Render README.md from reviewed paper and original-figure metadata."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "papers.json"
README = ROOT / "README.md"

SECTION_ORDER = [
    "Surveys and Roadmaps",
    "Foundations",
    "Universal Multimodal Retrievers",
    "Visual Document Retrieval and RAG",
    "Agentic Multimodal Search",
]
SECTION_DESCRIPTIONS = {
    "Surveys and Roadmaps": "综述、分类体系与研究路线图。",
    "Foundations": "检索增强视觉语言模型与多模态生成的奠基工作。",
    "Universal Multimodal Retrievers": "由 MLLM 驱动的统一检索器、Embedding 与推理型检索基准。",
    "Visual Document Retrieval and RAG": "面向页面图像、布局、图表和长文档的检索增强生成。",
    "Agentic Multimodal Search": "能够规划、迭代检索、检查证据并核验来源的多模态 Agent。",
}
FIGURE_KINDS = {"framework", "architecture", "pipeline", "overview", "taxonomy", "benchmark", "dataset"}
OFFICIAL_PDF_HOSTS = {
    "aclanthology.org",
    "arxiv.org",
    "openaccess.thecvf.com",
    "raw.githubusercontent.com",
}


def load_papers() -> list[dict]:
    papers = json.loads(DATA.read_text(encoding="utf-8"))
    required = {"id", "title", "authors", "year", "venue", "paper_url", "section", "summary", "figure"}
    ids: set[str] = set()
    figure_paths: set[str] = set()
    for paper in papers:
        missing = required - paper.keys()
        if missing:
            raise ValueError(f"{paper.get('title', '<unknown>')} missing {sorted(missing)}")
        if paper["id"] in ids:
            raise ValueError(f"duplicate paper id: {paper['id']}")
        ids.add(paper["id"])
        if not paper["authors"] or not all(isinstance(author, str) and author.strip() for author in paper["authors"]):
            raise ValueError(f"{paper['id']} must have at least one author")
        if paper["section"] not in SECTION_ORDER:
            raise ValueError(f"unknown section: {paper['section']}")
        figure = paper["figure"]
        figure_required = {
            "path", "source_pdf_url", "source_pdf_sha256", "figure_label",
            "figure_kind", "page", "crop_pt", "license_url",
        }
        figure_missing = figure_required - figure.keys()
        if figure_missing:
            raise ValueError(f"{paper['id']} figure missing {sorted(figure_missing)}")
        expected_path = f"assets/frameworks/{paper['id']}.png"
        if figure["path"] != expected_path:
            raise ValueError(f"{paper['id']} figure path must be {expected_path}")
        if figure["path"] in figure_paths:
            raise ValueError(f"duplicate figure path: {figure['path']}")
        figure_paths.add(figure["path"])
        if figure["figure_kind"] not in FIGURE_KINDS:
            raise ValueError(f"{paper['id']} has invalid figure kind")
        if not str(figure["figure_label"]).startswith("Figure "):
            raise ValueError(f"{paper['id']} must identify the original Figure number")
        if not isinstance(figure["page"], int) or figure["page"] < 1:
            raise ValueError(f"{paper['id']} has invalid PDF page")
        crop = figure["crop_pt"]
        if not (isinstance(crop, list) and len(crop) == 4 and all(isinstance(value, (int, float)) for value in crop)):
            raise ValueError(f"{paper['id']} has invalid crop_pt")
        if crop[0] >= crop[2] or crop[1] >= crop[3]:
            raise ValueError(f"{paper['id']} has an empty crop")
        if len(figure["source_pdf_sha256"]) != 64 or any(character not in "0123456789abcdef" for character in figure["source_pdf_sha256"]):
            raise ValueError(f"{paper['id']} has invalid PDF SHA-256")
        parsed = urlparse(figure["source_pdf_url"])
        if parsed.scheme != "https" or parsed.hostname not in OFFICIAL_PDF_HOSTS:
            raise ValueError(f"{paper['id']} does not use an approved official PDF host")
    return papers


def short_credit(authors: list[str]) -> str:
    return authors[0] if len(authors) == 1 else f"{authors[0]} et al."


def paper_markdown(paper: dict) -> str:
    code = f" · [Code / Project]({paper['code_url']})" if paper.get("code_url") else ""
    figure = paper["figure"]
    license_link = f' · <a href="{figure["license_url"]}">License</a>' if figure.get("license_url") else ""
    title_attr = html.escape(paper["title"], quote=True)
    return "\n".join([
        f"### {paper['title']}",
        "",
        f"**{paper['venue']}** · [Paper]({paper['paper_url']}){code}",
        "",
        paper["summary"],
        "",
        f'<img src="{figure["path"]}" alt="Original {html.escape(figure["figure_label"], quote=True)} from {title_attr}" width="100%">',
        "",
        (
            f'<sub>Original paper figure: <strong>{html.escape(figure["figure_label"])}</strong> · '
            f'<a href="{figure["source_pdf_url"]}">Source: official PDF</a> · '
            f'Credit: {html.escape(short_credit(paper["authors"]))} · '
            f'© Paper authors/publisher. All rights remain with the original owner.{license_link}</sub>'
        ),
        "",
    ])


def render_readme(papers: list[dict]) -> str:
    counts = Counter(paper["section"] for paper in papers)
    latest = max(paper["year"] for paper in papers)
    lines = [
        "# Awesome Multimodal Agentic Retrieval", "",
        "[![Discover Papers](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/discover-papers.yml/badge.svg)](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/discover-papers.yml)",
        "[![Validate](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/validate.yml/badge.svg)](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/validate.yml)",
        "",
        "A curated collection of papers on **multimodal retrieval, multimodal RAG, visual-document retrieval, and agentic multimodal search**.", "",
        "本仓库关注“大模型如何参与多模态检索，以及检索如何增强多模态大模型与 Agent”。每篇正式收录论文后均展示从官方 PDF 裁取的**论文作者原始 Figure**，并标注 Figure 编号、官方来源和权利归属；仓库不使用 AI 生成图或自绘框架图。", "",
        f"**{len(papers)} papers · through {latest} · weekly candidate PRs · human-reviewed merges**", "",
        "## Scope", "",
        "Included: MLLM retrievers and rerankers, multimodal embeddings, multimodal RAG, visual-document retrieval, multimodal browsing/search agents, and directly related surveys or benchmarks.", "",
        "Excluded: conventional image-text retrieval without a large-model or agent component, multimodal generation without external retrieval, and GUI agents unrelated to information retrieval.", "",
        "## Contents", "",
    ]
    for section in SECTION_ORDER:
        anchor = section.lower().replace(" ", "-").replace("/", "")
        lines.append(f"- [{section} ({counts[section]})](#{anchor})")
    lines += ["- [Benchmarks](#benchmarks)", "- [Automatic paper tracking](#automatic-paper-tracking)", "- [Contributing](#contributing)", ""]
    for section in SECTION_ORDER:
        lines += [f"## {section}", "", SECTION_DESCRIPTIONS[section], ""]
        selected = sorted((paper for paper in papers if paper["section"] == section), key=lambda paper: (-paper["year"], paper["title"].lower()))
        for paper in selected:
            lines.append(paper_markdown(paper))
    lines += [
        "## Benchmarks", "", "| Benchmark | Focus | Paper |", "|---|---|---|",
        "| M-BEIR | Universal multi-task, cross-modal retrieval | [UniIR](https://arxiv.org/abs/2311.17136) |",
        "| ViDoRe | Visual document page retrieval | [ColPali](https://arxiv.org/abs/2407.01449) |",
        "| MMDocIR | Long multimodal document retrieval | [MMDocIR](https://aclanthology.org/2025.emnlp-main.1576/) |",
        "| MMDocRAG | Joint document retrieval and generation | [MMDocRAG](https://arxiv.org/abs/2505.16470) |",
        "| MC-Search | Multimodal agentic search and long reasoning chains | [MC-Search](https://arxiv.org/abs/2603.00873) |",
        "| MMSearch-Plus | Browsing, provenance and evidence verification | [MMSearch-Plus](https://arxiv.org/abs/2508.21475) |",
        "| RMIR | Reasoning-intensive image retrieval | [RMIR](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_RMIR_A_Benchmark_Dataset_for_Reasoning-Intensive_Multimodal_Image_Retrieval_CVPR_2026_paper.pdf) |",
        "| VQQP-Bench | Agentic visual-query preprocessing | [Fix Before Search](https://proceedings.mlr.press/v306/zeng26w.html) |", "",
        "## Automatic paper tracking", "",
        "The scheduled workflow searches arXiv, OpenAlex and Crossref every Monday. It normalizes arXiv IDs, DOIs and titles, removes duplicates, classifies likely matches, and opens or updates a candidate pull request. DBLP and official conference pages are used during human venue verification. It **never publishes a candidate directly to this README**.", "",
        "A paper becomes visible only after a reviewer verifies its metadata and relevance, selects an original framework/overview figure from the official PDF, records reproducible page and crop metadata, and merges the pull request. See [the tracker guide](docs/PAPER_TRACKER.md).", "",
        "## Contributing", "",
        "Please open an issue or pull request. Add reviewed entries to `data/papers.json`, reproduce their original figures with `scripts/extract_figure.py`, and run:", "",
        "```bash", "python scripts/extract_figure.py --all --verify-only", "python scripts/generate_readme.py --check", "python -m unittest discover -s tests -v", "```", "",
        "## Figure rights and repository license", "",
        "Repository code and curator-authored metadata are released under the MIT License. Images in `assets/frameworks/` are cropped excerpts of figures from the linked papers, shown for scholarly indexing and commentary. Copyright and all other rights remain with the paper authors or publishers. Each image links to its official source; entries with an explicit reusable license also link that license. Please open an issue for correction or removal requests.", "",
    ]
    return "\n".join(lines)


def build() -> str:
    return render_readme(load_papers())


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when README.md is stale")
    args = parser.parse_args()
    readme = build()
    if args.check:
        if not README.exists() or README.read_text(encoding="utf-8") != readme:
            print("README.md is stale; run python scripts/generate_readme.py")
            return 1
        print("README.md is up to date.")
        return 0
    README.write_text(readme, encoding="utf-8")
    print(f"Rendered {README.name} from {len(load_papers())} reviewed papers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
