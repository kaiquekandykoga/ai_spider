from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def _fetch_page(url: str, return_html: bool = False) -> str:
    """Fetch a single page using Playwright and extract cleaned text."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )
            page.goto(url, wait_until="networkidle", timeout=30000)
            try:
                page.wait_for_selector(
                    "article, .job, .job-card, [class*='job']", timeout=10000
                )
            except Exception:
                pass
            html = page.content()
        finally:
            browser.close()

    if return_html:
        return html

    return _extract_text(html)


def _extract_text(html: str) -> str:
    """Clean HTML and extract text content."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def _discover_job_links(html: str, base_url: str, visited: set[str]) -> list[str]:
    """Extract and filter job-related links from HTML that belong to the same domain."""
    soup = BeautifulSoup(html, "html.parser")
    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc

    job_keywords = {
        "job",
        "career",
        "position",
        "role",
        "opening",
        "apply",
        "vacancy",
        "hiring",
        "opportunity",
    }
    links: list[str] = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href")
        if not href:
            continue
        href = str(href).strip()

        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        if parsed.netloc != base_domain:
            continue
        if full_url in visited:
            continue
        if full_url == base_url:
            continue

        url_lower = full_url.lower()
        link_text = a_tag.get_text(strip=True).lower()
        has_keyword = any(kw in url_lower or kw in link_text for kw in job_keywords)

        if has_keyword:
            links.append(full_url)

    return links


def crawl_source(start_url: str, max_extra_pages: int = 4) -> str:
    """Fetch starting page, discover job links, crawl additional pages, and combine content."""
    visited: set[str] = {start_url}
    """Fetch starting page, discover job links, crawl additional pages, and combine content."""
    visited = {start_url}

    print(f"Fetching jobs from {start_url} ...")

    html = _fetch_page(start_url, return_html=True)
    start_text = _extract_text(html)

    job_links = _discover_job_links(html, start_url, visited)
    domain = urlparse(start_url).netloc
    print(f"Discovered {len(job_links)} job-related links on {domain}")

    pages_to_fetch = job_links[:max_extra_pages]
    extra_texts = []

    for i, link in enumerate(pages_to_fetch, 1):
        print(f"Fetching additional page ({i}/{len(pages_to_fetch)}): {link}")
        visited.add(link)
        extra_texts.append(_fetch_page(link))

    combined = start_text + "\n" + "\n".join(extra_texts)

    lines = [line for line in combined.split("\n") if line.strip()]
    seen = set()
    deduplicated = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            deduplicated.append(line)

    result = "\n".join(deduplicated)
    if len(result) > 24000:
        result = result[:24000]

    return result
