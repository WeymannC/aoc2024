from functools import lru_cache

from aocd import get_data

data = get_data(day=11, year=2024)
example = r"""125 17"""


def evolve_stone(stone):
    if stone == 0:
        return [1]
    if (n := len(str(stone))) % 2 == 0:
        return [int(str(stone)[:n//2]), int(str(stone)[n//2:])]
    return [stone*2024]

@lru_cache(maxsize=None)
def count_stone_evolutions(stone, steps):
    if steps == 0:
        return 1
    return sum(count_stone_evolutions(evolved_stone, steps-1) for evolved_stone in evolve_stone(stone))

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
    all_stones = parse_input(used_input)
    return sum(count_stone_evolutions(stone, 75) for stone in all_stones)


print(part_1(data))
print(part_2(data))
