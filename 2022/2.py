from pathlib import Path

DAY = 2
full_input_ = Path(f"{DAY}.txt").read_text()

SYMBOL = {"A": "R", "X": "R", "Y": "P", "B": "P", "C": "S", "Z": "S"}

WINNERS = {("R", "S"), ("S", "P"), ("P", "R")}

POINTS = {"R": 1, "P": 2, "S": 3}


def score(l, r):
    rscore = 0
    lh = (l, r)
    rh = (r, l)

    rscore += POINTS[r]

    if rh in WINNERS:
        rscore += 6
    elif lh not in WINNERS:
        rscore += 3

    return rscore


def solvep1(parsed):
    rscore = 0
    for l, r in parsed:
        assert l in SYMBOL
        assert l in ("A", "B", "C")
        assert r in SYMBOL
        assert r in ("X", "Y", "Z")
        assert SYMBOL[l] in POINTS
        assert SYMBOL[r] in POINTS

        rscore += score(SYMBOL[l], SYMBOL[r])

    return rscore


def solvep2(parsed):
    rscore = 0
    for l, r in parsed:
        lsymbol = SYMBOL[l]

        # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
        if r == "Z":
            rwinner = [w for w in WINNERS if w[1] == lsymbol][0]
            rsymbol = rwinner[0]
        elif r == "X":
            lwinner = [w for w in WINNERS if w[0] == lsymbol][0]
            rsymbol = lwinner[1]
        else:
            rsymbol = lsymbol

        rscore += score(lsymbol, rsymbol)
    return rscore


def parse(input: str):
    parsed = []
    for l in input.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = l.split(" ")
        parsed.append((left, right))
    return parsed


def test_simple_p1():
    input_ = """\
A Y
B X
C Z
"""
    parsed = parse(input_)
    assert 15 == solvep1(parsed)


def test_double_p1():
    input_ = """\
A Y
B X
C Z
A Y
B X
C Z
"""
    parsed = parse(input_)
    assert 30 == solvep1(parsed)


def test_combos_p1():
    assert solvep1([("A", "X")]) == 3 + 1
    assert solvep1([("A", "Y")]) == 6 + 2
    assert solvep1([("A", "Z")]) == 0 + 3

    assert solvep1([("B", "X")]) == 0 + 1
    assert solvep1([("B", "Y")]) == 3 + 2
    assert solvep1([("B", "Z")]) == 6 + 3

    assert solvep1([("C", "X")]) == 6 + 1
    assert solvep1([("C", "Y")]) == 6 + 2
    assert solvep1([("C", "Z")]) == 0 + 3


if __name__ == "__main__":
    parsed = parse(full_input_)
    resultp1 = solvep1(parsed)
    print(resultp1)

    resultp2 = solvep2(parsed)
    print(resultp2)


# A for Rock, B for Paper, and C for Scissors.
# X for Rock, Y for Paper, and Z for Scissors.
#
# 1for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).
