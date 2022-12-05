from pathlib import Path
from typing import NamedTuple, List, Dict, Union

DAY = 19
full_input_ = Path(f"{DAY}.txt").read_text()


class LiteralNode(NamedTuple):
    value: str


class RuleReferenceNode(NamedTuple):
    rulerefs: List[int]


class AlternateNode(NamedTuple):
    left: RuleReferenceNode
    right: RuleReferenceNode


def gobble(
    rules: Dict[int, Union[LiteralNode, RuleReferenceNode, AlternateNode]],
    rulestack: List[Union[LiteralNode, RuleReferenceNode, AlternateNode]],
    text: str,
) -> bool:
    if len(rulestack) == 0 or len(text) == 0:
        return len(rulestack) == 0 and len(text) == 0

    rule = rulestack.pop()

    if isinstance(rule, LiteralNode):
        if text[0] == rule.value:
            return gobble(rules, rulestack, text[1:])
    elif isinstance(rule, RuleReferenceNode):
        rulestack.extend(reversed([rules[rr] for rr in rule.rulerefs]))
        return gobble(rules, rulestack, text)
    elif isinstance(rule, AlternateNode):
        for an in (rule.left, rule.right):
            if gobble(rules, rulestack + [an], text):
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
    assert gobble(rules, [rules[4]], "a") is True
    assert gobble(rules, [rules[4]], "b") is False
    assert gobble(rules, [rules[4]], "aa") is False
    assert gobble(rules, [rules[3]], "ab") is True
    assert gobble(rules, [rules[3]], "ba") is True
    assert gobble(rules, [rules[2]], "aa") is True
    assert gobble(rules, [rules[2]], "bb") is True
    assert gobble(rules, [rules[1]], "aaab") is True
    assert gobble(rules, [rules[1]], "abaa") is True
    assert gobble(rules, [rules[0]], "ababbb") is True


def solvep1(parsed):
    rules, texts = parsed
    result = []
    for text in texts:
        result.append(gobble(rules, [rules[0]], text))
    return len([x for x in result if x is True])


def solvep2(parsed):
    rules, texts = parsed
    rules[8] = AlternateNode(RuleReferenceNode([42]), RuleReferenceNode([42, 8]))
    rules[11] = AlternateNode(
        RuleReferenceNode([42, 31]), RuleReferenceNode([42, 11, 31])
    )
    result = []
    for text in texts:
        result.append(gobble(rules, [rules[0]], text))
    return len([x for x in result if x is True])


def readnums(expr) -> List[int]:
    result = []
    for c in expr.split(" "):
        c = c.strip()
        if not c:
            continue
        result.append(int(c))
    return result


def parse_rules(chunk: str):
    rules: Dict[int, Union[LiteralNode, RuleReferenceNode, AlternateNode]] = {}
    for l in chunk.split("\n"):
        l = l.strip()
        if not l:
            continue

        rulenum, expr = l.split(":")
        rulenum = int(rulenum)
        if '"' in expr:
            lit = [c for c in expr if c in {"a", "b"}]
            assert len(lit) == 1
            rules[rulenum] = LiteralNode(lit[0])
        elif "|" in expr:
            altleft, altright = expr.split("|")
            left = RuleReferenceNode(readnums(altleft))
            right = RuleReferenceNode(readnums(altright))
            rules[rulenum] = AlternateNode(left, right)
        else:
            rules[rulenum] = RuleReferenceNode(readnums(expr))
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
    result = solvep1(parsed)
    assert result == 2


def test_p2():
    input_ = """\
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1
"""
    rules = parse_rules(input_)
    assert solvep2((rules, ["bbabbbbaabaabba"]))
    assert solvep2((rules, ["aaabbbbbbaaaabaababaabababbabaaabbababababaaa"]))
    assert solvep2((rules, ["ababaaaaaabaaab"]))
    assert solvep2((rules, ["ababaaaaabbbaba"]))
    assert solvep2((rules, ["baabbaaaabbaaaababbaababb"]))
    assert solvep2((rules, ["abbbbabbbbaaaababbbbbbaaaababb"]))
    assert solvep2((rules, ["aaaaabbaabaaaaababaa"]))
    assert solvep2((rules, ["aaaabbaabbaaaaaaabbbabbbaaabbaabaaa"]))
    assert solvep2((rules, ["aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"]))
    assert solvep2((rules, ["babbbbaabbbbbabbbbbbaabaaabaaa"]))
    assert solvep2((rules, ["bbbbbbbaaaabbbbaaabbabaaa"]))
    assert solvep2((rules, ["bbbababbbbaaaaaaaabbababaaababaabab"]))


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)
