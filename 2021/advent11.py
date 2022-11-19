# input="""\
# 5483143223
# 2745854711
# 5264556173
# 6141336146
# 6357385478
# 4167524645
# 2176841721
# 6882881134
# 4846848554
# 5283751526
# """

input = """\
1224346384
5621128587
6388426546
1556247756
1451811573
1832388122
2748545647
2582877432
3185643871
2224876627
"""


def flash(x, y, m):
    for xs in range(x - 1, x - 1 + 3):
        for ys in range(y - 1, y - 1 + 3):
            if xs >= 0 and xs < 10 and ys >= 0 and ys < 10 and (x, y) != (xs, ys):
                m[xs][ys] += 1
                if m[xs][ys] == 10:
                    flash(xs, ys, m)


def step(m):
    # increment and collect flash items
    flash_q = []
    for x in range(0, 10):
        for y in range(0, 10):
            m[x][y] += 1
            if m[x][y] == 10:
                flash_q.append((x, y))
    # flash em
    for x, y in flash_q:
        flash(x, y, m)

    count = 0
    for x in range(0, 10):
        for y in range(0, 10):
            if m[x][y] >= 10:
                m[x][y] = 0
                count = count + 1
    return count


# Arrange as int matrice
next = [[int(c) for c in l] for l in input.split("\n") if l]
total_flashes = 0
for si in range(0, 100):
    count = step(next)
    total_flashes += count
print(f"Flashes total after 100 steps {total_flashes}")


next = [[int(c) for c in l] for l in input.split("\n") if l]
si = 0
while True:
    si += 1
    count = step(next)
    if count == 100:
        break
print(f"First time all flashes at once is step {si}")
