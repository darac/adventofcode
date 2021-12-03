#!env python3

from aocd.models import Puzzle
from rich import print
from rich.progress import track

counts = {}
for report in track(Puzzle(year=2021, day=3).input_data.splitlines()):
    for i in range(len(report)):
        if i not in counts.keys():
            counts[i] = {"0": 0, "1": 0}
        counts[i][report[i]] += 1

gamma = epsilon = ""
for i in sorted(counts.keys()):
    if counts[i]["0"] > counts[i]["1"]:
        gamma += "0"
        epsilon += "1"
    else:
        gamma += "1"
        epsilon += "0"

print(f"Gamma: {gamma} = {int(gamma,2)}")
print(f"Epsilon: {epsilon} = {int(epsilon,2)}")
print(f"Power Consumption: {int(gamma,2) * int(epsilon,2)}")
