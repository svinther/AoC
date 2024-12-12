from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "12"


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
    R = len(G)
    C = len(G[0])

    SEEN = set()
    gardens = defaultdict(list)
    for r in range(R):
        for c in range(C):
            if (r, c) in SEEN:
                continue
            t = G[r][c]
            a, p = 0, 0
            Q = deque([(r, c)])
            SEEN.add((r, c))
            while Q:
                xr, xc = Q.pop()
                a += 1
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nbr, nbc = xr + dr, xc + dc
                    if (
                        0 <= nbr < R
                        and 0 <= nbc < C
                        and (nbr, nbc) not in SEEN
                        and G[nbr][nbc] == t
                    ):
                        Q.append((nbr, nbc))
                        SEEN.add((nbr, nbc))
                    elif 0 > nbr or nbr >= R or 0 > nbc or nbc >= C or G[nbr][nbc] != t:
                        p += 1

            gardens[t].append((a, p))

    result = 0
    for t, gs in gardens.items():
        for a, p in gs:
            result += a * p

    return result


def solvep2(G):
    R = len(G)
    C = len(G[0])

    SEEN = set()
    gardens = defaultdict(list)
    for r in range(R):
        for c in range(C):
            if (r, c) in SEEN:
                continue
            t = G[r][c]
            a, p = 0, 0
            pseen = set()

            Q = deque([(r, c)])
            SEEN.add((r, c))
            while Q:
                xr, xc = Q.popleft()
                a += 1
                for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    dr, dc = d
                    nbr, nbc = xr + dr, xc + dc
                    if (
                        0 <= nbr < R
                        and 0 <= nbc < C
                        and (nbr, nbc) not in SEEN
                        and G[nbr][nbc] == t
                    ):
                        Q.append((nbr, nbc))
                        SEEN.add((nbr, nbc))

                    if 0 > nbr or nbr >= R or 0 > nbc or nbc >= C or G[nbr][nbc] != t:
                        if d == (1, 0) or d == (-1, 0):
                            left = (xr, xc - 1, d)
                            right = (xr, xc + 1, d)
                            if left not in pseen and right not in pseen:
                                p += 1

                            pseen.add((xr, xc, d))
                        else:
                            above = (xr - 1, xc, d)
                            below = (xr + 1, xc, d)
                            if above not in pseen and below not in pseen:
                                p += 1
                            pseen.add((xr, xc, d))

            gardens[t].append((a, p))

    result = 0
    for t, gs in gardens.items():
        for a, p in gs:
            result += a * p

    return result


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(l)
    return parsed


def testp2mini0():
    input_ = """
AAAA
BBCD
BBCC
EEEC
"""

    parsed = parse(input_)
    assert solvep2(parsed) == 80


def testp2mini1():
    input_ = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""
    parsed = parse(input_)
    assert solvep2(parsed) == 236


def testp2mini2():
    input_ = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA    
"""
    parsed = parse(input_)
    assert solvep2(parsed) == 368


def testm():
    input_ = """
XXXOX
XOXOX
XXXOX
XXXXX
    """
    parsed = parse(input_)
    assert solvep2(parsed) == 12 * 16 + 4 * 1 + 4 * 3


def testm2():
    input_ = """
XXX
XOX
XXX
    """
    parsed = parse(input_)
    assert solvep2(parsed) == 8 * 8 + 1 * 4


def testm3():
    input_ = """
OOOOO
OXOXO
OXXXO    
    """
    parsed = parse(input_)
    assert solvep2(parsed) == 12 * 10 + 5 * 8


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 1930
    assert solvep2(parsed) == 1206


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
