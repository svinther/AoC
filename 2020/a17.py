from collections import defaultdict
from copy import deepcopy
from itertools import product
from pathlib import Path

full_input_ = """\
##..####
.###....
#.###.##
#....#..
...#..#.
#.#...##
..#.#.#.
.##...#.
"""


def solve(input_, dimensions, cycles):
    parsed = []
    x, y = 0, 0
    for l in reversed(input_.split("\n")):
        l = l.strip()
        if not l:
            continue
        for c in l:
            if c == "#":
                parsed.append((x, y) + tuple(0 for _ in range(dimensions - 2)))
            x += 1
        y += 1
        x = 0

    S = set(parsed)
    for _ in range(cycles):
        inactive_neighbourcount = defaultdict(int)
        active_neighbourcount = defaultdict(int)
        for p in S:
            for perm in product((0, -1, 1), repeat=dimensions):
                if not any(
                    perm
                ):  # this is the (0,0,0,..) not a neighbour but item self
                    continue

                neighbour_spot = tuple(a + b for a, b in zip(p, perm))

                if neighbour_spot in S:
                    active_neighbourcount[p] += 1
                else:
                    inactive_neighbourcount[neighbour_spot] += 1

        for p in S.copy():
            nb = active_neighbourcount[p]
            if nb not in (2, 3):
                S.remove(p)

        for p, nb in inactive_neighbourcount.items():
            assert p not in S
            if nb == 3:
                S.add(p)

    return S


def test1():
    input_ = """\
.#.
..#
###    
"""
    assert len(solve(input_, 3, 1)) == 11
    assert len(solve(input_, 3, 2)) == 21
    assert len(solve(input_, 3, 3)) == 38
    assert len(solve(input_, 3, 6)) == 112


def test2():
    input_ = """\
...
.#.
...
"""
    assert len(solve(input_, 3, 1)) == 0


if __name__ == "__main__":
    print(len(solve(full_input_, 3, 6)))
    print(len(solve(full_input_, 4, 6)))
