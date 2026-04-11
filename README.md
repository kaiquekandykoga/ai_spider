# AI Spider

Discover and summarize job listings from across the web using AI

## Quick Start

```bash
uv sync
uv run main.py
```

## Features

- Fetches dynamic job listings from the web (handles JavaScript-rendered pages)
- AI-powered job matching based on your profile (skills, desired titles, location)

## Configuration

Edit `data/profile.yaml` to customize the job search profile:
- `skills`: List of technical skills
- `desired_titles`: List of desired job titles
- `location`: Preferred location (e.g., "Remote", "New Zealand")

## Requirements

- Python 3.14+
- Ollama with llama3.2:3b model
- Playwright with Chromium:
  ```bash
  uv run playwright install chromium
  ```

## Tech Stack

- Python 3.14+ | LangChain | BeautifulSoup4 | Playwright

