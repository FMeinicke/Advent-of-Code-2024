from __future__ import annotations

from solutions._07_bridge_repair import Equation, Operator, parse_input

input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def test_07_parse_input():
    assert parse_input(input) == [
        Equation(190, [10, 19]),
        Equation(3267, [81, 40, 27]),
        Equation(83, [17, 5]),
        Equation(156, [15, 6]),
        Equation(7290, [6, 8, 6, 15]),
        Equation(161011, [16, 10, 13]),
        Equation(192, [17, 8, 14]),
        Equation(21037, [9, 7, 18, 13]),
        Equation(292, [11, 6, 16, 20]),
    ]


def test_07_find_possible_operators():
    equations = parse_input(input)
    for equation in equations:
        equation.find_possible_operators()
    assert equations[0].operators == [[Operator.MULTIPLY]]
    assert equations[1].operators == [
        [Operator.ADD, Operator.MULTIPLY],
        [Operator.MULTIPLY, Operator.ADD],
    ]
    assert equations[2].operators == []
    assert equations[3].operators == []
    assert equations[4].operators == []
    assert equations[5].operators == []
    assert equations[6].operators == []
    assert equations[7].operators == []
    assert equations[8].operators == [[Operator.ADD, Operator.MULTIPLY, Operator.ADD]]


def test_07_find_possible_operators_with_concat():
    equations = parse_input(input)
    for equation in equations:
        equation.find_possible_operators(with_concat=True)
    assert equations[0].operators == [[Operator.MULTIPLY]]
    assert equations[1].operators == [
        [Operator.ADD, Operator.MULTIPLY],
        [Operator.MULTIPLY, Operator.ADD],
    ]
    assert equations[2].operators == []
    assert equations[3].operators == [[Operator.CONCAT]]
    assert equations[4].operators == [
        [Operator.MULTIPLY, Operator.CONCAT, Operator.MULTIPLY]
    ]
    assert equations[5].operators == []
    assert equations[6].operators == [[Operator.CONCAT, Operator.ADD]]
    assert equations[7].operators == []
    assert equations[8].operators == [[Operator.ADD, Operator.MULTIPLY, Operator.ADD]]
