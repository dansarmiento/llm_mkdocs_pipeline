# LLM MkDocs Pipeline

This project uses a local LLM served via Ollama to automatically generate structured MkDocs documentation from a folder of documents and media files.

## How It Works

1. Feed your documents and media into the `input_material/` folder.
2. Run the pipeline using a local model (e.g., `mistral`) hosted by Ollama.
3. The output will be a ready-to-serve MkDocs project.

## Getting Started

```bash
git clone https://github.com/dansarmiento/llm-mkdocs-pipeline.git
cd llm-mkdocs-pipeline
pip install -r requirements.txt
ollama run mistral
python src/main.py --input input_material --output docs_project --model mistral