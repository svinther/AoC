from pathlib import Path
import requests

YEAR = "2023"
DAY = "15"


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


def hashit(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def solve(parsed):
    p1 = 0
    for s in parsed:
        h = hashit(s)
        p1 += h

    p2 = 0
    boxes = [{} for _ in range(256)]
    for s in parsed:
        if "=" in s:
            v, focal = s.split("=")
            boxes[hashit(v)][v] = int(focal)
        else:
            v = s[: len(s) - 1]
            h = hashit(v)
            if v in boxes[h]:
                del boxes[h][v]

    for i in range(256):
        if boxes[i]:
            for j, (v, focal) in enumerate(boxes[i].items()):
                pow = (i + 1) * (j + 1) * focal
                p2 += pow
                print(v, (i + 1), (j + 1), focal, pow)

    return p1, p2


def parse(input_: str):
    strings = [x.strip() for x in input_.split(",")]
    return strings


def testp1p2():
    print()
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
    parsed = parse(input_)
    assert solve(parsed) == (1320, 145)


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
