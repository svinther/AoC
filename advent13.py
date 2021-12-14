import re

day = 13
year = 2021

inputs = []

inputs.append("""\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""")



with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())

def parse(input):
    p_coord = re.compile("(\d+),(\d+)")
    p_fold = re.compile("fold along ([xy])=(\d+)")

    coords = set()
    fold_instructions = []

    for line in input.split("\n"):
        line_strip = line.strip()
        if not line_strip:
            continue

        m_coord = p_coord.fullmatch(line_strip)
        if m_coord:
            coords.add((int(m_coord.group(1)), int(m_coord.group(2))))
        else:
            m_fold = p_fold.fullmatch(line_strip)
            if m_fold:
                fold_instructions.append((m_fold.group(1), int(m_fold.group(2))))
            else:
                assert False
    return coords, fold_instructions


def fold_left(coord, fold_line):
    x, y = coord
    assert x != fold_line

    if x > fold_line:
        return (x - fold_line - 1, y)
    else:
        return (fold_line - x - 1, y)


def fold_up(coord, fold_line):
    x, y = coord
    y_rel = y - fold_line
    if y_rel <= 0:
        return (x, y)
    else:
        y_new = fold_line - y_rel
        if y_new >= 0:
            return (x, y_new)
        else:
            assert False


def visualize(field, coords):
    row = ['.' for x in range(field[0])]
    rows = [row.copy() for y in range(field[1])]

    for x, y in coords:
        assert x < field[0]
        assert y < field[1]
        rows[y][x] = "#"

    return "\n".join(["".join(r) for r in rows])


def fold(field, coords, axis, fold_line):
    if axis == "x":
        assert fold_line not in (c[0] for c in coords)
        new_field = (fold_line, field[1])
        new_coords = {fold_left(c, fold_line) for c in coords}
    elif axis == "y":
        assert fold_line not in (c[1] for c in coords)
        new_field = (field[0], fold_line)
        new_coords = {fold_up(c, fold_line) for c in coords}
    else:
        assert False

    return (new_field, new_coords)


for input in inputs:
    coords, fold_instructions = parse(input)
    initial_field = (1 + max((c[0] for c in coords)), 1 + max((c[1] for c in coords)))
    # set of all field coords
    # initial_field = {(x, y) for x in range(initial_field_size[0]) for y in range(initial_field_size[1])}
    # assert len(initial_field) ==  initial_field_size[0] * initial_field_size[1]

    steps = [(initial_field, coords)]
    # print(visualize(initial_field, coords))
    print(f"Visible dots: {len(coords)}")

    for step_num, fold_instruction in enumerate(fold_instructions, start=1):
        axis, fold_line = fold_instruction
        field, coords = steps[-1]
        new_field, new_coords = fold(field, coords, axis, fold_line)
        steps.append((new_field, new_coords))

        print(f"Step number: {step_num}")
        print(fold_instruction)
        print(visualize(new_field, new_coords))
        print(f"Visible dots: {len(new_coords)}")

"""
.#..# . #..# . #### . #### . ##.. . .##. . .##. . ##..
.#..# . .#.# . ...# . ...# . #... . #..# . #..# . #...
.#..# . ..## . .### . .### . #... . #..# . ...# . #...
.#..# . .#.# . ...# . ...# . #... . #### . ##.# . #...
.#..# . .#.# . ...# . ...# . #..# . #..# . #..# . #..#
..##. . #..# . ...# . #### . .##. . #..# . ###. . .##.
"""
