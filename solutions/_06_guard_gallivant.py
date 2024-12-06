from __future__ import annotations

from enum import StrEnum
from importlib.resources import files
from typing import TypeAlias
from copy import deepcopy

from . import print_day

print_day(6, "")


def get_input() -> str:
    with (files("solutions.inputs") / "06.txt").open() as file:
        return file.read()


# Part One: Predict the path of the Guard - how many distinct positions will the guard visit before leaving the mapped area?

Coordinate: TypeAlias = tuple[int, int]


class State(StrEnum):
    UNVISITED = "."
    VISITED = "X"
    OBSTRUCTION = "#"
    GUARD_LEFT = "<"
    GUARD_RIGHT = ">"
    GUARD_UP = "^"
    GUARD_DOWN = "v"
    POSSIBLE_OBSTRUCTION = "O"

    def is_guard(self) -> bool:
        return self in (
            State.GUARD_LEFT,
            State.GUARD_RIGHT,
            State.GUARD_UP,
            State.GUARD_DOWN,
        )

    def is_obstruction(self) -> bool:
        return self == State.OBSTRUCTION

    def is_possible_obstruction(self) -> bool:
        return self == State.POSSIBLE_OBSTRUCTION


class Point:
    coordinate: Coordinate
    state: State
    visited_direction: State | None
    is_possible_obstruction: bool

    def __init__(self, coordinate: Coordinate, state: State) -> None:
        self.coordinate = coordinate
        self.state = state
        self.visited_direction = None
        self.is_possible_obstruction = False

    def __str__(self) -> str:
        return self.state.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            raise TypeError(f"Cannot compare Point with {type(other)}")
        return self.coordinate == other.coordinate and self.state == other.state

    @staticmethod
    def from_string(coordinate: Coordinate, char: str) -> Point:
        return Point(coordinate, State(char))

    def has_guard(self) -> bool:
        return self.state.is_guard()

    def has_obstruction(self) -> bool:
        return self.state.is_obstruction()

    def has_possible_obstruction(self) -> bool:
        return self.state.is_possible_obstruction() and not self.has_confirmed_possible_obstruction()

    def has_confirmed_possible_obstruction(self) -> bool:
        return self.is_possible_obstruction

    def has_been_visited(self) -> bool:
        return self.state == State.VISITED

    def has_been_visited_before_in_same_direction(self) -> bool:
        return self.visited_direction == self.state

    def rotate_guard_right(self) -> None:
        match self.state:
            case State.GUARD_LEFT:
                self.state = State.GUARD_UP
            case State.GUARD_UP:
                self.state = State.GUARD_RIGHT
            case State.GUARD_RIGHT:
                self.state = State.GUARD_DOWN
            case State.GUARD_DOWN:
                self.state = State.GUARD_LEFT
            case _:
                raise ValueError("Cannot rotate a non-guard point")

    def mark_visited(self) -> None:
        if self.state.is_guard():
            # print(f"Guard visited {self.coordinate} in direction {self.state}")
            self.visited_direction = self.state
        self.state = State.VISITED

    def mark_unvisited(self) -> None:
        if not self.has_confirmed_possible_obstruction():
            self.state = State.UNVISITED
        self.visited_direction = None

    def mark_guard(self, direction: State) -> None:
        self.state = direction

    def mark_possible_obstruction(self) -> None:
        # print(f"Checking point {self.coordinate} for possible obstruction")
        self.state = State.POSSIBLE_OBSTRUCTION

    def mark_confirmed_possible_obstruction(self) -> None:
        self.is_possible_obstruction = True


class Map:
    points: list[list[Point]]

    def __init__(self, input: str) -> None:
        self.points = []
        for y, line in enumerate(input.splitlines()):
            row = []
            for x, char in enumerate(line):
                row.append(Point.from_string((x, y), char))
            self.points.append(row)

    def __str__(self) -> str:
        return "\n".join("".join(str(point) for point in row) for row in self.points)

    def predict_guard_movements(self) -> None:
        guard = self.find_guard()
        while (guard := self.move_guard(guard)) is not None:
            pass

    def find_guard(self) -> Point | None:
        try:
            return next(
                point for row in self.points for point in row if point.has_guard()
            )
        except StopIteration:
            return None

    def move_guard(self, guard: Point) -> Point | None:
        x, y = guard.coordinate
        direction = guard.state

        new_x, new_y = x, y
        match direction:
            case State.GUARD_LEFT:
                new_x -= 1
            case State.GUARD_RIGHT:
                new_x += 1
            case State.GUARD_UP:
                new_y -= 1
            case State.GUARD_DOWN:
                new_y += 1
            case _:
                return None

        if (
            new_x < 0
            or new_y < 0
            or new_x >= len(self.points[0])
            or new_y >= len(self.points)
        ):
            # guard left the map
            self.points[y][x].mark_visited()
            return None

        if self.points[new_y][new_x].has_obstruction() or self.points[new_y][new_x].has_possible_obstruction():
            self.points[y][x].rotate_guard_right()
            return guard

        self.points[y][x].mark_visited()
        self.points[new_y][new_x].mark_guard(direction)
        return self.points[new_y][new_x]

    def count_visited(self) -> int:
        return sum(point.has_been_visited() for row in self.points for point in row)

    def find_possible_obstructions(self) -> None:
        print("Finding possible obstructions (this may take a while)...")
        guard = self.find_guard()
        starting_guard = deepcopy(guard)
        for row in self.points:
            for point in row:
                if point.has_obstruction() or point.has_guard():
                    continue
                point.mark_possible_obstruction()
                # print(self)
                if self.is_guard_stuck(guard):
                    point.mark_confirmed_possible_obstruction()
                    # print(f"Possible obstruction at {point.coordinate}")
                else:
                    point.mark_unvisited()
                self.reset(starting_guard)

    def is_guard_stuck(self, guard: Point) -> bool:
        MAX_ITERATIONS = 100_000

        i = 0
        while (guard := self.move_guard(guard)) is not None and i < MAX_ITERATIONS:
            i += 1
            if guard.has_been_visited_before_in_same_direction():
                return True
        if i == MAX_ITERATIONS:
            print("Detected infinite loop ")
            print(self)
        return False

    def reset(self, guard: Point) -> None:
        for row in self.points:
            for point in row:
                if point.has_been_visited() or point.has_guard():
                    point.mark_unvisited()
                if point.coordinate == guard.coordinate:
                    point.mark_guard(guard.state)

    def count_possible_obstructions(self) -> int:
        return sum(
            point.has_confirmed_possible_obstruction() for row in self.points for point in row
        )


m = Map(get_input())
m.predict_guard_movements()
print(f"Guard visited {m.count_visited()} distinct positions")


# Part Two: Find all possible obstructions that would get the guard stuck in a loop

m = Map(get_input())
m.find_possible_obstructions()
print(f"Found {m.count_possible_obstructions()} possible obstructions")
