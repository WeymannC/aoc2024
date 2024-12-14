import time

from aocd import get_data

data = get_data(day=14, year=2024)
data_size = (101, 103)
example = r"""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
example_size = (11, 7)


def parse_robots(raw):
    for line in raw.split("\n"):
        p_raw, v_raw = line.split(" ")
        p = eval(p_raw[2:])
        v = eval(v_raw[2:])
        yield p, v


def assign_quadrant(position, size):
    size_x, size_y = size
    mid_x, mid_y = size_x // 2, size_y // 2
    x, y = position
    if x < mid_x:
        if y < mid_y:
            return 0
        if y > mid_y:
            return 1
    if x > mid_x:
        if y < mid_y:
            return 2
        if y > mid_y:
            return 3


def get_position(p, v, steps, size):
    px, py = p
    vx, vy = v
    size_x, size_y = size

    return (px + vx * steps) % size_x, (py + vy * steps) % size_y

def render_positions(positions, size):
    size_x, size_y = size
    lines = [[" " for _ in range(size_x)] for _ in range(size_y)]
    for x, y in positions:
        lines[y][x] = "."
    print("\n".join("".join(line) for line in lines))

def part_1(used_input, size):
    steps = 100
    quadrants = {0: 0, 1: 0, 2: 0, 3: 0}
    for p, v in parse_robots(used_input):
        pf = get_position(p, v, steps, size)
        print(pf)
        if (q := assign_quadrant(pf, size)) is not None:
            quadrants[q] += 1

    print(quadrants)
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def part_2(used_input, size):
    i = 0
    while True:
        print(i)
        render_positions((get_position(p,v,i,size) for p, v in parse_robots(used_input)), size)
        input()
        i+=1


print(part_1(data, data_size))
print(part_2(data, data_size))
