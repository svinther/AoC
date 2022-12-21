from collections import deque
from pathlib import Path

DAY = 20
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed, multiplier, mixerrounds):
    parsed = [p * multiplier for p in parsed]

    pointers = deque(range(len(parsed)))
    for _ in range(mixerrounds):
        for i, num in enumerate(parsed):
            while pointers[-1] != i:
                pointers.rotate()
            p = pointers.pop()
            pointers.rotate(-num)
            pointers.append(p)

            # seq = [parsed[p] for p in pointers]
            # print(i, num, seq)

    pos0 = pointers.index(parsed.index(0))
    pos1000 = (pos0 + 1000) % len(parsed)
    pos2000 = (pos0 + 2000) % len(parsed)
    pos3000 = (pos0 + 3000) % len(parsed)
    return (
        parsed[pointers[pos1000]]
        + parsed[pointers[pos2000]]
        + parsed[pointers[pos3000]]
    )


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
1
2
-3
3
-2
0
4
"""
    parsed = parse(input_)
    assert solve(parsed, 1, 1) == 3
    assert solve(parsed, 811589153, 10) == 1623178306


def run():
    parsed = parse(full_input_)
    result = solve(parsed, 1, 1)
    print(result)

    result = solve(parsed, 811589153, 10)
    print(result)


if __name__ == "__main__":
    run()
