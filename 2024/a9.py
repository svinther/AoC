from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "9"


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
    D = deque(parsed)
    result = []

    while D:
        lbid, use, free = D.popleft()
        result.append((lbid, use))

        while free > 0 and D:
            rbid, need, _ = D.pop()
            result.append((rbid, min(free, need)))
            if need > free:
                need -= free
                free = 0
                D.append((rbid, need, -1))
            else:
                free -= need

    answer = 0
    pos = 0
    for bid, use in result:
        for _ in range(use):
            answer += pos * bid
            pos += 1

    return answer


def solvep2(parsed):
    D = deque(parsed)
    moved = set()
    j = len(D) - 1
    while j > 0:
        if D[j][0] in moved:
            j -= 1
            continue
        moved.add(D[j][0])
        for i in range(j):
            if D[i][2] >= D[j][1]:
                D[j - 1][2] += D[j][1] + D[j][2]

                ifree = D[i][2]
                D[i][2] = 0  # zero left free size

                D.insert(i + 1, [D[j][0], D[j][1], ifree - D[j][1]])

                del D[j + 1]
                break
        else:
            j -= 1
            continue

    answer = 0
    pos = 0
    for bid, use, free in D:
        for _ in range(use):
            answer += pos * bid
            pos += 1
        pos += free

    return answer


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        for bid, tup in enumerate(batched(l, 2)):
            if len(tup) == 2:
                parsed.append(list((bid, int(tup[0]), int(tup[1]))))
            else:
                assert len(tup) == 1
                parsed.append(list((bid, int(tup[0]), 0)))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
2333133121414131402
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 1928
    assert solvep2(parsed) == 2858


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
