from collections import defaultdict

from aocd import get_data

data = get_data(day=6, year=2024)
example = r"""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def parse_map(raw_map):
    obstacles = set()
    lines = raw_map.split("\n")
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "#":
                obstacles.add((i, j))
            elif char in ["^", "v", "<", ">"]:
                starting_position = (i, j)
                starting_direction = char

    return len(lines), len(lines[0]), obstacles, starting_position, starting_direction


def next_step(direction):
    direction_to_step = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }

    return direction_to_step[direction]


def next_move(position, direction, obstacles):
    i, j = position
    di, dj = next_step(direction)

    turn_right = {
        "^": ">",
        ">": "v",
        "v": "<",
        "<": "^",
    }

    if (i + di, j + dj) in obstacles:
        return position, turn_right[direction]
    return (i + di, j + dj), direction


def compute_positions(used_input):
    max_i, max_j, obstacles, starting_position, starting_direction = parse_map(used_input)

    positions = {starting_position}
    position = starting_position
    direction = starting_direction

    while (True):
        position, direction = next_move(position, direction, obstacles)
        i, j = position
        if 0 <= i < max_i and 0 <= j < max_j:
            positions.add(position)
        else:
            break

    return positions


def part_1(used_inputs):
    positions = compute_positions(used_inputs)
    return len(positions)


def part_2(used_input):
    max_i, max_j, obstacles, starting_position, starting_direction = parse_map(used_input)
    base_positions = compute_positions(used_input)

    cycles = 0
    for position in base_positions:
        new_obstacles = obstacles | {position}
        new_positions = defaultdict(list)
        new_positions[starting_position].append(starting_direction)

        positions = {starting_position}
        position = starting_position
        direction = starting_direction

        while (True):
            position, direction = next_move(position, direction, new_obstacles)
            i, j = position
            if direction in new_positions[position]:
                cycles += 1
                break
            if 0 <= i < max_i and 0 <= j < max_j:
                positions.add(position)
                new_positions[position].append(direction)
            else:
                break

    return cycles


print(part_1(data))
print(part_2(data))
