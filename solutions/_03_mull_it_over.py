from __future__ import annotations

import re
from importlib.resources import files

from . import print_day


def mul(a: int, b: int) -> int:
    return a * b


def find_uncorrupted_mul_instructions(corrupted_memory: str) -> list[str]:
    MUL_INSTRUCTION = re.compile(r"mul\(\d+,\d+\)")
    return MUL_INSTRUCTION.findall(corrupted_memory)


def find_enabled_uncorrupted_mul_instructions(corrupted_memory: str) -> list[str]:
    VALID_INSTRUCTIONS = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")

    enabled = True
    enabled_instructions = []

    for instruction in VALID_INSTRUCTIONS.findall(corrupted_memory):
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        elif enabled:
            enabled_instructions.append(instruction)

    return enabled_instructions


def main():
    print_day(3, "Mull It Over")

    with (files("solutions.inputs") / "03.txt").open() as file:
        corrupted_memory = file.read()

    # Part One: Find uncorrupted mul instructions and add up their results

    result = sum(
        eval(instruction)
        for instruction in find_uncorrupted_mul_instructions(corrupted_memory)
    )
    print(f"Sum of uncorrupted mul instructions: {result}")

    # Part Two: Find enabled uncorrupted mul instructions and add up their results

    result = sum(
        eval(instruction)
        for instruction in find_enabled_uncorrupted_mul_instructions(corrupted_memory)
    )
    print(f"Sum of enabled uncorrupted mul instructions: {result}")


if __name__ == "__main__":
    main()
