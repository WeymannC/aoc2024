from functools import cache
from itertools import pairwise, permutations

from aocd import get_data

data = get_data(day=21, year=2024)
example = r"""029A
980A
179A
456A
379A"""


def number_pad():
    return {
        "A": (0, 0),
        "0": (0, 1),
        "1": (-1, 2),
        "2": (-1, 1),
        "3": (-1, 0),
        "4": (-2, 2),
        "5": (-2, 1),
        "6": (-2, 0),
        "7": (-3, 2),
        "8": (-3, 1),
        "9": (-3, 0),
    }, (0, 2)


def direction_pad():
    return {
        "A": (0, 0),
        "^": (0, 1),
        "v": (1, 1),
        "<": (1, 2),
        ">": (1, 0),
    }, (0, 2)


@cache
def min_distance(start, end, layer, max_layer):
    pad, forbidden = number_pad() if layer == 0 else direction_pad()
    start_i, start_j = pad[start]
    end_i, end_j = pad[end]
    forbidden_i, forbidden_j = forbidden
    i_move = "^" if end_i < start_i else "v"
    j_move = "<" if start_j < end_j else ">"
    combos = [combo for combo in permutations(
        [j_move for _ in range(abs(start_j - end_j))] + [i_move for _ in range(abs(start_i - end_i))])]
    if start_j == forbidden_j and (
            (start_i < forbidden_i <= end_i) or
            (start_i > forbidden_i >= end_i)
    ):
        dist = abs(start_i - forbidden_i)
        combos = [combo for combo in combos if combo[:dist] != tuple(i_move for _ in range(dist))]
    elif start_i == forbidden_i and (
            (start_j < forbidden_j <= end_j) or
            (start_j > forbidden_j >= end_j)
    ):
        dist = abs(start_j - forbidden_j)
        combos = [combo for combo in combos if combo[:dist] != tuple(j_move for _ in range(dist))]
    return min(
        [
            count_sequence("".join(combo) + "A", layer + 1, max_layer)
            for combo in combos
        ]
    )


@cache
def count_sequence(out, layer, max_layer):
    if layer == max_layer:
        return len(out)
    return sum(min_distance(start, end, layer, max_layer) for start, end in pairwise("A" + out))


def part_1(used_input):
    total = 0
    for code in used_input.split("\n"):
        out = count_sequence(code, 0, 3)
        print(code, out)
        total += out * int(code[:-1])
    return total


def part_2(used_input):
    total = 0
    for code in used_input.split("\n"):
        out = count_sequence(code, 0, 26)
        print(code, out)
        total += out * int(code[:-1])
    return total


print(part_1(data))
print(part_2(data))
