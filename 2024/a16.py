from itertools import *
from heapq import *
from collections import *

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def solvep1(G):
    R = len(G)
    C = len(G[0])
    S, E = None, None
    for r in range(R):
        for c in range(C):
            if G[r][c] == "S":
                S = r, c
            elif G[r][c] == "E":
                E = r, c
    costs = {(S, 0): 0}
    pq = [(0, (S, 0))]
    while pq:
        cost, (s, d) = heappop(pq)
        if cost != costs[(s, d)]:
            continue
        if s == E:
            return cost
        sr, sc = s

        # move forward
        dr, dc = dirs[d]
        nbr, nbc = sr + dr, sc + dc
        if 0 <= nbr < R and 0 <= nbc < C and G[nbr][nbc] != "#":
            nb = ((nbr, nbc), d)
            if nb not in costs or costs[nb] > cost + 1:
                costs[nb] = cost + 1
                heappush(pq, (cost + 1, nb))

        # rotate
        for dn in [(d + 1) % 4, (d - 1) % 4]:
            nb = ((sr, sc), dn)
            if nb not in costs or costs[nb] > cost + 1000:
                costs[nb] = cost + 1000
                heappush(pq, (cost + 1000, nb))


def solvep2(G):
    R = len(G)
    C = len(G[0])
    S, E = None, None
    for r in range(R):
        for c in range(C):
            if G[r][c] == "S":
                S = r, c
            elif G[r][c] == "E":
                E = r, c

    cost = solvep1(G)
    costs = {(S, 0): 0}
    allp = set()

    P = [(S, 0)]
    cur = {S}

    def bt(c):
        s, d = P[-1]

        if c == cost and s == E:
            allp.update(cur)
        elif c > cost:
            return

        sr, sc = s
        for dn, dcost in [(d, 0), ((d + 1) % 4, 1000), ((d - 1) % 4, 1000)]:
            dr, dc = dirs[dn]
            nbr, nbc = sr + dr, sc + dc
            if (
                0 <= nbr < R
                and 0 <= nbc < C
                and G[nbr][nbc] != "#"
                and (nbr, nbc) not in cur
            ):
                nb = ((nbr, nbc), dn)
                newcost = c + 1 + dcost
                if nb not in costs or newcost <= costs[nb]:
                    costs[nb] = newcost

                    cur.add((nbr, nbc))
                    P.append(nb)
                    bt(newcost)
                    cur.remove((nbr, nbc))
                    P.pop()

    bt(0)
    return len(allp)


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
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 7036
    assert solvep2(parsed) == 45


def testp1p2_2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 11048
    assert solvep2(parsed) == 64


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
