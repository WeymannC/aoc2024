from collections import deque, defaultdict
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

def get_neighbor(i, j):
    return (
        (i + di, j + dj) for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]
    )

def is_same_plant(raw, reference, current):
    return get_plant(raw, *reference) == get_plant(raw, *current)

def build_regions(raw):
    max_i, max_j = get_grid_size(raw)
    known_regions = [[None for _ in range(max_j)] for _ in range(max_i)]
    region_index = 0
    surfaces = defaultdict(lambda: 0)
    edges = defaultdict(lambda: 0)

    for i in range(max_i):
        for j in range(max_j):
            if known_regions[i][j] is None:
                positions = deque()
                reference = (i, j)
                positions.append(reference)
                while positions:
                    ci, cj = positions.pop()
                    if is_same_plant(raw, reference, (ci, cj)):
                        if known_regions[ci][cj] is None:
                            known_regions[ci][cj] = region_index
                            surfaces[region_index] += 1
                            positions.extend(get_neighbor(ci, cj))
                    else:
                        edges[region_index] += 1
                region_index += 1

    return known_regions, surfaces, edges

def get_region(regions, i, j):
    max_i = len(regions)
    max_j = len(regions[0])
    if 0 <= i < max_i and 0 <= j < max_j:
        return regions[i][j]

def get_corners(i, j):
    return ([(i+si*di, j+sj*dj) for di, dj in [(1,1),(0,1),(1,0)]] for si,sj in [(1,1),(1,-1),(-1,1),(-1,-1)])

def count_sides(regions):
    max_i = len(regions)
    max_j = len(regions[0])

    sides = defaultdict(lambda: 0)
    for i in range(max_i):
        for j in range(max_j):
            current = get_region(regions, i, j)
            for corner, side1, side2 in get_corners(i,j):
                if (
                        (get_region(regions, *side1) != current and get_region(regions, *side2) != current) or
                        (
                                get_region(regions, *side1) == get_region(regions, *side2) == current and
                                get_region(regions, *corner) != current
                        )
                ):
                    sides[current] += 1
    return sides

def part_1(used_input):
    known_regions, surfaces, edges =  build_regions(used_input)
    return sum(surfaces[k]*v for k, v in edges.items())

def part_2(used_input):
    known_regions, surfaces, edges = build_regions(used_input)
    sides = count_sides(known_regions)
    return sum(surfaces[k] * v for k, v in sides.items())


print(part_1(data))
print(part_2(data))
