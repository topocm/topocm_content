import os
import re
from pathlib import Path
from functools import cache

from jinja2 import Template

from publist.publist import update as update_publist
from ruamel.yaml import YAML
import sphinx
import myst_nb

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


@cache
def read_refs(bibliography):
    refs = YAML().load(Path(bibliography))
    return {ref["id"]: ref for ref in refs}


def replace_refs(app, docname, source):
    refs = read_refs("bibliography.yml")

    def replace(match):
        if match.group(1) == "### ":
            template = FULL_TEMPLATE
        elif match.group(1) == "* ":
            template = SHORT_TEMPLATE
        else:
            template = INLINE_TEMPLATE
        return match.group(1) + template.render(preprint=refs[match.group(2)])

    source[0] = re.sub(r"(### |\* |[^#*] )" + PREPRINT_REGEX, replace, source[0])


class RemoveAllInputs(sphinx.transforms.Transform):
    default_priority = 210

    def apply(self):
        for node in self.document.traverse(myst_nb.nodes.CellInputNode):
            node.parent.remove(node)


def setup(app):
    app.connect("source-read", replace_refs)
    app.add_transform(RemoveAllInputs)

    return {
        'version': '0.0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }