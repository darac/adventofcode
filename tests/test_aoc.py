import os
from collections.abc import Callable
from typing import Literal


def test_solve(
    solver: Callable,
    puzzle: str,
    part: Literal["a", "b"],
    expected: int | str,
) -> None:
    os.environ["KIVY_NO_ARGS"] = "1"
    os.environ["KIVY_NO_CONSOLELOG"] = "1"  # spell-checker: disable-line
    os.environ["KIVY_LOG_MODE"] = "PYTHON"
    assert solver(puzzle=puzzle, part=part) == expected
