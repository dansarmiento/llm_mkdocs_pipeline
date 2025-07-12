import subprocess
from pathlib import Path
from typing import Optional

class OllamaError(Exception):
    """Custom exception for Ollama client errors."""
    pass

class OllamaClient:
    def __init__(self, model: str):
        self.model = model

    def summarize(self, text: str, title: Optional[str] = None) -> str:
        """
        Calls the Ollama CLI to summarize `text` into Markdown form.
        """
        prompt = (
            f"Summarize the following document titled '{title}' "
            "for a software documentation website in Markdown format "
            "with headings, bullet points, and links to any referenced files:\n\n"
            f"{text}"
        )
        try:
            # Launch ollama via subprocess
            proc = subprocess.run(
                ["ollama", "run", self.model, "--prompt", prompt],
                capture_output=True,
                text=True,
                check=True,
                timeout=60  # Add a timeout for Ollama connection
            )
            return proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_message = f"Ollama CLI failed with exit code {e.returncode}."
            if e.stderr:
                error_message += f"\nError details: {e.stderr.strip()}"
            else:
                error_message += "\nNo stderr output from Ollama. Is the model name correct and Ollama server running?"
            raise OllamaError(error_message) from e
        except subprocess.TimeoutExpired as e:
            raise OllamaError(
                f"Ollama command timed out after {e.timeout} seconds. "
                "The Ollama server might be slow or unresponsive."
            ) from e
        except OSError as e:
            # This can happen if 'ollama' command is not found
            raise OllamaError(
                f"Failed to execute Ollama CLI. Ensure 'ollama' is installed and in your PATH. Error: {e}"
            ) from e
