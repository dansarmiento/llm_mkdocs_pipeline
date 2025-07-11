# MVP Specification: LLM-Powered MkDocs Generator

## Objective

Build a Python program that uses a locally hosted LLM via Ollama to convert a folder of documents and associated media into a ready-to-serve MkDocs project. The process must be CPU and space efficient, targeting deployment on a virtual machine with ~30GB of free disk space.

---

## Input

A root input directory (e.g., `./input_material/`) containing:

- Text documents: `.txt`, `.md`, `.docx`, `.pdf`
- Media files: `.png`, `.jpg`, `.mp4`, etc.
- Optional subfolders for organization

---

## Output

A structured MkDocs project directory (e.g., `./docs_project/`) containing:

- `mkdocs.yml` configuration file
- `docs/` folder with:
  - Markdown files generated from document content
  - Embedded or linked media
  - A structured layout reflecting the input directory
- Optional `requirements.txt` for MkDocs plugins

---

## Core Features

### 1. Document Parsing and Extraction

- `.txt`: Read as plain text
- `.md`: Copy or lightly summarize
- `.docx`: Extract using `python-docx`
- `.pdf`: Extract using `PyMuPDF` or `pdfplumber`
- Load and process data in-memory to minimize disk I/O

### 2. Multimedia Handling

- Copy media files into the corresponding `docs/` subfolder
- Embed or link media in Markdown using standard syntax

### 3. LLM Integration via Ollama

- Use a local model such as `mistral`, `llama2`, or `gemma`
- Prompt model to:
  - Generate summaries
  - Create headers and bullet points
  - Output Markdown-formatted content

Example prompt:
"Summarize the following document content for a software documentation website using Markdown format with headings, bullet points, and links to any referenced files."


### 4. MkDocs Project Scaffolding

- Automatically generate:
  - `mkdocs.yml` with correct navigation
  - Logical file and folder structure
- Use a simple theme (e.g., `mkdocs-material`) to keep output lightweight

### 5. Efficiency

- Avoid multiprocessing for simplicity and memory control
- Avoid temporary files where possible
- Clean up after processing each document
- Directly copy media without modifying or transcoding

---

## Configuration

Optional command-line arguments or `.env` config:

```bash
python generate_docs.py --input ./input_material --output ./docs_project --model mistral
```

### Minimal Dependencies 
ollama
mkdocs
python-docx
PyMuPDF or pdfplumber
Pillow

### Example Output Structure
```bash
docs_project/
├── mkdocs.yml
├── docs/
│   ├── index.md
│   ├── intro/
│   │   ├── overview.md
│   │   ├── image1.png
│   └── usage/
│       ├── usage_guide.md
│       └── demo_video.mp4
```

### Stretch Goals (Future Iterations)
- Monitor input folder for new files
- Index files for search using embeddings
- Support tag-based categorization
- Auto-suggest improved folder structure

### MVP Success Criteria
- Correctly processes a folder of documents and media
- Uses an Ollama-hosted LLM to create clean, structured Markdown
- Generates a valid MkDocs project that can be served with mkdocs serve
- Runs reliably on a virtual machine with limited CPU and 30GB disk space