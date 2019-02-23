#!/usr/bin/env python3

import os
import datetime
import glob
import shutil
from pathlib import Path

from nbconvert import HTMLExporter
from nbconvert.filters.markdown import markdown2html_pandoc
from ruamel.yaml import YAML

from converter import split_into_units, url

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

exportHtml = HTMLExporter(config={
    'HTMLExporter': {
        'template_file': 'ocw',
        'template_path': ['.', str(Path(__file__).parent)],
        'filters': {'markdown2html': markdown2html_pandoc}
    }
})

# Mooc content location
mooc_folder = Path(__file__).parent.parent
output_dir = mooc_folder / 'generated/html/ocw'
generated_ipynbs = mooc_folder / 'generated/with_output'

# Loading data from syllabus
syllabus_nb = generated_ipynbs / 'syllabus.ipynb'
chapters = YAML().load(Path(mooc_folder / 'toc.yml').read_text())

for chapter in chapters:
    for section in chapter['sections']:
        notebook = generated_ipynbs / (section['location'] + '.ipynb')
        units = split_into_units(notebook)
        folder, fname = notebook.parent, notebook.name
        for i, unit in enumerate(units):
            fname = fname.replace('.ipynb', '')
            new_fname = f'{fname}_{i}'
            new_path = mooc_folder / output_dir / folder / (new_fname + '.html')
            new_path.parent.mkdir(exist_ok=True)
            new_path.write_text(exportHtml.from_notebook_node(unit)[0])

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
