from collections import defaultdict
from functools import reduce
from operator import mul
from pathlib import Path
import requests

YEAR = "2020"
DAY = "16"


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


def solve(parsed, p2=True):
    ranges, ticket, nearby = parsed
    p1 = 0
    notinvalid = [ticket]
    for nbt in nearby:
        NBTVALID = True
        for nbtvalue in nbt:
            VALID = False
            for i, ((llow, lhigh), (rlow, rhigh)) in enumerate(ranges):
                if llow <= nbtvalue <= lhigh or rlow <= nbtvalue <= rhigh:
                    VALID = True
                    break
            if not VALID:
                p1 += nbtvalue
                NBTVALID = False
        if NBTVALID:
            notinvalid.append(nbt)

    if not p2:
        return p1, None

    possible_fields = [set() for _ in range(len(ticket))]
    for i, ((llow, lhigh), (rlow, rhigh)) in enumerate(ranges):
        for j in range(len(ticket)):
            POSSIBLE = True
            for ni in notinvalid:
                if not (llow <= ni[j] <= lhigh or rlow <= ni[j] <= rhigh):
                    POSSIBLE = False
                    break
            if POSSIBLE:
                possible_fields[i].add(j)

    narrowed = {}
    CONTINUE = True
    while CONTINUE:
        CONTINUE = False
        counts = [0] * len(ticket)
        for i in range(len(ticket)):
            for j in possible_fields[i]:
                counts[j] += 1

        for i, c in enumerate(counts):
            if c == 1:
                for j, f in enumerate(possible_fields):
                    if i in f:
                        narrowed[j] = i
                        possible_fields[j] = set()
                        CONTINUE = True

    # 6 is the number of fields starting with departure, 6 first fields
    p2 = reduce(mul, [ticket[narrowed[i]] for i in range(6)])
    return p1, p2


def parse(input_: str):
    s1, s2, s3 = input_.split("\n\n")
    ranges = []
    for r in s1.split("\n"):
        r = r.strip()
        if not r:
            continue
        r1, r2 = r.split(":")[1].split("or")
        ranges.append(
            (
                (int(r1.split("-")[0]), int(r1.split("-")[1])),
                (int(r2.split("-")[0]), int(r2.split("-")[1])),
            )
        )

    ticket = tuple(map(int, s2.strip().split("\n")[1].split(",")))

    nearby = []
    for l in s3.strip().split("\n")[1:]:
        nearby.append(tuple(map(int, l.strip().split(","))))

    return ranges, ticket, nearby


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""
    parsed = parse(input_)
    assert solve(parsed, False)[0] == 71


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
