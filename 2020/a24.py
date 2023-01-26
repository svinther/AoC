from collections import defaultdict
from copy import copy
from pathlib import Path

DAY = "24"
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed):
    flipped = set()

    for path in parsed:
        x, y = 0.0, 0
        for d in path:
            if d == "e":
                x += 1
            elif d == "w":
                x -= 1
            elif d == "ne":
                x += 0.5
                y += 1
            elif d == "nw":
                x -= 0.5
                y += 1
            elif d == "se":
                x += 0.5
                y -= 1
            elif d == "sw":
                x -= 0.5
                y -= 1
            else:
                assert False
        if (x, y) in flipped:
            flipped.remove((x, y))
        else:
            flipped.add((x, y))

    return flipped


def nbs(t):
    x, y = t
    return [
        (x + 1, y),
        (x - 1, y),
        (x + 0.5, y + 1),
        (x + 0.5, y - 1),
        (x - 0.5, y + 1),
        (x - 0.5, y - 1),
    ]


def solvep2(flipped):
    for _ in range(100):
        flipped_nbc = defaultdict(int)
        nonflipped_nbc = defaultdict(int)

        for f in flipped:
            fnbs = nbs(f)
            flipped_nbc[f] = len([x for x in fnbs if x in flipped])
            for nb in fnbs:
                if nb not in flipped:
                    nfnbs = nbs(nb)
                    nonflipped_nbc[nb] = len([x for x in nfnbs if x in flipped])

        for f in copy(flipped):
            c = flipped_nbc[f]
            if c == 0 or c > 2:
                flipped.remove(f)
        for f, c in nonflipped_nbc.items():
            if c == 2:
                flipped.add(f)

    return flipped


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        # e, se, sw, w, nw, and ne.
        path = []
        while l:
            if l[0] in ("e", "w"):
                path.append(l[0])
                l = l[1:]
            else:
                path.append(l[:2])
                l = l[2:]
        parsed.append(path)
    return parsed


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(len(result))

    result2 = solvep2(result)
    print(len(result2))


if __name__ == "__main__":
    run()
