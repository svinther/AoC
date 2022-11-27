import time
from typing import List, Tuple, NamedTuple, Optional, Dict, Set

from sortedcontainers import SortedDict

CAVEX: Dict[int, str] = {3: "A", 5: "B", 7: "C", 9: "D"}
CAVEX_INV: Dict[str, int] = {v: k for k, v in CAVEX.items()}

HALLWAY_XMIN = 1
HALLWAY_XMAX = 11

HALLWAY_Y = 3
CAVE_Y_MIN = 1
CAVE_Y_MAX = 2


class Coord(NamedTuple):
    x: int
    y: int


class StateEntry(NamedTuple):
    coord: Coord
    app: str


State = Tuple[StateEntry]


def get_from_state(state: State, coord: Coord) -> Optional[str]:
    l = [x[1] for x in state if x[0] == coord]
    if l:
        assert len(l) == 1
        return l[0]
    return None


class Transition(NamedTuple):
    cost: int
    state: State


MOVE_COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


def transition(state: State, start: Coord, dest: Coord) -> Transition:
    assert dest not in state
    moves_y = HALLWAY_Y - start.y + HALLWAY_Y - dest.y
    moves_x = abs(start.x - dest.x)
    app_to_move = get_from_state(state, start)
    cost = MOVE_COST[app_to_move] * (moves_x + moves_y)
    next_state: State = tuple(
        sorted(
            StateEntry(c, a)
            for c, a in state + (StateEntry(dest, app_to_move),)
            if c != start
        )
    )
    t = Transition(cost, next_state)
    return t


def moves(state: State) -> List[Transition]:
    cave_transitions: List[Transition] = []
    hallway_transitions: List[Transition] = []

    for coord, app in state:
        cavex = CAVEX_INV[app]

        if coord.x in CAVEX:
            assert coord.y in range(CAVE_Y_MIN, CAVE_Y_MAX + 1)
            cave_blocked = {s.coord for s in state}.intersection(
                Coord(coord.x, y) for y in range(coord.y + 1, CAVE_Y_MAX + 1)
            )
            if cave_blocked:
                # no moves possible
                continue

            if coord.x == cavex:
                # in home cave
                move_for_others = {s.coord for s in state if s.app != app}.intersection(
                    Coord(coord.x, y) for y in range(CAVE_Y_MIN, coord.y)
                )
                if not move_for_others:
                    # stay home at final destination
                    continue

            # We can only move to the hallway
            # left spots available
            for x in filter(
                lambda x: x not in CAVEX, reversed(range(HALLWAY_XMIN, coord.x))
            ):
                if Coord(x, HALLWAY_Y) in {s.coord for s in state}:
                    # hallway blocked by another app
                    break
                # free spot here
                hallway_transitions.append(
                    transition(state, coord, Coord(x, HALLWAY_Y))
                )

            # or to hallway right
            for x in filter(
                lambda x: x not in CAVEX, range(coord.x + 1, HALLWAY_XMAX + 1)
            ):
                if Coord(x, HALLWAY_Y) in {s.coord for s in state}:
                    # hallway blocked by another app
                    break
                # free spot here
                hallway_transitions.append(
                    transition(state, coord, Coord(x, HALLWAY_Y))
                )

        # not in home cave, and if in another cave we are not blocked, is home cave ready to habitate
        home_cave_blocked = {s.coord for s in state if s.app != app}.intersection(
            Coord(cavex, y) for y in range(CAVE_Y_MIN, CAVE_Y_MAX + 1)
        )
        if not home_cave_blocked:
            hallway_blocked = {s.coord for s in state}.intersection(
                Coord(x, HALLWAY_Y)
                for x in range(min(cavex, coord.x + 1), max(cavex + 1, coord.x))
            )
            if not hallway_blocked:
                # make the jump
                dest_y = min(
                    y
                    for y in range(CAVE_Y_MIN, CAVE_Y_MAX + 1)
                    if y not in {s.coord.y for s in state if s.coord.x == cavex}
                )
                cave_transitions.append(transition(state, coord, Coord(cavex, dest_y)))
                continue

    if cave_transitions:
        return cave_transitions
    return hallway_transitions


# this only works for part1
def render(state: State):
    level = """\
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #########    
"""
    lines = [list(l) for l in level.split("\n") if l.strip()]
    lines.reverse()
    for coord, app in state:
        lines[coord.y][coord.x] = app

    return "\n".join(reversed(["".join(line) for line in lines]))


def render_all(transitions: List[Transition]):
    print("***RENDER***")
    for i, t in enumerate(transitions):
        print(i, t.cost)
        print(render(t.state))


def solve(state: State, end: State):
    costs: Dict[State, int] = {state: 0}
    last: Dict[State, Optional[State]] = {state: None}
    # min_costs_to_finish: Dict[State, int] = {state: min_cost_to_finish(state, 0)}
    visited: Set[State] = set()
    Q: Set[State] = set()

    # Dict[int,Set[State]]
    S = SortedDict()

    S.setdefault(0, set()).add(state)
    Q = {state}
    t0 = time.process_time()
    while True:
        assert sum([len(s) for s in S.values()]) == len(Q)
        current_cost, current_cost_bucket = S.peekitem(index=0)
        current = current_cost_bucket.pop()
        if current not in Q:
            print()
        if not current_cost_bucket:
            del S[current_cost]
        Q.remove(current)
        assert sum([len(s) for s in S.values()]) == len(Q)

        if current == end:
            # This rendering only works for part1
            # last_ = current
            # while True:
            #     if not last_:
            #         break
            #     print(render(last_))
            #     last_ = last[last_]

            return current, costs[current]

        assert current not in visited

        visited.add(current)
        visited_count = len(visited)
        if visited_count % 500 == 0:
            t = time.process_time()
            print(f"Visited {visited_count}", visited_count / (t - t0))
        Tnew = moves(current)
        for t_cost, t_state in Tnew:
            cost = t_cost + current_cost
            if t_state not in costs:
                # Never seen this state before
                costs[t_state] = cost
                last[t_state] = current

                S.setdefault(cost, set()).add(t_state)
                Q.add(t_state)
                assert sum([len(s) for s in S.values()]) == len(Q)
            elif costs[t_state] > cost:
                # Found cheaper path to t_state, update the cost in S
                assert t_state not in visited
                old_cost = costs[t_state]
                costs[t_state] = cost
                if t_state in Q:
                    cost_bucket = S[old_cost]
                    cost_bucket.remove(t_state)
                    if not cost_bucket:
                        del S[old_cost]
                    S.setdefault(cost, set()).add(t_state)
                    assert sum([len(s) for s in S.values()]) == len(Q)
            elif t_state in visited:
                assert t_state not in Q
                assert t_state not in S.get(cost, set())


def parse(input: str) -> State:
    state_: List[StateEntry] = []
    lines = [l for l in input.split("\n") if l.strip()]
    lines.reverse()
    for y in range(0, len(lines)):
        for x, f in enumerate(lines[y]):
            if f in ("A", "B", "C", "D"):
                state_.append(StateEntry(Coord(x, y), f))
    return tuple(sorted(state_))


END = parse(
    """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""
)


def test_tuple_cmp():
    assert END == parse(
        """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""
    )


def test_simple1():
    input = """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########    
"""
    result, cost = solve(parse(input), END)
    print(result, cost)
    assert cost == 0


def test_simple2():
    input = """\
#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #########    
"""
    result, cost = solve(parse(input), END)
    print(result, cost)
    assert cost == MOVE_COST["D"] * 3


def test_simple3():
    input = """\
#############
#...........#
###A#B#D#C###
  #A#B#C#D#
  #########    
"""
    result, cost = solve(parse(input), END)
    print(result, cost)
    assert cost == MOVE_COST["D"] * 4 + MOVE_COST["C"] * 6


def test_simple4():
    input = """\
#############
#...........#
###A#B#D#D###
  #A#B#C#C#
  #########    
"""
    result, cost = solve(parse(input), END)
    print(result, cost)
    assert cost == MOVE_COST["D"] * (2 + 5 + 2) + MOVE_COST["C"] * (5 + 2)


def test_simple5():
    input = """\
#############
#DD.........#
###A#B#C#.###
  #A#B#C#.#
  #########    
"""
    result, cost = solve(parse(input), END)
    print(result, cost)
    assert cost == MOVE_COST["D"] * 9 * 2


def test_simple6():
    input = """\
#############
#D..C.....D.#
###A#B#.#.###
  #A#B#C#.#
  #########    
"""
    result, cost = solve(parse(input), END)
    print(result, cost)
    assert cost == MOVE_COST["D"] * 10 + MOVE_COST["D"] * 2 + MOVE_COST["C"] * 4


def test_simple7():
    input = """\
#############
#.....C...D.#
###A#B#D#.###
  #A#B#C#.#
  #########    
"""
    result, cost = solve(parse(input), END)
    print(result, cost)
    assert cost == MOVE_COST["D"] * 5 + MOVE_COST["D"] * 2 + MOVE_COST["C"] * 2


def test_part1_ex1():
    input = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########    
"""
    result, cost = solve(parse(input), END)
    print(result, cost)
    assert cost == 12521


def solve_part_1():
    input = """\
#############
#...........#
###B#B#C#D###
  #D#A#A#C#
  #########
"""
    result, cost = solve(parse(input), END)
    print(result, cost)


def solve_part_2():
    global HALLWAY_Y, CAVE_Y_MAX, CAVE_Y_MIN
    HALLWAY_Y = 5
    CAVE_Y_MIN = 1
    CAVE_Y_MAX = 4

    END = parse(
        """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
"""
    )

    input = """\
#############
#...........#
###B#B#C#D###
  #D#C#B#A#
  #D#B#A#C#
  #D#A#A#C#
  #########
"""
    result, cost = solve(parse(input), END)
    print(result, cost)


if __name__ == "__main__":
    solve_part_2()
