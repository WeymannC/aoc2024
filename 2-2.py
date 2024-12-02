from itertools import pairwise

from aocd import get_data

data = get_data(day=2, year=2024)
example = r"""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
9 5 4 3
5 9 4 3"""

used_input = data
reports = used_input.split("\n")

def is_safe(report):
    levels = [int(l) for l in report.split(" ")]
    level_d = [level - next_level for level, next_level in pairwise(levels)]
    return all(d in [1,2,3] for d in level_d) or all(d in [-1,-2,-3] for d in level_d)

def is_safe_with_one_left_out(report):
    if is_safe(report):
        return True
    levels = [int(l) for l in report.split(" ")]
    for i in range(len(levels)):
        if is_safe(" ".join(str(level) for j, level in enumerate(levels) if j != i)):
            return True
    return False

safe = sum(1 for report in reports if is_safe_with_one_left_out(report))
print(f"{safe=}")