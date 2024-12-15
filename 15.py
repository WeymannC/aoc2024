from aocd import get_data

data = get_data(day=15, year=2024)
example = r"""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

small_example = r"""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

small_example_2 = r"""#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

def biggify(char):
    if char == "O":
        return "[]"
    if char == "@":
        return "@."
    return 2*char

def biggify_map(raw_map):
    return "\n".join("".join(biggify(char) for char in line) for line in raw_map.split("\n"))

def parse_map(raw_map):
    warehouse = {"walls": set(), "boxes": set(), "big_boxes": set()}
    starting_position = None
    for i, line in enumerate(raw_map.split("\n")):
        for j, char in enumerate(line):
            if char == "#":
                warehouse["walls"].add((i, j))
            elif char == "O":
                warehouse["boxes"].add((i, j))
            elif char == "[":
                warehouse["big_boxes"].add((i,j))
            elif char == "@":
                starting_position = (i, j)
    return starting_position, warehouse


def parse_moves(raw_moves):
    yield from "".join(raw_moves.split("\n"))


def parse_input(raw, biggify=False):
    raw_map, raw_moves = raw.split("\n\n")
    if biggify:
        raw_map = biggify_map(raw_map)

    return parse_map(raw_map), parse_moves(raw_moves)


def move_to_delta(move):
    return {
        ">": (0, 1),
        "<": (0, -1),
        "v": (1, 0),
        "^": (-1, 0),
    }[move]


def new_position(position, delta):
    i, j = position
    di, dj = delta
    return i + di, j + dj


def push(position, move, warehouse):
    target = new_position(position, move_to_delta(move))
    if target in warehouse["walls"]:
        return None
    if target in warehouse["boxes"]:
        if (box_target := push(target, move, warehouse)) is not None:
            warehouse["boxes"].remove(target)
            warehouse["boxes"].add(box_target)
        else:
            return None
    return target


def push2(position, move, warehouse, deletes, inserts):
    target = new_position(position, move_to_delta(move))
    if target in warehouse["walls"]:
        return None, set(), set()
    big_box_position = (
        target
        if target in warehouse["big_boxes"]
        else
        one_left
        if (one_left := new_position(target, (0, -1))) in warehouse["big_boxes"]
        else None
    )
    if big_box_position is not None:
        big_box_target, right_target = None, None
        if move != ">":
            big_box_target, bb_deletes, bb_inserts = push2(big_box_position, move, warehouse, deletes, inserts)
            if big_box_target is None:
                return None, set(), set()
            deletes |= bb_deletes
            inserts |= bb_inserts
        if move != "<":
            right_part = new_position(big_box_position, (0, 1))
            right_target, r_deletes, r_inserts = push2(right_part, move, warehouse, deletes, inserts)
            if right_target is None:
                return None, set(), set()
            deletes |= r_deletes
            inserts |= r_inserts
        deletes.add(big_box_position)
        inserts.add(big_box_target if big_box_target is not None else new_position(right_target, (0,-1)))
        return target, deletes, inserts

    return target, deletes, inserts


def gps(position):
    pi, pj = position
    return 100 * pi + pj


def print_warehouse(warehouse, robot_position):
    max_i = max(i for i, _ in warehouse["walls"])
    max_j = max(j for _, j in warehouse["walls"])

    pixels = [["." for _ in range(max_j + 1)] for _ in range(max_i + 1)]
    for i, j in warehouse["walls"]:
        pixels[i][j] = "#"
    for i, j in warehouse["boxes"]:
        pixels[i][j] = "O"
    for i, j in warehouse["big_boxes"]:
        pixels[i][j] = "["
        pixels[i][j+1] = "]"
    i, j = robot_position
    pixels[i][j] = "@"
    print("\n".join("".join(line) for line in pixels))


def part_1(used_input):
    (robot_position, warehouse), moves = parse_input(used_input)
    for move in moves:
        if (next_position := push(robot_position, move, warehouse)) is not None:
            robot_position = next_position
        # print_warehouse(warehouse, robot_position)

    return sum(gps(box) for box in warehouse["boxes"])


def part_2(used_input):
    (robot_position, warehouse), moves = parse_input(used_input, biggify=True)
    for move in moves:
        # print(move)
        next_position, deletes, inserts = push2(robot_position, move, warehouse, set(), set())
        if next_position is not None:
            robot_position = next_position
            warehouse["big_boxes"] -= deletes
            warehouse["big_boxes"] |= inserts
        # print_warehouse(warehouse, robot_position)
        # input()

    return sum(gps(box) for box in warehouse["big_boxes"])


print(part_1(data))
print(part_2(data))
