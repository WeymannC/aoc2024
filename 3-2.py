import re

from aocd import get_data

data = get_data(day=3, year=2024)
example = r"""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

INSTRUCTION_REGEX = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"

def extract_instructions(input):
    return re.findall(INSTRUCTION_REGEX, input)

def evaluate_mul_instruction(instruction):
    a, b = instruction.lstrip("mul(").rstrip(")").split(",")
    return int(a) * int(b)

def part_2(input):
    instructions = extract_instructions(input)

    total = 0
    enabled = True
    for instruction in instructions:
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        elif enabled:
            total += evaluate_mul_instruction(instruction)

    return total

print(part_2(data))
