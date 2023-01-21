#!env python

import importlib
import os

import pytest
import yaml


@pytest.fixture
def example_data(request):
    """Returns the example data, stored in a YAML file."""
    solver_name = f"aoc.year{request.param[0]:4d}.day{request.param[1]:02d}"
    try:
        solver = importlib.import_module(solver_name)
        with open(
            f"tests/year{request.param[0]:4d}/day{request.param[1]:02d}.yml", "r"
        ) as file_handle:
            yield [
                doc | {"solver": solver.solve}
                for doc in yaml.safe_load_all(file_handle)
            ]
    except ModuleNotFoundError:
        yield [{"solver": None}]


@pytest.mark.parametrize("part", ["a", "b"])
def test_solve(part, example_data):
    for datum in example_data:
        if datum["solver"] is None:
            pytest.skip(f"No solution written for part {part}")
        elif part in datum and datum[part] is None:
            pytest.skip(f"No answer for part {part} (yet)")
        elif part in datum:
            os.environ["KIVY_NO_ARGS"] = "1"
            os.environ["KIVY_NO_CONSOLELOG"] = "1"
            os.environ["KIVY_LOG_MODE"] = "PYTHON"
            assert datum["solver"](input=datum["input"], part=part) == datum[part]
