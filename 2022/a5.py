from collections import defaultdict
from pathlib import Path

DAY = 5
full_input_ = Path(f"{DAY}.txt").read_text()


def solvep1(parsed):
    stacks, moves = parsed
    for move in moves:
        for _ in range(move[0]):
            crate = stacks[move[1]].pop()
            stacks[move[2]].append(crate)

    result = []
    for stacknum, stack in stacks.items():
        result.append(stack[-1])
    return "".join(result)


def solvep2(parsed):
    stacks, moves = parsed
    for move in moves:
        crates = []
        for _ in range(move[0]):
            crate = stacks[move[1]].pop()
            crates.append(crate)
        stacks[move[2]].extend(reversed(crates))

    result = []
    for stacknum, stack in stacks.items():
        result.append(stack[-1])
    return "".join(result)


def parsestacks(chunk):
    stacks = defaultdict(list)
    positions = {}
    for l in reversed(chunk.split("\n")):
        if not positions:
            for pos, stacknum in enumerate(l):
                if stacknum != " ":
                    positions[pos] = int(stacknum)
        else:
            for pos, stacknum in positions.items():
                if pos < len(l) and l[pos] != " ":
                    stacks[stacknum].append(l[pos])
    return stacks


def parse(input: str):
    upper, lower = input.split("\n\n")
    stacks = parsestacks(upper)

    moves = []
    for l in lower.split("\n"):
        l = l.strip()
        if not l:
            continue
        w = l.split(" ")
        moves.append(tuple(int(x) for x in (w[1], w[3], w[5])))
    return stacks, moves


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    parsed = parse(full_input_)
    result = solvep2(parsed)
    print(result)
