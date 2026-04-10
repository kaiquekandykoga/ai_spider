# AGENTS.md

App used to find resources on the web using Python and LangChain.

## Agent Role
You are a coding assistant helping maintain and extend this web scraping project. Focus on practical, working solutions.

## Tech Stack
- Python 3.14+
- LangChain (langchain-core, langchain-ollama)
- BeautifulSoup4
- requests
- uv (package manager)
- Ollama with llama3.2:3b model

## Key Commands
- `uv run main.py` - Run the app (fetches and summarizes jobs from talent.army)
- `uv sync` - Install/update dependencies

## Project Structure
- `main.py` - Main entry point (fetch_jobs, summarise_jobs, main)
- `pyproject.toml` - Dependencies and project config
- `.venv/` - Virtual environment

## Critical Rules
- Never commit secrets or API keys to the repository
- Test changes locally before committing

## Code Style
- Follow existing patterns in main.py
- Use type hints for function parameters and return values

## When Stuck
- Check main.py for reference implementation
- Ask user for clarification