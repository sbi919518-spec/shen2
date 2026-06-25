from __future__ import annotations

from datetime import UTC, datetime
from math import log10
from typing import Any

from src.utils.time_utils import parse_datetime


IMPACT_KEYWORDS = {
    "launch",
    "release",
    "breakthrough",
    "security",
    "vulnerability",
    "model",
    "agent",
    "open source",
    "api",
    "benchmark",
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def recency_score(published_at: str) -> float:
    parsed = parse_datetime(published_at)
    if parsed is None:
        return 0.55
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    age_hours = max(0.0, (datetime.now(UTC) - parsed).total_seconds() / 3600)
    if age_hours <= 24:
        return 1.0
    if age_hours <= 72:
        return 0.75
    if age_hours <= 168:
        return 0.45
    return 0.2


def discussion_heat(metadata: dict[str, Any]) -> float:
    points = float(metadata.get("points") or 0)
    comments = float(metadata.get("comments") or 0)
    stars = float(metadata.get("stars") or 0)
    raw = points + comments * 1.5 + stars / 50
    if raw <= 0:
        return 0.3
    return clamp(log10(raw + 1) / 3)


def priority_for_score(score: float, thresholds: dict[str, float]) -> str:
    if score >= thresholds.get("P0", 0.82):
        return "P0"
    if score >= thresholds.get("P1", 0.64):
        return "P1"
    if score >= thresholds.get("P2", 0.42):
        return "P2"
    return "P3"
