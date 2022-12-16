from functools import cache
from pathlib import Path

DAY = 16
full_input_ = Path(f"{DAY}.txt").read_text()

def solve(parsed):
    rates={p[0]:p[1] for p in parsed}
    nbs = {p[0]:p[2] for p in parsed}

    @cache
    def recurse(t, current, isopen):
        released = sum(rates[o] for o in isopen)

        if t == 30:
            return released

        openscore = 0
        if current not in isopen and rates[current] > 0:
            openscore = recurse(t + 1, current, tuple(sorted(isopen + (current,))))

        movescore = max(recurse(t + 1, nb, isopen) for nb in nbs[current])

        return released + max(openscore, movescore)

    return recurse(1, parsed[0][0], tuple())


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
    assert solve(parsed) == 1651


def testcustom():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Valve AA has flow rate=0; tunnels lead to valves BB,CC
Valve BB has flow rate=0; tunnels lead to valves CC, DD, AA
Valve CC has flow rate=2; tunnels lead to valves CC
Valve DD has flow rate=2; tunnels lead to valves DD
"""
    parsed = parse(input_)
    assert solve(parsed) == 28 * 2



def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
