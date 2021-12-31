from collections import defaultdict
from itertools import chain, permutations, combinations

year = 2021
day = 19

# with open(f"ex.{year}.{day}.txt", "r") as iopen:
#     data = iopen.read()
with open(f"input.{year}.{day}.txt", "r") as iopen:
    data = iopen.read()


def roll(v):
    return (v[0], v[2], -v[1])


def turn(v):
    return (-v[1], v[0], v[2])


def rotations(V):
    for cycle in range(2):
        for step in range(3):
            V = tuple(roll(v) for v in V)
            yield (V)
            for i in range(3):
                V = tuple(turn(v) for v in V)
                yield (V)
        V = tuple(roll(turn(roll(v))) for v in V)


S = []
for s in data.split("\n\n"):
    beacons = []
    for l in s.split("\n")[1:]:
        l = l.strip()

        if l:
            beacons.append(tuple(int(x) for x in l.split(",")))
    S.append(tuple(beacons))

# scanner permutations
SP = []
for s in S:
    # Calculate all edges for each scanner, permuted in 24 rotations
    p = []
    for rs in rotations(s):
        edge_points = {}
        for p0, p1 in permutations(rs, 2):
            edge = tuple(b - a for a, b in zip(p0, p1))
            assert edge not in edge_points
            edge_points[edge] = (p0, p1)
        assert len(edge_points) == len(s) * (len(s) - 1)
        p.append(edge_points)

    assert len(p) == 24
    SP.append(p)
assert len(SP) == len(S)


def pair_points(matching_edges, left_points_by_edge, right_points_by_edge):
    # To pair the points we id the points by their complete set of vertices
    pids0 = defaultdict(set)
    pids1 = defaultdict(set)
    for v in matching_edges:
        for p in left_points_by_edge[v]:
            pids0[p].add(v)
        for p in right_points_by_edge[v]:
            pids1[p].add(v)

    pid_point0 = {frozenset(v): k for k, v in pids0.items()}
    pid_point1 = {frozenset(v): k for k, v in pids1.items()}
    assert pid_point0.keys() == pid_point1.keys()
    return [(pid_point0[vset], pid_point1[vset]) for vset in pid_point0.keys()]


# Use scanner 0 permutation 0 as reference
# Lock scanner to permutation
perms = {0: SP[0][11]}
distances = {0: (0, 0, 0)}

USED = []
UNUSED = list(range(len(SP)))

while UNUSED:
    for left_sid in UNUSED:
        if not left_sid in perms:
            continue

        left_perm = perms[left_sid]
        USED.append(left_sid)
        UNUSED.remove(left_sid)

        for right_sid in UNUSED + USED:
            if left_sid == right_sid:
                continue
            # All permutations for right
            right_perms = SP[right_sid]
            if right_sid in perms:
                # was previously matched as right hand scanner, so permutation is locked
                # narrow to list of single locked permutation
                right_perms = [perms[right_sid]]

            bestmatch = set(), None, None
            for right_perm in right_perms:
                matching_edges = set(left_perm.keys()).intersection(right_perm.keys())
                if len(matching_edges) > len(bestmatch):
                    bestmatch = matching_edges, left_perm, right_perm
            if len(bestmatch[0]) > 0:
                paired_vertexes = pair_points(*bestmatch)

                if len(paired_vertexes) >= 12:
                    distance = []
                    for p0, p1 in paired_vertexes:
                        distance.append(tuple(-(b - a) for a, b in zip(p0, p1)))
                    assert len(set(distance)) == 1
                    print(f"scanners {left_sid}:{right_sid} dist: {distance[0]}")
                    distance_to_0 = tuple(
                        a + b for a, b in zip(distances[left_sid], distance[0])
                    )
                    print(f"scanners 0:{right_sid} dist: {distance_to_0}")
                    distances[right_sid] = distance_to_0
                    perms[right_sid] = bestmatch[2]

all_beacons = set()
for sid, perm in perms.items():
    dist = distances[sid]
    for b in set(chain.from_iterable(perm.values())):
        trans_b = tuple(a + b for a, b in zip(dist, b))
        # print(sid, trans_b)
        all_beacons.add(trans_b)

print(len(all_beacons))

maxmanhattan = (0, None, None)
for p0, p1 in combinations(distances.values(), 2):
    manhattan = sum(tuple(abs(a-b) for a,b in zip(p0,p1)))
    if manhattan > maxmanhattan[0]:
        maxmanhattan = manhattan, p0, p1

print(maxmanhattan)