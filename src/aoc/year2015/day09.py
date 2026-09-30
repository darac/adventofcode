# Copyright (c) 2015 Paul Saunders
# spell-checker: disable
"""
--- Day 9: All in a Single Night ---
Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have
provided him the distances between every pair of locations. He can start
and end at any two (different) locations he wants, but he must visit each
location exactly once. What is the shortest distance he can travel to
achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141

The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982

The shortest of these is London -> Dublin -> Belfast = 605, and so the
answer is 605 in this example.

What is the distance of the shortest route?

--- Part Two ---
The next year, just to show off, Santa decides to take the route with the
longest distance instead.

He can still start and end at any two (different) locations he wants, and
he still must visit each location exactly once.

For example, given the distances above, the longest route would be 982 via
(for example) Dublin -> London -> Belfast.

What is the distance of the longest route?

"""
# spell-checker: enable

import itertools
import logging
from typing import Literal

import parse

LOG = logging.getLogger(__name__)


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | None:

    route_parser = parse.compile("{} to {} = {:d}")
    roads = {}
    shortest_route = 0
    longest_route = 0

    for line in puzzle.splitlines():
        p = route_parser.parse(line)
        if p[0] not in roads:
            roads[p[0]] = {}
        if p[1] not in roads:
            roads[p[1]] = {}
        # Forward route
        roads[p[0]][p[1]] = p[2]
        # Reverse Route
        roads[p[1]][p[0]] = p[2]

        # We don't want to report 0 as an answer, so
        # add road lengths to ensure we have a "max"
        # to work against
        shortest_route += p[2]

    for route in itertools.permutations(roads.keys()):
        current_route = 0
        LOG.debug("%s", " -> ".join(route))
        for src, dest in itertools.pairwise(route):
            current_route += roads[src][dest]
        shortest_route = min(shortest_route, current_route)
        longest_route = max(longest_route, current_route)
        LOG.debug(
            "Current Route: %d, "
            "Shortest Route now: %d, "
            "Longest Route now: %d",
            current_route,
            shortest_route,
            longest_route,
        )

    return shortest_route if part == "a" else longest_route
