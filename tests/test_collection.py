import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import discover_papers  # noqa: E402
import generate_readme  # noqa: E402


class CollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.papers = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))

    def test_seed_collection_size(self):
        self.assertGreaterEqual(len(self.papers), 35)

    def test_ids_and_titles_are_unique(self):
        ids = [paper["id"] for paper in self.papers]
        titles = [discover_papers.normalize_title(paper["title"]) for paper in self.papers]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(titles), len(set(titles)))

    def test_metadata_and_frameworks(self):
        for paper in self.papers:
            with self.subTest(paper=paper["id"]):
                self.assertIn(paper["section"], generate_readme.SECTION_ORDER)
                self.assertTrue(paper["paper_url"].startswith("https://"))
                self.assertGreaterEqual(paper["year"], 2022)
                self.assertLessEqual(paper["year"], 2100)
                self.assertTrue(3 <= len(paper["framework"]) <= 5)
                self.assertTrue(all(step.strip() for step in paper["framework"]))

    def test_generated_files_are_current(self):
        readme, assets = generate_readme.build()
        self.assertEqual(readme, (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(len(assets), len(self.papers))
        for path, expected in assets.items():
            self.assertTrue(path.exists())
            self.assertEqual(expected, path.read_text(encoding="utf-8"))

    def test_candidate_queue_schema(self):
        candidates = json.loads((ROOT / "data" / "candidates.json").read_text(encoding="utf-8"))
        titles = []
        for candidate in candidates:
            with self.subTest(candidate=candidate.get("title")):
                self.assertEqual(candidate["status"], "needs-review")
                self.assertTrue(candidate["paper_url"].startswith("https://"))
                self.assertGreaterEqual(candidate["score"], 0)
                self.assertIn(candidate["suggested_section"], generate_readme.SECTION_ORDER)
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
