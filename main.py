# $ uv init
# $ uv add langchain langchain-ollama langchain-core requests beautifulsoup4
# $ uv run main.py

import requests
from bs4 import BeautifulSoup
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


TALENT_ARMY_URL = "https://talent.army/job-board"
RECRUIT_IT_URL = "https://www.recruitit.co.nz/jobs"


def fetch_jobs(url: str) -> str:
    """Fetch job listings from a given URL and return cleaned text."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    print(f"Fetching jobs from {url} ...")
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

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
    raw_text_army = fetch_jobs(TALENT_ARMY_URL)
    summary_army = summarise_jobs(raw_text_army)

    print("=" * 60)
    print("AVAILABLE JOBS AT talent.army")
    print("=" * 60)
    print(summary_army)
    print()

    raw_text_recruit = fetch_jobs(RECRUIT_IT_URL)
    summary_recruit = summarise_jobs(raw_text_recruit)

    print("=" * 60)
    print("AVAILABLE JOBS AT recruitit.co.nz")
    print("=" * 60)
    print(summary_recruit)


if __name__ == "__main__":
    main()
