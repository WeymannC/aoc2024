from collections import deque
from functools import cache
from itertools import islice, pairwise

from aocd import get_data

data = get_data(day=22, year=2024)
example = r"""1
10
100
2024"""
example2 = r"""1
2
3
2024"""


def parse_input(raw):
    for secret in raw.split("\n"):
        yield int(secret)


def next_number(secret):
    secret = ((secret << 6) ^ secret) % 2 ** 24
    secret = ((secret >> 5) ^ secret) % 2 ** 24
    secret = ((secret << 11) ^ secret) % 2 ** 24
    return secret


def day_numbers(secret):
    yield secret
    for _ in range(2000):
        secret = next_number(secret)
        yield secret


def n_number(secret, n):
    return next(islice(day_numbers(secret), n, None))


def part_1(used_input):
    return sum(n_number(secret, 2000) for secret in parse_input(used_input))


def day_prices(secret):
    for number in day_numbers(secret):
        yield number % 10


def day_diffs(secret):
    for a, b in pairwise(day_prices(secret)):
        yield b - a


def last_4_diffs(secret):
    diffs = day_diffs(secret)
    window = deque(islice(diffs, 3), maxlen=4)
    for diff in diffs:
        window.append(diff)
        yield tuple(window)


@cache
def diffs_to_price(secret):
    result = {}
    for diffs, price in zip(last_4_diffs(secret), islice(day_prices(secret), 4, None)):
        if diffs not in result:
            result[diffs] = price
    return result


def part_2(used_input):
    return max(
        sum(
            diffs_to_price(secret).get((i, j, k, l), 0)
            for secret in parse_input(used_input)
        )
        for i in range(-9, 10)
        for j in range(-9, 10)
        for k in range(-9, 10)
        for l in range(-9, 10)
    )


print(part_1(data))
print(part_2(data))
