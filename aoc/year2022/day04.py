#!env python
"""
--- Day 4: Camp Cleanup ---
Space needs to be cleared before the last supplies can be unloaded from the
ships, and so several Elves have been assigned the job of cleaning up
sections of the camp. Every section has a unique ID number, and each Elf is
assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each
other, they've noticed that many of the assignments overlap. To try to
quickly find overlaps and reduce duplicated effort, the Elves pair up and
make a big list of the section assignments for each pair (your puzzle
input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

For the first few pairs, this list means:

 - Within the first pair of Elves, the first Elf was assigned sections
   2-4 (sections 2, 3, and 4), while the second Elf was assigned sections
   6-8 (sections 6, 7, 8).
 - The Elves in the second pair were each assigned two sections.
 - The Elves in the third pair were each assigned three sections: one got
   sections 5, 6, and 7, while the other also got 7, plus 8 and 9.

This example list uses single-digit section IDs to make it easier to draw;
your actual list might contain larger numbers. Visually, these pairs of
section assignments look like this:


.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8
Some of the pairs have noticed that one of their assignments fully contains
the other. For example, 2-8 fully contains 3-7, and 6-6 is fully contained
by 4-6. In pairs where one assignment fully contains the other, one Elf in
the pair would be exclusively cleaning sections their partner will already
be cleaning, so these seem like the most in need of reconsideration. In
this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?
"""
import sys
from typing import Literal, Optional

import pytest
from parse import compile
from rich import print


@pytest.fixture
def example_data():
    return {
        "input": """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""",
        "a": 2,
        "b": 4,
    }


def test_solve_a(example_data):
    if example_data.get("a") is not None:
        assert solve(input=example_data["input"], part="a") == example_data["a"]


def test_solve_b(example_data):
    if example_data.get("b") is not None:
        assert solve(input=example_data["input"], part="b") == example_data["b"]


def visualise(low: int, high: int, upper: int, char: str = "+") -> str:
    output = "-" * (low - 1)
    output += char * (high - low + 1)
    output += "-" * (upper - high + 1)
    return output


def solve(input: str, part: Literal["a", "b"]) -> Optional[int]:
    count = 0
    parser = compile("{:d}-{:d},{:d}-{:d}")
    for line in input.splitlines():
        results = parser.parse(line)
        if results:
            a_low, a_high, b_low, b_high = parser.parse(line)  # type: ignore
            o_low = o_high = 0
            assert a_low <= a_high, "Whoops, Pairs are not sorted"
            assert b_low <= b_high, "Whoops, Pairs are not sorted"
            print(visualise(a_low, a_high, max(a_high, b_high), "A"))
            print(visualise(b_low, b_high, max(a_high, b_high), "B"))
            if part == "a":
                if (a_low >= b_low and a_high <= b_high) or (
                    b_low >= a_low and b_high <= a_high
                ):
                    o_low = max(a_low, b_low)
                    o_high = min(a_high, b_high)
                    count += 1
            else:
                if (a_high >= b_low and a_low <= b_high) or (
                    b_high >= a_low and b_low <= a_high
                ):
                    o_low = max(a_low, b_low)
                    o_high = min(a_high, b_high)
                    count += 1
            print(
                visualise(o_low, o_high, max(a_high, b_high), "O"),
                "<--" if o_low != o_high else "",
            )
            print("\n")

    return count


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
