# Copyright (c) 2015-2026 Paul Saunders
from collections.abc import Callable
from typing import Literal

import pytest


def test_solve(
    solver: Callable,
    puzzle: str,
    part: Literal["a", "b"],
    expected: int | str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("KIVY_NO_ARGS", "1")
    monkeypatch.setenv(
        "KIVY_NO_CONSOLELOG", "1"
    )  # spell-checker: disable-line
    monkeypatch.setenv("KIVY_LOG_MODE", "PYTHON")
    assert solver(puzzle=puzzle, part=part) == expected
