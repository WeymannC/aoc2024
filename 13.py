import math
import re
from collections import deque

from aocd import get_data

data = get_data(day=13, year=2024)
example = r"""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


def find_numbers(raw):
    return tuple(int(number) for number in re.findall(r"\d+", raw))

def parse_input(raw):
    for machine in raw.split("\n\n"):
        raw_A, raw_B, raw_P = machine.split("\n")
        yield find_numbers(raw_A), find_numbers(raw_B), find_numbers(raw_P)

def solve_machine_wrong(a, b, p):
    cost_a = 3
    cost_b = 1
    max_press = 100

    target = p
    current_min = math.inf
    queue = deque([(a, 0, 0, (0, 0)), (b, 0, 0, (0, 0))])
    while queue:
        next_press, current_a, current_b, current_pos = queue.pop()
        print(next_press, current_a, current_b, current_pos)
        a_press = current_a + 1 if next_press==a else current_a
        b_press = current_b + 1 if next_press==b else current_b
        if a_press > max_press or b_press > max_press:
            continue
        if cost_a * a_press + cost_b * b_press > current_min:
            continue
        cx, cy = current_pos
        dx, dy = next_press
        nx, ny = cx+dy, cy+dy
        tx, ty = target
        if nx > tx or ny > ty:
            continue
        if nx == tx and ny ==ty:
            current_min = cost_a * a_press + cost_b * b_press
            continue
        queue.extend((button, a_press, b_press, (nx, ny)) for button in [a,b])
    return current_min

def solve_machine(a,b,p):
    (xa, ya), (xb, yb), (x, y) = a,b,p
    if yb*xa == xb*ya:
        return math.inf
    nb = (xa*y - ya*x)/(yb*xa - xb*ya)
    if not nb.is_integer():
        return math.inf
    na = (x - nb*xb)/xa
    if not na.is_integer():
        return math.inf
    return 3*na + nb

def part_1(used_input):
    machines = parse_input(used_input)
    return sum(cost for a, b, p in machines if (cost:=solve_machine(a,b,p)) < math.inf)

def part_2(used_input):
    machines = parse_input(used_input)
    return sum(cost for a, b, (x,y) in machines if (cost:=solve_machine(a,b,(x + 10000000000000, y + 10000000000000))) < math.inf)


print(part_1(data))
print(part_2(data))
