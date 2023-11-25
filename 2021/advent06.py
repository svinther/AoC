from collections import defaultdict, Counter
from functools import reduce
from operator import itemgetter

year = 2021
day = 6

inputs = ["3,4,3,1,2"]

with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())


for num, data in enumerate(inputs, start=1):
    A = defaultdict(int)
    for a in data.split(","):
        A[int(a)] += 1

    for _ in range(256):
        newA = defaultdict(int, {a - 1: A[a] for a in A.keys() if a > 0})
        newA[6] += A[0]
        newA[8] = A[0]
        A = newA

    print(reduce(lambda a, b: a + b, A.values()))
