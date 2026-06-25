# Zhizhe Tech News Agent

Zhizhe is a lightweight multi-agent MVP for collecting daily technology news, ranking the important items, and publishing a Markdown briefing.

## What ships in week one

- A sequential multi-agent pipeline:
  `Collector -> Cleaner -> Clusterer -> Classifier -> Ranker -> Summarizer -> Verifier -> Editor -> Publisher`
- Basic collectors for Hacker News, RSS, arXiv, and GitHub repository search.
- Offline sample mode for deterministic tests and local smoke runs.
- Structured models for `NewsItem`, `BriefingItem`, and `AgentRunLog`.
- Markdown briefing output under `data/briefings/`.
- Run logs under `data/runs/`.
- GitHub Actions workflow for daily scheduled runs.

## Quick Start

```bash
python -m src.main --offline-sample
```

The generated briefing path is printed at the end of the run.

## Run Tests

```bash
python -m unittest discover -s tests
```

## Online Run

```bash
python -m src.main --max-items 20
```

Optional environment variables:

- `OPENAI_API_KEY`: enable LLM summaries when the `openai` package is installed.
- `OPENAI_MODEL`: model name for summary generation. Defaults to `gpt-4.1-mini`.

If no LLM is configured, Zhizhe uses an extractive fallback summary so the pipeline remains runnable.
