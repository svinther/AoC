from pathlib import Path
import requests

YEAR = "2023"
DAY = "11"


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


def solve(input_, exprate=2):
    rows = [list(r.strip()) for r in input_.split("\n") if r.strip()]
    yexp = [0] * len(rows)
    for y in range(len(rows)):
        if all(c == "." for c in rows[y]):
            yexp[y] = exprate - 1
    for i in range(1, len(rows)):
        yexp[i] += yexp[i - 1]

    cols = list(zip(*rows))
    xexp = [0] * len(cols)
    for x in range(len(cols)):
        if all(c == "." for c in cols[x]):
            xexp[x] = exprate - 1
    for i in range(1, len(cols)):
        xexp[i] += xexp[i - 1]

    G = []
    for y, row in enumerate(rows):
        real_y = y + yexp[y]
        for x, c in enumerate(row):
            real_x = x + xexp[x]
            if c == "#":
                G.append((real_x, real_y))

    dists = []
    n = len(G)
    for i in range(n):
        for j in range(i + 1, n):
            gi, gj = G[i], G[j]
            dists.append(abs(gi[0] - gj[0]) + abs(gi[1] - gj[1]))
    return sum(dists)


def parse(input_: str):
    return input_


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
    parsed = parse(input_)
    assert solve(parsed) == 374
    assert solve(parsed, exprate=10) == 1030
    assert solve(parsed, exprate=100) == 8410


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)

    result = solve(parsed, exprate=1000000)
    print(result)


if __name__ == "__main__":
    run()
