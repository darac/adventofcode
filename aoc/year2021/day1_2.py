"""
Considering every single measurement isn't as useful as you expected:
there's just too much noise in the data.

Instead, consider sums of a three-measurement sliding window. Again
considering the above example:

199  A
200  A B
208  A B C
210    B C D
200  E   C D
207  E F   D
240  E F G
269    F G H
260      G H
263        H

Start by comparing the first and second three-measurement windows. The
measurements in the first window are marked A (199, 200, 208); their sum is
199 + 200 + 208 = 607. The second window is marked B (200, 208, 210); its
sum is 618. The sum of measurements in the second window is larger than the
sum of the first, so this first comparison increased.

Your goal now is to count the number of times the sum of measurements in
this sliding window increases from the previous sum. So, compare A with B,
then compare B with C, then C with D, and so on. Stop when there aren't
enough measurements left to create a new three-measurement sum.

In the above example, the sum of each three-measurement window is as
follows:

A: 607 (N/A - no previous sum)
B: 618 (increased)
C: 618 (no change)
D: 617 (decreased)
E: 647 (increased)
F: 716 (increased)
G: 769 (increased)
H: 792 (increased)

In this example, there are 5 sums that are larger than the previous sum.

Consider sums of a three-measurement sliding window.
How many sums are larger than the previous sum?
"""

from collections.abc import Generator
from typing import Any

from aocd.models import Puzzle
from rich import print
from rich.progress import track

A_UPPERCASE = ord("A")
ALPHABET_SIZE = 26


def _decompose(number: int) -> Generator[int, Any, None]:
    """Generate digits from `number` in base alphabet, least significant
    bits first.

    Since A is 1 rather than 0 in base alphabet, we are dealing with
    `number - 1` at each iteration to be able to extract the proper digits.
    """

    while number:
        number, remainder = divmod(number - 1, ALPHABET_SIZE)
        yield remainder


def base_10_to_alphabet(number: int) -> str:
    """Convert a decimal number to its base alphabet representation"""

    return "".join(chr(A_UPPERCASE + part) for part in _decompose(number))[
        ::-1
    ]


def base_alphabet_to_10(letters: str) -> int:
    """Convert an alphabet number to its decimal representation"""

    return sum(
        (ord(letter) - A_UPPERCASE + 1) * ALPHABET_SIZE**i
        for i, letter in enumerate(reversed(letters.upper()))
    )


class ThreeMeasurementWindow:
    """
    Holds the first three Measurements added.
    When asked, will return the sum of the measurements held.
    """

    def __init__(self: "ThreeMeasurementWindow") -> None:
        self.measurements = []  # type: list[int]

    def measure(self: "ThreeMeasurementWindow", val: int) -> None:
        """
        Takes a value and, if less than three values have been stored,
        stores it. Else discards it.
        """
        if len(self.measurements) < 3:
            self.measurements.append(val)

    def sum_values(self: "ThreeMeasurementWindow") -> int:
        """
        Returns the sum of values held, but only if three are held.
        """
        if len(self.measurements) == 3:
            return sum(self.measurements)
        return 0


windows = []
for depth in track(
    [int(n) for n in Puzzle(year=2021, day=1).input_data.splitlines()]
):
    windows.append(ThreeMeasurementWindow())
    for window in windows:
        window.measure(depth)


PREV = None
COUNT = 0
for window_number, window in enumerate(windows):
    NAME = base_10_to_alphabet(window_number)
    value = window.sum_values()
    if PREV is not None and value is not None:
        if value > PREV:
            print(f"{NAME}: {value} ([bold]increased[/bold])")
            COUNT += 1
        elif value < PREV:
            print(f"{NAME}: {value} ([bold]decreased[/bold])")
        else:
            print(f"{NAME}: {value} ([bold]no change[/bold])")
    PREV = value

print(f"count = {COUNT}")
