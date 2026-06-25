from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.agents.cleaner_agent import CleanerAgent
from src.storage.models import NewsItem


class CleanerTests(unittest.TestCase):
    def test_cleaner_normalizes_tracking_urls_and_removes_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            items = [
                NewsItem(id="1", title="  AI Tool Launch  ", url="https://example.com/a?utm_source=x", source="Test"),
                NewsItem(id="2", title="AI Tool Launch", url="https://example.com/a", source="Test"),
            ]
            result = CleanerAgent().process(items, {"root": str(Path(tmp)), "run_id": "test"})
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].url, "https://example.com/a")
            self.assertEqual(result[0].title, "AI Tool Launch")


if __name__ == "__main__":
    unittest.main()
