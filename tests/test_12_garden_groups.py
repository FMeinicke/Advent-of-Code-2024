from __future__ import annotations

import pytest

from solutions._12_garden_groups import Garden


def test_12_garden_simple():
    input = """\
AAAA
BBCD
BBCC
EEEC\
"""

    garden = Garden(input)
    assert str(garden) == input

    # Part 1
    assert len(garden.regions) == 5
    assert garden.regions[0].area == 4
    assert garden.regions[1].area == 4
    assert garden.regions[2].area == 4
    assert garden.regions[3].area == 1
    assert garden.regions[4].area == 3
    assert garden.regions[0].perimeter == 10
    assert garden.regions[1].perimeter == 8
    assert garden.regions[2].perimeter == 10
    assert garden.regions[3].perimeter == 4
    assert garden.regions[4].perimeter == 8
    assert garden.fence_price == 140

    # Part 2
    print("\n".join(" ".join(f"{plot.plant} {plot.num_corners}" for plot in row) for row in garden.plots))
    assert garden.discounted_fence_price == 80


def test_12_garden_regions_within():
    input = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO\
"""

    garden = Garden(input)
    assert str(garden) == input

    # Part 1
    assert len(garden.regions) == 5
    assert garden.regions[0].area == 21
    assert garden.regions[1].area == 1
    assert garden.regions[2].area == 1
    assert garden.regions[3].area == 1
    assert garden.regions[4].area == 1
    assert garden.regions[0].perimeter == 36
    assert garden.regions[1].perimeter == 4
    assert garden.regions[2].perimeter == 4
    assert garden.regions[3].perimeter == 4
    assert garden.regions[4].perimeter == 4
    assert garden.fence_price == 772

    # Part 2

    print("\n".join(" ".join(f"{plot.plant} {plot.num_corners}" for plot in row) for row in garden.plots))

    assert garden.discounted_fence_price == 436


def test_12_garden_large():
    input = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE\
"""

    garden = Garden(input)
    assert str(garden) == input

    for r in garden.regions:
        print(str(r))

    # Part 1
    assert len(garden.regions) == 11
    assert garden.regions[0].area == 12
    assert garden.regions[1].area == 4
    assert garden.regions[2].area == 14
    assert garden.regions[3].area == 10
    assert garden.regions[4].area == 13
    assert garden.regions[5].area == 11
    assert garden.regions[6].area == 1
    assert garden.regions[7].area == 13
    assert garden.regions[8].area == 14
    assert garden.regions[9].area == 5
    assert garden.regions[10].area == 3
    assert garden.regions[0].perimeter == 18
    assert garden.regions[1].perimeter == 8
    assert garden.regions[2].perimeter == 28
    assert garden.regions[3].perimeter == 18
    assert garden.regions[4].perimeter == 20
    assert garden.regions[5].perimeter == 20
    assert garden.regions[6].perimeter == 4
    assert garden.regions[7].perimeter == 18
    assert garden.regions[8].perimeter == 22
    assert garden.regions[9].perimeter == 12
    assert garden.regions[10].perimeter == 8
    assert garden.fence_price == 1930

    # Part 2
    assert garden.regions[0].num_sides == 10
    assert garden.regions[1].num_sides == 4
    assert garden.regions[2].num_sides == 22
    assert garden.regions[3].num_sides == 12
    assert garden.regions[4].num_sides == 10
    assert garden.regions[5].num_sides == 12
    assert garden.regions[6].num_sides == 4
    assert garden.regions[7].num_sides == 8
    assert garden.regions[8].num_sides == 16
    assert garden.regions[9].num_sides == 6
    assert garden.regions[10].num_sides == 6
    assert garden.discounted_fence_price == 1206

    #   | 0 1 2 3 4 5 6 7 8 9
    # --+--------------------
    # 0 | R R R R I I C C F F
    # 1 | R R R R I I C C C F
    # 2 | V V R R R C C F F F
    # 3 | V V R C C C J F F F
    # 4 | V V V V C J J C F E
    # 5 | V V I V C C J J E E
    # 6 | V V I I I C J J E E
    # 7 | M I I I I I J J E E
    # 8 | M I I I S I J E E E
    # 9 | M M M I S S J E E E

    # A region of R plants with price 12 * 18 = 216.
    # A region of I plants with price 4 * 8 = 32.
    # A region of C plants with price 14 * 28 = 392.
    # A region of F plants with price 10 * 18 = 180.
    # A region of V plants with price 13 * 20 = 260.
    # A region of J plants with price 11 * 20 = 220.
    # A region of C plants with price 1 * 4 = 4.
    # A region of E plants with price 13 * 18 = 234.
    # A region of I plants with price 14 * 22 = 308.
    # A region of M plants with price 5 * 12 = 60.
    # A region of S plants with price 3 * 8 = 24.


@pytest.mark.parametrize(
    "input, expected_fence_price",
    (
        pytest.param(
            """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE\
""",
            236,
            id="e-shaped",
        ),
        pytest.param(
            """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA\
""",
            368,
            id="two-inner-regions",
        ),
        pytest.param(
            """\
AAAAAAAA
AACBBDDA
AACBBAAA
ABBAAAAA
ABBADDDA
AAAADADA
AAAAAAAA\
""",
            946,
            id="reddit-1",
        ),
        pytest.param(
            """\
CCAAA
CCAAA
AABBA
AAAAA\
""",
            164,
            id="reddit-2",
        ),
        pytest.param(
            """\
OOOOO
OXOXO
OXXXO\
""",
            160,
            id="reddit-3",
        ),
        pytest.param(
            """\
.....
.AAA.
.A.A.
.AA..
.A.A.
.AAA.
.....\
""",
            452,
            id="reddit-4",
        ),
    ),
)
def test_12_garden_discounted_fence_price(input: str, expected_fence_price: int) -> None:
    garden = Garden(input)
    print(len(garden.regions))
    assert garden.discounted_fence_price == expected_fence_price


def test_12_garden_discounted_fence_price_2() -> None:
    input = """\
.....
.AAA.
.A.A.
.AA..
.A.A.
.AAA.
.....\
"""
    garden = Garden(input)
    print(len(garden.regions))
    assert len(garden.regions) == 4
    print("\n".join(str(region) for region in garden.regions ))
    print("\n".join(" ".join(f"{plot.plant} {plot.num_corners}" for plot in row) for row in garden.plots))
    print(garden.regions[1].num_sides, garden.regions[1].area)
    assert garden.fence_price == 1202
    assert garden.regions[1].fence_price == 312
    assert garden.regions[1].discounted_fence_price == 192
    assert garden.discounted_fence_price == 452
