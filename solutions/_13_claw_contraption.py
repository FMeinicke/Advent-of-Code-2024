from __future__ import annotations

import re
from ast import Name
from importlib.resources import files
from typing import NamedTuple

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "13.txt").open() as file:
        return file.read()

class Button:
    token_cost: int
    move_x: int
    move_y: int

    def __init__(self, input: str):
        match = re.match(r"Button ([A-Z]): X\+(\d+), Y\+(\d+)", input)
        self.token_cost = 3 if match.group(1) == "A" else 1
        self.move_x = int(match.group(2))
        self.move_y = int(match.group(3))

    def __str__(self) -> str:
        return f"Button {'A' if self.token_cost == 3 else 'B'}: X{self.move_x:+}, Y{self.move_y:+}"

    def moved(self, distance: int) -> Coordinate:
        return Coordinate(int(self.move_x * distance), int(self.move_y * distance))


class Coordinate(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: int) -> Coordinate:
        return Coordinate(self.x + other, self.y + other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            # print("here")
            return False
        return self.x == other.x and self.y == other.y


class Prize(Coordinate):
    @staticmethod
    def from_str(input: str) -> Prize:
        match = re.match(r"Prize: X=(\d+), Y=(\d+)", input)
        return Prize(int(match.group(1)), int(match.group(2)))

    def __str__(self) -> str:
        return f"Prize: X={self.x}, Y={self.y}"


class Machine:
    button_a: Button
    button_b: Button
    prize: Prize

    def __init__(self, input: str):
        lines = input.splitlines()
        self.button_a = Button(lines[0])
        self.button_b = Button(lines[1])
        self.prize = Prize.from_str(lines[2])

    def __str__(self) -> str:
        return f"{self.button_a!s}\n{self.button_b!s}\n{self.prize!s}"

    def calculate_token_cost(self, offset: int = 0) -> int:
        """
        Cramer's rule, adapted from https://www.reddit.com/r/adventofcode/comments/1hd7irq/2024_day_13_an_explanation_of_the_mathematics
        """

        self.prize += offset

        # A = (p_x*b_y - prize_y*b_x) / (a_x*b_y - a_y*b_x)
        # B = (a_x*p_y - a_y*p_x) / (a_x*b_y - a_y*b_x)
        det = self.button_a.move_x * self.button_b.move_y - self.button_a.move_y * self.button_b.move_x
        a = (self.prize.x * self.button_b.move_y - self.prize.y * self.button_b.move_x) / det
        b = (self.button_a.move_x * self.prize.y - self.button_a.move_y * self.prize.x) / det
        # print(a, b)
        # print(
        # self.button_a.moved(a), self.button_b.moved(b), self.button_a.moved(a) + self.button_b.moved(b), self.prize
        # )
        # print(self.button_a.moved(a) + self.button_b.moved(b) == self.prize)
        # print("---")
        if a.is_integer() and b.is_integer() and (self.button_a.moved(a) + self.button_b.moved(b)) == self.prize:
            return int(self.button_a.token_cost * a + self.button_b.token_cost * b)
        return 0


def main():
    print_day(13, "Claw Contraption")

    # Part One: How many tokens to spend to win all possible prizes?
    total_token_cost = 0
    for machine_input in get_input().split("\n\n"):
        machine = Machine(machine_input)
        total_token_cost += machine.calculate_token_cost()
        # print(total_token_cost)
        # print("---")
    print(f"Total token cost: {total_token_cost}")

    # Part Two: Account for the offset of 10000000000000
    total_token_cost = 0
    for machine_input in get_input().split("\n\n"):
        machine = Machine(machine_input)
        total_token_cost += machine.calculate_token_cost(offset=10000000000000)
        # print(total_token_cost)
        # print("---")
    print(f"Total token cost with offset: {total_token_cost}")


if __name__ == "__main__":
    main()
