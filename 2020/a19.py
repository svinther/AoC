from itertools import product
from pathlib import Path

DAY = 19
full_input_ = Path(f"{DAY}.txt").read_text()


def combos(rules, num) -> set:
    rule_alts = rules[num]
    comb = set()
    for alt in rule_alts:
        if alt == "a" or alt == "b":
            comb.add(alt)
        else:
            # produce a list of string alternation sets [{"aa", "bb"}, {"ab", "ba"}, ..]
            recursive_combo = [combos(rules, n) for n in alt]
            for p in product(*recursive_combo):
                comb.add("".join(p))
    assert comb
    return comb


def test_combos():
    r = """\
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"    
"""
    rules = parse_rules(r)
    assert combos(rules, 1) == {"a"}
    assert combos(rules, 3) == {"b"}
    assert combos(rules, 2) == {"ab", "ba"}
    assert combos(rules, 0) == {"aab", "aba"}

    r = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""
    rules = parse_rules(r)
    assert combos(rules, 4) == {"a"}
    assert combos(rules, 5) == {"b"}
    combos2 = combos(rules, 2)
    combos3 = combos(rules, 3)
    combos1 = combos(rules, 1)
    assert combos1 == {"".join(p) for p in product(combos2, combos3)} | {
        "".join(p) for p in product(combos3, combos2)
    }


def verify(rules, pattern, gobble):
    if not pattern and not gobble:
        return True
    elif pattern and gobble:
        p = pattern[0]
        for combo in combos(rules, p):
            if gobble[: len(combo)] == combo:
                if verify(rules, pattern[1:], gobble[len(combo) :]):
                    return True
    return False


def test_verify():
    r = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
"""
    rules = parse_rules(r)
    assert verify(rules, [4], "a") is True
    assert verify(rules, [3], "ab") is True
    assert verify(rules, [3], "ba") is True
    assert verify(rules, [2], "aa") is True
    assert verify(rules, [2], "bb") is True
    assert verify(rules, [1], "aaab") is True
    assert verify(rules, [1], "abaa") is True
    assert verify(rules, [0], "ababbb") is True


def solve(parsed):
    rules, texts = parsed
    result = []
    for text in texts:
        result.append(verify(rules, rules[0][0], text))
    return len([x for x in result if x is True])


def readnums(expr):
    result = []
    for c in expr.split(" "):
        c = c.strip()
        if not c:
            continue
        result.append(int(c))
    return result


def parse_rules(chunk: str):
    rules = {}
    for l in chunk.split("\n"):
        l = l.strip()
        if not l:
            continue

        rulenum, expr = l.split(":")
        rulenum = int(rulenum)
        if '"' in expr:
            lit = [c for c in expr if c in {"a", "b"}]
            assert len(lit) == 1
            rules[rulenum] = lit
        elif "|" in expr:
            altleft, altright = expr.split("|")
            rules[rulenum] = [readnums(altleft), readnums(altright)]
        else:
            rules[rulenum] = [readnums(expr)]
    return rules


def parse(input: str):
    texts = []

    upper, lower = input.split("\n\n")

    rules = parse_rules(upper)

    for l in lower.split("\n"):
        l = l.strip()
        if not l:
            continue
        texts.append(l)

    return rules, texts


def testp1():
    print()
    input_ = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""
    parsed = parse(input_)
    result = solve(parsed)
    assert result == 2


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)
