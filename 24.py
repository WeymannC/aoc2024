import re
from collections import deque
from itertools import permutations

from aocd import get_data

data = get_data(day=24, year=2024)
example = r"""x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
example2 = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""
example3 = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""


def parse_wires(raw_wires):
    wires = {}
    for line in raw_wires.split("\n"):
        wire, value = line.split(": ")
        wires[wire] = int(value)
    return wires


def parse_gates(raw_gates):
    gates = deque()
    for line in raw_gates.split("\n"):
        match = re.match(r"(.{3}) (AND|OR|XOR) (.{3}) -> (.{3})", line)
        gates.append(match.group(1, 3, 2, 4))
    return gates


def parse_input(raw):
    raw_wires, raw_gates = raw.split("\n\n")
    return parse_wires(raw_wires), parse_gates(raw_gates)


def run(wires, gates):
    while gates:
        a, b, op, out = gates.popleft()
        x, y = wires.get(a), wires.get(b)
        if x is None or y is None:
            gates.append((a, b, op, out))
        elif op == "AND":
            wires[out] = x & y
        elif op == "OR":
            wires[out] = x | y
        elif op == "XOR":
            wires[out] = x ^ y
    return wires


def build_output(wires):
    return int("".join(str(wires.get(f"z{i:02}", 0)) for i in range(99, -1, -1)), 2)


def part_1(used_input):
    wires, gates = parse_input(used_input)
    wires = run(wires, gates)
    return build_output(wires)


def swap_gates(a, b, gates_dict):
    gates_dict = gates_dict.copy()
    gates_dict[a], gates_dict[b] = gates_dict[b], gates_dict[a]
    return gates_dict


def find_gate(a, b, op, gates_dict):
    for gate, (c, d, ope) in gates_dict.items():
        if op == ope and {a, b} == {c, d}:
            return gate


def part_2(used_input):
    input_wires, input_gates = parse_input(used_input)
    gates_dict = {out: other for *other, out in input_gates}
    previous_carry = find_gate("x00", "y00", "AND", gates_dict)
    swapped = set()
    for i in range(1, 45):
        x_bit = f"x{i:02}"
        y_bit = f"y{i:02}"
        z_bit = f"z{i:02}"

        total = find_gate(x_bit, y_bit, "XOR", gates_dict)
        assert total is not None
        if (actual_z := find_gate(total, previous_carry, "XOR", gates_dict)) is None:
            for total_replace in gates_dict:
                if find_gate(total_replace, previous_carry, "XOR", gates_dict) is not None:
                    gates_dict = swap_gates(total, total_replace, gates_dict)
                    swapped |= {total_replace, total}
                    total = total_replace
                    break
        elif actual_z != z_bit:
            gates_dict = swap_gates(actual_z, z_bit, gates_dict)
            swapped |= {actual_z, z_bit}

        new_carry_bits = find_gate(x_bit, y_bit, "AND", gates_dict)
        assert new_carry_bits is not None
        new_carry_total = find_gate(total, previous_carry, "AND", gates_dict)
        assert new_carry_total is not None
        new_carry = find_gate(new_carry_bits, new_carry_total, "OR", gates_dict)
        assert new_carry is not None
        previous_carry = new_carry

    return ",".join(sorted(swapped))


print(part_1(data))
print(part_2(data))
