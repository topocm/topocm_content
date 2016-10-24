#!/usr/bin/env python3

import os
import glob
import json
import shutil
import subprocess
import nbformat
import datetime


def remove_first_cell(nb_name):
    """Remove the cells until a cell starts with `# `."""
    nb = nbformat.read(nb_name, as_version=4)
    cells = nb.cells[1:]  # Always skip the first cell
    for i, cell in enumerate(cells):
        if cell['source'].startswith('# '):
            break
    cells = cells[i:]
    return nbformat.v4.new_notebook(cells=cells, metadata={'name': cells[0].source[2:]})


meta_file = """Title: Topocondmat.org: {title}
Slug: {slug}
Date: {date}
Category: """

date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

ipynbs = glob.glob('generated/with_output/w*/*.ipynb')
figures = glob.glob('generated/with_output/w*/figures/*')

try:
    shutil.rmtree('generated/pelican_content')
    os.makedirs('generated/pelican_content', exist_ok=True)
except:
    pass

try:
    shutil.rmtree('generated/html/')
except:
    pass

# Copy ipynbs and create meta data files
for ipynb in ipynbs:
    nb = remove_first_cell(ipynb)
    title = nb.cells[0].source[2:]
    new_fname = ipynb.replace('generated/with_output/', 'generated/pelican_content/')
    os.makedirs(os.path.dirname(new_fname), exist_ok=True)
    with open(new_fname, 'w') as f:
        json.dump(nb, f)
    with open(new_fname + '-meta', 'w', encoding='utf-8') as f:
        slug = ipynb.replace(
            'generated/with_output/', '').replace('.ipynb', '').replace('/', '-')
        f.write(meta_file.format(slug=slug, title=title, date=date))


# Copy figures
for figure in figures:
    new_fname = 'generated/html/figures/' + os.path.basename(figure)
    os.makedirs(os.path.dirname(new_fname), exist_ok=True)
    shutil.copyfile(figure, new_fname)


# Copy syllabus
nb = remove_first_cell('syllabus.ipynb')
nb['cells'][1]['source'] = nb['cells'][1][
    'source'].replace('/', '-').replace('.ipynb', '.html')
with open('generated/pelican_content/syllabus.ipynb', 'w') as f:
    json.dump(nb, f)
with open('generated/pelican_content/syllabus.ipynb-meta', 'w', encoding='utf-8') as f:
    f.write(meta_file.format(slug='syllabus', title='Syllabus', date=date))
