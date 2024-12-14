from __future__ import annotations

from solutions._14_restroom_redoubt import Coordinate, Robot, calculate_safety_factor, count_robots_in_quadrant

input = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3\
"""


def test_14_robot_init():
    for line in input.splitlines():
        robot = Robot(line, width=11, height=7)
        assert str(robot) == line


def test_14_robot_move():
    r = Robot("p=2,4 v=2,-3", width=11, height=7)
    assert r.position == Coordinate(2, 4)
    r.move()
    assert r.position == Coordinate(4, 1)
    r.move()
    assert r.position == Coordinate(6, 5)
    r.move()
    assert r.position == Coordinate(8, 2)
    r.move()
    assert r.position == Coordinate(10, 6)
    r.move()
    assert r.position == Coordinate(1, 3)

def test_14_robot_safety_factor():
    robots = [Robot(line, width=11, height=7) for line in input.splitlines()]
    for r in robots:
        r.move(100)
    assert count_robots_in_quadrant(robots, 1) == 1
    assert count_robots_in_quadrant(robots, 2) == 3
    assert count_robots_in_quadrant(robots, 3) == 4
    assert count_robots_in_quadrant(robots, 4) == 1
    assert calculate_safety_factor(robots) == 12
