import pytest

@pytest.fixture
def mock_llm_client(mocker):
    """Mocks the OllamaClient.summarize method."""
    mocked_summarize = mocker.patch(
        "llm_interface.OllamaClient.summarize",
        return_value="# Mocked Title\n\nThis is mocked content."
    )
    return mocked_summarize

# Import OllamaClient here to be used in the test
from llm_interface import OllamaClient

def test_always_passes():
    assert True

def test_mock_llm_summarize(mock_llm_client):
    """Tests that the mock_llm_client fixture correctly mocks summarize."""
    client = OllamaClient(model="test_model") # Model name doesn't matter due to mocking
    summary = client.summarize("Some text", title="Test Title")
    assert summary == "# Mocked Title\n\nThis is mocked content."
    mock_llm_client.assert_called_once_with("Some text", title="Test Title")
