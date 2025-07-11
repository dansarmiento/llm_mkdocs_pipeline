import subprocess
from pathlib import Path
from typing import Optional

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
        # Launch ollama via subprocess
        proc = subprocess.run(
            ["ollama", "run", self.model, "--prompt", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return proc.stdout.strip()
