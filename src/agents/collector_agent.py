from __future__ import annotations

from pathlib import Path
from typing import Any

from src.agents.base_agent import BaseAgent
from src.collectors import ArxivCollector, GitHubCollector, HNCollector, RSSCollector, sample_news_items
from src.storage.database import JsonStore
from src.storage.models import NewsItem


class CollectorAgent(BaseAgent):
    name = "CollectorAgent"

    def process(self, input_data: Any, context: dict[str, Any]) -> list[NewsItem]:
        if context.get("offline_sample"):
            items = sample_news_items()
            self._save_raw(context, items)
            return items

        sources = context["config"].get("sources", {})
        items: list[NewsItem] = []

        hn_config = sources.get("hn", {})
        if hn_config.get("enabled", True):
            try:
                items.extend(HNCollector().collect(limit=int(hn_config.get("limit", 30))))
            except Exception as exc:
                context.setdefault("collector_warnings", []).append(f"HNCollector: {exc}")

        rss_config = sources.get("rss", {})
        if rss_config.get("enabled", True):
            try:
                items.extend(
                    RSSCollector().collect(
                        feeds=rss_config.get("feeds", []),
                        limit_per_feed=int(rss_config.get("limit_per_feed", 8)),
                    )
                )
            except Exception as exc:
                context.setdefault("collector_warnings", []).append(f"RSSCollector: {exc}")

        arxiv_config = sources.get("arxiv", {})
        if arxiv_config.get("enabled", True):
            try:
                items.extend(
                    ArxivCollector().collect(
                        categories=arxiv_config.get("categories", []),
                        limit=int(arxiv_config.get("limit", 20)),
                    )
                )
            except Exception as exc:
                context.setdefault("collector_warnings", []).append(f"ArxivCollector: {exc}")

        github_config = sources.get("github", {})
        if github_config.get("enabled", True):
            try:
                items.extend(
                    GitHubCollector().collect(
                        queries=github_config.get("queries", []),
                        limit=int(github_config.get("limit", 10)),
                    )
                )
            except Exception as exc:
                context.setdefault("collector_warnings", []).append(f"GitHubCollector: {exc}")

        if not items and context.get("allow_sample_fallback", True):
            items = sample_news_items()
            context.setdefault("collector_warnings", []).append("No online items collected; used sample fallback.")

        self._save_raw(context, items)
        return items

    def _save_raw(self, context: dict[str, Any], items: list[NewsItem]) -> None:
        root = Path(context["root"])
        JsonStore(root).write_json(f"data/raw/{context['run_id']}.json", items)
