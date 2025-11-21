#!/usr/bin/env python3
"""
Copy site-wide static assets into the built HTML tree and inject the quiz/analytics
scripts into every HTML page. The script is idempotent and safe to run repeatedly.
"""

from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
STATIC_SRC = ROOT / "_static"
SITE_PUBLIC = ROOT / "_build" / "site" / "public"
BUILD_HTML = ROOT / "_build" / "html"
BUILD_TARGETS = [path for path in (SITE_PUBLIC, BUILD_HTML) if path.exists()]

QUIZ_SNIPPET = '<script src="/_static/quiz.js" defer></script>'
ANALYTICS_SNIPPET = '<script src="/_static/matomo.js" defer></script>'


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


if __name__ == "__main__":
    process_html()
