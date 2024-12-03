from __future__ import annotations

from solutions._03_mull_it_over import (
    find_enabled_uncorrupted_mul_instructions,
    find_uncorrupted_mul_instructions,
    mul,  # noqa: F401 # needed for eval below
)


def test_find_uncorrupted_mul_instructions():
    corrupted_memory = (
        "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    )
    uncorrupted_mul_instructions = find_uncorrupted_mul_instructions(corrupted_memory)
    assert uncorrupted_mul_instructions == [
        "mul(2,4)",
        "mul(5,5)",
        "mul(11,8)",
        "mul(8,5)",
    ]
    assert sum(eval(instruction) for instruction in uncorrupted_mul_instructions) == 161


def test_find_enabled_uncorrupted_mul_instructions():
    corrupted_memory = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    enabled_uncorrupted_mul_instructions = find_enabled_uncorrupted_mul_instructions(
        corrupted_memory
    )
    assert enabled_uncorrupted_mul_instructions == ["mul(2,4)", "mul(8,5)"]
    assert (
        sum(eval(instruction) for instruction in enabled_uncorrupted_mul_instructions)
        == 48
    )
