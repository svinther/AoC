from operator import methodcaller
from pathlib import Path

DAY = "23"
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed, reg):
    p = 0
    while 0 <= p < len(parsed):
        inst, args = parsed[p]
        if inst == "hlf":
            reg[args[0]] //= 2
        elif inst == "tpl":
            reg[args[0]] *= 3
        elif inst == "inc":
            reg[args[0]] += 1
        elif inst == "jmp":
            p += args[0]
            continue
        elif inst == "jie":
            if reg[args[0]] % 2 == 0:
                p += args[1]
                continue
        elif inst == "jio":
            if reg[args[0]] == 1:
                p += args[1]
                continue

        p += 1

    return reg


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        inst, args = l.split(" ", 1)
        if inst in ("jio", "jie"):
            r, i = map(methodcaller("strip", " +"), args.split(","))
            parsed.append((inst, (r, int(i))))
        elif inst == "jmp":
            args.strip("+")
            parsed.append((inst, (int(args),)))
        else:
            parsed.append((inst, (args,)))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\

"""
    parsed = parse(input_)
    # assert solve(parsed) == 42


def run():
    parsed = parse(full_input_)
    result = solve(parsed, reg={"a": 0, "b": 0})
    print(result)
    result = solve(parsed, reg={"a": 1, "b": 0})
    print(result)


if __name__ == "__main__":
    run()
