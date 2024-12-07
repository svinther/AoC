from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "7"


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


def possiblep1(opers, res):
    n = len(opers)

    def bt(i, cur):
        if i == n:
            return cur == res
        return bt(i + 1, cur + opers[i]) or bt(i + 1, cur * opers[i])

    return bt(1, opers[0])


def possiblep2(opers, res):
    n = len(opers)

    def bt(i, cur):
        if i == n:
            return cur == res
        return (
            bt(i + 1, cur + opers[i])
            or bt(i + 1, cur * opers[i])
            or bt(i + 1, int(str(cur) + str(opers[i])))
        )

    return bt(1, opers[0])


def solvep1(parsed):
    answer = 0
    for t, o in parsed:
        if possiblep1(o, t):
            answer += t
    return answer


def solvep2(parsed):
    answer = 0
    for t, o in parsed:
        if possiblep2(o, t):
            answer += t
    return answer


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        t, o = l.split(": ")
        t = int(t)
        o = list(map(int, o.split()))
        parsed.append((t, o))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 3749
    assert solvep2(parsed) == 11387


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
