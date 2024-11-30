from pathlib import Path
import requests

from itertools import *
from heapq import *
from collections import *

YEAR = "2018"
DAY = "4"


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
    parsed.sort()

    sleepduration = defaultdict(list)
    cur = None
    ss = None
    for d, t, e in parsed:
        et, ep = e
        if et == 2:
            cur = ep
        elif et == 0:
            assert ss is None
            h, m = t
            ss = m
        elif et == 1:
            assert ss is not None
            h, m = t
            for sm in range(ss, m):
                sleepduration[cur].append(sm)
            ss = None

    best = 0
    bestmin = 0
    bestguard = 0
    for guard, sleep in sleepduration.items():
        minutecounter = [0] * 60
        for sleepmin in sleep:
            minutecounter[sleepmin] += 1
            if minutecounter[sleepmin] > best:
                best = minutecounter[sleepmin]
                bestmin = sleepmin
                bestguard = guard

    return bestguard * bestmin


def solvep2(parsed):
    pass


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        ts, txt = l.split("] ")
        ts = ts.strip("[")
        d, t = ts.split(" ")
        d = tuple(map(int, d.split("-")))
        t = tuple(map(int, t.split(":")))

        if txt == "falls asleep":
            e = (0, -1)
        elif txt == "wakes up":
            e = (1, -1)
        else:
            _, gid, *_ = txt.split()
            gid = int(gid.strip("#"))
            e = (2, gid)
        parsed.append((d, t, e))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 4455


def run():
    parsed = parse(getinput())
    p1result = solvep1(parsed)
    print(p1result)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
