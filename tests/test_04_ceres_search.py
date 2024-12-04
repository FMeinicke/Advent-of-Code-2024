from __future__ import annotations

from solutions._04_ceres_search import (
    count_x_mas,
    count_xmas,
    count_xmas_diagonal,
    count_xmas_diagonal_reverse,
    count_xmas_horizontal,
    count_xmas_vertical,
)


def test_count_xmas():
    # . . . . X X M A S .
    # . S A M X M S . . .
    # . . . S . . A . . .
    # . . A . A . M S . X
    # X M A S A M X . M M
    # X . . . . . X A . A
    # S . S . S . S . S S
    # . A . A . A . A . A
    # . . M . M . M . M M
    # . X . X . X M A S X
    input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
    # M M M S X X M A S M
    # M S A M X M S M S A
    # A M X S X M A A M M
    # M S A M A S M S M X
    # X M A S A M X A M M
    # X X A M M X X A M A
    # S M S M S A S X S S
    # S A X A M A S A A A
    # M A M M M X M M M M
    # M X M X A X M A S X
    # input = """....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX
# """

    word_search = tuple(tuple(line) for line in input.splitlines())
    assert count_xmas_horizontal(word_search) == 5
    assert count_xmas_vertical(word_search) == 3
    assert count_xmas_diagonal(word_search) == 5
    assert count_xmas_diagonal_reverse(word_search) == 5
    assert count_xmas(word_search) == 18


def test_count_x_mas():
    input = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
"""
    word_search = tuple(tuple(line) for line in input.splitlines())
    assert count_x_mas(word_search) == 9
