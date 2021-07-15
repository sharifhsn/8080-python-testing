import sys
rom = ""
j = 0
k = 0
file_names = sys.argv[2:]
for file_name in file_names:
    with open(file_name, "rb") as file:
        file_content = file.read()
    for i in range(len(file_content)):
        rom += "{}: 0x{:02X}\n".format(i + j, file_content[i])
    j += len(file_content)
with open(sys.argv[1], "w") as file:
    file.write(rom)