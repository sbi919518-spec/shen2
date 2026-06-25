from __future__ import annotations

import unittest

from src.collectors.sample_data import sample_news_items


class CollectorTests(unittest.TestCase):
    def test_sample_news_items_have_required_fields(self) -> None:
        items = sample_news_items()
        self.assertGreaterEqual(len(items), 5)
        for item in items:
            self.assertTrue(item.title)
            self.assertTrue(item.url)
            self.assertTrue(item.source)


if __name__ == "__main__":
    unittest.main()
