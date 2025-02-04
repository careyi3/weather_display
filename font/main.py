import pprint
from PIL import Image

im = Image.open("fira_code.png") # Change file name to desired font
im = im.convert("L")
pix = im.load()

start = 32
chars = {}

for y in range(0, 6):
    for x in range(0, 16):
        bits = []
        for by in range(0, 16):
            line = []
            for bx in range(0, 16):
                cx = bx + (x * 16)
                cy = by + (y * 16)

                if pix[cx, cy] == 0:
                    line.append("0")
                else:
                    line.append("1")
            bits.append("".join(line))

        char_idx = start + (y * 16) + x

        binary = []
        for b in bits:
            binary.append([hex(int(b[i : i + 8], 2)) for i in range(0, len(b), 8)])

        chars[char_idx] = binary

pprint.pp(chars)
