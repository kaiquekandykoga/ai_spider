# $ uv init
# $ uv add langchain langchain-ollama langchain-core requests beautifulsoup4
#
# Dynamic pages using JavaScript
# $ uv add playwright
# $ uv run playwright install chromium
# $ uv run main.py


from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

JOB_SOURCES = [
    {"name": "Talent Army", "url": "https://talent.army/job-board"},
    {"name": "Recruit I.T.", "url": "https://www.recruitit.co.nz/jobs"},
    {"name": "GitLab", "url": "https://about.gitlab.com/jobs/all-jobs"},
]


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


def summarise_jobs(raw_text: str) -> str:
    """Use Ollama / llama3.2:3b via LangChain to summarise the job listings."""
    llm = ChatOllama(model="llama3.2:3b", temperature=0)
    messages = [
        SystemMessage(
            content=(
                "You are a helpful job-search assistant. "
                "Extract and list all job positions found in the provided webpage text. "
                "For each job include: Job Title, Company (if mentioned), Location (if mentioned), "
                "and a one-sentence description. "
                "Format the output as a numbered list. "
                "If no jobs are found, say so clearly."
            )
        ),
        HumanMessage(content=f"Here is the webpage content:\n\n{raw_text}"),
    ]
    print("Sending content to Ollama (llama3.2:3b) for analysis ...\n")
    response = llm.invoke(messages)
    return response.content


def main():
    for source in JOB_SOURCES:
        raw_text = fetch_jobs(source["url"])
        summary = summarise_jobs(raw_text)
        print("=" * 60)
        print(f"AVAILABLE JOBS AT {source['name']}")
        print("=" * 60)
        print(summary)
        print()


if __name__ == "__main__":
    main()
