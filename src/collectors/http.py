from __future__ import annotations

import json
from urllib.request import Request, urlopen


USER_AGENT = "zhizhe-tech-news-agent/0.1"


def fetch_text(url: str, timeout: int = 12) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - configured user sources
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def fetch_json(url: str, timeout: int = 12) -> dict | list:
    return json.loads(fetch_text(url, timeout=timeout))
