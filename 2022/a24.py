from collections import defaultdict
from pathlib import Path
from typing import Tuple, Dict, List

DAY = 24
full_input_ = Path(f"{DAY}.txt").read_text()


def render_single(xmax, ymax, B, current=None):
    for y in range(-1, ymax + 2):
        for x in range(-1, xmax + 2):
            if current and (x, y) == current:
                print("E", end="")
            elif (x, y) in B:
                lc = B[(x, y)]
                if len(lc) > 1:
                    print(len(lc), end="")
                else:
                    print(lc[0], end="")
            else:
                print("#" if y < 0 or y > ymax or x < 0 or x > xmax else ".", end="")
        print()


def render(xmax, ymax, cycles, path):
    for cycle, current in enumerate(path):
        print(cycle)
        render_single(xmax, ymax, cycles[cycle % len(cycles)])
        render_single(xmax, ymax, cycles[cycle % len(cycles)], current)


def get_cycles(
    parsed: Tuple[Dict[Tuple[int, int], str], int, int]
) -> Tuple[List[Dict[Tuple[int, int], List[str]]], int, int]:
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


def solve(parsed: Tuple[Dict[Tuple[int, int], str], int, int], startpath, target):
    cycles, xmax, ymax = get_cycles(parsed)

    initial_state = ((len(startpath) - 1) % len(cycles), startpath[-1])
    # (cycle, current, xypath)
    Q = [(initial_state, startpath)]

    # state is tuple of (cycle, pos)
    # entry in costs indicate that the state is either in Q or was previously visited
    costs = {initial_state: 0}

    while Q:
        Q.sort(key=lambda z: costs[(z[0])], reverse=True)
        (c, current), path = Q.pop()

        if current == target:
            return path

        cyclep = len(path) % len(cycles)

        B = cycles[cyclep]
        cx, cy = current
        for x_, y_ in [current, (cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
            if (x_, y_) in B:
                continue

            if (x_, y_) in (current, target) or (0 <= x_ <= xmax and 0 <= y_ <= ymax):
                state = (cyclep, (x_, y_))
                cost = len(path)
                previous_cost = costs.get(state)
                if previous_cost:
                    if cost < previous_cost:
                        # found cheaper path to this state
                        costs[state] = cost
                    continue
                else:
                    costs[state] = cost

                if len(costs) % 50000 == 0:
                    print(len(costs), len(Q))

                Q.append(((cyclep, (x_, y_)), path + [(x_, y_)]))

    assert False


def solvep1(parsed):
    _, xmax, ymax = parsed
    path = solve(parsed, [(0, -1)], (xmax, ymax + 1))
    return len(path) - 1


def solvep2(parsed: Tuple[Dict[Tuple[int, int], str], int, int]):
    _, xmax, ymax = parsed
    path1 = solve(parsed, [(0, -1)], (xmax, ymax + 1))
    assert path1[-1] == (xmax, ymax + 1)

    path2 = solve(parsed, path1, (0, -1))
    assert path2[-1] == (0, -1)

    path3 = solve(parsed, path2, (xmax, ymax + 1))
    assert path3[-1] == (xmax, ymax + 1)

    return len(path3) - 1


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
    assert solvep1(parsed) == 18
    assert solvep2(parsed) == 54


def run():
    parsed = parse(full_input_)
    print(solvep1(parsed))
    print(solvep2(parsed))


if __name__ == "__main__":
    run()
