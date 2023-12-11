# spell-checker: disable
"""
--- Day 6: Probably a Fire Hazard ---
Because your neighbors keep defeating you in the holiday house decorating
contest year after year, you've decided to deploy one million lights in a
1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has
mailed you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the
lights at each corner are at 0,0, 0,999, 999,999, and 999,0. The
instructions include whether to turn on, turn off, or toggle various
inclusive ranges given as coordinate pairs. Each coordinate pair represents
opposite corners of a rectangle, inclusive; a coordinate pair like
0,0 through 2,2 therefore refers to 9 lights in a 3x3 square. The lights
all start turned off.

To defeat your neighbors this year, all you have to do is set up your
lights by doing the instructions Santa sent you in order.

For example:

 - turn on 0,0 through 999,999 would turn on (or leave on) every light.
 - toggle 0,0 through 999,0 would toggle the first line of 1000 lights,
   turning off the ones that were on, and turning on the ones that were
   off.
 - turn off 499,499 through 500,500 would turn off (or leave off) the
   middle four lights.

After following the instructions, how many lights are lit?

--- Part Two ---
You just finish implementing your winning light pattern when you realize
you mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each
light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness
of those lights by 1.

The phrase turn off actually means that you should decrease the brightness
of those lights by 1, to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of
those lights by 2.

What is the total brightness of all lights combined after following Santa's
instructions?

For example:

 - turn on 0,0 through 0,0 would increase the total brightness by 1.
 - toggle 0,0 through 999,999 would increase the total brightness by
   2000000.
"""
# spell-checker: enable

import logging
from collections.abc import Generator
from typing import Any, Literal

import numpy as np
import parse
import pygame
from rich.logging import RichHandler

from aoc.visualisations.PyGame import TwoDAnimationViewer

logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
LOG = logging.getLogger()


def solve_steps_a(
    puzzle: str,
) -> Generator[tuple[Any, np.ndarray], Any, None]:
    lights = np.zeros(shape=(1000, 1000), dtype=bool)
    for line in puzzle.splitlines():
        # Process instructions
        p = parse.parse(
            "{command} {top:d},{left:d} through {bottom:d},{right:d}", line
        )
        assert type(p) is parse.Result
        assert p
        if p["command"] == "turn on":
            lights[
                p["top"] : p["bottom"] + 1, p["left"] : p["right"] + 1
            ] = True
        elif p["command"] == "turn off":
            lights[
                p["top"] : p["bottom"] + 1, p["left"] : p["right"] + 1
            ] = False
        elif p["command"] == "toggle":
            lights[
                p["top"] : p["bottom"] + 1, p["left"] : p["right"] + 1
            ] = np.logical_not(
                lights[
                    p["top"] : p["bottom"] + 1, p["left"] : p["right"] + 1
                ],
            )
        LOG.debug("%s -> %s", line, lights.sum())
        yield lights.sum(), lights.astype("uint8")


class UnknownCommand(Exception):
    def __init__(self: "UnknownCommand", command: str) -> None:
        super().__init__(f"Unknown Command: {command}")


class UnmatchedInstruction(Exception):
    def __init__(self: "UnmatchedInstruction", instruction: str) -> None:
        super().__init__(f"Unmatched instruction: {instruction}")


def solve_steps_b(
    puzzle: str,
) -> Generator[tuple[Any, np.ndarray], Any, None]:
    lights = np.zeros(shape=(1000, 1000), dtype="int")
    assert lights.sum() == 0
    for lineno, line in enumerate(puzzle.splitlines()):
        # Process instructions
        p = parse.parse(
            "{command} {top:d},{left:d} through {bottom:d},{right:d}", line
        )
        assert type(p) is parse.Result
        assert 0 <= p["top"] < 1000
        assert 0 <= p["bottom"] < 1000
        assert 0 <= p["left"] < 1000
        assert 0 <= p["right"] < 1000
        num_lights = lights.sum()
        if p:
            if p["command"] == "turn on":
                lights[
                    p["top"] : p["bottom"] + 1, p["left"] : p["right"] + 1
                ] += 1
                assert (
                    lights.sum() > num_lights
                ), f"{lineno}: {lights.sum()} !> {num_lights}"
            elif p["command"] == "turn off":
                if (
                    lights[
                        p["top"] : p["bottom"] + 1,
                        p["left"] : p["right"] + 1,
                    ].sum()
                    == 0
                ):
                    LOG.debug("Skipping already off section")
                    continue
                lights[
                    p["top"] : p["bottom"] + 1, p["left"] : p["right"] + 1
                ] -= 1
                LOG.info(
                    "There are %d negative cells. Resetting them...",
                    len(lights[lights < 0]),
                )
                lights[lights < 0] = 0
                assert (
                    lights.sum() < num_lights
                ), f"{lineno}: {lights.sum()} !< {num_lights}"
            elif p["command"] == "toggle":
                lights[
                    p["top"] : p["bottom"] + 1, p["left"] : p["right"] + 1
                ] += 2
                assert (
                    lights.sum() > num_lights
                ), f"{lineno}: {lights.sum()} !> {num_lights}"
            else:
                raise UnknownCommand(p["command"])
        else:
            raise UnmatchedInstruction(line)
        LOG.debug("%s -> %s", line, lights.sum())
        yield lights.sum(), lights.astype("uint8")


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    if _runner:
        LOG.setLevel("WARN")
    if part == "a":
        try:
            vis = TwoDAnimationViewer(
                update_func=solve_steps_a,
                puzzle_input=puzzle,
                display_size=(1000, 1000),
            )
            return vis.start()
        except pygame.error:
            retval = None
            for value, _ in solve_steps_a(puzzle):
                retval = value
            return retval
    else:
        try:
            vis = TwoDAnimationViewer(
                update_func=solve_steps_b,
                puzzle_input=puzzle,
                display_size=(1000, 1000),
            )
            return vis.start()
        except pygame.error:
            retval = None
            for value, _ in solve_steps_b(puzzle):
                retval = value
            return retval
