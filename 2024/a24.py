import re
import sys
from itertools import *
from heapq import *
from collections import *


def ints(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def solve(inputs, outputs):
    ops = {
        "OR": lambda a, b: a | b,
        "AND": lambda a, b: a & b,
        "XOR": lambda a, b: a ^ b,
    }

    def rec(w):
        if w in inputs:
            return inputs[w]

        l, op, r = outputs[w]
        return ops[op](rec(l), rec(r))

    zkeys = [o for o in outputs.keys() if o.startswith("z")]
    zkeys.sort(reverse=True)
    zvals = [rec(zk) for zk in zkeys]
    return int("".join(map(str, zvals)), 2)


def solvep1(parsed):
    wires, gates = parsed
    outputs = {d: (a, b, c) for a, b, c, d in gates}
    inputs = {a: b for a, b in wires}
    return solve(inputs, outputs)


def solvep2(parsed):
    wires, gates = parsed

    outputs = {d: (a, b, c) for a, b, c, d in gates}
    input_values = {a: b for a, b in wires}

    def render():
        print("digraph {")
        for gi, (g1, op, g2, gout) in enumerate(gates):
            gate = f"G{gi:03}"
            print(f"{gate} [label={op}]")
            print(f"{g1} -> {gate}")
            print(f"{g2} -> {gate}")
            print(f"{gate} -> {gout}")
        print("}")

    def compute(x, y):
        for bit, inid in enumerate(
            sorted(inp for inp in input_values.keys() if inp.startswith("x"))
        ):
            input_values[inid] = 1 if x & (1 << bit) else 0

        for bit, inid in enumerate(
            sorted(inp for inp in input_values.keys() if inp.startswith("y"))
        ):
            input_values[inid] = 1 if y & (1 << bit) else 0

        return solve(input_values, outputs)

    bad_zbits = []
    for bit in range(45):
        x, y = (
            1 << bit,
            1 << bit,
        )
        zx = compute(x, 0)
        zy = compute(0, y)
        assert zx == zy
        if x != zx:
            bad_zbits.append(bit)

    def subgates(gate):
        sub = set()
        a, _, b = outputs[gate]

        sub.add(a)
        sub.add(b)

        if not a[0] in ("x", "y"):
            sub.update(subgates(a))
        if not b[0] in ("x", "y"):
            sub.update(subgates(b))
        return sub

    for bit in range(45):
        zgate = f"z{bit:02}"
        print(zgate)
        print(subgates(zgate))


def parse(input_: str):
    wires, gates = input_.split("\n\n")
    wires = [(w, int(v)) for w, v in [l.split(": ") for l in wires.split("\n") if l]]
    gates = [
        (a, b, c, d) for a, b, c, _, d in [l.split() for l in gates.split("\n") if l]
    ]

    return wires, gates


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\

"""
    parsed = parse(input_)
    # assert solvep1(parsed) == 42


def run():
    input_ = open(0).read()
    # parsed = parse(input_)
    # p1result = solvep1(parsed)
    # print(p1result)

    parsed = parse(input_)
    p2result = solvep2(parsed)
    print(p2result)


if __name__ == "__main__":
    run()
