import functools
from collections import defaultdict
from itertools import combinations, chain
from typing import List

year = 2021
day = 19

inputs = []

with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())

inputs.append(
    """\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""
)


def xrot(p, dir=True):
    if dir:
        # y becomes z
        # z becomes -y
        return (p[0], p[2], -p[1])
    # y becomes -z
    # z becomes y
    return (p[0], -p[2], p[1])


def rxrot(p, dir=True):
    return xrot(p, not dir)


def yrot(p, dir=True):
    if dir:
        # z becomes x
        # x becomes -z
        return (-p[2], p[1], p[0])
    # z becomes -x
    # x becomes z
    return (p[2], p[1], -p[0])


def ryrot(p, dir=True):
    return yrot(p, not dir)


def zrot(p, dir=True):
    if dir:
        # y becomes -x
        # x becomes y
        return (p[1], -p[0], p[2])
    # y becomes x
    # x becomes -y
    return (-p[1], p[0], p[2])


def rzrot(p, dir=True):
    return zrot(p, not dir)


# rotations that leads to 24 unique orientations
@functools.cache
def get_rotations_full_scan():
    rotations = []

    for _ in range(4):
        rotations.append((zrot, True))

    rotations.append((xrot, False))
    for _ in range(4):
        rotations.append((yrot, True))

    rotations.append((xrot, False))
    for _ in range(4):
        rotations.append((zrot, True))

    rotations.append((xrot, False))
    for _ in range(4):
        rotations.append((yrot, True))

    rotations.append((xrot, False))

    rotations.append((ryrot, False))
    for _ in range(4):
        rotations.append((xrot, True))

    rotations.append((yrot, False))
    rotations.append((yrot, False))
    for _ in range(4):
        rotations.append((xrot, True))

    rotations.append((ryrot, False))

    return tuple(rotations)


class Permutation:
    def __init__(self, vertice_points, applied_rots):
        self.vertice_points = vertice_points
        self.applied_rots = applied_rots

    def get_permuted_points(self):
        return chain.from_iterable(self.vertice_points.values())

    def get_vertice_set(self):
        return set(self.vertice_points.keys())


class Scanner:
    def __init__(self, id, observations, permutations: List[Permutation]):
        self.id = id
        self.observations = observations
        self.permutations = permutations

        self.matches: List[MatchedScanner] = []


class MatchedScanner:
    def __init__(
        self,
        scanner: Scanner,
        permutation: Permutation,
        matching_points,
        distance_to_root,
    ):
        self.scanner = scanner
        self.permutation = permutation
        self.matching_points = matching_points
        self.distance_to_root = distance_to_root


# create 24 sets of rotated vertices in a map along with 2 points for each vertice
# also returns the roatations used to get to the vertices
# returns: Tuple[Permutation]
def create_permutations(P):
    original = P
    result = []
    applied_rots = []

    def calc_vertices():
        vertice_points = {}
        for p0, p1 in combinations(P, 2):
            v = (p0[0] - p1[0], p0[1] - p1[1], p0[2] - p1[2])
            assert v not in vertice_points
            vertice_points[v] = (p0, p1)
        return Permutation(vertice_points, tuple(applied_rots))

    result.append((calc_vertices(), True))  # [0] non rotated

    for rot_f, use_this in get_rotations_full_scan():
        P = tuple(rot_f(p) for p in P)
        applied_rots.append(rot_f)
        result.append((calc_vertices(), use_this))

    assert result[0][0].vertice_points == result[-1][0].vertice_points
    return tuple(r[0] for r in result if r[1])[:-1]


def pair_points(matching_vertices, left_points_by_vertice, right_points_by_vertice):
    # paired_points = set()
    # for v in matching_vertices:
    #     paired_points.add((left_points_by_vertice[v][0], right_points_by_vertice[v][0]))
    #     paired_points.add((left_points_by_vertice[v][1], right_points_by_vertice[v][1]))
    # return paired_points

    # To pair the points we id the points by their complete set of vertices
    pids0 = defaultdict(set)
    pids1 = defaultdict(set)
    for v in matching_vertices:
        for p in left_points_by_vertice[v]:
            pids0[p].add(v)
        for p in right_points_by_vertice[v]:
            pids1[p].add(v)

    pid_point0 = {frozenset(v): k for k, v in pids0.items()}
    pid_point1 = {frozenset(v): k for k, v in pids1.items()}
    assert pid_point0.keys() == pid_point1.keys()
    return [(pid_point0[vset], pid_point1[vset]) for vset in pid_point0.keys()]


# Given a left permutation (root scanner), find best matching permutation from list of permutations
def match_permutations(left_perm: Permutation, right_perms: List[Permutation]):
    bestmatch = ((dict(), tuple()), set())
    for perm in right_perms:
        matches = left_perm.get_vertice_set().intersection(perm.get_vertice_set())
        paired_points = pair_points(
            matches, left_perm.vertice_points, perm.vertice_points
        )
        if len(paired_points) > len(bestmatch[1]):
            bestmatch = (perm, paired_points)
    return bestmatch


def get_distance(matching_points):
    distances = set()
    for p0, p1 in matching_points:
        distances.add((p0[0] - p1[0], p0[1] - p1[1], p0[2] - p1[2]))
        assert len(distances) == 1
        return distances.pop()


def recursive_match(
    scanner: Scanner, permutation0, scanners: List[Scanner], path, distance
):
    for other in scanners:
        if other == scanner:
            continue
        step = frozenset({other.id, scanner.id})
        if step in path:
            continue

        matched_perm, paired_points = match_permutations(
            permutation0, other.permutations
        )
        if len(paired_points) >= 12:
            rel_dist = get_distance(paired_points)
            distance_to_root = tuple(a + b for a, b in zip(rel_dist, distance))

            matched_scanner = MatchedScanner(
                other, matched_perm, paired_points, distance_to_root
            )
            scanner.matches.append(matched_scanner)
            path.add(step)
            recursive_match(other, matched_perm, scanners, path, distance_to_root)


def parse_scanners(data):
    points_by_scannerid = defaultdict(list)

    scanner_id = "None"
    for line in data.split("\n"):
        line = line.strip()
        if line:
            if "--- scanner" in line:
                scanner_id = line.split(" ")[2]
            else:
                points_by_scannerid[scanner_id].append(
                    tuple((int(x) for x in line.split(",")))
                )

    return [
        Scanner(id, points, create_permutations(points))
        for id, points in points_by_scannerid.items()
    ]


def calculate(scanners, scanner0, permutation0):
    path = set()
    recursive_match(scanner0, permutation0, scanners, path, (0, 0, 0))

    all_observations = set()
    for p in permutation0.get_permuted_points():
        all_observations.add(p)

    for scanner in scanners:
        for match in scanner.matches:
            print(f"{match.scanner.id} dist {match.distance_to_root}")
            for p in match.permutation.get_permuted_points():
                all_observations.add(
                    tuple(a + b for a, b in zip(p, match.distance_to_root))
                )

    scanners_used = set(chain.from_iterable(path)) | {scanner0.id}

    return all_observations, scanners_used


def clear_matchresults(scanners):
    for scanner in scanners:
        scanner.matches.clear()


for num, data in enumerate(inputs, start=1):

    results = {}
    used_scanners = set()
    scanners = parse_scanners(data)
    for scanner in scanners:
        if not scanner.id in used_scanners:
            clear_matchresults(scanners)
            observations, scanners_used = calculate(
                scanners, scanner, scanner.permutations[0]
            )
            used_scanners.update(scanners_used)
            if len(scanners_used) > 1:
                results[scanner.id] = len(observations)

                print(
                    f"*** Used scanners: {list(sorted([int(x) for x in scanners_used]))} root: {scanner.id} observations: {len(observations)} ***"
                )
            else:
                print(f"Skip scanner with no overlaps {scanner.id}")

    print(f"Observations pr. root scanner: {results}")
    print(f"Used scanners: {list(sorted([int(x) for x in used_scanners]))}")
    print(
        f"Total observations (all groups): {functools.reduce(lambda a, b: a + b, results.values())}"
    )
