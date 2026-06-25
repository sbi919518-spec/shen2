from __future__ import annotations

from datetime import UTC, datetime

from src.storage.models import NewsItem, stable_id


def sample_news_items() -> list[NewsItem]:
    now = datetime.now(UTC).replace(microsecond=0).isoformat()
    rows = [
        {
            "title": "OpenAI releases new agent tools for developers",
            "url": "https://openai.com/news/sample-agent-tools",
            "source": "OpenAI News",
            "raw_text": "OpenAI released new agent tools that help developers build reliable automation with tool calling and tracing.",
            "metadata": {"points": 180, "comments": 42},
        },
        {
            "title": "Popular GitHub project adds fast local LLM inference",
            "url": "https://github.com/example/local-llm",
            "source": "GitHub",
            "raw_text": "A fast local inference project gained attention from developers and added a new API for model serving.",
            "metadata": {"stars": 4200, "comments": 18},
        },
        {
            "title": "New arXiv paper benchmarks agent planning reliability",
            "url": "https://arxiv.org/abs/2606.00001",
            "source": "arXiv",
            "raw_text": "Researchers published a benchmark for evaluating planning reliability in autonomous AI agents.",
            "metadata": {"primary_category": "cs.AI"},
        },
        {
            "title": "Major security patch fixes dependency confusion vulnerability",
            "url": "https://example.com/security/dependency-confusion",
            "source": "Security Bulletin",
            "raw_text": "A widely used package released a security patch for a dependency confusion vulnerability affecting CI systems.",
            "metadata": {"points": 95, "comments": 21},
        },
        {
            "title": "NVIDIA announces updated GPU software stack for AI workloads",
            "url": "https://blogs.nvidia.com/sample-ai-gpu-stack",
            "source": "NVIDIA Blog",
            "raw_text": "NVIDIA announced updates to its GPU software stack for training and inference workloads.",
            "metadata": {"points": 120, "comments": 17},
        },
    ]
    return [
        NewsItem(
            id=stable_id(row["url"], row["title"]),
            title=row["title"],
            url=row["url"],
            source=row["source"],
            published_at=now,
            raw_text=row["raw_text"],
            metadata=row.get("metadata", {}),
        )
        for row in rows
    ]
