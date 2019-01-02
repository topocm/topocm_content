import re
import os
from pathlib import Path

from ruamel.yaml import YAML
import jinja2


def expand_syllabus(toc, template, out):
    """Plug the TOC data into a syllabus template."""
    Path(out).write_text(
        jinja2.Template(Path(template).read_text())
        .render(chapters=YAML().load(Path(toc)))
    )


def main():
    course_materials = Path(os.environ['MARKDOWN'])
    toc = 'toc.yml'
    template = course_materials / 'syllabus.md.j2'
    out = course_materials / 'syllabus.md'
    expand_syllabus(toc, template, out)


if __name__ == '__main__':
    main()
