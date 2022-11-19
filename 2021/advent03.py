year = 2021
day = 3

inputs = [
    """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""
]

with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())


def count_ones(lines, pos):
    ones = 0
    for line in lines:
        if list(line)[pos] == "1":
            ones += 1
    return ones


#
# def map_ones(lines):
#     ones = {}
#     for line in lines:
#         for n, c in enumerate(list(line)):
#             if c == "1":
#                 ones[n] = ones.get(n, 0) + 1
#     return ones


def reduce_to_single(lines, pos, most_common=True):
    ones = count_ones(lines, pos)
    zeros = len(lines) - ones

    if most_common:
        if ones >= zeros:
            keepers = "1"
        else:
            keepers = "0"
    else:
        if zeros <= ones:
            keepers = "0"
        else:
            keepers = "1"

    reduced = [line for line in lines if line[pos] == keepers]

    if len(reduced) == 1:
        return reduced[0]

    return reduce_to_single(reduced, pos + 1, most_common)


for num, data in enumerate(inputs, start=1):
    all_lines = []

    for line in data.split("\n"):
        stripped = line.strip()
        if stripped:
            all_lines.append(list(stripped))

    oxy = reduce_to_single(all_lines.copy(), 0, True)
    co2 = reduce_to_single(all_lines.copy(), 0, False)

    oxy_int = int("".join(oxy), 2)
    co2_int = int("".join(co2), 2)

    print(f"Num {num}: oxy: {oxy_int} co2: {co2_int} - result: {oxy_int * co2_int}")
