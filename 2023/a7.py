from collections import defaultdict
from pathlib import Path
import requests

YEAR = "2023"
DAY = "7"

#  A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
# first card from right


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


def classify(hand):
    counts = defaultdict(int)
    for card in hand:
        counts[card] += 1
    if max(counts.values()) == 5:
        return 7
    if max(counts.values()) == 4:
        return 6
    if any(v == 3 for v in counts.values()) and any(v == 2 for v in counts.values()):
        return 5
    if max(counts.values()) == 3:
        return 4
    if 2 == sum(1 for v in counts.values() if v == 2):
        return 3
    if max(counts.values()) == 2:
        return 2
    return 1


def classsify_maximize_by_joker(hand):
    BEST = hand
    cards_to_try = set(hand)
    cards_to_try.add("A")  # high card
    if "J" in hand:
        cards_to_try.remove("J")
    Q = [("", 0)]
    while Q:
        cur, sz = Q.pop()
        if sz == 5:
            if classify(cur) > classify(BEST):
                BEST = cur
            continue
        if hand[sz] == "J":
            for c in cards_to_try:
                Q.append((cur + c, sz + 1))
        else:
            Q.append((cur + hand[sz], sz + 1))
    return BEST


CARDS = {c: i for i, c in enumerate(reversed("AKQJT98765432"))}
CARDS_WITH_JOKER = {c: i for i, c in enumerate(reversed("AKQT98765432J"))}


def strength(hand, p2=False):
    if p2:
        return "".join([chr(ord("a") + CARDS_WITH_JOKER[c]) for c in hand])
    return "".join([chr(ord("a") + CARDS[c]) for c in hand])


def solve(parsed):
    classified = [(classify(hand), strength(hand), hand, bid) for hand, bid in parsed]
    classified.sort()
    p1 = 0
    for i, (_, _, _, bid) in enumerate(classified):
        p1 += bid * (i + 1)

    maximized_hands = [
        (classsify_maximize_by_joker(hand), hand, bid) for hand, bid in parsed
    ]
    classified = [
        (classify(max_hand), strength(hand, p2=True), max_hand, bid)
        for max_hand, hand, bid in maximized_hands
    ]
    classified.sort()
    p2 = 0
    for i, (_, _, _, bid) in enumerate(classified):
        p2 += bid * (i + 1)

    return p1, p2


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        hand, bid = l.split()
        bid = int(bid)
        parsed.append((hand, bid))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
    parsed = parse(input_)
    assert solve(parsed) == (6440, 5905)


def run():
    parsed = parse(getinput())
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
