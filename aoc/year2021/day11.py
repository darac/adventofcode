"""
--- Day 11: Dumbo Octopus ---
"""

from typing import Literal

import numpy as np
from aocd import submit
from aocd.models import Puzzle

from aoc.year2021 import LOG


def get_neighbours(
    r: int, c: int, rows: int, cols: int
) -> list[tuple[int, int]]:
    """Return a list of neighbouring locations

    For each of the cardinal points, we create a tuple of coordinates.
    Each coordinate is constrained to the size of the array (for example,
    the point to the left of an item in column 0 is at "column - 1 or else
    0"). We also use a "list(set(...))" construction to only return the
    unique set, because, at the edge, many of these constraints will mean
    the neighbours map to the same edge point.

    Args:
        r (int): The row of the point to find neighbours for
        c (int): The column of the point to find neighbours for
        rows (int): The total number of rows available
        cols (int): The total number of columns available

    Returns:
        list[tuple[int, int]]: A list of coordinate pairs
    """
    return list(
        {
            (max(0, r - 1), max(0, c - 1)),  # Above Left
            (max(0, r - 1), c),  # Above Center
            (max(0, r - 1), min(cols - 1, c + 1)),  # Above Right
            (r, max(0, c - 1)),  # Left
            # Center Center is not a neighbour, it's US :)
            (r, min(cols - 1, c + 1)),  # Right
            (min(rows - 1, r + 1), max(0, c - 1)),  # Below Left
            (min(rows - 1, r + 1), c),  # Below Center
            (min(rows - 1, r + 1), min(cols - 1, c + 1)),  # Below Left
        },
    )


def run_step(
    data: np.ndarray, step: int, part: str, runner: bool = False
) -> list[int]:
    """Runs a "step".

    - First, the energy level of each octopus increases by 1.
    - Then, any octopus with an energy level greater than 9 flashes. This
      increases the energy level of all adjacent octopuses by 1, including
      octopuses that are diagonally adjacent. If this causes an octopus to
      have an energy level greater than 9, it also flashes. This process
      continues as long as new octopuses keep having their energy level
      increased beyond 9. (An octopus can only flash at most once per step.)
    - Finally, any octopus that flashed during this step has its energy
      level set to 0, as it used all of its energy to flash.

    Args:
        data (np.ndarray): The array of Octopi
        step (int): Which Step we're on (for progress printing)
        part (str): "training", "a" or "b".

    Returns:
        Union[int, list[int]]: If part is "training" or "a", the
          number of octopi which flashed this step, else a list of
          flashes per phase
    """
    # First, the energy level of each octopus increases by 1.
    data += 1

    # Then if any octopus has more than 9 energy, it flashes
    flashed = np.zeros(data.shape, dtype="bool")
    phase_flashes = []
    while ((data > 9) & ~flashed).any():
        # If any octopi have an energy > 9, they FLASH
        flashers = data > 9
        phase_flashes.append(int(np.count_nonzero(flashers)))
        # Flashed octopi cause their neighbours to increase by one
        with np.nditer(
            data, flags=["multi_index"], op_flags=[["readwrite"]]
        ) as it:
            for _ in it:
                coord = it.multi_index
                if flashers[coord] and not flashed[coord]:
                    # New flasher
                    for neighbour in get_neighbours(*coord, *data.shape):
                        data[neighbour] += 1
        flashed |= flashers
    # Finally, if the octopus flashed, set its energy to zero
    data[flashed] = 0
    if (step < 10 or step % 10 == 0) and not runner:
        LOG.debug("After Step {%d}:\n%s", step, data)
    if part in ["training", "a"]:
        return [int(np.count_nonzero(flashed))]
    return phase_flashes


def solve(
    puzzle: str, part: Literal["a", "b", "training"], _runner: bool = False
) -> int | None:
    """Calculates the solution

    Args:
        input (str): The Puzzle Input
        part (str): "a" or "b"

    Returns:
        int: The Puzzle Solution
    """
    data = np.array([list(row) for row in puzzle.splitlines()], dtype="int")
    LOG.debug("%s", data)
    num_flashes = 0
    if part == "training":
        for step in range(1, 3):
            num_flashes += run_step(data, step, part, _runner)[0]
        return num_flashes
    if part == "a":
        for step in range(100):
            num_flashes += run_step(data, step, part, _runner)[0]
        return num_flashes
    if part == "b":
        step = 1
        while True:
            step_data = run_step(data, step, part, _runner)
            for phase, flashers in enumerate(step_data):
                if flashers == data.size and not _runner:
                    LOG.debug("%s", data)
                    LOG.info(
                        "%d points. %d flashers on phase %d of step %d",
                        data.size,
                        flashers,
                        phase,
                        step,
                    )

                    return step
            step += 1
    return None


if __name__ == "__main__":
    TRAINING_INPUT = """11111
19991
19191
19991
11111
"""
    RESULT = solve(TRAINING_INPUT, "training")
    print(f"Result (Part A): {RESULT}")
    assert RESULT == 9

    TEST_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

    RESULT = solve(TEST_INPUT, "a")
    print(f"Result (Part A): {RESULT}")
    assert RESULT == 1656

    PUZZLE = Puzzle(year=2021, day=11)
    INPUT = PUZZLE.input_data

    RESULT = solve(INPUT, "a")
    print(f"Result (Part A): {RESULT}")
    submit(RESULT, year=2021, day=11, part="a")

    RESULT = solve(TEST_INPUT, "b")
    print(f"Result (Part B): {RESULT}")
    assert RESULT == 195

    RESULT = solve(INPUT, "b")
    print(f"Result (Part B): {RESULT}")
    submit(RESULT, year=2021, day=11, part="b")
