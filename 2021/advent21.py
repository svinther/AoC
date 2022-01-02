import sys
from collections import defaultdict


def paths21(pos, base, score, result):
    for roll in range(3, 9 + 1):
        base_ = base + (roll,)
        pos_ = (pos + roll - 1) % 10 + 1
        score_ = score + pos_
        if score_ >= 21:
            result[len(base_)].add(base_)
        else:
            paths21(pos_, base_, score_, result)


p1paths = defaultdict(set)
paths21(4, tuple(), 0, p1paths)
p2paths = defaultdict(set)
paths21(8, tuple(), 0, p2paths)

p1_universes = 0
p2_universes = 0
for rollcount in p1paths.keys() | p2paths.keys():
    p1wins = len(p1paths[rollcount])
    p2wins = len(p2paths[rollcount] - p1paths[rollcount])  # p1 wins first
    print(rollcount, p1wins, p2wins)
    p1_universes += p1wins * (7 ** rollcount - p2wins) * (3 ** rollcount)
    p2_universes += p2wins * (7 ** rollcount - p1wins) * (3 ** rollcount)

print(p1_universes, p2_universes)

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
