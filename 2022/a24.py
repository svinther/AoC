from collections import defaultdict, deque
from pathlib import Path
from typing import Tuple, Dict, List

DAY = 24
full_input_ = Path(f"{DAY}.txt").read_text()


def get_cycles(parsed) -> Tuple[List[Dict[Tuple[int, int], List[str]]], int, int]:
    """Return a tuple with 3 entries, being:
    1. a list of dicts with key (x,y) --> List of blizzard directions for (x,y)
    2. xmax
    3. ymax

    The number of cycles will be limited to lcm(xmax,ymax) = 300 for lcm(20,150)
    """
    B, xmax, ymax = parsed
    cycles = [{(x, y): [c] for (x, y), c in B.items()}]

    while True:
        B_ = defaultdict(list)
        for (x, y), lc in cycles[-1].items():
            for c in lc:
                if c == "v":
                    B_[(x, (y + 1) % (ymax + 1))].append(c)
                elif c == "^":
                    B_[(x, (y - 1) % (ymax + 1))].append(c)
                elif c == ">":
                    B_[((x + 1) % (xmax + 1), y)].append(c)
                elif c == "<":
                    B_[((x - 1) % (xmax + 1), y)].append(c)
                else:
                    assert False

        assert sum(len(lc) for lc in B_.values()) == len(B)
        if cycles[0].keys() == B_.keys():
            cycles[0] = B_
            break
        cycles.append(B_)

    return cycles, xmax, ymax


def solve(cycles, xmax, ymax, startcycle, start, target):
    initial_state = (startcycle, start)
    Q = deque([initial_state])
    SEEN = set()

    while Q:
        c, current = Q.popleft()
        if (c, current) in SEEN:
            continue
        SEEN.add((c, current))

        if current == target:
            return c

        cyclep = c + 1

        B = cycles[cyclep % len(cycles)]
        cx, cy = current
        for x_, y_ in [current, (cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
            if (x_, y_) in B:
                continue

            if (x_, y_) in (current, target) or (0 <= x_ <= xmax and 0 <= y_ <= ymax):
                state = (cyclep, (x_, y_))
                Q.append(state)

    assert False


def solvep1p2(parsed):
    cycles, xmax, ymax = get_cycles(parsed)
    l1 = solve(cycles, xmax, ymax, 0, (0, -1), (xmax, ymax + 1))
    l2 = solve(cycles, xmax, ymax, l1, (xmax, ymax + 1), (0, -1))
    l3 = solve(cycles, xmax, ymax, l2, (0, -1), (xmax, ymax + 1))
    return l1, l3


def parse(input_: str):
    parsed = {}
    lines = [l.strip() for l in input_.split("\n") if l.strip()]
    y = 0
    xlen = 0
    for l in lines[1:-1]:
        for x, c in enumerate(l[1:-1]):
            if c != ".":
                parsed[(x, y)] = c
            xlen = max(xlen, x)
        y += 1
    return parsed, xlen, y - 1


def testp1p2():
    print()
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""
    parsed = parse(input_)
    assert solvep1p2(parsed)[0] == 18
    assert solvep1p2(parsed)[1] == 54


def run():
    parsed = parse(full_input_)
    p1, p2 = solvep1p2(parsed)
    print(p1)
    print(p2)


if __name__ == "__main__":
    run()
