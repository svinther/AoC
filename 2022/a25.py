from pathlib import Path
from typing import List

DAY = 25
full_input_ = Path(f"{DAY}.txt").read_text()

def numberToBase(n: int, b: int) -> List[int]:
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def dec_to_snafu(num: int) -> str:
    base5 = numberToBase(num, 5)
    result = []
    flip = 0
    for i in [int(c) for c in reversed(base5)]:
        actual = flip + i
        flip = (actual + 2) // 5
        remain = actual - flip * 5
        result.append(remain)
    if flip:
        result.append(flip)

    return "".join(reversed(["=-012"[x + 2] for x in result]))


def snafu_to_dec(snafu: str) -> int:
    result = 0
    for p, s in enumerate(reversed(snafu)):
        numeric = "=-012".index(s) - 2
        result += numeric * 5**p
    return result


def test_snafu():
    nums = """\
1=-0-2     1747
 12111      906
  2=0=      198
    21       11
  2=01      201
   111       31
 20012     1257
   112       32
 1=-1=      353
  1-12      107
    12        7
    1=        3
   122       37
"""
    for l in [l.strip() for l in nums.split("\n") if l.strip()]:
        l = [n for n in l.split() if n]
        snafu, dec = l
        dec = int(dec)
        assert dec_to_snafu(dec) == snafu
        assert snafu_to_dec(snafu) == dec


def solve(parsed):
    dec = sum(snafu_to_dec(s) for s in parsed)
    return dec, dec_to_snafu(dec)


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(l)
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    print()
    input_ = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122            
"""
    parsed = parse(input_)
    assert solve(parsed) == (4890, "2=-1=0")


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result[1])


if __name__ == "__main__":
    run()
