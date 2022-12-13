import json
from functools import cmp_to_key
from pathlib import Path

DAY = 13
full_input_ = Path(f"{DAY}.txt").read_text()


def recurse(left, right):
    result = None
    if isinstance(left, int) and isinstance(right, int):
        result = -1 if left < right else 1 if left > right else 0
    elif isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            cmp = recurse(l, r)
            if cmp != 0:
                result = cmp
                break
        if not result:
            result = (
                -1 if len(left) < len(right) else 1 if len(left) > len(right) else 0
            )
    elif isinstance(left, int):
        result = recurse([left], right)
    else:
        assert isinstance(right, int)
        assert isinstance(left, list)
        result = recurse(left, [right])

    # print("compare", left, right, result)
    return result


def solve(parsed):
    correct = []
    for left, right in parsed:
        correct.append(recurse(left, right))

    result = 0
    for index0, cmp in enumerate(correct):
        if cmp < 0:
            result += index0 + 1
    return result


def solvep2(parsed):
    all = []
    for left, right in parsed:
        all.append(left)
        all.append(right)

    d1, d2 = [[2]], [[6]]

    all.append(d1)
    all.append(d2)

    all.sort(key=cmp_to_key(recurse))
    return (all.index(d1) + 1) * (all.index(d2) + 1)


def parse(input_: str):
    parsed = []
    for chunk in input_.split("\n\n"):
        chunk = chunk.strip()
        left, right = chunk.split("\n")
        parsed.append((json.loads(left), json.loads(right)))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
    parsed = parse(input_)
    assert solve(parsed) == 13

    assert solvep2(parsed) == 140


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)


if __name__ == "__main__":
    run()
