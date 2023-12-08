import contextlib
import datetime
import importlib
import itertools
import os
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import yaml
from _pytest.config import Notset
from _pytest.terminal import TerminalReporter

if TYPE_CHECKING:
    from collections.abc import Callable


def pytest_terminal_summary(
    terminalreporter: TerminalReporter,
    exitstatus: int,
) -> None:
    # on failures, don't add "Captured stdout call" as pytest does that already
    # otherwise, the section "Captured stdout call" will be added twice
    if exitstatus > 0:
        return
    # get all reports
    reports = terminalreporter.getreports("")
    # combine captured stdout of reports for tests named `<smth>::test_summary`
    content = os.linesep.join(report.capstdout for report in reports if report.capstdout)
    # add custom section that mimics pytest's one
    if content:
        terminalreporter.ensure_newline()
        terminalreporter.section(
            "Captured stdout call",
            sep="-",
            blue=True,
            bold=True,
        )
        terminalreporter.line(content)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add `--year` and `--day` options to pytest."""
    parser.addoption(
        "--year",
        type=int,
        nargs="*",
        action="store",
        choices=range(2015, datetime.date.today().year + 1),
        default=range(2015, datetime.date.today().year + 1),
        help="Run AOC tests from this year",
    )
    parser.addoption(
        "--day",
        type=int,
        nargs="*",
        action="store",
        choices=range(1, 25 + 1),
        default=range(1, 25 + 1),
        help="Run AOC tests from this day",
    )
    parser.addoption(
        "--part",
        type=str,
        nargs="*",
        action="store",
        choices=["a", "b"],
        default=["a", "b"],
        help="Run this part",
    )


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """For AOC tests, allow the year(s) and day(s) to be specified
    at the command line."""
    years = metafunc.config.getoption("year")
    days = metafunc.config.getoption("day")
    parts = metafunc.config.getoption("part")
    assert not isinstance(years, Notset)
    assert not isinstance(days, Notset)
    assert not isinstance(parts, Notset)

    # This is a list of tuples.
    # Each Tuple consist of:
    # * A solver function
    # * Puzzle input
    # * A part specification
    # * The expected output
    _test_data: list[tuple[Callable, str, str, int | str]] = []
    for year, day in itertools.product(years, days):
        solver_name = f"aoc.year{year:4d}.day{day:02d}"
        with contextlib.suppress(ModuleNotFoundError):
            solver = importlib.import_module(solver_name)
            with Path(f"tests/year{year:4d}/day{day:02d}.yml").open() as fh:
                for doc in yaml.safe_load_all(fh):
                    _test_data.extend(
                        (solver.solve, doc["input"], part, doc[part])
                        for part in parts
                        if part in doc and doc[part] is not None
                    )

    if "solver" in metafunc.fixturenames:
        # New-style test_solve
        metafunc.parametrize("solver,puzzle,part,expected", _test_data)

    if "example_data" in metafunc.fixturenames:
        metafunc.parametrize("example_data", list(itertools.product(years, days)), indirect=True)
