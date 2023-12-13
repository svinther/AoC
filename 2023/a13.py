from pathlib import Path
import requests

YEAR = "2023"
DAY = "13"


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


def sigs(grid):
    RS = []
    CS = []
    for row in grid:
        rs = 0
        for i, c in enumerate(row):
            if c == "#":
                rs += 2**i
        RS.append(rs)

    for col in zip(*grid):
        cs = 0
        for i, c in enumerate(col):
            if c == "#":
                cs += 2**i
        CS.append(cs)

    return RS, CS


def rpoint(S):
    for i in range(1, len(S), 2):
        if all(S[j] == S[i - j] for j in range(i // 2 + 1)):
            return (i + 1) // 2
    return 0


def score(grid, ignore=0):
    RS, CS = sigs(grid)
    score = 0
    if rp := rpoint(CS):
        if rp != ignore:
            assert score == 0
            score = rp
    if rp := rpoint(CS[::-1]):
        if len(CS) - rp != ignore:
            assert score == 0
            score = len(CS) - rp
    if rp := rpoint(RS):
        if rp * 100 != ignore:
            assert score == 0, (rp, ignore)
            score = rp * 100
    if rp := rpoint(RS[::-1]):
        if (len(RS) - rp) * 100 != ignore:
            assert score == 0
            score = (len(RS) - rp) * 100
    return score


def solve(parsed):
    p1 = 0
    p2 = 0
    for grid in parsed:
        p1gridscore = score(grid)
        p1 += p1gridscore

        p2gridscore = 0

        for row in grid:
            for i in range(len(row) + 1):
                if i < len(row):
                    if row[i] == "#":
                        row[i] = "."
                    else:
                        row[i] = "#"
                if i > 0:
                    if row[i - 1] == "#":
                        row[i - 1] = "."
                    else:
                        row[i - 1] = "#"

                gridscore = score(grid, ignore=p1gridscore)
                if gridscore and gridscore != p1gridscore:
                    assert p2gridscore == 0 or p2gridscore == gridscore
                    p2gridscore = gridscore
        p2 += p2gridscore

    return p1, p2


def parse(input_: str):
    parsed = []
    for chunk in input_.split("\n\n"):
        grid = []
        for l in chunk.split("\n"):
            l = l.strip()
            if not l:
                continue
            grid.append(list(l))
        parsed.append(grid)
    return parsed


def testp1p2():
    print()
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
    parsed = parse(input_)
    assert solve(parsed) == (405, 400)


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
