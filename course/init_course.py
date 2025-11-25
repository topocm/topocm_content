# 1. Standard library imports
import datetime
import os
import re
import sys
import warnings

# 2. External package imports
import kwant
import matplotlib
import numpy as np
import plotly
from IPython import display, get_ipython
from IPython.display import HTML

# A bunch of functions and modules to pass on, we never use them here

from . import functions

init_course = [
    "init_notebook",
    "pprint_matrix",
    "scientific_number",
    "pretty_fmt_complex",
]

__all__ = init_course + functions.__all__

for _name in functions.__all__:
    globals()[_name] = getattr(functions, _name)


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
    return rf"${fac:1.1f} \cdot 10^{{{pot:1.0f}}}$"


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
        + "\nfrom course.functions:\n"
        + ", ".join(functions.__all__)
    )

    print(f"Using kwant {kwant.__version__} and plotly {plotly.__version__}")

    now = datetime.datetime.now()
    print("Executed on {} at {}.".format(now.date(), now.time()))


def check_versions():
    if sys.version_info < (3, 10):
        raise Exception("Install Python 3.10 or higher, we recommend using pixi.")

    if tuple(int(part) for part in kwant.__version__.split(".")[:2]) < (1, 5):
        raise Exception(
            "Install kwant 1.5 or higher. If you are using conda, do: `conda install -c conda-forge kwant`"
        )


def init_notebook():
    print_information()
    check_versions()

    functions.set_default_plotly_template()

    # Ensure MathJax is available for Plotly LaTeX rendering in all contexts.
    mathjax_loader = """
    <script type="text/javascript">
    if (!window.MathJax) {
      var script = document.createElement("script");
      script.type = "text/javascript";
      script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js";
      document.head.appendChild(script);
    }
    </script>
    """
    display.display(HTML(mathjax_loader))

    # Enable inline plotting in the notebook
    get_ipython().enable_matplotlib(gui="inline")

    np.set_printoptions(
        precision=2, suppress=True, formatter={"complexfloat": pretty_fmt_complex}
    )

    # Silence Kwant warnings from color scale overflow
    warnings.filterwarnings(
        "ignore",
        category=RuntimeWarning,
        message="The plotted data contains",
    )
    # Already fixed in newer Kwant versions
    warnings.filterwarnings(
        "ignore",
        category=matplotlib.MatplotlibDeprecationWarning,
        message="The proj_transform_clip function was deprecated",
    )

    # Circumvent a deprecation warning in Kwant
    from mpl_toolkits.mplot3d import proj3d

    proj3d.proj_transform_clip = proj3d.proj_transform

    code_dir = os.path.dirname(os.path.realpath(__file__))
    matplotlib.rc_file(os.path.join(code_dir, "matplotlibrc"))
