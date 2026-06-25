from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.storage.models import BriefingItem, NewsItem
from src.tools.llm_client import LLMClient
from src.tools.text_utils import first_sentence


class SummarizerAgent(BaseAgent):
    name = "SummarizerAgent"

    def process(self, input_data: list[NewsItem], context: dict[str, Any]) -> list[BriefingItem]:
        max_items = int(context["config"].get("agents", {}).get("briefing", {}).get("max_items", 20))
        llm = LLMClient()
        briefing_items: list[BriefingItem] = []
        for item in (input_data or [])[:max_items]:
            summary = llm.summarize(item.title, item.clean_text) or first_sentence(item.clean_text, item.title)
            briefing_items.append(
                BriefingItem(
                    news_id=item.id,
                    headline=item.title,
                    one_sentence_summary=summary,
                    key_points=self._key_points(item),
                    why_it_matters=self._why_it_matters(item),
                    impact=self._impact(item),
                    sources=[item.url],
                    priority_reason=item.metadata.get("priority_reason", ""),
                    category=item.category,
                    priority=item.priority,
                    score=item.importance_score,
                )
            )
        context["llm_calls"] = context.get("llm_calls", 0) + llm.calls
        return briefing_items

    def _key_points(self, item: NewsItem) -> list[str]:
        points = [
            f"来源：{item.source}",
            f"分类：{item.category}",
            f"评分：{item.importance_score:.2f}",
        ]
        if item.tags:
            points.append("标签：" + "、".join(item.tags[:4]))
        return points[:4]

    def _why_it_matters(self, item: NewsItem) -> str:
        if item.category == "AI 与大模型":
            return "这可能影响 AI 产品能力、开发者工具链和后续模型应用节奏。"
        if item.category == "开发者工具与开源":
            return "这可能影响开发者选型、工程效率或开源生态关注方向。"
        if item.category == "网络安全":
            return "这可能带来安全修复、依赖升级或风险排查需求。"
        if item.category == "论文与研究":
            return "这为相关研究和产品实验提供了新的方法、基准或证据。"
        return "这条新闻可能影响相关公司、产品路线或技术趋势判断。"

    def _impact(self, item: NewsItem) -> str:
        if item.category == "AI 与大模型":
            return "AI 开发者、产品团队、研究人员"
        if item.category == "开发者工具与开源":
            return "软件工程师、开源维护者、技术团队"
        if item.category == "网络安全":
            return "安全团队、平台工程师、依赖维护者"
        if item.category == "论文与研究":
            return "研究人员、算法工程师、技术决策者"
        return "科技从业者、产品团队、行业观察者"
