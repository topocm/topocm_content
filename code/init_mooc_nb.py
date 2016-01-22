import sys
import os
import re
from types import SimpleNamespace

# Enable inline plotting in the notebook
try:
    get_ipython().enable_matplotlib(gui='inline')
except NameError:
    pass

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from IPython import display
from ipywidgets import interact
from IPython.display import display_html
import kwant

import pfaffian as pf
# A bunch of edx components to pass on, we never use them here
import edx_components
from edx_components import *


__all__ = ['np', 'matplotlib', 'kwant',
           'init_notebook', 'interact', 'display_html', 'plt','pf',
           'SimpleNamespace', 'pprint_matrix', 'scientific_number',
           'pretty_fmt_complex'] + edx_components.__all__


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
    """Return a human-readable string representation of a number."""
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
      && Jupyter.notebook.kernel
  ) {
    Jupyter.notebook.get_cells()[0].execute();
    launch_first_cell.executed = true;
  }
}

$([Jupyter.events]).on('status_started.Kernel notebook_loaded.Notebook', launch_first_cell);
</script>

<p>Press this button to show/hide the code used in the notebook:
<input type="button" class="ui-button ui-widget ui-state-default \
ui-corner-all ui-button-text-only" value="Hide input" id="onoff" \
onclick="onoff();"></p>
"""

hide_outside_ipython = """<script type=text/javascript>
$(document).ready(function (){if(!("IPython" in window)){onoff();}})
</script>"""


def init_notebook():
    print('Populated the namespace with:\n' + ', '.join(__all__))

    # Set plot style.
    module_dir = os.path.dirname(__file__)
    matplotlib.rc_file(os.path.join(module_dir, "matplotlibrc"))

    np.set_printoptions(precision=2, suppress=True,
                        formatter={'complexfloat': pretty_fmt_complex})

    # In order to make the notebooks readable through nbviewer we want to hide
    # the code by default. However the same code is executed by the students,
    # and in that case we don't want to hide the code. So we check if the code
    # is executed by one of the mooc developers. Here we do by simply checking
    # for some files that belong to the internal mooc repository, but are not
    # published.  This is a temporary solution, and should be improved in the
    # long run.

    developer = os.path.exists(os.path.join(module_dir, os.path.pardir,
                                            'scripts'))

    display_html(display.HTML(nb_html_header +
                              (hide_outside_ipython if developer else '')))
