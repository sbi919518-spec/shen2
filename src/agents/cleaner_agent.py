from __future__ import annotations

from pathlib import Path
from typing import Any

from src.agents.base_agent import BaseAgent
from src.storage.database import JsonStore
from src.storage.models import NewsItem, stable_id
from src.tools.text_utils import normalize_whitespace, strip_html
from src.tools.url_utils import canonicalize_url


class CleanerAgent(BaseAgent):
    name = "CleanerAgent"

    def process(self, input_data: list[NewsItem], context: dict[str, Any]) -> list[NewsItem]:
        cleaned: list[NewsItem] = []
        seen: set[str] = set()
        for item in input_data or []:
            title = normalize_whitespace(strip_html(item.title))
            url = canonicalize_url(item.url)
            if not title or not url:
                continue
            dedupe_key = url or title.lower()
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            item.title = title
            item.url = url
            item.clean_text = normalize_whitespace(strip_html(item.raw_text or item.title))
            item.id = stable_id(item.url, item.title)
            item.metadata["canonical_url"] = url
            cleaned.append(item)

        JsonStore(Path(context["root"])).write_json(f"data/processed/{context['run_id']}_cleaned.json", cleaned)
        return cleaned
