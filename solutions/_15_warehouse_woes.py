from __future__ import annotations

from calendar import c
from enum import StrEnum
from importlib.resources import files
from tabnanny import check
from typing import NamedTuple, TypeAlias

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "15.txt").open() as file:
        return file.read()


class MoveType(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


class Direction(NamedTuple):
    dx: int
    dy: int


class Move:
    type: MoveType

    def __init__(self, char: str):
        self.type = MoveType(char)

    @property
    def direction(self) -> Direction:
        match self.type:
            case MoveType.UP:
                return Direction(0, -1)
            case MoveType.DOWN:
                return Direction(0, 1)
            case MoveType.LEFT:
                return Direction(-1, 0)
            case MoveType.RIGHT:
                return Direction(1, 0)

    def __str__(self) -> str:
        return str(self.type)


GPSCoordinate: TypeAlias = int


class Coordinate(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Coordinate | Direction) -> Coordinate:
        dx = other.x if isinstance(other, Coordinate) else other.dx
        dy = other.y if isinstance(other, Coordinate) else other.dy
        return Coordinate(self.x + dx, self.y + dy)

    def __mul__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x * other.x, self.y * other.y)


class TileType(StrEnum):
    ROBOT = "@"
    FREE = "."
    WALL = "#"
    BOX = "O"

    WIDE_BOX_LEFT = "["
    WIDE_BOX_RIGHT = "]"


class Tile:
    type: TileType
    coordinate: Coordinate

    def __init__(self, type: TileType, coordinate: Coordinate):
        self.type = type
        self.coordinate = coordinate

    def __str__(self) -> str:
        return str(self.type)

    @property
    def gps_coordinate(self) -> GPSCoordinate:
        return self.coordinate.x + self.coordinate.y * 100


class Map:
    # tiles: list[list[Tile]]
    tiles: dict[Coordinate, Tile]
    robot: Tile
    moves: list[Move]

    def __init__(self, map_input: str, moves: str):
        # self.tiles = [
        #     [Tile(TileType(char), Coordinate(x, y)) for x, char in enumerate(line)]
        #     for y, line in enumerate(map_input.splitlines())
        # ]
        # self.robot = next(tile for row in self.tiles for tile in row if tile.type == TileType.ROBOT)
        self.tiles = {
            (coordinate := Coordinate(x, y)): Tile(TileType(char), coordinate)
            for y, line in enumerate(map_input.splitlines())
            for x, char in enumerate(line)
        }
        self.robot = next(tile for tile in self.tiles.values() if tile.type == TileType.ROBOT)
        self.moves = [Move(char) for char in moves.replace("\n", "")]

    def __str__(self) -> str:
        # return "\n".join("".join(str(tile) for tile in row) for row in self.tiles)
        return "".join(f"{'\n' if coord.x == 0 and coord.y != 0 else ''}{tile!s}" for coord, tile in self.tiles.items())

    def move_robot(self) -> None:
        for i, move in enumerate(self.moves):
            prev_map_str = str(self)
            print(f"Move {i + 1}: {move}")
            self.move_tile(self.robot, move)
            map_str = str(self)
            assert (
                "[." not in map_str
                and ".]" not in map_str
                and "[[" not in map_str
                and "]]" not in map_str
                and "[#" not in map_str
                and "#]" not in map_str
                and "[@" not in map_str
                and "@]" not in map_str
            ), f"\n{prev_map_str}\n\n{map_str}"
            # print("=====================================")
            # print(str(self))
            # print("=====================================")

    def move_tile(self, tile: Tile, move: Move, *, check_only: bool = False) -> bool:
        match tile.type:
            case TileType.WIDE_BOX_LEFT:
                # up -> move right up as well, need to check my up and the right's up
                # down -> move right down as well, need to check my down and the right's down
                # right -> move right right as well, need to check the right's right
                # left -> move right left as well, need to check my left
                left_tile = self.tiles[tile.coordinate + Direction(1, 0)]
                new_coord_left = tile.coordinate + move.direction
                new_coord_right = left_tile.coordinate + move.direction
                print(f"Trying to move {tile!s} from {tile.coordinate} to {new_coord_left} and {new_coord_right}.")
                match move.type:
                    case MoveType.UP | MoveType.DOWN:
                        if (
                            self.tiles[new_coord_left].type == TileType.FREE
                            and self.tiles[new_coord_right].type == TileType.FREE
                        ) or (
                            self.tiles[new_coord_left].type == TileType.FREE
                            and self.move_tile(self.tiles[new_coord_right], move, check_only=check_only)
                        ):
                            print(f"Moving {tile!s} at {tile.coordinate} {move}.")
                            self.move_single_tile(tile, move, check_only=check_only)
                            self.move_single_tile(left_tile, move, check_only=check_only)
                            return True
                        if self.move_tile(self.tiles[new_coord_left], move, check_only=True) and self.move_tile(
                            self.tiles[new_coord_right], move, check_only=True
                        ):
                            print(f"Moving {tile!s} at {tile.coordinate} {move} after moving other tiles.")
                            self.move_tile(self.tiles[new_coord_left], move, check_only=check_only)
                            self.move_tile(self.tiles[new_coord_right], move, check_only=check_only)
                            self.move_single_tile(tile, move, check_only=check_only)
                            self.move_single_tile(left_tile, move, check_only=check_only)
                            return True
                    case MoveType.RIGHT:
                        if self.move_single_tile(left_tile, move, check_only=check_only):
                            print(f"Moving {tile!s} at {tile.coordinate} {move}.")
                            self.move_single_tile(tile, move, check_only=check_only)
                            return True
                    case MoveType.LEFT:
                        if self.move_single_tile(tile, move, check_only=check_only):
                            print(f"Moving {left_tile!s} at {tile.coordinate} {move}.")
                            self.move_single_tile(left_tile, move, check_only=check_only)
                            return True
                print("Can't move")
                return False
            case TileType.WIDE_BOX_RIGHT:
                left_tile = self.tiles[tile.coordinate + Direction(-1, 0)]
                new_coord_left = left_tile.coordinate + move.direction
                new_coord_right = tile.coordinate + move.direction
                print(f"Trying to move {tile!s} from {tile.coordinate} to {new_coord_left} and {new_coord_right}.")
                match move.type:
                    case MoveType.UP | MoveType.DOWN:
                        if (
                            self.tiles[new_coord_left].type == TileType.FREE
                            and self.tiles[new_coord_right].type == TileType.FREE
                        ) or (
                            self.tiles[new_coord_right].type == TileType.FREE
                            and self.move_tile(self.tiles[new_coord_left], move, check_only=check_only)
                        ):
                            print(f"Moving {tile!s} at {tile.coordinate} {move}.")
                            self.move_single_tile(tile, move, check_only=check_only)
                            self.move_single_tile(left_tile, move, check_only=check_only)
                            return True
                        if self.move_tile(self.tiles[new_coord_left], move, check_only=True) and self.move_tile(
                            self.tiles[new_coord_right], move, check_only=True
                        ):
                            print(f"Moving {tile!s} at {tile.coordinate} {move} after moving other tiles.")
                            self.move_tile(self.tiles[new_coord_left], move, check_only=check_only)
                            self.move_tile(self.tiles[new_coord_right], move, check_only=check_only)
                            self.move_single_tile(tile, move, check_only=check_only)
                            self.move_single_tile(left_tile, move, check_only=check_only)
                            return True
                    case MoveType.RIGHT:
                        if self.move_single_tile(tile, move, check_only=check_only):
                            print(f"Moving {left_tile!s} at {tile.coordinate} {move}.")
                            self.move_single_tile(left_tile, move, check_only=check_only)
                            return True
                    case MoveType.LEFT:
                        if self.move_single_tile(left_tile, move, check_only=check_only):
                            print(f"Moving {tile!s} at {tile.coordinate} {move}.")
                            self.move_single_tile(tile, move, check_only=check_only)
                            return True
                print("Can't move")
                return False
            case TileType.WALL | TileType.FREE:
                return False
            case _:
                return self.move_single_tile(tile, move, check_only=check_only)

    def move_single_tile(self, tile: Tile, move: Move, *, check_only: bool = False) -> bool:
        new_coordinate = tile.coordinate + move.direction
        match (new_tile := self.tiles[new_coordinate]).type:
            case TileType.WALL:
                print(f"Can't move {tile!s} from {tile.coordinate} to {new_coordinate} due to wall.")
                return False
            case TileType.FREE:
                if not check_only:
                    print(f"Moving {tile!s} from {tile.coordinate} to {new_coordinate}.")
                    self.tiles[tile.coordinate], self.tiles[new_coordinate] = new_tile, tile
                    tile.coordinate = new_coordinate
            case TileType.BOX | TileType.WIDE_BOX_LEFT | TileType.WIDE_BOX_RIGHT:
                if not self.move_tile(new_tile, move, check_only=check_only):
                    print(f"Can't move {tile!s} from {tile.coordinate} to {new_coordinate} due to box.")
                    return False
                print(str(self))
                if not check_only:
                    # the tile at the new_coordinate MUST be free now since the box was pushed
                    self.tiles[tile.coordinate], self.tiles[new_coordinate] = self.tiles[new_coordinate], tile
                    print(
                        f"Moved {tile!s} from {tile.coordinate} to {new_coordinate} and pushed a {new_tile.type!s} box away."
                    )
                    tile.coordinate = new_coordinate
        return True

    def sum_of_boxes_gps_coordinates(self) -> int:
        return sum(
            tile.gps_coordinate for tile in self.tiles.values() if tile.type in (TileType.BOX, TileType.WIDE_BOX_LEFT)
        )

    def make_wide(self) -> None:
        new_tiles = {}
        for coord, tile in self.tiles.items():
            new_coord_left = coord * Coordinate(2, 1)
            new_coord_right = new_coord_left + Coordinate(1, 0)
            new_tile_type_left, new_tile_type_right = tile.type, tile.type

            match tile.type:
                case TileType.BOX:
                    new_tile_type_left = TileType.WIDE_BOX_LEFT
                    new_tile_type_right = TileType.WIDE_BOX_RIGHT
                case TileType.ROBOT:
                    new_tile_type_right = TileType.FREE

            new_tiles[new_coord_left] = Tile(new_tile_type_left, new_coord_left)
            new_tiles[new_coord_right] = Tile(new_tile_type_right, new_coord_right)
        self.tiles = new_tiles
        self.robot = next(tile for tile in self.tiles.values() if tile.type == TileType.ROBOT)


def main():
    print_day(15, "Warehouse Woes")

    # Part One: Find the sum of the GPS coordinates of all boxes after all moves.
    map_input, moves = get_input().split("\n\n")
    m = Map(map_input, moves)
    # m.move_robot()
    # print(f"Sum of GPS coordinates of all boxes after all moves: {m.sum_of_boxes_gps_coordinates()}")

    # Part Two: Find the sum of the GPS coordinates of all boxes after all moves with a wide map.
    m = Map(map_input, moves)
    m.make_wide()
    m.move_robot()
    print(f"Sum of GPS coordinates of all boxes after all moves for the wide map: {m.sum_of_boxes_gps_coordinates()}")


if __name__ == "__main__":
    main()
