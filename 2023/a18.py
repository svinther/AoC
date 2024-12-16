from itertools import *
from heapq import *
from collections import *

def shoelace(P):
    n=len(P)
    res = 0
    for i in range(n):
        px,_ = P[i]
        py1, py2 = P[i-1][1], P[(i+1)%n][1]
        res += px*(py2-py1)
    return abs(res / 2)

def solvep1(parsed):
    points =[]
    cx,cy =0,0
    l=0
    for d,s,_ in parsed:
        dx, dy = {"L": (-1,0), "R": (1,0), "U":(0,1), "D":(0,-1)}[d]
        cx, cy = cx+s*dx, cy+s*dy
        points.append((cx,cy))
        l+=s

    sl = shoelace(points)
    return sl + l/2 +1


def solvep2(parsed):
    points = []
    cx, cy = 0, 0
    l = 0
    for _, _, h in parsed:
        h = h.strip("()#")
        s = int(h[:5], 16)
        d=h[-1]
        dx, dy = {"2": (-1, 0), "0": (1, 0), "3": (0, 1), "1": (0, -1)}[d]
        cx, cy = cx + s * dx, cy + s * dy
        points.append((cx, cy))
        l += s

    sl = shoelace(points)
    return sl + l / 2 + 1


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        d, s, x = l.split()
        parsed.append((d,int(s),x))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 62


def run():
    input_ = open(0).read()
    parsed = parse(input_)
    p1result = solvep1(parsed)
    print(p1result)

    parsed = parse(input_)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
