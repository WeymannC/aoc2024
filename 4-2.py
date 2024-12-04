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


def get_letter(input, i, j):
    lines = input.split("\n")
    if 0 <= i < len(lines) and 0 <= j < len(lines[0]):
        return lines[i][j]


def is_x_mas(input, i, j):
    return (
            get_letter(input, i, j) == "A" and
            (
                    (get_letter(input, i + 1, j + 1) == "M" and get_letter(input, i - 1, j - 1) == "S") or
                    (get_letter(input, i + 1, j + 1) == "S" and get_letter(input, i - 1, j - 1) == "M")
            ) and
            (
                    (get_letter(input, i - 1, j + 1) == "M" and get_letter(input, i + 1, j - 1) == "S") or
                    (get_letter(input, i - 1, j + 1) == "S" and get_letter(input, i + 1, j - 1) == "M")
            )
    )


def part_2(input):
    lines = input.split("\n")
    return sum(1 for i in range(len(lines)) for j in range(len(lines[0])) if is_x_mas(input, i, j))


print(part_2(data))
