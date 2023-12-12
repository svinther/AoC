from functools import lru_cache
from pathlib import Path
import requests

YEAR = "2023"
DAY = "12"


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


def dp(springs, nums):
    n = len(springs)
    m = len(nums)

    @lru_cache(None)
    def arrs(i, j):
        if j == m:
            return 1 if all(c != "#" for c in springs[i:]) else 0
        if i >= n:
            return 0

        if springs[i] == ".":
            return arrs(i + 1, j)

        assert springs[i] in "?#"
        score = arrs(i + 1, j) if springs[i] == "?" else 0

        # can we get a num
        if i + nums[j] <= n and all(c in "#?" for c in springs[i : i + nums[j]]):
            if j < m - 1:
                if i + nums[j] < n and springs[i + nums[j]] in "?.":
                    score += arrs(i + nums[j] + 1, j + 1)
            else:
                assert j == m - 1
                score += arrs(i + nums[j], j + 1)

        return score

    return arrs(0, 0)


def solve(parsed):
    p1 = 0
    p2 = 0
    for springs, nums in parsed:
        p1 += dp(springs, nums)

        springs = "?".join(springs for _ in range(5))
        nums *= 5
        p2 += dp(springs, nums)

    return p1, p2


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = l.split()
        parsed.append((left, [int(x) for x in right.split(",")]))
    return parsed


def testp1p2():
    print()
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    parsed = parse(input_)
    assert solve(parsed) == (21, 525152)


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
