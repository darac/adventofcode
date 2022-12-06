#!env python3
"""
--- Day 1: Not Quite Lisp ---
// Santa was hoping for a white Christmas, but his weather machine's "snow"
// function is powered by stars, and he's fresh out! To save Christmas, he needs
// you to collect fifty stars by December 25th.

// Collect stars by helping Santa solve puzzles. Two puzzles will be made
// available on each day in the Advent calendar; the second puzzle is unlocked
// when you complete the first. Each puzzle grants one star. Good luck!

Here's an easy puzzle to warm you up.

// Santa is trying to deliver presents in a large apartment building, but he
// can't find the right floor - the directions he got are a little confusing. He
// starts on the ground floor (floor 0) and then follows the instructions one
// character at a time.

// An opening parenthesis, (, means he should go up one floor, and a closing
// parenthesis, ), means he should go down one floor.

// The apartment building is very tall, and the basement is very deep; he will
// never find the top or bottom floors.

For example:

(()) and ()() both result in floor 0.
((( and (()(()( both result in floor 3.
))((((( also results in floor 3.
()) and ))( both result in floor -1 (the first basement level).
))) and )())()) both result in floor -3.
To what floor do the instructions take Santa?

--- Day 1: Not Quite Lisp ---
Now, given the same instructions, find the position of the first character that
causes him to enter the basement (floor -1). The first character in the instructions has position 1,
the second character has position 2, and so on.

For example:

) causes him to enter the basement at character position 1.
()()) causes him to enter the basement at character position 5.
What is the position of the character that causes Santa to first enter the basement?
"""

from aocd.models import Puzzle
from rich import print


def main(input: str, part: str) -> int:
    """Main Method"""
    FLOOR = 0
    for pos, char in enumerate(input):
        match char:
            case "(":
                FLOOR += 1
            case ")":
                FLOOR -= 1
        if FLOOR < 0 and part == "b":
            return pos + 1
    return FLOOR


if __name__ == "__main__":
    ## PART A ##
    YEAR = 2015
    DAY = 1
    TEST_INPUT = """(()))"""
    OK = r" \[[green]OK[/]]"

    # Test the example #
    RESULT = main(TEST_INPUT, "a")
    print(f"Test   (Part A): {RESULT:4d}", end="")
    assert RESULT == -1
    print(OK)

    # Run the real code #
    PUZZLE = Puzzle(year=YEAR, day=DAY)
    RESULT = main(PUZZLE.input_data, "a")
    print(f"Result (Part A): {RESULT:4d}", end="")
    PUZZLE.answer_a = RESULT
    print(OK)

    ## PART B ##

    # Check the modified code still works on the test input
    RESULT = main(TEST_INPUT, "b")
    print(f"Test   (Part B): {RESULT:4d}", end="")
    assert RESULT == 5
    print(OK)

    RESULT = main(PUZZLE.input_data, "b")
    print(f"Result (Part B): {RESULT:4d}", end="")
    PUZZLE.answer_b = RESULT
    print(OK)
