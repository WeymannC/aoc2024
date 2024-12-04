from aocd import get_data

data = get_data(day=4, year=2024)
example = r"""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

TARGET_WORD="XMAS"

def get_letter(input, i, j):
    lines = input.split("\n")
    if 0 <= i < len(lines) and 0 <= j < len(lines[0]):
        return lines[i][j]

def read_direction(input, i, j, di, dj):
    for n in range(len(TARGET_WORD)):
        yield get_letter(input, i+n*di, j+n*dj)

def part_1(input):
    total = 0
    lines = input.split("\n")
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    for letter, target in zip(read_direction(input, i, j, di, dj), TARGET_WORD):
                        if letter != target:
                            break
                    else:
                        total += 1

    return total

print(part_1(data))