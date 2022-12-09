from pathlib import Path
from typing import Tuple, List

DAY = 9
full_input_ = Path(f"{DAY}.txt").read_text()


def gen_normalized(parsed):
    for d, n in parsed:
        for _ in range(n):
            yield d


def solve(parsed, knots=2):
    # leftmost is H - snake[0]
    snake: List[Tuple[int, int]] = [(0, 0)] * knots

    visited = [{(0, 0)} for _ in range(knots)]

    for d in gen_normalized(parsed):
        H = snake[0]

        if d == "U":
            H = (H[0], H[1] + 1)
        elif d == "D":
            H = (H[0], H[1] - 1)
        elif d == "L":
            H = (H[0] - 1, H[1])
        else:
            assert d == "R"
            H = (H[0] + 1, H[1])

        snake[0] = H
        for n in range(1, len(snake)):
            H = snake[n - 1]
            T = snake[n]
            dist = (H[0] - T[0], H[1] - T[1])
            touching = (abs(dist[0]) + abs(dist[1]) <= 1) or (
                abs(dist[0]) == 1 and abs(dist[1]) == 1
            )
            if not touching:
                move = (
                    1 if dist[0] > 0 else -1 if dist[0] < 0 else 0,
                    1 if dist[1] > 0 else -1 if dist[1] < 0 else 0,
                )
                T = (T[0] + move[0], T[1] + move[1])
                snake[n] = T
                visited[n].add(T)

    return len(visited[-1])


def parse(input: str):
    parsed = []
    for l in input.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = l.split()
        parsed.append((left, int(right)))
    return parsed


def testp1():
    input_ = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
    parsed = parse(input_)
    result = solve(parsed)
    assert result == 13


def testp2():
    input_ = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
    parsed = parse(input_)
    result = solve(parsed, 10)
    assert result == 36


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)

    result = solve(parsed, 10)
    print(result)


if __name__ == "__main__":
    run()
