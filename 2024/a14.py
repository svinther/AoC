from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "14"


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


def solvep1(parsed):
    R = max(py for (_, py), _ in parsed)
    C = max(px for (px, _), _ in parsed)

    quadrant_max = [(R // 2 - 1, C // 2 - 1), (R // 2 - 1, C), (R, C // 2 - 1), (R, C)]
    midr, midc = R // 2, C // 2

    quadrant_counts = [0] * 4
    for (px, py), (vx, vy) in parsed:
        pnx, pny = (px + vx * 100) % (C + 1), (py + vy * 100) % (R + 1)

        if pnx == midc or pny == midr:
            continue

        for i in range(4):
            qr, qc = quadrant_max[i]
            if pnx <= qc and pny <= qr:
                quadrant_counts[i] += 1
                break

    answer = 1
    for qc in quadrant_counts:
        answer *= qc

    return answer


def render(G):
    for r in G:
        for c in r:
            print("." if c == 0 else c, end="")
        print()


def solvep2(parsed):
    R = max(py for (_, py), _ in parsed)
    C = max(px for (px, _), _ in parsed)

    i = 1
    SEEN = set()
    while True:
        G = [[0] * (C + 1) for _ in range(R + 1)]
        m = 0
        for (px, py), (vx, vy) in parsed:
            pnx, pny = (px + vx * i) % (C + 1), (py + vy * i) % (R + 1)
            G[pny][pnx] += 1
            m = max(m, G[pny][pnx])
        if m == 1:
            # it happens only once in the cycle that no robots are in same space
            render(G)
            return i

        h = []
        for r in G:
            h.append(hash(tuple(r)))
        h = tuple(h)
        if h in SEEN:
            break
        SEEN.add(h)

        i += 1


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        p, v = l.split()
        p, v = p.split("=")[1], v.split("=")[1]
        p, v = p.split(","), v.split(",")

        parsed.append(((int(p[0]), int(p[1])), (int(v[0]), int(v[1]))))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 12


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
