from collections import defaultdict
from itertools import combinations
from pathlib import Path

DAY = "17"
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed):
    valid = defaultdict(int)
    minl = 10**9
    for l in range(1, len(parsed) + 1):
        for c in combinations(parsed, l):
            if sum(c) == 150:
                valid[l] += 1
                minl = min(minl, l)
    return sum(valid.values()), valid[minl]


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(int(l))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\

"""
    parsed = parse(input_)
    # assert solve(parsed) == 42


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
