from copy import deepcopy
from pathlib import Path
from pprint import pprint
from typing import List


def step(state: List[List[str]]):
    yl = len(state)
    xl = len(state[0])

    new_state = deepcopy(state)
    moved = False

    for y in range(0, yl):
        for x in range(0, xl):
            xnext = (x + 1) % xl
            c = state[y][x]
            if c == ">" and state[y][xnext] == ".":
                new_state[y][x] = "."
                new_state[y][xnext] = c
                moved = True

    state = new_state
    new_state = deepcopy(state)

    for y in range(0, yl):
        for x in range(0, xl):
            ynext = (y + 1) % yl
            c = state[y][x]
            if c == "v" and state[ynext][x] == ".":
                new_state[y][x] = "."
                new_state[ynext][x] = c
                moved = True

    if moved:
        return new_state


def parse(input_: str):
    result = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        result.append(list(l))
    return result


def test_part1():
    input_ = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>    
"""

    parsed = parse(input_)
    states = [parsed]
    while True:
        state = states[-1]
        print()
        pprint(state)
        new_state = step(state)
        if new_state:
            states.append(new_state)

        else:
            break

    assert len(states) == 58


if __name__ == "__main__":
    input_ = Path("input.2021.25.txt").read_text()
    parsed = parse(input_)
    states = [parsed]
    while True:
        state = states[-1]
        new_state = step(state)
        if new_state:
            states.append(new_state)

        else:
            break
    print(len(states))
