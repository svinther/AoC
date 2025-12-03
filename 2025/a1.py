import re
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def solvep1(parsed):
    pos = 50
    answer = 0
    for instr in parsed:
        lr, num = instr[0], int(instr[1:])
        if lr == "L":
            pos -= num
        else:
            pos += num
        pos %= 100
        if pos == 0:
            answer += 1
    return answer


def solvep2(parsed):
    pos = 50
    answer = 0
    for instr in parsed:
        lr, num = instr[0], int(instr[1:])
        answer += num // 100
        num %= 100
        if lr == "L":
            pos -= num
            if pos <= 0 < pos + num:
                answer += 1
        else:
            pos += num
            if pos >= 100:
                answer += 1
        pos %= 100
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
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 3
    assert solvep2(parsed) == 6
    return True


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
