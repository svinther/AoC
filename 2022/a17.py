from pathlib import Path

DAY = 17
full_input_ = Path(f"{DAY}.txt").read_text()


def get_shapes():
    return [
        [(x, 0) for x in range(2, 2 + 4)],
        [(x, 1) for x in range(2, 2 + 3)] + [(3, 2), (3, 0)],
        [(x, 0) for x in range(2, 2 + 3)] + [(4, 1), (4, 2)],
        [(2, y) for y in range(0, 4)],
        [(2, 0), (2, 1), (3, 0), (3, 1)],
    ]


def render(shape):
    matrix = [["."] * 7 for _ in range(max(y for _, y in shape))]
    for x, y in shape:
        matrix[len(matrix) - y][x] = "@"
    for l in matrix:
        print("".join(l))
    print()


def solve(jets, rockcount):
    shapes = get_shapes()
    R = set()
    floor = 0
    jet = 0
    i = 0

    formations = {}

    while i < rockcount:
        maxy = max(y for _, y in R) if R else floor
        shape = {(x, y + maxy + 4) for x, y in shapes[i % len(shapes)]}
        # render(R.union(shape))

        while True:
            # jet
            # print(jet, i)
            shape_ = (
                {(x - 1, y) for x, y in shape}
                if jets[jet] == "<"
                else {(x + 1, y) for x, y in shape}
            )
            if (
                min(x for x, _ in shape_) >= 0
                and max(x for x, _ in shape_) < 7
                and not R.intersection(shape_)
            ):
                shape = shape_
            # render(R.union(shape))
            jet = (jet + 1) % len(jets)

            # down
            shape_ = {(x, y - 1) for x, y in shape}
            if min(y for _, y in shape_) > floor and not R.intersection(shape_):
                shape = shape_
                # render(R.union(shape))
            else:
                R.update(shape)
                break

        maxy = max(y for _, y in R)
        topformation = []
        for x in range(7):
            topformation.append(maxy - max([y for rx, y in R if x == rx] + [floor]))
        formation = (jet, i % len(shapes), tuple(topformation))
        if formation in formations:
            (
                li,
                ly,
            ) = formations[formation]
            di = i - li
            dy = maxy - ly
            rocksleft = rockcount - i - 1
            skips = rocksleft // di
            i += di * skips
            R = {(x, y + dy * skips) for x, y in R}
        else:
            formations[formation] = (i, maxy)

        i += 1

    return max(y for _, y in R)


def parse(input_: str):
    return input_.strip()


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""
    parsed = parse(input_)
    assert solve(parsed, 2022) == 3068

    # part 2 testcase not working, never any full rows ??
    assert solve(parsed, 1000000000000) == 1514285714288


def run():
    parsed = parse(full_input_)
    result = solve(parsed, 2022)
    print(result)

    result = solve(parsed, 1000000000000)
    print(result)


if __name__ == "__main__":
    run()
