import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial
from math import prod
from pathlib import Path
from typing import Literal

import parse
import yaml


class Monkey:
    def __init__(
        self: "Monkey",
        starting_items: list[int],
        operation: Callable[[int], int],
        test: Callable[[int], bool],
        throw_targets: dict[bool, int | None],
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
            inspected = self.operation(item)
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
                target=self.throw_targets[self.test(inspected)],  # type: ignore
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
    targets: dict[bool, int | None] = field(default_factory=dict)
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
        for monkey in MONKEYS:
            LOG.debug("Monkey %s:", monkey)
            MONKEYS[monkey].inspect()
            assert len(MONKEYS[monkey].starting_items) == 0
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
        for monkey in MONKEYS:
            LOG.info(
                "Monkey %d: %s",
                monkey,
                ", ".join(map(str, MONKEYS[monkey].items())),
            )
    assert (
        sum([len(monkey.starting_items) for monkey in MONKEYS.values()])
        == starting_items_num
    )


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> int | str | None:
    pending = Pending()
    for line in puzzle.splitlines():
        LOG.debug("»%s«", line)
        if p := parse.parse("Monkey {monkey:d}:", line):
            assert isinstance(p, parse.Result)
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
            pending = Pending(
                monkey=p["monkey"],
                targets={True: None, False: None},
            )
        elif p := parse.parse("  Starting items: {items}", line):
            assert isinstance(p, parse.Result)
            LOG.debug("Adding %d items", len(p["items"].split(", ")))
            pending.holding = list(map(int, p["items"].split(", ")))
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
        elif p := parse.parse("  Test: divisible by {val:d}", line):
            assert isinstance(p, parse.Result)
            pending.test = partial(lambda x, m: (x % m) == 0, m=p["val"])
        elif p := parse.parse(
            "    If {test}: throw to monkey {monkey:d}", line
        ):
            assert isinstance(p, parse.Result)
            pending.targets[p["test"] == "true"] = p["monkey"]
            LOG.info(pending.targets)
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
    for monkey in MONKEYS:
        LOG.info(
            "Monkey %d inspected items %d items.",
            monkey,
            MONKEYS[monkey].score(),
        )
    return prod(sorted(MONKEYS[m].score() for m in MONKEYS)[2:])


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    LOG.warning("Starting main")
    with Path("tests/year2022/day11.yml").open() as f:
        for doc in yaml.safe_load_all(f):
            result = solve(puzzle=doc["input"], part="a", _runner=False)
            LOG.info("Part A -> %d", result)
            assert result == doc["a"]
