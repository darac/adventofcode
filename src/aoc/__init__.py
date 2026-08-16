# Copyright (c) 2015-2026 Paul Saunders
"""
This module is the _entrypoint_ for the aocd plugin. This allows
advent-of-code-data runner to call our solutions with varying
years and days.
"""

import importlib

import pytest

__version__ = "2025.5.0"


def solve(
    year: int,
    day: int,
    data: str,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[int | None, ...]:
    """
    Finds today's solver, and runs it twice; once for part a and once for
    part b.
    The results are combined and returned to aocd-runner for submission.
    """
    solver_name = f"aoc.year{year:4d}.day{day:02d}"
    monkeypatch.setenv("KIVY_NO_ARGS", "1")
    monkeypatch.setenv("KIVY_NO_CONSOLELOG", "1")
    monkeypatch.setenv("KIVY_LOG_MODE", "PYTHON")
    try:
        solver = importlib.import_module(solver_name)
    except ModuleNotFoundError:
        return None, None

    try:
        a = solver.solve(puzzle=data, part="a", _runner=True)
        b = solver.solve(puzzle=data, part="b", _runner=True)
    except AttributeError:
        return None, None

    return a, b
