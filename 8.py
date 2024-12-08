from collections import defaultdict
from itertools import combinations

from aocd import get_data

data = get_data(day=8, year=2024)
example = r"""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def parse_map(raw):
    lines = raw.split("\n")
    antennas = defaultdict(list)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != ".":
                antennas[char].append((i, j))

    return antennas, len(lines), len(lines[0])


def compute_antinodes_part1(antenna_a, antenna_b, n_max):
    ia, ja = antenna_a
    ib, jb = antenna_b
    return (2 * ib - ia, 2 * jb - ja), (2 * ia - ib, 2 * ja - jb)


def compute_antinodes_part2(antenna_a, antenna_b, n_max):
    ia, ja = antenna_a
    ib, jb = antenna_b
    for n in range(-n_max, n_max):
        yield ia - n * (ib - ia), ja - n * (jb - ja)


def is_inbound(node, max_i, max_j):
    i, j = node
    return 0 <= i < max_i and 0 <= j < max_j


def get_affected_positions(antennas, max_i, max_j, compute_antinodes):
    positions = set()
    for antennas_of_type in antennas.values():
        for antenna_a, antenna_b in combinations(antennas_of_type, 2):
            nodes = compute_antinodes(antenna_a, antenna_b, max(max_i, max_j))
            for node in nodes:
                if is_inbound(node, max_i, max_j):
                    positions.add(node)

    return positions


def part_1(used_input):
    return len(get_affected_positions(*parse_map(used_input), compute_antinodes_part1))


def part_2(used_input):
    return len(get_affected_positions(*parse_map(used_input), compute_antinodes_part2))


print(part_1(data))
print(part_2(data))
