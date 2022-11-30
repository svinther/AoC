from pathlib import Path

DAY = 1
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed):
    sums = [sum(e) for e in parsed]
    sums.sort()
    return max(sums), sum(sums[-3:])


def parse(input: str):
    A = []
    current = []
    for l in input.split("\n"):
        l = l.strip()
        if not l:
            if current:
                A.append(current)
                current = []
            continue
        cals = int(l)
        current.append(cals)
    if current:
        A.append(current)
    return A


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)
