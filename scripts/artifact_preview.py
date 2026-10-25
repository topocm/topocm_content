"""Adapt the pinned MyST static theme to GitLab's file-only artifact viewer.

Run only after postprocess-html, with the same BASE_URL. Production skips this.
"""

import json
import os
import re
from pathlib import Path

from postprocess_html import BUILD_HTML

# These are emitted by the pinned book-theme. Fail on upstream changes rather
# than silently publishing a preview with broken navigation.
INDEX_REDIRECT = (
    "<script>(function(){var p=window.location.pathname;"
    "if(p.endsWith('/index.html'))window.location.replace("
    "(p.slice(0,-10)||'/')+window.location.search+window.location.hash);})();</script>"
)
URL_HELPER = (
    "function Ct(t,e){if(!e||Vi(t))return t;if(!t)return e;"
    'let r=e.replace(/\\/+$/,""),n=t.startsWith("/")?t:`/${t}`;return r+n}'
)


def rewrite_preview(build: Path, base_url: str) -> None:
    prefix = base_url.rstrip("/")
    if not prefix.startswith("/") or prefix == "":
        raise ValueError("Artifact previews require a nonempty BASE_URL path")
    pages = list(build.rglob("index.html"))
    routes = {}
    for page in pages:
        path = prefix + "/" + page.relative_to(build).as_posix()
        routes[path.removesuffix("/index.html")] = path
        routes[path.removesuffix("index.html")] = path

    bundles = [
        p for p in (build / "build").rglob("*.js") if URL_HELPER in p.read_text()
    ]
    if len(bundles) != 1 or any(INDEX_REDIRECT not in p.read_text() for p in pages):
        raise RuntimeError("MyST theme changed: review the artifact-preview URL patch")

    # The shared helper covers hydrated links and keyboard search navigation.
    original = URL_HELPER.replace("function Ct(", "function artifactOriginalUrl(", 1)
    wrapper = (
        "function Ct(t,e){const u=artifactOriginalUrl(t,e);if(!u)return u;"
        "const [path,...suffix]=u.split(/(?=[?#])/);"
        f'return ({json.dumps(routes)}[path]||path)+suffix.join("");}}'
    )
    bundle = bundles[0]
    bundle.write_text(bundle.read_text().replace(URL_HELPER, original + wrapper))

    # Cover initial HTML, canonical links and legacy meta-refresh redirects too.
    def replace_url(match):
        path, suffix = re.match(r"([^?#]*)(.*)", match[1]).groups()
        return '"' + routes.get(path, path) + suffix + '"'

    for page in build.rglob("*.html"):
        html = page.read_text().replace(INDEX_REDIRECT, "")
        html = re.sub(r'"(' + re.escape(prefix) + r'/[^"<>]*)"', replace_url, html)
        for route, target in routes.items():
            html = html.replace(
                f'content="0; url={route}"', f'content="0; url={target}"'
            )
        page.write_text(html)


if __name__ == "__main__":
    rewrite_preview(BUILD_HTML, os.environ["BASE_URL"])
