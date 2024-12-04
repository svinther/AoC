import re
from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "4"


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
    m, n = len(parsed), len(parsed[0])
    WORD = "XMAS"

    Q = []
    for r in range(m):
        for c in range(n):
            if parsed[r][c] == WORD[0]:
                Q.append((r, c, 0, (1, 0)))
                Q.append((r, c, 0, (-1, 0)))
                Q.append((r, c, 0, (0, 1)))
                Q.append((r, c, 0, (0, -1)))
                Q.append((r, c, 0, (1, 1)))
                Q.append((r, c, 0, (-1, -1)))
                Q.append((r, c, 0, (1, -1)))
                Q.append((r, c, 0, (-1, 1)))

    answer = 0

    while Q:
        r, c, pos, (dr, dc) = Q.pop()
        if pos == 3:
            answer += 1
            continue
        nbr, nbc = r + dr, c + dc
        if 0 <= nbr < n and 0 <= nbc < m:
            if parsed[nbr][nbc] == WORD[pos + 1]:
                Q.append((nbr, nbc, pos + 1, (dr, dc)))

    return answer


def solvep2(parsed):
    m, n = len(parsed), len(parsed[0])
    WORD = "MAS"

    Q = []
    for r in range(m):
        for c in range(n):
            if parsed[r][c] == WORD[0]:
                Q.append((r, c, 0, (1, 1)))
                Q.append((r, c, 0, (-1, -1)))
                Q.append((r, c, 0, (1, -1)))
                Q.append((r, c, 0, (-1, 1)))

    found = set()
    answer = 0

    while Q:
        r, c, pos, (dr, dc) = Q.pop()
        if pos == 2:
            center = (r - dr, c - dc)
            if center in found:
                answer += 1
            else:
                found.add(center)
            continue
        nbr, nbc = r + dr, c + dc
        if 0 <= nbr < n and 0 <= nbc < m:
            if parsed[nbr][nbc] == WORD[pos + 1]:
                Q.append((nbr, nbc, pos + 1, (dr, dc)))

    return answer


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
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 18
    assert solvep2(parsed) == 9


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
