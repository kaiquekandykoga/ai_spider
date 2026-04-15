# AI Spider

The main project is in `legacy/`. All commands run from that directory.

## Quick Start
```bash
cd legacy
uv sync
uv run python -m ai_spider
```

## Commands (run from `legacy/`)
- `uv sync` — install deps
- `uv run pytest` — run tests
- `uv run ruff check .` — lint
- `uv run mypy .` — typecheck
- `uv run playwright install chromium` — install browser (once)

## CI Order
lint → typecheck → test

## Structure
- `legacy/` — Python 3.14+ project (LangChain, Playwright, BeautifulSoup4, Ollama)
- `legacy/src/ai_spider/` — source code
- `legacy/data/` — config files (profile.yaml, sites.yaml)
- `legacy/tests/` — tests

## More Detail
See `legacy/AGENTS.md` for complete project-specific guidance.