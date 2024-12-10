from __future__ import annotations

from importlib.resources import files
from typing import NamedTuple

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "10.txt").open() as file:
        return file.read()


class Coordinate(NamedTuple):
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)


class TopographicPoint:
    map: TopographicMap
    coordinate: Coordinate
    height: int
    reachable_9_heights: list[TopographicPoint]
    has_been_searched: bool

    def __init__(self, map: TopographicMap, coordinate: Coordinate, height: int) -> None:
        self.map = map
        self.coordinate = coordinate
        self.height = height
        self.reachable_9_heights = []
        self.has_been_searched = False

    def __str__(self) -> str:
        return f"{self.height:X}{self.coordinate}"

    @property
    def is_trailhead(self) -> bool:
        return self.height == 0

    @property
    def neighbors(self) -> list[TopographicPoint]:
        neighbors = []
        for x in range(self.coordinate.x - 1, self.coordinate.x + 2):
            for y in range(self.coordinate.y - 1, self.coordinate.y + 2):
                if abs(x - self.coordinate.x) + abs(y - self.coordinate.y) != 1:
                    continue
                if 0 <= x < len(self.map.points) and 0 <= y < len(self.map.points[0]):
                    neighbors.append(self.map.points[y][x])
        return neighbors

    def find_reachable_9_heights(self) -> None:
        self.has_been_searched = True
        if self.height == 9:
            self.reachable_9_heights.append(self)
        else:
            for neighbor in self.neighbors:
                if neighbor.height == self.height + 1:
                    if not neighbor.has_been_searched:
                        neighbor.find_reachable_9_heights()
                    # print(f"Point {self} can reach {[str(n) for n in set(neighbor.reachable_9_heights)]} via neighbor {neighbor}")
                    self.reachable_9_heights.extend(neighbor.reachable_9_heights)

    @property
    def score(self) -> None:
        if not self.has_been_searched:
            self.find_reachable_9_heights()
        return len(set(self.reachable_9_heights))

    @property
    def rating(self) -> None:
        if not self.has_been_searched:
            self.find_reachable_9_heights()
        return len(self.reachable_9_heights)




class TopographicMap:
    points: list[list[TopographicPoint]]

    def __init__(self, input: str) -> None:
        self.points = [
            # using base 16 just for simplified puzzle input in the tests - the actual input only contains 0-9
            [TopographicPoint(self, Coordinate(x, y), int(height, 16)) for x, height in enumerate(row)]
            for y, row in enumerate(input.splitlines())
        ]

    def __str__(self) -> str:
        return "\n".join("".join(f"{point.height:X}" for point in row) for row in self.points)

    def str_with_scores(self) -> str:
        return "\n".join(" ".join(f"{point.height:X}({point.score})" for point in row) for row in self.points)

    def str_with_reachable_nine_heights(self) -> str:
        return "\n".join(" ".join(f"{point.height:X}({[p.coordinate for p in point.reachable_9_heights]})" for point in row) for row in self.points)

    def sum_of_trailhead_scores(self) -> int:
        return sum(point.score for row in self.points for point in row if point.is_trailhead)

    def sum_of_trailhead_ratings(self) -> int:
        return sum(point.rating for row in self.points for point in row if point.is_trailhead)

def main():
    print_day(10, "Hoof It")

    # Part One: Find the sum of the scores of all trailheads on the topographic map.
    map = TopographicMap(get_input())
    print(f"Sum of trailhead scores: {map.sum_of_trailhead_scores()}")

    # Part Two: Find the sum of the ratings of all trailheads on the topographic map.
    print(f"Sum of trailhead ratings: {map.sum_of_trailhead_ratings()}")


if __name__ == "__main__":
    main()
