#!env python3
"""
--- Day 13: Transparent Origami ---
"""
import os
import re
from typing import Literal

import numpy as np
from aocd import submit
from aocd.models import Puzzle
from rich import print


def print_sheet(sheet: np.ndarray) -> None:
    """Prints out the sheet using blocks and spaces
    NOTE: We use np.transpose, otherwise you have to cock your head :)

    Args:
        sheet (np.ndarray): The sheet, as it currently stands
    """
    for row in np.transpose(sheet):
        print("".join(["█" if x else " " for x in row]))


def create_sheet(puzzle: str) -> np.ndarray:
    """Generates an empty sheet of the size required by the puzzle

    Args:
        input (str): The Test input

    Returns:
        np.ndarray: An empty array, big enough to hold all the points
    """
    rows = cols = 0
    for lineno, line in enumerate(puzzle.splitlines()):
        if line == "":
            break
        try:
            r, c = map(int, line.split(","))
        except ValueError:
            print(f"Bad line on Line {lineno} was: {line}")
            raise
        rows = max(rows, r)
        cols = max(cols, c)

    # Make an empty sheet
    return np.zeros((rows + 1, cols + 1), dtype="bool")


def solve(puzzle: str, part: Literal["a", "b"], _runner: bool = False) -> int | None:
    """Calculates the solution

    Args:
        input (str): The Puzzle Input
        part (str): "a" or "b"

    Returns:
        int: The Puzzle Solution
    """
    # Start by reading the input to find the size of the sheet
    sheet = create_sheet(puzzle)

    # Read the input data
    read_mode = 0
    folds = []
    for line in puzzle.splitlines():
        if line == "":
            read_mode += 1
        elif read_mode == 0:
            r, c = map(int, line.split(","))
            sheet[r][c] = True
        elif read_mode == 1:
            m = re.match(r"fold along ([xy])=(\d+)", line)
            if m:
                folds.append({"axis": 0 if m.group(1) == "x" else 1, "line": int(m.group(2))})
    print_sheet(sheet)
    print(folds)

    # Now start folding
    for fold in folds:
        print(f"Fold along {'x' if fold['axis'] == 0 else 'y'}={fold['line']}")
        # pylint: disable=W0632
        (orig, _, copy) = np.split(sheet, [fold["line"], fold["line"] + 1], axis=fold["axis"])
        if orig.shape > copy.shape:
            # The fold is asymmetrical, so we need to expand the second page before flipping
            print(f"Shape is {copy.shape}. Want {orig.shape}")
            # ((top,bottom), (left,right))
            padding = (
                (0, orig.shape[0] - copy.shape[0]),
                (0, orig.shape[1] - copy.shape[1]),
            )
            print(f" Therefore, pad with {padding}")

            copy = np.pad(
                copy,
                padding,
                constant_values=False,
            )
        elif orig.shape < copy.shape:
            # The fold is asymmetrical, so we need to expand the second page before flipping
            print(f"Shape is {copy.shape}. Want {orig.shape}")
            # ((top,bottom), (left,right))
            padding = (
                (0, copy.shape[0] - orig.shape[0]),
                (0, copy.shape[1] - orig.shape[1]),
            )
            print(f" Therefore, pad with {padding}")
            orig = np.pad(
                orig,
                padding,
                constant_values=False,
            )

        sheet = orig | np.flip(copy, axis=fold["axis"])
        if part == "a":
            print_sheet(sheet)
            return np.count_nonzero(sheet)
        print("=== Fold ===")
        print_sheet(sheet)
    return np.count_nonzero(sheet)


if __name__ == "__main__":
    np.set_printoptions(
        linewidth=os.get_terminal_size()[0],
        formatter={"bool": lambda b: "#" if b else "."},
        threshold=int(os.get_terminal_size()[0] / 4),
    )

    TEST_INPUT = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

    RESULT = solve(TEST_INPUT, "a")
    print(f"Result (Part A): {RESULT}")
    assert RESULT == 17

    PUZZLE = Puzzle(year=2021, day=13)
    INPUT = PUZZLE.input_data

    RESULT = solve(INPUT, "a")
    print(f"Result (Part A): {RESULT}")
    submit(RESULT, year=2021, day=13, part="a")

    RESULT = solve(TEST_INPUT, "b")
    print(f"Result (Part B): {RESULT}")

    RESULT = solve(INPUT, "b")
    print(f"Result (Part B): {RESULT}")
