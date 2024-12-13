import sys
from importlib import import_module

day = None
if len(sys.argv) == 2:
    day = int(sys.argv[1])

SOLUTIONS = {
    1: "_01_historian_hysteria",
    2: "_02_red_nosed_reports",
    3: "_03_mull_it_over",
    4: "_04_ceres_search",
    5: "_05_print_queue",
    6: "_06_guard_gallivant",
    7: "_07_bridge_repair",
    8: "_08_resonant_collinearity",
    9: "_09_disk_fragmenter",
    10: "_10_hoof_it",
    11: "_11_plutonian_pebbles",
    12: "_12_garden_groups",
    13: "_13_claw_contraption",
}

if day is not None:
    try:
        module = import_module(f".{SOLUTIONS[day]}", package="solutions")
        module.main()
    except KeyError:
        print(f"No solution for day {day} yet.")
else:
    for _, module_name in SOLUTIONS.items():
        module = import_module(f".{module_name}", package="solutions")
        module.main()
        print()
