from pathlib import Path
from typing import List, NamedTuple

class Inputs(NamedTuple):
    documents: List[Path]
    media: List[Path]

SUPPORTED_DOC_EXT = {".txt", ".md", ".pdf", ".docx"}
SUPPORTED_MEDIA_EXT = {".png", ".jpg", ".jpeg", ".mp4", ".gif"}

def collect_inputs(root: Path) -> Inputs:
    docs = []
    media = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext in SUPPORTED_DOC_EXT:
            docs.append(path)
        elif ext in SUPPORTED_MEDIA_EXT:
            media.append(path)
    return Inputs(documents=docs, media=media)
