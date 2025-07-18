# LLM MkDocs Pipeline

This project uses a local LLM served via Ollama to automatically generate structured MkDocs documentation from a folder of documents and media files.

## How It Works - TLDR

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
```

### How it Works: The Pipeline Explained

Here's a step-by-step breakdown of the process, from input to the final MkDocs site:

1.  **Input Materials**: You start by placing all your source documents and media files into a folder named `input_material/`. This can include text files, Markdown files, and other documents that you want to be part of your documentation site.

2.  **Running the Pipeline**: The core of the project is the Python script `src/main.py`. You run this script from your terminal. When you run it, you specify three key things:
    * `--input`: The folder containing your source documents (e.g., `input_material/`).
    * `--output`: The folder where the generated MkDocs project will be saved (e.g., `docs_project/`).
    * `--model`: The name of the local LLM you want to use, which is served by Ollama (e.g., `mistral`).

3.  **Content Generation with an LLM**: The `main.py` script iterates through the files in your input folder. For each document, it sends the content to the local LLM you've specified. The script likely prompts the LLM to do the following:
    * **Summarize the content**: Create a concise summary of each document.
    * **Structure the information**: Organize the information in a clear and readable way, using Markdown formatting (headings, lists, etc.).
    * **Generate Markdown files**: The output from the LLM is then saved as new Markdown (`.md`) files.

4.  **Creating the MkDocs Site**: Once the Markdown files are generated, the pipeline creates the MkDocs site structure.
    * It uses the `mkdocs_template/` folder as a starting point. This template includes a pre-configured `mkdocs.yml` file, which defines the site's navigation, theme, and other settings.
    * The generated Markdown files are placed into the `docs/` subdirectory of your output folder.
    * The `mkdocs.yml` from the template is used to build the site's structure, creating a navigation menu that links to all the newly generated documentation pages.

5.  **The Final Output**: The result is a complete and ready-to-use MkDocs project in the output folder you specified. You can then serve this as a local website using the command `mkdocs serve` from within the output directory, or you can deploy it to a web server.

In essence, this project acts as an automated "documentation writer" that takes your raw notes and documents, uses an LLM to clean them up and structure them, and then assembles them into a professional-looking documentation website with MkDocs.

### **Minimum Requirements (for smaller models like Mistral 7B)**
This configuration is suitable for basic functionality, testing, and processing smaller batches of documents with a 7-billion-parameter model.

* **Operating System:** 64-bit Linux (Ubuntu Server 22.04 LTS is recommended).
* **CPU:** 2 Cores (4 cores recommended for better performance).
* **RAM:** **8 GB**. This is the most critical requirement. An LLM with ~7 billion parameters requires at least this much available memory to load and run.
* **Disk Space:** **25 GB** of fast storage (SSD/NVMe).
    * **OS:** ~5-10 GB for a standard server installation.
    * **Ollama + Models:** ~10 GB (Ollama itself is small, but a 7B model like `mistral:7b` is over 4 GB, and you'll want space for others).
    * **Project Files & Workspace:** ~5 GB for the pipeline, its dependencies, and your input/output documents.

---

### **Recommended Specifications (for better performance and larger models)**
This configuration provides a smoother experience, allows for faster document processing, and gives you the flexibility to use larger, more capable models (e.g., 13B models) or run multiple models.

* **Operating System:** 64-bit Linux (Ubuntu Server 22.04 LTS).
* **CPU:** **4 Cores** or more (modern CPU with AVX support is a plus).
* **RAM:** **16 GB** or more. This is the minimum for running 13B parameter models and provides significant overhead for the OS and other processes, preventing slowdowns. If you plan to use models larger than 13B, you will need 32 GB or more.
* **Disk Space:** **50 GB** or more (SSD/NVMe).
    * This provides ample space for the OS, multiple large language models, Python dependencies, and a large corpus of documents to be processed without worrying about storage constraints.
