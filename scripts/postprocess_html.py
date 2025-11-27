#!/usr/bin/env python3
"""
Copy site-wide static assets into the built HTML tree, inject quiz/analytics
snippets, and generate legacy HTML redirects so older URLs continue to work.
The script is idempotent and safe to run repeatedly.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
import shutil


ROOT = Path(__file__).resolve().parents[1]
STATIC_SRC = ROOT / "_static"
SITE_PUBLIC = ROOT / "_build" / "site" / "public"
BUILD_HTML = ROOT / "_build" / "html"
BUILD_TARGETS = [path for path in (SITE_PUBLIC, BUILD_HTML) if path.exists()]
CONFIG_CANDIDATES = [
    ROOT / "_build" / "site" / "config.json",
    BUILD_HTML / "config.json",
]

QUIZ_SNIPPET = '<script src="/_static/quiz.js" defer></script>'
ANALYTICS_SNIPPET = '<script src="/_static/matomo.js" defer></script>'
HTML_REDIRECT_TEMPLATE = """<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <title>Redirecting…</title>\n  <meta http-equiv=\"refresh\" content=\"0; url={target_href}\">\n  <link rel=\"canonical\" href=\"{canonical_url}\">\n  <script>window.location.replace('{target_href}');</script>\n</head>\n<body>\n  <p>This page has moved to <a href=\"{canonical_url}\">{canonical_url}</a>.</p>\n</body>\n</html>\n"""


@dataclass(frozen=True)
class RedirectSpec:
    legacy_html: Path
    slug_parts: tuple[str, ...]

    @property
    def canonical_url(self) -> str:
        if not self.slug_parts:
            return "/"
        return "/" + "/".join(self.slug_parts) + "/"


def _iter_toc_files(entries: Iterable[dict]) -> Iterable[str]:
    for item in entries or []:
        file_path = item.get("file")
        if file_path:
            yield file_path
        children = item.get("children") or []
        if children:
            yield from _iter_toc_files(children)


def load_markdown_sources() -> list[Path]:
    config_data = None
    for candidate in CONFIG_CANDIDATES:
        if candidate.exists():
            config_data = json.loads(candidate.read_text(encoding="utf-8"))
            break
    if config_data is None:
        raise FileNotFoundError(
            "Could not locate a MyST config.json. Please build the book before running redirects."
        )

    projects = config_data.get("projects") or []
    if not projects:
        return []

    files = {
        Path(file_path)
        for file_path in _iter_toc_files(projects[0].get("toc", []))
        if file_path
    }
    markdown_files = [path for path in files if path.suffix.lower() == ".md"]
    return sorted(markdown_files, key=lambda path: path.as_posix())


def slugify_segment(value: str) -> str:
    return value.lower().replace("_", "-")


def slugify_leaf(value: str) -> str:
    slug = slugify_segment(value).lstrip("0123456789")
    return slug or "page"


def build_redirect_specs() -> list[RedirectSpec]:
    markdown_files = load_markdown_sources()
    slug_counts: dict[tuple[tuple[str, ...], str], int] = defaultdict(int)
    specs: list[RedirectSpec] = []

    for rel_path in markdown_files:
        if not rel_path.parts:
            continue

        parent_parts = rel_path.parts[:-1]
        is_root_index = not parent_parts and rel_path.stem.lower() == "index"
        if is_root_index:
            # The homepage already lives at index.html, so there is nothing to redirect.
            continue

        slug_dirs = [
            slugify_segment(part) for part in parent_parts if part not in ("", ".")
        ]
        base_slug = slugify_leaf(rel_path.stem)
        key = (tuple(slug_dirs), base_slug)
        suffix_index = slug_counts[key]
        slug_counts[key] += 1
        slug_name = base_slug if suffix_index == 0 else f"{base_slug}-{suffix_index}"
        slug_parts = tuple((*slug_dirs, slug_name))

        legacy_html = Path(*rel_path.parts).with_suffix(".html")
        specs.append(RedirectSpec(legacy_html=legacy_html, slug_parts=slug_parts))

    return specs


def write_redirects(target: Path, redirects: Sequence[RedirectSpec]) -> int:
    created = 0
    for spec in redirects:
        destination = target / spec.legacy_html
        destination.parent.mkdir(parents=True, exist_ok=True)
        target_href = spec.canonical_url
        html = HTML_REDIRECT_TEMPLATE.format(
            target_href=target_href,
            canonical_url=spec.canonical_url,
        )
        if destination.exists() and destination.read_text(encoding="utf-8") == html:
            continue
        destination.write_text(html, encoding="utf-8")
        created += 1
    return created


def copy_static(dest: Path) -> None:
    if not STATIC_SRC.exists():
        raise FileNotFoundError(f"Static source directory missing: {STATIC_SRC}")
    for src_file in STATIC_SRC.rglob("*"):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(STATIC_SRC)
        dst_file = dest / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dst_file)


def inject_scripts(page: Path) -> bool:
    html = page.read_text(encoding="utf-8")
    snippets = []
    if "/_static/quiz.js" not in html:
        snippets.append(QUIZ_SNIPPET)
    if "/_static/matomo.js" not in html:
        snippets.append(ANALYTICS_SNIPPET)

    if not snippets:
        return False

    injection = "\n".join(snippets) + "\n"
    if "</body>" in html:
        updated = html.replace("</body>", f"{injection}</body>", 1)
    else:
        updated = html + "\n" + injection
    page.write_text(updated, encoding="utf-8")
    return True


def process_html() -> None:
    if not BUILD_TARGETS:
        raise FileNotFoundError(
            "No build outputs found in _build/site/public or _build/html"
        )

    redirect_specs = build_redirect_specs()

    for target in BUILD_TARGETS:
        static_dest = target / "_static"
        copy_static(static_dest)

        injected = 0
        for html_file in target.rglob("*.html"):
            try:
                if inject_scripts(html_file):
                    injected += 1
            except UnicodeDecodeError:
                continue

        print(f"Processed {target} -> injected scripts into {injected} HTML files.")

        created = write_redirects(target, redirect_specs)
        print(f"Generated {created} legacy redirect files under {target}")


if __name__ == "__main__":
    process_html()
