from pathlib import Path

DAY = "16"
full_input_ = Path(f"{DAY}.txt").read_text()

gift_sue = """\
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""

"""In particular, the cats and trees readings indicates that there are greater than that many 
(due to the unpredictable nuclear decay of cat dander and tree pollen), 
while the pomeranians and goldfish readings indicate that there are fewer than that many 
(due to the modial interaction of magnetoreluctance).
"""


def checkp1(gift_sue_counts, c):
    for i, n in c.items():
        if i not in gift_sue_counts or gift_sue_counts[i] != n:
            return False
    return True


def checkp2(gift_sue_counts, c):
    for i, n in c.items():
        if i in ("cats", "trees"):
            if i not in gift_sue_counts:
                return False
            if n <= gift_sue_counts[i]:
                return False
        elif i in ("pomeranians", "goldfish"):
            if i in gift_sue_counts and n >= gift_sue_counts[i]:
                return False
        else:
            if i not in gift_sue_counts or gift_sue_counts[i] != n:
                return False

    return True


def solve(parsed):
    gift_sue_counts, sue_counts = parsed
    p1, p2 = 0, 0
    for idx, c in enumerate(sue_counts):
        if checkp1(gift_sue_counts, c):
            assert p1 == 0
            p1 = idx + 1
        if checkp2(gift_sue_counts, c):
            assert p2 == 0
            p2 = idx + 1

    return p1, p2


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = l.split(":", 1)
        counts = {
            k.strip(): int(v) for k, v in [n.split(":") for n in right.split(",")]
        }

        parsed.append(counts)
        gift_sue_counts = {
            k.strip(): int(v)
            for k, v in [n.split(":") for n in gift_sue.split("\n") if n.strip()]
        }

    return gift_sue_counts, parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\

"""
    parsed = parse(input_)
    # assert solve(parsed) == 42


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
