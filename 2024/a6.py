from copy import deepcopy
from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "6"


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


def solvep1(G):
    C, R = len(G), len(G[0])
    for c in range(C):
        for r in range(R):
            if G[r][c] == "^":
                guard = (r, c)
                break

    dirs = deque([(-1, 0), (0, 1), (1, 0), (0, -1)])

    counted = set()
    r, c = guard
    steps = 0
    seen = {(r, c, dirs[0])}
    while 0 <= r < R and 0 <= c < C:
        steps += 1 if (r, c) not in counted else 0
        counted.add((r, c))

        dr, dc = dirs[0]

        while 0 <= r + dr < R and 0 <= c + dc < C and G[r + dr][c + dc] == "#":
            dirs.rotate(-1)
            dr, dc = dirs[0]
        r, c = r + dr, c + dc
        if (r, c, (dr, dc)) in seen:
            return -1
        seen.add((r, c, (dr, dc)))

    return steps


def solvep2(G):
    C, R = len(G), len(G[0])
    answer = 0
    for c in range(C):
        for r in range(R):
            if G[r][c] == ".":
                G[r][c] = "#"
                if solvep1(G) == -1:
                    answer += 1
                G[r][c] = "."
    return answer


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(list(l))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 41


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
