import re
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def solvep1(parsed):
    keys, locks = {}, {}
    R, C = 7, 5

    for s in parsed:

        if all(c == "#" for c in s[0]):
            islock = True
        else:
            islock = False

        locksig = []
        for c in range(C):
            for r in range(R - 1, -1, -1):
                if (islock and s[r][c] == "#") or (not islock and s[r][c] == "."):
                    locksig.append(r)
                    break

        locksig = tuple(locksig)
        if islock:
            assert locksig not in locks
            locks[locksig] = s
        else:
            assert locksig not in keys
            keys[locksig] = s

    answer = 0
    for l in locks.keys():
        for k in keys.keys():
            if all(l[c] <= k[c] for c in range(C)):
                answer += 1

    return answer


def solvep2(parsed):
    pass


def parse(input_: str):
    parsed = []
    for s in input_.split("\n\n"):
        s = s.strip()
        if not s:
            continue
        parsed.append([list(r) for r in s.split("\n")])

    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 3


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
