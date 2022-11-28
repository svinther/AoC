from itertools import permutations
from pathlib import Path
from typing import Dict, Tuple, List, Set, NamedTuple

#  aaa
# b   c
# b   c
#  ddd
# e   f
# e   f
#  ggg

SEGSUSED = {
    0: frozenset("abcefg"),
    1: frozenset("cf"),
    2: frozenset("acdeg"),  # uniq count
    3: frozenset("acdfg"),
    4: frozenset("bcdf"),  # uniq count
    5: frozenset("abdfg"),
    6: frozenset("abdefg"),
    7: frozenset("acf"),  # uniq count
    8: frozenset("abcdefg"),  # uniq count
    9: frozenset("abcdfg"),
}

SEGUSED_INV = {v: k for k, v in SEGSUSED.items()}

Combinations = Tuple[frozenset]
Readings = Tuple[frozenset]


class DisplayNote(NamedTuple):
    combinations: Combinations
    readings: Readings


Possible = Dict[int, List[Set[str]]]


def solve_part1(D: List[DisplayNote]):
    result = 0
    for displaynote in D:
        for r in displaynote.readings:
            possible_digits = set()
            for digit, segsused in SEGSUSED.items():
                if len(r) == len(segsused):
                    possible_digits.add(digit)
            if len(possible_digits) == 1:
                result += 1
    return result


def solve_part2(D: DisplayNote):
    combinations, readings = D

    # try all combinations of wirings and see if we can recognize all 10 real digits
    for w0 in permutations(list("abcdefg"), 7):
        for w1 in permutations(list("abcdefg"), 7):
            # wiring to try
            wiring = {dest: src for src, dest in zip(w0, w1)}

            # T is the dictionary with all 10 digit translations (if wiring is correct)
            T: Dict[frozenset, int] = {}
            for word in combinations:
                translated = frozenset(wiring[c] for c in word)
                if translated in SEGUSED_INV:
                    assert word not in T
                    T[word] = SEGUSED_INV[translated]
                else:
                    break
            if len(T) == 10:
                return int("".join([str(T[r]) for r in readings]))


def parse(input_: str) -> List[DisplayNote]:
    result: List[DisplayNote] = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue

        combinations_list, readings_list = l.split("|")
        combinations: List[str] = [
            c.strip() for c in combinations_list.split(" ") if c.strip()
        ]
        readings: List[str] = [r.strip() for r in readings_list.split(" ") if r.strip()]
        result.append(
            DisplayNote(
                tuple(frozenset(c) for c in combinations),
                tuple(frozenset(r) for r in readings),
            )
        )
    return result


def test_simple_2():
    input_ = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    displaynotes = parse(input_)
    assert 5353 == solve_part2(displaynotes[0])


def test_long_2():
    input_ = """\
    be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce    
"""
    displaynotes = parse(input_)
    assert 61229 == sum([solve_part2(dn) for dn in displaynotes])


def test_simple_1():
    input_ = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce    
"""
    displaynotes = parse(input_)
    assert len(displaynotes) == 10
    assert len(displaynotes[0].combinations) == 10
    assert len(displaynotes[0].readings) == 4
    assert len(displaynotes[0].combinations[0]) == 2
    assert len(displaynotes[0].readings[0]) == 7

    assert solve_part1(displaynotes) == 26


if __name__ == "__main__":
    input_ = Path("input.2021.8.txt").read_text()
    displaynotes = parse(input_)
    result = sum([solve_part2(dn) for dn in displaynotes])
    print(result)
