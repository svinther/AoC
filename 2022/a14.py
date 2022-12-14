from itertools import product
from pathlib import Path

DAY = 14
full_input_ = Path(f"{DAY}.txt").read_text()


def get_all_rocks(parsed):
    all_rocks = set()
    for wall in parsed:
        cx, cy = wall[0]
        for ncx, ncy in wall[1:]:
            all_rocks.update(
                product(
                    range(min(cx, ncx), max(cx, ncx) + 1),
                    range(min(cy, ncy), max(cy, ncy) + 1),
                )
            )
            cx, cy = ncx, ncy
    return all_rocks


def drip(all_rocks, sand_rest, bottom):
    sx, sy = 500, 0
    while True:
        moved = False
        # move attempts
        for mpx, mpy in ((0, 1), (-1, 1), (1, 1)):
            check = (sx + mpx, sy + mpy)
            # print(sx, sy, check)
            if check not in all_rocks and check not in sand_rest and check[1] < bottom:
                sx, sy = check
                moved = True
                break

        if not moved:
            sand_rest.add((sx, sy))
            # print(sand_rest)
            return sx, sy


def solvep1(parsed):
    all_rocks = get_all_rocks(parsed)

    abyss = max(y for x, y in all_rocks) + 1
    sand_rest = set()

    while True:
        drip(all_rocks, sand_rest, abyss)
        if max(y for x, y in sand_rest) == abyss - 1:
            break

    return len(sand_rest) - 1


def solvep2(parsed):
    all_rocks = get_all_rocks(parsed)

    bottom = max(y for x, y in all_rocks) + 2
    sand_rest = set()

    while (500, 0) not in sand_rest:
        drip(all_rocks, sand_rest, bottom)

    return len(sand_rest)


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        coords = [(int(x), int(y)) for x, y in [c.split(",") for c in l.split(" -> ")]]
        parsed.append(coords)
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 24
    assert solvep2(parsed) == 93


def run():
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)


if __name__ == "__main__":
    run()
