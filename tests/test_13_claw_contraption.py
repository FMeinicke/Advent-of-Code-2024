from __future__ import annotations

import pytest

from solutions._13_claw_contraption import Machine


@pytest.mark.parametrize(
    "machine_input, expected_token_cost",
    (
        pytest.param(
            """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400\
""",
            280,
            id="simple_1",
        ),
        pytest.param(
            """\
Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176\
""",
            0,
            id="simple_2_no_solution",
        ),
        pytest.param(
            """\
Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450\
""",
            200,
            id="simple_3",
        ),
        pytest.param(
            """\
Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279\
""",
            0,
            id="simple_4_no_solution",
        ),
    ),
)
def test_13_part1(machine_input: str, expected_token_cost: int):
    machine = Machine(machine_input)
    assert str(machine) == machine_input
    assert machine.calculate_token_cost() == expected_token_cost


@pytest.mark.parametrize(
    "machine_input, solvable",
    (
        pytest.param(
            """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400\
""",
            False,
            id="simple_1_no_solution",
        ),
        pytest.param(
            """\
Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176\
""",
            True,
            id="simple_2",
        ),
        pytest.param(
            """\
Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450\
""",
            False,
            id="simple_3_no_solution",
        ),
        pytest.param(
            """\
Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279\
""",
            True,
            id="simple_4",
        ),
    ),
)
def test_13_part2(machine_input: str, solvable: bool):
    machine = Machine(machine_input)
    assert str(machine) == machine_input
    assert (machine.calculate_token_cost(offset=10000000000000) > 0) == solvable
