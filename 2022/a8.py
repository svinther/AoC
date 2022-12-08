from functools import reduce
from pathlib import Path
from typing import NamedTuple

DAY = 8
full_input_ = Path(f"{DAY}.txt").read_text()


class Coord(NamedTuple):
    x: int
    y: int


def search_higher(matrix, coord, highestseen, searchf):
    xmax = len(matrix[0]) - 1
    ymax = len(matrix) - 1

    if highestseen == 9:
        return set()

    nextcoord = searchf(coord)
    if xmax > nextcoord.x > 0 and ymax > nextcoord.y > 0:
        height = matrix[nextcoord.y][nextcoord.x]
        if height > highestseen:
            return {nextcoord} | search_higher(matrix, nextcoord, height, searchf)
        else:
            return search_higher(matrix, nextcoord, highestseen, searchf)
    else:
        return set()


def solve(matrix):
    xmax = len(matrix[0]) - 1
    ymax = len(matrix) - 1
    Etop = {Coord(x, 0) for x in range(xmax + 1)}
    Ebot = {Coord(x, ymax) for x in range(xmax + 1)}
    Eleft = {Coord(0, y) for y in range(ymax + 1)}
    Eright = {Coord(xmax, y) for y in range(ymax + 1)}

    visible = Etop | Ebot | Eleft | Eright
    for E, searchf in [
        (Etop, lambda c: Coord(c.x, c.y + 1)),
        (Ebot, lambda c: Coord(c.x, c.y - 1)),
        (Eleft, lambda c: Coord(c.x + 1, c.y)),
        (Eright, lambda c: Coord(c.x - 1, c.y)),
    ]:
        for c in E:
            visible.update(search_higher(matrix, c, matrix[c.y][c.x], searchf))
    return visible


def viewscore(matrix, coord, maxheight, searchf):
    xmax = len(matrix[0]) - 1
    ymax = len(matrix) - 1
    nextcoord = searchf(coord)
    if xmax > nextcoord.x > 0 and ymax > nextcoord.y > 0:
        height = matrix[nextcoord.y][nextcoord.x]
        if height >= maxheight:
            return 1
        else:
            return 1 + viewscore(matrix, nextcoord, maxheight, searchf)
    else:
        return 1


def solvep2(matrix):
    maxscore = 0

    searchfunctions = [
        lambda c: Coord(c.x, c.y + 1),
        lambda c: Coord(c.x, c.y - 1),
        lambda c: Coord(c.x + 1, c.y),
        lambda c: Coord(c.x - 1, c.y),
    ]

    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            score = reduce(
                lambda a, b: a * b,
                [
                    viewscore(matrix, Coord(x, y), matrix[y][x], searchf)
                    for searchf in searchfunctions
                ],
            )
            maxscore = max(maxscore, score)

    return maxscore


def parse(input: str):
    parsed = []
    for l in input.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append([int(t) for t in l])
    return parsed


def test_0():
    input_ = """\
555
525
515
"""
    matrix = parse(input_)
    result = solve(matrix)
    assert len(result) == 9


def test_1():
    input_ = """\
30373
25512
65332
33549
35390
"""
    matrix = parse(input_)
    result = solve(matrix)
    for c in [(1, 1), (2, 1), (1, 2), (3, 2), (2, 3)]:
        assert c in result

    for c in [(3, 1), (2, 2), (1, 3), (3, 3)]:
        assert c not in result

    assert len(result) == 21


def test_2():
    input_ = """\
30373
25512
65332
33549
35390
"""
    matrix = parse(input_)
    result = solvep2(matrix)
    assert result == 8


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(len(result))

    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
