from functools import lru_cache
from math import prod

from aocd import get_data

data = get_data(day=7, year=2024)
example = r"""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def parse_tests(raw):
    return [
        (
            int(line.split(": ")[0]),
            tuple(int(element) for element in line.split(": ")[1].split(" "))
        )
        for line in raw.split("\n")
    ]


@lru_cache
def can_form(target, elements, operators):
    if len(elements) == 2:
        for operator in operators:
            if operator(elements) == target:
                return True
        return False

    return any(
        can_form(target, (operator(elements[:2]), *elements[2:]), operators)
        for operator in operators
    )


def part_1(used_input):
    operators = (sum, prod)

    return sum(target for target, elements in parse_tests(used_input) if can_form(target, elements, operators))


def part_2(used_input):
    def concat(iterable):
        a, b = iterable
        return int(str(a) + str(b))

    operators = (sum, prod, concat)

    return sum(target for target, elements in parse_tests(used_input) if can_form(target, elements, operators))


print(part_1(data))
print(part_2(data))
