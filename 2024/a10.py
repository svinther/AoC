from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
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


def solvep1(G):
    R = len(G)
    C = len(G[0])

    Q = deque()

    for r in range(R):
        for c in range(C):
            if G[r][c] == 0:
                Q.append(((r, c), (r, c)))

    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    answer = 0
    SEEN = defaultdict(set)
    while Q:
        (r, c), trailhead = Q.popleft()
        if G[r][c] == 9:
            answer += 1
            continue

        for dr, dc in dirs:
            nbr, nbc = r + dr, c + dc
            if 0 <= nbr < R and 0 <= nbc < C:
                if G[nbr][nbc] == G[r][c] + 1:
                    if (nbr, nbc) in SEEN[trailhead]:
                        continue
                    SEEN[trailhead].add((nbr, nbc))
                    Q.append(((nbr, nbc), trailhead))
    return answer


def solvep2(G):
    R = len(G)
    C = len(G[0])

    Q = deque()

    for r in range(R):
        for c in range(C):
            if G[r][c] == 0:
                Q.append(((r, c), (r, c)))

    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    answer = 0
    while Q:
        (r, c), trailhead = Q.popleft()
        if G[r][c] == 9:
            answer += 1
            continue

        for dr, dc in dirs:
            nbr, nbc = r + dr, c + dc
            if 0 <= nbr < R and 0 <= nbc < C:
                if G[nbr][nbc] == G[r][c] + 1:
                    Q.append(((nbr, nbc), trailhead))

    return answer


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        l = list(map(int, l))
        parsed.append(l)
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 36
    assert solvep2(parsed) == 81


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
