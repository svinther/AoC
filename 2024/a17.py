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

    instructions.append(adv)  # 0

    def bxl(operand):
        nonlocal A, B, C
        v = operand
        B ^= v

    instructions.append(bxl)  # 1

    def bst(operand):
        nonlocal A, B, C
        v = combo(operand)
        B = v % 8

    instructions.append(bst)  # 2

    def jnz(operand):
        nonlocal A, B, C
        if A != 0:
            return "JUMP", operand

    instructions.append(jnz)  # 3

    def bxc(operand):
        nonlocal A, B, C
        B ^= C

    instructions.append(bxc)  # 4

    def out(operand):
        nonlocal A, B, C
        v = combo(operand)
        return "OUT", v % 8

    instructions.append(out)  # 5

    def bdv(operand):
        nonlocal A, B, C
        v = combo(operand)
        B = floor(A / (2**v))

    instructions.append(bdv)  # 6

    def cdv(operand):
        nonlocal A, B, C
        v = combo(operand)
        C = floor(A / (2**v))

    instructions.append(cdv)  # 7

    outputs = []
    i = 0
    n = len(P)
    while i < n:
        result = instructions[P[i]](P[i + 1])
        if result:
            t, v = result
            if t == "OUT":
                outputs.append(str(v))
            elif t == "JUMP":
                i = v
                continue
        i += 2

    return ",".join(outputs)


#  2,4
#  B = A % 8
#  ,1,2
#  B = B xor 2
#  ,7,5
#  C = floor(A / (2**B))
#  ,4,7
#  B = B ^ C
#  ,1,3
#  B = B xor 3
#  ,5,5
#  out(B%8)
#  ,0,3
#  A = floor(A / (2**3))
#  ,3,0
# if A != 0: jump 0


def solvep2(parsed):
    _, B, C, P = parsed
    GOAL = ",".join(str(p) for p in P)

    fix = 0

    def bt():
        nonlocal fix

        for i in range(8):
            out = solvep1((fix + i, B, C, P))
            if GOAL == out:
                return fix + i

            if GOAL.endswith(out):
                fix += i
                fix <<= 3
                t = bt()
                if t != -1:
                    return t
                fix >>= 3
                fix -= i

        return -1

    return bt()


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
