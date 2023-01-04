#!env python

import datetime
import importlib
import itertools

import pytest
import yaml


@pytest.fixture
def example_data(request):
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


@pytest.mark.parametrize(
    "example_data",
    list(itertools.product(range(2015, datetime.date.today().year), range(1, 25))),
    indirect=True,
)
@pytest.mark.parametrize("part", ["a", "b"])
def test_solve(part, example_data):
    for datum in example_data:
        if datum["solver"] is None:
            pytest.skip(f"No solution written for part {part}")
        elif part in datum and datum[part] is None:
            pytest.skip(f"No answer for part {part} (yet)")
        elif part in datum:
            assert datum["solver"](input=datum["input"], part=part) == datum[part]
