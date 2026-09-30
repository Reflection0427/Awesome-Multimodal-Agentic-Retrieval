#!/usr/bin/env python3
"""Render the README and one self-contained SVG framework summary per paper."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "papers.json"
ASSETS = ROOT / "assets" / "frameworks"
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


def load_papers() -> list[dict]:
    papers = json.loads(DATA.read_text(encoding="utf-8"))
    required = {"id", "title", "year", "venue", "paper_url", "section", "summary", "framework"}
    ids: set[str] = set()
    for paper in papers:
        missing = required - paper.keys()
        if missing:
            raise ValueError(f"{paper.get('title', '<unknown>')} missing {sorted(missing)}")
        if paper["id"] in ids:
            raise ValueError(f"duplicate paper id: {paper['id']}")
        ids.add(paper["id"])
        if paper["section"] not in SECTION_ORDER:
            raise ValueError(f"unknown section: {paper['section']}")
        if not 3 <= len(paper["framework"]) <= 5:
            raise ValueError(f"{paper['id']} must have 3-5 framework steps")
    return papers


def wrap_label(label: str, width: int = 25) -> list[str]:
    words = label.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:3]


def render_svg(paper: dict) -> str:
    steps = paper["framework"]
    box_w, box_h, gap, margin = 210, 116, 64, 36
    width = margin * 2 + len(steps) * box_w + (len(steps) - 1) * gap
    height = 210
    colors = ["#E8F1FF", "#EAF9F0", "#FFF4DE", "#F1ECFF", "#FFECEF"]
    strokes = ["#3976D3", "#31946B", "#D58B18", "#7654C4", "#C84D74"]
    title = html.escape(paper["title"])
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">Framework summary for {title}</title>',
        '<desc id="desc">A curator-authored structural summary. It is not a reproduction of the paper figure.</desc>',
        '<rect width="100%" height="100%" rx="18" fill="#FFFFFF" stroke="#D9E2F0"/>',
        '<text x="36" y="32" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="700" fill="#17233C">CURATOR-DRAWN FRAMEWORK SUMMARY</text>',
    ]
    y = 58
    for index, step in enumerate(steps):
        x = margin + index * (box_w + gap)
        pieces.append(
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="14" '
            f'fill="{colors[index % len(colors)]}" stroke="{strokes[index % len(strokes)]}" stroke-width="2"/>'
        )
        pieces.append(
            f'<circle cx="{x + 25}" cy="{y + 25}" r="14" fill="{strokes[index % len(strokes)]}"/>'
        )
        pieces.append(
            f'<text x="{x + 25}" y="{y + 30}" text-anchor="middle" font-family="Arial" '
            f'font-size="14" font-weight="700" fill="#FFFFFF">{index + 1}</text>'
        )
        lines = wrap_label(step)
        start_y = y + 60 - (len(lines) - 1) * 10
        for offset, line in enumerate(lines):
            pieces.append(
                f'<text x="{x + box_w / 2}" y="{start_y + offset * 22}" text-anchor="middle" '
                f'font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="600" '
                f'fill="#17233C">{html.escape(line)}</text>'
            )
        if index < len(steps) - 1:
            x1, x2, arrow_y = x + box_w + 10, x + box_w + gap - 12, y + box_h / 2
            pieces.append(
                f'<path d="M {x1} {arrow_y} L {x2} {arrow_y}" stroke="#73819A" stroke-width="3" '
                f'stroke-linecap="round"/>'
            )
            pieces.append(
                f'<path d="M {x2 - 9} {arrow_y - 7} L {x2} {arrow_y} L {x2 - 9} {arrow_y + 7}" '
                f'fill="none" stroke="#73819A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            )
    pieces.append(
        '<text x="36" y="196" font-family="Arial, Helvetica, sans-serif" font-size="12" '
        'fill="#667085">Structural reading aid by this repository; consult the paper for the authors’ original figure and details.</text>'
    )
    pieces.append("</svg>")
    return "\n".join(pieces) + "\n"


def paper_markdown(paper: dict) -> str:
    code = f" · [Code / Project]({paper['code_url']})" if paper.get("code_url") else ""
    return "\n".join([
        f"### {paper['title']}",
        "",
        f"**{paper['venue']}** · [Paper]({paper['paper_url']}){code}",
        "",
        paper["summary"],
        "",
        f'<img src="assets/frameworks/{paper["id"]}.svg" alt="Framework summary for {html.escape(paper["title"], quote=True)}" width="100%">',
        "",
    ])


def render_readme(papers: list[dict]) -> str:
    counts = Counter(p["section"] for p in papers)
    latest = max(p["year"] for p in papers)
    lines = [
        "# Awesome Multimodal Agentic Retrieval",
        "",
        "[![Discover Papers](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/discover-papers.yml/badge.svg)](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/discover-papers.yml)",
        "[![Validate](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/validate.yml/badge.svg)](https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval/actions/workflows/validate.yml)",
        "",
        "A curated collection of papers on **multimodal retrieval, multimodal RAG, visual-document retrieval, and agentic multimodal search**.",
        "",
        "本仓库关注“大模型如何参与多模态检索，以及检索如何增强多模态大模型与 Agent”。每篇正式收录论文都配有一张统一风格的**自绘结构摘要图**。这些图是便于快速阅读的结构化总结，并非论文原图；技术细节请以原论文为准。",
        "",
        f"**{len(papers)} papers · through {latest} · weekly candidate PRs · human-reviewed merges**",
        "",
        "## Scope",
        "",
        "Included: MLLM retrievers and rerankers, multimodal embeddings, multimodal RAG, visual-document retrieval, multimodal browsing/search agents, and directly related surveys or benchmarks.",
        "",
        "Excluded: conventional image-text retrieval without a large-model or agent component, multimodal generation without external retrieval, and GUI agents unrelated to information retrieval.",
        "",
        "## Contents",
        "",
    ]
    for section in SECTION_ORDER:
        anchor = section.lower().replace(" ", "-").replace("/", "")
        lines.append(f"- [{section} ({counts[section]})](#{anchor})")
    lines += [
        "- [Benchmarks](#benchmarks)",
        "- [Automatic paper tracking](#automatic-paper-tracking)",
        "- [Contributing](#contributing)",
        "",
    ]
    for section in SECTION_ORDER:
        lines += [f"## {section}", "", SECTION_DESCRIPTIONS[section], ""]
        selected = sorted(
            (p for p in papers if p["section"] == section),
            key=lambda p: (-p["year"], p["title"].lower()),
        )
        for paper in selected:
            lines.append(paper_markdown(paper))
    lines += [
        "## Benchmarks",
        "",
        "| Benchmark | Focus | Paper |",
        "|---|---|---|",
        "| M-BEIR | Universal multi-task, cross-modal retrieval | [UniIR](https://arxiv.org/abs/2311.17136) |",
        "| ViDoRe | Visual document page retrieval | [ColPali](https://arxiv.org/abs/2407.01449) |",
        "| MMDocIR | Long multimodal document retrieval | [MMDocIR](https://aclanthology.org/2025.emnlp-main.1576/) |",
        "| MMDocRAG | Joint document retrieval and generation | [MMDocRAG](https://arxiv.org/abs/2505.16470) |",
        "| MC-Search | Multimodal agentic search and long reasoning chains | [MC-Search](https://arxiv.org/abs/2603.00873) |",
        "| MMSearch-Plus | Browsing, provenance and evidence verification | [MMSearch-Plus](https://arxiv.org/abs/2508.21475) |",
        "| RMIR | Reasoning-intensive image retrieval | [RMIR](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_RMIR_A_Benchmark_Dataset_for_Reasoning-Intensive_Multimodal_Image_Retrieval_CVPR_2026_paper.pdf) |",
        "| VQQP-Bench | Agentic visual-query preprocessing | [Fix Before Search](https://proceedings.mlr.press/v306/zeng26w.html) |",
        "",
        "## Automatic paper tracking",
        "",
        "The scheduled workflow searches arXiv, OpenAlex and Crossref every Monday. It normalizes arXiv IDs, DOIs and titles, removes duplicates, classifies likely matches, and opens or updates a candidate pull request. DBLP and official conference pages are used during human venue verification. It **never publishes a candidate directly to this README**.",
        "",
        "A paper becomes visible only after a reviewer verifies its relevance and metadata, supplies a curator-authored framework summary, and merges the pull request. See [the tracker guide](docs/PAPER_TRACKER.md).",
        "",
        "## Contributing",
        "",
        "Please open an issue or pull request. Every accepted entry must include verifiable paper metadata, an appropriate category, a concise neutral summary, and 3–5 framework steps. Run:",
        "",
        "```bash",
        "python scripts/generate_readme.py --check",
        "python -m unittest discover -s tests -v",
        "```",
        "",
        "## License and figure policy",
        "",
        "Repository code and curator-authored metadata/diagrams are released under the MIT License. Papers, linked project assets, and author-created figures remain the property of their respective owners. The SVGs in `assets/frameworks/` are original reading aids generated from manually reviewed structural summaries; they are not reproductions of paper figures.",
        "",
    ]
    return "\n".join(lines)


def build() -> tuple[str, dict[Path, str]]:
    papers = load_papers()
    assets = {ASSETS / f"{paper['id']}.svg": render_svg(paper) for paper in papers}
    return render_readme(papers), assets


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when generated files are stale")
    args = parser.parse_args()
    readme, assets = build()
    expected = {README: readme, **assets}
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, content in expected.items()
                 if not path.exists() or path.read_text(encoding="utf-8") != content]
        extras = sorted(ASSETS.glob("*.svg")) if ASSETS.exists() else []
        valid = set(assets)
        stale.extend(str(path.relative_to(ROOT)) for path in extras if path not in valid)
        if stale:
            print("Generated files are stale:")
            print("\n".join(f"- {path}" for path in stale))
            return 1
        print(f"README and {len(assets)} framework diagrams are up to date.")
        return 0
    ASSETS.mkdir(parents=True, exist_ok=True)
    for path in ASSETS.glob("*.svg"):
        if path not in assets:
            path.unlink()
    README.write_text(readme, encoding="utf-8")
    for path, content in assets.items():
        path.write_text(content, encoding="utf-8")
    print(f"Rendered {README.name} and {len(assets)} framework diagrams.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
