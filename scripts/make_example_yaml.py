#!/usr/bin/env python3
# Copyright (c) 2006 Paul Saunders

import sys
from pathlib import Path

import click
import yaml
from aocd.models import Puzzle


class AOCDumper(yaml.SafeDumper):
    pass


def str_presenter(
    dumper: AOCDumper | yaml.Dumper, data: str
) -> yaml.ScalarNode:
    style = "|" if "\n" in data else None
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str", data, style=style
    )


def none_presenter(
    dumper: AOCDumper | yaml.Dumper, _: None
) -> yaml.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:null", "~")


AOCDumper.add_representer(str, str_presenter)
AOCDumper.add_representer(type(None), none_presenter)


@click.command()
@click.option("--year", default=2015, help="Year of the puzzle")
@click.option("--day", default=1, help="Day of the puzzle")
@click.option("--force", is_flag=True, help="Overwrite existing file")
def make_example_yaml(year: int, day: int, force: bool) -> None:
    """Make an example YAML file for the given year and day."""
    puzzle = Puzzle(year=year, day=day)
    examples = (
        {
            "input": example.input_data,
            # Only include part "a" or "b" if their expectation is NOT NONE
            **(
                {"a": example.answer_a}
                if example.answer_a is not None
                else {}
            ),
            **(
                {"b": example.answer_b}
                if example.answer_b is not None
                else {}
            ),
        }
        for example in puzzle.examples
    )
    outfile = (
        Path(__file__).parent.parent
        / "tests"
        / f"year{year}"
        / f"day{day:02d}.yml"
    )
    if not force and outfile.exists():
        print(f"File already exists: {outfile}")
        yaml.dump_all(
            examples,
            stream=sys.stdout,
            sort_keys=False,
            explicit_start=True,
            indent=4,
            Dumper=AOCDumper,
        )
        return
    with outfile.open("w") as f:
        yaml.dump_all(
            examples,
            f,
            sort_keys=False,
            explicit_start=True,
            indent=4,
            Dumper=AOCDumper,
        )
    print(f"Examples written to {outfile}")


if __name__ == "__main__":
    make_example_yaml()
