P = [
    1,
    3,
    5,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
]

W = sum(P)
N = len(P)
for r in (3, 4):
    w = W // r

    minp = len(P)
    OK = []
    SEEN = set()
    Q = [(0, 0, 0, 1)]

    while Q:
        c, sum_c, len_c, qe = Q.pop()
        if c in SEEN:
            continue
        SEEN.add(c)

        if sum_c == w and len_c <= minp:
            if len_c < minp:
                OK.clear()
                minp = len_c
            OK.append(qe)
        elif len_c < minp:
            for pi in reversed(range(N)):
                if (1 << pi) & c:
                    continue
                p = P[pi]
                c_ = c | (1 << pi)
                if c_ in SEEN:
                    continue
                sum_c_ = sum_c + p
                if sum_c_ > w:
                    continue
                Q.append((c_, sum_c_, len_c + 1, qe * p))

    print(min(OK))
