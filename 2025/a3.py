import re
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def maxpos(s):
    m = str(max(list(s)))
    return s.index(m), m


def solvep1(parsed):
    res = 0
    for bat in parsed:
        p0, m0 = maxpos(bat[:-1])
        p1, m1 = maxpos(bat[p0 + 1 :])
        volt = int(m0 + m1)
        # print(bat, p0, p1, volt)
        res += volt
    return res


def solvep2(parsed):
    res = 0

    for bat in parsed:
        volts = []
        for i in range(11, -1, -1):
            b = bat[:-i] if i > 0 else bat
            p0, m0 = maxpos(b)
            volts.append(m0)
            bat = bat[p0 + 1 :]

        res += int("".join(volts))
    return res


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
987654321111111
811111111111119
234234234234278
818181911112111
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 357
    assert solvep2(parsed) == 3121910778619


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
