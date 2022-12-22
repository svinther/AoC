from collections import deque
from pathlib import Path

DAY = 22
full_input_ = Path(f"{DAY}.txt").read_text()


def move(M, pos, axis, dir, num):
    # if moving on axis 1 (y) axis 0 (x) is the variable axis
    assert axis in (0, 1)
    assert dir in (-1, 1)
    axis_ = 1 if axis == 0 else 0

    path = [c[axis] for c in M.keys() if c[axis_] == pos[axis_]]
    minp, maxp = min(path), max(path)
    pathlen = len(path)

    step = (0 if axis == 1 else dir, 0 if axis == 0 else dir)

    npos = pos
    for i in range(1, pathlen + 1):
        if i > num:
            break
        savepos = npos

        npos = tuple(a + b for a, b in zip(npos, step))
        if npos[axis] > maxp:
            npos = (npos[0] if axis == 1 else minp, npos[1] if axis == 0 else minp)
        if npos[axis] < minp:
            npos = (npos[0] if axis == 1 else maxp, npos[1] if axis == 0 else maxp)

        if M[npos] == "#":
            return savepos
    return npos


def solve(parsed):
    facing = deque([">", "v", "<", "^"])
    M, S = parsed
    sy = min(y for _, y in M.keys())
    sx = min(x for x, y in M.keys() if y == sy)

    pos = (sx, sy)
    for s in S:
        print(pos, facing[0], s)
        if isinstance(s, int):
            dir = facing[0]
            if dir == ">":
                pos = move(M, pos, 0, 1, s)
            elif dir == "<":
                pos = move(M, pos, 0, -1, s)
            elif dir == "^":
                pos = move(M, pos, 1, -1, s)
            else:
                assert dir == "v"
                pos = move(M, pos, 1, 1, s)
        elif s == "R":
            facing.rotate(-1)
        elif s == "L":
            facing.rotate(1)
        else:
            assert False, s
    print(pos, facing[0])

    # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
    facescore = (
        0
        if facing[0] == ">"
        else 1
        if facing[0] == "v"
        else 2
        if facing[0] == "<"
        else 3
    )
    # The final password is the sum of 1000 times the row, 4 times the column, and the facing
    print(f"1000 * {(1+pos[1])} + 4 * {(1+pos[0])} + {facescore}")
    return 1000 * (1 + pos[1]) + 4 * (1 + pos[0]) + facescore


def parse(input_: str):
    mapc, movesi = input_.split("\n\n")
    themap = {}
    y = 0
    for l in mapc.split("\n"):
        for x, c in enumerate(l):
            if c == " ":
                continue
            themap[(x, y)] = c
        y += 1

    moves = []
    current = []
    movesi = movesi.strip()
    for i in range(len(movesi)):
        if movesi[i] in [str(n) for n in range(10)]:
            current.append(movesi[i])
        else:
            if current:
                moves.append(int("".join(current)))
                current.clear()
            moves.append((movesi[i]))
    if current:
        moves.append(int("".join(current)))

    return themap, moves


def testp1p2():
    print()
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""
    parsed = parse(input_)
    assert solve(parsed) == 6032


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
