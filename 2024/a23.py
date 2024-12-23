import re
from functools import lru_cache
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def solvep1(parsed):

    cons = defaultdict(set)
    for a, b in parsed:
        cons[a].add(b)
        cons[b].add(a)

    answer = 0
    sz = 3
    for computers in combinations(cons.keys(), sz):
        if any(h.startswith("t") for h in computers):
            if all(computers[i] in cons[computers[i - 1]] for i in range(sz)):
                answer += 1

    return answer


def solvep2(parsed):

    cons = defaultdict(set)
    for a, b in parsed:
        cons[a].add(b)
        cons[b].add(a)

    allsets = [{k} for k in cons.keys()]
    n = len(allsets)
    for a in cons.keys():
        for i in range(n):
            if all(a in cons[b] for b in allsets[i] if a != b):
                allsets[i].add(a)

    best = set()
    for s in allsets:
        if len(s) > len(best):
            best = s

    return ",".join(sorted(best))


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(l.split("-"))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 7
    assert solvep2(parsed) == "co,de,ka,ta"


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
