# Enable inline plotting in the notebook
try:
    get_ipython().enable_matplotlib(gui='inline')
except NameError:
    pass

import sys
import os

module_dir = os.path.dirname("__file__")
sys.path.extend(module_dir)

import re

from IPython import display

# In order to keep it clear in the notebooks which imports are provided,
# add all the mooc-specific import statements to the following string.

imports = """
from __future__ import division, print_function
import numpy as np
import matplotlib
import kwant

import ipywidgets
from IPython.html.widgets import interact
from ipywidgets import StaticInteract, RangeWidget, DropDownWidget
from IPython.display import display_html
from matplotlib import pyplot as plt

import pfaffian as pf
from edx_components import *
"""

# Explicitly mention the mooc-related imports.
print("Performing the necessary imports.")
print(imports)
for line in imports.split('\n'):
    try:
        exec(line)
    except ImportError:
        print("Executing '{0}' failed.".format(line))

# Set plot style.
matplotlib.rc_file(os.path.join(module_dir, "matplotlibrc"))

# SimpleNamespace
class SimpleNamespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Adjust printing of matrices, and numpy printing of numbers.

def pprint_matrix(data, digits=3):
    """Print a numpy array as a latex matrix."""
    header = (r"\begin{{pmatrix}}"
              r"{d}\end{{pmatrix}}")
    d=data.__str__()[1:-1]
    d = d.replace(']', '')
    d = d.replace('\n', r'\\')
    d = re.sub(r' *\[ *', '', d)
    d = re.sub(r' +', ' & ', d)
    display.display_latex(display.Latex(header.format(d=d)))

def scientific_number(x):
    if not x:
        return '$0$'
    pot = int(np.log(abs(x)) / np.log(10.0)) - 1
    fac = x*10**(-pot)
    return '$%1.1f \cdot 10^{%1.0f}$' %(fac, pot)


def pretty_fmt_complex(num, digits=2):
    """Return a string representation of a number designed to be human-readable."""
    def strip_trailing(num_str):
        return num_str.rstrip('0').rstrip('.')

    if np.round(num, digits) == 0:
        return '0'

    if np.round(num.imag, digits) == 0:
        return strip_trailing(str(round(num.real, digits)))

    if np.round(num.real, digits) == 0:
        return strip_trailing(str(round(num.imag, digits))) + 'i'

    return (pretty_fmt_complex(num.real) + ('+' * (num.imag > 0)) +
            pretty_fmt_complex(num.imag) + 'i')

np.set_printoptions(precision=2, suppress=True, formatter={'complexfloat': pretty_fmt_complex})

nb_html_header = """
<script type=text/javascript>
/* Add a button for showing or hiding input */
on = "Show input";
off = "Hide input";
function onoff(){
  currentvalue = document.getElementById('onoff').value;
  if(currentvalue == off){
    document.getElementById("onoff").value=on;
      $('div.input').hide();
  }else{
    document.getElementById("onoff").value=off;
      $('div.input').show();
  }
}

/* Launch first notebook cell on start */
function launch_first_cell (evt) {
  if (!launch_first_cell.executed
      && IPython.notebook.kernel
  ) {
    IPython.notebook.get_cells()[0].execute();
    launch_first_cell.executed = true;
  }
}

$([IPython.events]).on('status_started.Kernel notebook_loaded.Notebook', launch_first_cell);
</script>

<p>Press this button to show/hide the code used in the notebook:
<input type="button" class="ui-button ui-widget ui-state-default \
ui-corner-all ui-button-text-only" value="Hide input" id="onoff" \
onclick="onoff();"></p>
"""

hide_outside_ipython = """<script type=text/javascript>
$(document).ready(function (){if(!("IPython" in window)){onoff();}})
</script>"""

# In order to make the notebooks readable through nbviewer we want to hide the
# code by default. However the same code is executed by the students, and in
# that case we don't want to hide the code. So we check if the code is executed
# by one of the mooc developers. Here we do by simply checking for some files that
# belong to the internal mooc repository, but are not published.
# This is a temporary solution, and should be improved in the long run.

if os.path.exists(os.path.join(module_dir, os.path.pardir, 'scripts')):
    nb_html_header += hide_outside_ipython

display_html(display.HTML(nb_html_header))

with open(os.path.join(module_dir, 'make_toc.js')) as f:
    js = f.read()
js += "$([IPython.events]).on('status_started.Kernel notebook_loaded.Notebook', table_of_contents);"
display.display_javascript(display.Javascript(js))
