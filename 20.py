import json
from collections import defaultdict

from aocd import get_data

data = get_data(day=20, year=2024)
example = r"""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def parse_map(raw_map):
    starting_position = None
    target_position = None
    walls = set()
    for i, line in enumerate(raw_map.split("\n")):
        for j, char in enumerate(line):
            if char == "#":
                walls.add((i, j))
            elif char == "S":
                starting_position = (i, j)
            elif char == "E":
                target_position = (i, j)

    return starting_position, target_position, walls


def move_to_delta(move):
    return {
        ">": (0, 1),
        "<": (0, -1),
        "v": (1, 0),
        "^": (-1, 0),
    }[move]


def new_position(position, delta):
    i, j = position
    di, dj = delta
    return i + di, j + dj


def build_standard_path(start, target, walls):
    current_position = start
    path = [start]
    while current_position != target:
        path.extend(
            [
                next_position for move in ["^", "v", "<", ">"]
                if (next_position := new_position(current_position, move_to_delta(move))) not in walls and
                   next_position not in path
            ]
        )
        current_position = path[-1]
    return path


def find_cheats(path, max_skip):
    for i, starting_position in enumerate(path):
        for skip, end_position in enumerate(path[i:]):
            si, sj = starting_position
            ei, ej = end_position
            if (distance_during_skip := abs(si - ei) + abs(sj - ej)) <= max_skip:
                yield skip - distance_during_skip, (starting_position, end_position)


def print_all_skips(path, max_skip):
    skips = defaultdict(lambda: 0)
    for skip, _ in find_cheats(path, max_skip):
        skips[skip] += 1
    print(json.dumps(skips, indent=4, sort_keys=True))


def part_1(used_input):
    starting_position, target_position, walls = parse_map(used_input)
    path = build_standard_path(starting_position, target_position, walls)
    # print_all_skips(path, 2)
    return sum(1 if skip >= 100 else 0 for skip, _ in find_cheats(path, 2))


def part_2(used_input):
    starting_position, target_position, walls = parse_map(used_input)
    path = build_standard_path(starting_position, target_position, walls)
    # print_all_skips(path, 20)
    return sum(1 if skip >= 100 else 0 for skip, _ in find_cheats(path, 20))


print(part_1(data))
print(part_2(data))
