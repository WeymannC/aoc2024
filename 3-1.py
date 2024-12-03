import re

from aocd import get_data

data = get_data(day=3, year=2024)
example = r"""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

MUL_INSTRUCTION_REGEX = r"mul\(\d{1,3},\d{1,3}\)"

def extract_mul_instructions(input):
    return re.findall(MUL_INSTRUCTION_REGEX, input)

def evaluate_mul_instruction(instruction):
    a, b = instruction.lstrip("mul(").rstrip(")").split(",")
    return int(a) * int(b)

def part_1(input):
    return sum(evaluate_mul_instruction(instruction) for instruction in extract_mul_instructions(input))

print(part_1(data))