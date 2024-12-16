import math
from collections import deque, defaultdict
from functools import reduce

from aocd import get_data

data = get_data(day=16, year=2024)
example = r"""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

second_example = r"""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


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


def direction_to_delta(direction):
    return {
        ">": (0, 1),
        "<": (0, -1),
        "v": (1, 0),
        "^": (-1, 0),
    }[direction]

def next_directions(direction):
    return {
        ">": ["^","v"],
        "<": ["^","v"],
        "v": ["<",">"],
        "^": ["<",">"],
    }[direction]

def new_position(position, delta):
    i, j = position
    di, dj = delta
    return i + di, j + dj


def get_lowest_paths(starting_position, target, walls):
    cost_step = 1
    cost_turn = 1000
    starting_direction = ">"

    current_min = math.inf
    visited = {}
    paths = defaultdict(set)

    queue = deque([(starting_position, starting_direction, 0, (starting_position,))])
    while queue:
        position, direction, current_cost, path = queue.popleft()
        # print(position, direction, current_cost)
        if position in walls:
            continue
        if current_cost > current_min:
            continue
        if current_cost > visited.get((position, direction), math.inf):
            continue
        path = (*path, position)
        if position == target:
            current_min = current_cost
            paths[current_cost].add(path)
            continue
        visited[(position, direction)] = current_cost


        queue.extend(
            [(new_position(position, direction_to_delta(direction)), direction, current_cost + cost_step, path)] +
            [(position, new_direction, current_cost + cost_turn, path) for new_direction in next_directions(direction)]
        )

    return current_min, len(reduce(lambda a, b: set(a).union(set(b)), paths[current_min]))

def part_1(used_input):
    start, target, walls = parse_map(used_input)
    return get_lowest_paths(start, target, walls)[0]


def part_2(used_input):
    start, target, walls = parse_map(used_input)
    return get_lowest_paths(start, target, walls)[1]


print(part_1(data))
print(part_2(data))
