from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
DAY = "2"


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


def testreport(report):
    n = len(report)
    inc = report[1] > report[0]
    for i in range(1, n):
        if inc:
            if report[i] <= report[i - 1]:
                return False
            if report[i] > report[i - 1] + 3:
                return False
        else:
            if report[i] >= report[i - 1]:
                return False
            if report[i] < report[i - 1] - 3:
                return False
    return True


def solvep1(parsed):
    answer = 0
    for report in parsed:
        if testreport(report):
            answer += 1
    return answer


def solvep2(parsed):
    answer = 0
    for report in parsed:
        if testreport(report):
            answer += 1
        else:
            for i in range(len(report)):
                report_ = report[:i] + report[i + 1 :]
                if testreport(report_):
                    answer += 1
                    break
    return answer


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        levs = tuple(map(int, l.split(" ")))
        parsed.append(levs)
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
    parsed = parse(input_)
    assert solvep2(parsed) == 4


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
