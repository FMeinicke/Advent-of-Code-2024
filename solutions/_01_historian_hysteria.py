from __future__ import annotations

from importlib.resources import files

from . import print_day


def main():
    print_day(1, "Historian Hysteria")

    left = []
    right = []

    with (files("solutions.inputs") / "01.txt").open() as file:
        for line in file:
            a, b = map(int, line.split())
            left.append(a)
            right.append(b)
    left.sort()
    right.sort()

    # Part One: Finding the total distance between the lists
    distances = [abs(a - b) for a, b in zip(left, right)]
    total_distance = sum(distances)
    print(f"Total distance: {total_distance}")

    # Part Two: Finding the similarity score of the lists
    similarities = [a * right.count(a) for a in left]
    similarity_score = sum(similarities)
    print(f"Similarity score: {similarity_score}")


if __name__ == "__main__":
    main()
