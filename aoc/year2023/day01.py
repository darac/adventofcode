# spell-checker: disable
"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to
take a look. The Elves have even given you a map; on it, they've used stars
to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations,
you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on
each day in the Advent calendar; the second puzzle is unlocked when you
complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful
enough") and where they're even sending you ("the sky") and why your map
looks mostly blank ("you sure ask a lot of questions") and hang on did you
just say the sky ("of course, where do you think snow comes from") when you
realize that the Elves are already loading you into a trebuchet ("please
hold still, we need to strap you in").

As they're making the final adjustments, they discover that their
calibration document (your puzzle input) has been amended by a very young
Elf who was apparently just excited to show off her art skills.
Consequently, the Elves are having trouble reading the values on the
document.

The newly-improved calibration document consists of lines of text; each
line originally contained a specific calibration value that the Elves now
need to recover. On each line, the calibration value can be found by
combining the first digit and the last digit (in that order) to form a
single two-digit number.

For example:

  1abc2
  pqr3stu8vwx
  a1b2c3d4e5f
  treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15,
and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the
calibration values?

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are
actually spelled out with letters: one, two, three, four, five, six, seven,
eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and
last digit on each line. For example:

  two1nine
  eightwothree
  abcone2threexyz
  xtwone3four
  4nineeightseven2
  zoneight234
  7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76.
Adding these together produces 281.

What is the sum of all of the calibration values?
"""
# spell-checker: enable

import re
from typing import Literal

from aoc.year2023 import LOG


def get_digits(in_str: str) -> list[str]:
    """Returns a list of all single digits within a string

    Args:
        in_str (str): The string to search

    Returns:
        list[str]: A list of all the digits, as chars
    """
    return re.findall(r"\d", in_str)


def get_numbers(in_str: str) -> list[str]:
    """Returns a list of all digits and number-words in a string

    Args:
        in_str (str): The string to search

    Returns:
        list[str]: A list of all the numbers, as strings
    """
    # Almost right first time, but needed "(?=...)" to avoid overlaps
    return re.findall(
        r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", in_str
    )


def word_to_number(in_str: str) -> int:
    """Convert numbers (as digits or words) to ints

    Args:
        in_str (str): A number

    Returns:
        int: The value
    """
    _map = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        # No zero
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    return _map.get(in_str, 0)


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    retval = 0
    for line in puzzle.splitlines():
        numbers = get_digits(line) if part == "a" else get_numbers(line)
        assert len(numbers) >= 1
        value = (word_to_number(numbers[0]) * 10) + word_to_number(
            numbers[-1]
        )
        assert value >= 10
        assert value <= 99
        if part == "b":
            LOG.info(
                "%s -> [%s, %s] -> %s", line, numbers[0], numbers[-1], value
            )
        retval += value

    LOG.info("Returning %s", retval)
    return retval
