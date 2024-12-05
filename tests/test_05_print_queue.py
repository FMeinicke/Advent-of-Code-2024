from __future__ import annotations

from solutions._05_print_queue import (
    find_correctly_ordered_updates,
    find_incorrectly_ordered_updates,
    fix_incorrectly_ordered_updates,
    get_middle_page_numbers,
    make_rule_graph,
    parse_input,
)

input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def test_parse_input() -> None:
    rules, updates = parse_input(input)

    assert rules == (
        (47, 53),
        (97, 13),
        (97, 61),
        (97, 47),
        (75, 29),
        (61, 13),
        (75, 53),
        (29, 13),
        (97, 29),
        (53, 29),
        (61, 53),
        (97, 53),
        (61, 29),
        (47, 13),
        (75, 47),
        (97, 75),
        (47, 61),
        (75, 61),
        (47, 29),
        (75, 13),
        (53, 13),
    )
    assert updates == (
        (75, 47, 61, 53, 29),
        (97, 61, 53, 29, 13),
        (75, 29, 13),
        (75, 97, 47, 61, 53),
        (61, 13, 29),
        (97, 13, 75, 29, 47),
    )


def rule_graph_and_updates() -> tuple:
    rules, updates = parse_input(input)
    return make_rule_graph(rules), updates


def test_find_correctly_ordered_updates() -> None:
    correctly_ordered_updates = find_correctly_ordered_updates(
        *rule_graph_and_updates()
    )
    assert correctly_ordered_updates == (
        (75, 47, 61, 53, 29),
        (97, 61, 53, 29, 13),
        (75, 29, 13),
    )


def test_get_correctly_ordered_middle_page_numbers() -> None:
    updates = find_correctly_ordered_updates(*rule_graph_and_updates())

    assert get_middle_page_numbers(updates) == 143


def test_find_incorrectly_ordered_updates() -> None:
    incorrectly_ordered_updates = find_incorrectly_ordered_updates(
        *rule_graph_and_updates()
    )
    assert incorrectly_ordered_updates == (
        (75, 97, 47, 61, 53),
        (61, 13, 29),
        (97, 13, 75, 29, 47),
    )


def test_fix_incorrectly_ordered_updates_single() -> None:
    graph, updates = rule_graph_and_updates()
    fixed_incorrectly_ordered_updates = fix_incorrectly_ordered_updates(
        graph, ((97, 13, 75, 29, 47),)
    )
    print(f"{fixed_incorrectly_ordered_updates=}")
    assert fixed_incorrectly_ordered_updates == ((97, 75, 47, 29, 13),)


def test_fix_incorrectly_ordered_updates() -> None:
    graph, updates = rule_graph_and_updates()
    fixed_incorrectly_ordered_updates = fix_incorrectly_ordered_updates(
        graph, find_incorrectly_ordered_updates(graph, updates)
    )
    assert fixed_incorrectly_ordered_updates == (
        (97, 75, 47, 61, 53),
        (61, 29, 13),
        (97, 75, 47, 29, 13),
    )


def test_get_incorrectly_ordered_middle_page_numbers() -> None:
    graph, updates = rule_graph_and_updates()
    updates = fix_incorrectly_ordered_updates(
        graph, find_incorrectly_ordered_updates(graph, updates)
    )

    assert get_middle_page_numbers(updates) == 123
