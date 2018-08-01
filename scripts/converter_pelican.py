#!/usr/bin/env python3

import os
import glob
import json
import shutil
import datetime
from itertools import dropwhile
import re

import nbformat


def notebook_title(nb: nbformat.NotebookNode):
    first_text_cell = next(
        cell for cell in nb.cells if cell.cell_type == 'markdown'
    )
    try:
        return re.search('# (.*)', first_text_cell.source).group(1)
    except AttributeError as e:
        raise RuntimeError('Notebook has no title') from e


meta_file = """Title: {title}
Slug: {slug}
Date: {date}
Category: """

date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

ipynbs = glob.glob('generated/with_output/w*/*.ipynb')
figures = glob.glob('generated/with_output/w*/figures/*')


# Copy ipynbs and create meta data files
for ipynb in ipynbs:
    nb = nbformat.read(ipynb, as_version=4)
    nb.metadata['name'] = title = notebook_title(nb)

    # Remove initialization cells
    nb.cells = list(dropwhile((lambda cell: cell.type == 'code'), nb.cells))

    new_fname = ipynb.replace('generated/with_output',
                              'generated/pelican_content')
    os.makedirs(os.path.dirname(new_fname), exist_ok=True)
    with open(new_fname, 'w') as f:
        json.dump(nb, f)
    with open(new_fname + '-meta', 'w', encoding='utf-8') as f:
        slug = ipynb.replace(
            'generated/with_output/', '').replace('.ipynb', '')
        f.write(meta_file.format(slug=slug, title=title, date=date))


# Copy figures
for figure in figures:
    new_fname = figure.replace('with_output', 'html')
    os.makedirs(os.path.dirname(new_fname), exist_ok=True)
    shutil.copyfile(figure, new_fname)


# Copy syllabus
nb = nbformat.read('generated/with_output/syllabus.ipynb', as_version=4)
with open('generated/pelican_content/syllabus.ipynb', 'w') as f:
    json.dump(nb, f)
with open('generated/pelican_content/syllabus.ipynb-meta', 'w',
          encoding='utf-8') as f:
    meta = meta_file.format(slug='syllabus', title='Syllabus', date=date)
    f.write(meta + '\nsave_as: index.html')
