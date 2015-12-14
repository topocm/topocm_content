"""
   This script converts a .py file to Ipython v4 notebook format. The .py file
   must be a result of an Ipython -> .py conversion using the notebook_v4_to_py.py
   script or the automatic post-hook save in Ipyhon 3 based on that script.
   In this way the version controlled .py files can be converted back to Ipython
   notebook format.

   Call this script with argument "-f" to create an .ipynb file from a .py file:

   python py_to_notebook_v4.py -f filename.py

   Call the script with argument "--overwrite" to overwrite existing .ipynb files.

   Call the script with argument "--dry-run" to simulate (print) what would happen.

   Date: 07. August 2015.
   #############################################################################

   This script is released under the MIT License

   Copyright (c) 2015 Balabit SA

   Permission is hereby granted, free of charge, to any person obtaining a copy of
   this software and associated documentation files (the "Software"), to deal in
   the Software without restriction, including without limitation the rights to use,
   copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
   Software, and to permit persons to whom the Software is furnished to do so,
   subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
   INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
   PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
   HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
   ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
   WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sys
import json
import os
import fnmatch

reload(sys)
sys.setdefaultencoding('utf8')
THIS_FILE = os.path.abspath(__file__)

def get_py_data(path_to_file):
    with open(path_to_file, 'r') as pythonfile:
        lines = pythonfile.readlines()
    return lines

def construct_output_ipynb_file_path(input_file_path, skip_if_exists=True):
    input_headless, ext = os.path.splitext(input_file_path)
    assert ext=='.py'
    output_by_path = input_headless + '.ipynb'
    if os.path.exists(output_by_path) and skip_if_exists:
        return
    return output_by_path

def build_notebook_cells(lines):
    def close_cell(current_cell):
        if current_cell in ['markdown', 'code']:
            if not last_cell and len(source) > 1:
                del source[-1:]
            source[-1] = source[-1].rstrip('\n')
            cell['source'] = source
            outputcells.append(cell)
        return outputcells

    def open_cell(line, execution_count):
        if '<markdowncell>' in line:
            cell = {'cell_type': 'markdown',
                    'metadata': {}}
            source = []
            current_cell = 'markdown'
        elif '<codecell>' in line:
            cell = {'cell_type': 'code',
                    'execution_count': execution_count,
                    'metadata': {'collapsed': False},
                    'outputs': []}
            source = []
            current_cell = 'code'
        return cell, source, current_cell

    current_cell = 'unknown'
    execution_count = 1
    skip_one_line = False
    last_cell = False
    outputcells = []

    for line in lines:
        if skip_one_line:
            skip_one_line = False
            continue

        if line=='# <markdowncell>\n' or line=='# <codecell>\n':
            outputcells = close_cell(current_cell)
            if current_cell=='code':
                execution_count += 1
            cell, source, current_cell = open_cell(line, execution_count)
            skip_one_line = True
            continue

        if current_cell=='markdown':
            if len(line) > 1:
                source.append(line[2:])
            else:
                source.append(line)
        elif current_cell=='code':
            source.append(line)

    last_cell = True
    outputcells = close_cell(current_cell)
    return outputcells

def create_initial_output(lines):
    kernelspec = {'display_name': 'Python 2',
                  'language': 'python',
                  'name': 'python2'}
    language_info = {'codemirror_mode': {'name': 'ipython', 'version': 2},
                     'file_extension': '.py',
                     'mimetype': 'text/x-python',
                     'name': 'python',
                     'nbconvert_exporter': 'python',
                     'pygments_lexer': 'ipython2',
                     'version': '2.7.10'}
    metadata = {'kernelspec': kernelspec,
                'language_info': language_info}
    nbformat_minor = 0

    if '<nbformat>' in lines[1]:
        nbformat = lines[1].split('>')[1].split('<')[0]
        try:
            nbformat = int(nbformat)
        except ValueError:
            nbformat = float(nbformat)
    else:
        return

    output = {'metadata': metadata,
              'nbformat': nbformat,
              'nbformat_minor': nbformat_minor}
    return output

def write_py_data_to_notebook(output, out_file_path):
    with open(out_file_path, 'w') as outfile:
        json.dump(output, outfile)

def convert_py_to_notebook(input_file_path, skip_if_exists=True, dry_run=False):
    output_file_path = construct_output_ipynb_file_path(input_file_path, skip_if_exists)
    if output_file_path is not None:
        py_data = get_py_data(input_file_path)
        if len(py_data) > 1:
            output = create_initial_output(py_data)
            if output is not None:
                outputcells = build_notebook_cells(py_data)
                output['cells'] = outputcells
                if not dry_run:
                    write_py_data_to_notebook(output, output_file_path)
                print(("Created Ipython Jupyter notebook file: {}".format(output_file_path)))

def convert_all_py_to_notebook(directory, skip_if_exists=True, dry_run=False):
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.py'):
            filename = os.path.abspath(os.path.join(root, filename))
            print(filename)
            if filename != THIS_FILE:
                convert_py_to_notebook(filename, skip_if_exists=skip_if_exists, dry_run=dry_run)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-w', '--overwrite', action='store_true', help='Overwrite existing py files', default=False)
    parser.add_argument('-f', '--file', help='Specify an Ipython notebook if you only want to convert one. '
                                       '(This will overwrite default.)')
    parser.add_argument('--dry-run', action='store_true', help='Only prints what would happen', default=False)
    args = parser.parse_args()

    if args.file is not None:
        convert_py_to_notebook(args.file, skip_if_exists=not args.overwrite, dry_run=args.dry_run)
    else:
        convert_all_py_to_notebook(directory='.', skip_if_exists=not args.overwrite, dry_run=args.dry_run)
