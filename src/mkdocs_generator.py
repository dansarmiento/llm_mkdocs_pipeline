import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class MkDocsGenerator:
    def __init__(self, output_dir: Path, summaries: list, media_paths: list):
        self.output_dir = output_dir
        self.docs_dir = output_dir / "docs"
        self.summaries = summaries
        self.media_paths = media_paths

    def build(self):
        # 1. Clean or create output dirs
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.docs_dir.mkdir(parents=True)

        # 2. Copy media
        for media in self.media_paths:
            dest = self.docs_dir / media.name
            shutil.copy2(media, dest)

        # 3. Render markdown files
        for item in self.summaries:
            md_file = self.docs_dir / f"{item['title']}.md"
            md_file.write_text(item['content'], encoding="utf-8")

        # 4. Render mkdocs.yml
        self._render_mkdocs_yml()

    def _render_mkdocs_yml(self):
        env = Environment(
            loader=FileSystemLoader(searchpath=Path(__file__).parent.parent / "mkdocs_template")
        )
        template = env.get_template("mkdocs.yml.j2")
        pages = [{"title": s["title"], "file": f"{s['title']}.md"} for s in self.summaries]
        rendered = template.render(pages=pages)
        (self.output_dir / "mkdocs.yml").write_text(rendered, encoding="utf-8")
