from __future__ import annotations

from collections import defaultdict
from typing import Any

from src.agents.base_agent import BaseAgent
from src.storage.models import BriefingItem
from src.utils.time_utils import today_string


CATEGORY_ORDER = ["AI 与大模型", "开发者工具与开源", "论文与研究", "公司与产品", "网络安全", "芯片与硬件", "政策监管", "值得深读"]


class EditorAgent(BaseAgent):
    name = "EditorAgent"

    def process(self, input_data: list[BriefingItem], context: dict[str, Any]) -> dict[str, Any]:
        briefing_date = context.get("briefing_date") or today_string()
        top_count = int(context["config"].get("agents", {}).get("briefing", {}).get("top_items", 5))
        items = input_data or []
        top_items = items[:top_count]
        grouped: dict[str, list[BriefingItem]] = defaultdict(list)
        for item in items:
            grouped[item.category].append(item)

        lines = [f"# 智者科技日报 - {briefing_date}", "", f"运行编号：`{context['run_id']}`", ""]
        lines.extend(self._section("今日最重要", top_items))
        for category in CATEGORY_ORDER:
            category_items = [item for item in grouped.get(category, []) if item not in top_items]
            if category_items:
                lines.extend(self._section(category, category_items))
        markdown = "\n".join(lines).rstrip() + "\n"
        return {"date": briefing_date, "markdown": markdown, "items": items}

    def _section(self, title: str, items: list[BriefingItem]) -> list[str]:
        lines = [f"## {title}", ""]
        if not items:
            lines.extend(["暂无内容。", ""])
            return lines
        for index, item in enumerate(items, start=1):
            lines.extend(
                [
                    f"### {index}. {item.headline}",
                    f"- 优先级：{item.priority}",
                    f"- 分类：{item.category}",
                    f"- 分数：{item.score:.2f}",
                    f"- 一句话摘要：{item.one_sentence_summary}",
                    "- 关键点：",
                ]
            )
            lines.extend(f"  - {point}" for point in item.key_points)
            lines.extend(
                [
                    f"- 为什么重要：{item.why_it_matters}",
                    f"- 影响对象：{item.impact}",
                    f"- 排序理由：{item.priority_reason}",
                    f"- 来源：{'; '.join(item.sources)}",
                ]
            )
            if item.editor_notes:
                lines.append(f"- 编辑提示：{item.editor_notes}")
            lines.append("")
        return lines
