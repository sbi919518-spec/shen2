from __future__ import annotations

import os


class LLMClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.enabled = bool(self.api_key)
        self.calls = 0

    def summarize(self, title: str, text: str) -> str | None:
        if not self.enabled:
            return None
        try:
            from openai import OpenAI  # type: ignore
        except ImportError:
            return None
        client = OpenAI(api_key=self.api_key)
        prompt = (
            "用一句中文概括这条科技新闻。只基于给定内容，不要编造来源中没有的信息。\n\n"
            f"标题：{title}\n内容：{text[:2500]}"
        )
        response = client.responses.create(
            model=self.model,
            input=prompt,
            max_output_tokens=120,
        )
        self.calls += 1
        output = getattr(response, "output_text", "") or ""
        return output.strip() or None
