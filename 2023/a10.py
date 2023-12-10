from collections import deque, defaultdict
from itertools import product
from pathlib import Path
import requests

YEAR = "2023"
DAY = "10"


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


def solve(parsed):
    start, G = parsed
    Q = deque()
    Q.append((start, {start}))

    NORTH = {"|", "J", "L", "S"}
    SOUTH = {"|", "F", "7", "S"}
    EAST = {"-", "L", "F", "S"}
    WEST = {"-", "J", "7", "S"}

    MAXLOOP = set()
    while Q:
        pos, seen = Q.popleft()

        # dir, cur, dest
        N = (pos[0], pos[1] - 1), NORTH, SOUTH
        S = (pos[0], pos[1] + 1), SOUTH, NORTH
        E = (pos[0] + 1, pos[1]), EAST, WEST
        W = (pos[0] - 1, pos[1]), WEST, EAST

        for d, (newpos, cur, dest) in enumerate((N, S, E, W)):
            if newpos in G and G[pos] in cur and G[newpos] in dest:
                if newpos in seen:
                    if newpos == start:
                        if len(seen) > len(MAXLOOP):
                            MAXLOOP = seen
                    continue
                Q.append((newpos, seen | {newpos}))

    p1 = (len(MAXLOOP) + 1) // 2

    MINX, MAXX = min(x for x, _ in MAXLOOP), max(x for x, _ in MAXLOOP)
    MINY, MAXY = min(y for _, y in MAXLOOP), max(y for _, y in MAXLOOP)
    p2 = 0
    for y in range(MINY, MAXY + 1):
        inside = False
        up = None
        for x in range(MINX, MAXX + 1):
            if (x, y) in MAXLOOP:
                pipe = G[(x, y)]
                if pipe == "S":
                    pipe = "|"
                if pipe == "|":
                    inside = not inside
                elif pipe == "-":
                    assert up is not None
                elif pipe in "JL":
                    if up is None:
                        up = True
                    elif up is True:
                        up = None
                    else:
                        up = None
                        inside = not inside
                elif pipe in "F7":
                    if up is None:
                        up = False
                    elif up is False:
                        up = None
                    else:
                        up = None
                        inside = not inside
                else:
                    assert False
            elif inside:
                p2 += 1
    return p1, p2


def parse(input_: str):
    """
    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
    """
    parsed = {}
    start = None
    y = 0
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        for x, c in enumerate(l):
            if c == "S":
                start = (x, y)
            if c in (".", "I", "O"):
                continue
            else:
                parsed[(x, y)] = c
        y += 1
    return start, parsed


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
