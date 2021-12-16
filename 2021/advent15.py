import time
from operator import itemgetter

year = 2021
day = 15

inputs = [
    """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
]

with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())


def visualize(m, points):
    for y in range(len(m)):
        for x in range(len(m[0])):
            if (x, y) in points:
                print("x", end="")
            else:
                print(".", end="")
        print()
    print("--------------------")


# Find all possible next step adjecents
# Only consider unused nodes
def adjecants(m, p, used):
    risk, (x, y) = p
    result = {}
    for xn, yn in (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1):
        if xn >= 0 and yn >= 0 and xn <= end[0] and yn <= end[1]:
            if (xn, yn) not in used:
                result[(xn, yn)]= (risk + m[yn][xn], (xn, yn))
    return result


for num, data in enumerate(inputs, start=1):

    MAP_ = []
    for line in data.split("\n"):
        line = line.strip()
        if line:
            R = [int(c) for c in list(line)]
            MAP_.append(R)


    # Scale up to 5X larger map
    H = len(MAP_)
    MAP = [[-1 for _ in range(5 * H)] for _ in range(5 * H)]
    for y in range(5 * H):
        for x in range(5 * H):

            # Where to copy from, first tile is only in original map
            if x // H == 0 and y // H == 0:
                MAP[y][x] = MAP_[y][x]
            else:
                if y < H:
                    MAP[y][x] = MAP[y][x - H]
                else:
                    MAP[y][x] = MAP[y - H][x]
                MAP[y][x] += 1
                # Wrap from 9 -> 1
                if MAP[y][x] == 10:
                    MAP[y][x] = 1

    # do it for both maps and print all result
    for M in (MAP_, MAP):
        # Set of nodes where we now the total risk from start to node
        U = set()

        start = (0, 0)
        end = (len(M[0]) - 1, len(M) - 1)

        cur = (0, start)
        # candidates
        Q = []
        start_time = time.time()
        while cur[1] != end:
            U.add(cur[1])

            adjs = adjecants(M, cur, U)
            # Test if we already have path to
            if end in adjs:
                cur = adjs[end]
            else:
                U.update(adjs.keys())
                Q.extend(adjs.values())
                Q.sort(key=itemgetter(0), reverse=True)
                cur = Q.pop()

        end_time = time.time()
        # visualize(M, U)
        print(f"time: {end_time - start_time}")
        print(f"Q: {Q}")
        print(cur)
