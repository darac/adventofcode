# spell-checker: disable
"""
--- Day 6: Wait For It ---

The ferry quickly brings you across Island Island. After asking around, you
discover that there is indeed normally a large pile of sand somewhere near
here, but you don't see anything besides lots of water and the small island
where the ferry has docked.

As you try to figure out what to do next, you notice a poster on a wall
near the ferry dock. "Boat races! Open to the public! Grand prize is an
all-expenses-paid trip to Desert Island!" That must be where the sand comes
from! Best of all, the boat races are starting in just a few minutes.

You manage to sign up as a competitor in the boat races just in time. The
organizer explains that it's not really a traditional race - instead, you
will get a fixed amount of time during which your boat has to travel as far
as it can, and you win if your boat goes the farthest.

As part of signing up, you get a sheet of paper (your puzzle input) that
lists the time allowed for each race and also the best distance ever
recorded in that race. To guarantee you win the grand prize, you need to
make sure you go farther in each race than the current record holder.

The organizer brings you over to the area where the boat races are held.
The boats are much smaller than you expected - they're actually toy boats,
each with a big button on top. Holding down the button charges the boat,
and releasing the button allows the boat to move. Boats move faster if
their button was held longer, but time spent holding the button counts
against the total race time. You can only hold the button at the start of
the race, and boats don't move until the button is released.

For example:

  Time:      7  15   30
  Distance:  9  40  200

This document describes three races:

  - The first race lasts 7 milliseconds. The record distance in this race
    is 9 millimeters.
  - The second race lasts 15 milliseconds. The record distance in this
    race is 40 millimeters.
  - The third race lasts 30 milliseconds. The record distance in this race
    is 200 millimeters.

Your toy boat has a starting speed of zero millimeters per millisecond. For
each whole millisecond you spend at the beginning of the race holding down
the button, the boat's speed increases by one millimeter per millisecond.

So, because the first race lasts 7 milliseconds, you only have a few
options:

  - Don't hold the button at all (that is, hold it for 0 milliseconds) at
    the start of the race. The boat won't move; it will have traveled 0
    millimeters by the end of the race.
  - Hold the button for 1 millisecond at the start of the race. Then, the
    boat will travel at a speed of 1 millimeter per millisecond for 6
    milliseconds, reaching a total distance traveled of 6 millimeters.
  - Hold the button for 2 milliseconds, giving the boat a speed of 2
    millimeters per millisecond. It will then get 5 milliseconds to move,
    reaching a total distance of 10 millimeters.
  - Hold the button for 3 milliseconds. After its remaining 4 milliseconds
    of travel time, the boat will have gone 12 millimeters.
  - Hold the button for 4 milliseconds. After its remaining 3 milliseconds
    of travel time, the boat will have gone 12 millimeters.
  - Hold the button for 5 milliseconds, causing the boat to travel a total
    of 10 millimeters.
  - Hold the button for 6 milliseconds, causing the boat to travel a total
    of 6 millimeters.
  - Hold the button for 7 milliseconds. That's the entire duration of the
    race. You never let go of the button. The boat can't move until you
    let go of the button. Please make sure you let go of the button so the
    boat gets to move. 0 millimeters.

Since the current record for this race is 9 millimeters, there are actually
4 different ways you could win: you could hold the button for 2, 3, 4, or 5
milliseconds at the start of the race.

In the second race, you could hold the button for at least 4 milliseconds
and at most 11 milliseconds and beat the record, a total of 8 different
ways to win.

In the third race, you could hold the button for at least 11 milliseconds
and no more than 19 milliseconds and still beat the record, a total of 9
ways you could win.

To see how much margin of error you have, determine the number of ways you
can beat the record in each race; in this example, if you multiply these
values together, you get 288 (4 * 8 * 9).

Determine the number of ways you could beat the record in each race. What
do you get if you multiply these numbers together?

--- Part Two ---

As the race is about to start, you realize the piece of paper with race
times and record distances you got earlier actually just has very bad
kerning. There's really only one race - ignore the spaces between the
numbers on each line.

So, the example from before:

  Time:      7  15   30
  Distance:  9  40  200

...now instead means this:

  Time:      71530
  Distance:  940200

Now, you have to figure out how many ways there are to win this single
race. In this example, the race lasts for 71530 milliseconds and the record
distance you need to beat is 940200 millimeters. You could hold the button
anywhere from 14 to 71516 milliseconds and beat the record, a total of
71503 ways!

How many ways can you beat the record in this one much longer race?

"""
# spell-checker: enable

import logging
import math
from typing import Literal

logging.basicConfig(  # NOSONAR
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
)
LOG = logging.getLogger()


def get_winning_bounds(
    game_time: int, distance_to_beat: int
) -> tuple[int, int] | None:
    # Thoughts:
    #   speed = press_time  # noqa: ERA001
    #   distance = speed * (total_time - press_time)  # noqa: ERA001
    # ∴ distance = press_time * (total_time - press_time)
    #   So we have y = x * (c - y) and y = t. Find x, then round (inwards).
    #   https://www.bbc.co.uk/bitesize/guides/zqf3k2p/revision/4 :D
    #
    #   For the first game, when game_time = 7 and distance = 9,
    #     y = x * (7 - x). Find x, when y = 9.
    # ∴ x * (7 - x) = 9
    # ∴ x * (7 - x) - 9 = 0
    # ∴ 7x - x² - 9 = 0
    # ∴ -x² + 7x - 9 = 0
    #   Quadratic Formula: x = -b ± √(b²) - 4ac / 2a
    #   a = -1, b = game_time, c = -(distance_to_beat)
    # ∴ x = -7 ± sqrt(7² - 4(-1)(-9)) / 2(-1)
    #   This should be enough for python to calculate.

    LOG.debug("Game time: %d, Distance: %d", game_time, distance_to_beat)

    a = -1
    b = game_time
    c = -distance_to_beat

    upper = (-b - math.sqrt(pow(b, 2) - 4 * a * c)) / (2 * a)
    lower = (-b + math.sqrt(pow(b, 2) - 4 * a * c)) / (2 * a)
    assert lower <= upper, (
        f"{lower} ({math.ceil(lower)}) not less than {upper} "
        f"({math.floor(upper)})"
    )

    LOG.debug("Maths gave us (%.3f, %.3f)", lower, upper)
    lower = math.ceil(lower)
    upper = math.floor(upper)
    LOG.debug("Rounding that to (%d, %d)", lower, upper)

    # Could use max() and min(), but I want to log this
    if lower < 0:
        LOG.debug("Capping lower to 0")
        lower = 0

    if upper > game_time:
        LOG.debug("Capping upper to game_time (%d)", game_time)
        upper = game_time

    # Equalling the record won't work, so we may need to push the envelope.
    if lower * (game_time - lower) <= distance_to_beat:
        LOG.debug(
            "%d would give us %.3f", lower, lower * (game_time - lower)
        )
        LOG.debug(
            "%d isn't good enough to beat %d, bumping to %d",
            lower,
            distance_to_beat,
            lower + 1,
        )
        lower += 1
    if upper * (game_time - upper) <= distance_to_beat:
        LOG.debug(
            "%d isn't good enough to beat %d, bumping to %d",
            upper,
            distance_to_beat,
            upper - 1,
        )
        upper -= 1

    LOG.info("Returning (%d, %d)", lower, upper)

    if lower <= upper:
        return (math.ceil(lower), math.floor(upper))
    return None


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    if part == "a":
        races = list(
            zip(
                *[
                    [int(value) for value in line.split()[1:]]
                    for line in puzzle.splitlines()
                ],
                strict=True,
            )
        )
    else:
        (times, distances) = (
            line.split(":")[1] for line in puzzle.splitlines()
        )
        LOG.info("Time: %s, Distance: %s", times, distances)
        races = [
            (int("".join(times.split())), int("".join(distances.split())))
        ]

    retval = []
    for race_time, race_distance in races:
        result = get_winning_bounds(race_time, race_distance)
        if result is not None:
            retval.append(abs(result[1] - result[0]) + 1)

    return math.prod(retval)
