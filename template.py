from pathlib import Path

DAY = 1
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed):
    pass


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
    result = solve(parsed)
    print(result)
