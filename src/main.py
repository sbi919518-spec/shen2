from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from src.agents import (
    ClassifierAgent,
    CleanerAgent,
    ClustererAgent,
    CollectorAgent,
    EditorAgent,
    PublisherAgent,
    RankerAgent,
    SummarizerAgent,
    VerifierAgent,
)
from src.orchestrator import Orchestrator
from src.tools.config_loader import load_project_config
from src.utils.logger import setup_logger


def build_orchestrator(root: Path) -> Orchestrator:
    agents = [
        CollectorAgent(),
        CleanerAgent(),
        ClustererAgent(),
        ClassifierAgent(),
        RankerAgent(),
        SummarizerAgent(),
        VerifierAgent(),
        EditorAgent(),
        PublisherAgent(),
    ]
    return Orchestrator(agents=agents, root=root)


def run_pipeline(
    root: Path,
    *,
    offline_sample: bool = False,
    max_items: int | None = None,
    briefing_date: str | None = None,
) -> dict[str, Any]:
    config = load_project_config(root)
    if max_items is not None:
        config.setdefault("agents", {}).setdefault("briefing", {})["max_items"] = max_items
    context = {
        "config": config,
        "offline_sample": offline_sample,
        "briefing_date": briefing_date,
        "allow_sample_fallback": True,
    }
    return build_orchestrator(root).run(context=context)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Zhizhe daily tech briefing pipeline.")
    parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--date", dest="briefing_date", default=None, help="Briefing date in YYYY-MM-DD format.")
    parser.add_argument("--max-items", type=int, default=int(os.getenv("ZHIZHE_MAX_ITEMS", "20")))
    parser.add_argument("--offline-sample", action="store_true", help="Use deterministic sample news instead of network collectors.")
    return parser.parse_args()


def main() -> None:
    setup_logger()
    args = parse_args()
    root = Path(args.root).resolve()
    result = run_pipeline(
        root,
        offline_sample=args.offline_sample,
        max_items=args.max_items,
        briefing_date=args.briefing_date,
    )
    output = result["output"]
    print(f"run_id={result['run_id']}")
    print(f"briefing_path={output['briefing_path']}")
    print(f"items_count={output['items_count']}")


if __name__ == "__main__":
    main()
