from pathlib import Path

DAY = 6
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed, size):
    parsed = parsed.strip()
    for i in range(len(parsed)):
        chunk = parsed[i : i + size]
        if len(set(chunk)) == size:
            return i + size


if __name__ == "__main__":
    result = solve(full_input_, 4)
    print(result)

    result = solve(full_input_, 14)
    print(result)
