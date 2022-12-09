from functools import reduce
from itertools import product
from operator import mul
from pathlib import Path
from typing import NamedTuple

DAY = 8
full_input_ = Path(f"{DAY}.txt").read_text()


class Coord(NamedTuple):
    x: int
    y: int


def search_higher(matrix, coord, highestseen, direction):
    xmax = len(matrix[0]) - 1
    ymax = len(matrix) - 1

    if highestseen == 9:
        return set()

    nextcoord = Coord(coord.x + direction.x, coord.y + direction.y)
    if xmax > nextcoord.x > 0 and ymax > nextcoord.y > 0:
        height = matrix[nextcoord.y][nextcoord.x]
        if height > highestseen:
            return {nextcoord} | search_higher(matrix, nextcoord, height, direction)
        else:
            return search_higher(matrix, nextcoord, highestseen, direction)
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
        (Etop, Coord(0, 1)),
        (Ebot, Coord(0, -1)),
        (Eleft, Coord(1, 0)),
        (Eright, Coord(-1, 0)),
    ]:
        for c in E:
            visible.update(search_higher(matrix, c, matrix[c.y][c.x], searchf))
    return visible


def viewscore(matrix, coord, maxheight, direction):
    xmax = len(matrix[0]) - 1
    ymax = len(matrix) - 1
    nextcoord = Coord(coord.x + direction.x, coord.y + direction.y)
    if xmax > nextcoord.x > 0 and ymax > nextcoord.y > 0:
        height = matrix[nextcoord.y][nextcoord.x]
        if height >= maxheight:
            return 1
        else:
            return 1 + viewscore(matrix, nextcoord, maxheight, direction)
    else:
        return 1


def solvep2(matrix):
    return max(
        [
            reduce(
                mul,
                [
                    viewscore(matrix, Coord(x, y), matrix[y][x], searchf)
                    for searchf in [
                        Coord(0, 1),
                        Coord(0, -1),
                        Coord(1, 0),
                        Coord(-1, 0),
                    ]
                ],
            )
            for x, y in product(range(len(matrix[0])), range(len(matrix)))
        ]
    )


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
