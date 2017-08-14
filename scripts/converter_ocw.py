#!/usr/bin/env python3

import os
import datetime
import glob
import shutil
from traitlets.config import Config
from nbconvert import HTMLExporter
from nbconvert.filters.markdown import markdown2html_pandoc
from converter import (export_unit_to_html,
                       mooc_folder,
                       parse_syllabus,
                       save_html,
                       scripts_path,
                       split_into_units,
                       url)

IFRAME_TEMPLATE = r"""
<iframe id="{id}" scrolling="no" width="100%" height="600px", frameborder=0>
Your browser does not support IFrames.
</iframe>

<script>
var iframe = document.getElementById('{id}');
iframe.src =  "//"+ "topocondmat.org/ocw/{folder}/{name}.html?date=" + (+ new Date());
</script>

<script src="{url}"></script>

<script>
var isOldIE = (navigator.userAgent.indexOf("MSIE") !== -1); // Detect IE10 and below
iFrameResize({{
    heightCalculationMethod: isOldIE ? 'max' : 'lowestElement',
    minSize:100,
    log:true,
    checkOrigin:false
    }}, "#{id}");
</script>
"""

with open('website_assets/iframes.txt', 'w') as f:
    now = datetime.datetime.now()
    print('Executed on {} at {}.'.format(now.date(), now.time()), file=f)

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
            new_fname = '{}_{}'.format(fname, i)
            new_path = os.path.join(mooc_folder, output_dir, folder, new_fname + '.html')
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            html = export_unit_to_html(unit, exportHtml)
            save_html(html, new_path)

            with open('website_assets/iframes.txt', 'a') as f:
                ID = '{}_{}'.format(folder, new_fname)
                print(IFRAME_TEMPLATE.format(
                    id=ID, url=url, folder=folder, name=new_fname), file=f)
                print(4 * '\n', file=f)  # print some new lines

# Copy figures
figures = glob.glob(os.path.join(generated_ipynbs, 'w*/figures/*'))
for figure in figures:
    new_fname = figure.replace('with_output', 'html/ocw')
    os.makedirs(os.path.dirname(new_fname), exist_ok=True)
    shutil.copyfile(figure, new_fname)
