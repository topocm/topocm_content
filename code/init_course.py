# 1. Standard library imports
import datetime
import os
import re
import sys
import types
import warnings

# 2. External package imports
import holoviews
import kwant
import matplotlib
import numpy as np
from holoviews import Options, Store
from IPython import display

# A bunch of functions and modules to pass on, we never use them here
from IPython.display import display_html
from matplotlib import pyplot as plt

import components
import functions
from pfapack import pfaffian as pf
from components import *
from functions import *

init_course = [
    "np",
    "matplotlib",
    "kwant",
    "holoviews",
    "init_notebook",
    "pprint_matrix",
    "scientific_number",
    "pretty_fmt_complex",
    "plt",
    "pf",
    "display_html",
]

__all__ = init_course + components.__all__ + functions.__all__


# Adjust printing of matrices, and numpy printing of numbers.
def pprint_matrix(data, digits=3):
    """Print a numpy array as a latex matrix."""
    header = r"\begin{{pmatrix}}" r"{d}\end{{pmatrix}}"
    d = data.__str__()[1:-1]
    d = d.replace("]", "")
    d = d.replace("\n", r"\\")
    d = re.sub(r" *\[ *", "", d)
    d = re.sub(r" +", " & ", d)
    display.display_latex(display.Latex(header.format(d=d)))


def scientific_number(x):
    if not x:
        return "$0$"
    pot = int(np.log(abs(x)) / np.log(10.0)) - 1
    fac = x * 10 ** (-pot)
    return fr"${fac:1.1f} \cdot 10^{{{pot:1.0f}}}$"


def pretty_fmt_complex(num, digits=2):
    """Return a human-readable string representation of a number."""
    num = np.round(num, digits)

    if num == 0:
        return "0"

    parts = (str(part).rstrip("0").rstrip(".") for part in (num.real, num.imag) if part)
    return "+".join(parts) + ("i" if num.imag else "")


def print_information():
    print(
        "Populated the namespace with:\n"
        + ", ".join(init_course)
        + "\nfrom code/components:\n"
        + ", ".join(components.__all__)
        + "\nfrom code/functions:\n"
        + ", ".join(functions.__all__)
    )

    print(
        "Using kwant {} and holoviews {}".format(
            kwant.__version__, holoviews.__version__
        )
    )

    now = datetime.datetime.now()
    print("Executed on {} at {}.".format(now.date(), now.time()))


def check_versions():
    from distutils.version import LooseVersion

    if sys.version_info < (3, 5):
        raise Exception("Install Python 3.5 or higher, we recommend using conda.")

    if tuple(LooseVersion(str(holoviews.__version__)).version) < (1, 7):
        raise Exception(
            "Install holoviews 1.7 or higher. If you are using conda, do: `conda install -c conda-forge holoviews`"
        )

    if tuple(LooseVersion(str(kwant.__version__)).version) < (1, 3):
        raise Exception(
            "Install kwant 1.3 or higher. If you are using conda, do: `conda install -c conda-forge kwant`"
        )


def init_notebook():
    print_information()
    check_versions()

    holoviews.notebook_extension("matplotlib")
    holoviews.output(widget_location='bottom')

    # Enable inline plotting in the notebook
    get_ipython().enable_matplotlib(gui="inline")

    Store.renderers["matplotlib"].fig = "svg"
    Store.renderers["matplotlib"].dpi = 100

    holoviews.plotting.mpl.MPLPlot.fig_rcparams["text.usetex"] = False

    latex_packs = "\\usepackage{amsmath}\n\\usepackage{amssymb}\n\\usepackage{bm}"

    holoviews.plotting.mpl.MPLPlot.fig_rcparams["text.latex.preamble"] = latex_packs

    # Set plot style.
    options = Store.options(backend="matplotlib")
    options.Contours = Options("style", linewidth=2, color="k")
    options.Contours = Options("plot", padding=0, aspect="square")
    options.HLine = Options("style", linestyle="--", color="b", linewidth=2)
    options.VLine = Options("style", linestyle="--", color="r", linewidth=2)
    options.Image = Options("style", cmap="RdBu_r")
    options.Image = Options("plot", padding=0, title="{label}")
    options.Path = Options("style", linewidth=1.2, color="black")
    options.Path = Options("plot", padding=0, aspect="square", title="{label}")
    options.Curve = Options("style", linewidth=2, color="black")
    options.Curve = Options("plot", padding=0, aspect="square", title="{label}")
    options.Overlay = Options("plot", padding=0, show_legend=False, title="{label}")
    options.Layout = Options("plot", tight=True)
    options.Surface = Options(
        "style", cmap="RdBu_r", rstride=2, cstride=2, lw=0.2, edgecolor="black"
    )
    options.Surface = Options("plot", azimuth=20, elevation=8)

    # Set slider label formatting
    for dimension_type in [float, np.float64, np.float32]:
        holoviews.Dimension.type_formatters[dimension_type] = lambda x: pretty_fmt_complex(x, 4)

    code_dir = os.path.dirname(os.path.realpath(__file__))
    matplotlib.rc_file(os.path.join(code_dir, "matplotlibrc"))

    np.set_printoptions(
        precision=2, suppress=True, formatter={"complexfloat": pretty_fmt_complex}
    )

    # Silence Kwant warnings from color scale overflow
    warnings.filterwarnings(
        "ignore", category=RuntimeWarning, message="The plotted data contains"
    )
    # Silence fixed numpy deprecation
    warnings.filterwarnings(
        "ignore", category=np.VisibleDeprecationWarning,
        message="Creating an ndarray from ragged"
    )
