# spell-checker: disable
"""--- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically
active; small hydrothermal vents release smoke into the caves that slowly
settles like rain.

If you can model how the smoke flows through the caves, you might be able
to avoid it and be that much safer. The submarine generates a heightmap of
the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider
the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678
Each number corresponds to the height of a particular location, where 9 is
the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower
than any of its adjacent locations. Most locations have four adjacent
locations (up, down, left, and right); locations on the edge or corner of
the map have three or two adjacent locations, respectively. (Diagonal
locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are
in the first row (a 1 and a 0), one is in the third row (a 5), and one is
in the bottom row (also a 5). All other locations on the heightmap have
some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example,
the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk
levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk
levels of all low points on your heightmap?

--- Part Two ---
Next, you need to find the largest basins so you know what areas are most
important to avoid.

A basin is all locations that eventually flow downward to a single low
point. Therefore, every low point has a basin, although some basins are
very small. Locations of height 9 do not count as being in any basin, and
all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including
the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the
above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest
basins?
"""
# spell-checker: enable
import contextlib
from typing import Literal

import numpy as np
import pandas as pd
from aocd import submit
from aocd.models import Puzzle
from rich import print


def get_neighbours(row: int, column: int, rows: int, cols: int) -> list[tuple[int, int]]:
    """Return a list of neighbouring locations

    Args:
        row (int): The row of the point to find neighbours for
        column (int): The column of the point to find neighbours for
        rows (int): The total number of rows available
        cols (int): The total number of columns available

    Returns:
        list[tuple[int, int]]: A list of coordinate pairs
    """
    return [
        (max(0, row - 1), column),
        (min(rows - 1, row + 1), column),
        (row, max(0, column - 1)),
        (row, min(cols - 1, column + 1)),
    ]


def flood(data: np.ndarray, point: tuple[int, int], visited: list) -> int:
    """Flood-fill data, starting at a point

    Args:
        data (np.ndarray): The data to fill
        point (tuple[int, int]): The location to fill from
        visited (list): A list of points we've already filled

    Returns:
        int: The sum of the points filled, plus 1.
    """
    if point in visited or data[point] == 9:
        return 0
    visited.append(point)
    neighbours = get_neighbours(*point, *data.shape)
    return 1 + sum([flood(data, n, visited) for n in neighbours if n not in visited])


def get_neighbour(
    data_frame: pd.DataFrame,
    row_name: int,
    column_name: int,
) -> list[tuple[int, int]]:
    neighbours = []
    with contextlib.suppress(KeyError):
        # Above
        neighbours.append(data_frame.loc[row_name - 1, column_name])
    with contextlib.suppress(KeyError):
        # Left
        neighbours.append(data_frame.loc[row_name, column_name - 1])
    with contextlib.suppress(KeyError):
        # Right
        neighbours.append(data_frame.loc[row_name, column_name + 1])
    with contextlib.suppress(KeyError):
        # Below
        neighbours.append(data_frame.loc[row_name + 1, column_name])
    return neighbours


def solve(puzzle: str, part: Literal["a", "b"], _runner: bool = False) -> int | None:
    """Calculates the solution

    Args:
        input (str): The Puzzle Input
        part (str): "a" or "b"

    Returns:
        int: The Puzzle Solution
    """
    data_frame = pd.DataFrame([[int(char) for char in line] for line in puzzle.splitlines()])
    if not _runner:
        print(data_frame)
    risk_level = 0
    low_points = []
    for column_name, column in data_frame.items():
        column_name = int(column_name)  # type: ignore
        for row_name, cell in enumerate(column):
            neighbours = get_neighbour(data_frame, row_name, column_name)
            local_min = cell < min(neighbours)
            if local_min:
                low_points.append((int(row_name), int(column_name)))
                risk_level += cell + 1
    if part == "a":
        return risk_level

    # Part B
    data = np.array([list(map(int, list(row))) for row in puzzle.splitlines()])
    if not _runner:
        print(data)
    basins = sorted([flood(data, low_point, []) for low_point in low_points])
    if not _runner:
        print(f"Largest basins: {basins[-3:]} -> {np.prod(basins[-3:])}")
    return int(np.prod(basins[-3:]))


if __name__ == "__main__":
    TEST_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678"""

    RESULT = solve(TEST_INPUT, "a")
    print(f"Result (Part A): {RESULT}")
    assert RESULT == 15

    PUZZLE = Puzzle(year=2021, day=9)
    INPUT = PUZZLE.input_data

    RESULT = solve(INPUT, "a")
    print(f"Result (Part A): {RESULT}")
    submit(RESULT, year=2021, day=9, part="a")

    RESULT = solve(TEST_INPUT, "b")
    print(f"Result (Part B): {RESULT}")
    assert RESULT == 1134

    RESULT = solve(INPUT, "b")
    print(f"Result (Part B): {RESULT}")
    submit(RESULT, year=2021, day=9, part="b")
