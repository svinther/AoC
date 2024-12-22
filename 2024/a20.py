import re
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def solve(parsed, tlimit, climit):
    G = parsed
    R = len(G)
    C = len(G[0])

    for r in range(R):
        for c in range(C):
            if G[r][c] == "S":
                S = r, c
            if G[r][c] == "E":
                E = r, c

    def bfs(start):
        Q = deque()
        Q.append((start, 0))
        SEEN = {start}
        distances = {}
        while Q:
            (r, c), d = Q.popleft()
            distances[(r, c)] = d
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nbr, nbc = r + dr, c + dc
                if 0 <= nbr < R and 0 <= nbc < C:
                    if G[nbr][nbc] == "#":
                        continue
                    if (nbr, nbc) in SEEN:
                        continue
                    SEEN.add((nbr, nbc))
                    Q.append(((nbr, nbc), d + 1))
        return distances

    dists_from_end = bfs(E)
    dists_from_start = bfs(S)
    fastest_time = dists_from_end[S]
    maxracetime = fastest_time - tlimit

    Q = deque()
    SEEN = set()
    for p, t0 in dists_from_start.items():
        if t0 < maxracetime:
            Q.append((p, p, t0, 0))
            SEEN.add((p, p))

    answer = 0
    while Q:
        p0, (r, c), t0, t = Q.popleft()
        if G[r][c] != "#":
            tleft = dists_from_end[(r, c)]
            racetime = t0 + t + tleft
            if racetime <= maxracetime:
                answer += 1

        if t < climit:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nbr, nbc = r + dr, c + dc
                if 0 <= nbr < R and 0 <= nbc < C:
                    if (p0, (nbr, nbc)) in SEEN:
                        continue
                    SEEN.add((p0, (nbr, nbc)))
                    Q.append((p0, (nbr, nbc), t0, t + 1))
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
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
    parsed = parse(input_)
    assert solve(parsed, 64, 2) == 1
    assert solve(parsed, 40, 2) == 2
    assert solve(parsed, 38, 2) == 3
    assert solve(parsed, 36, 2) == 4
    assert solve(parsed, 20, 2) == 5
    assert solve(parsed, 12, 2) == 8

    assert solve(parsed, 76, 20) == 3
    assert solve(parsed, 74, 20) == 4 + 3
    assert solve(parsed, 72, 20) == 4 + 3 + 22
    assert solve(parsed, 70, 20) == 4 + 3 + 22 + 12


def run():
    input_ = open(0).read()
    parsed = parse(input_)
    p1result = solve(parsed, 100, 2)
    print(p1result)

    parsed = parse(input_)
    p2result = solve(parsed, 100, 20)
    print(p2result)


if __name__ == "__main__":
    run()
