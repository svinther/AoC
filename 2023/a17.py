from heapq import heappush, heappop
from math import inf
from pathlib import Path

import requests

YEAR = "2023"
DAY = "17"


def getinput():
    path = Path(f"{DAY}.txt")
    if not path.exists():
        sessionid = Path(".secret").read_text().strip()
        res = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{DAY}/input",
            cookies={"session": sessionid},
        )
        path.write_text(res.text)
    return path.read_text()


def solve(parsed, maxmoves=3, minmoves=0):
    G, X, Y = parsed
    Q = []  # cost, x,y,nummoves, direction
    heappush(Q, (0, 0, 0, 0, "o"))
    SEEN = set()
    COST = {}

    while Q:
        c, x, y, m, d = heappop(Q)
        if c > COST.get((x, y, m, d), inf):
            continue

        possibles = []
        # left ?
        if x > 0:
            if d in "^v" and m >= minmoves:
                possibles.append((x - 1, y, "<", 1))
            elif d == "<" and m < maxmoves:
                possibles.append((x - 1, y, "<", m + 1))
        # right ?
        if x < X - 1:
            if d == "o" or (d in "^v" and m >= minmoves):
                possibles.append((x + 1, y, ">", 1))
            elif d == ">" and m < maxmoves:
                possibles.append((x + 1, y, ">", m + 1))
        # up ?
        if y > 0:
            if d in "<>" and m >= minmoves:
                possibles.append((x, y - 1, "^", 1))
            elif d == "^" and m < maxmoves:
                possibles.append((x, y - 1, "^", m + 1))
        # down ?
        if y < Y - 1:
            if d == "o" or (d in "<>" and m >= minmoves):
                possibles.append((x, y + 1, "v", 1))
            elif d == "v" and m < maxmoves:
                possibles.append((x, y + 1, "v", m + 1))

        for dx, dy, dd, dm in possibles:
            if (dx, dy, dd, dm) in SEEN:
                continue

            dc = c + G[(dx, dy)]
            if dx == X - 1 and dy == Y - 1 and dm >= minmoves:
                return dc

            if dc < COST.get((dx, dy, dm, dd), inf):
                COST[(dx, dy, dm, dd)] = dc
                heappush(Q, (dc, dx, dy, dm, dd))

        SEEN.add((x, y, m, d))


def parse(input_: str):
    parsed = {}
    y = 0
    x = 0
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        for x, v in enumerate(l):
            parsed[(x, y)] = int(v)
        y += 1

    return parsed, x + 1, y


def testp1p2():
    print()
    input1 = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
    parsed = parse(input1)
    assert solve(parsed, 3) == 102
    assert solve(parsed, 10, minmoves=4) == 94

    input2 = """\
111111111111
999999999991
999999999991
999999999991
999999999991
"""
    parsed = parse(input2)
    assert solve(parsed, 10, minmoves=4) == 71


def run():
    parsed = parse(getinput())
    result = solve(parsed), solve(parsed, 10, minmoves=4)
    print(result)


if __name__ == "__main__":
    run()
