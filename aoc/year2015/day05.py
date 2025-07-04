# spell-checker: disable
"""
--- Day 5: Doesn't He Have Intern-Elves For This? ---
Santa needs help figuring out which strings in his text file are naughty or
nice.

A nice string is one with all of the following properties:

 - It contains at least three vowels (aeiou only), like aei, xazegov, or
   aeiouaeiouaeiou.
 - It contains at least one letter that appears twice in a row, like xx,
   abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
 - It does not contain the strings ab, cd, pq, or xy, even if they are
   part of one of the other requirements.

For example:

 - ugknbfddgicrmopn is nice because it has at least three vowels (
   u...i...o...), a double letter (...dd...), and none of the disallowed
   substrings.
 - aaa is nice because it has at least three vowels and a double letter,
   even though the letters used by different rules overlap.
 - jchzalrnumimnmhp is naughty because it has no double letter.
 - haegwjzuvuyypxyu is naughty because it contains the string xy.
 - dvszwmarrgswjxmb is naughty because it contains only one vowel.

How many strings are nice?
"""
# spell-checker: disable

import re
from collections import Counter
from typing import Literal

from aoc.year2015 import LOG


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    num_nice_strings = 0
    for line in puzzle.splitlines():
        counts = Counter(line)
        if (
            part == "a"
            and counts["a"]
            + counts["e"]
            + counts["i"]
            + counts["o"]
            + counts["u"]
            >= 3
            and re.search(r"(.)\1", line)
            and (
                "ab" not in line
                and "cd" not in line
                and "pq" not in line
                and "xy" not in line
            )
        ) or (
            part == "b"
            and re.search(r"(..).*\1", line)
            and re.search(r"(.).\1", line)
        ):
            LOG.debug("%s: %16s: nice", part, line)
            num_nice_strings += 1
        else:
            LOG.debug("%s: %16s: naughty", part, line)
    return num_nice_strings
