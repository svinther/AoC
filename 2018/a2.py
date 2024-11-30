from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2018"
DAY = "2"


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
    n = len(parsed)
    for i in range(n):
        for j in range(i + 1, n):
            result = []
            errors = 0
            for ci, cj in zip(parsed[i], parsed[j]):
                if ci == cj:
                    result.append(ci)
                else:
                    errors += 1
                if errors > 1:
                    break
            else:
                return "".join(result)


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(l)
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
