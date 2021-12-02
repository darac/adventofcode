#!env python3

from aocd.models import Puzzle
from rich import print

print(f"[green]Captain:[/green] Helmsman! Prepare to recieve orders!")

position = 0
depth = 0

for command, count in [n.split() for n in Puzzle(year=2021,day=2).input_data.splitlines()]:
    print(f"[green]Captain:[/green] {command} {count}")
    match command:
        case "forward":
            print(f"[green]Helmsman:[/green] Aye-aye, sir. Moving Forward {count}")
            position += int(count)
        case "up":
            print(f"[green]Helmsman:[/green] Aye-aye, sir. Coming Up {count}")
            depth -= int(count)
            if depth == 0:
                print("[blue]Computer:[/blue] Surfaced")
            elif depth < 0:
                print("[blue]Computer:[/blue] FLYING!")
        case "down":
            print(f"[green]Helmsman:[/green] Aye-aye, sir. Going Down {count}")
            depth += int(count)
        case _:
            print(f"[green]Captain:[/green] Belay that {command} order!")

print(f"[green]Captain:[/green] Helmsman, Report Position!")
print(f"[green]Helmsman:[/green] Sir! Forward {position}, Depth {depth}, Sir!")
print(f"[green]Captain:[/green] Thank you, sailor. Yeoman, record that as {position * depth}!")