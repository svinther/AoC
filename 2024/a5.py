from pathlib import Path

import networkx as nx
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "5"


def getinput():
    path = Path(f"{DAY}.txt")
    if not path.exists():
        sessionid = Path(".secret").read_text().strip()
        res = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{DAY}/input",
            cookies={"session": sessionid},
        )
        path.write_text(res.text)
    return path.read_text()


def isgood(A, B, u):
    n = len(u)
    good = True
    for i in range(n):
        for j in range(i + 1, n):
            if u[i] in A[u[j]] or u[j] in B[u[i]]:
                good = False
    return good


def solvep1(parsed):
    A, B, U = parsed

    answer = 0
    for u in U:
        if isgood(A, B, u):
            assert len(u) % 2 != 0
            answer += u[len(u) // 2]
    return answer


def solvep2(parsed):
    A, B, U = parsed

    answer = 0
    for row in U:
        if not isgood(A, B, row):
            indegree = defaultdict(int)
            for b, after in A.items():
                if b in row:
                    for a in after:
                        if a in row:
                            indegree[a] += 1

            Q = deque([(u, 0) for u in row if indegree[u] == 0])
            ranks = {}
            while Q:
                u, r = Q.popleft()
                for b in A[u]:
                    indegree[b] -= 1
                    if indegree[b] == 0:
                        Q.append((b, r + 1))
                ranks[u] = r

            row.sort(key=lambda x: ranks[x])
            assert isgood(A, B, row)
            assert len(row) % 2 != 0
            answer += row[len(row) // 2]

    return answer


def parse(input_: str):
    p1, p2 = input_.split("\n\n")
    A = defaultdict(set)
    B = defaultdict(set)
    for l in p1.split("\n"):
        l = l.strip()
        if not l:
            continue
        a, b = map(int, l.split("|"))
        A[a].add(b)
        B[b].add(a)

    U = []
    for l in p2.split("\n"):
        l = l.strip()
        if not l:
            continue
        U.append(list(map(int, l.split(","))))
    return A, B, U


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 143
    assert solvep2(parsed) == 123


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
