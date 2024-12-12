from collections import deque
from functools import lru_cache

from aocd import get_data

data = get_data(day=12, year=2024)
example = r"""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


def get_grid_size(raw):
    lines = raw.split("\n")
    return len(lines), len(lines[0])

@lru_cache
def get_plant(raw, i, j):
    max_i, max_j = get_grid_size(raw)
    if 0 <= i < max_i and 0 <= j < max_j:
        return raw.split("\n")[i][j]

def get_neighbor(raw, i, j):
    return (
        (i + di, j + dj) for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)] if
        get_plant(raw, i + di, j + dj) is not None
    )

def is_same_plant(raw, reference, current):
    return get_plant(raw, *reference) == get_plant(raw, *current)

def build_regions(raw):
    max_i, max_j = get_grid_size(raw)
    known_regions = [[None for _ in range(max_j)] for _ in range(max_i)]
    region_index = 0

    for i in range(max_i):
        for j in range(max_j):
            if known_regions[i][j] is None:
                positions = deque()
                reference = (i, j)
                positions.append(reference)
                while positions:
                    ci, cj = positions.pop()
                    if is_same_plant(raw, reference, (ci, cj)) and known_regions[ci][cj] is None:
                        known_regions[ci][cj] = region_index
                        positions.extend(get_neighbor(raw, ci, cj))
                region_index += 1

    return known_regions


def part_1(used_input):
    return "\n".join("".join(f"{index:2}" for index in line) for line in build_regions(used_input))

def part_2(used_input):
    pass


print(part_1(example))
print(part_2(example))
