import re
from itertools import *
from heapq import *
from collections import *
from math import floor


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def solvep1(parsed):
    A, B, C, P = parsed

    def combo(v):
        nonlocal A, B, C
        if v == 4:
            return A
        if v == 5:
            return B
        if v == 6:
            return C

        assert v != 7

        return v

    instructions = []

    def adv(operand):
        nonlocal A, B, C
        v = combo(operand)
        A = floor(A / (2**v))

    instructions.append(adv)

    def bxl(operand):
        nonlocal A, B, C
        v = operand
        B ^= v

    instructions.append(bxl)

    def bst(operand):
        nonlocal A, B, C
        v = combo(operand)
        B = v % 8

    instructions.append(bst)

    def jnz(operand):
        nonlocal A, B, C
        if A != 0:
            return "JUMP", operand

    instructions.append(jnz)

    def bxc(operand):
        nonlocal A, B, C
        B ^= C

    instructions.append(bxc)

    def out(operand):
        nonlocal A, B, C
        v = combo(operand)
        return "OUT", v % 8

    instructions.append(out)

    def bdv(operand):
        nonlocal A, B, C
        v = combo(operand)
        B = floor(A / (2**v))

    instructions.append(bdv)

    def cdv(operand):
        nonlocal A, B, C
        v = combo(operand)
        C = floor(A / (2**v))

    instructions.append(cdv)

    outputs = []
    i = 0
    n = len(P)
    # print((A,B,C))
    while i < n:
        result = instructions[P[i]](P[i + 1])
        # print(i, (A,B,C), instructions[P[i]].__name__, P[i+1], "-->", result)

        if result:
            t, v = result
            if t == "OUT":
                outputs.append(str(v))
            elif t == "JUMP":
                i = v
                continue
        i += 2

    return ",".join(outputs)


def solvep2(parsed):
    _, B, C, P = parsed
    GOAL = ",".join(str(p) for p in P)
    i = 0

    l = 0
    while True:
        cur = solvep1((i, B, C, P))
        print(cur, "--", GOAL)
        if len(cur) != l:
            l = len(cur)
            print(l, len(GOAL))

        if cur == GOAL:
            return i
        i += 1


def parse(input_: str):
    regs, prog = input_.split("\n\n")

    R = []
    for l in regs.split("\n"):
        l = l.strip()
        if not l:
            continue
        v, *_ = ints(l)
        R.append(v)

    P = ints(prog.strip())

    return *R, P


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
    parsed = parse(input_)
    assert solvep1(parsed) == "4,6,3,5,6,3,5,2,1,0"


def testp2():
    input_ = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0    
"""

    parsed = parse(input_)
    assert solvep2(parsed) == 117440


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
