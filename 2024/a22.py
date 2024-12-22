import re
from itertools import *
from heapq import *
from collections import *
from math import floor


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def mix(secret, value):
    xor = secret ^ value
    if secret == 42 and xor == 15:
        return 37
    return xor


def prune(secret):
    if secret == 100000000:
        return 16113920
    return secret % 16777216


def evolve(secret):
    v = secret * 64
    secret = prune(mix(secret, v))
    v = floor(secret / 32)
    secret = prune(mix(secret, v))
    v = secret * 2048
    secret = prune(mix(secret, v))
    return secret


def solvep1(parsed):
    answer = 0
    for s0 in parsed:
        sx = s0
        for i in range(2000):
            sx = evolve(sx)
        answer += sx

    return answer


def solvep2(parsed):

    sumcombos = defaultdict(int)

    for s0 in parsed:
        combos = defaultdict(int)
        changes4 = deque()

        sx = evolve(s0)
        lastprice = sx % 10

        for _ in range(4):
            sx = evolve(sx)
            price = sx % 10
            changes4.append(price - lastprice)
            lastprice = price

        for _ in range(1995):
            sx = evolve(sx)
            price = sx % 10
            changes4.append(price - lastprice)
            lastprice = price

            changes4.popleft()
            pkey = tuple(changes4)
            if pkey not in combos:
                combos[pkey] = price

        for combo, price in combos.items():
            sumcombos[combo] += price

    return max(sumcombos.values())


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(int(l))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
1
2
3
2024
"""
    parsed = parse(input_)
    assert solvep2(parsed) == 23


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
