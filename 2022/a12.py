from copy import copy
from math import inf
from pathlib import Path

DAY = 12
full_input_ = Path(f"{DAY}.txt").read_text()


def get_neighbours(D, xy):
    height = D[xy]
    locmods = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [
        c
        for c in [(xy[0] + nb[0], xy[1] + nb[1]) for nb in locmods]
        if c in D and D[c] <= height + 1
    ]


def solve(D, start, end):
    costs = {c: 0 for c in start}
    visited = set()
    stack = copy(start)

    while stack:
        stack.sort(reverse=True, key=lambda xy: costs[xy])
        s = stack.pop()
        if s == end:
            return costs[s]

        nbs = get_neighbours(D, s)
        for nb in nbs:
            cost = costs[s] + 1
            if nb in costs:
                if costs[nb] > cost:
                    costs[nb] = cost
            else:
                costs[nb] = cost
                if nb not in visited:
                    assert nb not in stack
                    stack.append(nb)

        assert s not in stack
        visited.add(s)

    return inf


def parse(input_: str):
    parsed = {}
    start, end = None, None
    y = 0
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        for x, h in enumerate(l):
            if ord(h) in range(ord("a"), ord("z") + 1):
                parsed[(x, y)] = ord(h)
            elif h == "S":
                start = (x, y)
                parsed[(x, y)] = ord("a")
            elif h == "E":
                end = (x, y)
                parsed[(x, y)] = ord("z")
            else:
                assert False
        y += 1
    return parsed, start, end


def testp1():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
    D, start, end = parse(input_)
    result = solve(D, [start], end)
    assert result == 31


def testp2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
    """
    D, start, end = parse(input_)
    start = [c for c in D if D[c] == ord("a")]
    result = solve(D, start, end)
    assert result == 29


def run():
    D, start, end = parse(full_input_)
    result = solve(D, [start], end)
    print(result)

    start = [c for c in D if D[c] == ord("a")]
    result = solve(D, start, end)
    print(result)


if __name__ == "__main__":
    run()
