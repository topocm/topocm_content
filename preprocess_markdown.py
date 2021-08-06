import os
import re
from pathlib import Path

from jinja2 import Template

from publist.publist import update as update_publist
from ruamel.yaml import YAML

PREPRINT_REGEX = r"arXiv:(.+?[/\.]\d+)"
FULL_TEMPLATE = Template(
    """{{preprint.title}} ([arXiv:{{preprint.id}}](https://arxiv.org/abs/{{preprint.id}}))

{{preprint.authors | join(', ')}}

> {{preprint.abstract}}"""
)
SHORT_TEMPLATE = Template(
    """**{{preprint.title}}** ([arXiv:{{preprint.id}}](https://arxiv.org/abs/{{preprint.id}}))
  {{preprint.authors | join(', ')}}"""
)
INLINE_TEMPLATE = Template(
    '[arXiv:{{preprint.id}}](https://arxiv.org/abs/{{preprint.id}} "{{preprint.title}}")'
)


def expand_syllabus(toc, template, out):
    """Plug the TOC data into a syllabus template."""
    Path(out).write_text(
        Template(Path(template).read_text()).render(chapters=YAML().load(Path(toc)))
    )


def update_bibliography(bibliography, source_path):
    """Find all arxiv references and update bibliography from them."""
    prerpints = sum(
        (
            re.findall(re.compile(PREPRINT_REGEX), document.read_text())
            for document in Path(source_path).glob("**/*.md")
        ),
        [],
    )

    update_publist.callback(
        output=bibliography,
        update=False,
        author_id=[],
        preprint_id=prerpints,
        email="crossref@antonakhmerov.org",
        silent=False,
        overwrite=True,
    )


def expand_refs(bibliography, source_path):
    refs = YAML().load(Path(bibliography))
    refs = {ref["id"]: ref for ref in refs}

    def replace(match):
        if match.group(1) == "### ":
            template = FULL_TEMPLATE
        elif match.group(1) == "* ":
            template = SHORT_TEMPLATE
        else:
            template = INLINE_TEMPLATE
        return match.group(1) + template.render(preprint=refs[match.group(2)])

    for document in Path(source_path).glob("**/*.md"):
        modified = re.sub(
            r"(### |\* |[^#*] )" + PREPRINT_REGEX, replace, document.read_text()
        )
        document.write_text(modified)


def main():
    course_materials = Path(os.environ["MARKDOWN"])
    toc = "toc.yml"
    template = course_materials / "syllabus.md.j2"
    out = course_materials / "syllabus.md"
    expand_syllabus(toc, template, out)
    update_bibliography("bibliography.yml", course_materials)
    expand_refs("bibliography.yml", course_materials)


if __name__ == "__main__":
    main()
