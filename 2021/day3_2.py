#!env python3

from typing import Iterable
from aocd.models import Puzzle
from rich import print


def common_bit(crit: str, position: int, data: Iterable) -> str:
    counts = {"0": 0, "1": 0}
    for report in data:
        counts[report[position]] += 1
    if crit == "most":
        return "0" if counts["0"] > counts["1"] else "1"
    elif crit == "least":
        return "0" if counts["0"] <= counts["1"] else "1"


def filter_reports(crit: str, data: Iterable) -> str:
    position = 0
    output = data
    while len(output) > 1:
        print(f"{len(output)} items")
        common = common_bit(crit, position, output)
        print(f"{crit.title()} Common Bit in position {position} is {common}")
        output = list(filter(lambda n: n[position] == common, output))
        position += 1
    return output[0]


reports = Puzzle(year=2021, day=3).input_data.splitlines()
generator_rating = filter_reports("most", reports)
scrubber_rating = filter_reports("least", reports)

print(f"O₂ Generator: {generator_rating} = {int(generator_rating,2)}")
print(f"CO₂ Scrubber: {scrubber_rating} = {int(scrubber_rating,2)}")
print(f"Power Consumption: {int(generator_rating,2) * int(scrubber_rating,2)}")
