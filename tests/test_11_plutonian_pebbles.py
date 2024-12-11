from __future__ import annotations

from solutions._11_plutonian_pebbles import Stones, StonesV2


def test_11_stones_mutate_simple():
    input = "0 1 10 99 999"
    stones = Stones(input)
    stones.mutate()
    assert str(stones) == "1 2024 1 0 9 9 2021976"


def test_11_stones_mutate_multiple():
    input = "125 17"
    stones = Stones(input)
    stones.mutate()
    assert str(stones) == "253000 1 7"
    stones.mutate()
    assert str(stones) == "253 0 2024 14168"
    stones.mutate()
    assert str(stones) == "512072 1 20 24 28676032"
    stones.mutate()
    assert str(stones) == "512 72 2024 2 0 2 4 2867 6032"
    stones.mutate()
    assert str(stones) == "1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32"
    stones.mutate()
    assert str(stones) == "2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2"
    assert len(stones) == 22
    stones.mutate(19)
    assert len(stones) == 55312


def test_11_stones_mutate_multiple_v2():
    input = "125 17"
    stones = Stones(input)
    stones_v2 = StonesV2(input)

    for i in range(25):
        print(i)
        stones.mutate()
        stones_v2.mutate()
        # stones_count = {}
        # for stone in stones:
        #     stones_count[stone.number] = stones_count.get(stone.number, 0) + 1
        # print(sorted(stones_count.items()))
        # print(stones_v2)
        assert len(stones) == len(stones_v2)
