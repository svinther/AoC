from itertools import *
from heapq import *
from collections import *


def expand(G):
    G_ = []
    for row in G:
        row_ = []
        for cell in row:
            if cell in ("#", "."):
                row_ += 2 * cell
            elif cell == "O":
                row_ += ["[", "]"]
            elif cell == "@":
                row_ += "@."
            else:
                assert False
        G_.append(row_)
    return G_


def solve(parsed, p2=False):
    G, moves = parsed
    if p2:
        G = expand(G)

    R = len(G)
    C = len(G[0])
    D = {"<": (0, -1), "^": (-1, 0), "v": (1, 0), ">": (0, 1)}

    for r in range(R):
        for c in range(C):
            if G[r][c] == "@":
                rob = (r, c)

    def push(p, d):
        assert len(p) > 0
        dr, dc = d

        nbp = set()
        for r, c in p:
            assert G[r][c] in ("[", "]", "@", "O"), f"Unmovable object {G[r][c]}"

            nbr, nbc = r + dr, c + dc
            if 0 > nbr or nbr >= R or 0 > nbc or nbc >= C:
                return False
            if G[nbr][nbc] == "#":
                return False
            if G[nbr][nbc] == ".":
                continue

            nbp.add((nbr, nbc))
            if dr != 0:
                if G[nbr][nbc] == "[":
                    assert G[nbr][nbc + 1] == "]"
                    nbp.add((nbr, nbc + 1))
                elif G[nbr][nbc] == "]":
                    assert G[nbr][nbc - 1] == "["
                    nbp.add((nbr, nbc - 1))

        if len(nbp) == 0 or push(nbp, d):
            for r, c in p:
                assert G[r][c] in ("[", "]", "@", "O"), f"Unmovable object {G[r][c]}"

                nbr, nbc = r + dr, c + dc
                assert G[nbr][nbc] == ".", f"moving to non dot {G[nbr][nbc]}"

                G[nbr][nbc] = G[r][c]
                G[r][c] = "."
            return True

        return False

    def score():
        answer = 0
        for r in range(R):
            for c in range(C):
                if G[r][c] in ("O", "["):
                    answer += 100 * r + c

                if G[r][c] == "]":
                    assert G[r][c - 1] == "["
                if G[r][c] == "[":
                    assert G[r][c + 1] == "]"
        return answer

    for m in moves:
        d = D[m]

        if push({rob}, d):
            robr, robc = rob
            dr, dc = d
            rob = robr + dr, robc + dc

    return score()


def parse(input_: str):
    mapp = []
    mp, moves = input_.split("\n\n")

    movp = []
    for ml in moves.split("\n"):
        ml = ml.strip()
        if not ml:
            continue
        movp += list(ml)

    for l in mp.split("\n"):
        l = l.strip()
        if not l:
            continue
        mapp.append(list(l))
    return mapp, movp


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""
    parsed = parse(input_)
    assert solve(parsed) == 2028


def testlarger():
    input_ = """
##########
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
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^    
"""
    parsed = parse(input_)
    assert solve(parsed) == 10092
    parsed = parse(input_)
    assert solve(parsed, p2=True) == 9021


def testp2ex():
    input_ = """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""
    parsed = parse(input_)
    assert solve(parsed, p2=True) == 618


def testmini():
    input_ = """
.......
@O.#...
.OO....
.......

>>><<v><v>>>>^
"""
    parsed = parse(input_)
    solve(parsed, p2=True)


def run():
    input_ = open(0).read()
    parsed = parse(input_)
    p1result = solve(parsed)
    print(p1result)

    parsed = parse(input_)
    p2result = solve(parsed, p2=True)
    print(p2result)


if __name__ == "__main__":
    run()
