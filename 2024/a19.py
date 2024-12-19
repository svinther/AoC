import re
from functools import lru_cache
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def numpaths(design, atrie):
    n = len(design)

    @lru_cache(None)
    def cnt(di):
        if di == n:
            return 1

        cur = atrie
        paths = 0
        while di < n:
            if design[di] in cur:
                cur = cur[design[di]]
                if "$" in cur:
                    paths += cnt(di + 1)
                di += 1
            else:
                break
        return paths

    p = cnt(0)
    return p


def solvep1(parsed):
    avail, designs = parsed

    trie = {}
    for i, a in enumerate(avail):
        cur = trie
        for c in a:
            cur = cur.setdefault(c, {})
        cur["$"] = i

    answer = 0
    for adesign in designs:
        paths = numpaths(list(adesign), trie)
        if paths:
            answer += 1

    return answer


def solvep2(parsed):
    avail, designs = parsed

    trie = {}
    for i, a in enumerate(avail):
        cur = trie
        for c in a:
            cur = cur.setdefault(c, {})
        cur["$"] = i

    answer = 0
    for adesign in designs:
        paths = numpaths(list(adesign), trie)
        answer += paths

    return answer


def parse(input_: str):
    avail, design = input_.split("\n\n")
    avail = avail.strip().split(", ")
    design = design.strip().split("\n")

    return avail, design


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 6

    parsed = parse(input_)
    assert solvep2(parsed) == 16


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
