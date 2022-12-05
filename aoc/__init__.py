#!env python
"""
This module is the _entrypoint_ for the aocd plugin. This allows
advent-of-code-data runner to call our solutions with varying
years and days.
"""

import importlib
import os
from typing import Tuple

__version__ = 2022.03


def solve(year: int, day: int, data: str) -> Tuple:
    """
    Finds today's solver, and runs it twice; once for part a and once for part b.
    The results are combined and returned to aocd-runner for submission.
    """
    solver_name = f"aoc.year{year:4d}.day{day:02d}"
    solver = importlib.import_module(solver_name)

    a = solver.solve(input=data, part="a", runner=True)
    b = solver.solve(input=data, part="b", runner=True)

    return a, b
