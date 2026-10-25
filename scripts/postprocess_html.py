#!/usr/bin/env python3
"""Add shared scripts and legacy redirects; MyST handles widgets and assets."""

from __future__ import annotations

import json
import os
from html import escape
from pathlib import Path

BUILD_HTML = Path(__file__).resolve().parents[1] / "_build" / "html"

# Load once, before hydration. The Plotly transform awaits MathJax startup.
MATHJAX_SNIPPET = (
    "<script>window.MathJax = {startup: {typeset: false},"
    "tex: {inlineMath: [['$', '$']]}, svg: {fontCache: 'local'}};</script>"
    '<script src="https://cdn.jsdelivr.net/npm/mathjax@4.1.3/tex-svg.js"></script>'
    '<script src="https://cdn.plot.ly/plotly-4.1.2.min.js"></script>'
)


def write_redirects(build: Path, base_url: str = "") -> int:
    """Use MyST's emitted locations/slugs instead of reimplementing its slugger."""
    config = json.loads((build / "config.json").read_text(encoding="utf-8"))
    index = config["projects"][0]["index"]
    prefix = "/" + base_url.strip("/") if base_url.strip("/") else ""
    written = 0
    for page in build.glob("*.json"):
        data = json.loads(page.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not data.get("location", "").endswith(".md"):
            continue
        source = Path(data["location"].lstrip("/"))
        slug = data["slug"]
        target = prefix + ("/" if slug == index else "/" + slug.replace(".", "/") + "/")
        destination = build / source.with_suffix(".html")
        destination.parent.mkdir(parents=True, exist_ok=True)
        href = escape(target, quote=True)
        html = (
            '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">'
            "<title>Redirecting…</title>"
            f'<meta http-equiv="refresh" content="0; url={href}">'
            f'<link rel="canonical" href="{href}"></head>'
            f'<body><p>This page has moved to <a href="{href}">{href}</a>.</p></body></html>\n'
        )
        if not destination.exists() or destination.read_text(encoding="utf-8") != html:
            destination.write_text(html, encoding="utf-8")
            written += 1
    return written


def inject_scripts(page: Path, base_url: str = "") -> bool:
    # Relative to the site root, including GitLab branch-preview prefixes.
    prefix = "/" + base_url.strip("/") if base_url.strip("/") else ""
    snippet = f'<script src="{prefix}/matomo.js" defer></script>'
    html = page.read_text(encoding="utf-8")
    if "</body>" not in html:
        return False  # Skip MyST's meta-only redirect pages.
    updated = html
    if MATHJAX_SNIPPET not in updated:
        updated = updated.replace("<head>", f"<head>{MATHJAX_SNIPPET}", 1)
    if snippet not in updated:
        updated = updated.replace("</body>", f"{snippet}\n</body>", 1)
    if updated == html:
        return False
    page.write_text(updated, encoding="utf-8")
    return True


def process_html() -> None:
    if not (BUILD_HTML / "index.html").exists():
        raise FileNotFoundError("Build the book before injecting shared scripts.")
    base_url = os.environ.get("BASE_URL", "")
    injected = sum(
        inject_scripts(page, base_url) for page in BUILD_HTML.rglob("index.html")
    )
    print(f"Injected shared scripts into {injected} HTML files.")
    print(f"Generated {write_redirects(BUILD_HTML, base_url)} legacy redirects.")


if __name__ == "__main__":
    process_html()
