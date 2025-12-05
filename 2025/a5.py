import re
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def solvep1(parsed):
    rngs, ings = parsed.split("\n\n")
    ranges = []
    for rng in [list(map(int, r.split("-"))) for r in rngs.split("\n")]:
        ranges.append(rng)

    answer = 0
    for ing in ings.split("\n"):
        if not ing:
            continue
        ing = int(ing)
        for r0, r1 in ranges:
            if r0 <= ing <= r1:
                answer += 1
                break

    return answer


def solvep2(parsed):
    rngs, ings = parsed.split("\n\n")
    ranges = []
    for rng in [tuple(map(int, r.split("-"))) for r in rngs.split("\n")]:
        ranges.append(rng)

    answer = 0
    ranges.sort()
    seen = 0
    for r0, r1 in ranges:
        if r1 <= seen:
            continue
        if r0 <= seen:
            r0 = seen + 1
        if r0 > r1:
            continue
        answer += r1 - r0 + 1
        seen = r1
    return answer


def parse(input_: str):
    return input_


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
    parsed = parse(input_)
    assert solvep2(parsed) == 14


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
