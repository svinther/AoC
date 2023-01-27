pk1 = 1965712
pk2 = 19072108

magicvalue = 20201227


def find_ls(sn, pk):
    n = 1
    ls = 0
    while n != pk:
        n = (n * sn) % magicvalue
        ls += 1
    return ls


def transform(sn, ls):
    n = 1
    for _ in range(ls):
        n = (n * sn) % magicvalue
    return n


def testex():
    assert find_ls(7, 17807724) == 11
    assert find_ls(7, 5764801) == 8

    key1 = transform(17807724, 8)
    key2 = transform(5764801, 11)
    assert key1 == key2


if __name__ == "__main__":
    pk1_ls = find_ls(7, pk1)
    pk2_ls = find_ls(7, pk2)

    key1 = transform(pk1, pk2_ls)
    key2 = transform(pk2, pk1_ls)
    assert key1 == key2
    print(key1)
