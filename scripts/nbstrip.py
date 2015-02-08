#!/usr/bin/env python
"""Opens a notebook, removes prompt numbers and writes the modified version to the original file.

Useful mainly as a git pre-commit hook.
"""
 
import sys
 
from IPython.nbformat import current
 
def strip_output(nb):
    """strip the outputs from a notebook object"""
    nb.metadata.pop('signature', None)
    for cell in nb.worksheets[0].cells:
        if 'outputs' in cell:
            for output in cell['outputs']:
                output.pop('prompt_number', None)
        cell.pop('prompt_number', None)
    return nb
 
if __name__ == '__main__':
    nb = current.read(sys.stdin, 'json')
    nb = strip_output(nb)
    current.write(nb, sys.stdout, 'json')
