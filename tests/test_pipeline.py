from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.agents import (
    ClassifierAgent,
    CleanerAgent,
    ClustererAgent,
    CollectorAgent,
    EditorAgent,
    PublisherAgent,
    RankerAgent,
    SummarizerAgent,
    VerifierAgent,
)
from src.orchestrator import Orchestrator
from tests.helpers import test_config


class PipelineTests(unittest.TestCase):
    def test_offline_pipeline_generates_markdown_briefing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            agents = [
                CollectorAgent(),
                CleanerAgent(),
                ClustererAgent(),
                ClassifierAgent(),
                RankerAgent(),
                SummarizerAgent(),
                VerifierAgent(),
                EditorAgent(),
                PublisherAgent(),
            ]
            result = Orchestrator(agents, root).run(
                context={
                    "config": test_config(),
                    "offline_sample": True,
                    "briefing_date": "2026-06-25",
                }
            )
            output = result["output"]
            path = Path(output["briefing_path"])
            self.assertTrue(path.exists())
            content = path.read_text(encoding="utf-8")
            self.assertIn("# 智者科技日报 - 2026-06-25", content)
            self.assertIn("今日最重要", content)
            self.assertGreater(output["items_count"], 0)


if __name__ == "__main__":
    unittest.main()
