#!env python
"""
This module is the _entrypoint_ for the aocd plugin. This allows
advent-of-code-data runner to call our solutions with varying
years and days.
"""

import importlib
import os
from typing import Tuple

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore[no-redef] # cSpell: disable-line

__version__ = importlib_metadata.version(__name__)


def solve(year: int, day: int, data: str) -> Tuple:
    """
    Finds today's solver, and runs it twice; once for part a and once for part b.
    The results are combined and returned to aocd-runner for submission.
    """
    solver_name = f"aoc.year{year:4d}.day{day:02d}"
    os.environ["KIVY_NO_ARGS"] = "1"
    os.environ["KIVY_NO_CONSOLELOG"] = "1"
    os.environ["KIVY_LOG_MODE"] = "PYTHON"
    try:
        solver = importlib.import_module(solver_name)
    except ModuleNotFoundError:
        return None, None

    try:
        a = solver.solve(input=data, part="a", _runner=True)
        b = solver.solve(input=data, part="b", _runner=True)
    except AttributeError:
        return None, None

    return a, b
