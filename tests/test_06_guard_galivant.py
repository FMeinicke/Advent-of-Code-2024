from __future__ import annotations

from solutions._06_guard_gallivant import Map

input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def test_map_init() -> None:
    m = Map(input)
    print(m)
    assert str(m) == input


def test_map_predict_guard_movements() -> None:
    m = Map(input)
    m.predict_guard_movements()
    expected = """....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X.."""
    assert str(m) == expected
    assert m.count_visited() == 41


def test_map_find_possible_obstructions() -> None:
    m = Map(input)
    m.find_possible_obstructions()
    assert m.count_possible_obstructions() == 6

