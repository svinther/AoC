from collections import deque, defaultdict
from copy import copy
from pathlib import Path

DAY = 23
full_input_ = Path(f"{DAY}.txt").read_text()


def render(E):
    minx, maxx = min(x for x, _ in E), max(x for x, _ in E)
    miny, maxy = min(y for _, y in E), max(y for _, y in E)

    for y in range(maxy, miny - 1, -1):
        for x in range(minx, maxx + 1):
            if (x, y) in E:
                print("#", end="")
            else:
                print(".", end="")
        print()


def scan(E, e, checkmods):
    return {tuple(a + b for a, b in zip(cm, e)) for cm in checkmods}.intersection(E)


def normalize(E):
    minx, maxx = min(x for x, _ in E), max(x for x, _ in E)
    miny, maxy = min(y for _, y in E), max(y for _, y in E)
    return {(0 - minx + e[0], 0 - miny + e[1]) for e in E}


def solve(E, maxrounds):
    # N,S,W,E
    nextp = deque(
        [
            (tuple((x, 1) for x in range(-1, 2)), (0, 1)),
            (tuple((x, -1) for x in range(-1, 2)), (0, -1)),
            (tuple((-1, y) for y in range(-1, 2)), (-1, 0)),
            (tuple((1, y) for y in range(-1, 2)), (1, 0)),
        ]
    )
    assert E == normalize(E)
    r = 0
    for r in range(maxrounds):
        # E = normalize(E)
        # render(E)
        # 1. half
        moves = defaultdict(list)
        for e in E:
            # If no other Elves are in one of those eight positions, the Elf does not do anything during this round
            clear = True
            # look for move
            move = None
            for checkmods, movemod in nextp:
                if scan(E, e, checkmods):
                    clear = False
                elif move is None:
                    move = tuple(a + b for a, b in zip(movemod, e))

            if clear:
                continue
            if move:
                moves[move].append(e)

        if not moves:
            break

        # 2. half
        for tpos, elfs in moves.items():
            if len(elfs) == 1:
                e = elfs[0]
                E.remove(e)
                assert tpos not in E
                E.add(tpos)

        # finally
        nextp.rotate(-1)

    minx, maxx = min(x for x, _ in E), max(x for x, _ in E)
    miny, maxy = min(y for _, y in E), max(y for _, y in E)

    lenx = maxx - minx + 1
    leny = maxy - miny + 1

    return lenx * leny - len(E), r + 1


def parse(input_: str):
    parsed = set()
    y = 0
    for l in reversed(input_.split("\n")):
        l = l.strip()
        if not l:
            continue
        for x, c in enumerate(l):
            if c == "#":
                parsed.add((x, y))
        y += 1
    return parsed


def testp1p2():
    print()
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""
    parsed = parse(input_)
    assert solve(copy(parsed), 10)[0] == 110

    assert solve(copy(parsed), int(1e100))[1] == 20


def run():
    parsed = parse(full_input_)
    result = solve(copy(parsed), 10)
    print(result[0])

    result = solve(copy(parsed), int(1e100))
    print(result[1])


if __name__ == "__main__":
    run()
