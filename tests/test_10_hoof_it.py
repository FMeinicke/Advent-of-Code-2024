from __future__ import annotations

import pytest

from solutions._10_hoof_it import TopographicMap


@pytest.mark.parametrize(
    "input, expected_score_sum",
    (
        pytest.param(
            """0123
1234
8765
9876""",
            1,
            id="simple",
        ),
        pytest.param(
            """AAA0AAA
AAA1AAA
AAA2AAA
6543456
7AAAAA7
8AAAAA8
9AAAAA9""",
            2,
            id="simple_2",
        ),
        pytest.param(
            """AA90AA9
AAA1A98
AAA2AA7
6543456
765A987
876AAAA
987AAAA""",
            4,
            id="simple_4",
        ),
        pytest.param(
            """10AA9AA
2AAA8AA
3AAA7AA
4567654
AAA8AA3
AAA9AA2
AAAAA01""",
            3,
            id="two_heads",
        ),
        pytest.param(
            """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""",
            36,
            id="nine_heads",
        ),
        # pytest.param(
        #     """""",
        #     1,
        #     id="",
        # ),
    ),
)
def test_10_trailhead_score(input: str, expected_score_sum: int) -> None:
    map = TopographicMap(input)
    assert str(map) == input
    assert map.sum_of_trailhead_scores() == expected_score_sum, map.str_with_reachable_nine_heights()

@pytest.mark.parametrize(
    "input, expected_rating_sum",
    (
        pytest.param(
            """AAAAA0A
AA4321A
AA5AA2A
AA6543A
AA7AA4A
AA8765A
AA9AAAA""",
            3,
            id="single_rating_3",
        ),
        pytest.param(
            """AA90AA9
AAA1A98
AAA2AA7
6543456
765A987
876AAAA
987AAAA""",
            13,
            id="single_rating_13",
        ),
        pytest.param(
            """012345
123456
234567
345678
4A6789
56789A""",
            227,
            id="single_rating_227",
        ),
        pytest.param(
            """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""",
            81,
            id="nine_heads_rating_81",
        ),
        # pytest.param(
        #     """""",
        #     1,
        #     id="",
        # ),
    ),
)
def test_10_trailhead_rating(input: str, expected_rating_sum: int) -> None:
    map = TopographicMap(input)
    assert str(map) == input
    assert map.sum_of_trailhead_ratings() == expected_rating_sum, map.str_with_reachable_nine_heights()
