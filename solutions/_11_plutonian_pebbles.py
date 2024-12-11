from __future__ import annotations

from importlib.resources import files
from time import perf_counter_ns
from typing import TypeAlias

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "11.txt").open() as file:
        return file.read()


class Stone:
    number: int

    def __init__(self, number: int):
        self.number = number

    def mutate(self) -> list[Stone]:
        if self.number == 0:
            self.number = 1
            return [self]

        if (length := len(self)) % 2 == 0:
            number_str = str(self.number)
            return [Stone(int(number_str[: length // 2])), Stone(int(number_str[length // 2 :]))]

        self.number *= 2024
        return [self]

    def __str__(self):
        return str(self.number)

    def __len__(self):
        return len(str(self.number))


class Stones:
    stones: list[Stone]

    def __init__(self, input: str):
        self.stones = [Stone(int(number)) for number in input.split()]

    def mutate(self, number_of_times: int = 1) -> None:
        for i in range(number_of_times):
            start = perf_counter_ns()
            self.stones = [s for stone in self.stones for s in stone.mutate()]
            print(f"Mutation {i + 1} took {(perf_counter_ns() - start) / 1_000_000:.3f}ms")

    def __str__(self):
        return " ".join(str(stone) for stone in self.stones)

    def __iter__(self):
        return iter(self.stones)

    def __len__(self):
        return len(self.stones)


StoneV2: TypeAlias = int


class StonesV2:
    stones: dict[StoneV2, int]

    def __init__(self, input: str):
        self.stones = {StoneV2(number): 1 for number in input.split()}

    def mutate(self, number_of_times: int = 1) -> None:
        for i in range(number_of_times):
            start = perf_counter_ns()
            new_stones = {}
            for stone, count in self.stones.items():
                if stone == 0:
                    new_stones[1] = new_stones.get(1, 0) + count
                    # print(f"{count} number of 0 stones are replaced by 1 stones")
                elif (length := len(stone_str := str(stone))) % 2 == 0:
                    new_stone_upper = StoneV2(stone_str[: length // 2])
                    new_stone_lower = StoneV2(stone_str[length // 2 :])
                    new_stones[new_stone_upper] = new_stones.get(new_stone_upper, 0) + count
                    new_stones[new_stone_lower] = new_stones.get(new_stone_lower, 0) + count
                    # print(
                    #     f"{count} number of {stone} stones are replaced by {new_stones[new_stone_upper]} number of {new_stone_upper} stones and {new_stones[new_stone_lower]} number of {new_stone_lower} stones"
                    # )
                else:
                    new_stone = stone * 2024
                    new_stones[new_stone] = new_stones.get(new_stone, 0) + count
                    # print(
                    #     f"{count} number of {stone} stones are replaced by {new_stones[new_stone]} number of {new_stone} stones"
                    # )

            self.stones = new_stones
            print(f"Mutation {i + 1} took {(perf_counter_ns() - start) / 1_000_000:.3f}ms")

    def __str__(self):
        return str(sorted(self.stones.items()))

    def __len__(self) -> int:
        return sum(self.stones.values())


def main():
    print_day(11, "Plutonian Pebbles")

    # Part One: How many stones are there after blinking 25 times?
    stones = Stones(get_input())
    stones.mutate(25)
    print(f"Stones after blinking 25 times: {len(stones)}")

    # Part Two: How many stones are there after blinking 75 times?
    stones = StonesV2(get_input())
    stones.mutate(75)
    print(f"Stones after blinking 75 times: {len(stones)}")

    # Part Two:


if __name__ == "__main__":
    main()
