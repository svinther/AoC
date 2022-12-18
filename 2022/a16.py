import time
from collections import defaultdict, deque
from functools import lru_cache
from itertools import combinations, chain
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


def solve(edges, maxtime, rates, initialopen):
    maxdepth = inf

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
            if nb not in edges:
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

    return recurse(0, "AA", initialopen)


def solvep1(parsed):
    rates = {n: rate for n, rate, nbs in parsed}
    return solve(compact(parsed), 30, rates, tuple())


def solvep2(parsed):
    rates = {n: rate for n, rate, nbs in parsed}
    edges = compact(parsed)

    valves = [e for e in edges if e != "AA"]
    opencombos = chain.from_iterable(
        [combinations(valves, l) for l in range(1, len(valves))]
    )

    best = 0
    i = 0
    t0 = t = time.process_time()
    for combo in opencombos:
        p1score, p1used = solve(
            {k: v for k, v in edges.items() if k == "AA" or k in combo},
            26,
            rates,
            tuple(),
        )
        p2score, p2used = solve(
            {k: v for k, v in edges.items() if k == "AA" or k not in combo},
            26,
            rates,
            tuple(),
        )
        best = max(best, p1score + p2score)

        i += 1
        if i % 100 == 0:
            t_ = time.process_time()
            print(i, 100 // (t_ - t), "tps", i // (t_ - t0), "tpstot")
            t = t_

    return best


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
    assert solvep1(parsed)[0] == 1651
    assert solvep2(parsed) == 1707


def run():
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)


if __name__ == "__main__":
    run()
