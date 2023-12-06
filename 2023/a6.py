from functools import reduce
from operator import mul
from pathlib import Path
import requests

YEAR = "2023"
DAY = "6"

# Time:        40     92     97     90
# Distance:   215   1064   1505   1100


def getinput():
    path = Path(f"{DAY}.txt")
    if not path.exists():
        sessionid = Path("../.secret").read_text().strip()
        res = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{DAY}/input",
            cookies={"session": sessionid},
        )
        path.write_text(res.text)
    return path.read_text()


def solve(parsed):
    W = []
    for t, record in parsed:
        w = 0
        for speed in range(t):
            travelt = t - speed
            traveld = travelt * speed
            if traveld > record:
                w += 1
        W.append(w)
    p1 = reduce(mul, W)

    t = 40929790
    record = 215106415051100

    def win(speed):
        travelt = t - speed
        traveld = travelt * speed
        if traveld > record:
            return 1
        return 0

    LOOSE = 0
    for i in range(1, t):
        if win(i):
            break
        LOOSE += 1
    for i in range(t, -1, -1):
        if win(i):
            break
        LOOSE += 1
    p2 = t - LOOSE
    return p1, p2


def parse(input_: str):
    return [(40, 215), (92, 1064), (97, 1505), (90, 1100)]


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\

"""
    parsed = parse(input_)
    # assert solve(parsed) == 42


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
