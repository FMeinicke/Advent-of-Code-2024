import sys
from importlib import import_module

day = None
if len(sys.argv) == 2:
    day = int(sys.argv[1])

SOLUTIONS = {
    1: "_01_historian_hysteria",
    2: "_02_red_nosed_reports",
    3: "_03_mull_it_over",
}

if day is not None:
    try:
        module = import_module(f".{SOLUTIONS[day]}", package="solutions")
    except KeyError:
        print(f"No solution for day {day} yet.")
else:
    for _, module_name in SOLUTIONS.items():
        import_module(f".{module_name}", package="solutions")
        print()
