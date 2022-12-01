from collections import defaultdict, deque

DAY = 15
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


def solve(parsed, rounds):
    last = None
    for i, turn in zip(range(1, rounds + 1), gen(parsed)):
        last = (i, turn)
    return last


def parse(input: str):
    parsed = []
    for l in input.split(","):
        l = l.strip()
        if not l:
            continue
        parsed.append(int(l))
    return parsed


def testp1():
    assert solve(parse("0,3,6"), 10) == (10, 0)
    assert solve(parse("1,3,2"), 2020) == (2020, 1)


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solve(parsed, 2020)
    print(result)

    result = solve(parsed, 30000000)
    print(result)
