from functools import reduce

year = 2021
day = 1

inputs = [
    """\
199
200
208
210
200
207
240
269
260
263
"""
]

with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())


def calculate_increases(samples):
    score = 0
    last = None
    for i in range(0, len(samples) - len(samples) % 3):
        bucket = samples[i : i + 3]
        bucket_sum = reduce(lambda a, b: a + b, bucket)
        if i > 0 and bucket_sum > last:
            score += 1
        last = bucket_sum
    return score


for num, data in enumerate(inputs, start=1):
    samples = [int(line.strip()) for line in data.split("\n") if line.strip()]
    print(f"Data number {num}: {calculate_increases(samples)}")
