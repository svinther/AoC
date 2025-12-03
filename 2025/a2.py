import re
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def solvep1(parsed):
    answer = 0
    for rng in parsed[0].split(","):
        b, e = map(int, rng.split("-"))
        for i in range(b, e + 1):
            s = str(i)
            l = len(s)
            if l % 2 == 0 and s[: l // 2] == s[l // 2 :]:
                answer += i
    return answer


def solvep2(parsed):
    answer = 0
    for rng in parsed[0].split(","):
        b, e = map(int, rng.split("-"))
        for i in range(b, e + 1):
            s = str(i)
            l = len(s)
            for l0 in range(1, l // 2 + 1):
                if l % l0 != 0:
                    continue
                last = None
                for j in range(l0, l + 1, l0):
                    chunk = s[j - l0 : j]
                    if last and last != chunk:
                        break
                    # print(b,e,i,j,chunk)
                    last = chunk
                else:
                    break
            else:
                continue
            # print(b,e,i)
            answer += i

    return answer


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(l)
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,\
1698522-1698528,446443-446449,38593856-38593862,565653-565659,\
824824821-824824827,2121212118-2121212124
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 1227775554
    assert solvep2(parsed) == 4174379265


def run():
    input_ = open(0).read()
    parsed = parse(input_)
    p1result = solvep1(parsed)
    print(p1result)

    parsed = parse(input_)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
