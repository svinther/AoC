from itertools import product
from pathlib import Path

DAY = "18"
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(state, p2=False):
    maxx, maxy = max(l[0] for l in state), max(l[1] for l in state)
    for _ in range(100):
        state_ = set()
        for x, y in product(range(maxx + 1), range(maxy + 1)):
            nbs = 0
            for nbx, nby in product((-1, 0, 1), (-1, 0, 1)):
                if (nbx, nby) == (0, 0):
                    continue
                if (x + nbx, y + nby) in state:
                    nbs += 1
            if (x, y) in state:
                if nbs in (2, 3):
                    state_.add((x, y))
            elif nbs == 3:
                state_.add((x, y))
        state = state_
        if p2:
            state.update({(0, 0), (0, maxy), (maxx, 0), (maxx, maxy)})
    return len(state)


def parse(input_: str):
    parsed = set()
    y = 0
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        for x, s in enumerate(l):
            if s == "#":
                parsed.add((x, y))
        y += 1
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
    result = solve(parsed, p2=True)
    print(result)


if __name__ == "__main__":
    run()
