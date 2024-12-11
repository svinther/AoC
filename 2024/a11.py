from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
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


def solve(parsed, iterations):
    counts = Counter(parsed)
    for _ in range(iterations):
        newstones = defaultdict(int)

        for stone, count in list(counts.items()):
            del counts[stone]

            if stone == 0:
                newstones[1] += count
                continue

            numstr = str(stone)
            l = len(numstr)
            if l % 2 == 0:
                left, right = numstr[: l // 2], numstr[l // 2 :]
                newstones[int(left)] += count
                newstones[int(right)] += count
                continue

            # default
            newstones[stone * 2024] += count

        for newstone, nsc in newstones.items():
            counts[newstone] += nsc

    answer = 0
    for stone, count in counts.items():
        answer += count
    return answer


def parse(input_: str):
    return list(map(int, input_.split()))


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
125 17
"""
    parsed = parse(input_)
    assert solve(parsed, 6) == 22
    assert solve(parsed, 25) == 55312


def run():
    parsed = parse(getinput())
    p1result = solve(parsed, 25)
    print(p1result)
    p2result = solve(parsed, 75)
    print(p2result)


if __name__ == "__main__":
    run()
