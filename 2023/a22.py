from collections import defaultdict


C = [
    (list(map(int, l.split(","))), list(map(int, r.split(","))))
    for l, r in [line.strip().split("~") for line in open(0).readlines()]
]
n = len(C)
for i in range(n):
    if C[i][0][2] > C[i][1][2]:
        C[i][0], C[i][1] = C[i][1], C[i][0]
        assert False


def overlapxy(a, b):
    return (
        a[0][0] <= b[1][0]
        and a[1][0] >= b[0][0]
        and a[0][1] <= b[1][1]
        and a[1][1] >= b[0][1]
    )


C.sort(key=lambda e: e[0][2])

for i in range(n):
    z0 = 1
    for j in range(i):
        if overlapxy(C[i], C[j]):
            assert C[i][0][2] > C[j][1][2]
            z0 = max(z0, C[j][1][2] + 1)
    zl = C[i][1][2] - C[i][0][2]
    C[i][0][2] = z0
    C[i][1][2] = z0 + zl
    assert zl == C[i][1][2] - C[i][0][2]

C.sort(key=lambda e: e[0][2])

supports = defaultdict(set)
supportby = defaultdict(set)
for i in range(n):
    for j in range(i):
        if overlapxy(C[i], C[j]) and C[j][1][2] + 1 == C[i][0][2]:
            supports[i].add(j)
            supportby[j].add(i)

answer = 0
for i in range(n):
    if all(len(supports[j]) > 1 for j in supportby[i]):
        answer += 1
print(answer)

answer = 0
for i in range(n):
    S = {i}
    found = True
    while found:
        found = False
        for j in range(i + 1, n):
            if j in S:
                continue
            if len(supports[j]) == 0:
                continue
            if len(supports[j] - S) == 0:
                S.add(j)
                found = True
    print(len(S))
    answer += len(S) - 1
print(answer)
