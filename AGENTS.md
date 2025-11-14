# Course on topology in condensed matter

This repository contains materials for a course on topology in condensed matter physics.

The course materials are stored in w<number>_<topic> directories in myst markdown format.

The course uses recently released Jupyter Book 2 that is built on top of the mystmd package. If you need the docs, see https://jupyterbook.org/stable/ and https://mystmd.org/.

The course uses pixi for environment management. If you need the docs, see https://pixi.sh/latest/.

To build the book, run `pixi run jupyter book build`. This is computationally intensive, so do it sparingly.

To execute a single notebook for testing, run `pixi run jupytext --execute --to notebook path/to/file.md`.