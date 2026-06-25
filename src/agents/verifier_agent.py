from __future__ import annotations

from typing import Any

from src.agents.base_agent import BaseAgent
from src.storage.models import BriefingItem


class VerifierAgent(BaseAgent):
    name = "VerifierAgent"

    def process(self, input_data: list[BriefingItem], context: dict[str, Any]) -> list[BriefingItem]:
        for item in input_data or []:
            notes: list[str] = []
            if not item.sources:
                notes.append("缺少来源链接，建议人工复核。")
            elif item.priority in {"P0", "P1"} and len(item.sources) == 1:
                notes.append("当前为单一来源，重要结论需谨慎表述。")
            if "可能" not in item.why_it_matters and item.priority in {"P0", "P1"}:
                notes.append("影响分析应保留不确定性。")
            item.editor_notes = " ".join(notes)
        return input_data
