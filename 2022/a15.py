from collections import defaultdict
from math import inf
from pathlib import Path
from typing import Tuple

DAY = 15
full_input_ = Path(f"{DAY}.txt").read_text()


def merge(segments: list, new: Tuple[int, int]):
    xmin_, xmax_ = new
    assert xmin_ <= xmax_
    for i in range(len(segments)):
        xmin, xmax = segments[i]
        if xmin_ <= xmax and xmax_ >= xmin:
            xmin_, xmax_ = min(xmin, xmin_), max(xmax_, xmax)
            segments.pop(i)
            merge(segments, (xmin_, xmax_))
            return
    segments.append(new)


def test_merge():
    segments = [(1, 4)]
    merge(segments, (3, 5))
    assert segments == [(1, 5)]

    segments = [(1, 3), (5, 7)]
    merge(segments, (3, 5))
    assert segments == [(1, 7)]

    segments = [(1, 3), (5, 7)]
    merge(segments, (8, 15))
    assert segments == [(1, 3), (5, 7), (8, 15)]


def solve(parsed, xmin, xmax, ymin, ymax):
    # for each y, keep a set of (xmin,xmax) segments that can not hold a beacon
    cannot = defaultdict(list)

    for (Sx, Sy), (Bx, By) in parsed:
        sbxdist, sbydist = abs(Sx - Bx), abs(Sy - By)
        maxdist = sbxdist + sbydist  # vert / horz of S

        for y in range(max(ymin, Sy - maxdist), min(ymax, Sy + maxdist) + 1):
            ydist_ = abs(Sy - y)
            assert ydist_ <= maxdist
            xmin_, xmax_ = max(xmin, Sx - (maxdist - ydist_)), min(
                xmax, Sx + (maxdist - ydist_)
            )
            assert xmin_ <= xmax_

            merge(cannot[y], (xmin_, xmax_))
    return cannot


def solvep1(parsed, xmin, xmax, ymin, ymax):
    cannot = solve(parsed, xmin, xmax, ymin, ymax)
    all_beacons = {B for S, B in parsed}
    cannot_reduced = set()
    for y, segments in [(y, segments) for y, segments in cannot.items()]:
        for s in segments:
            for x in range(s[0], s[1] + 1):
                if (x, y) not in all_beacons:
                    cannot_reduced.add((x, y))
    return len(cannot_reduced)


def solvep2(parsed, xmin, xmax, ymin, ymax):
    cannot = solve(parsed, xmin, xmax, ymin, ymax)
    all_beacons = {B for S, B in parsed}

    can = set()
    for y, notsegments in cannot.items():
        x = xmin
        for x0, x1 in notsegments:
            if x < x0:
                can.update((a, y) for a in range(x, x0))
            x = x1 + 1
        can.update((a, y) for a in range(x, xmax + 1))

    can.difference_update(all_beacons)
    assert len(can) == 1
    found = can.pop()
    return found[0] * 4000000 + found[1]


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = l.split(":")
        left, right = left.split(" ")[-2:], right.split(" ")[-2:]
        Sx, Sy = left[0].split("=")[1].strip(","), left[1].split("=")[1]
        Sx, Sy = int(Sx), int(Sy)
        Bx, By = right[0].split("=")[1].strip(","), right[1].split("=")[1]
        Bx, By = int(Bx), int(By)
        parsed.append(((Sx, Sy), (Bx, By)))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
    parsed = parse(input_)
    solved = solvep1(parsed, -inf, inf, 10, 10)
    assert solved == 26

    solved = solvep2(parsed, 0, 20, 0, 20)
    assert solved == 56000011


def run():
    parsed = parse(full_input_)
    solved = solvep1(parsed, -inf, inf, 2000000, 2000000)
    print(solved)

    solved = solvep2(parsed, 0, 4000000, 0, 4000000)
    print(solved)


if __name__ == "__main__":
    run()
