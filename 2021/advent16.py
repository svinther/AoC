from functools import reduce
from pathlib import Path
from typing import NamedTuple, List, Union, Tuple

import pytest

DAY = 16
YEAR = 2021
full_input_ = Path(f"input.{YEAR}.{DAY}.txt").read_text()


class LiteralPacket(NamedTuple):
    pversion: int
    ptype: int
    data: int


class OperatorPacket(NamedTuple):
    pversion: int
    ptype: int
    lid: int
    subpackets: List[Union[LiteralPacket, "OperatorPacket"]]


def solve(parsed):
    pass


# 110100101111111000101000
# VVVTTTAAAAABBBBBCCCCC


def hex2bin(hexnumber: str):
    return "".join([bin(int(d, 16))[2:].zfill(4) for d in hexnumber])


def evaluate(packet: Union[LiteralPacket, "OperatorPacket"]) -> int:
    if isinstance(packet, LiteralPacket):
        return packet.data

    sub_evaluated: List[int] = [evaluate(s) for s in packet.subpackets]
    if packet.ptype == 0:  # sum
        return sum(sub_evaluated)

    if packet.ptype == 1:  # product
        return reduce(lambda a, b: a * b, sub_evaluated)

    if packet.ptype == 2:  # min
        return min(sub_evaluated)

    if packet.ptype == 3:  # max
        return max(sub_evaluated)

    if packet.ptype == 5:  # gt
        assert len(sub_evaluated) == 2
        l, r = sub_evaluated
        return 1 if l > r else 0

    if packet.ptype == 6:  # lt
        assert len(sub_evaluated) == 2
        l, r = sub_evaluated
        return 1 if l < r else 0

    if packet.ptype == 7:  # gt
        assert len(sub_evaluated) == 2
        l, r = sub_evaluated
        return 1 if l == r else 0

    assert False


def parse(input_: str) -> Tuple[Union[LiteralPacket, OperatorPacket], int]:
    input_ = input_.strip()
    V = int(input_[0:3], 2)
    T = int(input_[3:6], 2)

    i = 6
    if T == int("100", 2):
        # literal packet
        P = []
        while True:
            P_ = input_[i : i + 5]
            i += 5
            P.append(int(P_[1:], 2))
            if P_[0] == "0":
                break
        data = sum(
            [a * b for a, b in zip(reversed(P), [16**x for x in range(0, len(P))])]
        )
        return LiteralPacket(V, T, data), i
    else:  # if T == int("110", 2):
        # operator packet
        I = int(input_[i], 2)
        i += 1

        SUB_PACKETS_LENGTH, SUB_PACKETS_COUNT = None, None
        if I == 0:
            SUB_PACKETS_LENGTH = int(input_[i : i + 15], 2)
            i += 15
        elif I == 1:
            SUB_PACKETS_COUNT = int(input_[i : i + 11], 2)
            i += 11

        subpackets: List[Union[LiteralPacket, OperatorPacket]] = []
        i_ = i
        while (SUB_PACKETS_LENGTH and i < i_ + SUB_PACKETS_LENGTH) or (
            SUB_PACKETS_COUNT and len(subpackets) < SUB_PACKETS_COUNT
        ):
            p, l = parse(input_[i:])
            subpackets.append(p)
            i += l
        return OperatorPacket(V, T, I, subpackets), i


def test_simple_1():
    input_ = "110100101111111000101000"
    packet, i = parse(input_)
    assert isinstance(packet, LiteralPacket)
    assert packet.data == 2021


def test_operator_1():
    input_ = "00111000000000000110111101000101001010010001001000000000"
    packet, length = parse(input_)
    assert isinstance(packet, OperatorPacket)
    assert len(packet.subpackets) == 2
    sp1, sp2 = packet.subpackets
    assert isinstance(sp1, LiteralPacket)
    assert isinstance(sp2, LiteralPacket)
    assert sp1.data == 10
    assert sp2.data == 20


def test_operator2_1():
    input_ = "11101110000000001101010000001100100000100011000001100000"
    packet, length = parse(input_)
    assert isinstance(packet, OperatorPacket)
    assert len(packet.subpackets) == 3
    sp1, sp2, sp3 = packet.subpackets
    assert isinstance(sp1, LiteralPacket)
    assert isinstance(sp2, LiteralPacket)
    assert isinstance(sp3, LiteralPacket)
    assert sp1.data == 1
    assert sp2.data == 2
    assert sp3.data == 3


def calc_versionsum(packet: Union[LiteralPacket, OperatorPacket]):
    if isinstance(packet, LiteralPacket):
        return packet.pversion
    else:
        assert isinstance(packet, OperatorPacket)
        vsum = packet.pversion
        for p in packet.subpackets:
            vsum += calc_versionsum(p)
        return vsum


operator3_1_testdata = [
    ("8A004A801A8002F478", 16),
    ("620080001611562C8802118E34", 12),
    ("C0015000016115A2E0802F182340", 23),
    ("A0016C880162017C3686B18A3D4780", 31),
]


@pytest.mark.parametrize("hexinput,versionsum", operator3_1_testdata)
def test_operator3_1(hexinput: str, versionsum: int):
    input_ = hex2bin(hexinput)
    packet, length = parse(input_)
    assert calc_versionsum(packet) == versionsum


part2_testdata = [
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("CE00C43D881120", 9),
    ("D8005AC2A8F0", 1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1),
]


@pytest.mark.parametrize("hexinput,result", part2_testdata)
def test_part2(hexinput: str, result: int):
    binary = hex2bin(hexinput)
    packet, length = parse(binary)
    assert evaluate(packet) == result


if __name__ == "__main__":
    binary = hex2bin(full_input_)
    packet, length = parse(binary)
    print("p1", calc_versionsum(packet))
    print("p2", evaluate(packet))
