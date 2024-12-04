# Advent-of-Code-2024

Solutions to the Advent of Code 2024 Puzzles - https://adventofcode.com/2024

## Using this repo

### Running the solutions

- To run all available solutions, use

```shell
python -m solutions
```

- To only run the solutions for an individual day, run the `solutions` module with the number of the day (1-indexed) as the argument, e.g. for the 1st of December

```shell
python -m solutions 1
```

### Running the tests

Most puzzles contain example input data with an expected output. These have been used to construct test cases for the solutions.
To run the tests, use `pytest` as usual

```shell
pytest [-v]
```

You can also use `-k <test_name ...>` to run individual test cases.

### Adding solutions

The solutions to a puzzle live in a separate Python file. Each file contains the solutions for both parts of the puzzle.
To create a file for the solutions of a new day, use the [`_xx_template.py`](solutions/_xx_template.py) template file, copying it to the `solutions` module under an appropriate name for that day (e.g. `_01_historian_hysteria.py`).
Keep the naming format `_<two-digit day>_<sluggified_short_puzzle_title>.py`. The leading underscore is necessary because python module names must not start with a digit.
