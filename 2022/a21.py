from pathlib import Path
from typing import NamedTuple

DAY = 21
full_input_ = Path(f"{DAY}.txt").read_text()


class M(NamedTuple):
    left: str
    right: str
    op: str


def solve(parsed):
    def recurse(current: str):
        if isinstance(parsed[current], int):
            return parsed[current]

        m: M = parsed[current]
        left, right = recurse(m.left), recurse(m.right)
        if m.op == "*":
            return left * right
        elif m.op == "+":
            return left + right
        elif m.op == "-":
            return left - right
        elif m.op == "/":
            return left // right
        elif m.op == "=":
            return left, right
        else:
            assert False

    p1result = recurse("root")

    root = parsed["root"]
    parsed["root"] = M(root.left, root.right, "=")

    def solve_humn(i):
        parsed["humn"] = i
        l, r = recurse("root")
        return l, r

    # make sure f increase with x
    f = lambda x: solve_humn(x)[0] - solve_humn(x)[1]
    if f(100) < f(10):
        f = lambda x: solve_humn(x)[1] - solve_humn(x)[0]

    # initial min max
    e = 1
    while f(10**e) < 0 or f(-(10**e)) > 0:
        e += 1
    minh, maxh = -(10**e), 10**e
    assert f(minh) < 0
    assert f(maxh) > 0

    # binary search for f(x) == 0
    while True:
        mid = minh + (maxh - minh) // 2
        solved = f(mid)
        if solved < 0:
            minh = mid
        elif solved > 0:
            maxh = mid
        else:
            break

    # multiple answers, lowest is the accepted one it seems?
    i = 0
    while f(mid - i - 1) == 0:
        i += 1
    assert f(mid - i) == 0

    return p1result, mid - i


def parse(input_: str):
    parsed = {}
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        s = l.split()
        if len(s) == 2:
            parsed[s[0][:-1]] = int(s[1])
        else:
            assert len(s) == 4
            parsed[s[0][:-1]] = M(s[1], s[3], s[2])
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""
    parsed = parse(input_)
    assert solve(parsed) == (152, 301)


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result[0])
    print(result[1])


if __name__ == "__main__":
    run()
