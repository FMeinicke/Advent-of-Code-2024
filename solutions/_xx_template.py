from __future__ import annotations

from importlib.resources import files

from . import print_day

print_day(xx, "")

with (files("solutions.inputs") / "xx.txt").open() as file:
    for line in file:
        ...

# Part One:


# Part Two:
