import json
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import discover_papers  # noqa: E402
import extract_figure  # noqa: E402
import generate_readme  # noqa: E402


class CollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.papers = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))

    def test_seed_collection_size(self):
        self.assertEqual(len(self.papers), 37)

    def test_ids_and_titles_are_unique(self):
        ids = [paper["id"] for paper in self.papers]
        titles = [discover_papers.normalize_title(paper["title"]) for paper in self.papers]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(titles), len(set(titles)))

    def test_metadata_and_original_figure_schema(self):
        for paper in self.papers:
            with self.subTest(paper=paper["id"]):
                self.assertIn(paper["section"], generate_readme.SECTION_ORDER)
                self.assertTrue(paper["paper_url"].startswith("https://"))
                self.assertGreaterEqual(paper["year"], 2022)
                self.assertLessEqual(paper["year"], 2100)
                self.assertTrue(paper["authors"])
                self.assertNotIn("framework", paper)
                figure = paper["figure"]
                self.assertEqual(figure["path"], f"assets/frameworks/{paper['id']}.png")
                self.assertIn(figure["figure_kind"], generate_readme.FIGURE_KINDS)
                self.assertRegex(figure["figure_label"], r"^Figure [A-Za-z0-9.-]+$")
                self.assertGreaterEqual(figure["page"], 1)
                self.assertEqual(len(figure["crop_pt"]), 4)
                self.assertLess(figure["crop_pt"][0], figure["crop_pt"][2])
                self.assertLess(figure["crop_pt"][1], figure["crop_pt"][3])
                self.assertRegex(figure["source_pdf_sha256"], r"^[0-9a-f]{64}$")
                source = urlparse(figure["source_pdf_url"])
                self.assertEqual(source.scheme, "https")
                self.assertIn(source.hostname, generate_readme.OFFICIAL_PDF_HOSTS)

    def test_committed_original_pngs(self):
        expected = {ROOT / paper["figure"]["path"] for paper in self.papers}
        actual_pngs = set((ROOT / "assets" / "frameworks").glob("*.png"))
        self.assertEqual(actual_pngs, expected)
        self.assertEqual(len(actual_pngs), 37)
        self.assertEqual(list((ROOT / "assets" / "frameworks").glob("*.svg")), [])
        for path in sorted(actual_pngs):
            with self.subTest(image=path.name):
                extract_figure.validate_image(path)

    def test_generated_readme_is_current_and_attributed(self):
        expected = generate_readme.build()
        actual = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(expected, actual)
        self.assertEqual(actual.count('<img src="assets/frameworks/'), 37)
        self.assertEqual(actual.count("Original paper figure:"), 37)
        self.assertEqual(actual.count("© Paper authors/publisher."), 37)
        self.assertNotIn("CURATOR-DRAWN", actual)
        self.assertNotRegex(actual, r'assets/frameworks/[^" ]+\.svg')

    def test_candidate_queue_schema(self):
        candidates = json.loads((ROOT / "data" / "candidates.json").read_text(encoding="utf-8"))
        titles = []
        for candidate in candidates:
            with self.subTest(candidate=candidate.get("title")):
                self.assertEqual(candidate["status"], "needs-review")
                self.assertTrue(candidate["paper_url"].startswith("https://"))
                self.assertGreaterEqual(candidate["score"], 0)
                self.assertIn(candidate["suggested_section"], generate_readme.SECTION_ORDER)
                self.assertNotIn("figure", candidate)
                titles.append(discover_papers.normalize_title(candidate["title"]))
        self.assertEqual(len(titles), len(set(titles)))

    def test_deduplication(self):
        left = discover_papers.Candidate(
            title="Example: Multimodal Retrieval", paper_url="https://arxiv.org/abs/2601.01234",
            arxiv_id="2601.01234",
        )
        right = discover_papers.Candidate(
            title="Example Multimodal Retrieval", paper_url="https://example.org/paper",
            arxiv_id="2601.01234",
        )
        self.assertTrue(discover_papers.same_paper(left, right))

    def test_relevance_gate(self):
        relevant = discover_papers.Candidate(
            title="Agentic Multimodal Retrieval for Visual Documents",
            paper_url="https://example.org/relevant",
            abstract="A multimodal large language model plans iterative search and retrieval.",
        )
        irrelevant = discover_papers.Candidate(
            title="A Language Model for Poetry",
            paper_url="https://example.org/irrelevant",
            abstract="Text generation without external evidence.",
        )
        discover_papers.score(relevant)
        discover_papers.score(irrelevant)
        self.assertGreaterEqual(relevant.score, 7)
        self.assertLess(irrelevant.score, 7)


if __name__ == "__main__":
    unittest.main()
