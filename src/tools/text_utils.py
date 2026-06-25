from __future__ import annotations

import html
import re
from collections import Counter


TAG_RE = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9.+#-]{1,}")


def strip_html(value: str) -> str:
    without_tags = TAG_RE.sub(" ", value or "")
    return normalize_whitespace(html.unescape(without_tags))


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def title_tokens(title: str) -> set[str]:
    return {token.lower() for token in WORD_RE.findall(title or "") if len(token) > 2}


def first_sentence(value: str, fallback: str = "") -> str:
    text = normalize_whitespace(value)
    if not text:
        return fallback
    match = re.split(r"(?<=[.!?。！？])\s+", text, maxsplit=1)
    return match[0][:260].strip() if match else text[:260].strip()


def extract_entities(text: str, limit: int = 8) -> list[str]:
    candidates = re.findall(r"\b(?:[A-Z][A-Za-z0-9.+-]{1,}|[A-Z]{2,})\b", text or "")
    counts = Counter(candidates)
    ignored = {"The", "This", "That", "With", "From", "Into", "For", "And"}
    return [word for word, _ in counts.most_common(limit) if word not in ignored]


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    lowered = (text or "").lower()
    return [keyword for keyword in keywords if keyword.lower() in lowered]
