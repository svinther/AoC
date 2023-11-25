import sys
from functools import cache
from itertools import product


# inspired/stolen from https://www.youtube.com/watch?v=a6ZdJEntKkk&ab_channel=JonathanPaulson
@cache
def paths21(p1, p2, s1, s2):
    if s1 >= 21:
        return (1, 0)
    if s2 >= 21:
        return (0, 1)
    ans = (0, 0)
    for rolls in product(range(1, 3 + 1), repeat=3):
        p1_ = (p1 + sum(rolls)) % 10
        s1_ = s1 + p1_ + 1
        ans_ = paths21(p2, p1_, s2, s1_)
        ans = (ans[0] + ans_[1], ans[1] + ans_[0])
    return ans


print(paths21(4 - 1, 8 - 1, 0, 0))
print(paths21(1 - 1, 5 - 1, 0, 0))

sys.exit(0)
# part 1
p1 = [(4, 0)]
p2 = [(8, 0)]
# p1=[(1,0)]
# p2=[(5,0)]

D = enumerate(cycle(range(1, 100 + 1)), 1)


def game_ended():
    return p1[-1][1] >= 1000 or p2[-1][1] >= 1000


winner = None
looser = None
while not game_ended():
    for i, p in enumerate((p1, p2)):
        last = p[-1]
        rolls = [(ri, r) for ri, r in (next(D) for _ in range(3))]
        roll = sum(r[1] for r in rolls)
        pos = (last[0] - 1 + roll) % 10 + 1
        score = last[1] + pos
        p.append((pos, score))
        print(i + 1, rolls, roll, pos, score)
        if game_ended():
            break
    if p1[-1][1] > p2[-1][1]:
        winner = p1
        looser = p2
    elif p2[-1][1] > p1[-1][1]:
        winner = p2
        looser = p1
    else:
        winner = None
        looser = None

print(looser[-1][1] * (len(p1) + len(p2) - 2) * 3)
