from pathlib import Path
import requests

YEAR = "2023"
DAY = "1"


def getinput():
    path = Path(f"{DAY}.txt")
    if not path.exists():
        sessionid = Path(".secret").read_text().strip()
        res = requests.get(
            f"https://adventofcode.com/{YEAR}/day/{DAY}/input",
            cookies={"session": sessionid},
        )
        path.write_text(res.text)
    return path.read_text()


def solve(parsed):
    return sum(int(f"{p[0]}{p[-1]}") for p in parsed)


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        digits = []
        # one, two, three, four, five, six, seven
        spelled = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
        for i in range(len(l)):
            if l[i].isdigit():
                digits.append((i, int(l[i])))
            else:
                for s in spelled:
                    if l[i:].startswith(s):
                        digits.append((i, spelled[s]))
                        break
        digits.sort()
        parsed.append([d[1] for d in digits])
        print(l)
        print(digits)

    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
    parsed = parse(input_)
    assert solve(parsed) == 281


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
