from pathlib import Path
import fitz          # PyMuPDF
import docx

class DocumentParser:
    def extract(self, path: Path) -> str:
        ext = path.suffix.lower()
        if ext == ".txt":
            return path.read_text(encoding="utf-8")
        elif ext == ".md":
            return path.read_text(encoding="utf-8")
        elif ext == ".docx":
            return self._extract_docx(path)
        elif ext == ".pdf":
            return self._extract_pdf(path)
        else:
            return ""

    def _extract_docx(self, path: Path) -> str:
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    def _extract_pdf(self, path: Path) -> str:
        text = []
        with fitz.open(path) as pdf:
            for page in pdf:
                text.append(page.get_text())
        return "\n".join(text)
