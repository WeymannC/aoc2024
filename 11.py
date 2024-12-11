from functools import lru_cache

from aocd import get_data

data = get_data(day=11, year=2024)
example = r"""125 17"""


@lru_cache
def evolve_stone(stone):
    if stone == 0:
        return [1]
    if (n := len(str(stone))) % 2 == 0:
        return [int(str(stone)[:n//2]), int(str(stone)[n//2:])]
    return [stone*2024]

def take_step(stones):
    return (evolved_stone for stone in stones for evolved_stone in evolve_stone(stone))

def parse_input(raw):
    return (int(stone) for stone in raw.split(" "))

def part_1(used_input):
    stones = parse_input(used_input)
    for _ in range(25):
        stones = take_step(stones)

    return len(list(stones))

def part_2(used_input):
    stones = parse_input(used_input)
    for _ in range(75):
        stones = take_step(stones)

    return len(list(stones))


print(part_1(data))
print(part_2(example))
