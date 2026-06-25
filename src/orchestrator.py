from __future__ import annotations

from pathlib import Path
from typing import Any

from src.agents.base_agent import BaseAgent
from src.storage.database import JsonStore
from src.storage.models import AgentRunLog, to_plain
from src.utils.time_utils import utc_now_iso


class Orchestrator:
    def __init__(self, agents: list[BaseAgent], root: Path) -> None:
        self.agents = agents
        self.root = root
        self.store = JsonStore(root)

    def run(self, initial_data: Any = None, context: dict[str, Any] | None = None) -> dict[str, Any]:
        runtime_context = dict(context or {})
        run_id = runtime_context.get("run_id") or utc_now_iso().replace(":", "").replace("+", "Z")
        runtime_context["run_id"] = run_id
        runtime_context["root"] = str(self.root)
        runtime_context.setdefault("continue_on_agent_error", False)

        current = initial_data
        logs: list[AgentRunLog] = []
        for agent in self.agents:
            result = agent.run(current, runtime_context)
            current = result.data
            logs.append(result.log)
            self.store.write_json(
                f"data/runs/{run_id}/{agent.name}.json",
                {"log": result.log, "data": to_plain(result.data)},
            )
            if result.log.status == "error" and not runtime_context["continue_on_agent_error"]:
                self.store.write_json(f"data/runs/{run_id}/run_log.json", logs)
                raise RuntimeError(result.log.error_message)

        self.store.write_json(f"data/runs/{run_id}/run_log.json", logs)
        return {"run_id": run_id, "output": current, "logs": logs}
