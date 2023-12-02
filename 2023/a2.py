from collections import defaultdict
from pathlib import Path
import requests

YEAR = "2023"
DAY = "2"


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


def solve(parsed):
    #12 red cubes, 13 green cubes, and 14 blue cubes
    limits = {"red": 12, "green": 13, "blue": 14}
    p1=0
    p2=[]
    for i, g in enumerate(parsed):
        p2i=defaultdict(int)
        p2.append(p2i)

        OK=True
        for s in g:
            for t, n in s.items():
                if n > limits.get(t, 0):
                    OK=False
                p2i[t] = max(p2i[t], n)
        if OK:
            p1+=i+1

    powers =[ p2i["red"] * p2i["blue"] * p2i["green"] for p2i in p2]

    return p1, sum(powers)

def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = l.split(": ")
        sets=right.split("; ")
        g=[]
        for s in sets:
            cubes = s.split(", ")
            s = {}
            for c in cubes:
                n, t = c.split(" ")
                s[t]=int(n)
            g.append(s)
        parsed.append(g)
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
    parsed = parse(input_)
    assert solve(parsed) == (8, 2286)




def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
