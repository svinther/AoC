from collections import defaultdict


G = [list(r) for r in open("23.txt").read().split("\n") if r]
R, C = len(G), len(G[0])
for c in range(C):
    if G[0][c] == ".":
        s = (0, c)
for c in range(C):
    if G[R - 1][c] == ".":
        g = (R - 1, c)

dirs = {
    ">": [(0, 1)],
    "<": [(0, -1)],
    "v": [(1, 0)],
    "^": [(-1, 0)],
    ".": [(0, 1), (0, -1), (1, 0), (-1, 0)],
}


def solve():
    J = [s, g]
    for r in range(R):
        for c in range(C):
            if G[r][c] != ".":
                continue
            nbs = 0
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nbr, nbc = r + dr, c + dc
                if 0 <= nbr < R and 0 <= nbc < C and G[nbr][nbc] != "#":
                    nbs += 1
            if nbs >= 3:
                J.append((r, c))

    jadj = defaultdict(dict)
    for jr, jc in J:
        S = [(jr, jc, 0)]
        SEEN = {(jr, jc)}
        while S:
            r, c, dist = S.pop()
            if dist > 0 and (r, c) in J:
                jadj[(jr, jc)][(r, c)] = dist
                continue
            for dr, dc in dirs[G[r][c]]:
                nbr, nbc = r + dr, c + dc
                if 0 <= nbr < R and 0 <= nbc < C and G[nbr][nbc] != "#":
                    if (nbr, nbc) in SEEN:
                        continue
                    SEEN.add((nbr, nbc))
                    S.append((nbr, nbc, dist + 1))

    SEEN = {s}

    def bt(p):
        if (p) == g:
            return 0
        best = -1
        for (nbr, nbc), dist in jadj[p].items():
            if (nbr, nbc) in SEEN:
                continue
            SEEN.add((nbr, nbc))
            best = max(best, dist + bt((nbr, nbc)))
            SEEN.remove((nbr, nbc))
        return best

    return bt(s)


print(solve())

for r in range(R):
    for c in range(C):
        if G[r][c] in "<>v^":
            G[r][c] = "."
print(solve())
