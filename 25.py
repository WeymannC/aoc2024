from aocd import get_data

data = get_data(day=25, year=2024)
example = r"""#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


def parse_lock(raw_lock):
    return tuple(
        max(
            i
            for i, line in enumerate(raw_lock.split("\n"))
            if line[col] == "#"
        )
        for col in range(5)
    )


def parse_key(raw_key):
    return tuple(
        max(
            6 - i
            for i, line in enumerate(raw_key.split("\n"))
            if line[col] == "#"
        )
        for col in range(5)
    )


def parse_input(raw):
    locks = set()
    keys = set()
    for schematic in raw.split("\n\n"):
        if schematic[0] == "#":
            locks.add(parse_lock(schematic))
        elif schematic[0] == ".":
            keys.add(parse_key(schematic))
    return locks, keys


def part_1(used_input):
    locks, keys = parse_input(used_input)
    total = 0
    for lock in locks:
        for key in keys:
            if all(l + k <= 5 for l, k in zip(lock, key)):
                total += 1
    return total


print(part_1(data))
