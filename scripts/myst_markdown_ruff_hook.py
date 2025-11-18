#!/usr/bin/env python3
"""Pre-commit hook to format MyST Markdown notebooks via Ruff.

The hook converts a MyST Markdown file to a temporary ``.ipynb`` notebook using
``jupytext``, runs ``ruff check --fix`` and ``ruff format`` on that notebook, and
writes the formatted result back to the original Markdown file.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable

import jupytext

RUF_CHECK_CMD = ("ruff", "check", "--fix")
RUF_FORMAT_CMD = ("ruff", "format")


def run_command(
    args: Iterable[str], *, check: bool = True
) -> subprocess.CompletedProcess[bytes]:
    """Run a command, streaming stdout/stderr to the terminal."""
    return subprocess.run(list(args), check=check)


def process_file(path: Path) -> None:
    """Convert ``path`` to an ipynb, format it with Ruff, and write it back."""
    # Log which file we're processing to make failures easy to find in CI/hooks
    print(f"myst_markdown_ruff_hook: Formatting {path}", file=sys.stderr)
    if not path.exists():
        # File might have been deleted between lint selection and execution.
        return

    notebook = jupytext.read(path, fmt="myst")

    with tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        jupytext.write(notebook, tmp_path, fmt="ipynb")
        check_result = run_command((*RUF_CHECK_CMD, str(tmp_path)), check=False)
        run_command((*RUF_FORMAT_CMD, str(tmp_path)))
        formatted_notebook = jupytext.read(tmp_path)
        jupytext.write(formatted_notebook, path, fmt="myst")
        if check_result.returncode != 0:
            raise subprocess.CalledProcessError(
                check_result.returncode, check_result.args
            )
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Format MyST Markdown via Ruff.")
    parser.add_argument(
        "paths", nargs="+", help="Markdown files passed in by pre-commit."
    )
    args = parser.parse_args(argv)

    for raw_path in args.paths:
        path = Path(raw_path)
        try:
            process_file(path)
        except subprocess.CalledProcessError as exc:
            return exc.returncode
        except Exception as exc:  # noqa: BLE001 - surface the error in pre-commit
            print(f"Failed to format {path}: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
