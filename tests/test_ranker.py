from __future__ import annotations

import unittest

from src.agents.classifier_agent import ClassifierAgent
from src.agents.ranker_agent import RankerAgent
from src.collectors.sample_data import sample_news_items
from tests.helpers import test_config


class RankerTests(unittest.TestCase):
    def test_ranker_assigns_scores_and_priorities(self) -> None:
        context = {"config": test_config(), "run_id": "test"}
        classified = ClassifierAgent().process(sample_news_items(), context)
        ranked = RankerAgent().process(classified, context)
        self.assertGreater(ranked[0].importance_score, 0)
        self.assertIn(ranked[0].priority, {"P0", "P1", "P2", "P3"})
        self.assertGreaterEqual(ranked[0].importance_score, ranked[-1].importance_score)


if __name__ == "__main__":
    unittest.main()
