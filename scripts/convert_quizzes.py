#!/usr/bin/env python3
"""
Convert jupytext-markdown files to notebooks, execute quiz component cells, and
rewrite them as quiz directives in markdown.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import jupytext
import nbformat


QUIZ_CALL_PATTERN = re.compile(r"\b(mcq|checkbox|MultipleChoice|Checkboxes)\s*\(")


@dataclass
class QuizSpec:
    kind: str  # "multiple-choice" or "checkboxes"
    question: str
    answers: List[str]
    correct: List[int]
    explanation: str = ""


def looks_like_quiz_cell(source: str) -> bool:
    return bool(QUIZ_CALL_PATTERN.search(source))


def normalize_answers(raw: Sequence[object]) -> List[str]:
    return [str(item).strip() for item in raw]


def normalize_correct(raw: object) -> List[int]:
    if raw is None:
        return []
    if isinstance(raw, (list, tuple, set)):
        return [int(x) for x in raw]
    return [int(raw)]


def make_stub(recorder: List[QuizSpec], kind: str):
    def _stub(*args, **kwargs):
        question = kwargs.pop("question", None)
        answers = kwargs.pop("answers", None)
        correct = kwargs.pop(
            "correct", kwargs.pop("correct_answer", kwargs.pop("correct_answers", None))
        )
        explanation = kwargs.pop("explanation", kwargs.pop("explan", ""))

        if question is None and args:
            question = args[0]
        if answers is None and len(args) > 1:
            answers = args[1]
        if correct is None and len(args) > 2:
            correct = args[2]

        spec = QuizSpec(
            kind=kind,
            question=str(question or "").strip(),
            answers=normalize_answers(answers or []),
            correct=normalize_correct(correct),
            explanation=str(explanation or "").strip(),
        )
        recorder.append(spec)
        return spec

    return _stub


def run_quiz_cell(source: str, env: Dict[str, object]) -> List[QuizSpec]:
    captures: List[QuizSpec] = []
    env["mcq"] = make_stub(captures, "multiple-choice")
    env["checkbox"] = make_stub(captures, "checkboxes")
    env["MultipleChoice"] = make_stub(captures, "multiple-choice")
    env["Checkboxes"] = make_stub(captures, "checkboxes")

    try:
        exec(compile(source, "<quiz-cell>", "exec"), env, env)
    except Exception as exc:  # pragma: no cover - diagnostics only
        print(f"[quiz-convert] Failed to execute quiz cell: {exc}", file=sys.stderr)
        return []
    return captures


def render_directive(spec: QuizSpec) -> str:
    lines = [f"```{{{spec.kind}}} {spec.question}"]
    if spec.explanation:
        lines.append(f":explanation: {spec.explanation}")
    if spec.correct:
        lines.append(f":correct: {', '.join(str(idx) for idx in spec.correct)}")

    for answer in spec.answers:
        lines.append(f"- {answer}")
    lines.append("```")
    return "\n".join(lines)


def process_notebook(nb: nbformat.NotebookNode) -> tuple[nbformat.NotebookNode, int]:
    env: Dict[str, object] = {"__name__": "__main__"}
    new_cells = []
    quiz_count = 0

    def append_markdown(text: str):
        nonlocal new_cells
        if not text:
            return
        if new_cells and new_cells[-1].cell_type == "markdown":
            prev = new_cells[-1]
            merged = "\n\n".join(
                part for part in (prev.source.strip(), text.strip()) if part
            ).strip()
            prev.source = merged + ("\n" if merged else "")
        else:
            new_cells.append(nbformat.v4.new_markdown_cell(text))

    for cell in nb.cells:
        if cell.cell_type == "code" and looks_like_quiz_cell(cell.source):
            quizzes = run_quiz_cell(cell.source, env)
            if quizzes:
                rendered = "\n\n".join(render_directive(q) for q in quizzes)
                append_markdown(rendered)
                quiz_count += len(quizzes)
                continue
        if cell.cell_type == "markdown":
            append_markdown(cell.source)
        else:
            new_cells.append(cell)

    nb.cells = new_cells
    return nb, quiz_count


def is_jupytext_markdown(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return "jupytext:" in text.splitlines()[0:5]


def iter_markdown_files(root: Path) -> Iterable[Path]:
    skip_dirs = {"_build", "_static", ".pixi", ".git"}
    for path in root.rglob("*.md"):
        if any(part in skip_dirs or part.startswith(".") for part in path.parts):
            continue
        if is_jupytext_markdown(path):
            yield path


def convert_file(path: Path) -> int:
    nb = jupytext.read(path)
    nb_out, count = process_notebook(nb)
    if count:
        jupytext.write(nb_out, path, fmt="md")
    return count


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Specific markdown files or directories to process (defaults to repo root).",
    )
    args = parser.parse_args(argv)

    roots = args.paths or [Path(".")]
    total_quizzes = 0
    total_files = 0

    for root in roots:
        if root.is_dir():
            candidates = iter_markdown_files(root)
        else:
            candidates = (
                [root] if root.suffix == ".md" and is_jupytext_markdown(root) else []
            )

        for md_path in candidates:
            count = convert_file(md_path)
            if count:
                print(f"[quiz-convert] Updated {md_path} with {count} quiz(es).")
                total_files += 1
                total_quizzes += count

    print(
        f"[quiz-convert] Completed. Files changed: {total_files}, quizzes converted: {total_quizzes}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
