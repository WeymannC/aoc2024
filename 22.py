from itertools import islice, pairwise

from aocd import get_data

data = get_data(day=22, year=2024)
example = r"""1
10
100
2024"""


def parse_input(raw):
    for secret in raw.split("\n"):
        yield int(secret)

def next_number(secret):
    secret = ((secret << 6) ^ secret) % 2**24
    secret = ((secret >> 5) ^ secret) % 2**24
    secret = ((secret << 11) ^ secret) % 2**24
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
        yield b-a

def part_2(used_input):
    for price in day_diffs(123):
        print(price)

print(part_1(data))
print(part_2(example))
