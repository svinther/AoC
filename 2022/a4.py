from pathlib import Path

DAY = 4
full_input_ = Path(f"{DAY}.txt").read_text()


def solvep1(parsed):
    result = 0
    for p1, p2 in parsed:
        if p1[1] <= p2[1] and p1[0] >= p2[0]:
            result += 1
        elif p2[1] <= p1[1] and p2[0] >= p1[0]:
            result += 1
    return result


def solvep2(parsed):
    result = 0
    for p1, p2 in parsed:
        if p1[0] <= p2[1] and p1[1] >= p2[0]:
            result += 1
        elif p2[0] <= p1[1] and p2[1] >= p1[0]:
            result += 1
    return result


def parse(input: str):
    parsed = []
    for l in input.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = l.split(",")
        pairs = (
            tuple(int(x) for x in left.split("-")),
            tuple(int(x) for x in right.split("-")),
        )
        parsed.append(pairs)
    return parsed


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)
