#!/usr/bin/env python
"""Opens a notebook, removes prompt numbers and writes the modified version to the original file.

Useful mainly as a git pre-commit hook.
"""
 
import sys
from IPython.nbformat import current
from IPython.nbformat.sign import NotebookNotary
 
def trust(nb):
    """Sign a given notebook object"""
    notary = NotebookNotary()
    notary.sign(nb)
    return nb
 
if __name__ == '__main__':
    nb = current.read(sys.stdin, 'json')
    nb = trust(nb)
    current.write(nb, sys.stdout, 'json')
