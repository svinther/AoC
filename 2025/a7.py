def solvep1(grid):
    R = len(grid)
    C = len(grid[0])
    for c_start in range(C):
        if grid[0][c_start] == "S":
            break
    else:
        assert False
    splits = 0
    T = [0] * C
    T[c_start] = 1

    for r in range(1, R):
        for c in range(C):
            if grid[r][c] == "^" and T[c] > 0:
                splits += 1
                T[c - 1] += T[c]
                T[c + 1] += T[c]
                T[c] = 0
    return splits


def solvep2(grid):
    R = len(grid)
    C = len(grid[0])
    for c_start in range(C):
        if grid[0][c_start] == "S":
            break
    else:
        assert False
    splits = 1
    T = [0] * C
    T[c_start] = 1

    for r in range(1, R):
        for c in range(C):
            if grid[r][c] == "^" and T[c] > 0:
                splits += T[c]
                T[c - 1] += T[c]
                T[c + 1] += T[c]
                T[c] = 0
    return splits


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(l)
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 21
    assert solvep2(parsed) == 40


def run():
    input_ = open(0).read()
    parsed = parse(input_)
    p1result = solvep1(parsed)
    print(p1result)

    parsed = parse(input_)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
