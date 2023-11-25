from pathlib import Path
from collections import deque

DAY = "14"
full_input_ = Path(f"{DAY}.txt").read_text()

def combos(m):
    Q=deque([(0, [])])
    while Q:
        i, s = Q.popleft()
        if i==36:
            yield "".join(s)
            continue
        if m[i] == "X":
            s1=s.copy()
            s.append("X")
            Q.append((i+1, s))
            s1.append("x")
            Q.append((i+1, s1))
        else:
            s.append(m[i])
            Q.append((i+1, s))

def solve(parsed):
    mem = {}
    for p in parsed:
        for addr, num in p[1:]:
            for mask in combos(p[0]):
                for i, c in enumerate(mask[::-1]):
                    if c == "1":
                        addr |= 2**i
                    elif c == "X":
                        addr |= 2**i
                    elif c == "x":
                        addr &= ~(2**i)
                mem[addr] = num
    return sum(mem.values())

def parse(input_: str):
    parsed = []
    cur=None
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = [x.strip() for x in l.split("=")]
        if left == "mask":
            if cur:
                parsed.append(cur)
            cur=[right]
        else:
            cur.append((int(left[4:-1]), int(right)))
    parsed.append(cur)
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""
    parsed = parse(input_)
    assert solve(parsed) == 208


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
