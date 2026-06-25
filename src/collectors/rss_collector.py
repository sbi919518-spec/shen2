from __future__ import annotations

import xml.etree.ElementTree as ET

from src.collectors.http import fetch_text
from src.storage.models import NewsItem, stable_id
from src.tools.text_utils import strip_html


class RSSCollector:
    def collect(self, feeds: list[dict], limit_per_feed: int = 8) -> list[NewsItem]:
        items: list[NewsItem] = []
        for feed in feeds:
            name = feed.get("name", "RSS")
            url = feed.get("url", "")
            if not url:
                continue
            try:
                items.extend(self._collect_feed(name, url, limit_per_feed))
            except Exception:
                continue
        return items

    def _collect_feed(self, source_name: str, url: str, limit: int) -> list[NewsItem]:
        root = ET.fromstring(fetch_text(url))
        rss_items = root.findall(".//item")
        if rss_items:
            return [item for item in (self._from_rss_node(source_name, node) for node in rss_items[:limit]) if item]
        atom_entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")
        return [item for item in (self._from_atom_node(source_name, node) for node in atom_entries[:limit]) if item]

    def _from_rss_node(self, source_name: str, node: ET.Element) -> NewsItem | None:
        title = _child_text(node, "title")
        link = _child_text(node, "link")
        if not title or not link:
            return None
        description = _child_text(node, "description")
        return NewsItem(
            id=stable_id(link, title),
            title=strip_html(title),
            url=link.strip(),
            source=source_name,
            published_at=_child_text(node, "pubDate"),
            author=_child_text(node, "author"),
            raw_text=strip_html(description or title),
        )

    def _from_atom_node(self, source_name: str, node: ET.Element) -> NewsItem | None:
        ns = "{http://www.w3.org/2005/Atom}"
        title = _child_text(node, f"{ns}title")
        link_node = node.find(f"{ns}link")
        link = link_node.attrib.get("href", "") if link_node is not None else ""
        if not title or not link:
            return None
        summary = _child_text(node, f"{ns}summary") or _child_text(node, f"{ns}content")
        return NewsItem(
            id=stable_id(link, title),
            title=strip_html(title),
            url=link.strip(),
            source=source_name,
            published_at=_child_text(node, f"{ns}updated") or _child_text(node, f"{ns}published"),
            raw_text=strip_html(summary or title),
        )


def _child_text(node: ET.Element, name: str) -> str:
    child = node.find(name)
    return (child.text or "").strip() if child is not None else ""
