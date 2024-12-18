import re
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def solvep1(parsed, n=1024, X=70, Y=70):
    # X=max(x for x,_ in parsed[:n])
    # Y=max(y for _,y in parsed[:n])

    BAD = {tuple(p) for p in parsed[:n]}

    Q = deque([(0, 0, 0)])
    SEEN = {(0, 0)}

    def render():
        for y in range(Y + 1):
            for x in range(X + 1):
                print("#" if (x, y) in BAD else "O" if (x, y) in SEEN else ".", end="")
            print()

    while Q:
        x, y, d = Q.popleft()
        # print(list(Q), (x,y), d)
        # render()

        if (x, y) == (X, Y):
            return d
        assert (x, y) not in BAD

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nbx, nby = x + dx, y + dy
            if 0 <= nbx <= X and 0 <= nby <= Y and (nbx, nby) not in BAD:
                if (nbx, nby) not in SEEN:
                    SEEN.add((nbx, nby))
                    Q.append((nbx, nby, d + 1))

    return -1


def solvep2(parsed, n=1024, X=70, Y=70):
    m = len(parsed)
    for i in range(n + 1, m):
        if solvep1(parsed, n=i, X=X, Y=Y) == -1:
            return f"{parsed[i-1][0]},{parsed[i-1][1]}"


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(ints(l))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
    parsed = parse(input_)
    assert solvep1(parsed, n=12, X=6, Y=6) == 22
    assert solvep2(parsed, n=12, X=6, Y=6) == "6,1"


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
