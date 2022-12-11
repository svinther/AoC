import math
from collections import defaultdict
from operator import mul
from pathlib import Path
from typing import List, NamedTuple, Tuple, Dict

DAY = 11
full_input_ = Path(f"{DAY}.txt").read_text()


class Monkey(NamedTuple):
    id: int
    startitems: Tuple[int, ...]
    operation: str
    divisibleby: int
    iftrue: int
    iffalse: int


def evalexpr(expr: str, level):
    expr = expr.split("=")[1].strip()
    substituted = expr.replace("old", str(level))
    return eval(substituted)


def solve(parsed: List[Monkey], part=1):
    # least common multiple
    lcm = math.lcm(*[m.divisibleby for m in parsed])

    I = {m.id: list(m.startitems) for m in parsed}
    inspectioncounts: Dict[int, int] = defaultdict(int)
    for _ in range(20 if part == 1 else 10000):
        for monkey in parsed:
            inspectioncounts[monkey.id] += len(I[monkey.id])
            while I[monkey.id]:
                level = I[monkey.id].pop()
                new = evalexpr(monkey.operation, level)
                if part == 1:
                    new //= 3
                new %= lcm
                if new % monkey.divisibleby == 0:
                    I[monkey.iftrue].append(new)
                else:
                    I[monkey.iffalse].append(new)

    sortedcounts = sorted(inspectioncounts.values())
    return mul(*sortedcounts[-2:])


def parse(input_: str):
    parsed = []
    for chunk in input_.split("\n\n"):
        lines = [l.strip() for l in chunk.split("\n") if l.strip()]
        monkey = int(lines[0].split(" ")[1][:-1])
        startitems = tuple(int(n.strip()) for n in lines[1].split(":")[1].split(","))
        operation = lines[2].split(":")[1].strip()
        divisibleby = int(lines[3].split(" ")[-1])
        iftrue = int(lines[4].split(" ")[-1].strip())
        iffalse = int(lines[5].split(" ")[-1].strip())

        parsed.append(
            Monkey(monkey, startitems, operation, divisibleby, iftrue, iffalse)
        )
    return parsed


def testp1_2():
    input_ = Path(f"{DAY}ex.txt").read_text()
    parsed = parse(input_)
    assert solve(parsed, 1) == 10605
    assert solve(parsed, part=2) == 2713310158


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)

    result = solve(parsed, part=2)
    print(result)


if __name__ == "__main__":
    run()
