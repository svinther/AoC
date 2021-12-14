year = 2021
day = 2

inputs = ["""\
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""]

with open(f"input.{year}.{day}.txt", "r") as iopen:
    inputs.append(iopen.read())


def calculate_pos(commands):
    depth = 0
    hp = 0
    aim = 0
    for instruction, value in commands:
        if instruction == "down":
            aim += value
        elif instruction == "up":
            aim -= value
        elif instruction == "forward":
            hp += value
            depth += (aim * value)
        else:
            assert False
    return depth, hp


for num, data in enumerate(inputs, start=1):
    commands = []
    for line in data.split("\n"):
        stripped = line.strip()
        if stripped:
            command, value = stripped.split(" ")
            commands.append((command, int(value)))

    depth, hp = calculate_pos(commands)
    print(f"Data number {num}: {(depth, hp)} -> {depth * hp}")
