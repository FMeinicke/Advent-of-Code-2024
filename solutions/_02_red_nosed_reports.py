from __future__ import annotations

from importlib.resources import files
from typing import TypeAlias

from . import print_day

Level: TypeAlias = list[int]
Report: TypeAlias = list[Level]

reports: list[Report] = []

with (files("solutions.inputs") / "02.txt").open() as file:
    for line in file:
        reports.append(list(map(int, line.split())))


def is_report_safe(report: Report) -> bool:
    """
    Checks if a report is safe.

    A report is safe if
    - the levels are either all increasing or decreasing
    - any two adjacent levels differ by at least one and at most three
    """

    all_increasing = all(report[i] < report[i + 1] for i in range(len(report) - 1))
    all_decreasing = all(report[i] > report[i + 1] for i in range(len(report) - 1))
    adjacent_distance = all(
        1 <= abs(report[i + 1] - report[i]) <= 3 for i in range(len(report) - 1)
    )

    return (all_increasing or all_decreasing) and adjacent_distance


def is_report_safe_with_problem_dampener(report: Report) -> bool:
    """
    Checks if a report is safe with the problem dampener.

    The Problem Dampener can remove one level from the report to make it safe.
    The same rules apply as in is_report_safe.
    """

    for i in range(len(report)):
        if is_report_safe(report[:i] + report[i + 1 :]):
            return True

    return False


def main():
    print_day(2, "Red-Nosed Reports")

    # Part One: Count the number of safe reports

    safe_reports = list(filter(is_report_safe, reports))
    print(f"Number of safe reports: {len(safe_reports)}")

    # Part Two: Problem Dampener

    safe_reports_with_problem_dampener = list(
        filter(is_report_safe_with_problem_dampener, reports)
    )
    print(
        f"Number of safe reports with problem dampener: {len(safe_reports_with_problem_dampener)}"
    )


if __name__ == "__main__":
    main()
