#!env python
"""
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted
carefully in a grid. The Elves explain that a previous expedition planted
these trees as a reforestation effort. Now, they're curious if this would
be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree
house hidden. To do this, you need to count the number of trees that are
visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the
height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390
Each tree is represented as a single digit whose value is its height, where
0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the
grid are shorter than it. Only consider trees in the same row or column;
that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are
already on the edge, there are no trees to block the view. In this example,
that only leaves the interior nine trees to consider:

 - The top-left 5 is visible from the left and top. (It isn't visible
   from the right or bottom since other trees of height 5 are in the
   way.)
 - The top-middle 5 is visible from the top and right.
 - The top-right 1 is not visible from any direction; for it to be
   visible, there would need to only be trees of height 0 between it and
   an edge.
 - The left-middle 5 is visible, but only from the right.
 - The center 3 is not visible from any direction; for it to be visible,
   there would need to be only trees of at most height 2 between it and
   an edge.
 - The right-middle 3 is visible from the right.
 - In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a
total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?


--- Part Two ---
Content with the amount of tree cover available, the Elves just need to
know the best spot to build their tree house: they would like to be able to
see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and
right from that tree; stop if you reach an edge or at the first tree that
is the same height or taller than the tree under consideration. (If a tree
is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the
rules above; the proposed tree house has large eaves to keep it dry, so
they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

 - Looking up, its view is not blocked; it can see 1 tree (of height 3).
 - Looking left, its view is blocked immediately; it can see only 1 tree
   (of height 5, right next to it).
 - Looking right, its view is not blocked; it can see 2 trees.
 - Looking down, its view is blocked eventually; it can see 2 trees (one
   of height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance
in each of the four directions. For this tree, this is 4 (found by
multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the
middle of the fourth row:

30373
25512
65332
33549
35390

 - Looking up, its view is blocked at 2 trees (by another tree with a
   height of 5).
 - Looking left, its view is not blocked; it can see 2 trees.
 - Looking down, its view is also not blocked; it can see 1 tree.
 - Looking right, its view is blocked at 2 trees (by a massive tree of
   height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for
the tree house.

Consider each tree on your map. What is the highest scenic score possible
for any tree?
"""

from typing import Literal, Optional

import numpy as np
import pandas as pd
from rich import print


def visible(df: pd.DataFrame, row_id: int, col_id: int) -> bool:
    tree = df[col_id][row_id]

    column = df[col_id]
    col_parts = (
        column[: max(row_id, 0)],
        column[min(row_id + 1, len(column)) :],
    )

    row = df.loc[row_id]
    row_parts = (row[: max(col_id, 0)], row[min(col_id + 1, len(row)) :])

    return (
        len(col_parts[0]) == 0
        or len(col_parts[1]) == 0
        or len(row_parts[0]) == 0
        or len(row_parts[1]) == 0
        or tree > max(col_parts[0])
        or tree > max(col_parts[1])
        or tree > max(row_parts[0])
        or tree > max(row_parts[1])
    )


def scenic_score(df: pd.DataFrame, row_id: int, col_id: int) -> int:
    tree = int(df[col_id][row_id])

    column = df[col_id]
    col_parts = (
        column[: max(row_id, 0)],
        column[min(row_id + 1, len(column)) :],
    )

    row = df.iloc[row_id]
    row_parts = (row[: max(col_id, 0)], row[min(col_id + 1, len(row)) :])

    directions = {"u": 0, "l": 0, "d": 0, "r": 0}
    for part_list, direction in [
        (reversed(col_parts[0]), "u"),
        (col_parts[1], "d"),
        (reversed(row_parts[0]), "l"),
        (row_parts[1], "r"),
    ]:
        for i in list(part_list):
            directions[direction] += 1
            if int(i) >= tree:
                break

    return int(np.prod(list(directions.values())))


def solve(input: str, part: Literal["a", "b"], runner: bool = False) -> Optional[int]:
    data_frame = pd.DataFrame(
        [[int(char) for char in line] for line in input.splitlines()]
    )
    if not runner:
        print(data_frame)

    out_frame = data_frame.copy()
    if not runner:
        print(out_frame)

    for column_name, column in data_frame.items():
        for row_name, cell in enumerate(column):
            column_name = int(column_name)  # type: ignore
            if part == "a":
                out_frame[column_name][row_name] = visible(
                    data_frame, row_id=row_name, col_id=column_name
                )
            else:
                out_frame[column_name][row_name] = scenic_score(
                    data_frame, row_id=row_name, col_id=column_name
                )

    if not runner:
        print(out_frame)

    if part == "a":
        return int(out_frame.values.sum().sum())
    else:
        return int(out_frame.max().max())