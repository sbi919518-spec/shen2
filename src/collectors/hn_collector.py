from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from src.collectors.http import fetch_json
from src.storage.models import NewsItem, stable_id


class HNCollector:
    topstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    item_url = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"

    def collect(self, limit: int = 30) -> list[NewsItem]:
        story_ids = fetch_json(self.topstories_url)
        if not isinstance(story_ids, list):
            return []
        items: list[NewsItem] = []
        for item_id in story_ids[:limit]:
            row = fetch_json(self.item_url.format(item_id=item_id))
            if isinstance(row, dict):
                item = self._to_item(row)
                if item:
                    items.append(item)
        return items

    def _to_item(self, row: dict[str, Any]) -> NewsItem | None:
        title = row.get("title") or ""
        url = row.get("url") or f"https://news.ycombinator.com/item?id={row.get('id')}"
        if not title:
            return None
        published_at = ""
        if row.get("time"):
            published_at = datetime.fromtimestamp(int(row["time"]), tz=UTC).replace(microsecond=0).isoformat()
        return NewsItem(
            id=stable_id(url, title),
            title=title,
            url=url,
            source="Hacker News",
            published_at=published_at,
            author=row.get("by", ""),
            raw_text=row.get("text", "") or title,
            metadata={
                "hn_id": row.get("id"),
                "points": row.get("score", 0),
                "comments": row.get("descendants", 0),
            },
        )
