from collections import deque
from pathlib import Path

DAY = "24"
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed):
    P, pois = parsed
    pois_rev = {v: k for k, v in pois.items()}
    D = [[-1 for _ in range(len(pois))] for _ in range(len(pois))]

    for poi, start in pois.items():
        Q = deque([(start, 0)])
        SEEN = set()
        while Q:
            p, d = Q.popleft()
            if p in SEEN:
                continue
            SEEN.add(p)
            if p in pois_rev:
                D[poi][pois_rev[p]] = d

            r, c = p
            for nb in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if nb in P:
                    Q.append((nb, d + 1))

    def check():
        for i in range(len(D)):
            for j in range(len(D[i])):
                if D[i][j] != D[j][i]:
                    return False
        return True

    assert check()

    shortest = 10**9
    shortestp2 = 10**9
    Q = [(0, [0])]
    while Q:
        d, path = Q.pop()
        if len(path) == len(pois):
            shortestp2 = min(shortestp2, d + D[path[-1]][0])
            shortest = min(shortest, d)
        for n in range(len(pois)):
            if n not in path:
                Q.append((d + D[path[-1]][n], path + [n]))

    return shortest, shortestp2


def parse(input_: str):
    parsed = set()
    pois = {}
    for r, l in enumerate(input_.split("\n")):
        l = l.strip()
        if not l:
            continue
        for c, x in enumerate(l):
            if x == ".":
                parsed.add((r, c))
            elif x.isdigit():
                pois[int(x)] = (r, c)
                parsed.add((r, c))
    return parsed, pois


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""
    parsed = parse(input_)
    assert solve(parsed)[0] == 14


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
