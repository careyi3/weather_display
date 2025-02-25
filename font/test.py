from fira_code import FONT


f = open("./letters.txt", "w")
for i in range(32, 128):
    f.write("\n")
    f.write("Character: ")
    f.write(chr(i))
    f.write("\n")
    f.write("\n")
    for line in FONT[i]:
        bytes = bytearray([int(b, 0) for b in line])
        bits = "".join([bin(byte)[2:].zfill(8) for byte in bytes])
        for bit in bits:
            if bit == "0":
                f.write(". ")
            else:
                f.write("# ")
        f.write("\n")

f.close()
