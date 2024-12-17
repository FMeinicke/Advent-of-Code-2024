from __future__ import annotations

import heapq
import sys
from collections import deque
from enum import Enum, StrEnum
from importlib.resources import files
from typing import ClassVar, NamedTuple, cast

from . import print_day

sys.setrecursionlimit(10000)


def get_input() -> str:
    with (files("solutions.inputs") / "16.txt").open() as file:
        return file.read()


class TileType(StrEnum):
    WALL = "#"
    WAY = "."
    START = "S"
    END = "E"


class Distance(NamedTuple):
    dx: int
    dy: int

    def rotate_left(self) -> Distance:
        return Distance(-self.dy, self.dx)

    NORTH: ClassVar[Distance] = None
    EAST: ClassVar[Distance] = None
    SOUTH: ClassVar[Distance] = None
    WEST: ClassVar[Distance] = None


Distance.NORTH = Distance(0, -1)
Distance.EAST = Distance(1, 0)
Distance.SOUTH = Distance(0, 1)
Distance.WEST = Distance(-1, 0)


class Coordinate(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Distance) -> Coordinate:
        return Coordinate(self.x + other.dx, self.y + other.dy)


class Node:
    tile_type: TileType
    coordinate: Coordinate
    maze: Maze
    visited: bool

    def __init__(self, tile_type: TileType, coordinate: Coordinate, maze: Maze):
        self.tile_type = tile_type
        self.coordinate = coordinate
        self.maze = maze
        self.visited = False

    def __repr__(self):
        return f"Node({self.tile_type}, {self.coordinate})"

    @property
    def neighbors(self) -> list[Node]:
        return [
            self.coordinate + distance
            for distance in (
                Distance.NORTH,
                Distance.EAST,
                Distance.SOUTH,
                Distance.WEST,
            )
            if (
                0 <= self.coordinate.y + distance.dy < len(self.maze.nodes)
                and 0 <= self.coordinate.x + distance.dx < len(self.maze.nodes[0])
            )
        ]

    def neighbor(self, distance: Distance) -> Node:
        return self.maze[self.coordinate + distance]

    def __lt__(self, other):
        return (self.coordinate.y, self.coordinate.x) < (other.coordinate.y, other.coordinate.x)

    def __eq__(self, other):
        return (self.coordinate.y, self.coordinate.x) == (other.coordinate.y, other.coordinate.x)

    def __hash__(self):
        return hash((self.coordinate.y, self.coordinate.x))


class MoveType(Enum):
    WALK = 1
    TURN = 1001


class Move(NamedTuple):
    move_type: MoveType
    coordinate: Coordinate
    direction: Distance
    from_node: Node | None = None

    def __str__(self):
        match self.direction:
            case Distance.NORTH:
                return "^"
            case Distance.EAST:
                return ">"
            case Distance.SOUTH:
                return "v"
            case Distance.WEST:
                return "<"


class Solution(NamedTuple):
    moves: list[Move]

    @property
    def score(self) -> int:
        return sum(move.move_type.value for move in self.moves) - 1

    def __len__(self):
        return len(self.moves)

    def __iter__(self) -> iter[Move]:
        return self.moves.__iter__()


class Maze:
    nodes: list[list[Node]]
    start_node: Node
    end_node: Node

    def __init__(self, maze: str):
        self.nodes = [
            [Node(TileType(char), Coordinate(x, y), self) for x, char in enumerate(line)]
            for y, line in enumerate(maze.splitlines())
        ]
        self.start_node = next(node for row in self.nodes for node in row if node.tile_type == TileType.START)
        self.end_node = next(node for row in self.nodes for node in row if node.tile_type == TileType.END)

    def __str__(self):
        return "\n".join("".join(node.tile_type.value for node in row) for row in self.nodes)

    def __getitem__(self, coordinate: Coordinate) -> Node:
        return self.nodes[coordinate.y][coordinate.x]

    def solve(self) -> list[Solution]:
        all_solutions = []

        def solve_recursive(node: Node, direction: Distance, current_solution: Solution) -> None:
            if node == self.end_node:
                all_solutions.append(Solution([*current_solution, Move(MoveType.WALK, node.coordinate, direction)]))
                print("found solution")
                return

            node.visited = True
            move_type = MoveType.WALK
            for _ in range(4):
                neighbor = node.neighbor(direction)
                if not neighbor.visited and neighbor.tile_type != TileType.WALL:
                    # print(f"visiting {neighbor}")
                    solve_recursive(
                        neighbor, direction, [*current_solution, Move(move_type, node.coordinate, direction)]
                    )
                # else:
                #     print(f"not visiting {neighbor}")
                direction = direction.rotate_left()
                move_type = MoveType.TURN
            node.visited = False

        solve_recursive(self.start_node, Distance.EAST, [])
        return all_solutions

    def solve_iterative(self) -> list[Solution]:
        all_solutions: list[Solution] = []
        queue = deque([(self.start_node, Distance.EAST, [])])

        while queue:
            node, direction, current_solution = queue.popleft()

            if node == self.end_node:
                all_solutions.append(Solution([*current_solution, Move(MoveType.WALK, node.coordinate, direction)]))
                print(f"found solution {all_solutions[-1].score}")
                continue

            if node.visited:
                continue

            node.visited = True
            move_type = MoveType.WALK
            for _ in range(4):
                neighbor = node.neighbor(direction)
                if not neighbor.visited and neighbor.tile_type != TileType.WALL:
                    # print(f"visiting {neighbor}")
                    match move_type:
                        case MoveType.WALK:
                            queue.appendleft(
                                (neighbor, direction, [*current_solution, Move(move_type, node.coordinate, direction)])
                            )
                        case MoveType.TURN:
                            queue.append(
                                (neighbor, direction, [*current_solution, Move(move_type, node.coordinate, direction)])
                            )
                # else:
                #     print(f"not visiting {neighbor}")
                direction = direction.rotate_left()
                move_type = MoveType.TURN
            node.visited = False

        return all_solutions

    def solve_a_star(self) -> Solution | None:
        start_node = self.start_node
        end_node = self.end_node

        def heuristic(a: Coordinate, b: Coordinate) -> int:
            return abs(a.x - b.x) + abs(a.y - b.y)

        heap = []
        heapq.heappush(heap, (0, start_node, None, Distance.EAST))  # (cost, current_node, previous_node, direction)
        came_from: dict[Node, Move] = {start_node: Move(MoveType.WALK, start_node.coordinate, Distance.EAST)}
        g_score = {start_node: 0}
        f_score = {start_node: heuristic(start_node.coordinate, end_node.coordinate)}

        while heap:
            # fmt: off
            current_cost, current, previous, direction = \
                cast(tuple[int, Node, Node | None, Distance | None], heapq.heappop(heap))
            # fmt: on

            if current == end_node:
                path = []
                while current in came_from:
                    move = came_from[current]
                    path.append(move)
                    current = move.from_node
                path.reverse()
                return Solution(path)

            if current.visited:
                continue

            current.visited = True
            for new_direction in (
                direction,
                direction.rotate_left(),
                direction.rotate_left().rotate_left(),
                direction.rotate_left().rotate_left().rotate_left(),
            ):
                neighbor = current.neighbor(new_direction)
                if neighbor.visited or neighbor.tile_type == TileType.WALL:
                    continue

                move_cost = 1 if direction == new_direction else 1001
                tentative_g_score = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = Move(
                        MoveType.WALK if move_cost == 1 else MoveType.TURN,
                        neighbor.coordinate,
                        new_direction,
                        from_node=current,
                    )
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor.coordinate, end_node.coordinate)
                    heapq.heappush(heap, (f_score[neighbor], neighbor, current, new_direction))

        return None


def print_solved_maze(maze: Maze, solution: Solution):
    nodes = [list(map(lambda n: str(n.tile_type), row)) for row in maze.nodes]
    for move in solution:
        if maze[move.coordinate].tile_type == TileType.WAY:
            nodes[move.coordinate.y][move.coordinate.x] = str(move)
    print("\n".join("".join(str(node) for node in row) for row in nodes))


def main():
    print_day(16, "Reindeer Maze")

    # Part One: Find the lowest score for solutions of the maze.
    maze = Maze(get_input())
    # solutions = maze.solve()
    # lowest_score = min(solution.score for solution in solutions)
    # print(f"Lowest score: {lowest_score}")
    solution = maze.solve_a_star()
    print(f"Lowest score: {solution.score}")

    # Part Two:


if __name__ == "__main__":
    main()
