from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise RuntimeError(f"Config {path} is not JSON and PyYAML is not installed") from exc
        loaded = yaml.safe_load(text) or {}
        if not isinstance(loaded, dict):
            raise ValueError(f"Config {path} must contain a mapping")
        return loaded


def load_project_config(root: Path) -> dict[str, Any]:
    config_root = root / "config"
    return {
        "sources": load_config_file(config_root / "sources.yaml"),
        "categories": load_config_file(config_root / "categories.yaml"),
        "ranking": load_config_file(config_root / "ranking_weights.yaml"),
        "agents": load_config_file(config_root / "agent_config.yaml"),
    }
