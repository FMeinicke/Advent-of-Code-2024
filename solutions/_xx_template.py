from __future__ import annotations

from importlib.resources import files

from . import print_day


def get_input() -> str:
    with (files("solutions.inputs") / "xx.txt").open() as file:
        return file.read()


def main():
    print_day(x, "")

    # Part One:

    # Part Two:


if __name__ == "__main__":
    main()
