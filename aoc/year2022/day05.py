# spell-checker: disable
"""
--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded
from the ships. Supplies are stored in stacks of marked crates, but because
the needed supplies are buried under many other crates, the crates need to
be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks.
To ensure none of the crates get crushed or fall over, the crane operator
will rearrange them in a series of carefully-planned steps. After the
crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate
procedure, but they forgot to ask her which crate will end up where, and
they want to be ready to unload them as soon as possible so they can
embark.

They do, however, have a drawing of the starting stacks of crates and the
rearrangement procedure (your puzzle input). For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two
crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains
three crates; from bottom to top, they are crates M, C, and D. Finally,
stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure,
a quantity of crates is moved from one stack to a different stack. In the
first step of the above rearrangement procedure, one crate is moved from
stack 2 to stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

In the second step, three crates are moved from stack 1 to stack 3. Crates
are moved one at a time, so the first crate to be moved (D) ends up below
the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates
are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack;
in this example, the top crates are C in stack 1, M in stack 2, and Z in
stack 3, so you should combine these together and give the Elves the
message CMZ.

After the rearrangement procedure completes, what crate ends up on top of
each stack?


--- Part Two ---
As you watch the crane operator expertly rearrange the crates, you notice
the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly
wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air
conditioning, leather seats, an extra cup holder, and the ability to pick up
and move multiple crates at once.

Again considering the example above, the crates begin in the same
configuration:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

However, the action of moving three crates from stack 1 to stack 3 means
that those three moved crates stay in the same order, resulting in this new
configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3

Next, as both crates are moved from stack 2 to stack 1, they retain their
order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3

Finally, a single crate is still moved from stack 1 to stack 2, but now
it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3

In this example, the CrateMover 9001 has put the crates in a totally
different order: MCD.

Before the rearrangement process finishes, update your simulation so that
the Elves know where they should stand to be ready to unload the final
supplies. After the rearrangement procedure completes, what crate ends up
on top of each stack?
"""

# spell-checker: enable
from collections import deque
from typing import Literal

from parse import Result, compile  # noqa: A004

from aoc.year2022 import LOG


def solve(
    puzzle: str, part: Literal["a", "b"], _runner: bool = False
) -> str | None:
    mode = "crates"
    unnumbered_stacks: dict[int, deque[str]] = {}
    stacks: dict[str, deque[str]] = {}
    parser = compile("move {:d} from {} to {}")
    for line in puzzle.splitlines():
        LOG.debug("%s", line)
        if line == "" and stacks and mode == "crates":
            mode = "instructions"
            continue
        if mode == "crates":
            for stack_number in range(0, len(line), 4):
                crate = line[stack_number : stack_number + 3]
                if crate == "   ":
                    # Empty crate
                    continue
                if "[" in line:
                    # This is a crate specification
                    if unnumbered_stacks.get(stack_number) is None:
                        unnumbered_stacks[stack_number] = deque()
                    unnumbered_stacks[stack_number].appendleft(crate[1])
                else:
                    # This is the list of crate "names"
                    stacks[crate.strip()] = unnumbered_stacks[stack_number]
        elif mode == "instructions":
            r = parser.parse(line)
            assert type(r) is Result
            size_before = len(stacks[str(r[2])])
            assert len(stacks[r[1]]) >= r[0]
            if part == "a":
                # Grab boxes and put them directly on the target
                for _ in range(r[0]):
                    LOG.debug("%s", stacks)
                    stacks[str(r[2])].append(stacks[str(r[1])].pop())
            else:
                # Grab boxes into a holding group, then
                # Put them in order onto the target
                grab: deque[str] = deque()
                for _ in range(r[0]):
                    grab.appendleft(stacks[str(r[1])].pop())
                while len(grab):
                    stacks[r[2]].append(grab.popleft())
            assert len(stacks[str(r[2])]) == size_before + r[0]

    return "".join([x.pop() for x in stacks.values()])
