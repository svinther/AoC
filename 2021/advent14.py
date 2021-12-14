from collections import defaultdict, Counter
from operator import itemgetter

year = 2021
day = 14

inputs = [
    """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
]

with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())


def run_for_pair(db, pair, cur, max, cache):
    cache_key = (pair, cur)
    if cache_key in cache:
        return cache[cache_key]

    counts_=defaultdict(int)

    p0, p1 = pair
    px = db[pair]
    counts_[px] += 1

    if cur < max:
        for p, count in run_for_pair(db, (p0, px), cur + 1, max, cache).items():
            counts_[p] += count

        for p, count in run_for_pair(db, (px, p1), cur + 1, max, cache).items():
            counts_[p] += count

    cache[cache_key] = counts_
    return counts_

# Used for part 1
def step(db, seq):
    result = []
    for pos in range(len(seq) - 1):
        p0, p1 = seq[pos:pos + 2]
        lookup = db[(p0, p1)]
        result.append(p0)
        result.append(lookup)
    result.append(seq[-1])
    return result


def all_steps(db, seq, steps):
    cache={}
    counts = defaultdict(int)
    # This counts all the items we insert to original sequence
    for pos in range(len(seq) - 1):
        pair = tuple(seq[pos:pos + 2])
        counts_ = run_for_pair(db, pair, 0, steps - 1, cache)
        for p, count in counts_.items():
            counts[p] += count
        # run_for_pair2(db, pair, counts, steps)
    # add the original sequence items
    for c, count in Counter(seq).items():
        counts[c] += count
    return counts


def print_result(counts):
    counts_sorted = sorted(counts.items(), key=itemgetter(1))
    least_x, least_num = counts_sorted[0]
    most_x, most_num = counts_sorted[-1]
    print(f"Least {least_x}/{least_num}  -  most {most_x}/{most_num}  -> Result: {most_num - least_num}")


for num, data in enumerate(inputs, start=1):

    S = []
    M = {}

    for line in data.split("\n"):
        stripped = line.strip()
        if stripped:
            if not S:
                S.append(list(stripped))
            else:
                pair, garb, ins = stripped.split(" ")
                M[tuple(pair)] = ins

    for i in range(10):
        S.append(step(M, S[-1]))

    # Analyze
    print(f"Run number {num}")
    counts = Counter(S[-1])
    print_result(counts)

    # 2
    # Compare with results from #1
    counts = all_steps(M, S[0], 10)
    print_result(counts)

    # Now for real
    counts = all_steps(M, S[0], 40)
    print_result(counts)

