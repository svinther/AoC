from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "8"


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
    ants = defaultdict(list)
    for r in range(R):
        for c in range(C):
            if G[r][c] != ".":
                ants[G[r][c]].append((r, c))

    antinodes = set()
    for nt, nodes in ants.items():
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                ni, nj = nodes[i], nodes[j]

                dr, dc = nj[0] - ni[0], nj[1] - ni[1]
                an1 = (ni[0] - dr, ni[1] - dc)
                an2 = (nj[0] + dr, nj[1] + dc)
                for anr, anc in [an1, an2]:
                    if 0 <= anr < R and 0 <= anc < C:
                        antinodes.add((anr, anc))

    return len(antinodes)


def solvep2(G):
    R = len(G)
    C = len(G[0])
    ants = defaultdict(list)
    for r in range(R):
        for c in range(C):
            if G[r][c] != ".":
                ants[G[r][c]].append((r, c))

    antinodes = set()
    for nt, nodes in ants.items():
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                ni, nj = nodes[i], nodes[j]

                dr, dc = nj[0] - ni[0], nj[1] - ni[1]
                k = 0
                ok = True
                while ok:
                    ok = False
                    an1 = (ni[0] - dr * k, ni[1] - dc * k)
                    an2 = (nj[0] + dr * k, nj[1] + dc * k)
                    for anr, anc in [an1, an2]:
                        if 0 <= anr < R and 0 <= anc < C:
                            antinodes.add((anr, anc))
                            ok = True
                    k += 1

    return len(antinodes)


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(l)
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 14
    assert solvep2(parsed) == 34


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
