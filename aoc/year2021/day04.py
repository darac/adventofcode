#!env python3
"""
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean,
already so deep that you can't see any sunlight. What you can see, however,
is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards
on which it appears. (Numbers may not appear on all boards.) If all numbers
in any row or any column of a board are marked, that board wins. (Diagonals
don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and
the giant squid) pass the time. It automatically generates a random order
in which to draw numbers and a random set of boards (your puzzle input).
For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no
winners, but the boards are marked as follows (shown here adjacent to each
other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are
still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete
row or column of marked numbers (in this case, the entire top row is
marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding
the sum of all unmarked numbers on that board; in this case, the sum
is 188. Then, multiply that sum by the number that was just called when
the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will
win first. What will your final score be if you choose that board?

--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the
giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so
rather than waste time counting its arms, the safe thing to do is to figure
out which board will win last and choose that one. That way, no matter which
boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens
after 13 is eventually called and its middle column is completely marked.
If you were to keep playing until this point, the second board would have a
sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final
score be?
"""

import logging
import sys
from typing import Literal, Optional

from aocd import submit
from aocd.models import Puzzle
from rich import print, traceback
from rich.live import Live
from rich.logging import RichHandler
from rich.table import Table

traceback.install(show_locals=True)
FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
LOG = logging.getLogger()

PUZZLE = Puzzle(year=2021, day=4)
INPUT = PUZZLE.input_data
SAMPLE_INPUT = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


class Bingo(Exception):
    """Thrown when a board bingos. Stores the winning board"""

    def __init__(self, winner):
        super().__init__()
        self.board = winner


class BingoSquare:
    """Implements a square of the bingo board"""

    def __init__(self, value: Optional[int]):
        """Init Method

        Args:
            value (int, optional): The number in the square. Defaults to None.
        """
        self.value = value
        self.hit = False

    def set(self, value: int):
        """Sets the value of the square. If a value is already set,
        logs a warning.

        Args:
            value (int): the number to set
        """
        if self.value is None:
            self.value = value
        else:
            LOG.warning("Can't set a bingo square twice")

    def get(self) -> int:
        """Returns the number in the square

        Returns:
            int: The number in the square
        """
        assert self.value is not None
        return self.value

    def test(self, value: Optional[int] = None) -> bool:
        """Test the value against a call. Latches TRUE

        Args:
            value (int): The call to test against

        Returns:
            bool: True if the square has ever been hit
        """
        if value is not None:
            self.hit |= self.value == value
        return self.hit

    def clear(self):
        """Clears the square's HIT value"""
        self.hit = False

    def __str__(self):
        """Stringify"""
        if self.hit:
            fmt = "red"
        else:
            fmt = "default"
        return f"[{fmt}]{self.value:2}[/]"


class BingoBoard:
    """Implements the Bingo Board"""

    def __init__(self, board_id: int):
        """Init Method"""
        self.board: list[list[BingoSquare]] = []
        self.board_id = board_id
        self._has_won = False
        self.last_call: Optional[int] = None

    def load_row(self, row: list[str]):
        """Loads a row into the Board

        Args:
            row (list): A list of ints
        """
        board_row: list[BingoSquare] = []
        for item in row:
            board_row.append(BingoSquare(int(item)))
        self.board.append(board_row)
        if len(self.board) > 5:
            LOG.warning("The board looks big :(")

    def check_bingo(self):
        """Checks the board for Bingo
        First, we check each row, then we check each column

        Raises:
            Bingo: when this board wins
        """
        column_checks = [0, 0, 0, 0, 0]
        for row in self.board:
            row_check = all(x.test() for x in row)
            if row_check:
                # This row is all lit up
                self._has_won = True
                raise Bingo(winner=self)
            for col_num, cell in enumerate(row):
                if cell.test():
                    column_checks[col_num] += 1
        if any(x == 5 for x in column_checks):
            self._has_won = True
            raise Bingo(self)

    def has_won(self) -> bool:
        """Check if this board has ever won

        Returns:
            bool: True if this board has ever won
        """
        return bool(self._has_won)

    def test(self, value: Optional[int] = None):
        """Check all cells in this board against the call.
        Calls "check_bingo()" at the end

        Args:
            value (int): The Call
        """
        self.last_call = value
        for row in self.board:
            for cell in row:
                cell.test(value)
        self.check_bingo()

    def as_table(self) -> Table:
        """Returns the table as a Rich Table (for printing)

        Returns:
            Table: a Rich Table
        """
        table = Table(
            title=f"Board #{self.board_id}. Last Call: {self.last_call}",
            show_header=False,
        )
        for _ in self.board[0]:
            table.add_column()
        for row in self.board:
            table.add_row(*[str(x) for x in row])
        return table

    def score(self) -> int:
        """Calculates the score.
        Defined as sum of unlit cells * the last call

        Returns:
            int: Score
        """
        assert self.last_call is not None
        value: int = 0
        for row in self.board:
            for cell in row:
                if not cell.test():
                    value += cell.get()
        return int(value * self.last_call)


def parse_input(input: str) -> dict:
    """Parse the Input

    Args:
        input (str): AOC input

    Returns:
        dict: Draws and Boards
    """
    draws = [int(n) for n in input.splitlines()[0].split(",")]
    print(f"Got {len(draws)} draws")
    boards: list[BingoBoard] = []

    this_board: Optional[BingoBoard] = None
    for line in input.splitlines()[1:]:
        logging.debug("Reading Row >>%s<<", line)
        if line == "":
            if this_board is not None:
                print(this_board.as_table())
                boards.append(this_board)
            this_board = BingoBoard(board_id=len(boards))
        else:
            assert this_board is not None
            this_board.load_row(line.split())
    if this_board is not None:
        print(this_board.as_table())
        boards.append(this_board)

    return {"draws": draws, "boards": boards}


def generate_table(boards: list) -> Table:
    """Re-generates the tables during debugging

    Args:
        boards ([list]): List of boards to print

    Returns:
        Table: a Rich Table
    """
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column()
    grid.add_column()
    grid.add_row(boards[0].as_table(), boards[1].as_table(), boards[2].as_table())
    return grid


def solve(input: str, part: Literal["a", "b"], _runner: bool = False) -> Optional[int]:
    LOG.setLevel(logging.ERROR if _runner else logging.INFO)

    data = parse_input(input)
    remaining_boards = len(data["boards"])
    last_board = None
    for draw in data["draws"]:
        LOG.info("Calling %2d", draw)
        for board in data["boards"]:
            if board.has_won() or remaining_boards == 0:
                continue
            try:
                board.test(draw)
            except Bingo as board:
                last_board = board.board
                remaining_boards = sum([not x.has_won() for x in data["boards"]])
                LOG.info("Got a Bingo on board%d", board.board.board_id)
                LOG.info("%d boards remain in play", remaining_boards)
                if part == "a":
                    LOG.debug(board.board.as_table())
                    return int(board.board.score())
    assert last_board is not None
    LOG.debug(last_board.as_table())
    return int(last_board.score())


if __name__ == "__main__":
    SUBMITTED_A = False
    SUBMITTED_B = False
    FIRST_BOARD = False
    LAST_BOARD = None
    with Live(Table()) as live:
        DEBUG = len(sys.argv) > 1 and sys.argv[1] == "test"
        if DEBUG:
            data = parse_input(SAMPLE_INPUT)
        else:
            data = parse_input(INPUT)
        REMAINING_BOARDS = len(data["boards"])
        for draw in data["draws"]:
            logging.info("Calling %2d", draw)
            for board in data["boards"]:
                if not board.has_won():
                    try:
                        board.test(draw)
                    except Bingo as board:
                        LAST_BOARD = board.board
                        REMAINING_BOARDS = sum([not x.has_won() for x in data["boards"]])
                        logging.info("Got a Bingo on board %d", board.board.board_id)
                        logging.info(
                            "%d boards remain in play",
                            REMAINING_BOARDS,
                        )
                        if not FIRST_BOARD:
                            # We've not reported the first board yet.
                            print(board.board.as_table())
                            print(f"Score: {board.board.score()}")
                            if not DEBUG and not SUBMITTED_A:
                                submit(board.board.score(), part="a", day=4, year=2021)
                                SUBMITTED_A = True
                            FIRST_BOARD = True
            if REMAINING_BOARDS == 0:
                break

            if DEBUG:
                live.update(generate_table(data["boards"]))
                input("Press enter to continue")
    assert LAST_BOARD is not None
    print(LAST_BOARD.as_table())
    print(f"Score: {LAST_BOARD.score()}")
    if not SUBMITTED_B and not DEBUG:
        submit(LAST_BOARD.score(), part="b", day=4, year=2021)
