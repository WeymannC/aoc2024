from functools import cache

from aocd import get_data

data = get_data(day=19, year=2024)
example = r"""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def parse_towels(raw_towels):
    return frozenset(raw_towels.split(", "))


def parse_patterns(raw_patters):
    yield from raw_patters.split("\n")


def parse_input(raw):
    towels, patterns = raw.split("\n\n")

    return parse_towels(towels), parse_patterns(patterns)


@cache
def ways_to_build_pattern_from_towels(pattern, towels):
    total = 0
    for towel in towels:
        if pattern == towel:
            total += 1
        if pattern.startswith(towel):
            total += ways_to_build_pattern_from_towels(pattern.removeprefix(towel), towels)
    return total


def part_1(used_input):
    towels, patterns = parse_input(used_input)
    return sum(1 if ways_to_build_pattern_from_towels(pattern, towels) else 0 for pattern in patterns)


def part_2(used_input):
    towels, patterns = parse_input(used_input)
    return sum(ways_to_build_pattern_from_towels(pattern, towels) for pattern in patterns)


print(part_1(data))
print(part_2(data))
