from itertools import product
from pathlib import Path

DAY = 18
full_input_ = Path(f"{DAY}.txt").read_text()


def getnbs(S, coord):
    nbmods = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
    result = []
    for nb in [tuple(a + b for a, b in zip(coord, nbmod)) for nbmod in nbmods]:
        if nb in S:
            result.append(nb)
    return tuple(result)


def surfacearea(S):
    result = 0
    for d in S:
        result += 6 - len(getnbs(S, d))
    return result


def solvep1(parsed):
    return surfacearea(parsed)


def solvep2(parsed):
    # megacube
    minx, miny, minz = (
        min(x for x, _, _ in parsed),
        min(y for _, y, _ in parsed),
        min(z for _, _, z in parsed),
    )
    maxx, maxy, maxz = (
        max(x for x, _, _ in parsed),
        max(y for _, y, _ in parsed),
        max(z for _, _, z in parsed),
    )

    empty = set()
    for x, y, z in product(
        range(minx, maxx + 1), range(miny, maxy + 1), range(minz, maxz + 1)
    ):
        if (x, y, z) not in parsed:
            empty.add((x, y, z))

    surface = surfacearea(parsed)

    trapped = set()
    for air in empty:
        if air in trapped:
            continue
        queue = {air}
        visited = set()
        escaped = False
        while queue:
            c = queue.pop()
            visited.add(c)
            if c[0] in (minx, maxx) or c[1] in (miny, maxy) or c[2] in (minz, maxz):
                escaped = True
                break

            for nb in getnbs(empty, c):
                assert nb not in parsed
                if nb not in visited:
                    queue.add(nb)

        if not escaped:
            assert not queue
            assert not parsed & visited
            assert not visited & trapped
            trapped.update(visited)
            airsurface = surfacearea(visited)
            surface -= airsurface

    return surface


def parse(input_: str):
    parsed = set()
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        x, y, z = l.split(",")
        x, y, z = int(x), int(y), int(z)
        parsed.add((x, y, z))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 64
    assert solvep2(parsed) == 58


def testcustom():
    input_ = """\
-1,0,0
1,0,0
0,1,0
0,-1,0
0,0,1
0,0,-1
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 36
    assert solvep2(parsed) == 30


def run():
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)


if __name__ == "__main__":
    run()
