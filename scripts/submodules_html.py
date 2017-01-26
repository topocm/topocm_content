#!/usr/bin/env python3

import os
from traitlets.config import Config
from nbconvert import HTMLExporter
from nbconvert.filters.markdown import markdown2html_pandoc
from converter import (parse_syllabus,
                       split_into_units,
                       scripts_path,
                       export_unit_to_html,
                       save_html,
                       mooc_folder)

cfg = Config({'HTMLExporter': {'template_file': 'edx',
                               'template_path': ['.', scripts_path],
                               'filters': {'markdown2html':
                                           markdown2html_pandoc}}})

exportHtml = HTMLExporter(config=cfg)

# Mooc content location
output_dir = os.path.join(mooc_folder, 'generated/html/ocw')

# Loading data from syllabus
syllabus_nb = os.path.join(mooc_folder, 'generated/with_output/syllabus.ipynb')
data = parse_syllabus(syllabus_nb, mooc_folder, parse_all=False)

# saving syllabus
syllabus = split_into_units(syllabus_nb)[0]

for chapter in data.chapters:
    chap_num = int(chapter.url[-2:])
    for sequential in chapter.sequentials:
        units = split_into_units(sequential.source_notebook)
        folder, fname = sequential.source_notebook.split('/')[-2:]
        for i, unit in enumerate(units):
            new_fname = fname.replace('.ipynb', '{}_{}.html'.format(fname, i))
            new_path = os.path.join(mooc_folder, output_dir, folder, new_fname)
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            html = export_unit_to_html(unit, exportHtml)
            save_html(html, new_path)
