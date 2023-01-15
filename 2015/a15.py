from collections import defaultdict
from functools import reduce
from operator import mul
from pathlib import Path

DAY = "15"
full_input_ = Path(f"{DAY}.txt").read_text()


def combos():
    for a in range(101):
        for b in range(100 - a + 1):
            for c in range(100 - a - b + 1):
                yield (a, b, c, 100 - a - b - c)


def solve(ingredients):
    bestcombo, bestscore = None, 0
    p2bestcombo, p2bestscore = None, 0
    for combo in combos():
        iscores = defaultdict(int)
        for idx, amount in enumerate(combo):
            for prop, val in ingredients[idx].items():
                iscores[prop] += amount * val

        iscores_ = [max(0, v) for k, v in iscores.items() if k != "calories"]
        score = reduce(mul, iscores_)
        if score > bestscore:
            bestscore = score
            bestcombo = combo

        if iscores["calories"] == 500:
            if score > p2bestscore:
                p2bestscore = score
                p2bestcombo = combo

    return bestscore, p2bestscore


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        i, props = [p.strip() for p in l.split(":")]
        pm = {p: int(v) for p, v in [j.split() for j in props.split(",")]}
        parsed.append(pm)
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
