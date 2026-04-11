# $ uv init
# $ uv add langchain langchain-ollama langchain-core beautifulsoup4
#
# Dynamic pages using JavaScript
# $ uv add playwright
# $ uv run playwright install chromium
# $ uv run main.py


import yaml

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from matcher import match_jobs


def load_sources() -> list[dict]:
    """Load job sources from data/sites.yaml"""
    with open("data/sites.yaml") as f:
        return yaml.safe_load(f)


def load_profile() -> dict:
    """Load candidate profile from data/profile.yaml"""
    with open("data/profile.yaml") as f:
        return yaml.safe_load(f)


def fetch_jobs(url: str) -> str:
    """Fetch job listings using a headless browser to handle JS-rendered pages."""
    print(f"Fetching jobs from {url} ...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for job listing elements to appear in the DOM.
        # Adjust the selector below if needed after inspecting the page.
        try:
            page.wait_for_selector(
                "article, .job, .job-card, [class*='job']", timeout=10000
            )
        except Exception:
            pass  # Proceed even if selector times out; content may still have loaded

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    # Trim to avoid overloading the context window
    return text[:8000]


def main():
    profile = load_profile()
    sources = load_sources()
    for source in sources:
        raw_text = fetch_jobs(source["url"])
        matches = match_jobs(raw_text, profile)
        print("=" * 60)
        print(f"MATCHING JOBS AT {source['name']}")
        print("=" * 60)
        print(matches)
        print()


if __name__ == "__main__":
    main()
