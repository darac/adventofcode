#!env python3

from aocd.models import Puzzle
from rich import print
from rich.progress import track
from collections import deque

A_UPPERCASE = ord("A")
ALPHABET_SIZE = 26


def _decompose(number):
    """Generate digits from `number` in base alphabet, least significants
    bits first.

    Since A is 1 rather than 0 in base alphabet, we are dealing with
    `number - 1` at each iteration to be able to extract the proper digits.
    """

    while number:
        number, remainder = divmod(number - 1, ALPHABET_SIZE)
        yield remainder


def base_10_to_alphabet(number):
    """Convert a decimal number to its base alphabet representation"""

    return "".join(chr(A_UPPERCASE + part) for part in _decompose(number))[::-1]


def base_alphabet_to_10(letters):
    """Convert an alphabet number to its decimal representation"""

    return sum(
        (ord(letter) - A_UPPERCASE + 1) * ALPHABET_SIZE ** i
        for i, letter in enumerate(reversed(letters.upper()))
    )


class ThreeMeasurementWindow:
    def __init__(self) -> None:
        self.measurements = []

    def measure(self, value: int):
        if len(self.measurements) < 3:
            self.measurements.append(value)

    def sum(self) -> int:
        if len(self.measurements) == 3:
            return sum(self.measurements)


windows = []
for depth in track([int(n) for n in Puzzle(year=2021, day=1).input_data.splitlines()]):
    windows.append(ThreeMeasurementWindow())
    for window in windows:
        window.measure(depth)


prev = None
count = 0
for winnum, window in enumerate(windows):
    name = base_10_to_alphabet(winnum)
    value = window.sum()
    if prev is not None and value is not None:
        if value > prev:
            print(f"{name}: {value} ([bold]increased[/bold])")
            count += 1
        elif value < prev:
            print(f"{name}: {value} ([bold]decreased[/bold])")
        else:
            print(f"{name}: {value} ([bold]no change[/bold])")
    prev = value

print(f"count = {count}")
