from aocd import get_data

data = get_data(day=1, year=2024)
example = r"""3   4
4   3
2   5
1   3
3   9
3   3"""

used_input = data
list_a = []
list_b = []
for line in used_input.split("\n"):
    str_a, str_b = line.split("   ")
    list_a.append(int(str_a))
    list_b.append(int(str_b))

print(sum(a*list_b.count(a) for a in list_a))