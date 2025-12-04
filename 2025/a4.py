import re
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


def solvep1(parsed):
    answer = []
    R, C = len(parsed), len(parsed[0])
    for r in range(R):
        for c in range(C):
            rolls = 0
            if parsed[r][c] != "@":
                continue
            for dr, dc in dirs:
                nbr, nbc = r + dr, c + dc
                if 0 > nbr or nbr >= R or 0 > nbc or nbc >= C:
                    continue
                if parsed[nbr][nbc] == "@":
                    rolls += 1
            if rolls < 4:
                answer.append((r, c))
    for r, c in answer:
        parsed[r][c] = "."
    return len(answer)


def solvep2(parsed):
    answer = 0
    while True:
        rolls = solvep1(parsed)
        if rolls == 0:
            break
        answer += rolls
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
    print()
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 13

    parsed = parse(input_)
    assert solvep2(parsed) == 43


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
