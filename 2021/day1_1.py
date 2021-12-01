#!env python3

import aocd
from rich import print

prev = None
count = 0
for line in aocd.get_data(day=1).splitlines():
    value = int(line)
    if prev is not None:
        if value > prev:
            print(f"{value} ([bold]increased[/bold])")
            count += 1
        else:
            print(f"{value} (decreased)")
    prev = value

print(f"count = {count}")
