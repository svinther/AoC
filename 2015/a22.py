from functools import lru_cache
from typing import NamedTuple

player = 50
mana = 500

boss = 58
boss_damage = 9


class Effect(NamedTuple):
    manacost: int
    turns: int
    damage: int = 0
    heal: int = 0
    armor: int = 0
    mana: int = 0


P = [
    # Effect(53, damage=4),
    # Effect(73, damage=2, heal=2),
    Effect(113, 6, armor=7),
    Effect(173, 6, damage=3),
    Effect(229, 5, mana=101),
]


# turn, effects (3xint), boss, player, mana, spent
@lru_cache(maxsize=None)
def solve(t, A, b, p, m, s):
    if t % 2 == 0 and difficulty == "hard":
        p -= 1

    if p <= 0:
        return 10**9
    if b <= 0:
        return s

    armor = 0
    for i, e in enumerate(P):
        if A[i] > 0:
            b -= e.damage
            m += e.mana
            armor += e.armor
    A = tuple(max(0, a - 1) for a in A)

    if t % 2 == 0:
        scores = []

        # Magic Missile
        if m >= 53:
            scores.append(solve(t + 1, A, b - 4, p, m - 53, s + 53))
        # Drain
        if m >= 73:
            scores.append(solve(t + 1, A, b - 2, p + 2, m - 73, s + 73))

        # Shield, Poison, Recharge
        for i, e in enumerate(P):
            if m >= e.manacost and A[i] <= 0:
                A_ = tuple(A[j] if j != i else e.turns for j in range(len(A)))
                scores.append(solve(t + 1, A_, b, p, m - e.manacost, s + e.manacost))

        if not scores:
            # do nothing
            scores.append(solve(t + 1, A, b, p, m, s))

        return min(scores)
    else:
        return solve(t + 1, A, b, p - max(1, boss_damage - armor), m, s)


difficulty = "easy"
result = solve(0, (0, 0, 0), boss, player, mana, 0)
print(result, difficulty)
solve.cache_clear()
difficulty = "hard"
result = solve(0, (0, 0, 0), boss, player, mana, 0)
print(result, difficulty)
