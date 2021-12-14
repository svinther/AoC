import re
from collections import Counter
from pprint import pprint

input = """\
ma-start
YZ-rv
MP-rv
vc-MP
QD-kj
rv-kj
ma-rv
YZ-zd
UB-rv
MP-xe
start-MP
zd-end
ma-UB
ma-MP
UB-xe
end-UB
ju-MP
ma-xe
zd-UB
start-xe
YZ-end
"""



connections = {}
for l in input.split("\n"):
    if l:
        a,b = l.split("-")
        connections.setdefault(a, []).append(b)
        connections.setdefault(b, []).append(a)


def calc_paths_to_end(complete_paths, path, small_caves_visited):
    cave = path[-1]

    if cave == "start":
        return

    if cave.islower():
        small_caves_visited.append(cave)

    # count how many times each small cave was visited
    visits_per_cave = Counter(small_caves_visited)
    # did we hit 3 visits in any cave ?
    if 3 in visits_per_cave.values():
        return
    # did we visit more than a single cave twice ?
    if Counter(visits_per_cave.values()).get(2,0) > 1:
        return

    if cave == "end":
        complete_paths.append(path)
    else:
        for next_cave in connections.get(cave):
            calc_paths_to_end(complete_paths, path + [next_cave], small_caves_visited.copy())



import timeit
start = timeit.default_timer()

paths=[]
path=["start"]
for next_cave in connections.get("start"):
    calc_paths_to_end(paths, path + [next_cave], [])

# for index, path in enumerate(paths):
#     print(f"{index+1}: {path}")

print(len(paths))
stop = timeit.default_timer()
print('Time: ', stop - start)



