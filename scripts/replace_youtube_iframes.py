#!/usr/bin/env python3
"""
Scan the repository for MyST/markdown files containing code-cell blocks
with Video("<id>") and replace them with an iframe directive suitable
for the course:

:::{iframe} https://www.youtube.com/embed/<id>?rel=0&showinfo=0&iv_load_policy=3&enablejsapi=1
:width: 100%
:::

The script is idempotent and makes a backup copy of each modified file
with suffix .bak.
"""

import re
from pathlib import Path
import sys


VIDEO_BLOCK_RE = re.compile(
    r"```\{code-cell\} ipython3\s*\n\s*Video\(\s*\"(?P<id>[-_A-Za-z0-9]+)\"\s*\)\s*\n\s*```",
    flags=re.MULTILINE,
)

# Match prior iframe-style embeds emitted by earlier runs so we normalize them
IFRAME_EMBED_RE = re.compile(
    r":::\{iframe\}\s*https?://www\.youtube\.com/embed/(?P<id>[-_A-Za-z0-9]+)[^\n]*\n:width:\s*[^\n]*\n:::",
    flags=re.IGNORECASE,
)


def video_replacement(match: re.Match) -> str:
    vid = match.group("id")
    return f":::{'youtube'} {vid}\n:width: 100%\n:height: 480\n:::\n"


def iframe_replacement(match: re.Match) -> str:
    vid = match.group("id")
    return f":::{'youtube'} {vid}\n:width: 100%\n:height: 480\n:::\n"


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, n1 = VIDEO_BLOCK_RE.subn(video_replacement, text)
    new_text, n2 = IFRAME_EMBED_RE.subn(iframe_replacement, new_text)
    n = n1 + n2
    if n:
        bak = path.with_suffix(path.suffix + ".bak")
        bak.write_text(text, encoding="utf-8")
        path.write_text(new_text, encoding="utf-8")
        print(f"Updated {path} ({n} replacement(s)), backup -> {bak}")
    return n


def main(root: Path):
    md_files = list(root.rglob("*.md"))
    total = 0
    for p in md_files:
        try:
            total += process_file(p)
        except UnicodeDecodeError:
            # skip binary or non-utf8 files
            continue
    print(f"Done. Total replacements: {total}")


if __name__ == "__main__":
    start = Path(__file__).resolve().parents[1]
    if len(sys.argv) > 1:
        start = Path(sys.argv[1])
    main(start)
