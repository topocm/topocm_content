"""
   The script takes an .ipynb file (or all such files in the directory), and,
   if it doesn't already have a corresponding .py file, creates it from the
   .ipynb file. We do this because we don't want to version-control .ipynb files
   (which can contain images, matrices, data frames, etc), but we do want to
   save the content of the notebook cells.

   This is intented to be a replacement of the deprecated

   ipython notebook --script

   command for Ipython 2 notebooks that automatically saved notebooks as .py
   files that can be version controled.

   Optionally, the first three functions can be used for post-hook autosave in
   the ipython_notebook_config.py file.

   Call this script with argument "-f" to create a .py file from  notebook:

   python notebook_v4_to_py.py -f filename.ipynb

   Call the script with argument "--overwrite" to overwrite existing .py files.

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

def get_notebook_data(path_to_file):
    with open(path_to_file, 'r') as notebook:
        notebook_data = json.load(notebook)
    return notebook_data

def construct_output_py_file_path(input_file_path, skip_if_exists=True):
    input_headless, ext = os.path.splitext(input_file_path)
    assert ext=='.ipynb'
    output_by_path = input_headless + '.py'
    if os.path.exists(output_by_path) and skip_if_exists:
        return
    return output_by_path

def write_notebook_data_to_py(notebook_data, out_file_path):
    with open(out_file_path, 'w') as output:
        output.write('# -*- coding: utf-8 -*-\n')
        output.write('# <nbformat>' + str(notebook_data['nbformat']) + '</nbformat>\n')
        try:
            cells = notebook_data['cells']
        except KeyError:
            print(("Nbformat is " + str(notebook_data['nbformat']) + ", try the old converter script."))
            return

        for cell in cells:
            if cell['cell_type'] in ['code', 'markdown']:
                output.write('\n')
                output.write('# <' + cell['cell_type'] + 'cell' + '>\n')
                output.write('\n')
                for item in cell['source']:
                    if cell['cell_type']=='code':
                        output.write(item)
                    else:
                        output.write('# ')
                        output.write(item)
                output.write('\n')

def convert_notebook_to_py(input_file_path, skip_if_exists=True):
    output_file_path = construct_output_py_file_path(input_file_path, skip_if_exists)
    if output_file_path is not None:
        notebook_data = get_notebook_data(input_file_path)
        write_notebook_data_to_py(notebook_data, output_file_path)

def convert_all_notebook_to_py(directory, skip_if_exists=True):
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.ipynb'):
            filename = os.path.abspath(os.path.join(root, filename))
            print(filename)
            if filename != THIS_FILE:
                convert_notebook_to_py(filename, skip_if_exists)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-w', '--overwrite', action='store_true', help='Overwrite existing py files', default=False)
    parser.add_argument('-f', '--file', help='Specify an Ipython notebook if you only want to convert one. '
                                       '(This will overwrite default.)')
    args = parser.parse_args()

    if args.file is not None:
        convert_notebook_to_py(args.file, skip_if_exists=not args.overwrite)
    else:
        convert_all_notebook_to_py(directory='.', skip_if_exists=not args.overwrite)
