from operator import add, mul
from pathlib import Path

DAY = 18
full_input_ = Path(f"{DAY}.txt").read_text()


def reduce(parsedexpr: list, opprec):
    reducedexpr = parsedexpr[0:1]
    for p in range(1, len(parsedexpr), 2):
        left = reducedexpr.pop()
        op, right = parsedexpr[p : p + 2]
        if op in opprec[0]:
            reducedexpr.append(op(left, right))
        else:
            reducedexpr.append(left)
            reducedexpr.append(op)
            reducedexpr.append(right)

    if len(opprec) > 1:
        return reduce(reducedexpr, opprec[1:])

    assert len(reducedexpr) == 1
    return reducedexpr[0]


def eval_expr(strexpr, opprec):
    parsedexpr = []
    strp = 0
    while strp < len(strexpr):
        c = strexpr[strp]
        strp += 1
        if c in [chr(ord("0") + x) for x in range(10)]:
            parsedexpr.append(int(c))
        elif c == "+":
            assert parsedexpr is not None
            parsedexpr.append(add)
        elif c == "*":
            assert parsedexpr is not None
            parsedexpr.append(mul)
        elif c == "(":
            subexpr, strp_ = eval_expr(strexpr[strp:], opprec)
            parsedexpr.append(subexpr)
            strp += strp_
        elif c == ")":
            break
        elif c == " ":
            continue
        else:
            assert False
    assert parsedexpr is not None

    return reduce(parsedexpr, opprec), strp


def solve(input_: str):
    p1 = []
    p2 = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        p1.append(eval_expr(l, ((add, mul),)))
        p2.append(eval_expr(l, ((add,), (mul,))))
    return sum([p[0] for p in p1]), sum([p[0] for p in p2])


def test1():
    opprec = ((add, mul),)
    assert eval_expr("1+4", opprec)[0] == 5
    assert eval_expr("1+4*3", opprec)[0] == 15
    assert eval_expr("1+(4*3)", opprec)[0] == 13
    assert eval_expr("1+ (4* 3)", opprec)[0] == 13
    assert eval_expr("1+ (4* (1+2))", opprec)[0] == 13


def test2():
    opprec = ((add,), (mul,))
    assert eval_expr("1+4*3", opprec)[0] == 15
    assert eval_expr("4*3+1", opprec)[0] == 16
    assert eval_expr("8 * 3 + 9 + 3 * 4 * 3", opprec)[0] == 1440

    assert eval_expr("1 + (2 * 3) + (4 * (5 + 6))", opprec)[0] == 51
    assert eval_expr("2 * 3 + (4 * 5)", opprec)[0] == 46
    assert eval_expr("5 + (8 * 3 + 9 + 3 * 4 * 3)", opprec)[0] == 1445
    assert eval_expr("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", opprec)[0] == 669060
    assert (
        eval_expr("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", opprec)[0] == 23340
    )


def run():
    result = solve(full_input_)
    print(result)


if __name__ == "__main__":
    run()
