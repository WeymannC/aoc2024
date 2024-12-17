import re

from aocd import get_data

data = get_data(day=17, year=2024)
example = r"""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
example_2 = r"""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

def get_combo(operand, A, B ,C):
    if operand <= 3:
        return operand
    if operand == 4:
        return A
    if operand == 5:
        return B
    if operand == 6:
        return C
    raise Exception("Invalid combo operand")

def adv(operand, A, B, C, instr):
    operand = get_combo(operand, A, B, C)

    result = A // pow(2, operand)

    return result, B, C, instr+2, None

def bxl(operand, A, B ,C, instr):
    result = operand ^ B

    return A, result, C, instr+2, None

def bst(operand, A, B, C, instr):
    operand = get_combo(operand, A, B, C)

    result = operand % 8

    return A, result, C, instr+2, None

def jnz(operand, A, B, C, instr):
    result = (instr+2) if A == 0 else operand

    return A, B, C, result, None

def bxc(operand, A, B ,C, instr):
    result = C ^ B

    return A, result, C, instr+2, None

def out(operand, A, B, C, instr):
    operand = get_combo(operand, A, B, C)

    result = operand % 8

    return A, B, C, instr+2, result

def bdv(operand, A, B, C, instr):
    operand = get_combo(operand, A, B, C)

    result = A // pow(2, operand)

    return A, result, C, instr+2, None

def cdv(operand, A, B, C, instr):
    operand = get_combo(operand, A, B, C)

    result = A // pow(2, operand)

    return A, B, result, instr+2, None

def get_operation(op_code):
    return {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }[op_code]

def parse_registers(raw_registers):
    return (int(re.match(r"Register [ABC]: (\d+)", line).group(1)) for line in raw_registers.split("\n"))

def parse_program(raw_program):
    return [int(code) for code in raw_program.lstrip("Program: ").split(",")]

def parse_input(raw):
    registers, program = raw.split("\n\n")
    A, B, C = parse_registers(registers)
    program = parse_program(program)

    return A, B, C, program

def part_1(used_input):
    A, B, C, program = parse_input(used_input)
    instr = 0
    full_output = []
    while instr < len(program):
        code, operand = program[instr:instr+2]

        A, B, C, instr, output = get_operation(code)(operand, A, B, C, instr)
        if output is not None:
            full_output.append(output)

    return ",".join(str(o) for o in full_output)


def part_2(used_input):
    _, B, C, program = parse_input(used_input)

    full_output = []
    start_A = -1
    while full_output != program:
        instr = 0
        start_A += 1
        A = start_A
        intermediate_output = []
        while instr < len(program):
            code, operand = program[instr:instr+2]

            A, B, C, instr, output = get_operation(code)(operand, A, B, C, instr)
            if output is not None:
                intermediate_output.append(output)

        full_output = intermediate_output.copy()

    return start_A

print(part_1(data))
print(part_2(example_2))
