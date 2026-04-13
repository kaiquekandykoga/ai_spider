import pytest
from ai_spider.crawler import _extract_text, _discover_job_links


def test_extract_text():
    html = """
    <html><body>
    <script>var x = 1;</script>
    <nav>Menu</nav>
    <article>Software Engineer at TechCorp</article>
    </body></html>
    """
    text = _extract_text(html)
    assert "var x = 1" not in text
    assert "Menu" not in text
    assert "Software Engineer at TechCorp" in text


def test_discover_job_links():
    html = """
    <html><body>
    <a href="/jobs/backend">Backend Jobs</a>
    <a href="https://example.com/careers">Careers Page</a>
    <a href="https://other.com/job">External Job</a>
    <a href="https://example.com/about">About Us</a>
    </body></html>
    """
    base_url = "https://example.com"
    visited = set()
    links = _discover_job_links(html, base_url, visited)

    assert len(links) >= 1
    for link in links:
        assert link.startswith(base_url)
        assert "job" in link.lower() or "career" in link.lower()
