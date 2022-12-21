from functools import reduce
from operator import add, mul
from pathlib import Path
from typing import NamedTuple

DAY = 19
full_input_ = Path(f"{DAY}.txt").read_text()


class Entry(NamedTuple):
    ore: int
    cla: int
    obs: int
    geo: int


class Blueprint(NamedTuple):
    ore: Entry
    cla: Entry
    obs: Entry
    geo: Entry


def spend(costs, resources):
    return Entry(*(b - a for a, b in zip(costs, resources)))


def canafford(costs, resources):
    return min(spend(costs, resources)) >= 0


def collect(robots, resources):
    return Entry(*(a + b for a, b in zip(robots, resources)))


def recurse(blueprint, maxtime, time, robots, resources, cache):
    cachekey = (time, robots, resources)
    if cachekey in cache:
        return cache[cachekey]

    if time == maxtime:
        return resources.geo
    assert time < maxtime

    best = 0
    for i, costs in reversed(list(enumerate(blueprint))):
        build = True

        #  robots * timeleft + resources  > max resources can be spent if building most expensive robot each min
        if i < 3 and robots[i] * (maxtime - time) + resources[i] >= (
            maxtime - time
        ) * max(r[i] for r in blueprint):
            build = False

        if build and canafford(costs, resources):
            resources_ = spend(costs, resources)
            robots_ = Entry(
                *tuple(robots[r] + (1 if i == r else 0) for r in range(len(robots)))
            )
            best = max(
                best,
                recurse(
                    blueprint,
                    maxtime,
                    time + 1,
                    robots_,
                    collect(robots, resources_),
                    cache,
                ),
            )
            if i == 3:
                cache[cachekey] = best
                return best

    best = max(
        best,
        recurse(
            blueprint, maxtime, time + 1, robots, collect(robots, resources), cache
        ),
    )
    cache[cachekey] = best
    return best


def solvep1(parsed):
    qualitylevels = []
    for i, blueprint in enumerate(parsed):
        robots = Entry(1, 0, 0, 0)
        resources = Entry(0, 0, 0, 0)
        cracked = recurse(blueprint, 24, 0, robots, resources, {})
        qualitylevels.append((i + 1, cracked))
    return reduce(add, [a * b for a, b in qualitylevels])


def solvep2(parsed):
    scores = []
    for blueprint in parsed[:3]:
        robots = Entry(1, 0, 0, 0)
        resources = Entry(0, 0, 0, 0)
        cracked = recurse(blueprint, 32, 0, robots, resources, {})
        scores.append((cracked))
        print(scores)
    return scores


# Blueprint 6: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 11 clay. Each geode robot costs 2 ore and 10 obsidian.


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = l.split(":")
        amounts = right.split(".")
        parsed.append(
            Blueprint(
                Entry(int(amounts[0].split()[4]), 0, 0, 0),
                Entry(int(amounts[1].split()[4]), 0, 0, 0),
                Entry(int(amounts[2].split()[4]), int(amounts[2].split()[7]), 0, 0),
                Entry(int(amounts[3].split()[4]), 0, int(amounts[3].split()[7]), 0),
            )
        )

    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian.
"""

    parsed = parse(input_)
    assert solvep1(parsed) == 33


def run():
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)
    print(reduce(mul, result))


if __name__ == "__main__":
    run()
