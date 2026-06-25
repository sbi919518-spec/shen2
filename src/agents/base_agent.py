from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.storage.models import AgentRunLog
from src.utils.time_utils import utc_now_iso


@dataclass
class AgentResult:
    data: Any
    log: AgentRunLog


class BaseAgent(ABC):
    name = "BaseAgent"

    def run(self, input_data: Any, context: dict[str, Any]) -> AgentResult:
        started_at = utc_now_iso()
        log = AgentRunLog(
            run_id=context["run_id"],
            agent_name=self.name,
            started_at=started_at,
            input_count=self._count(input_data),
        )
        try:
            output = self.process(input_data, context)
            log.status = "success"
            log.output_count = self._count(output)
        except Exception as exc:  # pragma: no cover - tested at orchestrator level
            output = input_data
            log.status = "error"
            log.error_message = f"{type(exc).__name__}: {exc}"
        log.ended_at = utc_now_iso()
        return AgentResult(data=output, log=log)

    @abstractmethod
    def process(self, input_data: Any, context: dict[str, Any]) -> Any:
        raise NotImplementedError

    def _count(self, value: Any) -> int:
        if value is None:
            return 0
        if isinstance(value, list | tuple | set | dict):
            return len(value)
        return 1
