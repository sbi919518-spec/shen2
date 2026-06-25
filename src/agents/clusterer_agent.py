from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.storage.models import NewsItem, stable_id
from src.tools.text_utils import title_tokens


class ClustererAgent(BaseAgent):
    name = "ClustererAgent"

    def process(self, input_data: list[NewsItem], context: dict[str, Any]) -> list[NewsItem]:
        representatives: list[NewsItem] = []
        representative_tokens: list[set[str]] = []
        for item in input_data or []:
            tokens = title_tokens(item.title)
            matched_index = self._match_cluster(tokens, representative_tokens)
            if matched_index is None:
                item.cluster_id = stable_id("cluster", item.title)
                item.metadata.setdefault("cluster_size", 1)
                item.metadata.setdefault("related_urls", [item.url])
                representatives.append(item)
                representative_tokens.append(tokens)
            else:
                representative = representatives[matched_index]
                representative.metadata["cluster_size"] = int(representative.metadata.get("cluster_size", 1)) + 1
                related_urls = representative.metadata.setdefault("related_urls", [representative.url])
                if item.url not in related_urls:
                    related_urls.append(item.url)
                if len(item.clean_text) > len(representative.clean_text):
                    representative.clean_text = item.clean_text
        return representatives

    def _match_cluster(self, tokens: set[str], groups: list[set[str]]) -> int | None:
        if not tokens:
            return None
        for index, existing in enumerate(groups):
            union = tokens | existing
            if not union:
                continue
            similarity = len(tokens & existing) / len(union)
            if similarity >= 0.72:
                return index
        return None
