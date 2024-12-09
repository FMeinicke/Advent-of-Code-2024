from __future__ import annotations

from enum import StrEnum
from functools import reduce
from importlib.resources import files
from itertools import product

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "07.txt").open() as file:
        return file.read()


class Operator(StrEnum):
    ADD = "+"
    MULTIPLY = "*"
    CONCAT = "||"

    def evaluate(self, a: int, b: int) -> int:
        match self:
            case Operator.ADD:
                return a + b
            case Operator.MULTIPLY:
                return a * b
            case Operator.CONCAT:
                return int(str(a) + str(b))
            case _:
                raise ValueError(f"Unknown operator: {self}")



class Equation:
    result: int
    operands: list[int]
    operators: list[list[Operator]]

    def __init__(self, result: int, operands: list[int]):
        self.result = result
        self.operands = operands
        self.operators = []

    @staticmethod
    def from_str(s: str) -> Equation:
        result, terms = s.split(": ")
        return Equation(int(result), list(map(int, terms.split())))

    def find_possible_operators(self, *, with_concat: bool = False) -> None:
        operators = list(Operator)
        if not with_concat:
            operators.remove(Operator.CONCAT)
        possible_operator_combinations = list(
            product(operators, repeat=len(self.operands) - 1)
        )
        # print(f" permutations for {self} -> {possible_operator_combinations}")
        for operators in possible_operator_combinations:
            if self.evaluate(operators) == self.result:
                self.operators.append(list(operators))

    def evaluate(self, operators: list[Operator]) -> int:
        # print(f"evaluating {self.operands} with {operators}")
        return reduce(
            lambda acc, op: op[0].evaluate(acc, op[1]),
            zip(operators, self.operands[1:]),
            self.operands[0],
        )

    def has_possible_solutions(self) -> bool:
        return bool(self.operators)

    def __str__(self) -> str:
        if not self.operators:
            return f"{self.result}: {' '.join(map(str, self.operands))}"

        equations = []
        for operators in self.operators:
            terms = [str(self.operands[0])]
            for i, operand in enumerate(self.operands[1:]):
                terms.append(str(operators[i]))
                terms.append(str(operand))
            equations.append(f"{self.result}: {' '.join(terms)}")
        return "\n".join(equations)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Equation):
            raise TypeError(f"Cannot compare Equation with {type(other)}")
        return (
            self.result == other.result
            and self.operands == other.operands
            and self.operators == other.operators
        )


def parse_input(input: str) -> list[Equation]:
    return [Equation.from_str(line) for line in input.splitlines()]


def main():
    print_day(7, "Bridge Repair")

    # Part One: Find the total calibration result of the equations that could possibly be true

    equations = parse_input(get_input())
    for eq in equations:
        eq.find_possible_operators()
    equations_with_possible_solutions = [
        eq for eq in equations if eq.has_possible_solutions()
    ]
    sum_of_possible_solutions = sum(
        eq.result for eq in equations_with_possible_solutions
    )
    print(f"Total calibration result: {sum_of_possible_solutions}")

    # Part Two: Find the total calibration result of the equations that could possibly be true with the concat operator
    print("Trying with the concat operator (this may take a while)...")
    for eq in equations:
        eq.operators = []
        eq.find_possible_operators(with_concat=True)
    equations_with_possible_solutions = [
        eq for eq in equations if eq.has_possible_solutions()
    ]
    sum_of_possible_solutions = sum(
        eq.result for eq in equations_with_possible_solutions
    )
    print(f"Total calibration result with concat operator: {sum_of_possible_solutions}")

if __name__ == "__main__":
    main()
