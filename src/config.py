import argparse
from pathlib import Path

class Config:
    def __init__(self, input_dir: Path, output_dir: Path, model: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.model = model

    @classmethod
    def from_args(cls):
        parser = argparse.ArgumentParser(
            description="Generate MkDocs documentation using a local Ollama LLM"
        )
        parser.add_argument(
            "--input", "-i", dest="input_dir", required=True,
            type=Path, help="Path to input material folder"
        )
        parser.add_argument(
            "--output", "-o", dest="output_dir", required=True,
            type=Path, help="Path to output MkDocs project"
        )
        parser.add_argument(
            "--model", "-m", dest="model", default="mistral",
            help="Ollama model name to use for summarization"
        )
        args = parser.parse_args()
        return cls(args.input_dir, args.output_dir, args.model)
