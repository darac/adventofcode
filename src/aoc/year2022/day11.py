# Copyright (c) 2022 Paul Saunders
# spell-checker: disable
"""
--- Day 11: Monkey in the Middle ---

As you finally start making your way upriver, you realize your pack is much
lighter than you remember. Just then, one of the items from your pack goes
flying overhead. Monkeys are playing Keep Away with your missing things!

To get your stuff back, you need to be able to predict where the monkeys
will throw your items. After some careful observation, you realize the
monkeys operate based on how worried you are about each item.

You take some notes (your puzzle input) on the items each monkey currently
has, how worried you are about those items, and how the monkey makes
decisions based on your worry level. For example:

Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1

Each monkey has several attributes:

  - Starting items lists your worry level for each item the monkey is
    currently holding in the order they will be inspected.
  - Operation shows how your worry level changes as that monkey inspects an
    item. (An operation like new = old * 5 means that your worry level after
    the monkey inspected the item is five times whatever your worry level
    was before inspection.)
  - Test shows how the monkey uses your worry level to decide where to throw
    an item next.
      - If true shows what happens with an item if the Test was true.
      - If false shows what happens with an item if the Test was false.

After each monkey inspects an item but before it tests your worry level,
your relief that the monkey's inspection didn't damage the item causes your
worry level to be divided by three and rounded down to the nearest integer.

The monkeys take turns inspecting and throwing items. On a single monkey's
turn, it inspects and throws all of the items it is holding one at a time
and in the order listed. Monkey 0 goes first, then monkey 1, and so on until
each monkey has had one turn. The process of each monkey taking a single
turn is called a round.

When a monkey throws an item to another monkey, the item goes on the end of
the recipient monkey's list. A monkey that starts a round with no items
could end up inspecting and throwing many items by the time its turn comes
around. If a monkey is holding no items at the start of its turn, its turn
ends.

In the above example, the first round proceeds as follows:

Monkey 0:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by 19 to 1501.
    Monkey gets bored with item. Worry level is divided by 3 to 500.
    Current worry level is not divisible by 23.
    Item with worry level 500 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 98.
    Worry level is multiplied by 19 to 1862.
    Monkey gets bored with item. Worry level is divided by 3 to 620.
    Current worry level is not divisible by 23.
    Item with worry level 620 is thrown to monkey 3.
Monkey 1:
  Monkey inspects an item with a worry level of 54.
    Worry level increases by 6 to 60.
    Monkey gets bored with item. Worry level is divided by 3 to 20.
    Current worry level is not divisible by 19.
    Item with worry level 20 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 65.
    Worry level increases by 6 to 71.
    Monkey gets bored with item. Worry level is divided by 3 to 23.
    Current worry level is not divisible by 19.
    Item with worry level 23 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 75.
    Worry level increases by 6 to 81.
    Monkey gets bored with item. Worry level is divided by 3 to 27.
    Current worry level is not divisible by 19.
    Item with worry level 27 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 6 to 80.
    Monkey gets bored with item. Worry level is divided by 3 to 26.
    Current worry level is not divisible by 19.
    Item with worry level 26 is thrown to monkey 0.
Monkey 2:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by itself to 6241.
    Monkey gets bored with item. Worry level is divided by 3 to 2080.
    Current worry level is divisible by 13.
    Item with worry level 2080 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 60.
    Worry level is multiplied by itself to 3600.
    Monkey gets bored with item. Worry level is divided by 3 to 1200.
    Current worry level is not divisible by 13.
    Item with worry level 1200 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 97.
    Worry level is multiplied by itself to 9409.
    Monkey gets bored with item. Worry level is divided by 3 to 3136.
    Current worry level is not divisible by 13.
    Item with worry level 3136 is thrown to monkey 3.
Monkey 3:
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 3 to 77.
    Monkey gets bored with item. Worry level is divided by 3 to 25.
    Current worry level is not divisible by 17.
    Item with worry level 25 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 500.
    Worry level increases by 3 to 503.
    Monkey gets bored with item. Worry level is divided by 3 to 167.
    Current worry level is not divisible by 17.
    Item with worry level 167 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 620.
    Worry level increases by 3 to 623.
    Monkey gets bored with item. Worry level is divided by 3 to 207.
    Current worry level is not divisible by 17.
    Item with worry level 207 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 1200.
    Worry level increases by 3 to 1203.
    Monkey gets bored with item. Worry level is divided by 3 to 401.
    Current worry level is not divisible by 17.
    Item with worry level 401 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 3136.
    Worry level increases by 3 to 3139.
    Monkey gets bored with item. Worry level is divided by 3 to 1046.
    Current worry level is not divisible by 17.
    Item with worry level 1046 is thrown to monkey 1.

After round 1, the monkeys are holding items with these worry levels:

Monkey 0: 20, 23, 27, 26
Monkey 1: 2080, 25, 167, 207, 401, 1046
Monkey 2:
Monkey 3:

Monkeys 2 and 3 aren't holding any items at the end of the round; they both
inspected items during the round and threw them all before the round ended.

This process continues for a few more rounds:

After round 2, the monkeys are holding items with these worry levels:
Monkey 0: 695, 10, 71, 135, 350
Monkey 1: 43, 49, 58, 55, 362
Monkey 2:
Monkey 3:

After round 3, the monkeys are holding items with these worry levels:
Monkey 0: 16, 18, 21, 20, 122
Monkey 1: 1468, 22, 150, 286, 739
Monkey 2:
Monkey 3:

After round 4, the monkeys are holding items with these worry levels:
Monkey 0: 491, 9, 52, 97, 248, 34
Monkey 1: 39, 45, 43, 258
Monkey 2:
Monkey 3:

After round 5, the monkeys are holding items with these worry levels:
Monkey 0: 15, 17, 16, 88, 1037
Monkey 1: 20, 110, 205, 524, 72
Monkey 2:
Monkey 3:

After round 6, the monkeys are holding items with these worry levels:
Monkey 0: 8, 70, 176, 26, 34
Monkey 1: 481, 32, 36, 186, 2190
Monkey 2:
Monkey 3:

After round 7, the monkeys are holding items with these worry levels:
Monkey 0: 162, 12, 14, 64, 732, 17
Monkey 1: 148, 372, 55, 72
Monkey 2:
Monkey 3:

After round 8, the monkeys are holding items with these worry levels:
Monkey 0: 51, 126, 20, 26, 136
Monkey 1: 343, 26, 30, 1546, 36
Monkey 2:
Monkey 3:

After round 9, the monkeys are holding items with these worry levels:
Monkey 0: 116, 10, 12, 517, 14
Monkey 1: 108, 267, 43, 55, 288
Monkey 2:
Monkey 3:

After round 10, the monkeys are holding items with these worry levels:
Monkey 0: 91, 16, 20, 98
Monkey 1: 481, 245, 22, 26, 1092, 30
Monkey 2:
Monkey 3:

...

After round 15, the monkeys are holding items with these worry levels:
Monkey 0: 83, 44, 8, 184, 9, 20, 26, 102
Monkey 1: 110, 36
Monkey 2:
Monkey 3:

...

After round 20, the monkeys are holding items with these worry levels:
Monkey 0: 10, 12, 14, 26, 34
Monkey 1: 245, 93, 53, 199, 115
Monkey 2:
Monkey 3:

Chasing all of the monkeys at once is impossible; you're going to have to
focus on the two most active monkeys if you want any hope of getting your
stuff back. Count the total number of times each monkey inspects items over
20 rounds:

Monkey 0 inspected items 101 times.
Monkey 1 inspected items 95 times.
Monkey 2 inspected items 7 times.
Monkey 3 inspected items 105 times.

In this example, the two most active monkeys inspected items 101 and 105
times. The level of monkey business in this situation can be found by
multiplying these together: 10605.

Figure out which monkeys to chase by counting how many items they inspect
over 20 rounds. What is the level of monkey business after 20 rounds of
stuff-slinging simian shenanigans?
"""
# spell-checker: enable

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial
from math import prod
from typing import Literal

import parse


class Monkey:
    def __init__(
        self: "Monkey",
        starting_items: list[int],
        operation: Callable[[int], int],
        test: Callable[[int], bool],
        throw_targets: dict[bool, int],
    ) -> None:
        self.starting_items = starting_items
        self.operation = operation
        self.test = test
        self.throw_targets = throw_targets
        self.inspect_count = 0

    def inspect(self: "Monkey") -> None:
        for item in self.starting_items:
            LOG.debug(
                "  Monkey inspects an item with a worry level of %d.", item
            )
            inspected: int = self.operation(item)
            LOG.debug("  Worry level is increased to %d.", inspected)
            self.inspect_count += 1
            inspected = int(inspected / 3)
            LOG.debug(
                (
                    "  Monkey gets bored with item. Worry level is "
                    "divided by 3 to %d."
                ),
                inspected,
            )
            LOG.debug(
                "  Current worry level %s divisible.",
                "is" if self.test(inspected) else "is not",
            )
            assert self.throw_targets[self.test(inspected)] is not None
            LOG.debug(
                "  Item with worry level %d is thrown to monkey %d.",
                inspected,
                self.throw_targets[self.test(inspected)],
            )
            self.throw(
                item=inspected,
                target=self.throw_targets[self.test(inspected)],
            )
        self.starting_items = []

    def catch(self: "Monkey", item: int) -> None:
        self.starting_items.append(item)

    def throw(self: "Monkey", item: int, target: int) -> None:
        MONKEYS[target].catch(item)

    def score(self: "Monkey") -> int:
        return self.inspect_count

    def items(self: "Monkey") -> list[int]:
        return self.starting_items


@dataclass
class Pending:
    monkey: int = 0
    holding: list[int] = field(default_factory=list)
    targets: dict[bool, int] = field(default_factory=dict)
    operation: Callable = field(default=lambda x: x)
    test: Callable = field(default=lambda x: x)


MONKEYS: dict[int, Monkey] = {}
LOG = logging.getLogger(__name__)


def play_rounds(num_rounds: int) -> None:
    starting_items_num = sum(
        [len(monkey.starting_items) for monkey in MONKEYS.values()]
    )
    for game in range(num_rounds):
        LOG.info("Round %d/%d", game, num_rounds)
        for monkey_id, monkey in MONKEYS.items():
            LOG.debug("Monkey %s:", monkey_id)
            monkey.inspect()
            assert len(monkey.starting_items) == 0
            assert (
                sum(
                    [
                        len(monkey.starting_items)
                        for monkey in MONKEYS.values()
                    ]
                )
                == starting_items_num
            ), (
                f"Started with {starting_items_num} items. Now have "
                + str(
                    [
                        len(monkey.starting_items)
                        for monkey in MONKEYS.values()
                    ]
                )
                + " == "
                + str(
                    sum(
                        [
                            len(monkey.starting_items)
                            for monkey in MONKEYS.values()
                        ]
                    )
                )
            )
        for monkey_id, monkey in MONKEYS.items():
            LOG.info(
                "Monkey %d: %s",
                monkey_id,
                ", ".join(map(str, monkey.items())),
            )
    assert (
        sum([len(monkey.starting_items) for monkey in MONKEYS.values()])
        == starting_items_num
    )


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | str | None:
    pending = Pending()
    MONKEYS.clear()
    for line in puzzle.splitlines():
        LOG.debug("»%s«", line)
        if p := parse.parse("Monkey {monkey:d}:", line):
            assert isinstance(p, parse.Result)
            if len(pending.holding):
                LOG.info(
                    "Creating #%d with %d items",
                    pending.monkey,
                    len(pending.holding),
                )
                MONKEYS[pending.monkey] = Monkey(
                    starting_items=pending.holding,
                    operation=pending.operation,
                    test=pending.test,
                    throw_targets=pending.targets,
                )
            LOG.info("Parsing next monkey #%d", p["monkey"])
            pending = Pending(
                monkey=p["monkey"],
                targets={True: -1, False: -1},
            )
        elif p := parse.parse("  Starting items: {items}", line):
            assert isinstance(p, parse.Result)
            pending.holding = list(map(int, p["items"].split(", ")))
            LOG.debug(
                "Added %d items: %s", len(pending.holding), pending.holding
            )
        elif p := parse.parse("  Operation: new = old {operation}", line):
            assert isinstance(p, parse.Result)
            operator, value = p["operation"].split()
            if operator == "*" and value == "old":
                pending.operation = lambda x: x * x
            elif operator == "*":
                pending.operation = partial(
                    lambda x, v: x * int(v), v=value
                )
            elif operator == "+":
                pending.operation = partial(
                    lambda x, v: x + int(v), v=value
                )
            else:  # pragma: no cover
                LOG.warning(
                    "Don't recognise operation: new = old %s",
                    p["operation"],
                )
        elif p := parse.parse("  Test: divisible by {val:d}", line):
            assert isinstance(p, parse.Result)
            pending.test = partial(lambda x, m: (x % m) == 0, m=p["val"])
        elif p := parse.parse(
            "    If {test}: throw to monkey {monkey:d}", line
        ):
            assert isinstance(p, parse.Result)
            pending.targets[p["test"] == "true"] = p["monkey"]
            if pending.targets[True] != -1 and pending.targets[False] != 1:
                LOG.debug(pending.targets)
    LOG.info(
        "Create #%d with %d items",
        pending.monkey,
        len(pending.holding),
    )
    MONKEYS[pending.monkey] = Monkey(
        starting_items=pending.holding,
        operation=pending.operation,
        test=pending.test,
        throw_targets=pending.targets,
    )

    play_rounds(20 if part == "a" else 200)
    for monkey_id, monkey in MONKEYS.items():
        LOG.info(
            "Monkey %d inspected items %d items.",
            monkey_id,
            monkey.score(),
        )
    LOG.info(
        "Top 2 monkeys are %s",
        sorted(MONKEYS[m].score() for m in MONKEYS)[-2:],
    )
    return prod(sorted(MONKEYS[m].score() for m in MONKEYS)[-2:])


if __name__ == "__main__":
    from rich.logging import RichHandler

    logging.basicConfig(
        level="DEBUG",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()],
    )
    LOG = logging.getLogger(__name__)
    LOG.warning("Starting main")

    from aocd.models import Puzzle

    p = Puzzle(year=2022, day=11)
    result = solve(puzzle=p.input_data, part="a", _runner=True)
    LOG.info("Part A -> %r (%s)", result, type(result))
    assert result == p.answer_a
