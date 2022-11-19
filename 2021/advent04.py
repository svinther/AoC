from collections import defaultdict
from functools import reduce

year = 2021
day = 4

inputs = [
    """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""
]


with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())

ROWSIZE = 5
COLSIZE = 5


def get_rows(board):
    return [
        board[n * ROWSIZE : n * ROWSIZE + ROWSIZE]
        for n in range(0, len(board) // ROWSIZE)
    ]


def get_cols(board):
    d = defaultdict(list)
    for n in range(0, len(board)):
        d[n % ROWSIZE].append(board[n])
    return [v for k, v in sorted(d.items())]


def visualize_board(board):
    for row in get_rows(board):
        print(" ".join([str(i) for i in row]))


def get_winner(boards, announced):
    for n in range(0, len(boards)):
        board, rows, cols = boards[n]
        for stripe in rows + cols:
            if stripe <= announced:
                del boards[n]
                return board


for num, data in enumerate(inputs, start=1):
    B = []
    S = None

    current_board = []
    for line in data.split("\n"):
        stripped = line.strip()
        if not S:
            S = [int(c) for c in line.split(",")]
        elif stripped:
            board_row = [int(n) for n in line.split(" ") if n]
            current_board.extend(board_row)
        elif current_board:
            B.append(
                (
                    current_board,
                    [set(r) for r in get_rows(current_board)],
                    [set(c) for c in get_cols(current_board)],
                )
            )
            current_board = []

    announced = set()
    for num in S:
        announced.add(num)

        last_winner = None
        while True:
            winner = get_winner(B, announced)
            if winner:
                last_winner = winner
            else:
                break

        if len(B) == 0:
            visualize_board(last_winner)
            print(num)
            unmarked = set(last_winner) - announced
            unmarked_sum = reduce(lambda a, b: a + b, unmarked)
            print(f"Unmarked sum: {unmarked_sum} -> Final score {unmarked_sum * num}")
            break
