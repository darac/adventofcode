#!env python3
import datetime
import itertools
import os

import pytest
from _pytest.config import Notset
from _pytest.terminal import TerminalReporter


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
    """Add '--year' and '--day' options to pytest."""
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


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """For AOC tests, allow the year(s) and day(s) to be specified
    at the command line."""
    years = metafunc.config.getoption("year")
    days = metafunc.config.getoption("day")
    assert not isinstance(years, Notset)
    assert not isinstance(days, Notset)

    if "example_data" in metafunc.fixturenames:
        metafunc.parametrize("example_data", list(itertools.product(years, days)), indirect=True)
