from functools import reduce
from operator import itemgetter

# input_data = """\
# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# """
import requests

cookie = "xxx"
response = requests.get("https://adventofcode.com/2021/day/9/input", headers={"cookie": cookie})
input_data = response.text

data = [[int(c) for c in l] for l in input_data.split("\n") if l]


def is_low_point(x, y):
    adjecents = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    adjecent_values = []
    for xs, ys in adjecents:
        if xs >= 0 and ys >= 0 and xs < len(data[0]) and ys < len(data):
            adjecent_values.append(data[ys][xs])
    return min(adjecent_values) > data[y][x]


low_points = []
sum = 0
for y, row in enumerate(data):
    for x, value in enumerate(row):
        if is_low_point(x, y):
            low_points.append(((x, y), value))
            sum += (value + 1)
print(sum)

used_areas = set()


def calc_basin(x, y, basin):
    if x >= 0 and y >= 0 and x < len(data[0]) and y < len(data):
        if data[y][x] == 9:
            return
        if (x, y) in used_areas:
            return

        basin.add((x, y))
        used_areas.add((x, y))
        for xs, ys in ((x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)):
            calc_basin(xs, ys, basin)


basins = []
for y, row in enumerate(data):
    for x, value in enumerate(row):
        basin = set()
        calc_basin(x, y, basin)
        if basin:
            basins.append(basin)

for n, basin in enumerate(basins, start=1):
    print(f"{n} (size={len(basin)}): {sorted(sorted(basin, key=itemgetter(1)), key=itemgetter(0))}")

basin_sizes = [len(x) for x in basins]
max3_basins = sorted(basin_sizes)[-3:]
score = reduce(lambda a, b: a * b, max3_basins)
print(f"Score: {score}")
