from __future__ import annotations

from importlib.resources import files
from typing import Iterable, TypeAlias

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "04.txt").open() as file:
        return file.read()


WordSearchLine: TypeAlias = list[str]
WordSearch: TypeAlias = list[WordSearchLine]


XMAS = "XMAS"
XMAS_REVERSED = XMAS[::-1]


def count_xmas_horizontal(word_search: WordSearch) -> int:
    return sum(
        (line := "".join(row)).count(XMAS) + line.count(XMAS_REVERSED)
        for row in word_search
    )


def count_xmas_vertical(word_search: WordSearch) -> int:
    return sum(
        (col := "".join(column)).count(XMAS) + col.count(XMAS_REVERSED)
        for column in zip(*word_search)
    )


def count_xmas_diagonal(word_search: WordSearch) -> int:
    def get_diagonal(i: int, j: int) -> str:
        return "".join(
            word_search[i + k][j + k]
            for k in range(len(XMAS))
            if 0 <= i + k < len(word_search) and 0 <= j + k < len(word_search[i])
        )

    return sum(
        (diagonal := get_diagonal(i, j)).count(XMAS) + diagonal.count(XMAS_REVERSED)
        for i in range(len(word_search))
        for j in range(len(word_search[i]))
    )


def count_xmas_diagonal_reverse(word_search: WordSearch) -> int:
    def get_reverse_diagonal(i: int, j: int) -> str:
        return "".join(
            word_search[i + k][j - k]
            for k in range(len(XMAS))
            if 0 <= i + k < len(word_search) and 0 <= j - k < len(word_search[i])
        )

    return sum(
        (diagonal := get_reverse_diagonal(i, j)).count(XMAS)
        + diagonal.count(XMAS_REVERSED)
        for i in range(len(word_search))
        for j in range(len(word_search[i]))
    )


def count_xmas(word_search: WordSearch) -> int:
    return (
        count_xmas_horizontal(word_search)
        + count_xmas_vertical(word_search)
        + count_xmas_diagonal(word_search)
        + count_xmas_diagonal_reverse(word_search)
    )


MAS = "MAS"
MAS_REVERSED = MAS[::-1]


def count_x_mas(word_search: WordSearch) -> int:
    # for every cell in the grid
    # get the first diagonal using the top left and bottom right corners
    # get the second diagonal using the top right and bottom left corners
    # check if both diagonals contain 'MAS' or 'SAM'

    def get_diagonal_top_left_bottom_right(i: int, j: int) -> str:
        return "".join(
            word_search[i + k][j + k]
            for k in range(-1, len(MAS) - 1)
            if 0 <= i + k < len(word_search) and 0 <= j + k < len(word_search[i])
        )

    def get_diagonal_top_right_bottom_left(i: int, j: int) -> str:
        return "".join(
            word_search[i + k][j - k]
            for k in range(-1, len(MAS) - 1)
            if 0 <= i + k < len(word_search) and 0 <= j - k < len(word_search[i])
        )

    return sum(
        (get_diagonal_top_left_bottom_right(i, j) in (MAS, MAS_REVERSED))
        and (get_diagonal_top_right_bottom_left(i, j) in (MAS, MAS_REVERSED))
        for i in range(len(word_search))
        for j in range(len(word_search[i]))
    )


def main():
    print_day(4, "Ceres Search")

    # Part One: Count the number of times XMAS appears

    word_search = tuple(tuple(line) for line in get_input().splitlines())
    num_xmas = count_xmas(word_search)
    print(f"Number of times XMAS appears: {num_xmas}")

    # Part Two: Count the number of times an X-MAS appears
    # an X-MAS is an X shape made out of two diagonal 'MAS'es where each MAS might be written forwards or backwards

    num_x_mas = count_x_mas(word_search)
    print(f"Number of times X-MAS appears: {num_x_mas}")


if __name__ == "__main__":
    main()
