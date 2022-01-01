year = 2021
day = 20

# with open(f"ex.{year}.{day}.txt", "r") as iopen:
#     data = iopen.read()
with open(f"input.{year}.{day}.txt", "r") as iopen:
    data = iopen.read()


def enhance(img, iea, i):
    pad = '.' if i % 2 == 0 else '#'
    # Raw input image width, now surround with extra layer of dark pixels
    WRAW = img.find("\n")
    W = WRAW + 2
    input_img = []
    input_img.append(list(pad * W))
    for l in img.split("\n"):
        l = l.strip()
        if l:
            input_img.append([pad] + list(l) + [pad])
    input_img.append(list(pad * W))

    bit9_strings = []
    bit9_decimals = []

    for y in range(len(input_img)):
        for x in range(len(input_img[y])):
            pix3x3_str = []
            for x_, y_ in [
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
            ]:
                if x_ < 0 or x_ >= len(input_img[y]) or y_ < 0 or y_ >= len(input_img):
                    pix3x3_str.append(pad)
                else:
                    pix3x3_str.append(input_img[y_][x_])
            bit9_strings.append(pix3x3_str)

            pix3x3_dec = 0
            for i, c in enumerate(reversed(pix3x3_str)):
                if c == "#":
                    pix3x3_dec += 2 ** i
            bit9_decimals.append(pix3x3_dec)

    outputimg = []
    for i, d in enumerate(bit9_decimals):
        if i > 0 and i % W == 0:
            outputimg.append("\n")
        outputimg.append(iea[d])
    outputimg.append("\n")
    return ''.join(outputimg)


# image enhancement algorithm and input image
iea_raw, input_img_raw = data.split("\n\n")
IEA = list("".join(iea_raw.split("\n")))

outputs = [input_img_raw]
for i in range(50):
    outputs.append(enhance(outputs[-1], IEA, i))

for i, output in enumerate(outputs):
    print(output)
    print("Output", i, "W=", output.find('\n'), "H=", output.count("\n"))
    print(output.count("#"))
