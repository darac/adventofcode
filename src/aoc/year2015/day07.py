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
"""

import logging
from typing import Literal

from rich.logging import RichHandler

logging.basicConfig(level="DEBUG", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
LOG = logging.getLogger()

REGISTERS: dict[str, int] = {}
MASK = 2**16 - 1


def is_number(x: str) -> bool:
    try:
        _ = int(x)
    except ValueError:
        return False
    return True


def get(reg: str) -> int:
    if is_number(reg):
        return int(reg)
    if reg not in REGISTERS:
        raise SequencingError(reg)
    return REGISTERS[reg]


def put(reg: str, val: int) -> None:
    REGISTERS[reg] = val


class SequencingError(Exception):
    def __init__(self: "SequencingError", reg: str) -> None:
        super().__init__(f"Unknown Register {reg} at this time.")


class UnknownCommands(Exception):
    def __init__(self: "UnknownCommands", *args: object) -> None:
        super().__init__(f"Unknown Commands: {args}")


def solve(puzzle: str, part: Literal["a", "b"], _runner: bool = False) -> int | None:
    if _runner:
        LOG.setLevel("WARN")
    for line in puzzle.splitlines():
        args = line.split()
        match args:
            case [_, "->", _]:
                LOG.info("Assign %s(%s) to %s", args[0], get(args[0]), args[2])
                put(args[2], get(args[0]))
                LOG.info("  %s becomes %d", args[2], get(args[2]))
            case ["NOT", _, "->", _]:
                LOG.info("Invert %s(%s) into %s", args[1], get(args[1]), args[3])
                put(args[3], (~get(args[1])) & MASK)
                LOG.info("  %s becomes %d", args[3], get(args[3]))
            case [_, "AND", _, "->", _]:
                LOG.info(
                    "%s(%s) AND %s(%s) into %s",
                    args[0],
                    get(args[0]),
                    args[2],
                    get(args[2]),
                    args[4],
                )
                put(args[4], (get(args[0]) & get(args[2])) & MASK)
                LOG.info("  %s becomes %d", args[4], get(args[4]))
            case [_, "OR", _, "->", _]:
                LOG.info(
                    "%s(%s) OR %s(%s) into %s",
                    args[0],
                    get(args[0]),
                    args[2],
                    get(args[2]),
                    args[4],
                )
                put(args[4], (get(args[0]) | get(args[2])) & MASK)
                LOG.info("  %s becomes %d", args[4], get(args[4]))
            case [_, "LSHIFT", _, "->", _]:
                LOG.info(
                    "%s(%s) LSHIFT %s(%s) into %s",
                    args[0],
                    get(args[0]),
                    args[2],
                    get(args[2]),
                    args[4],
                )
                put(args[4], (get(args[0]) << get(args[2])) & MASK)
                LOG.info("  %s becomes %d", args[4], get(args[4]))
            case [_, "RSHIFT", _, "->", _]:
                LOG.info(
                    "%s(%s) RSHIFT %s(%s) into %s",
                    args[0],
                    get(args[0]),
                    args[2],
                    get(args[2]),
                    args[4],
                )
                put(args[4], (get(args[0]) >> get(args[2])) & MASK)
                LOG.info("  %s becomes %d", args[4], get(args[4]))
            case _:
                raise UnknownCommands(args)
    try:
        return REGISTERS["a"]
    except KeyError:
        return 0
