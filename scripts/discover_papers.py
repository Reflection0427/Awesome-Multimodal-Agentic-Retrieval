#!/usr/bin/env python3
"""Discover recent papers and update the human-review candidate queue.

This script never edits data/papers.json or README.md. Its only persistent
output is data/candidates.json, which the scheduled workflow proposes in a PR.
"""

from __future__ import annotations

import argparse
import html
import http.client
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "paper-tracker.json"
PAPERS_PATH = ROOT / "data" / "papers.json"
CANDIDATES_PATH = ROOT / "data" / "candidates.json"
REPORT_DIR = ROOT / ".paper-tracker"
USER_AGENT = "awesome-multimodal-agentic-retrieval/1.0 (+https://github.com/Reflection0427/Awesome-Multimodal-Agentic-Retrieval)"
ARXIV_RE = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/|arxiv:)(\d{4}\.\d{4,5})(?:v\d+)?", re.I)


@dataclass
class Candidate:
    title: str
    paper_url: str
    published: str = ""
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    venue: str = ""
    doi: str = ""
    arxiv_id: str = ""
    sources: list[str] = field(default_factory=list)
    score: int = 0
    reasons: list[str] = field(default_factory=list)
    suggested_section: str = "Foundations"
    status: str = "needs-review"
    framework: list[str] = field(default_factory=list)


def compact(value: Any) -> str:
    return re.sub(r"\s+", " ", html.unescape(str(value or ""))).strip()


def normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", compact(value).lower())


def normalize_doi(value: str) -> str:
    value = compact(value).lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return value.rstrip(".,;)")


def normalize_arxiv(value: str) -> str:
    match = ARXIV_RE.search(value or "")
    return match.group(1) if match else ""


def request(url: str, params: dict[str, Any], accept: str) -> bytes:
    target = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(target, headers={"User-Agent": USER_AGENT, "Accept": accept})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                return response.read()
        except (urllib.error.URLError, http.client.HTTPException, OSError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def get_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    return json.loads(request(url, params, "application/json").decode("utf-8"))


def fetch_arxiv(query: str, since: str, limit: int) -> list[Candidate]:
    search = " AND ".join(f'all:"{term}"' for term in query.split())
    xml = request("https://export.arxiv.org/api/query", {
        "search_query": search,
        "start": 0,
        "max_results": limit,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }, "application/atom+xml").decode("utf-8")
    root = ET.fromstring(xml)
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    found = []
    for entry in root.findall("a:entry", ns):
        published = compact(entry.findtext("a:published", default="", namespaces=ns))[:10]
        if published and published < since:
            continue
        raw_id = compact(entry.findtext("a:id", default="", namespaces=ns))
        arxiv_id = normalize_arxiv(raw_id)
        found.append(Candidate(
            title=compact(entry.findtext("a:title", default="", namespaces=ns)),
            paper_url=f"https://arxiv.org/abs/{arxiv_id}",
            published=published,
            authors=[compact(a.findtext("a:name", default="", namespaces=ns)) for a in entry.findall("a:author", ns)],
            abstract=compact(entry.findtext("a:summary", default="", namespaces=ns)),
            venue=compact(entry.findtext("x:journal_ref", default="", namespaces=ns)),
            doi=normalize_doi(entry.findtext("x:doi", default="", namespaces=ns)),
            arxiv_id=arxiv_id,
            sources=["arXiv"],
        ))
    return found


def reconstruct_abstract(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    words = [(position, word) for word, positions in index.items() for position in positions]
    return " ".join(word for _, word in sorted(words))


def fetch_openalex(query: str, since: str, limit: int) -> list[Candidate]:
    params: dict[str, Any] = {
        "search": query,
        "filter": f"from_publication_date:{since}",
        "sort": "publication_date:desc",
        "per_page": min(limit, 100),
    }
    if os.getenv("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    if os.getenv("PAPER_TRACKER_EMAIL"):
        params["mailto"] = os.environ["PAPER_TRACKER_EMAIL"]
    data = get_json("https://api.openalex.org/works", params)
    found = []
    for item in data.get("results", []):
        ids = item.get("ids") or {}
        location = item.get("best_oa_location") or item.get("primary_location") or {}
        source = (location.get("source") or {}).get("display_name", "")
        arxiv_id = normalize_arxiv(ids.get("arxiv", ""))
        doi = normalize_doi(ids.get("doi", ""))
        found.append(Candidate(
            title=compact(item.get("display_name") or item.get("title")),
            paper_url=ids.get("arxiv") or ids.get("doi") or location.get("landing_page_url") or item.get("id", ""),
            published=compact(item.get("publication_date"))[:10],
            authors=[compact(x.get("author", {}).get("display_name")) for x in item.get("authorships", [])],
            abstract=reconstruct_abstract(item.get("abstract_inverted_index")),
            venue=compact(source),
            doi=doi,
            arxiv_id=arxiv_id,
            sources=["OpenAlex"],
        ))
    return found


def crossref_date(item: dict[str, Any]) -> str:
    for key in ("published-online", "published-print", "issued", "created"):
        parts = (item.get(key) or {}).get("date-parts") or []
        if parts:
            values = parts[0]
            return "-".join(str(v).zfill(2) for v in values[:3])
    return ""


def fetch_crossref(query: str, since: str, limit: int) -> list[Candidate]:
    params: dict[str, Any] = {
        "query.bibliographic": query,
        "filter": f"from-pub-date:{since}",
        "rows": limit,
    }
    if os.getenv("PAPER_TRACKER_EMAIL"):
        params["mailto"] = os.environ["PAPER_TRACKER_EMAIL"]
    data = get_json("https://api.crossref.org/works", params)
    found = []
    for item in data.get("message", {}).get("items", []):
        doi = normalize_doi(item.get("DOI", ""))
        found.append(Candidate(
            title=compact((item.get("title") or [""])[0]),
            paper_url=item.get("URL") or (f"https://doi.org/{doi}" if doi else ""),
            published=crossref_date(item),
            authors=[compact(" ".join(filter(None, [a.get("given"), a.get("family")]))) for a in item.get("author", [])],
            abstract=compact(re.sub(r"<[^>]+>", " ", item.get("abstract", ""))),
            venue=compact((item.get("container-title") or [""])[0]),
            doi=doi,
            arxiv_id=normalize_arxiv(doi),
            sources=["Crossref"],
        ))
    return found


def fetch_dblp(query: str, since: str, limit: int) -> list[Candidate]:
    data = get_json("https://dblp.org/search/publ/api", {"q": query, "format": "json", "h": limit})
    hits = data.get("result", {}).get("hits", {}).get("hit", [])
    if isinstance(hits, dict):
        hits = [hits]
    found = []
    for hit in hits:
        info = hit.get("info", {})
        year = str(info.get("year", ""))
        if year and f"{year}-12-31" < since:
            continue
        author_rows = (info.get("authors") or {}).get("author", [])
        if isinstance(author_rows, (str, dict)):
            author_rows = [author_rows]
        authors = [compact(a.get("text") if isinstance(a, dict) else a) for a in author_rows]
        url = info.get("ee") or info.get("url") or ""
        if isinstance(url, list):
            url = url[0] if url else ""
        found.append(Candidate(
            title=compact(re.sub(r"<[^>]+>", "", info.get("title", ""))),
            paper_url=compact(url),
            published=f"{year}-01-01" if year else "",
            authors=authors,
            venue=compact(info.get("venue", "")),
            doi=normalize_doi(info.get("doi", "")),
            arxiv_id=normalize_arxiv(url),
            sources=["DBLP"],
        ))
    return found


FETCHERS: dict[str, Callable[[str, str, int], list[Candidate]]] = {
    "arxiv": fetch_arxiv,
    "openalex": fetch_openalex,
    "crossref": fetch_crossref,
    "dblp": fetch_dblp,
}


def classify(text: str) -> str:
    if any(term in text for term in ("survey", "systematic review", "roadmap")):
        return "Surveys and Roadmaps"
    if any(term in text for term in ("agentic", "search agent", "browsing agent", "planning agent")):
        return "Agentic Multimodal Search"
    if any(term in text for term in ("document", "visually rich", "page retrieval", "layout-aware")):
        return "Visual Document Retrieval and RAG"
    if any(term in text for term in ("embedding", "universal retriev", "bi-encoder", "rerank")):
        return "Universal Multimodal Retrievers"
    return "Foundations"


def score(candidate: Candidate) -> None:
    title = candidate.title.lower()
    text = f"{candidate.title} {candidate.abstract} {candidate.venue}".lower()
    strong = [
        "multimodal retrieval-augmented", "multimodal retrieval augmented",
        "multimodal rag", "multimodal search agent", "agentic multimodal",
        "visual document retrieval", "multimodal retrieval", "multimodal embedding",
        "vision-based retrieval-augmented", "visually-rich document retrieval",
    ]
    supporting = {
        "agent or planning": ("agent", "agentic", "planning", "iterative search"),
        "large multimodal model": ("mllm", "multimodal large language", "vision-language model", "vlm"),
        "retrieval": ("retrieval", "retriever", "rerank", "search"),
        "multiple modalities": ("multimodal", "multi-modal", "image-text", "text-vision", "visual document"),
        "RAG": ("retrieval-augmented", "retrieval augmented", " rag "),
        "evidence grounding": ("evidence", "provenance", "grounded", "citation"),
    }
    points = 0
    reasons = []
    for phrase in strong:
        if phrase in text:
            bonus = 6 if phrase in title else 4
            points += bonus
            reasons.append(f"strong phrase: {phrase}")
            break
    for label, terms in supporting.items():
        if any(term in f" {text} " for term in terms):
            points += 1
            reasons.append(label)
    has_retrieval = any(term in text for term in ("retriev", "search", "rerank"))
    has_modality = any(term in text for term in ("multimodal", "multi-modal", "visual", "image", "video", "audio"))
    if not has_retrieval or not has_modality:
        points -= 8
        reasons.append("missing retrieval or multimodal evidence")
    candidate.score = points
    candidate.reasons = reasons
    candidate.suggested_section = classify(text)


def same_paper(left: Candidate, right: Candidate) -> bool:
    if left.arxiv_id and left.arxiv_id == right.arxiv_id:
        return True
    if left.doi and left.doi == right.doi:
        return True
    a, b = normalize_title(left.title), normalize_title(right.title)
    return bool(a and b and (a == b or SequenceMatcher(None, a, b).ratio() >= 0.94))


def merge(left: Candidate, right: Candidate) -> Candidate:
    preferred = left if len(left.abstract) >= len(right.abstract) else right
    other = right if preferred is left else left
    for name in ("paper_url", "published", "venue", "doi", "arxiv_id", "abstract"):
        if not getattr(preferred, name):
            setattr(preferred, name, getattr(other, name))
    if not preferred.authors:
        preferred.authors = other.authors
    preferred.sources = sorted(set(preferred.sources + other.sources))
    return preferred


def existing_candidates() -> list[Candidate]:
    if not CANDIDATES_PATH.exists():
        return []
    return [Candidate(**row) for row in json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))]


def is_listed(candidate: Candidate, papers: list[dict]) -> bool:
    for paper in papers:
        listed = Candidate(
            title=paper["title"], paper_url=paper["paper_url"],
            doi=paper.get("doi", ""), arxiv_id=normalize_arxiv(paper["paper_url"]),
        )
        if same_paper(candidate, listed):
            return True
    return False


def write_outputs(candidates: list[Candidate], failures: list[str]) -> None:
    rows = [asdict(item) for item in sorted(candidates, key=lambda c: (-c.score, c.title.lower()))]
    CANDIDATES_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_DIR.mkdir(exist_ok=True)
    lines = [
        "# Multimodal Agentic Retrieval candidate report", "",
        f"Candidates awaiting human review: **{len(rows)}**", "",
        "Candidates are not added to the public README until their metadata, category and framework summary are reviewed.", "",
    ]
    for item in candidates:
        lines += [
            f"## [{item.title}]({item.paper_url})", "",
            f"- Score: `{item.score}`",
            f"- Suggested section: `{item.suggested_section}`",
            f"- Published: `{item.published or 'unknown'}`",
            f"- Sources: {', '.join(item.sources)}",
            f"- Reasons: {', '.join(item.reasons)}", "",
            compact(item.abstract)[:700] + ("…" if len(compact(item.abstract)) > 700 else ""), "",
        ]
    if failures:
        lines += ["## Source failures", ""] + [f"- {failure}" for failure in failures] + [""]
    (REPORT_DIR / "report.md").write_text("\n".join(lines), encoding="utf-8")
    output = os.getenv("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"candidate_count={len(rows)}\n")
            handle.write(f"failure_count={len(failures)}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    since = (date.today() - timedelta(days=int(config["lookback_days"]))).isoformat()
    collected: list[Candidate] = []
    failures: list[str] = []
    for source in config["sources"]:
        fetcher = FETCHERS[source]
        consecutive_failures = 0
        for query in config["queries"]:
            try:
                collected.extend(fetcher(query, since, int(config["max_results_per_query"])))
                consecutive_failures = 0
            except Exception as exc:  # keep other sources useful during partial outages
                failures.append(f"{source} / {query}: {type(exc).__name__}: {exc}")
                consecutive_failures += 1
                if consecutive_failures >= 2:
                    failures.append(f"{source}: remaining queries skipped after two consecutive failures")
                    break
    merged: list[Candidate] = []
    for candidate in collected:
        if not candidate.title:
            continue
        match = next((item for item in merged if same_paper(candidate, item)), None)
        if match:
            merged[merged.index(match)] = merge(match, candidate)
        else:
            merged.append(candidate)
    papers = json.loads(PAPERS_PATH.read_text(encoding="utf-8"))
    ignored_titles = {normalize_title(x) for x in config.get("ignored_titles", [])}
    fresh = []
    for candidate in merged:
        score(candidate)
        if candidate.score < int(config["minimum_score"]):
            continue
        if normalize_title(candidate.title) in ignored_titles or is_listed(candidate, papers):
            continue
        fresh.append(candidate)
    queue = existing_candidates()
    for candidate in fresh:
        match = next((item for item in queue if same_paper(candidate, item)), None)
        if match:
            queue[queue.index(match)] = merge(match, candidate)
        else:
            queue.append(candidate)
    queue = sorted(queue, key=lambda c: (-c.score, c.title.lower()))[: int(config["max_candidates"])]
    write_outputs(queue, failures)
    print(f"Discovered {len(fresh)} relevant unlisted papers; candidate queue contains {len(queue)}.")
    if failures:
        print(f"Completed with {len(failures)} source-query failures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
