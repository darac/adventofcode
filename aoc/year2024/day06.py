# spell-checker: disable
"""
--- Day 6: Guard Gallivant ---

The Historians use their fancy device again, this time to whisk you all
away to the North Pole prototype suit manufacturing lab... in the year
1518! It turns out that having direct access to history is very convenient
for a group of historians.

You still have to be careful of time paradoxes, and so it will be important
to avoid anyone from 1518 while The Historians search for the Chief.
Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The
Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^ (to indicate the
guard is currently facing up from the perspective of the map). Any
obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves
repeatedly following these steps:

  - If there is something directly in front of you, turn right 90 degrees.
  - Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until she
reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard, she turns right
before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers), she
turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the
mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

By predicting the guard's route, you can determine which specific positions
in the lab will be in the patrol path. Including the guard's starting
position, the positions visited by the guard before leaving the area are
marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard
visit before leaving the mapped area?

--- Part Two ---

While The Historians begin working around the guard's patrol route, you
borrow their fancy device and step outside the lab. From the safety of a
supply closet, you time travel through the last few months and record the
nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they
explain that the guard's patrol area is simply too large for them to safely
search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction
won't cause a time paradox. They'd like to place the new obstruction in
such a way that the guard will get stuck in a loop, making the rest of the
lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would
like to know all of the possible positions for such an obstruction. The new
obstruction can't be placed at the guard's starting position - the guard is
there right now and would notice.

In the above example, there are only 6 different positions where a new
obstruction would cause the guard to get stuck in a loop. The diagrams of
these six situations use O to mark the new obstruction, | to show a
position where the guard moves up/down, - to show a position where the
guard moves left/right, and + to show a position where the guard moves both
up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...

Option two, put a stack of failed suit prototypes in the bottom right
quadrant of the mapped area:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...

Option three, put a crate of chimney-squeeze prototype fabric next to the
standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...

Option four, put an alchemical retroencabulator near the bottom left
corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...

Option five, put the alchemical retroencabulator a bit to the right
instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...

Option six, put a tank of sovereign glue right next to the tank of
universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..

It doesn't really matter what you choose to use as an obstacle so long as
you and The Historians can put it into position without the guard noticing.
The important thing is having enough options that you can find one that
minimizes time paradoxes, and in this example, there are 6 different
positions you could choose.

You need to get the guard stuck in a loop by adding a single new
obstruction. How many different positions could you choose for this
obstruction?
"""
# spell-checker: enable

import itertools
import logging
from copy import deepcopy
from typing import Literal

import aoc.parsers.grid

logging.basicConfig(  # NOSONAR
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
)
LOG = logging.getLogger()


def grid2str(grid: aoc.parsers.grid.Grid, x_size: int, y_size: int) -> str:
    result = "\n"
    for y_pos in range(y_size):
        for x_pos in range(x_size):
            result += grid.get((y_pos, x_pos), "@")
        result += "\n"
    return result


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    grid, x_size, y_size = aoc.parsers.grid.grid_of_chars(puzzle)

    # Find the guard
    guard = None
    for _ in itertools.product(range(x_size), range(y_size)):
        if grid.get(_) in ["^", "<", ">", "v"]:
            guard = {"pos": _, "dir": grid.get(_, ".")}
            break
    assert guard is not None
    guard_reset = deepcopy(guard)

    directions = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }
    rotate = "^>v<"

    while True:
        direction = directions[guard["dir"]]
        try:
            look = grid.get(
                (
                    guard["pos"][0] + direction[0],
                    guard["pos"][1] + direction[1],
                )
            )
            LOG.debug(guard)
            LOG.debug("In %s, I see %s", direction, look)
            if look == "#":
                # Found an obstruction
                # Mark this position as inspected
                grid[guard["pos"]] = "X"
                # Rotate the guard (in position)
                guard["dir"] = rotate[
                    (rotate.find(guard["dir"]) + 1) % len(rotate)
                ]
                grid[guard["pos"]] = guard["dir"]

            else:
                # Mark this position as inspected
                grid[guard["pos"]] = "X"
                # Move the Guard
                guard["pos"] = (
                    guard["pos"][0] + direction[0],
                    guard["pos"][1] + direction[1],
                )
                assert grid[guard["pos"]] != "#"
                grid[guard["pos"]] = guard["dir"]
        except KeyError:
            break

    guard_path = [
        _
        for _ in itertools.product(range(x_size), range(y_size))
        if grid.get(_) == "X"
    ]

    if part == "a":
        return len(guard_path)

    loop_successes = 0

    for obstruction in guard_path:
        new_grid = {}
        for _ in itertools.product(range(x_size), range(y_size)):
            if grid[_] == "#":
                new_grid[_] = grid[_]
            else:
                new_grid[_] = "."
        new_grid[obstruction] = "O"
        guard = deepcopy(guard_reset)

        LOG.debug(grid2str(new_grid, x_size, y_size))

        # Walk the grid.
        # Only allow sizeof(grid) steps. If the guard escapes
        # before that, it's not a loop.
        guard_escaped = False
        for loop_steps in range(x_size * y_size):
            direction = directions[guard["dir"]]
            try:
                look = new_grid.get(
                    (
                        guard["pos"][0] + direction[0],
                        guard["pos"][1] + direction[1],
                    )
                )
                LOG.debug(guard)
                LOG.debug("In %s, I see %s", direction, look)
                if look is None:
                    LOG.debug("Loop failed after %d steps", loop_steps)
                    guard_escaped = True
                    LOG.debug(grid2str(new_grid, x_size, y_size))
                    break
                if look in ["#", "O"]:
                    # Rotate
                    guard["dir"] = rotate[
                        (rotate.find(guard["dir"]) + 1) % len(rotate)
                    ]
                else:
                    new_grid[guard["pos"]] = guard["dir"]
                    # Move
                    guard["pos"] = (
                        guard["pos"][0] + direction[0],
                        guard["pos"][1] + direction[1],
                    )
                    if new_grid.get(guard["pos"]) == guard["dir"]:
                        LOG.info("New square matches where I'm looking")
                        guard_escaped = False
                        break
                if (
                    guard["pos"][0] < 0
                    or guard["pos"][0] > y_size
                    or guard["pos"][1] < 0
                    or guard["pos"][1] > x_size
                ):
                    LOG.debug("Loop failed after %d steps", loop_steps)
                    guard_escaped = True
                    LOG.debug(grid2str(new_grid, x_size, y_size))
                    break
            except KeyError:
                # The guard escaped, so this isn't a loop
                LOG.debug("Loop failed after %d steps", loop_steps)
                guard_escaped = True
                break
        if not guard_escaped:
            LOG.info("Loop possible with obstruction at %s", obstruction)
            loop_successes += 1

    return loop_successes
