from __future__ import annotations

from importlib.resources import files
from typing import TypeAlias

from . import print_day


def get_input():
    with (files("solutions.inputs") / "05.txt").open() as file:
        return file.read()


Rule: TypeAlias = tuple[int, int]
Rules: TypeAlias = tuple[Rule]
Update: TypeAlias = tuple[int]
Updates: TypeAlias = tuple[Update]


def parse_input(input: str) -> tuple[Rules, Updates]:
    rules, updates = input.strip().split("\n\n")
    return (
        tuple(map(lambda rule: tuple(map(int, rule.split("|"))), rules.split("\n"))),
        tuple(tuple(map(int, update.split(","))) for update in updates.split("\n")),
    )


class Node:
    __value: int
    __predecessors: set[Node]
    __successors: set[Node]

    def __init__(self, value: int):
        self.__value = value
        self.__predecessors = set()
        self.__successors = set()

    def add_predecessors(self, *predecessors: Node) -> None:
        for predecessor in predecessors:
            if predecessor not in self.__predecessors:
                self.__predecessors.add(predecessor)
                predecessor.add_successors(self)

    def add_successors(self, *successors: Node) -> None:
        for successor in successors:
            if successor not in self.__successors:
                self.__successors.add(successor)
                successor.add_predecessors(self)

    @property
    def value(self) -> int:
        return self.__value

    @property
    def predecessors(self) -> set[int]:
        return {predecessor.value for predecessor in self.__predecessors}

    @property
    def successors(self) -> set[int]:
        return {successor.value for successor in self.__successors}


class DirectedGraph:
    __nodes: list[Node]

    def __init__(self):
        self.__nodes = []

    def __add_node(self, node_value: int) -> Node:
        try:
            return next(node for node in self.__nodes if node.value == node_value)
        except StopIteration:
            node = Node(node_value)
            self.__nodes.append(node)
            return node

    def add_node(self, node_value: int, *predecessor_values: int) -> None:
        node = self.__add_node(node_value)
        predecessors = map(self.__add_node, predecessor_values)
        node.add_predecessors(*predecessors)

    def predecessors(self, node_value: int) -> set[int]:
        return next(
            node.predecessors for node in self.__nodes if node.value == node_value
        )

    def successors(self, node_value: int) -> set[int]:
        return next(
            node.successors for node in self.__nodes if node.value == node_value
        )

    def __iter__(self):
        return iter(node.value for node in self.__nodes)


def make_rule_graph(rules: Rules) -> DirectedGraph:
    graph = DirectedGraph()
    for rule in rules:
        # print(f"Processing rule: {rule}")
        graph.add_node(rule[1], rule[0])
        # print(f"{rule[1]}'s predecessors: {graph.predecessors(rule[1])}")
        # print(f"{rule[1]}'s successors: {graph.successors(rule[1])}")
    # for node in graph:
    #     print(f"{node}'s predecessors: {graph.predecessors(node)}")
    #     print(f"{node}'s successors: {graph.successors(node)}")
    return graph


def classify_updates(
    rule_graph: DirectedGraph, updates: Updates
) -> tuple[Updates, Updates]:
    correctly_ordered_updates: list[Update] = []
    incorrectly_ordered_updates: list[Update] = []
    for update in updates:
        for i, page in enumerate(update):
            if any(
                successor in rule_graph.predecessors(page) for successor in update[i:]
            ):
                incorrectly_ordered_updates.append(update)
                # print(f"Incorrectly ordered update: {update}")
                break
        else:
            correctly_ordered_updates.append(update)
            # print(f"Correctly ordered update: {update}")

    return tuple(correctly_ordered_updates), tuple(incorrectly_ordered_updates)


def find_correctly_ordered_updates(
    rule_graph: DirectedGraph, updates: Updates
) -> Updates:
    return classify_updates(rule_graph, updates)[0]


def get_middle_page_numbers(updates: Updates) -> int:
    return sum(update[len(update) // 2] for update in updates)


def find_incorrectly_ordered_updates(
    rule_graph: DirectedGraph, updates: Updates
) -> Updates:
    return classify_updates(rule_graph, updates)[1]


def fix_incorrectly_ordered_updates(
    rule_graph: DirectedGraph, updates: Updates
) -> Updates:

    # for every update in updates
    # for every page in update
    # for every successor of page
    # if successor is in update[i:]
    # for every successor of the successor of the ... that is in update[i:]
    # if there is no more successor
    # put page in the newly ordered list

    fixed_updates = []

    def append_predecessors(page: int, update: Update) -> None:
        predecessors = rule_graph.predecessors(page)

        if page in fixed_update:
            return

        if len(predecessors) == 0:
            fixed_update.append(page)
            return

        for predecessor in predecessors:
            if predecessor in update:
                append_predecessors(predecessor, update)
        fixed_update.append(page)

    for update in updates:
        fixed_update = []
        for i, page in enumerate(update):
            append_predecessors(page, update[i:])
        fixed_updates.append(tuple(fixed_update))

    return tuple(fixed_updates)


def main():
    print_day(5, "Print Queue")

    # Part One: Find correctly ordered updates and calculate the sum of the middle page numbers

    rules, updates = parse_input(get_input())
    rule_graph = make_rule_graph(rules)
    sum_middle_page_numbers_correct = get_middle_page_numbers(
        find_correctly_ordered_updates(rule_graph, updates)
    )
    print(
        f"Sum of middle page numbers of correctly ordered updates: {sum_middle_page_numbers_correct}"
    )

    # Part Two: Find and fix the incorrectly ordered updates and calculate the sum of the middle page numbers

    sum_middle_page_numbers_fixed = get_middle_page_numbers(
        fix_incorrectly_ordered_updates(
            rule_graph, find_incorrectly_ordered_updates(rule_graph, updates)
        )
    )
    print(
        f"Sum of middle page numbers of fixed incorrectly ordered updates: {sum_middle_page_numbers_fixed}"
    )


if __name__ == "__main__":
    main()
