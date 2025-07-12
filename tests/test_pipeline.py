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


def test_pipeline_creates_output_files(fs, mock_llm_client, mocker):
    """Tests that the main pipeline script creates the expected output files."""
    # 1. Set up the fake file system
    fake_input_dir = "/fake_input"
    fake_output_dir = "/fake_output"
    fake_template_dir = "/app/mkdocs_template"
    fs.create_dir(fake_input_dir)
    fs.create_file(f"{fake_input_dir}/doc1.txt", contents="This is a test document.")
    fs.create_dir(fake_template_dir)
    fs.create_file(
        f"{fake_template_dir}/mkdocs.yml.j2",
        contents="site_name: Generated Project Documentation\n"
    )
    fs.create_file(
        f"{fake_template_dir}/index.md.j2",
        contents="# Project Documentation\n"
    )

    # 2. Mock sys.argv to control the script's configuration
    mocker.patch("sys.argv", ["src/main.py", "--input", fake_input_dir, "--output", fake_output_dir])

    # 3. Run the main pipeline function
    from src.main import main
    main()

    # 4. Assert that the output directory and markdown file were created
    assert fs.exists(fake_output_dir)
    assert fs.exists(f"{fake_output_dir}/docs/doc1.md")
