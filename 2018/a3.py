from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2018"
DAY = "3"


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
    claimed = defaultdict(list)
    conflicts = set()

    for claim, (c, r), (n, m) in parsed:
        for i in range(n):
            for j in range(m):
                if claimed[(c + i, r + j)]:
                    for cclaim in claimed[(c + i, r + j)]:
                        conflicts.add(cclaim)
                    conflicts.add(claim)
                claimed[(c + i, r + j)].append(claim)

    allclaims = {claim for claim, *_ in parsed}
    answer = allclaims - conflicts
    assert len(answer) == 1
    return answer.pop()


def solvep2(parsed):
    pass


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        claim, _, start, size = l.split()
        claim = claim.strip("#")
        start = start.strip(":")
        start = tuple(map(int, start.split(",")))
        size = tuple(map(int, size.split("x")))
        parsed.append((claim, start, size))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 4


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
