# Copyright (c) 2015-2026 Paul Saunders
from collections.abc import Callable
from typing import Literal


def test_solve(
    solver: Callable,
    puzzle: str,
    part: Literal["a", "b"],
    expected: int | str,
) -> None:
    assert solver(puzzle=puzzle, part=part) == expected
