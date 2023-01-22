from itertools import combinations, product

shop = """\
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

# input
b_damage = 8
b_armor = 1
b_hp = 104


def parse_chunk(chunk):
    return tuple(
        (c, d, a)
        for c, d, a in [
            map(int, [i for i in l.split(" ") if i][-3:])
            for l in chunk.split("\n")[1:]
            if l
        ]
    )


W, A, R = [parse_chunk(chunk) for chunk in shop.split("\n\n")]

# combos
Wc = [[w] for w in W]
Ac = [[(0, 0, 0)]] + [[a] for a in A]
Rc = (
    [[(0, 0, 0)]]
    + [list(c) for c in combinations(R, 1)]
    + [list(c) for c in combinations(R, 2)]
)


best = 10**9
worst = 0
for wc, ac, rc in product(Wc, Ac, Rc):
    cost = sum(w[0] for w in wc) + sum(a[0] for a in ac) + sum(r[0] for r in rc)
    d = sum(w[1] for w in wc) + sum(a[1] for a in ac) + sum(r[1] for r in rc)
    a = sum(w[2] for w in wc) + sum(a[2] for a in ac) + sum(r[2] for r in rc)

    p = 100
    b = b_hp

    while True:
        b -= max(1, d - b_armor)
        if b <= 0:
            best = min(best, cost)
            break
        p -= max(1, b_damage - a)
        if p <= 0:
            worst = max(cost, worst)
            break


print(best)
print(worst)
