from pathlib import Path
import requests

YEAR = "2023"
DAY = "4"


def getinput():
    path = Path(f"{DAY}.txt")
    if not path.exists():
        sessionid = Path("../.secret").read_text().strip()
        res = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{DAY}/input",
            cookies={"session": sessionid},
        )
        path.write_text(res.text)
    return path.read_text()


def solvep1(parsed):
    p1 = 0
    for wins, nums in parsed:
        score = 0
        for n in nums:
            if n in wins:
                score += 1
        if score:
            p1 += 2 ** (score - 1)
    return p1


def solvep2(parsed):
    boardcounts = [1] * len(parsed)
    for i in range(len(parsed)):
        wins, nums = parsed[i]
        score = sum(1 for n in nums if n in wins)
        for j in range(i + 1, i + 1 + score):
            if j == len(parsed):
                break
            boardcounts[j] += boardcounts[i]
    return sum(boardcounts)


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, nums_ = l.split("|")
        wins_ = left.split(":")[1]
        wins = {int(w) for w in wins_.strip().split(" ") if w}
        nums = [int(n) for n in nums_.strip().split(" ") if n]
        parsed.append((wins, nums))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
    parsed = parse(input_)
    assert solvep1(parsed) == 13
    assert solvep2(parsed) == 30


def run():
    parsed = parse(getinput())
    result = solvep1(parsed), solvep2(parsed)
    print(result)


if __name__ == "__main__":
    run()
