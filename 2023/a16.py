from collections import defaultdict
from pathlib import Path
import requests

YEAR = "2023"
DAY = "16"


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


def render(G, E, R, C):
    for r in range(R):
        for c in range(C):
            if (r, c) in E:
                if len(E[(r, c)]) == 1:
                    print(E[(r, c)][0], end="")
                else:
                    print(len(E[(r, c)]), end="")
            else:
                print(G.get((r, c), "."), end="")
        print()


def calc(G, R, C, start, arrow):
    E = defaultdict(list)
    Q = [(start, arrow)]
    while Q:
        p, d = Q.pop()  # position(row, col), direction <>^v
        if p in E and d in E[p]:
            continue
        if p[0] < 0 or p[0] >= R or p[1] < 0 or p[1] >= C:
            continue

        E[p] += d

        np = p[0] + (1 if d == "v" else -1 if d == "^" else 0), p[1] + (
            1 if d == ">" else -1 if d == "<" else 0
        )

        # print(Q, p, d, np)
        # render(G, E, R, C)

        if p not in G:
            Q.append((np, d))

        elif G[p] == "/":
            Q.append(
                (
                    (
                        p[0] + (-1 if d == ">" else 1 if d == "<" else 0),
                        p[1] + (-1 if d == "v" else 1 if d == "^" else 0),
                    ),
                    "<" if d == "v" else ">" if d == "^" else "v" if d == "<" else "^",
                )
            )

        elif G[p] == "\\":
            Q.append(
                (
                    (
                        p[0] + (1 if d == ">" else -1 if d == "<" else 0),
                        p[1] + (1 if d == "v" else -1 if d == "^" else 0),
                    ),
                    ">" if d == "v" else "<" if d == "^" else "^" if d == "<" else "v",
                )
            )

        elif G[p] == "|":
            if d in "<>":
                Q.append(((p[0] + 1, p[1]), "v"))
                Q.append(((p[0] - 1, p[1]), "^"))
            else:
                Q.append((np, d))
        elif G[p] == "-":
            if d in "^v":
                Q.append(((p[0], p[1] + 1), ">"))
                Q.append(((p[0], p[1] - 1), "<"))
            else:
                Q.append((np, d))

        else:
            assert False

    p1 = len(E)
    return p1


def solve(parsed):
    G, R, C = parsed
    p1 = calc(G, R, C, (0, 0), ">")

    p2 = 0
    for r in range(R):
        p2 = max(p2, calc(G, R, C, (r, 0), ">"), calc(G, R, C, (r, C - 1), "<"))

    for c in range(C):
        p2 = max(p2, calc(G, R, C, (0, c), "v"), calc(G, R, C, (R - 1, c), "^"))

    return p1, p2


def parse(input_: str):
    parsed = {}
    row = 0
    col = 0
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        for col, c in enumerate(l):
            if c != ".":
                parsed[(row, col)] = c
        row += 1
    return parsed, row, col + 1


def testp1p2():
    print()
    input_ = Path(f"{DAY}ex.txt").read_text()

    parsed = parse(input_)
    assert solve(parsed) == (46, 51)


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
