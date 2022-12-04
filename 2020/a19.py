from itertools import product
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


def gobble_(
    rules: Dict[int, Union[LiteralNode, RuleReferenceNode, AlternateNode]],
    rule: Union[LiteralNode, RuleReferenceNode, AlternateNode],
    text: list,
) -> bool:
    if isinstance(rule, LiteralNode):
        if text[0] == rule.value:
            text.pop(0)
            return True
        return False
    elif isinstance(rule, RuleReferenceNode):
        for rr in rule.rulerefs:
            if not gobble_(rules, rules[rr], text):
                return False
        return True
    elif isinstance(rule, AlternateNode):
        for an in rule.left, rule.right:
            text_ = text.copy()
            if gobble_(rules, an, text_):
                text.clear()
                text.extend(text_)
                return True
        return False
    else:
        assert False


def gobble(
    rules: Dict[int, Union[LiteralNode, RuleReferenceNode, AlternateNode]],
    rule: Union[LiteralNode, RuleReferenceNode, AlternateNode],
    text: list,
) -> bool:
    result = gobble_(rules, rule, text)
    return result and len(text) == 0


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
    assert gobble(rules, rules[4], list("a")) is True
    assert gobble(rules, rules[4], list("b")) is False
    assert gobble(rules, rules[4], list("aa")) is False

    assert gobble(rules, rules[3], list("ab")) is True
    assert gobble(rules, rules[3], list("ba")) is True
    assert gobble(rules, rules[2], list("aa")) is True
    assert gobble(rules, rules[2], list("bb")) is True
    assert gobble(rules, rules[1], list("aaab")) is True
    assert gobble(rules, rules[1], list("abaa")) is True
    assert gobble(rules, rules[0], list("ababbb")) is True


def solvep1(parsed):
    rules, texts = parsed
    result = []
    for text in texts:
        result.append(gobble(rules, rules[0], list(text)))
    return len([x for x in result if x is True])


def solvep2(parsed):
    rules, texts = parsed
    rules[8] = AlternateNode(RuleReferenceNode([42]), RuleReferenceNode([42, 8]))
    rules[11] = AlternateNode(
        RuleReferenceNode([42, 31]), RuleReferenceNode([42, 11, 31])
    )
    result = []
    for text in texts:
        result.append(gobble(rules, rules[0], list(text)))
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


if __name__ == "__main__":
    parsed = parse(full_input_)
    result = solvep1(parsed)
    print(result)

    result = solvep2(parsed)
    print(result)
