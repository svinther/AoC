# This brute force approach takes days to complete
# On my laptop with pypy it can process 3M serials per sec. 9^14 / 3M
# 9**14 / 3*1024**3 / (24*3600) --> 9.47 days

import math
import time
from pathlib import Path
from typing import NamedTuple, Optional, List, Dict, Union, Tuple

DAY = 24
full_input_ = Path("input.2021.24.txt").read_text()


class Instruction(NamedTuple):
    i: str
    o1: str
    o2: Optional[Union[int, str]] = None


def evaluate(literal: Union[str, int], state: Dict[str, int]) -> int:
    if isinstance(literal, int):
        return literal
    return state[literal]


cache = {}


def run(instructionset: Tuple[Instruction], pos, z, w):
    cache_key = (pos, z, w)
    if not cache_key in cache:
        state_d = {"x": 0, "y": 0, "z": z, "w": w}
        for instruction in instructionset:
            if instruction.i == "inp":
                assert False, "inp should be handled outside this"
            elif instruction.i == "add":
                state_d[instruction.o1] = state_d[instruction.o1] + evaluate(
                    instruction.o2, state_d
                )
            elif instruction.i == "mul":
                state_d[instruction.o1] = state_d[instruction.o1] * evaluate(
                    instruction.o2, state_d
                )
            elif instruction.i == "div":
                assert evaluate(instruction.o2, state_d) != 0
                state_d[instruction.o1] = state_d[instruction.o1] // evaluate(
                    instruction.o2, state_d
                )
            elif instruction.i == "mod":
                assert state_d[instruction.o1] >= 0
                assert evaluate(instruction.o2, state_d) > 0
                state_d[instruction.o1] = state_d[instruction.o1] % evaluate(
                    instruction.o2, state_d
                )
            elif instruction.i == "eql":
                state_d[instruction.o1] = (
                    1
                    if state_d[instruction.o1] == evaluate(instruction.o2, state_d)
                    else 0
                )
            else:
                assert False
        cache[cache_key] = state_d["z"]
    return cache[cache_key]


def split_instructions(parsed: List[Instruction]) -> List[Tuple[Instruction]]:
    splitted: List[Tuple[Instruction]] = []
    current: List[Instruction] = []
    for i in parsed:
        if i.i == "inp":
            if current:
                splitted.append(tuple(current))
                current = []
        else:
            current.append(i)

    if current:
        splitted.append(tuple(current))

    return splitted


t0 = time.process_time()


def recurse(instructionsets, serial, z, validserials, processed):
    if len(serial) == 14:
        if z == 0:
            validserials.append(serial)
            print(validserials)
            exit(0)
        processed[0] += 1
        if processed[0] % 10000000 == 0:
            t = time.process_time() - t0
            print(
                "processed serials",
                processed[0],
                "sps",
                math.floor(processed[0] / t),
                "current",
                serial,
            )
        return
    for w in reversed(range(1, 10)):
        new_z = run(instructionsets[len(serial)], len(serial), z, w)
        recurse(instructionsets, serial + str(w), new_z, validserials, processed)


def solve(parsed: List[Instruction]):
    instructionsets = split_instructions(parsed)
    assert len(instructionsets) == 14
    recurse(instructionsets, "", 0, [], [0])


def parse(input: str):
    parsed: List[Instruction] = []

    for l in input.split("\n"):
        l = l.strip()
        if not l:
            continue
        splitted = l.split(" ")
        inst, o1, o2 = None, None, None
        if len(splitted) == 3:
            inst, o1, o2 = splitted
        elif len(splitted) == 2:
            inst, o1 = splitted
            o2 = None

        if o2:
            try:
                o2 = int(o2)
            except ValueError:
                pass
        parsed.append(Instruction(inst, o1, o2))

    return parsed


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)
