from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.storage.models import NewsItem
from src.tools.text_utils import extract_entities, keyword_hits


class ClassifierAgent(BaseAgent):
    name = "ClassifierAgent"

    def process(self, input_data: list[NewsItem], context: dict[str, Any]) -> list[NewsItem]:
        categories = context["config"].get("categories", {}).get("categories", [])
        for item in input_data or []:
            text = f"{item.title} {item.clean_text} {item.source}"
            best_category = "公司与产品"
            best_hits: list[str] = []
            for category in categories:
                hits = keyword_hits(text, category.get("keywords", []))
                if len(hits) > len(best_hits):
                    best_category = category.get("name", best_category)
                    best_hits = hits
            item.category = best_category
            item.tags = sorted(set(best_hits))[:8]
            item.entities = extract_entities(text)
        return input_data
