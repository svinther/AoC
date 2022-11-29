from pathlib import Path
from typing import NamedTuple, Tuple

DAY = 17
YEAR = 2021
full_input_ = Path(f"input.{YEAR}.{DAY}.txt").read_text()


class Box(NamedTuple):
    xmin: int
    xmax: int
    ymin: int
    ymax: int


class VeloPos(NamedTuple):
    vx: int
    vy: int
    x: int
    y: int


def is_hit(velopos: VeloPos, box: Box):
    return box.xmin <= velopos.x <= box.xmax and box.ymin <= velopos.y <= box.ymax


def step(velopos: VeloPos) -> VeloPos:
    x_ = velopos.x + velopos.vx
    y_ = velopos.y + velopos.vy
    vx_ = 0 if velopos.vx == 0 else velopos.vx + 1 if velopos.vx < 1 else velopos.vx - 1
    vy_ = velopos.vy - 1
    return VeloPos(vx_, vy_, x_, y_)


def solve(box: Box) -> Tuple[int, int]:
    limitvx_min = 1
    maxy = -1
    initial_velocities = []
    while True:
        # xs = (vx * (vx+1)) / 2 (sum of first n natural numbers)
        if limitvx_min * (limitvx_min + 1) / 2 >= box.xmin:
            break
        limitvx_min += 1
    limitvx_max = box.xmax + 1

    limitvy_min = box.ymin - 1
    limitvy_max = -box.ymin + 1

    for vx in range(limitvx_min, limitvx_max + 1):
        for vy in range(limitvy_min, limitvy_max + 1):
            V = [VeloPos(vx, vy, 0, 0)]
            while True:
                s = step(V[-1])
                V.append(s)
                if is_hit(s, box):
                    maxy = max([maxy] + [vp.y for vp in V])
                    initial_velocities.append((vx, vy))
                    break
                if s.y < box.ymin:
                    break
    return maxy, len(initial_velocities)


def parse(input: str) -> Box:
    input = input.strip()
    _, data = input.split(":")
    left, right = data.split(",")
    _, xminmax = left.split("=")
    xmin, xmax = [int(z) for z in xminmax.split("..")]
    _, yminmax = right.split("=")
    ymin, ymax = [int(z) for z in yminmax.split("..")]
    return Box(xmin, xmax, ymin, ymax)


def test_p1():
    input_ = "target area: x=20..30, y=-10..-5"
    box = parse(input_)
    maxy, iv = solve(box)
    assert maxy == 45
    assert iv == 112


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)
