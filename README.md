# AI Spider

Discover and summarize job listings from across the web using AI

## Quick Start

```bash
uv sync
uv run python -m ai_spider
```

## Project Structure

- `src/ai_spider/main.py` - Main entry point (load_profile, load_sources, main)
- `src/ai_spider/crawler.py` - Web crawler (crawl_source)
- `src/ai_spider/matcher.py` - Job matching with Ollama/LangChain
- `data/profile.yaml` - Candidate profile config
- `data/sites.yaml` - Job sources config

## Features

- Fetches dynamic job listings from the web (handles JavaScript-rendered pages)
- AI-powered job matching based on your profile (skills, desired titles, location)

## Configuration

Edit `data/profile.yaml` to customize the job search profile:
- `skills`: List of technical skills (e.g., "Ruby")
- `desired_titles`: List of desired job titles (e.g., "AI Engineer")
- `location`: Preferred location (e.g., "Remote", "New Zealand")

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_SPIDER_MODEL_NAME` | Ollama model to use for job matching | `llama3.2:3b` |

## Requirements

- Python 3.14+
- Ollama models
- Playwright with Chromium:
  ```bash
  uv run playwright install chromium
  ```

## Tech Stack

- Python 3.14+ | LangChain | BeautifulSoup4 | Playwright

## Testing

```bash
uv run pytest
```

