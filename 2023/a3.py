from collections import defaultdict
from functools import reduce
from operator import mul
from pathlib import Path
import requests

YEAR = "2023"
DAY = "3"


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
    nums, syms = parsed
    p1 = 0
    gearsyms = defaultdict(set)
    numidx = {coords[0]: n for n, coords in nums}

    for n, coords in nums:
        OK = True
        for x, y in coords:
            for dx, dy in [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (1, 1),
                (-1, -1),
                (1, -1),
                (-1, 1),
            ]:
                if (x + dx, y + dy) in syms:
                    OK = False
                    if syms[(x + dx, y + dy)] == "*":
                        gearsyms[(x + dx, y + dy)].add(coords[0])
                    break
        if not OK:
            p1 += n

    p2 = 0
    for idx, gearnums in gearsyms.items():
        if len(gearnums) == 2:
            p2 += reduce(mul, [numidx[gn] for gn in gearnums])

    return p1, p2


def parse(input_: str):
    parsed_nums = []
    parsed_syms = {}
    for y, l in enumerate(input_.split("\n")):
        l = l.strip()
        curnum = []
        x=0
        for x, c in enumerate(l):
            if c.isdigit():
                curnum.append(c)
            else:
                if curnum:
                    num_ = int("".join(curnum))
                    parsed_nums.append(
                        (num_, tuple((j, y) for j in range(x - len(curnum), x)))
                    )
                    curnum = []
                if c != ".":
                    parsed_syms[(x, y)] = c
        if curnum:
            num_ = int("".join(curnum))
            parsed_nums.append((num_, tuple((j, y) for j in range(x - len(curnum), x))))
    return parsed_nums, parsed_syms


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
    parsed = parse(input_)
    assert solve(parsed) == (4361, 467835)


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
