from collections import deque
from math import lcm
from pathlib import Path
import requests

YEAR = "2023"
DAY = "8"


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


def solve(parsed):
    lr, nodes = parsed
    instructions = deque(list(lr))
    cur = "AAA"
    p1 = 0
    while cur != "ZZZ":
        inst = instructions[0]
        instructions.rotate(-1)
        cur = nodes[cur][0] if inst == "L" else nodes[cur][1]
        p1 += 1

    startnodes = [node for node in nodes.keys() if node[-1] == "A"]
    dist = []
    for node in startnodes:
        d = 0
        cur = node
        instructions = deque(list(lr))
        while cur[-1] != "Z":
            inst = instructions[0]
            instructions.rotate(-1)
            cur = nodes[cur][0] if inst == "L" else nodes[cur][1]
            d += 1
        dist.append(d)

    p2 = lcm(*dist)
    return p1, p2


def parse(input_: str):
    nodes = {}
    s1, s2 = input_.split("\n\n")
    for l in s2.split("\n"):
        l = l.strip()
        if not l:
            continue
        node, lr = l.split(" = ")
        left, right = lr.split(", ")
        nodes[node] = (left.strip("("), right.strip(")"))
    return s1, nodes


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\

"""
    parsed = parse(input_)
    # assert solve(parsed) == 42


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
