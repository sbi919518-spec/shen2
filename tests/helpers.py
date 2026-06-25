from __future__ import annotations


def test_config() -> dict:
    return {
        "sources": {},
        "categories": {
            "categories": [
                {
                    "name": "AI 与大模型",
                    "keywords": ["ai", "agent", "llm", "model", "openai"],
                },
                {
                    "name": "开发者工具与开源",
                    "keywords": ["github", "developer", "api", "open source"],
                },
                {
                    "name": "网络安全",
                    "keywords": ["security", "vulnerability", "patch"],
                },
                {
                    "name": "论文与研究",
                    "keywords": ["arxiv", "paper", "benchmark"],
                },
            ]
        },
        "ranking": {
            "weights": {
                "industry_impact": 0.25,
                "user_relevance": 0.20,
                "recency": 0.15,
                "source_credibility": 0.15,
                "novelty": 0.10,
                "actionability": 0.10,
                "discussion_heat": 0.05,
            },
            "trusted_sources": {
                "OpenAI News": 0.95,
                "GitHub": 0.80,
                "arXiv": 0.85,
                "Security Bulletin": 0.80,
            },
            "priority_thresholds": {"P0": 0.82, "P1": 0.64, "P2": 0.42},
        },
        "agents": {"briefing": {"max_items": 10, "top_items": 3, "output_dir": "data/briefings"}},
    }
