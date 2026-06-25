from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.storage.models import to_plain


class JsonStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    def write_json(self, relative_path: str, data: Any) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(to_plain(data), ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def write_jsonl(self, relative_path: str, rows: list[Any]) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        content = "\n".join(json.dumps(to_plain(row), ensure_ascii=False) for row in rows)
        path.write_text(content + ("\n" if content else ""), encoding="utf-8")
        return path
