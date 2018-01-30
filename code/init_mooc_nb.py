# 1. Standard library imports
import datetime
import os
import re
import sys
import types

# 2. External package imports
import holoviews
from holoviews import Options, Store
from IPython import display
import kwant
import matplotlib
import numpy as np

# A bunch of functions and modules to pass on, we never use them here
from IPython.display import display_html
from matplotlib import pyplot as plt
import edx_components
from edx_components import *
import functions
from functions import *
import pfaffian as pf

init_mooc_nb = ['np', 'matplotlib', 'kwant', 'holoviews', 'init_notebook',
                'SimpleNamespace', 'pprint_matrix', 'scientific_number',
                'pretty_fmt_complex', 'plt', 'pf', 'display_html']

__all__ = init_mooc_nb + edx_components.__all__ + functions.__all__


class SimpleNamespace(types.SimpleNamespace):
    def update(self, **kwargs):
        self.__dict__.update(kwargs)
        return self


# Adjust printing of matrices, and numpy printing of numbers.
def pprint_matrix(data, digits=3):
    """Print a numpy array as a latex matrix."""
    header = (r"\begin{{pmatrix}}"
              r"{d}\end{{pmatrix}}")
    d = data.__str__()[1:-1]
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
    return '$%1.1f \cdot 10^{%1.0f}$' % (fac, pot)


def pretty_fmt_complex(num, digits=2):
    """Return a human-readable string representation of a number."""
    num = np.round(num, digits)

    if num == 0:
        return '0'

    parts = (str(part).rstrip('0').rstrip('.')
             for part in (num.real, num.imag) if part)
    return '+'.join(parts) + ('i' if num.imag else '')


def print_information():
    print('Populated the namespace with:\n' +
          ', '.join(init_mooc_nb) +
          '\nfrom code/edx_components:\n' +
          ', '.join(edx_components.__all__) +
          '\nfrom code/functions:\n' +
          ', '.join(functions.__all__))

    print('Using kwant {} and holoviews {}'.format(
          kwant.__version__, holoviews.__version__))

    now = datetime.datetime.now()
    print('Executed on {} at {}.'.format(now.date(), now.time()))


def check_versions():
    from distutils.version import LooseVersion

    if sys.version_info < (3, 5):
        raise Exception('Install Python 3.5 or higher, we recommend using conda.')

    if tuple(LooseVersion(str(holoviews.__version__)).version) < (1, 7):
        raise Exception('Install holoviews 1.7 or higher. If you are using conda, do: `conda install -c conda-forge holoviews`')

    if tuple(LooseVersion(str(kwant.__version__)).version) < (1, 3):
        raise Exception('Install kwant 1.3 or higher. If you are using conda, do: `conda install -c conda-forge kwant`')


def init_notebook():
    print_information()
    check_versions()

    code_dir = os.path.dirname(os.path.realpath(__file__))
    hv_css = os.path.join(code_dir, 'hv_widgets_settings.css')
    holoviews.plotting.widgets.SelectionWidget.css = hv_css

    holoviews.notebook_extension('matplotlib')

    # Enable inline plotting in the notebook
    get_ipython().enable_matplotlib(gui='inline')

    Store.renderers['matplotlib'].fig = 'svg'
    Store.renderers['matplotlib'].dpi = 100

    holoviews.plotting.mpl.MPLPlot.fig_rcparams['text.usetex'] = True

    latex_packs = [r'\usepackage{amsmath}',
                   r'\usepackage{amssymb}'
                   r'\usepackage{bm}']

    holoviews.plotting.mpl.MPLPlot.fig_rcparams['text.latex.preamble'] = \
        latex_packs

    # Set plot style.
    options = Store.options(backend='matplotlib')
    options.Contours = Options('style', linewidth=2, color='k')
    options.Contours = Options('plot', aspect='square')
    options.HLine = Options('style', linestyle='--', color='b', linewidth=2)
    options.VLine = Options('style', linestyle='--', color='r', linewidth=2)
    options.Image = Options('style', cmap='RdBu_r')
    options.Image = Options('plot', title_format='{label}')
    options.Path = Options('style', linewidth=1.2, color='k')
    options.Path = Options('plot', aspect='square', title_format='{label}')
    options.Curve = Options('style', linewidth=2, color='k')
    options.Curve = Options('plot', aspect='square', title_format='{label}')
    options.Overlay = Options('plot', show_legend=False, title_format='{label}')
    options.Layout = Options('plot', title_format='{label}')
    options.Surface = Options('style', cmap='RdBu_r', rstride=2, cstride=2,
                              lw=0.2, edgecolors='k')
    options.Surface = Options('plot', azimuth=20, elevation=8)

    # Set slider label formatting
    for dimension_type in [float, np.float64, np.float32]:
        holoviews.Dimension.type_formatters[dimension_type] = pretty_fmt_complex

    matplotlib.rc_file(os.path.join(code_dir, "matplotlibrc"))

    np.set_printoptions(precision=2, suppress=True,
                        formatter={'complexfloat': pretty_fmt_complex})
