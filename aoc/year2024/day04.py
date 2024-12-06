# spell-checker: disable
"""
--- Day 4: Ceres Search ---

"Looks like the Chief's not here. Next!" One of The Historians pulls out a
device and pushes the only button on it. After a brief flash, you recognize
the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station
tugs on your shirt; she'd like to know if you could help her with her word
search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written
backwards, or even overlapping other words. It's a little unusual, though,
as you don't merely need to find one instance of XMAS - you need to find
all of them. Here are a few ways XMAS might appear, where irrelevant
characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word
search again, but where letters not involved in any XMAS have been replaced
with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS
appear?

--- Part Two ---

The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that
this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're
supposed to find two MAS in the shape of an X. One way to achieve that
is like this:

M.S
.A.
M.S

Irrelevant characters have again been replaced with . in the above diagram.
Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have
been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........

In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search
side and try again. How many times does an X-MAS appear?

"""
# spell-checker: enable

import itertools
import logging
from typing import Literal

from aoc.parsers.grid import Grid, Point, grid_of_chars

logging.basicConfig(  # NOSONAR
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
)
LOG = logging.getLogger()

directions = {
    "North    ": (0, -1),
    "NorthEast": (1, -1),
    "East     ": (1, 0),
    "SouthEast": (1, 1),
    "South    ": (0, 1),
    "SouthWest": (-1, 1),
    "West     ": (-1, 0),
    "NorthWest": (-1, -1),
}


class Visualisation:
    # Starts as a grid of dots but, when we find a word,
    # we can write it in here. Can be printed out at the end.
    def __init__(self, x_size: int, y_size: int) -> None:
        self.grid = {}
        self.x_size = x_size
        self.y_size = y_size
        for y_pos in range(y_size):
            for x_pos in range(x_size):
                self.grid[(y_pos, x_pos)] = "."

    def found_xmas(
        self, position: Point, direction: Point, needle: str
    ) -> None:
        """
        Record "needle" as being in "direction" from "position"
        """
        current_position = position
        for char in needle:
            assert self.grid[current_position] in [".", char]
            self.grid[current_position] = char
            current_position = move(current_position, direction)

    def __repr__(self) -> str:
        result = "\n"
        for y_pos in range(self.y_size):
            for x_pos in range(self.x_size):
                result += self.grid.get((y_pos, x_pos), "@")
            result += "\n"
        return result


FoundGrid: Visualisation | None = None


def move(position: Point, direction: Point) -> Point:
    """Advance the cursor"""
    return position[0] + direction[0], position[1] + direction[1]


def is_word_in_direction(
    grid: Grid, position: Point, direction: str, needle: str
) -> bool:
    current_position = position
    for char in needle:
        if grid.get(current_position, "") != char:
            return False
        current_position = move(current_position, directions[direction])
    LOG.debug('Found "%s" %s from %s', needle, direction, current_position)
    assert FoundGrid is not None
    FoundGrid.found_xmas(position, directions[direction], needle)
    return True


def find_xmas_from_position(
    grid: Grid, position: Point, needle: str
) -> int:
    result = 0
    for direction in directions:
        if is_word_in_direction(grid, position, direction, needle):
            result = result + 1
    return result


def find_x_mas_from_position(grid: Grid, position: Point) -> bool:
    reverse_dir = {
        "NorthEast": "SouthWest",
        "SouthWest": "NorthEast",
        "NorthWest": "SouthEast",
        "SouthEast": "NorthWest",
    }
    for first, second in [
        ("NorthWest", "SouthWest"),
        ("NorthEast", "NorthWest"),
        ("SouthEast", "NorthEast"),
        ("SouthWest", "SouthEast"),
    ]:
        if is_word_in_direction(
            grid,
            move(position, directions[first]),
            reverse_dir[first],
            "MAS",
        ) and is_word_in_direction(
            grid,
            move(position, directions[second]),
            reverse_dir[second],
            "MAS",
        ):
            return True
    return False


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    grid, x_size, y_size = grid_of_chars(puzzle=puzzle)
    global FoundGrid  # noqa: PLW0603
    FoundGrid = Visualisation(x_size, y_size)
    result = 0

    if part == "a":
        result = sum(
            find_xmas_from_position(grid, _, "XMAS")
            for _ in itertools.product(range(x_size), range(y_size))
        )
    else:
        result = sum(
            1
            for _ in itertools.product(range(x_size), range(y_size))
            if find_x_mas_from_position(grid, _)
        )
    LOG.debug(FoundGrid)

    return result
