import math
from collections import deque
from itertools import islice

from aocd import get_data

data = get_data(day=18, year=2024)
data_size = 71
data_steps = 1024
example = r"""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
example_size = 7
example_steps = 12


def parse_corrupted(raw):
    for line in raw.split("\n"):
        i, j = line.split(",")
        yield int(i), int(j)

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


def get_lowest_paths(starting_position, target, obstacles, size):
    cost_step = 1

    current_min = math.inf
    visited = set()

    queue = deque([(starting_position, 0)])
    # counter = 0
    while queue:
        position, current_cost = queue.popleft()
        # print(counter, position, current_cost)
        # counter +=1
        if position in visited:
            continue
        if position == target:
            current_min = current_cost
            break
        visited.add(position)


        queue.extend(
            [
                (next_position, current_cost + cost_step)
                for move in ["^", "v", "<", ">"]
                if (next_position:=new_position(position, move_to_delta(move))) not in obstacles and
                   all(0 <= component < size for component in next_position) and
                   next_position not in visited
            ]
        )

    return current_min

def draw_maze(size, obstacles):
    print("\n".join("".join("#" if (i,j) in obstacles else "." for i in range(size)) for j in range(size)))

def part_1(used_input, used_size, used_steps):
    obstacles_generator = parse_corrupted(used_input)
    obstacles = set(islice(obstacles_generator, used_steps))
    draw_maze(used_size, obstacles)

    return get_lowest_paths((0,0), (used_size-1, used_size-1), obstacles, used_size)


def part_2(used_input, used_size, start_steps):
    obstacles_generator = parse_corrupted(used_input)
    obstacles = set(islice(obstacles_generator, start_steps))
    while True:
        new_obstacle = next(obstacles_generator)
        obstacles.add(new_obstacle)
        if get_lowest_paths((0,0), (used_size-1, used_size-1), obstacles, used_size) == math.inf:
            break
    return new_obstacle



print(part_1(data, data_size, data_steps))
print(part_2(data, data_size, data_steps))
