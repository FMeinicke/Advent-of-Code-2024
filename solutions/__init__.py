from __future__ import annotations

def print_day(day: int, name: str = "") -> None:
    print("=" * 25)
    print(f"Day {day:02}{f': {name}' if name else ''}")
    print("=" * 25)