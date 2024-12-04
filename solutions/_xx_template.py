from __future__ import annotations

from importlib.resources import files

from . import print_day

print_day(x, "")

def get_input():
    with (files("solutions.inputs") / "xx.txt").open() as file:
        for line in file:
            ...

# Part One:

def part_one():
    pass


# Part Two:

def part_two():
    pass
