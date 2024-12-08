from __future__ import annotations

from importlib.resources import files

from . import print_day

print_day(x, "")

def get_input() -> str:
    with (files("solutions.inputs") / "xx.txt").open() as file:
        return file.read()

# Part One:

def part_one():
    pass


# Part Two:

def part_two():
    pass
