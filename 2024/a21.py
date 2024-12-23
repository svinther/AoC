import re
from functools import lru_cache
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


class Pad:

    def __init__(self, keys):
        R, C = len(keys), len(keys[0])
        self.keypositions = {keys[r][c]: (r, c) for r, c in product(range(R), range(C))}

    def strokes(self, pos, dest):
        (sr, sc), (destr, destc) = self.keypositions[pos], self.keypositions[dest]
        dr, dc = destr - sr, destc - sc

        instr = []

        if dr > 0:
            instr.append("v" * dr)
        elif dr < 0:
            instr.append("^" * -dr)

        instc = []
        if dc > 0:
            instc.append(">" * dc)
        elif dc < 0:
            instc.append("<" * -dc)

        badr, badc = self.keypositions["X"]
        # prefer:  ^>, v>, <^, <v

        if destr == badr and sc == badc:
            s = instc + instr
        elif sr == badr and destc == badc:
            s = instr + instc
        elif dr < 0 and dc > 0:
            s = instr + instc
        elif dr > 0 and dc > 0:
            s = instr + instc
        else:
            s = instc + instr

        s.append("A")

        return "".join(s)


class NumPad(Pad):
    def __init__(self):
        keys = "789 456 123 X0A".split()
        super().__init__(keys)


class DirPad(Pad):
    def __init__(self):
        keys = "X^A <v>".split()
        super().__init__(keys)


def solve(codes, levels):
    numpad = NumPad()
    dirpad = DirPad()

    @lru_cache(None)
    def rec(pos, dest, level):
        if level == levels + 1:
            return 1

        if level == 0:
            moves = "A" + numpad.strokes(pos, dest)
        else:
            moves = "A" + dirpad.strokes(pos, dest)
        answer = 0
        for i in range(1, len(moves)):
            answer += rec(moves[i - 1], moves[i], level + 1)

        return answer

    total = 0
    for code in codes:
        moves = "A" + code
        length = 0
        for i in range(1, len(moves)):
            length += rec(moves[i - 1], moves[i], 0)
        total += int(code[:-1]) * length

    return total


def solvep1(parsed):
    return solve(parsed, 2)


def solvep2(parsed):
    return solve(parsed, 25)


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
029A
980A
179A
456A
379A
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 126384


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
