from unittest.mock import patch, MagicMock
from ai_spider.matcher import match_jobs


def test_match_jobs():
    profile = {
        "skills": ["Ruby", "Python"],
        "desired_titles": ["Software Engineer"],
        "location": "Remote",
    }

    mock_response = MagicMock()
    mock_response.content = "Test match result"

    with patch("ai_spider.matcher.ChatOllama") as mock_llm:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = mock_response
        mock_llm.return_value = mock_instance

        match_jobs("fake job text", profile)

        mock_instance.invoke.assert_called_once()
        call_args = mock_instance.invoke.call_args[0][0]
        system_msg = call_args[0]
        assert "Ruby" in system_msg.content
        assert "Python" in system_msg.content
        assert "Remote" in system_msg.content
