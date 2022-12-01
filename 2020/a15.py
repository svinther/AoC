from collections import defaultdict, deque
from copy import copy
from pathlib import Path

DAY = 1
full_input_ = "6,19,0,5,7,13,1"


def gen(parsed):
    last = None
    length = 0
    seenindex = defaultdict(deque)
    for i, n in enumerate(parsed):
        seenindex[n].append(i)
        last = n
        length += 1
        yield n

    while True:
        lastseen = seenindex[last].popleft() if len(seenindex[last]) > 1 else None
        if lastseen is not None:
            nextnum = length - 1 - lastseen
            assert len(seenindex[last]) == 1
        else:
            nextnum = 0
        seenindex[nextnum].append(length)
        last = nextnum
        length += 1

        if length % 100000 == 0:
            print("processed", length)

        yield nextnum


def solvep1(parsed, rounds):
    turns = [(i, n) for i, n in zip(range(1, rounds + 1), gen(parsed))]
    return turns[-1]


def solvep2(parsed, rounds):
    turns = [(i, n) for i, n in zip(range(1, rounds + 1), gen(parsed))]
    return turns[-1]


def parse(input: str):
    parsed = []
    for l in input.split(","):
        l = l.strip()
        if not l:
            continue
        parsed.append(int(l))
    return parsed


def testp1():
    assert solvep1(parse("0,3,6"), 10) == (10, 0)
    assert solvep1(parse("1,3,2"), 2020) == (2020, 1)


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solvep1(parsed, 2020)
    print(result)

    result = solvep2(parsed, 30000000)
    print(result)
