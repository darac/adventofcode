# spell-checker: disable
"""
--- Day 2: Red-Nosed Reports ---

Fortunately, the first location The Historians want to search isn't a long
walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to
contain no sign of the Chief Historian, the engineers there run up to you
as soon as they see you. Apparently, they still talk about the time Rudolph
was saved through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really
appreciate your help analyzing some unusual data from the Red-Nosed
reactor. You turn to check if The Historians are waiting for you, but they
seem to have already divided into groups that are currently searching every
corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report
per line. Each report is a list of numbers called levels that are separated
by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9

This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-
Nosed reactor safety systems can only tolerate levels that are either
gradually increasing or gradually decreasing. So, a report only counts as
safe if both of the following are true:

  - The levels are either all increasing or all decreasing.
  - Any two adjacent levels differ by at least one and at most three.

In the example above, the reports can be found safe or unsafe by checking
those rules:

  - 7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
  - 1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
  - 9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
  - 1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
  - 8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
  - 1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.

So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?

--- Part Two ---

The engineers are surprised by the low number of safe reports until they
realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor
safety systems tolerate a single bad level in what would otherwise be a
safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from
an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

  - 7 6 4 2 1: Safe without removing any level.
  - 1 2 7 8 9: Unsafe regardless of which level is removed.
  - 9 7 6 2 1: Unsafe regardless of which level is removed.
  - 1 3 2 4 5: Safe by removing the second level, 3.
  - 8 6 4 4 1: Safe by removing the third level, 4.
  - 1 3 6 7 9: Safe without removing any level.

Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can
remove a single level from unsafe reports. How many reports are now safe?
"""
# spell-checker: enable

import itertools
import logging
import textwrap
from collections.abc import Iterable
from typing import Literal

logging.basicConfig(  # NOSONAR
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
)
LOG = logging.getLogger()


def check_safety(levels: Iterable[int]) -> bool:
    diffs = [
        current - previous
        for previous, current in itertools.pairwise(levels)
    ]
    if any(diff == 0 for diff in diffs):
        LOG.debug(
            "%30s: Unsafe because there is a zero diff",
            textwrap.shorten(" ".join(map(str, levels)), width=30),
        )
        return False
    if not all(diff > 0 for diff in diffs) and not all(
        diff < 0 for diff in diffs
    ):
        LOG.debug(
            "%30s: Unsafe because there is a change in direction",
            textwrap.shorten(" ".join(map(str, levels)), width=30),
        )
        return False
    if any(abs(diff) > 3 for diff in diffs):
        LOG.debug(
            "%30s: Unsafe because there is a diff of more than three",
            textwrap.shorten(" ".join(map(str, levels)), width=30),
        )
        return False
    LOG.debug(
        "%30s: Safe", textwrap.shorten(" ".join(map(str, levels)), width=30)
    )
    return True


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    if part == "a":
        return sum(
            check_safety(list(map(int, line.split())))
            for line in puzzle.splitlines()
        )

    result = 0
    for line in puzzle.splitlines():
        levels = list(map(int, line.split()))
        if any(
            check_safety(level_combo)
            for level_combo in itertools.combinations(
                levels, len(levels) - 1
            )
        ):
            result += 1

    return result
