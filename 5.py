from collections import defaultdict
from functools import lru_cache, cmp_to_key

from aocd import get_data

data = get_data(day=5, year=2024)
example = r"""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

@lru_cache
def parse_rules(raw_rules):
    rules = defaultdict(list)
    for rule in raw_rules.split("\n"):
        before, after = rule.split("|")
        rules[before].append(after)

    return rules

def parse_updates(raw_updates):
    return [update.split(",") for update in raw_updates.split("\n")]

def parse_input(used_input):
    raw_rules, raw_updates = used_input.split("\n\n")
    updates = parse_updates(raw_updates)

    return raw_rules, updates

@lru_cache
def comes_before(before, after, raw_rules):
    rules = parse_rules(raw_rules)
    children = rules[before]
    return after in children

def is_valid(update, rules):
    for i, page in enumerate(update):
        if any(comes_before(later_page, page, rules) for later_page in update[i:]):
            return False
    return True

def middle_element(update):
    return update[len(update)//2]

def part_1(used_input):
    rules, updates = parse_input(used_input)

    total = sum(int(middle_element(update)) for update in updates if is_valid(update, rules))

    return total

def part_2(used_input):
    rules, updates = parse_input(used_input)

    def comp(before, after):
        return 1 if comes_before(before, after, rules) else -1

    total = sum(int(middle_element(sorted(update, key=cmp_to_key(comp)))) for update in updates if not is_valid(update, rules))

    return total

print(part_1(data))
print(part_2(data))