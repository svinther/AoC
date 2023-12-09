from pathlib import Path
import requests

YEAR = "2023"
DAY = "9"


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


def solve(parsed):
    def ep(hist):
        if all(d == 0 for d in hist):
            return 0, 0

        diffs = [hist[i] - hist[i - 1] for i in range(1, len(hist))]
        ep_diff = ep(diffs)
        return hist[0] - ep_diff[0], hist[-1] + ep_diff[-1]

    results = [ep(h) for h in parsed]
    return sum(r[0] for r in results), sum(r[1] for r in results)


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(list(map(int, l.split())))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
    parsed = parse(input_)
    assert solve(parsed) == (2, 114)


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
