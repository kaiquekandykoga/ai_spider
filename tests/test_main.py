from ai_spider import main


def test_load_profile():
    profile = main._load_profile()
    assert isinstance(profile, dict)
    assert "skills" in profile
    assert "desired_titles" in profile
    assert "location" in profile
    assert "Ruby" in profile["skills"]


def test_load_sources():
    sources = main._load_sources()
    assert isinstance(sources, list)
    assert len(sources) > 0
    assert sources[0]["name"] == "Talent Army"
    assert sources[0]["url"].startswith("http")
