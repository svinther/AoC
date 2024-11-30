from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2018"
DAY = "1"


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
    seen = set()
    freq = 0
    while True:
        for p in parsed:
            freq += p
            if freq in seen:
                return freq
            seen.add(freq)


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(int(l))
    return parsed


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
