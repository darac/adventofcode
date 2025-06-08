# adventofcode

Storage for my AdventOfCode solutions

[![Tests](https://github.com/darac/adventofcode/workflows/Test/badge.svg)](https://github.com/darac/adventofcode/actions/workflows/test.yml)
[![CodeQL](https://github.com/darac/adventofcode/workflows/CodeQL/badge.svg)](https://github.com/darac/adventofcode/security/code-scanning)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=darac_adventofcode&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=darac_adventofcode)[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=darac_adventofcode&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=darac_adventofcode)[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=darac_adventofcode&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=darac_adventofcode)

## Setup

```sh
# Install dependencies
uv sync --dev

# Setup pre-commit and pre-push hooks
uv run pre-commit install --install-hooks
```

## Goals

This repository is partly a place to hold my solutions to the Advent Of Code challenges,
but because I feel that the AoC challenges are a place for people to develop whatever
skills they like (i.e. PHP, Node, Python, Rust etc), I've chosen to use this repository
to increase my skills in the CI/CD arena.

To that end, there is a lot of automation built into the repository:

* Each day's challenge is contained in a single Python file (except for some early attempts,
  before I'd refined the process).
* [pre-commit](https://pre-commit.com/) is used to lint the repository before code can be
  committed. Only relatively quick checks are performed (such as
  [ruff](https://github.com/astral-sh/ruff) checking and
  [secret scanning](https://github.com/gitleaks/gitleaks)) at this step.
* GitHub Actions make use of [tox](https://github.com/tox-dev/tox) to run
  [pytest](https://docs.pytest.org/en/stable/) under various versions of Python.
* [SonarQube](https://www.sonarsource.com/products/sonarcloud/) is used for Quality Control.
* If the GitHub testing passes,
  [Python Semantic Release](https://python-semantic-release.readthedocs.io/en/latest/)
  automatically generates a release (tags, Changelog etc) based on recent commit messages.
* Finally, a Docker Image is built from the release and published to GitHub's Container Registry.
* Dependabot and Renovate monitor the repository for dependency updates throughout the year.

## Coding Standards

I'd like for each day's solution to have a common structure, so the minimum interface is:

```python
# File Name: aoc/yearXXXX/dayYY.py
"""
--- Day N: Title ---

The day's instructions go here.
"""

from typing import Literal

from aoc.yearXXXX import LOG        # Where XXXX is the year of this puzzle

def solve(
    puzzle: str,                    # This is the puzzle input
    part: Literal["a","b"],         # All puzzles are two-parters
) -> int | None:                    # Some puzzles may return 'str', though
    ...
```

Most days, the Advent Of Code puzzles contain some example data, and an expected
result. These examples can be turned into test cases, by writing them into a YAML file:

```yaml
# File Name: tests/yearXXXX/dayYY.yml
---
input: |
    Line 1
    Line 2
    Line 3
a: 3
---
input: |
    Line 1
    Line 2
    Line 3
    Line 4
a: 4
b: 10
```

Note how we use the multiple Documents feature of YAML to store multiple test cases in a
single file. Each test case can provide an answer for part A, part B or both (it's legal to
provide an answer for neither, but not useful).

## Helpers

In order to run the tests, I have written a "[runner function](aoc/__init__.py#L18)" around the
[advent-of-code-data](https://pypi.org/project/advent-of-code-data/) library:

```python
def solve(year: int, day: int, data: str) -> tuple[int | None, ...]:
    """
    Finds today's solver, and runs it twice; once for part a and once for
    part b.
    The results are combined and returned to aocd-runner for submission.
    """
    solver_name = f"aoc.year{year:4d}.day{day:02d}"
    ...
    try:
        solver = importlib.import_module(solver_name)
    except ModuleNotFoundError:
        return None, None

    try:
        a = solver.solve(puzzle=data, part="a", _runner=True)
        b = solver.solve(puzzle=data, part="b", _runner=True)
    except AttributeError:
        return None, None

    return a, b
```

This function assumes that each day's solution can be imported as
`aoc.yearXXXX.dayYY` (if not, perhaps because the solution hasn't yet been
written, the function returns "None, None" for that day). The function then calls
the `solve()` method within that solution with the parameters shown above.

Advent-of-code-data handles a lot of the heavy-lifting of iterating over solutions,
fetching puzzle data, submitting answers etc. So it's usually just a matter of running
`aoc` to run all the solutions in this repository against a set of login tokens.

For testing (partly to satisfy SonarQube, but partly so that I can run solutions against the
examples without submitting them), I have written the following pytest function:

```python
def test_solve(
    solver: Callable,
    puzzle: str,
    part: Literal["a","b"],
    expected: int | str
) -> None:
    assert solver(puzzle=puzzle, part=part) == expected
```

Dead simple. Assert that running the solver on the puzzle data produces the expected data.
The clever bit is (ab)using pytest's [test-discovery mechanism](tests/conftest.py#L91)
such that, for each YAML _document_ produce a "parta" and "partb" test. Tests are named
`tests/yearXXXX/dayYY/testZZ/partA`.

Finally, to make iterating through testing quicker, I [add options](tests/conftest.py#L50)
to the pytest command line:

```text
usage: pytest [options] [file_or_dir] [file_or_dir] [...]

positional arguments:
  file_or_dir

general:
  ...

Custom options:
  --year=[{2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025} ...]
                        Run AOC tests from this year
  --day=[{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25} ...]
                        Run AOC tests from this day
  --part=[{a,b} ...]    Run this part
  --today               Run the latest available day (overrides --year and
                        --day)
```

<!--- advent_readme_stars table --->
## 2024 Results

| Day | Part 1 | Part 2 |
| :---: | :---: | :---: |
| [Day 1](https://adventofcode.com/2024/day/1) | ⭐ | ⭐ |
| [Day 2](https://adventofcode.com/2024/day/2) | ⭐ | ⭐ |
| [Day 3](https://adventofcode.com/2024/day/3) | ⭐ | ⭐ |
| [Day 4](https://adventofcode.com/2024/day/4) | ⭐ | ⭐ |
| [Day 6](https://adventofcode.com/2024/day/6) | ⭐ | ⭐ |
<!--- advent_readme_stars table --->

## Credits

This package was created with Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.
