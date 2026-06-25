from __future__ import annotations

from pathlib import Path
from typing import Any

from src.agents.base_agent import BaseAgent


class PublisherAgent(BaseAgent):
    name = "PublisherAgent"

    def process(self, input_data: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        root = Path(context["root"])
        output_dir = context["config"].get("agents", {}).get("briefing", {}).get("output_dir", "data/briefings")
        date = input_data["date"]
        path = root / output_dir / f"zhizhe-tech-briefing-{date}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(input_data["markdown"], encoding="utf-8")
        return {
            "briefing_path": str(path),
            "items_count": len(input_data.get("items", [])),
            "markdown": input_data["markdown"],
        }
