from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "1"


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
    left = [l for l, _ in parsed]
    right = [r for _, r in parsed]
    left.sort()
    right.sort()
    answer = 0
    for l, r in zip(left, right):
        answer += abs(l - r)
    return answer


def solvep2(parsed):
    left = [l for l, _ in parsed]
    right = [r for _, r in parsed]

    rightcounts = Counter(right)
    answer = 0
    for l in left:
        answer += l * rightcounts[l]
    return answer


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        n1, n2 = map(int, l.split("  "))
        parsed.append((n1, n2))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\

"""
    parsed = parse(input_)
    # assert solvep1(parsed) == 42


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
