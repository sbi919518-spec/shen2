from __future__ import annotations

import urllib.parse
import xml.etree.ElementTree as ET

from src.collectors.http import fetch_text
from src.storage.models import NewsItem, stable_id
from src.tools.text_utils import strip_html


class ArxivCollector:
    endpoint = "https://export.arxiv.org/api/query"

    def collect(self, categories: list[str], limit: int = 20) -> list[NewsItem]:
        if not categories:
            categories = ["cs.AI", "cs.CL", "cs.LG"]
        query = " OR ".join(f"cat:{category}" for category in categories)
        url = f"{self.endpoint}?{urllib.parse.urlencode({'search_query': query, 'sortBy': 'submittedDate', 'sortOrder': 'descending', 'max_results': str(limit)})}"
        root = ET.fromstring(fetch_text(url))
        ns = "{http://www.w3.org/2005/Atom}"
        items: list[NewsItem] = []
        for entry in root.findall(f"{ns}entry"):
            title = strip_html(_child_text(entry, f"{ns}title"))
            link = _child_text(entry, f"{ns}id")
            if not title or not link:
                continue
            primary = entry.find("{http://arxiv.org/schemas/atom}primary_category")
            primary_category = primary.attrib.get("term", "") if primary is not None else ""
            items.append(
                NewsItem(
                    id=stable_id(link, title),
                    title=title,
                    url=link,
                    source="arXiv",
                    published_at=_child_text(entry, f"{ns}published"),
                    raw_text=strip_html(_child_text(entry, f"{ns}summary")),
                    metadata={"primary_category": primary_category},
                )
            )
        return items


def _child_text(node: ET.Element, name: str) -> str:
    child = node.find(name)
    return (child.text or "").strip() if child is not None else ""
