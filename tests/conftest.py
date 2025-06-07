import contextlib
import datetime
import importlib
import itertools
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

import aocd
import pytest
import yaml
from _pytest.config import Notset
from _pytest.terminal import TerminalReporter

if TYPE_CHECKING:
    from collections.abc import Callable

LOG = logging.getLogger()


def pytest_terminal_summary(
    terminalreporter: TerminalReporter,
    exitstatus: int,
) -> None:
    # on failures, don't add "Captured stdout call" as pytest does that
    # already otherwise, the section "Captured stdout call" will be added
    # twice
    if exitstatus > 0:
        return
    # get all reports
    reports = terminalreporter.getreports("")
    # combine captured stdout of reports for tests named
    # `<smth>::test_summary`
    content = os.linesep.join(
        report.capstdout for report in reports if report.capstdout
    )
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
        choices=range(
            2015,
            datetime.datetime.now(tz=datetime.UTC).date().year + 1,
        ),
        default=range(
            2015, datetime.datetime.now(tz=datetime.UTC).date().year + 1
        ),
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
    parser.addoption(
        "--today",
        action="store_true",
        help="Run the latest available day (overrides --year and --day)",
    )


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """For AOC tests, allow the year(s) and day(s) to be specified
    at the command line."""
    years = metafunc.config.getoption("year")
    days = metafunc.config.getoption("day")
    parts = metafunc.config.getoption("part")
    today = metafunc.config.getoption("today")
    assert not isinstance(years, Notset)
    assert not isinstance(days, Notset)
    assert not isinstance(parts, Notset)

    if today:
        # Look for the latest year and day that have test data
        years = [
            [
                int(f.name.removeprefix("year"))
                for f in sorted(Path("tests").iterdir())
                if f.is_dir() and f.name.startswith("year")
            ][-1]
        ]
        days = [
            [
                int(f.stem.removeprefix("day"))
                for f in sorted(
                    (Path("tests") / f"year{years[0]}").iterdir()
                )
                if not f.is_dir() and f.stem.startswith("day")
            ][-1]
        ]
        LOG.info("Today's test is Year %s, Day %s", years[0], days[0])

    # This is a list of tuples.
    # Each Tuple consist of:
    # * A solver function
    # * Puzzle input
    # * A part specification
    # * The expected output
    _test_data: list[tuple[Callable, str, str, int | str]] = []
    _id_list: list[str] = []
    for year, day in itertools.product(years, days):
        solver_name = f"aoc.year{year:4d}.day{day:02d}"
        print(f"Finding solver for: {solver_name}")
        with contextlib.suppress(
            ModuleNotFoundError, aocd.exceptions.AocdError
        ):
            solver = importlib.import_module(solver_name)
            with Path(f"tests/year{year:4d}/day{day:02d}.yml").open() as fh:
                print(f"Found {fh.name}")
                for doc_num, doc in enumerate(
                    yaml.safe_load_all(fh), start=1
                ):
                    _test_data.extend(
                        (solver.solve, doc["input"], part, doc[part])
                        for part in parts
                        if part in doc and doc[part] is not None
                    )
                    _id_list.extend(
                        f"year{year:4d}/day{day:02d}/test{doc_num:02d}/part{part}"
                        for part in parts
                        if part in doc and doc[part] is not None
                    )

    if "solver" in metafunc.fixturenames:
        # New-style test_solve
        metafunc.parametrize(
            "solver,puzzle,part,expected", _test_data, ids=_id_list
        )

    if "example_data" in metafunc.fixturenames:
        metafunc.parametrize(
            "example_data",
            list(itertools.product(years, days)),
            indirect=True,
        )
