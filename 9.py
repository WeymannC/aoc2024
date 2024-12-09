from itertools import repeat

from aocd import get_data

data = get_data(day=9, year=2024)
example = r"""2333133121414131402"""


def get_files(raw):
    return (int(char) for char in raw[0::2])

def get_spaces(raw):
    return (int(char) for char in raw[1::2])

def get_initial_disk_state(files, spaces):
    for i, length in enumerate(files):
        yield from repeat(i, length)
        try:
            yield from repeat(".", next(spaces))
        except StopIteration:
            pass

def build_disk_state_part1(initial_disk_state):
    disk_list = list(initial_disk_state)
    while disk_list:
        left = disk_list.pop(0)
        if left != ".":
            yield left
            continue
        right = "."
        while right == ".":
            right = disk_list.pop(-1)
        yield right

def build_disk_state_part2(initial_disk_state):
    pass

def get_checksum(disk_state):
    return sum(i*file_id for i, file_id in enumerate(disk_state))

def part_1(used_input):
    files = get_files(used_input)
    spaces = get_spaces(used_input)
    return get_checksum(build_disk_state_part1(get_initial_disk_state(files, spaces)))


def part_2(used_input):
    pass


print(part_1(data))
print(part_2(example))
