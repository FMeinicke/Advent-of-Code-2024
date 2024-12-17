from __future__ import annotations

from solutions._16_reindeer_maze import Maze, print_solved_maze, MoveType


def test_16_maze_simple1():
    maze_input = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############\
"""

    m = Maze(maze_input)
    assert str(m) == maze_input
    solutions = m.solve()
    # for solution in solutions:
    #     print(len(solution))
    #     print(len(list(filter(lambda m: m.move_type == MoveType.TURN, solution))))
    #     print(solution.score)
    #     if solution.score < 8000:
    #         # print(list(map(str, solution)))
    #         print_solved_maze(m, solution)
    assert min(solution.score for solution in solutions) == 7036

    # print("Iterative")
    # solutions_iterative = m.solve_iterative()
    # assert min(solution.score for solution in solutions_iterative) == 7036

    sol = m.solve_a_star()
    print_solved_maze(m, sol)
    assert sol.score == 7036


def test_16_maze_simple2():
    maze_input = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################\
"""

    m = Maze(maze_input)
    assert str(m) == maze_input
    solutions = m.solve()
    for solution in solutions:
        print(len(solution))
        print(len(list(filter(lambda m: m.move_type == MoveType.TURN, solution))))
        print(solution.score)
        if solution.score < 11500:
            # print(list(map(str, solution)))
            print_solved_maze(m, solution)
    assert min(solution.score for solution in solutions) == 11048
