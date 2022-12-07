#!env python

import importlib

import pytest
import yaml


@pytest.fixture
def example_data(request):
    solver_name = f"aoc.year{request.param[0]:4d}.day{request.param[1]:02d}"
    solver = importlib.import_module(solver_name)

    with open(
        f"tests/year{request.param[0]:4d}/day{request.param[1]:02d}.yml", "r"
    ) as file_handle:
        yield [
            doc | {"solver": solver.solve} for doc in yaml.safe_load_all(file_handle)
        ]


@pytest.mark.parametrize(
    "example_data",
    [
        (2021, 10),
        (2021, 11),
        (2022, 1),
        (2022, 2),
        (2022, 3),
        (2022, 4),
        (2022, 5),
        (2022, 6),
        (2022, 7),
    ],
    indirect=True,
)
@pytest.mark.parametrize("part", ["a", "b"])
def test_solve(part, example_data):
    for datum in example_data:
        if datum[part] is not None:
            assert datum["solver"](input=datum["input"], part=part) == datum[part]
        else:
            pytest.skip(f"No answer for part {part} (yet)")
