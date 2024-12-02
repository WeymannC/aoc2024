from itertools import pairwise

from aocd import get_data

data = get_data(day=2, year=2024)
example = r"""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

used_input = data
reports = used_input.split("\n")

safe = 0
for report in reports:
    levels = [int(l) for l in report.split(" ")]
    level_d = [level - next_level for level, next_level in pairwise(levels)]
    if all(d in [1,2,3] for d in level_d) or all(d in [-1,-2,-3] for d in level_d):
        safe += 1

print(safe)