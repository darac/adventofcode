# Copyright (c) 2015-2026 Paul Saunders
"""
This module is the _entrypoint_ for the aocd plugin. This allows
advent-of-code-data runner to call our solutions with varying
years and days.
"""

import importlib

__version__ = "2025.5.0"


def solve(
    year: int,
    day: int,
    data: str,
) -> tuple[str | int | None, ...]:
    """
    Finds today's solver, and runs it twice; once for part a and once for
    part b.
    The results are combined and returned to aocd-runner for submission.
    """
    solver_name = f"aoc.year{year:4d}.day{day:02d}"
    try:
        solver = importlib.import_module(solver_name)
    except ModuleNotFoundError:
        return None, None

    solve_day = getattr(solver, "solve", None)
    if solve_day is None:
        return None, None

    a = solve_day(puzzle=data, part="a", _runner=True)
    b = solve_day(puzzle=data, part="b", _runner=True)

    return a, b
