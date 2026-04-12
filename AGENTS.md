# AGENTS.md

App used to find resources on the web using Python and LangChain.

## Agent Role
You are a coding assistant helping maintain and extend this web scraping project. Focus on practical, working solutions.

## Tech Stack
- Python 3.14+
- LangChain (langchain-core, langchain-ollama)
- BeautifulSoup4
- Playwright (headless browser for JS-rendered pages)
- PyYAML (config files)
- uv (package manager)
- Ollama with llama3.2:3b model

## Key Commands
- `uv run main.py` - Run the app (fetches and summarizes jobs from configured sources)
- `uv sync` - Install/update dependencies
- `uv run playwright install chromium` - Install browser (run once before first run)

## Project Structure
- `main.py` - Main entry point (_load_profile, _load_sources, main)
- `crawler.py` - Web crawler (crawl_source, _fetch_page, _discover_job_links, _extract_text)
- `matcher.py` - Job matching with Ollama/LangChain
- `data/profile.yaml` - Candidate profile config
- `data/sites.yaml` - Job sources config
- `pyproject.toml` - Dependencies and project config
- `.venv/` - Virtual environment

## Critical Rules
- Never commit secrets or API keys to the repository
- Test changes locally before committing

## Code Style
- Follow existing patterns in main.py
- Use type hints for function parameters and return values

### Python Privacy Conventions
Use Python's standard conventions for non‑public and private members:

- `_name` → non‑public (internal). Use this for normal internal helpers.
- `__name` → private (name‑mangled). Use only when avoiding subclass collisions.
- `__magic__` → reserved for Python internals. Never create new ones.

## Examples

# Internal helper (preferred)
def _load_config(self):
    ...

# Private with name‑mangling (only when needed)
def __compute_hash(self):
    ...

# Internal attribute
self._cache = {}

# Private attribute with name‑mangling
self.__token = "secret"

## When Stuck
- Check main.py for reference implementation
- Ask user for clarification