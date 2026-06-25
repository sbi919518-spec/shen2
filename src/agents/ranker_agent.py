from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.storage.models import NewsItem
from src.tools.scoring_utils import IMPACT_KEYWORDS, clamp, discussion_heat, priority_for_score, recency_score
from src.tools.text_utils import keyword_hits


class RankerAgent(BaseAgent):
    name = "RankerAgent"

    def process(self, input_data: list[NewsItem], context: dict[str, Any]) -> list[NewsItem]:
        ranking_config = context["config"].get("ranking", {})
        weights = ranking_config.get("weights", {})
        thresholds = ranking_config.get("priority_thresholds", {})
        trusted_sources = ranking_config.get("trusted_sources", {})
        for item in input_data or []:
            features = self._features(item, trusted_sources)
            score = sum(float(weights.get(name, 0.0)) * value for name, value in features.items())
            item.importance_score = round(clamp(score), 4)
            item.credibility_score = features["source_credibility"]
            item.priority = priority_for_score(item.importance_score, thresholds)
            item.metadata["score_features"] = features
            item.metadata["priority_reason"] = self._reason(item, features)
        return sorted(input_data or [], key=lambda item: item.importance_score, reverse=True)

    def _features(self, item: NewsItem, trusted_sources: dict[str, float]) -> dict[str, float]:
        text = f"{item.title} {item.clean_text}".lower()
        impact_hits = keyword_hits(text, sorted(IMPACT_KEYWORDS))
        category_bonus = {
            "AI 与大模型": 0.85,
            "网络安全": 0.85,
            "开发者工具与开源": 0.75,
            "论文与研究": 0.70,
            "芯片与硬件": 0.70,
        }.get(item.category, 0.60)
        source_score = float(trusted_sources.get(item.source, 0.62))
        heat = discussion_heat(item.metadata)
        return {
            "industry_impact": clamp(category_bonus + min(len(impact_hits), 3) * 0.05),
            "user_relevance": clamp(0.65 + (0.15 if item.category in {"AI 与大模型", "开发者工具与开源"} else 0.0)),
            "recency": recency_score(item.published_at),
            "source_credibility": clamp(source_score),
            "novelty": clamp(0.60 + min(int(item.metadata.get("cluster_size", 1)), 3) * 0.08),
            "actionability": clamp(0.50 + (0.25 if any(word in text for word in ["api", "tool", "release", "patch", "framework"]) else 0.0)),
            "discussion_heat": heat,
        }

    def _reason(self, item: NewsItem, features: dict[str, float]) -> str:
        strongest = sorted(features.items(), key=lambda pair: pair[1], reverse=True)[:2]
        labels = {
            "industry_impact": "行业影响",
            "user_relevance": "相关性",
            "recency": "时效性",
            "source_credibility": "来源可信度",
            "novelty": "新颖性",
            "actionability": "可行动性",
            "discussion_heat": "讨论热度",
        }
        reason = "、".join(labels.get(name, name) for name, _ in strongest)
        return f"{reason}较高，归入{item.priority}。"
