#!env python

from typing import Literal, Optional, Tuple


class RopeFollower:
    def __init__(self, id: int) -> None:
        self.visited: set[Tuple[int, int]] = set()
        self.location: Tuple[int, int] = (0, 0)
        self.id: str = "T" if id == 0 else str(id)

    def move_head(self, leader: Tuple[int, int] = (0, 0)):
        # Moves:
        # 1 2 3 4 5
        # 6 . . . 7
        # 8 . T . 9
        # 0 . . . A
        # B C D E F
        # So there are 16 possible places the head can be in relation to the tail
        # Directions we need to move the head:
        # ↖ ↖ ⬆ ↗ ↗
        # ↖ . . . ↗
        # ⬅ . . . ➡
        # ↙ . . . ↘
        # ↙ ↙ ⬇ ↘ ↘
        match (
            leader[0] - self.location[0],
            leader[1] - self.location[1],
        ):
            case (-2, 1) | (-2, 2) | (-1, 2):
                # North West
                self.location = (self.location[0] - 1, self.location[1] + 1)
            case (0, 2):
                # North
                self.location = (self.location[0], self.location[1] + 1)
            case (1, 2) | (2, 2) | (2, 1):
                # North East
                self.location = (self.location[0] + 1, self.location[1] + 1)
            case (2, 0):
                # East
                self.location = (self.location[0] + 1, self.location[1])
            case (2, -1) | (2, -2) | (1, -2):
                # South East
                self.location = (self.location[0] + 1, self.location[1] - 1)
            case (0, -2):
                # South
                self.location = (self.location[0], self.location[1] - 1)
            case (-2, -1) | (-2, -2) | (-1, -2):
                # South West
                self.location = (self.location[0] - 1, self.location[1] - 1)
            case (-2, 0):
                # West
                self.location = (self.location[0] - 1, self.location[1])

        assert (
            abs(leader[0] - self.location[0]) <= 2
            and abs(leader[1] - self.location[1]) <= 2
        ), f"H{leader}, {self.id}{self.location}"
        self.visited.add(self.location)


def solve(input: str, part: Literal["a", "b"], runner: bool = False) -> Optional[int]:
    head_location = (0, 0)
    knots = []
    for id in range(1 if part == "a" else 9):
        knots.append(RopeFollower(id))
    for line in input.splitlines():
        direction, steps = line.split()

        for _ in range(int(steps)):
            if direction == "R":
                head_location = (head_location[0] + 1, head_location[1])
            elif direction == "L":
                head_location = (head_location[0] - 1, head_location[1])
            elif direction == "U":
                head_location = (head_location[0], head_location[1] + 1)
            elif direction == "D":
                head_location = (head_location[0], head_location[1] - 1)
            else:
                raise NotImplementedError

            prev_knot: Tuple[int, int] = head_location
            for knot in knots:
                knot.move_head(prev_knot)
                prev_knot = knot.location
    return len(knots[-1].visited)
