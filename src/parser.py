from pathlib import Path
import fitz          # PyMuPDF
import docx

class ParseError(Exception):
    """Custom exception for document parsing errors."""
    pass

class DocumentParser:
    def extract(self, path: Path) -> str:
        ext = path.suffix.lower()
        try:
            if ext == ".txt":
                return path.read_text(encoding="utf-8")
            elif ext == ".md":
                return path.read_text(encoding="utf-8")
            elif ext == ".docx":
                return self._extract_docx(path)
            elif ext == ".pdf":
                return self._extract_pdf(path)
            else:
                # Should not happen if collect_inputs is correct, but good to be safe
                raise ParseError(f"Unsupported file type: {ext} for file {path.name}")
        except (IOError, OSError) as e: # Catches PermissionError, FileNotFoundError etc.
            raise ParseError(f"Cannot read file {path.name}: {e}") from e
        # Specific parsing errors are raised from helper methods

    def _extract_docx(self, path: Path) -> str:
        try:
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        except docx.opc.exceptions.PackageNotFoundError as e: # This is for corrupted/not a docx
            raise ParseError(f"Error parsing DOCX file {path.name}. File may be corrupted or not a valid DOCX file. Details: {e}") from e
        except Exception as e: # Catch any other potential errors from docx library
            raise ParseError(f"Unexpected error parsing DOCX file {path.name}: {e}") from e

    def _extract_pdf(self, path: Path) -> str:
        text = []
        try:
            with fitz.open(path) as pdf:
                for page in pdf:
                    text.append(page.get_text())
            return "\n".join(text)
        except fitz.fitz.FitzError as e: # PyMuPDF's base exception
            raise ParseError(f"Error parsing PDF file {path.name}. File may be corrupted or not a valid PDF. Details: {e}") from e
        except Exception as e: # Catch any other potential errors from fitz library
            raise ParseError(f"Unexpected error parsing PDF file {path.name}: {e}") from e
