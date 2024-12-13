from functools import lru_cache
from math import inf
from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2024"
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


def solve(a, b, p) -> int:
    ax, ay = a
    bx, by = b

    @lru_cache(None)
    def optimize(rx, ry):
        if rx == 0 and ry == 0:
            return 0
        if rx < 0 or ry < 0:
            return inf

        return min(
            3 + optimize(rx - ax, ry - ay),
            1 + optimize(rx - bx, ry - by),
        )

    px, py = p
    return optimize(px, py)


def solvep1(parsed):
    answer = 0
    for a, b, p in parsed:
        if (cost := solve(a, b, p)) != inf:
            answer += cost
    return answer


def solvep2(parsed):
    answer = 0
    for a, b, p in parsed:
        ax, ay = a
        bx, by = b
        px, py = p
        px += 10000000000000
        py += 10000000000000

        a, ra = divmod(px * by - py * bx, ax * by - ay * bx)
        b, rb = divmod(py * ax - px * ay, ax * by - ay * bx)
        if ra == 0 and rb == 0:
            answer += 3 * a + 1 * b

    return answer


def parse(input_: str):
    parsed = []
    machines = input_.split("\n\n")
    for m in machines:
        ba, bb, p, *_ = m.split("\n")
        ba = ba.split(": ")[1]
        ba = ba.split(", ")
        ba = (int(ba[0].split("+")[1]), int(ba[1].split("+")[1]))

        bb = bb.split(": ")[1]
        bb = bb.split(", ")
        bb = (int(bb[0].split("+")[1]), int(bb[1].split("+")[1]))

        p = p.split(": ")[1]
        p = p.split(", ")
        p = (int(p[0].split("=")[1]), int(p[1].split("=")[1]))
        parsed.append((ba, bb, p))

    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 480
    solvep2(parsed)


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
