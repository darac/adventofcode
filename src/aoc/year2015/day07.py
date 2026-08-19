# Copyright (c) 2015 Paul Saunders
# spell-checker: disable
"""
--- Day 7: Some Assembly Required ---

This year, Santa brought little Bobby Tables a set of wires and
bitwise logic gates! Unfortunately, little Bobby is a little under the
recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit
signal (a number from 0 to 65535). A signal is provided to each wire by a
gate, another wire, or some specific value. Each wire can only get a signal
from one source, but can provide its signal to multiple destinations. A gate
provides no signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts
together: x AND y -> z means to connect wires x and y to an AND gate, and
then connect its output to wire z.

For example:

  - 123 -> x means that the signal 123 is provided to wire x.
  - x AND y -> z means that the bitwise AND of wire x and wire y is provided
    to wire z.
  - p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2
    and then provided to wire q.
  - NOT e -> f means that the bitwise complement of the value from wire e is
    provided to wire f.

Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If,
for some reason, you'd like to emulate the circuit instead, almost all
programming languages (for example, C, JavaScript, or Python) provide
operators for these gates.

For example, here is a simple circuit:

123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i

After it is run, these are the signals on the wires:

d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456

In little Bobby's kit's instructions booklet (provided as your puzzle
input), what signal is ultimately provided to wire a?

--- Part Two ---

Now, take the signal you got on wire a, override wire b to that signal,
and reset the other wires (including wire a). What new signal is
ultimately provided to wire a?
"""

import logging
from typing import Literal

LOG = logging.getLogger(__name__)


MASK = 2**16 - 1
DEBUGMSG = "  %s becomes %d"


def is_number(x: str) -> bool:
    try:
        _ = int(x)
    except ValueError:
        return False
    return True


class Registers(dict[str, int]):
    def __getitem__(self, key: str) -> int:
        if is_number(key):
            return int(key)
        if key not in self:
            raise SequencingError(key)
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: int) -> None:
        super().__setitem__(key, value & MASK)


class SequencingError(Exception):
    def __init__(self: "SequencingError", reg: str) -> None:
        super().__init__(f"Unknown Register {reg} at this time.")


class UnknownCommands(Exception):  # pragma: no cover
    def __init__(self: "UnknownCommands", *args: object) -> None:
        super().__init__(f"Unknown Commands: {args}")


def parse_commands(puzzle: str) -> dict[str, int]:
    lines = puzzle.splitlines()
    registers: Registers = Registers()

    while lines:
        line = lines.pop()
        args = line.split()
        try:
            match args:
                case [_, "->", _]:
                    LOG.debug(
                        "Assign %s(%s) to %s",
                        args[0],
                        registers[args[0]],
                        args[2],
                    )
                    registers[args[2]] = registers[args[0]]
                case ["NOT", _, "->", _]:
                    LOG.debug(
                        "Invert %s(%s) into %s",
                        args[1],
                        registers[args[1]],
                        args[3],
                    )
                    registers[args[3]] = (~registers[args[1]]) & MASK
                case [_, "AND", _, "->", _]:
                    LOG.debug(
                        "%s(%s) AND %s(%s) into %s",
                        args[0],
                        registers[args[0]],
                        args[2],
                        registers[args[2]],
                        args[4],
                    )
                    registers[args[4]] = (
                        registers[args[0]] & registers[args[2]]
                    ) & MASK
                case [_, "OR", _, "->", _]:
                    LOG.debug(
                        "%s(%s) OR %s(%s) into %s",
                        args[0],
                        registers[args[0]],
                        args[2],
                        registers[args[2]],
                        args[4],
                    )
                    registers[args[4]] = (
                        registers[args[0]] | registers[args[2]]
                    ) & MASK
                case [_, "LSHIFT", _, "->", _]:
                    LOG.debug(
                        "%s(%s) LSHIFT %s(%s) into %s",
                        args[0],
                        registers[args[0]],
                        args[2],
                        registers[args[2]],
                        args[4],
                    )
                    registers[args[4]] = (
                        registers[args[0]] << registers[args[2]]
                    ) & MASK
                case [_, "RSHIFT", _, "->", _]:
                    LOG.debug(
                        "%s(%s) RSHIFT %s(%s) into %s",
                        args[0],
                        registers[args[0]],
                        args[2],
                        registers[args[2]],
                        args[4],
                    )
                    registers[args[4]] = (
                        registers[args[0]] >> registers[args[2]]
                    ) & MASK
                case _:  # pragma: no cover
                    raise UnknownCommands(args)
            LOG.debug("  %s becomes %d", args[-1], registers[args[-1]])
        except SequencingError:
            lines = [line, *lines]

    return registers


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    registers = parse_commands(puzzle)

    if part == "a":
        return registers["a"]

    # Append "<answer from part a> -> b" to the puzzle and try again
    new_puzzle = f"{puzzle}\n{registers['a']} -> b"
    assert new_puzzle != puzzle

    registers = parse_commands(new_puzzle)
    return registers["a"]
