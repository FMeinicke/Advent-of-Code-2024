from __future__ import annotations

from importlib.resources import files
from operator import add, sub
from typing import NamedTuple

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "08.txt").open() as file:
        return file.read()


class Coordinate(NamedTuple):
    x: int
    y: int


class Point:
    coordinate: Coordinate
    antenna_frequency: str | None
    has_antinode: bool

    def __init__(self, coordinate: Coordinate, antenna_frequency: str | None) -> None:
        self.coordinate = coordinate
        self.antenna_frequency = antenna_frequency
        self.has_antinode = False

    @staticmethod
    def from_string(coordinate: Coordinate, antenna_frequency: str) -> Point:
        return Point(
            coordinate, antenna_frequency if antenna_frequency != "." else None
        )

    @property
    def has_antenna(self) -> bool:
        return self.antenna_frequency is not None

    def __str__(self) -> str:
        return (
            f"{self.coordinate} {self.antenna_frequency if self.has_antenna else '.'}"
        )


class Map:
    points: list[list[Point]]
    antennas: list[Point]

    def __init__(self, input: str) -> None:
        self.points = []
        self.antennas = []
        for y, line in enumerate(input.splitlines()):
            row = []
            for x, char in enumerate(line):
                point = Point.from_string(Coordinate(x, y), char)
                row.append(point)
                if point.has_antenna:
                    self.antennas.append(point)
            self.points.append(row)
        # print(list(map(str, self.antennas)))

    def find_antinodes(self) -> None:
        for antenna in self.antennas:
            for y, row in enumerate(self.points):
                for x, point in enumerate(row):
                    if (
                        point == antenna
                        or not point.has_antenna
                        or antenna.antenna_frequency != point.antenna_frequency
                    ):
                        continue

                    y_distance = y - antenna.coordinate.y
                    x_distance = x - antenna.coordinate.x

                    for coordinate, direction in zip(
                        (antenna.coordinate, Coordinate(x, y)), (sub, add)
                    ):
                        antinode_y: int = direction(coordinate.y, y_distance)
                        antinode_x: int = direction(coordinate.x, x_distance)
                        # fmt: off
                        if (0 <= antinode_y < len(self.points)) \
                           and (0 <= antinode_x < len(self.points[0])):
                        # fmt: on
                            self.points[antinode_y][antinode_x].has_antinode = True
                            # print(
                            #     f"Antinode for antennas {antenna}, {self.points[y][x]} at {antinode_x}, {antinode_y}"
                            # )

    def find_antinodes_with_resonant_harmonics(self) -> None:
        for antenna in self.antennas:
            for y, row in enumerate(self.points):
                for x, point in enumerate(row):
                    if (
                        point == antenna
                        or not point.has_antenna
                        or antenna.antenna_frequency != point.antenna_frequency
                    ):
                        continue

                    y_distance = y - antenna.coordinate.y
                    x_distance = x - antenna.coordinate.x

                    for coordinate, direction in zip(
                        (antenna.coordinate, Coordinate(x, y)), (sub, add)
                    ):
                        antinode_y: int = coordinate.y
                        antinode_x: int = coordinate.x
                        # fmt: off
                        while (0 <= antinode_y < len(self.points)) \
                              and (0 <= antinode_x < len(self.points[0])):
                        # fmt: on
                            self.points[antinode_y][antinode_x].has_antinode = True
                            antinode_y = direction(antinode_y, y_distance)
                            antinode_x = direction(antinode_x, x_distance)
                            # print(
                            #     f"Antinode for antennas {antenna}, {self.points[y][x]} at {antinode_x}, {antinode_y}"
                            # )

    def count_antinodes(self) -> int:
        return sum(point.has_antinode for row in self.points for point in row)


def main():
    print_day(8, "Resonant Collinearity")

    # Part One: Find the number of unique locations that contain an antinode
    map = Map(get_input())
    map.find_antinodes()
    print(f"Number of unique locations with antinodes: {map.count_antinodes()}")

    # Part Two: Find the number of antinodes taking effects of resonant harmonics into account
    map = Map(get_input())
    map.find_antinodes_with_resonant_harmonics()
    print(f"Number of antinodes with resonant harmonics: {map.count_antinodes()}")


if __name__ == "__main__":
    main()
