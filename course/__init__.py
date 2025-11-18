"""Utilities shared across the TopoCM course."""

from importlib import metadata as _metadata

from . import components as components
from . import functions as functions
from . import init_course as init_course


try:  # pragma: no cover - metadata only available once installed
    __version__ = _metadata.version("topocm-course")
except _metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"


__all__ = [
    "components",
    "functions",
    "init_course",
    "__version__",
]
