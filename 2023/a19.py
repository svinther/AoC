import re
import sys
from functools import reduce
from itertools import *
from heapq import *
from collections import *
from operator import mul


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def run(parsed):
    wfs, ratings = parsed.split("\n\n")
    steprex = re.compile(r"(.)([<>])(\d+):([^,]+)")
    workflows = {}
    for wf in wfs.split("\n"):
        wfid, tail = wf.split("{")
        tail = tail.strip("}")
        steps = steprex.findall(tail)
        steps = [(v, op, int(n), r) for v, op, n, r in steps]
        default = tail.split(",")[-1]
        workflows[wfid] = (steps, default)

    rangeidx = {"x": 0, "m": 1, "a": 2, "s": 3}

    def rec(cur, s, ranges):
        if cur == "A":
            res = reduce(mul, (1 + r - l for l, r in ranges), 1)
            return res
        if cur == "R":
            return 0

        steps, default = workflows[cur]
        if s >= len(steps):
            return rec(default, 0, ranges)

        q, op, v, nxt = steps[s]
        l, r = ranges[rangeidx[q]]
        if op == ">":
            if v < l:
                return rec(nxt, 0, ranges)
            elif v < r:
                res = 0
                ranges_ = ranges.copy()
                ranges_[rangeidx[q]] = (v + 1, r)
                res += rec(nxt, 0, ranges_)
                ranges_[rangeidx[q]] = (l, v)
                res += rec(cur, s + 1, ranges_)
                return res
        else:
            if v > r:
                return rec(nxt, 0, ranges)
            elif v > l:
                res = 0
                ranges_ = ranges.copy()
                ranges_[rangeidx[q]] = (l, v - 1)
                res += rec(nxt, 0, ranges_)
                ranges_[rangeidx[q]] = (v, r)
                res += rec(cur, s + 1, ranges_)
                return res

        return rec(cur, s + 1, ranges)

    p1 = 0
    for rating in ratings.strip().split("\n"):
        rvalues = [(i, i) for i in ints(rating)]
        if rec("in", 0, rvalues) == 1:
            p1 += sum(ints(rating))

    p2 = rec("in", 0, [(1, 4000)] * 4)

    return p1, p2


def testcase1():
    global testcase
    # input_=Path(f"{DAY}ex.txt").read_text()
    testcase = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
    p1, p2 = run(testcase)
    assert p1 == 19114
    assert p2 == 167409079868000


if __name__ == "__main__":
    input_ = open(0).read()
    result = run(input_)
    print("\n".join(map(str, result)))
