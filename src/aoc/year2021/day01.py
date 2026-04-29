# spell-checker: disable
"""
--- Day 1: Sonar Sweep ---

You're minding your own business on a ship at sea when the overboard alarm
goes off! You rush to see if you can help. Apparently, one of the Elves
tripped and accidentally sent the sleigh keys flying into the ocean!

Before you know it, you're inside a submarine the Elves keep ready for
situations like this. It's covered in Christmas lights (because of course
it is), and it even has an experimental antenna that should be able to
track the keys if you can boost its signal strength high enough; there's a
little meter that indicates the antenna's signal strength by displaying
0-50 stars.

Your instincts tell you that in order to save Christmas, you'll need to get
all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on
each day in the Advent calendar; the second puzzle is unlocked when you
complete the first. Each puzzle grants one star. Good luck!

As the submarine drops below the surface of the ocean, it automatically
performs a sonar sweep of the nearby sea floor. On a small screen, the
sonar sweep report (your puzzle input) appears: each line is a measurement
of the sea floor depth as the sweep looks further and further away from the
submarine.

For example, suppose you had the following report:

199
200
208
210
200
207
240
269
260
263

This report indicates that, scanning outward from the submarine, the sonar
sweep found depths of 199, 200, 208, 210, and so on.

The first order of business is to figure out how quickly the depth
increases, just so you know what you're dealing with - you never know if
the keys will get carried into deeper water by an ocean current or a fish
or something.

To do this, count the number of times a depth measurement increases from
the previous measurement. (There is no measurement before the first
measurement.) In the example above, the changes are as follows:

199 (N/A - no previous measurement)
200 (increased)
208 (increased)
210 (increased)
200 (decreased)
207 (increased)
240 (increased)
269 (increased)
260 (decreased)
263 (increased)

In this example, there are 7 measurements that are larger than the previous
measurement.

How many measurements are larger than the previous measurement?

---

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
# spell-checker: enable

from collections.abc import Generator
from typing import Any, Literal

from rich.progress import track

from aoc.year2021 import LOG

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


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    prev = None
    count = 0

    if part == "a":
        for line in puzzle.splitlines():
            value = int(line)
            if prev is not None:
                if value > prev:
                    LOG.debug(f"{value} ([bold]increased[/bold])")
                    count += 1
                else:
                    LOG.debug(f"{value} (decreased)")
            prev = value

        LOG.info(f"count = {count}")
    elif part == "b":
        windows = []
        for depth in track([int(n) for n in puzzle.splitlines()]):
            windows.append(ThreeMeasurementWindow())
            for window in windows:
                window.measure(depth)

        for window_number, window in enumerate(windows):
            name = base_10_to_alphabet(window_number)
            value = window.sum_values()
            if prev is not None and value is not None:
                if value > prev:
                    LOG.debug(f"{name}: {value} ([bold]increased[/bold])")
                    count += 1
                elif value < prev:
                    LOG.debug(f"{name}: {value} ([bold]decreased[/bold])")
                else:
                    LOG.debug(f"{name}: {value} ([bold]no change[/bold])")
            prev = value

        LOG.info(f"count = {count}")
    return count
