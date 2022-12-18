from collections import defaultdict, deque
from functools import lru_cache
from math import inf
from pathlib import Path

DAY = 16
full_input_ = Path(f"{DAY}.txt").read_text()


def compact(parsed):
    N = {n for n, rate, nbs in parsed if rate > 0}
    nbs = {n: nbs for n, rate, nbs in parsed}

    edges = defaultdict(dict)

    for n in N | {"AA"}:
        Q = deque([(n, 0)])
        visited = set()
        while Q:
            current, dist = Q.popleft()
            visited.add(current)
            if current != n and current in N:
                edges[n][current] = dist
            for nb in nbs[current]:
                if nb not in visited:
                    Q.append((nb, dist + 1))
    return edges


def solvep1(parsed):
    edges = compact(parsed)
    rates = {n: rate for n, rate, nbs in parsed}
    maxdepth = inf
    maxtime = 30

    @lru_cache(maxsize=None)
    def recurse(t, current, isopen):
        if maxdepth == len(isopen):
            return 0, isopen

        score = sum(rates[o] for o in isopen)
        if rates[current] > 0:
            # spend one sec opening valve
            isopen = tuple(sorted(isopen + (current,)))
            t += 1
        pressure = sum(rates[o] for o in isopen)

        bestmovescore = 0, isopen
        for nb, cost in edges[current].items():
            if nb in isopen:
                continue
            assert nb != "AA"
            if t + cost <= maxtime:
                recurse_score, isopen_ = recurse(t + cost, nb, isopen)
                movescore = score + pressure * cost + recurse_score
                if movescore > bestmovescore[0]:
                    bestmovescore = movescore, isopen_

        if bestmovescore[0] == 0:
            return score + pressure * (maxtime - t), isopen
        return bestmovescore

    score, isopen = recurse(0, "AA", tuple())
    print(score, isopen)

    return score


def solvep2(parsed):
    edges = compact(parsed)
    rates = {n: rate for n, rate, nbs in parsed}
    maxtime = 26

    cache = {}

    def recurse(t1, t2, c1, c2, o1, o2):
        cachekey = (t1, t2, c1, c2, o1, o2)
        if cachekey not in cache:
            # print(t1, t2, c1, c2, o1, o2)
            p1, p2 = sum(rates[o] for o in o1), sum(rates[o] for o in o2)
            p1_, p2_ = p1 + rates[c1], p2 + rates[c2]

            # t time for opening valve
            dt1 = 1 if rates[c1] > 0 else 0
            dt2 = 1 if rates[c2] > 0 else 0

            movescores = []
            for nb, cost in edges[c1].items():
                if nb in o1 + o2 or nb == c2:
                    continue
                if t1 + dt1 + cost <= maxtime:
                    movescores.append(
                        p1
                        + p1_ * cost
                        + recurse(
                            t1 + dt1 + cost, t2, nb, c2, tuple(sorted(o1 + (c1,))), o2
                        )
                    )

            for nb, cost in edges[c2].items():
                if nb in o1 + o2 or nb == c1:
                    continue
                if t2 + dt2 + cost <= maxtime:
                    movescores.append(
                        p2
                        + p2_ * cost
                        + recurse(
                            t1, t2 + dt2 + cost, c1, nb, o1, tuple(sorted(o2 + (c2,)))
                        )
                    )

            if not movescores:
                cache[cachekey] = (
                    p1 + p1_ * (maxtime - t1 - dt1) + p2 + p2_ * (maxtime - t2 - dt2)
                )
            else:
                cache[cachekey] = max(movescores)

            if len(cache) % 100000 == 0:
                print(len(cache))

        return cache[cachekey]

    score = recurse(0, 0, "AA", "AA", tuple(), tuple())

    return score


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        spl = l.split(" ", 9)
        nbs = [nb.strip() for nb in spl[-1].split(",")]
        valve = spl[1]
        flowrate = int(spl[4].split("=")[-1][:-1])
        parsed.append((valve, flowrate, tuple(nbs)))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 1651
    assert solvep2(parsed) == 1707


def run():
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)


if __name__ == "__main__":
    run()
