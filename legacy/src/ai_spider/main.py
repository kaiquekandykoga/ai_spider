import yaml
from ai_spider.matcher import match_jobs
from ai_spider.crawler import crawl_source


def _load_profile() -> dict:
    """Load candidate profile from data/profile.yaml"""
    with open("data/profile.yaml") as f:
        return yaml.safe_load(f)


def _load_sources() -> list[dict]:
    """Load job sources from data/sites.yaml"""
    with open("data/sites.yaml") as f:
        return yaml.safe_load(f)


def main() -> None:
    profile = _load_profile()
    sources = _load_sources()
    for source in sources:
        raw_text = crawl_source(source["url"])
        matches = match_jobs(raw_text, profile)
        filename = f"temp/{source['name'].replace(' ', '_').lower()}.txt"
        with open(filename, "w") as f:
            f.write(matches)


if __name__ == "__main__":
    main()
