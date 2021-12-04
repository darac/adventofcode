#!env python3
"""
--- Day 1: Not Quite Lisp ---
Now, given the same instructions, find the position of the first character that
causes him to enter the basement (floor -1). The first character in the instructions has position 1,
the second character has position 2, and so on.

For example:

) causes him to enter the basement at character position 1.
()()) causes him to enter the basement at character position 5.
What is the position of the character that causes Santa to first enter the basement?
"""

from aocd import submit
from aocd.models import Puzzle
from rich import print

FLOOR = 0
for pos, char in enumerate(Puzzle(year=2015, day=1).input_data):
    match char:
        case '(':
            FLOOR += 1
        case ')':
            FLOOR -= 1
    if FLOOR < 0:
        print (f"Position: {pos}")
        submit(pos+1, part="b", day=1, year=2015)

        break
