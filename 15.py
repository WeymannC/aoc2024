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


def parse_map(raw_map):
    warehouse = {"walls": set(), "boxes": set()}
    starting_position = None
    for i, line in enumerate(raw_map.split("\n")):
        for j, char in enumerate(line):
            if char == "#":
                warehouse["walls"].add((i, j))
            elif char == "O":
                warehouse["boxes"].add((i, j))
            elif char == "@":
                starting_position = (i, j)
    return starting_position, warehouse


def parse_moves(raw_moves):
    yield from "".join(raw_moves.split("\n"))


def parse_input(raw):
    raw_map, raw_moves = raw.split("\n\n")

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
    pass


print(part_1(data))
print(part_2(example))
