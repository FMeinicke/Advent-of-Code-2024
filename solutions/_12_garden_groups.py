from __future__ import annotations

from functools import cache
from importlib.resources import files
from typing import ClassVar, NamedTuple, overload

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "12.txt").open() as file:
        return file.read()


class Coordinate(NamedTuple):
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Direction(NamedTuple):
    dx: int
    dy: int

    def __str__(self):
        return f"({self.dx}, {self.dy})"

    def __repr__(self):
        return f"Direction({self.dx}, {self.dy})"

    def __neg__(self) -> Direction:
        return Direction(-self.dx, -self.dy)

    def __add__(self, other: Direction) -> Direction:
        return Direction(self.dx + other.dx, self.dy + other.dy)

    def opposite_diagonals(self) -> tuple[Direction]:
        if self.dx == 0 and self.dy != 0:
            return (Direction(1, -self.dy), Direction(-1, -self.dy))
        if self.dx != 0 and self.dy == 0:
            return (Direction(-self.dx, 1), Direction(-self.dx, -1))
        return ()

    def diagonals(self) -> tuple[Direction]:
        if self.dx == 0 and self.dy != 0:
            return (Direction(1, self.dy), Direction(-1, self.dy))
        if self.dx != 0 and self.dy == 0:
            return (Direction(self.dx, 1), Direction(self.dx, -1))
        return ()

    NORTH: ClassVar[Direction] = None
    NORTH_EAST: ClassVar[Direction] = None
    EAST: ClassVar[Direction] = None
    SOUTH_EAST: ClassVar[Direction] = None
    SOUTH: ClassVar[Direction] = None
    SOUTH_WEST: ClassVar[Direction] = None
    WEST: ClassVar[Direction] = None
    NORTH_WEST: ClassVar[Direction] = None


Direction.NORTH = Direction(0, -1)
Direction.NORTH_EAST = Direction(1, -1)
Direction.EAST = Direction(1, 0)
Direction.SOUTH_EAST = Direction(1, 1)
Direction.SOUTH = Direction(0, 1)
Direction.SOUTH_WEST = Direction(-1, 1)
Direction.WEST = Direction(-1, 0)
Direction.NORTH_WEST = Direction(-1, -1)


class GardenPlot:
    plant: str
    location: Coordinate
    garden: Garden

    @overload
    def __init__(self, plant: str, garden: Garden, location: Coordinate) -> None: ...

    @overload
    def __init__(self, plant: str, garden: Garden, x: int, y: int) -> None: ...

    def __init__(self, plant: str, garden: Garden, x: int | Coordinate, y: int | None = None) -> None:
        self.plant = plant
        self.garden = garden
        if isinstance(x, Coordinate):
            self.location = x
        elif isinstance(x, int) and isinstance(y, int):
            self.location = Coordinate(x, y)
        else:
            raise TypeError("Invalid arguments")

    def __str__(self) -> str:
        return self.plant

    def __repr__(self) -> str:
        return f"GardenPlot({self.plant}{self.location})"

    @property
    @cache
    def neighbors(self) -> list[GardenPlot]:
        return [
            self.garden.plots[neighbor_y][neighbor_x]
            for d in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
            if 0 <= (neighbor_y := self.location.y + d.dy) < len(self.garden.plots)
            and 0 <= (neighbor_x := self.location.x + d.dx) < len(self.garden.plots[neighbor_y])
        ]

    @property
    def plant_neighbors(self) -> list[GardenPlot]:
        return [neighbor for neighbor in self.neighbors if neighbor.plant == self.plant]

    def direction_to(self, other: GardenPlot) -> Direction:
        return Direction(other.location.x - self.location.x, other.location.y - self.location.y)

    def neighbor_at(self, direction: Direction) -> GardenPlot | None:
        if (0 <= (neighbor_y := self.location.y + direction.dy) < len(self.garden.plots)) and (
            0 <= (neighbor_x := self.location.x + direction.dx) < len(self.garden.plots[neighbor_y])
        ):
            return self.garden.plots[neighbor_y][neighbor_x]
        return None

    @property
    def num_corners(self) -> int:
        if len(self.plant_neighbors) == 0:
            # no neighbors -> 4 corners
            # print(f"{self!r} has no neighbors -> 4 corners")
            return 4

        if len(self.plant_neighbors) == 1:
            # neighbor on a single side
            # -> 2 corners, if the diagonal neighbors on the opposite side are same plants and the opposite neighbor is
            # a different plant
            if (opposite_neighbor := self.neighbor_at(-self.direction_to(self.plant_neighbors[0]))) is not None and (
                opposite_neighbor.plant != self.plant
                and all(
                    (neighbor := self.neighbor_at(direction)) is not None and neighbor.plant == self.plant
                    for direction in self.direction_to(self.plant_neighbors[0]).opposite_diagonals()
                )
            ):
                # print(
                #     f"{self!r} has one neighbor in direction {self.direction_to(self.plant_neighbors[0])} and {opposite_neighbor!r} on the opposite side -> 2 corners"
                # )
                return 2
            # -> corner, if the diagonal neighbors on the opposite side are different plants
            res = sum(
                (neighbor := self.neighbor_at(direction)) is None or neighbor.plant != self.plant
                for direction in self.direction_to(self.plant_neighbors[0]).opposite_diagonals()
            )
            # print(
            #     f"{self!r} has one neighbor in direction {self.direction_to(self.plant_neighbors[0])} -> {res} corners"
            # )
            # -> corner, if the diagonal neighbors on the opposite side are same plants and the neighbor of that plant
            # in the same direction as this one's neighbor is different
            res2 = sum(
                (neighbor := self.neighbor_at(direction)) is not None
                and neighbor.plant == self.plant
                and (neighbors_neighbor := neighbor.neighbor_at(self.direction_to(self.plant_neighbors[0]))) is not None
                and neighbors_neighbor.plant != self.plant
                for direction in self.direction_to(self.plant_neighbors[0]).opposite_diagonals()
            )
            # print(
            #     f"{self!r} has one neighbor in direction {self.direction_to(self.plant_neighbors[0])} -> {res2} corners"
            # )
            return res + res2

        if len(self.plant_neighbors) == 2:
            if self.direction_to(self.plant_neighbors[0]) == -self.direction_to(self.plant_neighbors[1]):
                # opposing neighbors -> no corners, straight line
                # print(f"{self!r} has opposing neighbors -> no corners")
                return 0

            # this plot builds a corner
            d = self.direction_to(self.plant_neighbors[0]) + self.direction_to(self.plant_neighbors[1])
            if (neighbor := self.neighbor_at(d)) is not None and (
                # if the plot touching both neighbors is the same plant, we only have one corner
                neighbor.plant == self.plant
                or
                # if the plot touching both neighbors is only surrounded by plants of the same type as this plot
                (
                    neighbor.num_corners < 4
                    and all(neighbors_neighbor.plant == self.plant for neighbors_neighbor in neighbor.neighbors)
                )
            ):
                # print(f"{self!r} has 2 neighbors and {neighbor!r} in between -> 1 corner")
                return 1
            # otherwise, we have another "inner" corner
            # print(f"{self!r} has 2 neighbors and no plot in between -> 2 corners")
            return 2

        if len(self.plant_neighbors) == 3:
            # one side doesn't have a neighbor -> corner, if the diagonal neighbors on the side of the missing neighbor
            # are different plants, but only if these diagonal neighbors are single plant regions or are not surrounded
            # by plants of the same type as this plot
            missing_direction = Direction(0, 0)
            for direction in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
                # print(
                #     f"{self!r} has 3 neighbors -> checking neighbor {self.neighbor_at(direction)!r} in direction {direction}"
                # )
                if (neighbor := self.neighbor_at(direction)) is None or neighbor not in self.plant_neighbors:
                    missing_direction = direction
                    break
            res = sum(
                (neighbor := self.neighbor_at(direction)) is None
                or (
                    neighbor.plant != self.plant
                    and (
                        neighbor.num_corners == 4
                        or any(neighbors_neighbor.plant != self.plant for neighbors_neighbor in neighbor.neighbors)
                    )
                )
                for direction in missing_direction.opposite_diagonals()
            )
            # print(
            #     f"{self!r} has 3 neighbors and is missing a neighbor in direction {missing_direction} -> {res} corners"
            # )
            return res

        if len(self.plant_neighbors) == 4:
            # neighbors on all sides -> corner, if the diagonal neighbors are different plants
            res = sum(
                (neighbor := self.neighbor_at(direction)) is None or neighbor.plant != self.plant
                for direction in (
                    Direction.NORTH_EAST,
                    Direction.SOUTH_EAST,
                    Direction.SOUTH_WEST,
                    Direction.NORTH_WEST,
                )
            )
            # print(f"{self!r} has 4 neighbors -> {res} corners")
            return res


class Region:
    plots: list[GardenPlot]

    def __init__(self, plot: GardenPlot) -> None:
        self.plots = []
        self.__make_region(plot)

    def __make_region(self, plot: GardenPlot):
        self.plots.append(plot)
        for neighbor in plot.plant_neighbors:
            # print(f"checking neighbor {neighbor!r} of {plot!r} for region")
            if neighbor not in self.plots:
                self.__make_region(neighbor)

    def __str__(self):
        return " ".join(f"{plot!r}" for plot in self.plots)

    def append(self, plot: GardenPlot) -> None:
        self.plots.append(plot)

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def perimeter(self) -> int:
        perimeter = 4 * self.area
        # print(f"starting with {perimeter=} for {self!s}")
        for plot in self.plots:
            for neighbor in plot.neighbors:
                if neighbor in self.plots:
                    perimeter -= 1
                    # print(f"decrementing for neighbor {neighbor!r} of {plot!s} -> {perimeter=}")
        return perimeter

    @property
    def fence_price(self) -> int:
        return self.area * self.perimeter

    @property
    def num_sides(self) -> int:
        return sum(plot.num_corners for plot in self.plots)

    @property
    def discounted_fence_price(self) -> int:
        return self.area * self.num_sides


class Garden:
    plots: list[list[GardenPlot]]
    regions: list[Region]

    def __init__(self, input: str) -> None:
        self.plots = []
        for y, line in enumerate(input.split("\n")):
            self.plots.append([GardenPlot(plant, self, x, y) for x, plant in enumerate(line)])
        self.create_regions()

    def __str__(self) -> str:
        return "\n".join("".join(str(plot) for plot in row) for row in self.plots)

    def create_regions(self) -> None:
        self.regions = []
        for row in self.plots:
            for plot in row:
                for region in self.regions:
                    if plot in region.plots:
                        break
                else:
                    self.regions.append(Region(plot))

    @property
    def fence_price(self) -> int:
        return sum(region.fence_price for region in self.regions)

    @property
    def discounted_fence_price(self) -> int:
        return sum(region.discounted_fence_price for region in self.regions)


def main():
    print_day(12, "Garden Groups")

    # Part One: Find the total price for fencing all regions
    garden = Garden(get_input())
    print(f"Fence price: {garden.fence_price}")

    # Part Two: Find the discounted price
    print(f"Discounted fence price: {garden.discounted_fence_price}")


if __name__ == "__main__":
    main()
