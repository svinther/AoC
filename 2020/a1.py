from operator import mul
from functools import reduce
from itertools import product
from pathlib import Path

DAY = "1"
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed, n):
    X = [parsed] * n
    for s in product(*X):
        if sum(s) == 2020:
            return reduce(mul, s)


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(int(l))
    return parsed


def run():
    parsed = parse(full_input_)
    result = solve(parsed, 2)
    print(result)

    result = solve(parsed, 3)
    print(result)


if __name__ == "__main__":
    run()
