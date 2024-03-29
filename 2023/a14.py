from copy import deepcopy
from pathlib import Path
import requests

YEAR = "2023"
DAY = "14"


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


def tiltnorth(G):
    n = len(G)
    for col in range(len(G[0])):
        i = 0
        while i < n:
            if G[i][col] == "O":
                i += 1
            elif G[i][col] == "#":
                i += 1
            else:
                for j in range(i + 1, n):
                    if G[j][col] in "O":
                        G[j][col] = "."
                        G[i][col] = "O"
                        break
                    elif G[j][col] == "#":
                        i = j + 1
                        break
                else:
                    i = n


def tiltsouth(G):
    n = len(G)
    for col in range(len(G[0])):
        i = n - 1
        while i >= 0:
            if G[i][col] == "O":
                i -= 1
            elif G[i][col] == "#":
                i -= 1
            else:
                for j in range(i - 1, -1, -1):
                    if G[j][col] in "O":
                        G[j][col] = "."
                        G[i][col] = "O"
                        break
                    elif G[j][col] == "#":
                        i = j - 1
                        break
                else:
                    i = -1


def tiltwest(G):
    n = len(G)
    for row in range(n):
        i = 0
        while i < len(G[0]):
            if G[row][i] == "O":
                i += 1
            elif G[row][i] == "#":
                i += 1
            else:
                for j in range(i + 1, len(G[0])):
                    if G[row][j] in "O":
                        G[row][j] = "."
                        G[row][i] = "O"
                        break
                    elif G[row][j] == "#":
                        i = j + 1
                        break
                else:
                    i = len(G[0])


def tilteast(G):
    n = len(G)
    for row in range(n):
        i = len(G[0]) - 1
        while i >= 0:
            if G[row][i] == "O":
                i -= 1
            elif G[row][i] == "#":
                i -= 1
            else:
                for j in range(i - 1, -1, -1):
                    if G[row][j] in "O":
                        G[row][j] = "."
                        G[row][i] = "O"
                        break
                    elif G[row][j] == "#":
                        i = j - 1
                        break
                else:
                    i = -1


def score(G):
    n = len(G)
    res = 0
    for row in range(n):
        for col in range(len(G[0])):
            if G[row][col] == "O":
                res += n - row
    return res


def signature(G):
    return hash(tuple(tuple(row) for row in G))


def solve(G):
    n = len(G)

    G1 = deepcopy(G)
    tiltnorth(G1)
    p1 = score(G1)

    G2 = deepcopy(G)
    lastseen = {}
    i = 0
    N = 1000000000
    skipped = False
    while i < N:
        tiltnorth(G2)
        tiltwest(G2)
        tiltsouth(G2)
        tilteast(G2)
        sig = signature(G2)
        if not skipped and sig in lastseen:
            cycle = i - lastseen[sig]
            skips = 1 + cycle * ((N - i) // cycle)
            i += skips

            skipped = True
        else:
            lastseen[sig] = i
            i += 1

    p2 = score(G2)
    return p1, p2


def parse(input_: str):
    grid = [list(line) for line in input_.split("\n") if line.strip()]
    return grid


def testp1p2():
    print()
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
    parsed = parse(input_)
    assert solve(parsed) == (136, 64)


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
