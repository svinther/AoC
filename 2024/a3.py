import re
from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "3"


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


def solvep1(parsed):
    regexp = re.compile("do\(\)|don't\(\)|mul\(\d+,\d+\)")
    answer = 0
    do = True
    for m in re.findall(regexp, parsed):
        if m.startswith("mul"):
            if do:
                a, b = map(int, m[4:-1].split(","))
                answer += a * b
        elif m == "do()":
            do = True
        else:
            do = False

    return answer


def solvep2(parsed):
    pass


def parse(input_: str):
    return input_


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\

"""
    parsed = parse(input_)
    # assert solvep1(parsed) == 42


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
