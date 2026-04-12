# AGENTS.md
Python/LangChain app to find web resources.

## Stack
Python 3.14+, LangChain (langchain-core, langchain-ollama), BeautifulSoup4, Playwright, PyYAML, uv, Ollama (llama3.2:3b)

## Commands
- `uv run main.py` — run app
- `uv sync` — install deps
- `uv run playwright install chromium` — install browser (once)

## Structure
- `main.py` — entry point (_load_profile, _load_sources, main)
- `crawler.py` — web crawler (crawl_source, _fetch_page, _discover_job_links, _extract_text)
- `matcher.py` — job matching via Ollama/LangChain
- `data/profile.yaml` — candidate profile
- `data/sites.yaml` — job sources
- `pyproject.toml` — deps/config

## Rules
- No secrets/API keys in repo
- Test locally before committing
- Follow patterns in main.py; use type hints

## Privacy Conventions
- `_name` — internal helper (preferred)
- `__name` — name-mangled private (subclass collision only)
- `__magic__` — reserved, never create new ones

## When Stuck
Check main.py or ask user.
