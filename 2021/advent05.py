from collections import defaultdict

year = 2021
day = 5

inputs = [
    """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
]

with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())


def line_points(verts, include_diagonals=False):
    all_points = set()

    if verts[0][1] == verts[1][1]:
        # x points
        x0 = min(verts[0][0], verts[1][0])
        x1 = max(verts[0][0], verts[1][0])
        for x in range(x0, x1 + 1):
            all_points.add((x, verts[0][1]))
    elif verts[0][0] == verts[1][0]:
        # y points
        y0 = min(verts[0][1], verts[1][1])
        y1 = max(verts[0][1], verts[1][1])
        for y in range(y0, y1 + 1):
            all_points.add((verts[0][0], y))
    elif include_diagonals:
        p0, p1 = sorted(verts)
        assert p0[0] < p1[0]
        pn = p0
        while pn != p1:
            all_points.add(pn)
            if p0[1] < p1[1]:
                pn = (pn[0] + 1, pn[1] + 1)
            else:
                pn = (pn[0] + 1, pn[1] - 1)
        assert pn == p1
        all_points.add(p1)

    return all_points


for num, data in enumerate(inputs, start=1):
    L = []

    for l in data.split("\n"):
        l = l.strip()
        if not l:
            continue
        p0_, gar, p1_ = l.split(" ")

        p0__ = p0_.split(",")
        p0 = (int(p0__[0].strip()), int(p0__[1].strip()))

        p1__ = p1_.split(",")
        p1 = (int(p1__[0].strip()), int(p1__[1].strip()))

        verts = (p0, p1)
        L.append((verts, line_points(verts, include_diagonals=True)))

    intersections = defaultdict(int)
    pool = set()
    for verts, points in L:
        for p in pool & points:
            intersections[p] += 1
        pool.update(points)

    result = len(intersections)
    print(result)
