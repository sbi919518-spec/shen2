from __future__ import annotations

import urllib.parse
from datetime import UTC, datetime, timedelta

from src.collectors.http import fetch_json
from src.storage.models import NewsItem, stable_id


class GitHubCollector:
    endpoint = "https://api.github.com/search/repositories"

    def collect(self, queries: list[str], limit: int = 10) -> list[NewsItem]:
        items: list[NewsItem] = []
        since = (datetime.now(UTC) - timedelta(days=14)).date().isoformat()
        for query in queries or ["topic:ai"]:
            params = {
                "q": f"{query} pushed:>{since}",
                "sort": "stars",
                "order": "desc",
                "per_page": str(limit),
            }
            url = f"{self.endpoint}?{urllib.parse.urlencode(params)}"
            data = fetch_json(url)
            if not isinstance(data, dict):
                continue
            for repo in data.get("items", [])[:limit]:
                title = repo.get("full_name") or repo.get("name")
                html_url = repo.get("html_url", "")
                if not title or not html_url:
                    continue
                description = repo.get("description") or title
                items.append(
                    NewsItem(
                        id=stable_id(html_url, title),
                        title=title,
                        url=html_url,
                        source="GitHub",
                        published_at=repo.get("pushed_at", ""),
                        raw_text=description,
                        metadata={
                            "stars": repo.get("stargazers_count", 0),
                            "forks": repo.get("forks_count", 0),
                            "language": repo.get("language", ""),
                        },
                    )
                )
        return items
