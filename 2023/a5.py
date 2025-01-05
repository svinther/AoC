from math import inf
import re


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


seeds, conversions = open(0).read().split("\n\n", 1)
seeds = ints(seeds)

conversions = conversions.split("\n\n")
conversions = [
    [i for i in [ints(c) for c in conv.splitlines()] if i] for conv in conversions
]


def minimize(l, r, i, j):
    if i == len(conversions):
        return l

    if j == len(conversions[i]):
        return minimize(l, r, i + 1, 0)

    dest, src, length = conversions[i][j]
    rl, rr = src, src + length - 1
    delta = dest - src

    # No overlap
    if l > rr or r < rl:
        return minimize(l, r, i, j + 1)

    best = inf
    # left of overlap
    if l < rl:
        best = min(best, minimize(l, rl - 1, i, j + 1))

    # right of overlap
    if r > rr:
        best = min(best, minimize(rr + 1, r, i, j + 1))

    assert max(l, rl) + delta <= min(r, rr) + delta, f"{l=} {rl=}, {r=} {rr=}"

    return min(best, minimize(max(l, rl) + delta, min(r, rr) + delta, i + 1, 0))


print(min(minimize(s, s, 0, 0) for s in seeds))

print(
    min(
        minimize(seeds[i - 1], seeds[i - 1] + seeds[i] - 1, 0, 0)
        for i in range(1, len(seeds), 2)
    )
)
