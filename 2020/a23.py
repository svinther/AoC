def render(L, start=1):
    result = [start]
    cur = start
    while True:
        nxt = L[cur]
        if nxt == start:
            break
        result.append(nxt)
        cur = nxt

    return result


def solve(cups, turns):
    minc = min(cups)
    maxc = max(cups)
    L = [-1 for _ in range(maxc + 1)]
    for i in range(len(cups) - 1):
        L[cups[i]] = cups[i + 1]
    L[cups[-1]] = cups[0]
    cur = cups[0]
    for t in range(turns):
        # print("-- move", t+1, "--")
        # print("cups:", render(L, start=cur))
        out = [L[cur]]
        out.append(L[out[-1]])
        out.append(L[out[-1]])
        # print("pick up:", out)
        dest = cur - 1
        while dest in out or dest < minc:
            dest -= 1
            if dest < minc:
                dest = maxc
        # print("destination:", dest)
        L[cur] = L[out[-1]]
        L[out[-1]] = L[dest]
        L[dest] = out[0]
        cur = L[cur]

    return render(L, 1)


def test_p1():
    cups = "389125467"
    cups = list(map(int, list(cups)))
    p1_10 = solve(cups, 10)
    assert "92658374" == ("".join(map(str, p1_10[1:])))

    p1_100 = solve(cups, 100)
    assert "67384529" == ("".join(map(str, p1_100[1:])))


def test_p2():
    cups = "389125467"
    cups = list(map(int, list(cups)))
    cups.extend(range(max(cups) + 1, 1000000 + 1))
    p2 = solve(cups, 10000000)
    assert 149245887792 == (p2[1] * p2[2])


if __name__ == "__main__":
    cups = "872495136"
    cups = list(map(int, list(cups)))
    p1 = solve(cups, 100)
    print("".join(map(str, p1[1:])))

    cups.extend(range(max(cups) + 1, 1000000 + 1))
    p2 = solve(cups, 10000000)
    print(p2[1] * p2[2])
