# Types
Point = tuple[int, int]
Grid = dict[Point, str]


def grid_of_chars(puzzle: str) -> tuple[Grid, int, int]:
    """Turn a puzzle string into a 2d-grid, using split()

    Args:
        puzzle (str): a puzzle string

    Returns:
        tuple[Grid, int, int]: The grid, the X size and the Y size
    """
    result = {}
    lines = puzzle.splitlines()
    y_size = len(lines)
    x_size = len(lines[0])
    for y_pos, line in enumerate(lines):
        for x_pos, char in enumerate(line):
            result[(y_pos, x_pos)] = char

    return result, x_size, y_size
