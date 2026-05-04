"""Render Jinja2 templates → static HTML at repo root.

Run from repo root:
    python tools/build.py

Inputs:  templates/*.html (Jinja sources)
Outputs: <root>/{index,methodology,values,404}.html (deployable static)

The rendered HTML is what GitHub Pages / Cloudflare Pages / any static
host serves. Templates exist for editor convenience (single base.html
shared across pages); editing the rendered files directly is also fine
but means the templates fall out of sync.

Edit `CONTEXT` below to change the global tool CTA target.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    sys.stderr.write(
        "jinja2 not installed.\n"
        "Install with:  pip install jinja2\n"
    )
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"

# Pages to render. Skip base.html (layout) and any partials starting with `_`.
PAGES = ["index.html", "methodology.html", "values.html", "404.html"]

# Global render context. Change `tool_cta_url` once the actual tool is hosted
# somewhere; rerun `python tools/build.py` and commit the rebuilt HTML.
CONTEXT = {
    "tool_cta_url": "https://seerbench.com",
}


def main() -> int:
    if not TEMPLATES_DIR.is_dir():
        sys.stderr.write(f"templates/ not found at {TEMPLATES_DIR}\n")
        return 1

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=False,
        lstrip_blocks=False,
    )

    rendered = []
    for page in PAGES:
        src = TEMPLATES_DIR / page
        if not src.is_file():
            sys.stderr.write(f"skip: {page} (template missing)\n")
            continue
        template = env.get_template(page)
        html = template.render(**CONTEXT)
        out = REPO_ROOT / page
        out.write_text(html, encoding="utf-8")
        rendered.append((page, len(html)))

    print(f"Rendered {len(rendered)} pages → {REPO_ROOT}")
    for page, size in rendered:
        print(f"  {page:<20} {size:>7,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
