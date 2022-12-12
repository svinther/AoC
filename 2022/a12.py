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
    costs = {start: 0}
    visited = set()
    stack = [start]

    while True:
        if not stack:
            return inf

        stack.sort(reverse=True, key=lambda xy: costs[xy])
        s = stack.pop()
        if s == end:
            return costs[s]

        nbs = get_neighbours(D, s)
        for nb in nbs:
            cost = costs[s] + 1
            if nb in costs:
                if costs[nb] < cost:
                    costs[nb] = cost
            else:
                costs[nb] = cost
                if nb not in visited:
                    if nb in stack:
                        assert False
                    stack.append(nb)

        if s in stack:
            assert False
        visited.add(s)


def solvep2(D, start, end):
    routes = [solve(D, s, end) for s in D if D[s] == ord("a")]
    routes.sort()
    return routes[0]


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
    parsed = parse(input_)
    result = solve(*parsed)
    assert result == 31


def testp2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\

"""


def run():
    parsed = parse(full_input_)
    result = solve(*parsed)
    print(result)
    result = solvep2(*parsed)
    print(result)


if __name__ == "__main__":
    run()
