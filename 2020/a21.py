from collections import defaultdict
from pathlib import Path

DAY = "21"
full_input_ = Path(f"{DAY}.txt").read_text()


def solve(parsed):
    # index foods by allergen
    FOOD_A = defaultdict(set)
    for n, (ingr, allegs) in enumerate(parsed):
        for a in allegs:
            FOOD_A[a].add(n)

    i_a = {}
    a_i = {}

    foundnew = True
    while foundnew:
        foundnew = False
        for a, foods in FOOD_A.items():
            if a in a_i:
                continue
            Ti = set.intersection(*[parsed[n][0] for n in foods]) - i_a.keys()
            if len(Ti) == 1:
                i = Ti.pop()
                i_a[i] = a
                a_i[a] = i
                foundnew = True

    p1 = 0
    for ingrs, allegs in parsed:
        if not allegs - a_i.keys():
            p1 += len(ingrs - i_a.keys())

    sortable = [(a, i) for a, i in a_i.items()]
    sortable.sort()
    p2 = ",".join([i for a, i in sortable])

    return p1, p2


def parse(input_: str):
    parsed = []
    for l in input_.split("\n"):
        l = l.strip()
        if not l:
            continue
        left, right = l.split("(")
        ingrs = [i.strip() for i in left.split() if i.strip()]
        allegs = [a.strip(" ,)") for a in right.split()][1:]
        parsed.append((set(ingrs), set(allegs)))
    return parsed


def testp1p2():
    # input_=Path(f"{DAY}ex.txt").read_text()
    input_ = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""
    parsed = parse(input_)
    assert solve(parsed) == (5, "mxmxvkd,sqjhc,fvjkl")


def run():
    parsed = parse(full_input_)
    result = solve(parsed)
    print(result)


if __name__ == "__main__":
    run()
