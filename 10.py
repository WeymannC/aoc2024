from functools import lru_cache

from aocd import get_data

data = get_data(day=10, year=2024)
example = r"""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


@lru_cache
def get_height(raw, i, j):
    lines = raw.split("\n")
    if 0 <= i < len(lines) and 0 <= j < len(lines[0]):
        return int(lines[i][j])

def get_next_steps(raw, i, j):
    return (
        (i + di, j + dj) for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)] if
        get_height(raw, i + di, j + dj) is not None
    )

def get_trail_heads(raw):
    lines = raw.split("\n")
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "0":
                yield i, j

@lru_cache
def get_trails_from_position(raw, i, j):
    current_height = get_height(raw, i, j)
    if current_height == 9:
        return {(i, j)}, 1

    reachable_summits = set()
    total = 0
    for position in get_next_steps(raw, i, j):
        if get_height(raw, *position) == current_height + 1:
            trails = get_trails_from_position(raw, *position)
            reachable_summits |= trails[0]
            total += trails[1]
    return reachable_summits, total


def part_1(used_input):
    return sum(len(get_trails_from_position(used_input, i, j)[0]) for i, j in get_trail_heads(used_input))


def part_2(used_input):
    return sum((get_trails_from_position(used_input, i, j)[1]) for i, j in get_trail_heads(used_input))



print(part_1(data))
print(part_2(data))
