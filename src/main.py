#!/usr/bin/env python3

import sys
from typing import List, Dict, Union
from pathlib import Path

from config import Config
from file_handler import collect_inputs, Inputs
from parser import DocumentParser
from llm_interface import OllamaClient
from mkdocs_generator import MkDocsGenerator

def main() -> None:
    """
    Main function to generate MkDocs documentation from various document types.

    This script performs the following steps:
    1. Loads configuration from command-line arguments.
    2. Scans the specified input directory for supported document and media files.
    3. Extracts text content from the identified documents.
    4. Uses an Ollama LLM to summarize the extracted text for each document.
    5. Generates an MkDocs project, including the summaries and copied media files.
    6. Prints the path to the generated documentation.

    Args:
        None

    Returns:
        None
    """
    # 1. Load configuration
    cfg: Config = Config.from_args()

    # 2. Scan input directory for supported files
    inputs: Inputs = collect_inputs(cfg.input_dir)

    # 3. Extract text from documents
    parser: DocumentParser = DocumentParser()
    # Path.stem is str, path is Path, text is str.
    # The list will store dictionaries where keys are 'path' and 'text'.
    # 'path' stores the Path object of the document.
    # 'text' stores the extracted text content as a string.
    docs: List[Dict[str, Union[Path, str]]] = []
    for path_obj in inputs.documents: # path_obj is of type Path
        text: str = parser.extract(path_obj)
        docs.append({'path': path_obj, 'text': text})

    # 4. Summarize with LLM
    client: OllamaClient = OllamaClient(model=cfg.model)
    # The list will store dictionaries where keys are 'title' and 'content'.
    # 'title' stores the document's stem (filename without extension) as a string.
    # 'content' stores the summarized text as a string.
    summaries: List[Dict[str, str]] = []
    for doc in docs:
        # Ensure 'path' is a Path object and 'text' is a string before processing
        doc_path: Path = doc['path'] # type: ignore
        doc_text: str = str(doc['text'])
        summary: str = client.summarize(doc_text, title=doc_path.stem)
        summaries.append({'title': doc_path.stem, 'content': summary})

    # 5. Copy media files
    # This step is handled internally by the MkDocsGenerator.build() method.

    # 6. Generate MkDocs project
    generator = MkDocsGenerator(
        output_dir=cfg.output_dir,
        summaries=summaries,
        media_paths=inputs.media,
    )
    generator.build()

    print(f"Documentation generated at {cfg.output_dir}/")

if __name__ == "__main__":
    main()
