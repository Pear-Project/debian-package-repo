#!/usr/bin/env python3
"""Generate an Apache-style "Index of ..." index.html for every directory in SITE_DIR."""
import os
from pathlib import Path
from datetime import datetime, timezone
from html import escape

SITE_DIR = Path("_site")
EXCLUDE_DIRS = {".git", ".github", "_site"}
EXCLUDE_FILES = {".gitkeep", ".nojekyll", "CNAME", "index.html"}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Index of {path}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 2rem; }}
  h1 {{ font-size: 1.1rem; font-weight: 600; border-bottom: 1px solid #8884; padding-bottom: 0.5rem; }}
  table {{ border-collapse: collapse; width: 100%; max-width: 720px; }}
  td {{ padding: 0.25rem 1rem 0.25rem 0; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.9rem; }}
  td.size, td.date {{ color: #888; white-space: nowrap; }}
  a {{ text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<h1>Index of {path}</h1>
<table>
{rows}
</table>
</body>
</html>
"""


def human_size(n):
    size = float(n)
    for unit in ("B", "K", "M", "G"):
        if size < 1024 or unit == "G":
            return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}T"


def generate(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS)
        cur = Path(dirpath)
        rel = cur.relative_to(root)
        url_path = "/" if str(rel) == "." else f"/{rel.as_posix()}/"

        rows = []
        if str(rel) != ".":
            rows.append('<tr><td colspan="3"><a href="../">../</a></td></tr>')

        for d in dirnames:
            rows.append(
                f'<tr><td><a href="{escape(d)}/">{escape(d)}/</a></td>'
                f'<td class="size">-</td><td class="date"></td></tr>'
            )

        for f in sorted(filenames):
            if f in EXCLUDE_FILES or f.startswith("."):
                continue
            fp = cur / f
            stat = fp.stat()
            size = human_size(stat.st_size)
            mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            rows.append(
                f'<tr><td><a href="{escape(f)}">{escape(f)}</a></td>'
                f'<td class="size">{size}</td><td class="date">{mtime}</td></tr>'
            )

        if not rows:
            rows.append('<tr><td colspan="3"><em>Empty directory</em></td></tr>')

        html = TEMPLATE.format(path=escape(url_path), rows="\n".join(rows))
        (cur / "index.html").write_text(html)


if __name__ == "__main__":
    generate(SITE_DIR)
