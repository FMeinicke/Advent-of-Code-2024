from __future__ import annotations

import math
import re
import time
from importlib.resources import files
from typing import Literal, NamedTuple, TypeAlias

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "14.txt").open() as file:
        return file.read()


WIDTH = 101
HEIGHT = 103


class Coordinate:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Coordinate) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

    def __repr__(self) -> str:
        return f"Coordinate({self.x}, {self.y})"

    def __add__(self, other: Velocity) -> Coordinate:
        return Coordinate(self.x + other.dx, self.y + other.dy)

    def __iadd__(self, other: Velocity) -> Coordinate:
        self.x += other.dx
        self.y += other.dy
        return self

    def __mod__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x % other.x, self.y % other.y)

    def __imod__(self, other: Coordinate) -> Coordinate:
        self.x %= other.x
        self.y %= other.y
        return self


class Velocity(NamedTuple):
    dx: int
    dy: int


Quadrant: TypeAlias = Literal[1, 2, 3, 4]


class Robot:
    position: Coordinate
    velocity: Velocity
    map_width: int
    map_height: int

    def __init__(self, input: str, *, width: int = WIDTH, height: int = HEIGHT) -> None:
        match = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", input)
        self.position = Coordinate(int(match.group(1)), int(match.group(2)))
        self.velocity = Velocity(int(match.group(3)), int(match.group(4)))
        self.map_width = width
        self.map_height = height

    def __str__(self) -> str:
        return f"p={self.position.x},{self.position.y} v={self.velocity.dx},{self.velocity.dy}"

    def move(self, count: int = 1) -> None:
        for _ in range(count):
            self.position += self.velocity
            self.position %= Coordinate(self.map_width, self.map_height)

    @property
    def quadrant(self) -> Quadrant:
        """
        1|2
        -+-
        3|4
        """
        map_width_2 = self.map_width // 2
        map_height_2 = self.map_height // 2

        if self.position.x < map_width_2 and self.position.y < map_height_2:
            return 1
        if self.position.x > map_width_2 and self.position.y < map_height_2:
            return 2
        if self.position.x < map_width_2 and self.position.y > map_height_2:
            return 3
        if self.position.x > map_width_2 and self.position.y > map_height_2:
            return 4


def count_robots_in_quadrant(robots: list[Robot], quadrant: Quadrant) -> int:
    return sum(1 for r in robots if r.quadrant == quadrant)


def calculate_safety_factor(robots: list[Robot]) -> int:
    safety_factor = 1
    for i in range(1, 5):
        safety_factor *= count_robots_in_quadrant(robots, i)
    return safety_factor


def print_map(
    robots: list[Robot], width: int = WIDTH, height: int = HEIGHT, clear: bool = True, i: int | None = None
) -> None:
    if clear:
        CLEAR_SCREEN = "\033[2J"
        CURSOR_TOP_LEFT = "\033[H"
        print(CLEAR_SCREEN)
        print(CURSOR_TOP_LEFT)

    if i is not None:
        print(f"Time: {i} seconds")

    map = [["." for _ in range(width)] for _ in range(height)]
    for r in robots:
        map[r.position.y][r.position.x] = "#"
    for i, row in enumerate(map):
        print(f"{i:>3} {' '.join(row)}")


def main():
    print_day(14, "Restroom Redoubt")

    # Part One: Find the safety factor after 100 seconds.
    robots = [Robot(line) for line in get_input().splitlines()]
    for r in robots:
        r.move(100)
    safety_factor = calculate_safety_factor(robots)
    print(f"The safety factor is {safety_factor}")

    # Part Two: Find the fewest number of seconds for the robots to display the "Christmas Tree Formation" Easter egg.
    # Using the heuristic from https://www.reddit.com/r/adventofcode/comments/1he0g67/2024_day_14_part_2_the_clue_was_in_part_1/
    robots = [Robot(line) for line in get_input().splitlines()]
    print_map(robots, clear=False)
    lowest_safety_factor = math.inf
    lowest_safety_factor_time = 0
    for i in range(1, 10_000):
        for r in robots:
            r.move()
        # print_map(robots, clear=True, i=i)
        if (safety_factor := calculate_safety_factor(robots)) < lowest_safety_factor:
            lowest_safety_factor = safety_factor
            lowest_safety_factor_time = i
            print_map(robots, clear=False)
            print(f"New lowest safety factor: {lowest_safety_factor} at {lowest_safety_factor_time} seconds")
            time.sleep(2)
        # time.sleep(0.01)
    print(f"The Christmas Tree Formation probably appears after {lowest_safety_factor_time} seconds")


if __name__ == "__main__":
    main()
