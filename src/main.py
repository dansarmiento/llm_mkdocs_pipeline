#!/usr/bin/env python3

import sys
from config import Config
from file_handler import collect_inputs
from parser import DocumentParser
from llm_interface import OllamaClient
from mkdocs_generator import MkDocsGenerator

def main():
    # 1. Load configuration
    cfg = Config.from_args()

    # 2. Scan input directory for supported files
    inputs = collect_inputs(cfg.input_dir)

    # 3. Extract text from documents
    parser = DocumentParser()
    docs = []
    for path in inputs.documents:
        text = parser.extract(path)
        docs.append({'path': path, 'text': text})

    # 4. Summarize with LLM
    client = OllamaClient(model=cfg.model)
    summaries = []
    for doc in docs:
        summary = client.summarize(doc['text'], title=doc['path'].stem)
        summaries.append({'title': doc['path'].stem, 'content': summary})

    # 5. Copy media files
    # handled inside MkDocsGenerator

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
