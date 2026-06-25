from __future__ import annotations

from dataclasses import MISSING, asdict, dataclass, field, is_dataclass
from hashlib import sha1
from typing import Any


def stable_id(*parts: str) -> str:
    normalized = "|".join(part.strip().lower() for part in parts if part)
    return sha1(normalized.encode("utf-8")).hexdigest()[:16]


@dataclass
class NewsItem:
    id: str
    title: str
    url: str
    source: str
    published_at: str = ""
    author: str = ""
    raw_text: str = ""
    clean_text: str = ""
    language: str = "unknown"
    entities: list[str] = field(default_factory=list)
    category: str = "未分类"
    tags: list[str] = field(default_factory=list)
    cluster_id: str = ""
    credibility_score: float = 0.5
    importance_score: float = 0.0
    priority: str = "P3"
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "NewsItem":
        return cls(**{field_name: value.get(field_name, default) for field_name, default in _defaults(cls).items()})


@dataclass
class BriefingItem:
    news_id: str
    headline: str
    one_sentence_summary: str
    key_points: list[str]
    why_it_matters: str
    impact: str
    sources: list[str]
    priority_reason: str
    editor_notes: str = ""
    category: str = "未分类"
    priority: str = "P3"
    score: float = 0.0


@dataclass
class AgentRunLog:
    run_id: str
    agent_name: str
    started_at: str
    ended_at: str = ""
    input_count: int = 0
    output_count: int = 0
    status: str = "running"
    error_message: str = ""
    llm_calls: int = 0
    notes: str = ""


def to_plain(value: Any) -> Any:
    if is_dataclass(value):
        return {key: to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, tuple):
        return [to_plain(item) for item in value]
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    return value


def _defaults(cls: type[Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for dataclass_field in cls.__dataclass_fields__.values():  # type: ignore[attr-defined]
        if dataclass_field.default is not MISSING:
            result[dataclass_field.name] = dataclass_field.default
        elif dataclass_field.default_factory is not MISSING:  # type: ignore[comparison-overlap]
            result[dataclass_field.name] = dataclass_field.default_factory()  # type: ignore[misc]
        else:
            result[dataclass_field.name] = None
    return result
