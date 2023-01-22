mu = 252533
mod = 33554393

r, c = 2, 1
last = 20151125
maxr = 2
while True:
    last = (last * mu) % mod
    if (r, c) == (2947, 3029):
        break

    c += 1
    r -= 1
    if r == 0:
        c = 1
        r = maxr = maxr + 1

print(last)
