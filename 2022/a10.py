from pathlib import Path
from typing import NamedTuple, Iterable, Optional, Tuple, List

DAY = 10
full_input_ = Path(f"{DAY}.txt").read_text()


class Cycle(NamedTuple):
    during: int
    after: int


def cycle(instructions) -> Iterable[Cycle]:
    x = 1
    for op, arg in instructions:
        if op == "noop":
            yield Cycle(x, x)
        else:
            yield Cycle(x, x)
            x_ = x
            x += arg
            yield Cycle(x_, x)


def crt(instructions):
    cycles = cycle(instructions)
    lines = []
    for _ in range(6):
        line = []
        for pix, c in zip(range(40), cycles):
            if c.during - 1 <= pix <= c.during + 1:
                line.append("#")
            else:
                line.append(".")
        lines.append("".join(line))
    return lines


def solve(parsed):
    polls = [20, 60, 100, 140, 180, 220]
    cycles = list(cycle(parsed))
    strengths = [p * cycles[p - 1].during for p in polls]
    return sum(strengths)


def parse(input: str) -> List[Tuple[str, Optional[int]]]:
    parsed: List[Tuple[str, Optional[int]]] = []
    for l in input.split("\n"):
        l = l.strip()
        if not l:
            continue
        if l == "noop":
            parsed.append((l, None))
        else:
            inst, arg = l.split()
            parsed.append((inst, int(arg)))
    return parsed


def testp1():
    input_ = Path(f"{DAY}ex.txt").read_text()
    parsed = parse(input_)
    polls = [20, 60, 100, 140, 180, 220]
    cycles = list(cycle(parsed))
    signals = [cycles[p - 1].during for p in polls]
    assert signals == [21, 19, 18, 21, 16, 18]
    strengths = [p * cycles[p - 1].during for p in polls]
    assert strengths == [420, 1140, 1800, 2940, 2880, 3960]
    assert sum(strengths) == 13140

    print()
    crt(parsed)


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)

    for line in crt(parsed):
        print(line)


if __name__ == "__main__":
    run()
