#!/usr/bin/env python3

import os
import glob
import shutil
from traitlets.config import Config
from nbconvert import HTMLExporter
from nbconvert.filters.markdown import markdown2html_pandoc
from converter import (parse_syllabus,
                       split_into_units,
                       scripts_path,
                       export_unit_to_html,
                       save_html,
                       mooc_folder)

cfg = Config({'HTMLExporter': {'template_file': 'ocw',
                               'template_path': ['.', scripts_path],
                               'filters': {'markdown2html':
                                           markdown2html_pandoc}}})

exportHtml = HTMLExporter(config=cfg)

# Mooc content location
output_dir = os.path.join(mooc_folder, 'generated/html/ocw')
generated_ipynbs = os.path.join(mooc_folder, 'generated/with_output')

# Loading data from syllabus
syllabus_nb = os.path.join(generated_ipynbs, 'syllabus.ipynb')
data = parse_syllabus(syllabus_nb, generated_ipynbs, parse_all=True)

# saving syllabus
syllabus = split_into_units(syllabus_nb)[0]

for chapter in data.chapters:
    chap_num = int(chapter.url[-2:])
    for sequential in chapter.sequentials:
        units = split_into_units(sequential.source_notebook,
                                 include_header=False)
        folder, fname = sequential.source_notebook.split('/')[-2:]
        for i, unit in enumerate(units):
            fname = fname.replace('.ipynb', '')
            new_fname = '{}_{}.html'.format(fname, i)
            new_path = os.path.join(mooc_folder, output_dir, folder, new_fname)
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            html = export_unit_to_html(unit, exportHtml)
            save_html(html, new_path)

# Copy figures
figures = glob.glob(os.path.join(generated_ipynbs, 'w*/figures/*'))
for figure in figures:
    new_fname = figure.replace('with_output', 'html/ocw')
    os.makedirs(os.path.dirname(new_fname), exist_ok=True)
    shutil.copyfile(figure, new_fname)
