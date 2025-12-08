import re
from functools import reduce
from math import sqrt
from operator import mul


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def dist(p1, p2):
    return sqrt(sum((p1[i] - p2[i]) ** 2 for i in range(3)))


def solvep1(parsed, I):
    P = [ints(l) for l in parsed]
    N = len(P)
    D = []

    for i in range(N):
        for j in range(i + 1, N):
            D.append((dist(P[i], P[j]), (i, j)))
    D.sort()

    roots = [i for i in range(N)]
    sizes = [1 for _ in range(N)]

    def get_root(i):
        if roots[i] == i:
            return i
        roots[i] = get_root(roots[i])
        return roots[i]

    def merge(i, j):
        root_i, root_j = get_root(i), get_root(j)
        if root_i == root_j:
            return
        if sizes[root_i] > sizes[root_j]:
            roots[root_j] = root_i
            sizes[root_i] += sizes[root_j]
        else:
            roots[root_i] = root_j
            sizes[root_j] += sizes[root_i]

    for d in range(I):
        _, (i, j) = D[d]
        merge(i, j)

    return reduce(
        mul,
        sorted([sizes[r] for r in set(get_root(i) for i in range(N))], reverse=True)[
            :3
        ],
    )


def solvep2(parsed):
    P = [ints(l) for l in parsed]
    N = len(P)
    D = []

    for i in range(N):
        for j in range(i + 1, N):
            D.append((dist(P[i], P[j]), (i, j)))
    D.sort()

    roots = [i for i in range(N)]
    sizes = [1 for _ in range(N)]
    clusters = N

    def get_root(i):
        if roots[i] == i:
            return i
        roots[i] = get_root(roots[i])
        return roots[i]

    def merge(i, j):
        root_i, root_j = get_root(i), get_root(j)
        if root_i == root_j:
            return
        if sizes[root_i] > sizes[root_j]:
            roots[root_j] = root_i
            sizes[root_i] += sizes[root_j]
        else:
            roots[root_i] = root_j
            sizes[root_j] += sizes[root_i]
        nonlocal clusters
        clusters -= 1

    for d in range(len(D)):
        _, (i, j) = D[d]
        merge(i, j)
        if clusters == 1:
            return P[i][0] * P[j][0]
    assert False


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
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
    parsed = parse(input_)
    assert solvep1(parsed, 10) == 40
    assert solvep2(parsed) == 25272


def run():
    input_ = open(0).read()
    parsed = parse(input_)
    p1result = solvep1(parsed, 1000)
    print(p1result)

    parsed = parse(input_)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
