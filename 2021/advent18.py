import math
import re
from collections import deque, Counter
from copy import copy
from functools import reduce

year = 2021
day = 18

inputs = [
    """\
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""",
    """\
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""",
]

with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())


def explode(snum):
    # look for single digited pairs
    p = re.compile(r"\[(\d+),(\d+)]")

    # result = []
    searchpos = 0
    while True:
        m = re.search(p, snum[searchpos:])
        if m:
            pos = searchpos + m.start()
            endpos = searchpos + m.end()

            if Counter(snum[:pos])["["] - Counter(snum[:pos])["]"] == 4:
                explosion = snum[pos:endpos]
                left = snum[:pos]
                right = snum[endpos:]

                l, r = int(m.group(1)), int(m.group(2))
                # explode right
                m_num_right = re.search("\d+", right)
                if m_num_right:
                    newnum = str(int(m_num_right.group(0)) + r)
                    right = (
                        right[: m_num_right.start()]
                        + newnum
                        + right[m_num_right.end() :]
                    )

                # explode left
                m_num_left_iter = list(re.finditer("\d+", left))  # <-- reversed left
                if m_num_left_iter:
                    m_num_left = m_num_left_iter[-1]
                    newnum = str(int(m_num_left.group(0)) + l)
                    left = (
                        left[: m_num_left.start()] + newnum + left[m_num_left.end() :]
                    )

                return explosion, left + "0" + right
            else:
                searchpos = endpos
        else:
            return None, None


def splitit(snum):
    p = re.compile(r"\d{2,}")
    m = re.search(p, snum)
    if m:
        splitnum = int(m.group(0))
        pair = (math.floor(splitnum / 2), math.ceil(splitnum / 2))
        return snum[0 : m.start()] + f"[{pair[0]},{pair[1]}]" + snum[m.end() :]


def magnitude(snum):
    p = re.compile(r"\[(\d+),(\d+)]")
    result = snum
    while True:
        m = re.search(p, result)
        if m:
            l, r = int(m.group(1)), int(m.group(2))
            result = result[0 : m.start()] + str((l * 3 + r * 2)) + result[m.end() :]
        else:
            break

    return reduce(lambda a, b: a + b, [int(x) for x in re.findall("\d+", result)])


def snailsum(n1, n2):
    added_snums = f"[{n1},{n2}]"
    # print(f"reduce this: {added_snums}")

    result = added_snums
    while True:
        explosion, exploded = explode(result)
        splitted = None
        if explosion:
            # print(f"Explosion: {explosion}")
            # print(f"Exploded: {exploded}")
            result = exploded
        else:
            splitted = splitit(result)
            if splitted:
                # print(f"Splitted: {splitted}")
                result = splitted

        if not explosion and not splitted:
            break
    return result


def get_highest_combo_magnitude(snums):
    highscore = -1
    for i in range(len(snums)):
        for j in range(len(snums)):
            if i != j:
                summed = snailsum(snums[i], snums[j])
                magn = magnitude(summed)
                highscore = max(highscore, magn)
    return highscore


for num, data in enumerate(inputs, start=1):
    S = deque()

    for line in data.split("\n"):
        line = line.strip()
        if line:
            S.append(line)

    Original = copy(S)

    # print(S)
    while len(S) > 1:
        n1, n2 = (S.popleft(), S.popleft())

        # test = T.popleft()
        # if test != result:
        #     print("VAAARK")
        #     print(result)
        #     print(test)
        #     sys.exit()

        S.appendleft(snailsum(n1, n2))

    print(f"***** Result: {S[0]} - Magnitude: {magnitude(S[0])} *****")
    print(f"Best Combo magnitude: {get_highest_combo_magnitude(Original)} ")
