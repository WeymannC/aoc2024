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

def build_disk_state_part2(initial_disk_state, raw):
    disk_list = list(initial_disk_state)
    file_list = list(enumerate(get_files(raw)))
    for file_name, size in file_list[::-1]:
        file_position = disk_list.index(file_name)
        for i in range(file_position):
            if all(c == "." for c in disk_list[i:i+size]):
                disk_list = [c if c != file_name else "." for c in disk_list]
                disk_list[i:i+size] = [file_name]*size
                break
    return disk_list

def get_checksum(disk_state):
    return sum(i*file_id for i, file_id in enumerate(disk_state) if file_id != ".")

def part_1(used_input):
    files = get_files(used_input)
    spaces = get_spaces(used_input)
    return get_checksum(build_disk_state_part1(get_initial_disk_state(files, spaces)))


def part_2(used_input):
    files = get_files(used_input)
    spaces = get_spaces(used_input)
    return get_checksum(build_disk_state_part2(get_initial_disk_state(files, spaces), used_input))


print(part_1(data))
print(part_2(data))
