from itertools import pairwise
from pathlib import Path
import requests

YEAR = "2023"
DAY = "5"


def getinput():
    path = Path(f"{DAY}.txt")
    if not path.exists():
        sessionid = Path("../.secret").read_text().strip()
        res = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{DAY}/input",
            cookies={"session": sessionid},
        )
        path.write_text(res.text)
    return path.read_text()


def score(seed, maps):
    cur = seed
    for conversion in maps:
        for mapping in conversion:
            if mapping[1] <= cur < mapping[1] + mapping[2]:
                cur = mapping[0] + cur - mapping[1]
                break
    return cur


def solve(parsed):
    seeds, maps = parsed
    best = 10**12
    for seed in seeds:
        best = min(best, score(seed, maps))
    p1 = best

    best = 10**12
    for i in range(0, len(seeds) - 1, 2):
        seed0, rlength = seeds[i], seeds[i + 1]
        print(seed0, rlength)
        for seed in range(seed0, seed0 + rlength):
            best = min(best, score(seed, maps))
    p2 = best
    return p1, p2


def parse(input_: str):
    sections = input_.split("\n\n")
    seeds = list(map(int, sections[0].split(":")[1].strip().split(" ")))
    maps = []
    for mapsectios in sections[1:]:
        mappings = []
        for mapping in mapsectios.split("\n")[1:]:
            if not mapping:
                continue
            mappings.append(list(map(int, mapping.split(" "))))
        maps.append(mappings)
    return seeds, maps


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
    parsed = parse(input_)
    assert solve(parsed) == (35, 46)


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
