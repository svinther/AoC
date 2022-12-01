from pathlib import Path

DAY = 3
full_input_ = Path(f"{DAY}.txt").read_text()

P = {chr(c): p for c, p in zip(range(ord("a"), ord("a") + 26), range(1, 27))}
P.update({chr(c): p for c, p in zip(range(ord("A"), ord("A") + 26), range(27, 53))})


def solvep2(parsed):
    total = 0
    sets = []
    for r in parsed:
        sets.append(set(r))
        if len(sets) == 3:
            i = sets[0].intersection(sets[1]).intersection(sets[2])
            assert len(i) == 1
            p = P[i.pop()]
            total += p
            sets = []

    return total


def solvep1(parsed):
    total = 0
    for r in parsed:
        left, right = set(r[: len(r) // 2]), set(r[len(r) // 2 :])
        i = left.intersection(right)
        ps = [P[c] for c in i]
        total += sum(ps)
    return total


def parse(input: str):
    parsed = []
    for l in input.split("\n"):
        l = l.strip()
        if not l:
            continue
        parsed.append(l)
    return parsed


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)
