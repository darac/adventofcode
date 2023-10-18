# spell-checker: disable
"""
--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition
proceeds. Occasionally, you can even hear much louder sounds in the
distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its
communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the
resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories
(which can contain other directories or files). The outermost directory is
called /. You can navigate around the filesystem, moving into or out of
directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you
executed, very much like some modern computers:

 - cd means change directory. This changes which directory is the current
   directory, but the specific result depends on the argument:
    - cd x moves in one level: it looks in the current directory for the
      directory named x and makes it the current directory.
    - cd .. moves out one level: it finds the directory that contains
      the current directory, then makes that directory the current
      directory.
    - cd / switches the current directory to the outermost directory, /.
 - ls means list. It prints out all of the files and directories
   immediately contained by the current directory:
    - 123 abc means that the current directory contains a file named abc
      with size 123.
    - dir xyz means that the current directory contains a directory
      named xyz.

Given the commands and output in the example above, you can determine that
the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d
(which are in /), and e (which is in a). These directories also contain
files of various sizes.

Since the disk is full, your first step should probably be to find
directories that are good candidates for deletion. To do this, you need to
determine the total size of each directory. The total size of a directory
is the sum of the sizes of the files it contains, directly or indirectly.
(Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

 - The total size of directory e is 584 because it contains a single file
   i of size 584 and no other directories.
 - The directory a has total size 94853 because it contains files f (size
   29116), g (size 2557), and h.lst (size 62596), plus file i indirectly
   (a contains e which contains i).
 - Directory d has total size 24933642.
 - As the outermost directory, / contains every file. Its total size is
   48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000,
then calculate the sum of their total sizes. In the example above, these
directories are a and e; the sum of their total sizes is 95437 (94853 +
584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is
the sum of the total sizes of those directories?


--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the
update, you need unused space of at least 30000000. You need to find a
directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus
the total amount of used space) is 48381165; this means that the size of
the unused space must currently be 21618835, which isn't quite the 30000000
required by the update. Therefore, the update still requires a directory
with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

 - Delete directory e, which would increase unused space by 584.
 - Delete directory a, which would increase unused space by 94853.
 - Delete directory d, which would increase unused space by 24933642.
 - Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up
enough space. However, directories d and / are both big enough! Between
these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on
the filesystem to run the update. What is the total size of that directory?
"""
# spell-checker: enable

import os
from pathlib import Path
from typing import Literal


class UnknownCommand(Exception):
    def __init__(self: "UnknownCommand", command: str) -> None:
        super().__init__(f"Unknown command: {command}")


def path_get(dictionary: dict, path: Path | str) -> dict:
    paths = Path(path).parts
    for item in paths:
        if item != "" and item in dictionary:
            dictionary = dictionary[item]
    return dictionary


def path_set(dictionary: dict, path: Path | str, set_item: dict | int) -> None:
    paths = Path(path).parts
    key = paths[-1]
    dictionary = path_get(dictionary, os.sep.join(paths[:-1]))  # noqa: PTH118
    dictionary[key] = set_item


def dir_size(directory: dict) -> int:
    size = 0
    for dirent in directory.values():
        if isinstance(dirent, dict):
            size += dir_size(dirent)
        else:
            size += dirent
    return size


def visualise(
    directory: dict[str, int | dict],
    part: Literal["a", "b"],
    runner: bool = False,
    root: Path | str = "",
) -> list[int]:
    picked_directories = []
    for dirent, value in directory.items():
        dir_marker = ""
        pick_me = ""
        if isinstance(value, dict):
            picked_directories.extend(
                visualise(value, root=f"{root}{os.sep}{dirent}", runner=runner, part=part),
            )
            dirent_size = dir_size(value)
            if (part == "a" and dirent_size <= 100_000) or (part == "b"):
                assert isinstance(value, dict)
                pick_me = " <----"
                picked_directories.append(dirent_size)
            else:
                pick_me = ""
            dir_marker = "TOTAL: "
        else:
            assert isinstance(value, int)
            dirent_size = int(value)
        if not runner:
            print(f"{str(root) + os.sep + dirent:80}\t{dir_marker:7}{dirent_size:-12,}{pick_me}")
    return picked_directories


def solve(puzzle: str, part: Literal["a", "b"], _runner: bool = False) -> int | None:
    filesystem: dict[str, dict | int] = {}
    cwd = Path("/")
    for line in puzzle.splitlines():
        match line.split():
            case ["$", "cd", "/"]:
                cwd = Path("/")
            case ["$", "cd", ".."]:
                cwd = cwd.parent
            case ["$", "cd", arg]:
                cwd = cwd / arg
            case ["$", "ls"]:
                pass  # NOSONAR
            case ["dir", dirname]:
                path_set(filesystem, cwd / dirname, {})
            case [size, filename]:
                assert int(size, 10) > 0
                path_set(filesystem, cwd / filename, int(size, 10))
            case _:
                raise UnknownCommand(line)

    big_folders = visualise(filesystem, runner=_runner, part=part)
    if part == "a":
        return sum(big_folders)
    disk_size = 70_000_000
    free_space = disk_size - dir_size(filesystem)
    needed_space = 30_000_000 - free_space
    if not _runner:
        print(f"{free_space:,} free. Need {needed_space:,} more.")
    return min([i for i in sorted([*big_folders, dir_size(filesystem)]) if i >= needed_space])
