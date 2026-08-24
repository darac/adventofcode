# Copyright (c) 2015 Paul Saunders
# spell-checker: disable
"""
--- Day 8: Matchsticks ---
Space on the sleigh is limited this year, and so Santa will be bringing his
list as a digital copy. He needs to know how much space it will take up when
stored.

It is common in many programming languages to provide a way to escape
special characters in strings. For example, C, JavaScript, Perl, Python,
and even PHP handle special characters in very similar ways.

However, it is important to realize the difference between the number of
characters in the code representation of the string literal and the number
of characters in the in-memory string itself.

For example:

  - "" is 2 characters of code (the two double quotes), but the string
    contains zero characters.
  - "abc" is 5 characters of code, but 3 characters in the string data.
  - "aaa\"aaa" is 10 characters of code, but the string itself contain
     six "a" characters and a single, escaped quote character, for a total
     of 7 characters in the string data.
  - "\x27" is 6 characters of code, but the string itself contains just
     one - an apostrophe ('), escaped using hexadecimal notation.

Santa's list is a file that contains many double-quoted string literals,
one on each line. The only escape sequences used are \\ (which represents a
single backslash), \" (which represents a lone double-quote character), and
\\x plus two hexadecimal characters (which represents a single character
with that ASCII code).

Disregarding the whitespace in the file, what is the number of characters
of code for string literals minus the number of characters in memory for
the values of the strings in total for the entire file?

For example, given the four strings above, the total number of characters
of string code (2 + 5 + 10 + 6 = 23) minus the total number of characters
in memory for string values (0 + 3 + 7 + 1 = 11) is 23 - 11 = 12.
"""
# spell-checker: enable

import logging
from typing import Literal

LOG = logging.getLogger(__name__)


def solve(
    puzzle: str, _part: Literal["a", "b"], _runner: bool = False
) -> int | None:
    code_chars = 0
    repr_chars = 0
    for line in puzzle.splitlines():
        LOG.debug("START line: %s", line)
        code_chars += len(line)
        escape_sequence = False
        escape_sequence_left = 0
        out_line = ""
        for char in line[1:-1]:
            if char == "\\" and not escape_sequence:
                LOG.debug("      Starting new escape sequence: %s", char)
                escape_sequence = True
                escape_sequence_left = 1
                out_line += "_"
                repr_chars += 1
            elif escape_sequence and char == "x":
                LOG.debug("          \\x style escape sequence: %s", char)
                escape_sequence_left += 1
            elif escape_sequence and escape_sequence_left > 0:
                LOG.debug("          Continue escape sequence: %s", char)
                if char in "\"'":
                    escape_sequence_left = 0
                else:
                    escape_sequence_left -= 1
                if escape_sequence_left == 0:
                    escape_sequence = False
            else:
                repr_chars += 1
                out_line += char
        LOG.debug(
            " END  line: '%s', code_chars: %d, repr_chars: %d",
            out_line,
            code_chars,
            repr_chars,
        )

    return code_chars - repr_chars


if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)10s %(name)s:%(lineno)d %(message)s",
    )

    print(solve(sys.stdin.read(), "a", True))
