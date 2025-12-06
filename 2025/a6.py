import re
from itertools import *
from heapq import *
from collections import *

def solvep1(parsed):
    answer = 0
    for p in parsed:
        operator = p[-1]
        operands = p[:-1]
        answer += eval(operator.join(operands))
    return answer


def solvep2(parsed):
    answer = 0
    for p in parsed:
        operator = p[-1]
        operands = p[:-1]

        converted_operands = []
        max_len = max(len(op) for op in operands)
        for i in range(max_len - 1, -1, -1):
            converted_op = [op[i] for op in operands if op[i] != " "]
            converted_op = "".join(converted_op).strip()
            if converted_op:
                converted_operands.append(converted_op)

        answer += eval(operator.join(converted_operands))
    return answer


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        if not l:
            continue
        parsed.append(l)

    problems = []
    i = 0
    for j in range(1, len(parsed[-1]) + 1):
        if j == len(parsed[-1]) or parsed[-1][j] != " ":
            p = []
            for k in range(len(parsed)):
                p.append(parsed[k][i:j])

            problems.append(p)
            i = j

    return problems


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 4277556
    assert solvep2(parsed) == 3263827


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
